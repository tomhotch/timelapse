#!/usr/bin/python

import os

import unittest
import take_photo

class TestFileManager(unittest.TestCase):
    def test_default_root_dir(self):
        f = take_photo.FileManager()
        self.assertEqual(f.root_dir, ".", \
            "FileManager default root_dir is current directory")

    def test_set_root_dir(self):
        root_dir = "/path/to/root/dir"
        f = take_photo.FileManager(root_dir)
        self.assertEqual(f.root_dir, root_dir, "Can set FileManager root_dir")

    def test_get_datetime(self):
        f = take_photo.FileManager()
        year, month, day, hour, minute, second = f._get_datetime()
        # TODO: Should I mock the python now function to test for specific
        # values?
        # Checks that the year is between 2016 and 2099.  2099 is somewhat
        # arbitrary - the test will work for many years ... probably more
        # than is necessary.
        self.assertIn(year, range(2016, 2100),
            "FileManger get_datetime returns a valid year")
        self.assertIn(month, range(1, 13),
            "FileManger get_datetime returns a valid month")
        self.assertIn(day, range(1, 32),
            "FileManger get_datetime returns a valid day")
        self.assertIn(hour, range(1, 25),
            "FileManger get_datetime returns a valid hour")
        self.assertIn(minute, range(0, 60),
            "FileManger get_datetime returns a valid minute")
        self.assertIn(second, range(0, 60),
            "FileManger get_datetime returns a valid second")

    def test_create_direcotry(self):
        root_dir = "./test/temp"
        f = take_photo.FileManager(root_dir)
        # Pick some specific values to verify the right directories get created
        year, month, day = '2001', '09', '11'

        self.assertFalse(os.path.isdir(os.path.join(root_dir, year)),
            "Verify year directory does not exist before creating it")

        f._create_directories(year, month, day)
        self.assertTrue(os.path.isdir(os.path.join(root_dir, year, month, day)),
            "Verify directories created successfully")

        # Clean up - remove directories created just for this test
        os.rmdir(os.path.join(root_dir, year, month, day))
        os.rmdir(os.path.join(root_dir, year, month))
        os.rmdir(os.path.join(root_dir, year))
        self.assertFalse(os.path.isdir(os.path.join(root_dir, year)),
            "Verify year directory does not exist after clean up")

        # TODO Verify the directories all exist, check permissions?
        # TODO Verify exceptions when directories can't be created
        # - Bogus root directory?
        # - Insufficient permissions?

suite = unittest.TestLoader().loadTestsFromTestCase(TestFileManager)
unittest.TextTestRunner(verbosity=2).run(suite)

