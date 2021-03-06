#!/usr/bin/python3

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

# TODO: Make unit test use a mock PiCamera
# TODO: Refactor per
# http://www.oreilly.com/programming/free/files/real-world-maintainable-software.pdf
#
# TODO: Error handling and logging
#
# TODO: Don't take photos at night

import os
import logging

from FileManager import FileManager
from Photo import take_and_save_photo
from settings import CameraSettings
from settings import FileSettings


def take_photo():
    file_settings = FileSettings()

    logging.basicConfig(
        filename=file_settings.log_file(),
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO)
    logging.debug('Starting take_photo')
    try:
        logging.debug('Creating FileManager')
        file_mgr = FileManager(file_settings.project_dir)
        logging.debug('Getting file path')
        file_name_path = file_mgr.get_file_path()
        logging.debug('Photo file path name: %s', file_name_path)
    except:
        # Got an error trying to create the directory.
        # NEXT file_name_path isn't set on an exception.  What exception
        #      message is raised?  Print that?  Yes, need to debug the error.
        # NEXT Create a unit (or behavioral test) to check this logic - does
        #      it need to be put into a separate module?
        logging.error('Failed to create: %s', os.path.dirname(file_name_path))
        return

    logging.info('Taking photo with file path: %s', file_name_path)

    camera_settings = CameraSettings()
    # Camera is mounted upside down in the weatherproof housing
    # Need to rotate 180 degrees so photo is right side up
    camera_settings.rotation = 180

    take_and_save_photo(camera_settings, file_name_path)
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
