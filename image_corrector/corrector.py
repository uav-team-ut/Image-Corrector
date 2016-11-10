from datetime import datetime
import json
from math import pi
import os
from threading import Thread
from time import sleep, time

from .client import Client
from .image import AerialImage


class Corrector:

    ASPECT_RATIO = 16 / 9
    HORIZ_FOV = pi / 6

    def __init__(self, image_folder=None):
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

        self._image_folder = image_folder
        self._image_list = []
        self._closed = False

        self._d_time = 0

        self._empty_images()

        self._archive_name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

        if not os.path.exists(self.image_folder + '/archive/' + \
                self.archive_name):
            os.makedirs(self.image_folder + '/archive/' + self.archive_name)

        self._client = Client(self)

        self._start_thread()

    def _start_thread(self):
        def corrector_thread():
            while not self._closed:
                new_files = self._get_new_files()

                for new_file in new_files:
                    time = self._d_time + os.path.getmtime(
                        self.image_folder + '/new/' + new_file
                    )

                    image = AerialImage(self, new_file)
                    self.add_image(image)

                    alert = json.dumps({
                        'type': 'image',
                        'message': {
                            'type': 'alert',
                            'format': 'original',
                            'number': self.image_count,
                            'status': 'available'
                        }
                    })

                    request = json.dumps({
                        'type': 'telemetry',
                        'message': {
                            'type': 'image-request',
                            'time': time,
                            'number': self.image_count
                        }
                    })

                    self._client.send(alert)
                    self._client.send(request)

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
        self.image_list.append(image)

    def set_time(self, time):
        self._d_time = time - time()

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
