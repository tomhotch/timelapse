import os
import datetime

class FileManager:
    """Create directories and file names for storing photos"""
    # One photo per minute is 1,440 photos per day, so use one dir per day:
    # year/month/day

    def __init__(self, root_dir="."):
        self.root_dir = root_dir

    def _get_datetime(self):
        # Get the current year, month, day, hour, minute, second
        now = datetime.datetime.now()
        return (now.year, now.month, now.day, now.hour, now.minute, now.second)

    def _create_directories(self, root, year, month, day):
        # Create root/year/month/day directories (if needed)

        # On Raspberry Pi, it seems os.makedirs ignores the mode parameter,
        # so the umask has to be changed to control permissions.  I want
        # world rwx access to allow different users from different hosts
        # to read/edit/delete files and directories (I don't have things
        # set up to access the NFS server as a specific user).  Set the
        # umask to 0 to make the directories world rwx.
        # TODO: Make umask a parameter or class attribute.
        UMASK = 0
        os.umask(UMASK)

        # TODO Could be a generic routine that joins an arbitrary
        # number of args to create a directory.
        # TODO Handle errors
        dir = os.path.join(root, year, month, day)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        return

    def get_file_path(self):
        # Create root/year/month/day sub-directories, as needed.
        # Return the path + the file name to create
        # Use a filename of year-month-day_hour-min-sec
        # Assume two photos will not be taken in the same second

        year, month, day, hour, minute, second = self._get_datetime()
        year_str = "{:04d}".format(year)
        month_str = "{:02d}".format(month)
        day_str = "{:02d}".format(day)

        self._create_directories(self.root_dir, year_str, month_str, day_str)

        self.file_name = (
            year_str + "-" + month_str + "-" + day_str + "_"
            + "{:02d}-{:02d}-{:02d}.jpg".format(hour, minute, second))
        
        return os.path.join(self.root_dir, year_str, month_str, day_str,
            self.file_name)
