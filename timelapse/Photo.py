import time
import picamera

def take_and_save_photo(camera_settings, file_path_name):
    # Take a photo and save it in the given file path name
    # file_path_name includes a relative or absolute path to the file

    with picamera.PiCamera() as camera:
        camera.resolution = (camera_settings.horizontal_resolution,
                             camera_settings.vertical_resolution)
        camera.rotation = camera_settings.rotation

        # TODO Do we want to add anything to exif data?

        time.sleep(camera_settings.camera_start_up_time)
        camera.capture(file_path_name)

    return
