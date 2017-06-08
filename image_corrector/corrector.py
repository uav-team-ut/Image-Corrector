from datetime import datetime
import json
from math import pi
import os
from threading import Thread
from time import sleep, time

import requests

from .image import AerialImage, Position


class Corrector(object):
    ASPECT_RATIO = 16 / 9
    HORIZ_FOV = 1.1693705988

    def __init__(self, flight_view_url, image_folder=None):
        if not image_folder:
            image_folder = os.path.expanduser('~') + '/Image Corrector Images'

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

            print('Created new file \'{}\'.'.format(image_folder))

        if not os.path.exists(image_folder + '/new'):
            os.makedirs(image_folder + '/new')

        if not os.path.exists(image_folder + '/current'):
            os.makedirs(image_folder + '/current')

        if not os.path.exists(image_folder + '/archive'):
            os.makedirs(image_folder + '/archive')

        self._flight_view_url = 'http://' + flight_view_url;
        self._image_folder = image_folder
        self._image_list = []
        self._closed = False

        self._d_time = 0

        self._empty_images()

        self._archive_name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

        if not os.path.exists(self.image_folder + '/archive/' + \
                self.archive_name):
            os.makedirs(self.image_folder + '/archive/' + self.archive_name)

        self._start_thread()

    def _start_thread(self):
        def corrector_thread():
            r = requests.get(self._flight_view_url + '/api/time', timeout=None)

            self.set_time(float(r.text))

            while not self._closed:
                new_files = self._get_new_files()

                for new_file in new_files:
                    time = self._d_time + os.path.getmtime(
                        self.image_folder + '/new/' + new_file
                    )

                    image = AerialImage(self, new_file)
                    self.add_image(image)

                sleep(0.1)

        self._corrector_thread = Thread(target=corrector_thread)
        self._corrector_thread.start()

    def _get_new_files(self):

        files = []

        for file in os.listdir(self.image_folder + '/new'):
            if file.endswith('.png'):
                files.append(file)

        return files

    def _empty_images(self):

        # Delete /current/*
        for f in os.listdir(self.image_folder + '/current/'):
            os.remove(self.image_folder + '/current/' + f)

        # Remove empty dirs in archive (LBYL style)
        for f in os.listdir(self.image_folder + '/archive/'):
            folder = self.image_folder + '/archive/' + f
            # If folder is empty, remove. Leave files alone.
            if os.path.isdir(folder) and not os.listdir(folder):
                os.rmdir(folder)

    def add_image(self, image):
        r_t = requests.get(
            self._flight_view_url + '/api/telemetry/' + str(
                time() + self._d_time),
            timeout=None
        )

        telemetry = r_t.json()

        position = Position(
            lat=telemetry['lat'],
            lon=telemetry['lon'],
            alt=telemetry['alt'],
            yaw=telemetry['yaw'],
            pitch=telemetry['pitch'],
            roll=telemetry['roll'],
            cam_pitch=telemetry['cam_pitch'],
            cam_roll=telemetry['cam_roll']
        )

        did_warp = image.set_position(position)
        r = None

        if did_warp:
            unwarped_json = image.to_json()
            warped_json = image.to_json(True)

            image_json = warped_json
            image_json['data_original'] = unwarped_json['data_original']

            r = requests.post(
                self._flight_view_url + '/api/images/',
                json=image_json,
                timeout=None
            )
        else:
            r = requests.post(
                self._flight_view_url + '/api/images',
                json=image.to_json(),
                timeout=None
            )

        if r.status_code != 200 and r.status_code != 201:
            print('Got a bad status code while sending image: ' +
                    str(r.status_code))

        self.image_list.append(image)

    def set_time(self, new_time):
        self._d_time = new_time - time()

    @property
    def archive_name(self):
        return self._archive_name

    @property
    def image_folder(self):
        return self._image_folder

    @property
    def image_list(self):
        return self._image_list

    @property
    def image_count(self):
        return len(self.image_list)

    def close(self):
        self._closed = True
        self._client.close()
