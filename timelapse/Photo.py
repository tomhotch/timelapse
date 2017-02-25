import time
import picamera

class Photo:
    """Actions and meta data for a photo"""

    def __init__(self, camera_settings):
        self.camera_settings = camera_settings

    def take_and_save_photo(self, file_path_name):
        # Take a photo and save it in the given file path name
        # file_path_name includes a relative or absolute path to the file

        with picamera.PiCamera() as camera:

            camera.resolution = (self.camera_settings.horizontal_resolution,
                    self.camera_settings.vertical_resolution)

            camera.rotation = self.camera_settings.rotation
            # TODO Do we want to add anything to exif data?

            time.sleep(self.camera_settings.camera_start_up_time)
            camera.capture(file_path_name)

        return
