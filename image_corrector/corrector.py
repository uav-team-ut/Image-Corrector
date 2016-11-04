from datetime import datetime
import json
from math import pi
import os
from threading import Thread
from time import sleep

from .client import Client
from .image import AerialImage


class Corrector:

    ASPECT_RATIO = 16 / 9
    HORIZ_FOV = pi / 6

    def __init__(self, image_folder=None):
        if not image_folder:
            image_folder = os.path.expanduser('~') + '/Image Corrector'

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

            print('Created new file \'{}\'.'.format(image_folder))

        if not os.path.exists(image_folder + '/new'):
            os.makedirs(image_folder + '/new')

        if not os.path.exists(image_folder + '/current'):
            os.makedirs(image_folder + '/current')

        self._image_folder = image_folder
        self._image_list = []
        self._closed = False

        self._archive_name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        newpath = r'C:\Program Files\arbitrary'
        if not os.path.exists(self.image_folder+'/archive/'+self.archive_name):
            os.makedirs(self.image_folder + '/archive/' + self.archive_name)

        self._empty_images()

        self._client = Client(self)

        self._start_thread()

    def _start_thread(self):
        def corrector_thread():
            while not self._closed:
                new_files = self._get_new_files()

                for new_file in new_files:
                    time = os.path.getmtime(
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
                            'type': 'request',
                            'time': time,
                            'number': self.image_count
                        }
                    })

                    self._client.send(alert)
                    self._client.send(request)

                    self._empty_new()

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

        pass

        # TODO: empty the /current folder
        # TODO: get rid of empty archive files

    def _empty_new(self):

        pass

        # TODO: empty the /new folder

    def add_image(self, image):
        self.image_list.append(image)

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
