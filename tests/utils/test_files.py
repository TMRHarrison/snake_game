"""File and directory manipulation"""

import unittest
from unittest.mock import patch

from utils.files import get_savedir


class TestFiles(unittest.TestCase):
    """Test the functions"""

    @patch("sys.platform", "win32")
    @patch("pathlib.Path.home", lambda : "C:/Users/Test")
    def test_get_savedir_windows(self):
        """Mock windows system"""

        self.assertEqual(get_savedir("test"), "C:/Users/Test/AppData/Roaming/test")


    @patch("sys.platform", "darwin")
    @patch("pathlib.Path.home", lambda : "/Users/Test")
    def test_get_savedir_macos(self):
        """Mock macintosh system"""

        self.assertEqual(get_savedir("test"), "/Users/Test/Library/Application Support/test")


    @patch("sys.platform", "linux")
    @patch("pathlib.Path.home", lambda : "/home/Test")
    def test_get_savedir_linux(self):
        """Mock macintosh system"""

        self.assertEqual(get_savedir("test"), "/home/Test/.local/share/test")


    @patch("sys.platform", "unknown")
    @patch("pathlib.Path.home", lambda : "/something/else")
    def test_get_savedir_other(self):
        """Mock macintosh system"""

        self.assertEqual(get_savedir("test"), None)
