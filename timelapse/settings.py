import os

class CameraSettings:
    """Settings for Pi Camera"""

    def __init__(self):
        self.horizontal_resolution = 1920
        self.vertical_resolution = 1080

        # An internet search suggests 1 second is enough for camera start up time,
        # so 2 seconds should be safe.
        self.camera_start_up_time = 2
        self.rotation = 0

class FileSettings:
    """Settings for directories and files"""

    def __init__(self):
        # PROJECT_DIR = "/synology211j/Share/raspberry-pi/timelapse/"

        self.project_dir = "/media/usb1/projects/timelapse"
        
        self.log_file_name = "take_photo.log"

    def log_file(self):
        return os.path.join(self.project_dir, self.log_file_name)


