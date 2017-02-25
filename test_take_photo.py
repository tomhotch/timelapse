#!/usr/bin/python

import os

import unittest
import timelapse.take_photo
from timelapse.CameraSettings import CameraSettings

class TestTakePhoto(unittest.TestCase):
    # NEXT: This runs the take_photo function.  Need to create a set of tests
    # Might need to add some parameters to make the functions more testable.
    # Example: Running this logs to a default logfile - want to log to a
    # test log file to test the logging functions.
    def test_take_photo(self):
        timelapse.take_photo.take_photo()

suite = unittest.TestLoader().loadTestsFromTestCase(TestTakePhoto)
unittest.TextTestRunner(verbosity=2).run(suite)

