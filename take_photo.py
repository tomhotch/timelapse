#!/usr/bin/python

# Purpose: Take a photo for creating a time lapse video
# - Save in a date based directory structure - one directory per day
# - File name includes date and time for easy search by date
#
# Pre-conditions:
# - Called as a scheduled cron task
# - Access to storage for saving the photo
#   Storage could be local, an external USB drive, or NFS
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

# TODO: Refactor per
# http://www.oreilly.com/programming/free/files/real-world-maintainable-software.pdf
#
# TODO: Error handling and logging
#
# TODO: Don't take phots at night

import os
import time
import datetime
import logging

import picamera

from CameraSettings import CameraSettings

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

def take_photo():
    # PROJECT_DIR = "/synology211j/Share/raspberry-pi/timelapse/"
    PROJECT_DIR = "/media/usb1/projects/timelapse"
    # PROJECT_DIR = "/home/pi/projects/timelapse/photos"
    # PROJECT_DIR = '/bogus'

    LOG_FILE = os.path.join(PROJECT_DIR, 'take_photo.log')

    logging.basicConfig(filename=LOG_FILE,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO)
    logging.debug('Starting take_photo')
    try:
        logging.debug('Creating FileManager')
        file_mgr = FileManager(PROJECT_DIR)
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

    logging.info('Taking photo with file path: %s', file_name_path)

    camera_settings = CameraSettings();
    # Camera is mounted upside down in the weatherproof housing
    # Need to rotate 180 degrees so photo is right side up
    camera_settings.rotation = 180
    photo = Photo(camera_settings)
    photo.take_and_save_photo(file_name_path)
    # WIP  Add message logging
    # NEXT Add tests for logging and top level take_photo
    # NEXT Is a try/except needed for take_and_save_photo?
    # NEXT Add check as to whether or not to take a photo - don't take photos
    #      when it's dark.  Log a message either way.
    # LATER Add a separate monitoring routine to send email if photos
    #       aren't being added to the NFS share (maye run on a different
    #       computer in case the Pi dies?

# Enable running the module as a script
if __name__ == "__main__":
    take_photo()
