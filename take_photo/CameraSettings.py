class CameraSettings:
    """Settings for Pi Camera"""

    def __init__(self):
        self.horizontal_resolution = 1920
        self.vertical_resolution = 1080

        # An internet search suggests 1 second is enough for camera start up time,
        # so 2 seconds should be safe.
        self.camera_start_up_time = 2
        self.rotation = 0
