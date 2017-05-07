# Add the timelapse package to test to the system path
import os
import sys
sys.path.insert(0, os.path.abspath(
                       os.path.join(os.path.dirname(__file__), 'timelapse')))

import timelapse
