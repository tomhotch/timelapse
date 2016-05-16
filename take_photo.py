#!/usr/bin/python

# Purpose: Take a photo for creating a time lapse video
# - Save in a date based directory structure - one directory per day
# - File name includes date and time for easy search by date
#
# Pre-conditions:
# - Called as a scheduled cron task
# - Access to an NFS drive for saving photos
# - Runs on Raspberry Pi linux. Depends on the Pi camera and some code is
#   linux specific.
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
import logging

import picamera

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

    def _create_directories(self, root, year, month, day):
        # Create root/year/month/day directories (if needed)

        # On Raspberry Pi, it seems os.makedirs ignores the mode parameter,
        # so the umask has to be changed to control permissions.  I want
        # world rwx access to allow different users from different hosts
        # to read/edit/delete files and directories (I don't have things
        # set up to access the NFS server as a specific user).  Set the
        # umask to 0 to make the directories world rwx.
        # TODO: Make umask a parameter or class attribute.
        UMASK = 0
        os.umask(UMASK)

        # TODO Could be a generic routine that joins an arbitrary
        # number of args to create a directory.
        # TODO Handle errors
        dir = os.path.join(root, year, month, day)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        return

    def get_file_path(self):
        # Create root/year/month/day sub-directories, as needed.
        # Return the path + the file name to create
        # Use a filename of year-month-day_hour-min-sec
        # Assume two photos will not be taken in the same second

        year, month, day, hour, minute, second = self._get_datetime()
        year_str = "{:04d}".format(year)
        month_str = "{:02d}".format(month)
        day_str = "{:02d}".format(day)

        self._create_directories(self.root_dir, year_str, month_str, day_str)

        self.file_name = year_str + "-" + month_str + "-" + day_str + "_" \
            + "{:02d}-{:02d}-{:02d}.jpg".format(hour, minute, second)
        
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

def take_photo():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO)
    # ROOT_DIR = "/synology211j/Share/raspberry-pi/timelapse/"
    ROOT_DIR = "/media/usb1/projects/timelapse"
    # ROOT_DIR = "/home/pi/projects/timelapse/photos"
    # ROOT_DIR = '/bogus'
    logging.debug('Starting take_photo')
    try:
        logging.debug('Creating FileManager')
        file_mgr = FileManager(ROOT_DIR)
        logging.debug('Getting file path')
        file_name_path = file_mgr.get_file_path()
        logging.debug('Photo file path name: %s', file_name_path)
    except:
        # Got an error trying to create the directory.
        # NEXT file_name_path isn't set on an exception.  What exception message
        #      is raised?  Print that?  Yes, need to debug the error.
        # NEXT Create a unit (or behavioral test) to check this logic - does
        #      it need to be put into a separate module?
        logging.error('Failed to create: %s', os.path.dirname(file_name_path))
        return

    photo = Photo()
    photo.take_and_save_photo(file_name_path)
    # NEXT Add message logging
    # NEXT Add tests for logging and top level take_photo
    # NEXT Add check as to whether or not to take a photo - provide a way
    #      to turn off/on capture without editing cron tab.  Log a message
    #      if disabled
    # LATER Add a separate monitoring routine to send email if photos
    #       aren't being added to the NFS share (maye run on a different
    #       computer in case the Pi dies?

# Enable running the module as a script
if __name__ == "__main__":
    take_photo()
