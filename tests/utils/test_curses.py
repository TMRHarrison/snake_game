"""Curses utility functions"""

import curses
import re
import unittest

from tests import window_to_list
from utils.curses import Alignment, check_boundaries, get_old_cursor_visibility, printf
from utils.errors import WindowSizeError


class TestAlignment(unittest.TestCase):
    """Test the alignment object"""

    def test_creation(self):
        """Get alignment objects"""

        self.assertEqual(Alignment("left"), Alignment.LEFT)
        self.assertEqual(Alignment("center"), Alignment.CENTER)
        self.assertEqual(Alignment("right"), Alignment.RIGHT)

    def test_missing(self):
        """Make sure the missing value message is descriptive"""

        with self.assertRaisesRegex(
            ValueError,
            re.escape(
                "test is not a valid value for Alignment. Must be one of "\
                "{'LEFT': <Alignment.LEFT: 'left'>, "\
                "'CENTER': <Alignment.CENTER: 'center'>, "\
                "'RIGHT': <Alignment.RIGHT: 'right'>}"
            )
        ):
            Alignment("test")


class TestFunctions(unittest.TestCase):
    """Test the functions"""

    def setUp(self):
        curses.initscr()


    def test_printf_left(self):
        """Print left aligned text"""

        window = curses.newwin(3, 10)
        printf(
            window,
            "left aligned\n"\
                "left\n"\
                "left",
            -1,
            1,
            8,
            "left"
        )

        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(window)],
            [
                "          ",
                "eft aligne",
                "eft       "
            ]
        )


    def test_printf_center(self):
        """Print center aligned text"""

        window = curses.newwin(3, 10)
        printf(
            window,
            "center aligned\n"\
                "center\n"\
                "center",
            -1,
            1,
            8,
            "center"
        )

        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(window)],
            [
                "          ",
                "er aligned",
                "center    "
            ]
        )


    def test_printf_right(self):
        """Print right aligned text"""

        window = curses.newwin(3, 10)
        printf(
            window,
            "right aligned\n"\
                "right\n"\
                "right",
            -1,
            1,
            8,
            "right"
        )

        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(window)],
            [
                "          ",
                "aligned   ",
                "  right   "
            ]
        )


    def test_printf_lower_right(self):
        """Don't error out while writing the lower right space"""

        window = curses.newwin(3, 10)
        printf(
            window,
            "right aligned",
            0,
            2,
            10,
            "right"
        )

        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(window)],
            [
                "          ",
                "          ",
                "ht aligned"
            ]
        )


    def test_printf_misaligned(self):
        """Print right aligned text"""

        window = curses.newwin(3, 10)
        with self.assertRaises(ValueError):
            printf(
                window,
                "not aligned",
                -1,
                1,
                8,
                "test"
            )


    def test_get_old_cursor_visibility(self):
        """Get the old cursor visibility"""

        old_cursor = curses.curs_set(2)

        try:
            self.assertEqual(
                get_old_cursor_visibility(),
                2
            )
            self.assertEqual(curses.curs_set(1), 2)
        finally:
            curses.curs_set(old_cursor)


    def test_check_boundaries(self):
        """check the window boundaries"""

        window = curses.newwin(10, 10)

        # boundaries are ok
        check_boundaries(window, 10, 10)
        # Window bigger than boundaries is ok
        check_boundaries(window, 5, 5)

        # check both dimensions
        with self.assertRaises(WindowSizeError):
            check_boundaries(window, 11, 10)
        with self.assertRaises(WindowSizeError):
            check_boundaries(window, 10, 11)
