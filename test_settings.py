#!/usr/bin/python

import os
import unittest
from timelapse.settings import CameraSettings
from timelapse.settings import FileSettings

class TestCameraSettings(unittest.TestCase):
    def test_default_camera_settings(self):
        cs = CameraSettings()
        self.assertEqual(
            cs.horizontal_resolution, 1920,
            "Default horizontal resolution should be 1920")
        self.assertEqual(
            cs.vertical_resolution, 1080,
            "Default vertical resolution should be 1080")
        self.assertEqual(
            cs.camera_start_up_time, 2,
            "Default camera start up time should be 2 seconds")
        self.assertEqual(cs.rotation, 0, "Default rotation should be zero")

    def test_modify_camera_settings(self):
        cs = CameraSettings()
        self.assertEqual(cs.rotation, 0, "Default rotation should be zero")
        cs.rotation=180
        self.assertEqual(cs.rotation, 180, "Can change rotation")

class TestFileSettings(unittest.TestCase):
    def test_default_file_setting(self):
        fs = FileSettings()
        self.assertEqual(
            fs.project_dir, "/media/usb1/projects/timelapse",
            "Default project dir is correct")
        self.assertEqual(
            fs.log_file_name, "take_photo.log",
            "Default log file name is take_photo.log")
        self.assertEqual(
            fs.log_file(), "/media/usb1/projects/timelapse/take_photo.log",
            "Default log file name with path is correct")

    def test_modify_file_settings(self):
        fs = FileSettings()
        self.assertEqual(
            fs.project_dir, "/media/usb1/projects/timelapse",
            "Default project dir is correct")
        fs.project_dir = "/new/project/dir"
        self.assertEqual(
            fs.project_dir, "/new/project/dir",
            "Can change the project directory")
        self.assertEqual(
            fs.log_file_name, "take_photo.log",
            "Default log file name is take_photo.log")
        fs.log_file_name = "new_file_name"
        self.assertEqual(
            fs.log_file_name, "new_file_name",
            "Can change the log_file_name")
        self.assertEqual(
            fs.log_file(), "/new/project/dir/new_file_name",
            "Log file name with path matches changes to file name and project dir")

suite = unittest.TestLoader().loadTestsFromTestCase(TestCameraSettings)
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFileSettings))
unittest.TextTestRunner(verbosity=2).run(suite)
