from threading import Thread
from time import sleep

from client import Client
from image import AerialImage


class Corrector:

    def __init__(self, image_folder):

        self._image_folder = image_folder
        self._image_list = []
        self._closed = False

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

                    self._empty_images()

                sleep(0.1)

        self._corrector_thread = Thread(target=corrector_thread)
        self._corrector_thread.start()

    def _get_new_files(self):

        pass

        # TODO: return new files as file objects, return None if
        # there aren't any

    def _empty_images(self):

        pass

        # TODO: empty the /current folder

    def add_image(self, image):

        self._image_list.append(image)

    @property
    def image_count(self):
        return len(self._image_list)

    def close(self):

        self._closed = True
        self._client.close()
