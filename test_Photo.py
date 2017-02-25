#!/usr/bin/python

import os

import unittest
from timelapse.CameraSettings import CameraSettings
from timelapse.Photo import Photo

class TestPhoto(unittest.TestCase):
    def test_take_and_save_photo(self):
        test_dir = "test"
        os.makedirs(test_dir)
        test_file = "test.jpg"
        test_file_path = os.path.join(test_dir, test_file)

        self.assertFalse(os.path.isfile(test_file_path),
            "Verify test file does not exist before taking photo")

        # TODO: Add some tests to validate the range of start up times
        #       Should be in a unit test for CameraSettings?
        camera_settings = CameraSettings()

        # Reduce the start up time for the test to run fast
        camera_settings.camera_start_up_time = 0.5
        p = Photo(camera_settings)
        p.take_and_save_photo(test_file_path)
        self.assertTrue(os.path.isfile(test_file_path),
            "Verify test file exists after taking photo")

        # Expected size of .jpg with 1920 x 1080 resolution
        MIN_FILE_SIZE =  600000
        MAX_FILE_SIZE = 1500000
        size = os.path.getsize(test_file_path)
        msg = "File size is: {:d}. ".format(size)
        msg = msg + "Should be between {:d} and {:d}".format(
            MIN_FILE_SIZE, MAX_FILE_SIZE)
        self.assertIn(size, range(MIN_FILE_SIZE, MAX_FILE_SIZE), msg)

        # NEXT Should we check exif properties, maybe resolution?

        # Clean up test directories and files
        os.remove(test_file_path)
        os.removedirs(test_dir)

        self.assertFalse(os.path.isfile(test_dir),
            "Verify test directory does not exist after clean-up")

suite = unittest.TestLoader().loadTestsFromTestCase(TestPhoto)
unittest.TextTestRunner(verbosity=2).run(suite)

