"""Expected errors the game can produce. These are meant to be captured."""

import unittest

from utils.errors import SnakeError, WindowSizeError


class TestErr(unittest.TestCase):
    """Test the errors"""

    def test_window_size_err(self):
        """Make sure the window size error is both windowsize and snake error.
        """

        with self.assertRaises(WindowSizeError):
            raise WindowSizeError()

        with self.assertRaises(SnakeError):
            raise WindowSizeError()


    def test_snake_err(self):
        """This is only one kind of error"""

        with self.assertRaises(SnakeError):
            raise SnakeError()
