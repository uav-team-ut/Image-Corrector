import json
from math import atan, tan, cos, sin, pi
import os
from shutil import copy2

from geo_distance import Distance


class AerialImage:

    def __init__(self, corrector, file_name):
        self._number = corrector.image_count + 1
        self._file_name = str(self._number) + '.' +
            file_name.split('.')[1]
        self._position = None

        self._save_original(file_name)

        time = os.path.getmtime(
            self._corrector.image_folder + '/new/' + file_name
        )

        alert = json.dumps({
            'type': 'image',
            'message': {
                'type': 'alert',
                'format': 'original',
                'status': 'available'
            }
        })

        request = json.dumps({
            'type': 'telemetry',
            'message': {
                'type': 'request',
                'time': time,
                'image-number': self._number
            }
        })

        self._corrector.client.send(alert)
        self._corrector.client.send(request)

    def set_position(self, position):
        self._position = position

        did_warp = self._warp()

        alert = json.dumps({
            'type': 'image',
            'message': {
                'type': 'alert',
                'format': 'warped',
                'status': 'available' if did_warp else 'unavailable'
            }
        })

        self._corrector.client.send(alert)

    def _save_original(self, file_name):
        shutil.copy2(
            self._corrector.image_folder + '/new/' + file_name,
            self._corrector.image_folder + '/current/' + self._file_name
        )

        shutil.copy2(
            self._corrector.image_folder + '/new/' + file_name,
            self._corrector.image_folder + '/archive/' +
            self._corrector.archive_name + '/' + self._file_name
        )

    @property
    def has_position(self):
        return self._position is not None

    def _warp(self):

        pass

        # warp the image using SimpleCV / OpenCV
        # leave the corners of the warped image transparent
        # save the warped image in /current/ and in /archive/ just
        # as _save_original does
        # return False if the horizon was visible.


class Position:
    """Represents the position of a plane and its camera.

    All units are in radians and meters. For the plane, a yaw of 0
    radians points North and pi / 2 points East, a pitch of 0 radians
    is horizontal and a positive pitch points upwards, and a roll of
    0 radians is level and a positive roll indicates the plane has
    rolled to the right. For the camera, a pitch of 0 radians points
    downwards and a positive pitch points towards the front of the
    plane and a roll of 0 radians points to the center of the plane
    and a positive roll points to the right.
    """

    def __init__(self, lat, lon, alt, yaw, pitch, roll, cam_pitch, cam_roll):
        """Instantiate a Position object.

        All units are in radians and meters.
        """
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.cam_pitch = cam_pitch
        self.cam_roll = cam_roll

    def get_distance(self, d_pitch=0, d_roll=0):
        """Return the ground distance of a camera's line of sight.

        d_pitch and d_roll are the angles above and to the left of
        where the center of the camera is pointing. A Distance object
        is returned with the distance North in y and the distance
        West in x in meters. None if returned if the camera is
        pointing to the sky.
        """
        alt = self.alt
        yaw = self.yaw
        pitch = self.pitch + self.cam_pitch + d_pitch
        roll = -self.roll + self.cam_roll + d_roll

        # FIXME: Improve is pointed at sky expression
        if abs(pitch) + d_pitch >= pi / 2 or abs(roll) + d_roll >= pi / 2:
            return None

        x = alt * (tan(roll) / cos(pitch) * cos(yaw) + tan(pitch) * sin(yaw))
        y = alt * (tan(pitch) * cos(yaw) - tan(roll) / cos(pitch) * sin(yaw))

        return Distance(x, y)

    def get_corner_distances(self, aspect_ratio, horiz_fov):
        """Return the ground distance of the camera's corners.

        aspect_ratio is the ratio of the width to the height of the
        image and horiz_fov is the horizontal field of view of the
        camera in radians. A list of four Distance objects is
        returned in the order of top-left, top-right, bottom-left,
        and bottom-right corners from get_distance(). None is
        returned if the horizon is visible.
        """
        vert_fov = 2 * atan(tan(horiz_fov / 2) / aspect_ratio)

        corners = [self.get_distance(i * vert_fov / 2, j * horiz_fov / 2)
            for i in (1, -1) for j in (-1, 1)]

        if None in corners:
            print('Cannot warp image', self._file_name,
                'since horizon is visible.')

            return None

        return corners
