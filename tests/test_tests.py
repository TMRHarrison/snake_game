"""Test the testing functions"""

import curses
import time
import unittest

from tests import MockWindow, timeout_wrapper, window_to_list


class TestTimeoutWrapper(unittest.TestCase):
    """Test the wrapper that prevents infinite loops in the tests"""

    def test_infinite_loop(self):
        """This loop will timeout after 0.1 seconds."""

        with self.assertRaises(TimeoutError):
            with timeout_wrapper(0.1):
                while True:
                    pass


    def test_normal_completion(self):
        """Don't timeout if the operation happens fast enough"""

        with timeout_wrapper(0.1):
            time.sleep(0.05)


class TestWindowToList(unittest.TestCase):
    """Convert windows to lists, track changes with those"""

    def setUp(self):
        """Initialize curses"""
        curses.initscr()


    def test_window_to_list(self):
        """convert windows to lists"""

        window = curses.newwin(5, 5)

        self.assertListEqual(
            window_to_list(window),
            [
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )

        window.addstr(2, 0, "string")

        self.assertListEqual(
            window_to_list(window),
            [
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                ["s", "t", "r", "i", "n"],
                ["g", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )


    def test_no_chr(self):
        """Test no conversion to character from integer"""

        window = curses.newwin(5, 5)

        self.assertListEqual(
            window_to_list(window, no_chr=True),
            [
                [32, 32, 32, 32, 32],
                [32, 32, 32, 32, 32],
                [32, 32, 32, 32, 32],
                [32, 32, 32, 32, 32],
                [32, 32, 32, 32, 32]
            ]
        )


class TestMockWindow(unittest.TestCase):
    """Test replacing a function with a mock"""

    def setUp(self):
        """Initialize curses"""
        curses.initscr()


    def test_mock_border(self):
        """Make a mockwindow subclass that replaces the border method"""

        class MockWindowBorder(MockWindow): #pylint: disable=too-few-public-methods
            """Replace the border method"""

            def border(self):
                """Mocked border method"""
                self.window.addch(0, 0, "0")
                self.window.addch(0, 4, "0")
                self.window.addch(4, 0, "0")
                self.window.insch(4, 4, "0")


        window = MockWindowBorder(
            curses.newwin(5, 5)
        )

        self.assertListEqual(
            window_to_list(window), #type: ignore
            [
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )

        window.border()

        self.assertListEqual(
            window_to_list(window), #type: ignore
            [
                ["0", " ", " ", " ", "0"],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                ["0", " ", " ", " ", "0"]
            ]
        )
