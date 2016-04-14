#!/usr/bin/python

# Purpose: Take a photo for creating a time lapse video
# - Save in a date based directory structure - one directory per day
# - File name includes date and time for easy search by date
#
# Pre-conditions:
# - Called as a scheduled cron task
# - Access to an NFS drive for saving photos
#
# Post-conditions:
# - Create a new directory if necessary
# - Photo saved in the correct directory
# - Messages written to log file (errors or success)
#
# Usage:
# take_photo.py
#
# Options:
# Currently none - could add resolution, burst, naming, root directory, etc.

import os
import time
import datetime

import picamera

def take_photo():
    ROOT_DIR = "/synology211j/Share/raspberry-pi/timelapse/"
    file_mgr = FileManager(ROOT_DIR)
    file_name_path = file_mgr.get_file_path()
    photo.take_and_save_photo(file_name_path)
    # Log a message

class FileManager:
    """Create directories and file names for storing photos"""
    # One photo per minute is 1,440 photos per day, so use one dir per day:
    # year/month/day

    def __init__(self, root_dir="."):
        self.root_dir = root_dir

    def _get_datetime(self):
        # Get the current year, month, day, hour, minute, second
        now = datetime.datetime.now()
        return (now.year, now.month, now.day, now.hour, now.minute, now.second)

    def _create_directories(self, year, month, day):
        # Create year/month/day directories (if needed)
        # TODO Handle errors
        os.makedirs(os.path.join(self.root_dir, year, month, day))
        return

    def get_file_path(self):
        # Create year/month/day sub-directories, as needed.
        # Return the path + the file name to create
        # Use a filename of year-month-day_hour-min-sec
        # Assume two photos will not be taken in the same second

        year, month, day, hour, minute, second = self._get_datetime()
        year_str = "{:04d}".format(year)
        month_str = "{:02d}".format(month)
        day_str = "{:02d}".format(day)
        self._create_directories(year_str, month_str, day_str)
        self.file_name = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(
            year, month, day, hour, minute, second)
        
        # TODO Decide what to do if a file with the target name exists.
        return os.path.join(self.root_dir, year_str, month_str, day_str,
            self.file_name)


class Photo:
    """Actions and meta data for a photo"""

    def take_and_save_photo(self, file_path_name):
        # Take a photo and save it in the given file path name
        # file_path_name includes a relative or absolute path to the file

        with picamera.PiCamera() as camera:
            # Let camera start up and stabilize
            # A quick internet suggests at least 1 sec, so 2 is safe
            CAMERA_START_UP_TIME = 2

            # 1920x108o is HD video at about 1.2MB per jpg file
            HORIZONTAL_RESOLUTION = 1920
            VERTICAL_RESOLUTION = 1080
            camera.resolution = (HORIZONTAL_RESOLUTION, VERTICAL_RESOLUTION)
            # TODO Do we want to add anything to exif data?

            time.sleep(CAMERA_START_UP_TIME)
            camera.capture(file_path_name)

        return


# Enable running the module as a script
if __name__ == "__main__":
    take_photo()
