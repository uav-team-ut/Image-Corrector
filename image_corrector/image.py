# from [module] import Distance

class AerialImage:

    def __init__(self, corrector, image):
        self._number = corrector.image_count + 1
        self._position = None

    @static_method
    def get_distance(yaw, pitch, roll, alt):

        # Get the distance of a point on the ground given the yaw,
        # pitch, roll, and alt. Return a Distance() object

        # x =
        # y =

        return Distance(x, y, yaw)

    def set_position(position):

        self._position = position

        # TODO: save to JSON file

    @property
    def has_position(self):
        return not self._position == None

    def warp(self):

        pass

        # warp the image using SimpleCV
        # save a high and low resolution image in the same folder


class Position:
    """Represents the position of a plane and its camera.

    All units are in radians and meters. For the plane, a yaw of 0
    radians points North and pi / 2 points East, a pitch of 0 radians
    is horizontal and a positive pitch points upwards, and a roll of
    0 radians is level and a positive roll indicates the plane has
    turned to the right. For the camera, a pitch of 0 radians points
    downwards and a positive pitch points towards the front of the
    plane and a roll of 0 radians points to the center of the plane
    and a positive roll points to the right.
    """

    def __init__(self, lat, lon, alt, yaw, pitch, roll, cam_pitch, cam_roll):
        """Instantiate a Position object.

        Once the object has been created the values cannot be
        changed. All units are in radians and meters.
        """
        self._lat = lat
        self._lon = lon
        self._alt = alt
        self._yaw = yaw
        self._pitch = pitch
        self._roll = roll
        self._cam_pitch = cam_pitch
        self._cam_roll = cam_roll

    @property
    def lat(self):
        """Return the latitude of the plane in radians."""
        return self._lat

    @property
    def lon(self):
        """Return the longitude of the plane in radians."""
        return self._lon

    @property
    def alt(self):
        """Return the altitude of the plane in meters."""
        return self._alt

    @property
    def yaw(self):
        """Return the yaw of the plane in radians."""
        return self._yaw

    @property
    def pitch(self):
        """Return the pitch of the plane in radians."""
        return self._pitch

    @property
    def roll(self):
        """Return the roll of the plane in radians."""
        return self._roll

    @property
    def cam_pitch(self):
        """Return the pitch of the camera in radians."""
        return self._cam_pitch

    @property
    def cam_roll(self):
        """Return the roll of the camera in radians."""
        return self._cam_roll
