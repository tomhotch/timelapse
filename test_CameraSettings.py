#!/usr/bin/python

import os
import unittest
from timelapse.CameraSettings import CameraSettings

class TestCameraSettings(unittest.TestCase):
    def test_default_camera_settings(self):
        cs = CameraSettings()
        self.assertEqual(cs.horizontal_resolution, 1920,
            "Default horizontal resolution should be 1920")
        self.assertEqual(cs.vertical_resolution, 1080,
            "Default vertical resolution should be 1080")
        self.assertEqual(cs.camera_start_up_time, 2,
            "Default camera start up time should be 2 seconds")
        self.assertEqual(cs.rotation, 0, "Default rotation should be zero")

    def test_modify_camera_settings(self):
        cs = CameraSettings()
        self.assertEqual(cs.rotation, 0, "Default rotation should be zero")
        cs.rotation=180
        self.assertEqual(cs.rotation, 180, "Can change rotation")

suite = unittest.TestLoader().loadTestsFromTestCase(TestCameraSettings)
unittest.TextTestRunner(verbosity=2).run(suite)
