#!/usr/bin/python3

import os
import unittest
import context

import take_photo

class TestTakePhoto(unittest.TestCase):
    # NEXT: This runs the take_photo function.
    # TODO: This test saves a photo in the "normal" location for photos.
    #       Find a way to put the test photo someplace else and clean up.
    # Need to create a set of tests
    # Might need to add some parameters to make the functions more testable.
    # Example: Running this logs to a default logfile - want to log to a
    # test log file to test the logging functions.
    def test_take_photo(self):
        take_photo.take_photo()

suite = unittest.TestLoader().loadTestsFromTestCase(TestTakePhoto)
unittest.TextTestRunner(verbosity=2).run(suite)

