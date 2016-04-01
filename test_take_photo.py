#!/usr/bin/python

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
        f.get_datetime()
        # TODO: Should I mock the python now function to test for specific values?
        # Checks that the year is between 2016 and 2099.  2099 is somewhat arbitrary -
        # the test will work for many years ... probably more than is necessary.
        self.assertIn(f.year, range(2016, 2100), "FileManger get_datetime sets year correctly")
        self.assertIn(f.month, range(1, 13), "FileManager get_datetime sets month correctly")
        self.assertIn(f.day, range(1, 32), "FileManager get_datetime sets day correctly")
        self.assertIn(f.hour, range(1, 25), "FileManager get_datetime sets hour correctly")
        self.assertIn(f.minute, range(0, 60), "FileManager get_datetime sets minute correctly")
        self.assertIn(f.second, range(0, 60), "FileManager get_datetime sets second correctly")

suite = unittest.TestLoader().loadTestsFromTestCase(TestFileManager)
unittest.TextTestRunner(verbosity=2).run(suite)

