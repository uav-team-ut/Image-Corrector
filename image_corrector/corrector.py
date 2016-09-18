from threading import Thread

class Corrector:

    def __init__(self, image_folder):

        self._image_folder = image_folder
        self._image_list = []

        self._empty_images()

        self._monitor_thread = Thread(target=_monitor_thread)
        self._monitor_thread.start()

    def _monitor_thread(self):

        pass

        # Finds when a new image has been added to the images/new folder
        # Creates a new image for each

    def _empty_images(self):

        pass

        # Empties the images/current folder

    def add_image(self, image):

        self._image_list.append(image)

    @property
    def image_count(self):
        return len(self._image_list)
