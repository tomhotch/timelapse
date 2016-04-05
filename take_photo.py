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
import datetime

def take_photo():
    ROOT_DIR = "/synology211j/Share/raspberry-pi/timelapse/"
    file_mgr = FileManager(ROOT_DIR)
    file_mgr.get_file_path()
    # photo = Photo()
    # photo.get_datetime()
    # photo.take_and_save_photo()
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
        # Use a filename of year-month-day_hour-min-sec
        # Assume two photos will not be taken in the same second
        year, month, day, hour, minute, second = self._get_datetime()
        # NEXT Should we have a separate path and file name?
        self.file_name = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(
            year, month, day, hour, minute, second)
        sub_dir = "{:04d}/{:02d}/{:02d}/".format(self.year, self.month, self.day)
        self.file_path = self.root_dir + "/" + sub_dir + self.file_name + ".jpg"
        # TODO What function should create the directories?
        # TODO Decide what to do if a file with the target name exists.
        print self.file_path
        return self.file_path


class Photo:
    """Actions and meta data for a photo"""

    def take_and_save_photo(self, file_name):
        # Take photo
        # Use PiCamera python module
        # Use raspistill -n (--nopreview)
        # raspistill --mode 1 is for 1920x1080, what's partial FOV?
        # Is date time and other info saved in the exif data by default?
        return


# Enable running the module as a script
if __name__ == "__main__":
    take_photo()
