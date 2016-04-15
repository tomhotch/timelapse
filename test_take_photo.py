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
        root_dir = os.path.join("/", "path", "to", "root", "dir")
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
        root_dir = os.path.join(".", "test", "temp")

        try:
            f = take_photo.FileManager(root_dir)
            os.makedirs(root_dir)

            # Pick some specific values to verify the right directories get created
            year, month, day = '2001', '09', '11'

            self.assertFalse(os.path.isdir(os.path.join(root_dir, year)),
                "Verify year directory does not exist before creating it")

            f._create_directories(year, month, day)
            self.assertTrue(os.path.isdir(os.path.join(root_dir, year, month, day)),
                "Verify directories created successfully")

        finally:
            # Clean up - remove directories created just for this test
            os.removedirs(os.path.join(root_dir, year, month, day))
            self.assertFalse(os.path.isdir(root_dir),
                "Verify test directory does not exist after clean up")

        # TODO Check permissions?
        # TODO Verify exceptions when directories can't be created
        # - Bogus root directory?
        # - Insufficient permissions?

    def test_get_file_path(self):
        root_dir = os.path.join(".", "test", "temp")
        os.makedirs(root_dir)

        try:
            f = take_photo.FileManager(root_dir)
            file_path = f.get_file_path()

            # TODO: The regex path check is unix specific.  Is there
            # a way to have a regexp check for os path separator?
            path, basename = os.path.split(file_path)
            self.assertRegexpMatches(path, "\d\d\d\d/\d\d/\d\d",
                "Verify path format is yyyy/mm/dd")

            self.assertRegexpMatches(basename, "\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d",
                "Verify file name format is year-month-day_hour-minute-second")

        finally:
            # Clean up - remove directories created just for this test
            os.removedirs(os.path.dirname(file_path))
            self.assertFalse(os.path.isdir(root_dir),
                "Verify test directory does not exist after clean up")

class TestPhoto(unittest.TestCase):
    def test_take_and_save_photo(self):
        test_dir = "test"
        os.makedirs(test_dir)
        test_file = "test.jpg"
        test_file_path = os.path.join(test_dir, test_file)

        try:
            self.assertFalse(os.path.isfile(test_file_path),
                "Verify test file does not exist before taking photo")

            p = take_photo.Photo()
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

        finally:
            # Clean up test directories and files
            os.remove(test_file_path)
            os.removedirs(test_dir)
            self.assertFalse(os.path.isfile(test_dir),
                "Verify test directory does not exist after clean-up")
        return

suite = unittest.TestLoader().loadTestsFromTestCase(TestFileManager)
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPhoto))
unittest.TextTestRunner(verbosity=2).run(suite)

