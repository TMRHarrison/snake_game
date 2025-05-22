"""Pellet tests"""

import unittest
import curses

from entities.pellet import Pellet
from tests import window_to_list


class TestPellet(unittest.TestCase):
    """Test pellet methods"""

    def test_creation(self):
        """Make a pellet and ensure it has the correct attributes"""

        pellet = Pellet(0, 0)

        self.assertEqual(pellet.x_pos, 0)
        self.assertEqual(pellet.y_pos, 0)
        self.assertEqual(pellet.icon, "N")



class TestCurses(unittest.TestCase):
    """Test curses-related functions"""

    def setUp(self):
        """Initialize curses for each test in the category"""
        curses.initscr()


    def test_draw(self):
        """Draw the pellet to a curses window"""

        window = curses.newwin(5, 5)
        window.clear()

        x_pos = 3
        y_pos = 1
        pellet = Pellet(x_pos, y_pos)

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
        pellet.draw(window)
        self.assertListEqual(
            window_to_list(window),
            [
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", "N", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )
