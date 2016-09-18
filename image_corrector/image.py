# from [module] import Distance

class Image:

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

    def __init__(self, lat, lon, alt, yaw, pitch, roll, cam_pitch, cam_roll):
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
        return self._lat

    @property
    def lon(self):
        return self._lon

    @property
    def alt(self):
        return self._alt

    @property
    def yaw(self):
        return self._yaw

    @property
    def pitch(self):
        return self._pitch

    @property
    def roll(self):
        return self._roll

    @property
    def cam_pitch(self):
        return self._cam_pitch

    @property
    def cam_roll(self):
        return self._cam_roll
