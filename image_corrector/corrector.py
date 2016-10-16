from datetime import datetime
from threading import Thread
from time import sleep

from client import Client
from image import AerialImage
from os import listdir


class Corrector:

    def __init__(self, image_folder):

        self._image_folder = image_folder
        self._image_list = []
        self._closed = False

        self._archive_name = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
        self._empty_images()

        self._client = Client(self)

        self._start_thread()

    def _start_thread(self):
        def corrector_thread(self):
            while not self._closed:
                new_files = self._get_new_files()

                for new_file in new_files:
                    image = AerialImage(self, new_file)
                    self.add_image(image)

                    self._empty_new()

                sleep(0.1)

        self._corrector_thread = Thread(target=corrector_thread(self))
        self._corrector_thread.start()

    def _get_new_files(self):

        return (listdir(self._image_folder+'/new'))

        # TODO: return new files in /new as a list of strings, return
        # [] if there aren't any

    def _empty_images(self):

        pass

        # TODO: empty the /current folder

    def _empty_new(self):

        pass

        # TODO: empty the /new folder

    def add_image(self, image):

        self._image_list.append(image)

    @property
    def archive_name(self):
        return self._archive_name

    @property
    def client(self):
        return self._client

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
