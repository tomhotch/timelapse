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

        # Successful cases
        root_dir = os.path.join("test")
        test_dirs = []

        # TODO: Test fails if root_dir was not deleted from a previous failing
        #       test run.  I thought I fixed that, but I missed something.
        try:
            # Pick some specific values to verify the right directories get created
            year, month, day = '2001', '09', '11'
            year_dir = os.path.join(root_dir, year)
            expected_dir = os.path.join(root_dir, year, month, day)
            test_dirs.append(expected_dir)

            self.assertFalse(os.path.isdir(root_dir),
                "Verify year directory does not exist before creating it")

            f = take_photo.FileManager(root_dir)
            f._create_directories(root_dir, year, month, day)
            self.assertTrue(os.path.isdir(expected_dir),
                "Verify directories created successfully")

            # Make sure the top level directory created has owner, group,
            # and world read/write/execute permission.  I didn't set up
            # proper usernames on different systems, so I want to be able
            # to read, write and delete files from different computers
            # (including from Windows) as different users.
            #
            # Assume Linux since the script is designed to run on
            # Raspberry Pi

            mode = os.stat(year_dir).st_mode & 0777
            self.assertEqual(mode, 0777,
                "Verity year directory is user, group, world read/write/execute")

            f._create_directories(root_dir, year, month, day)
            self.assertTrue(os.path.isdir(expected_dir),
                "Verify create_directories works if the directory already exists")

            # Try making just a day directory (year and month exist)
            day = '12'
            expected_dir = os.path.join(root_dir, year, month, day)
            test_dirs.append(expected_dir)
            self.assertFalse(os.path.isdir(expected_dir),
                "Verify day directory does not exist before creating it")

            f._create_directories(root_dir, year, month, day)
            self.assertTrue(os.path.isdir(expected_dir),
                "Verify a new day directory was created successfully")


        finally:
            # Clean up - remove directories created just for this test
            for dir in test_dirs:
                os.removedirs(dir)
                self.assertFalse(os.path.isdir(dir),
                    "Verify test directory does not exist after clean up")

            self.assertFalse(os.path.isdir(root_dir),
                "Verify root test directory does not exist after clean up")

    def test_get_file_path(self):

        # Successful cases
        root_dir = os.path.join("temp")
        try:
            f = take_photo.FileManager(root_dir)
            file_path = f.get_file_path()

            # TODO: The regex path check is unix specific.  Is there
            # a way to have a regexp check for os path separator?
            path, basename = os.path.split(file_path)
            self.assertRegexpMatches(path, "\d\d\d\d/\d\d/\d\d",
                "Verify path format is yyyy/mm/dd")

            self.assertRegexpMatches(basename,
                "\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d.jpg",
                "Verify file name format is year-month-day_hour-minute-second.jpg")

        finally:
            # Clean up - remove directories created just for this test
            os.removedirs(os.path.dirname(file_path))
            self.assertFalse(os.path.isdir(root_dir),
                "Verify test directory does not exist after clean up")

        # Error Cases
        # Create a directory that can't be written to
        unwritable_dir = "unwritable"
        TEST_UMASK = 0222
        orig_umask = os.umask(TEST_UMASK)
        os.makedirs(unwritable_dir)

        try:
            # Make sure we get an exception if creating the directory fails
            f = take_photo.FileManager(unwritable_dir)
            self.assertRaises(OSError, f.get_file_path )

        finally:
            os.umask(orig_umask)
            os.removedirs(unwritable_dir)


class TestPhoto(unittest.TestCase):
    def test_take_and_save_photo(self):
        test_dir = "test"
        os.makedirs(test_dir)
        test_file = "test.jpg"
        test_file_path = os.path.join(test_dir, test_file)

        # NEXT: With the try finally, if something fails in the try, the
        #       messages are hidden - you get an error message from the
        #       finally block.  Need a way to show the failure messages
        #       and guarantee clean up.  Maybe an after hook to remove
        #       the test directory?
        try:
            self.assertFalse(os.path.isfile(test_file_path),
                "Verify test file does not exist before taking photo")

            # TODO: Add some tests to validate the range of start up times
            #       Should be in a unit test for CameraSettings?
            camera_settings = take_photo.CameraSettings()

            # Reduce the start up time for the test to run fast
            camera_settings.camera_start_up_time = 0.5
            p = take_photo.Photo(camera_settings)
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

class TestTakePhoto(unittest.TestCase):
    # NEXT: This runs the take_photo function.  Need to create a set of tests
    # Might need to add some parameters to make the functions more testable.
    # Example: Running this logs to a default logfile - want to log to a
    # test log file to test the logging functions.
    def test_take_photo(self):
        take_photo.take_photo()

suite = unittest.TestLoader().loadTestsFromTestCase(TestFileManager)
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPhoto))
# suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTakePhoto))
unittest.TextTestRunner(verbosity=2).run(suite)

