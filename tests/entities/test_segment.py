"""Test segment objects"""

import curses
import random
import unittest

from entities.pellet import Pellet
from entities.segment import Segment
from tests import window_to_list


class TestSegment(unittest.TestCase):
    """Test the segment methods"""

    def test_creation(self):
        """Make segments and ensure they have the correct attributes"""

        random.seed(1)

        segment1 = Segment(0, 0)

        self.assertEqual(segment1.x_pos, 0)
        self.assertEqual(segment1.y_pos, 0)
        self.assertEqual(segment1.icon, "A")

        segment2 = Segment(0, 0)

        self.assertEqual(segment2.x_pos, 0)
        self.assertEqual(segment2.y_pos, 0)
        self.assertEqual(segment2.icon, "G")


    def test_repr(self):
        """Test the string representation of the segment"""

        random.seed(1)

        segment1 = Segment(0, 0)

        self.assertEqual(
            repr(segment1),
            "<Segment 'A' at (0,0)>"
        )


    def test_equality_segments(self):
        """Check that the segment is equal to a segment at the same place"""

        random.seed(1)

        segment1 = Segment(4, 1)
        segment2 = Segment(4, 1)

        self.assertEqual(segment1, segment2)
        # these don't need to be the same
        self.assertEqual(segment1.icon, "A")
        self.assertEqual(segment2.icon, "G")


    def test_equality_pellet(self):
        """Check that the segment is equal to a pellet at the same place"""

        random.seed(1)

        segment = Segment(4, 1)
        pellet = Pellet(4, 1)

        self.assertEqual(segment, pellet)
        self.assertEqual(pellet, segment)
        # these don't need to be the same
        self.assertNotEqual(segment.icon, pellet.icon)


    def test_equality_other(self):
        """Check that the segment is not equal to other objects"""

        random.seed(1)

        segment = Segment(4, 1)

        self.assertNotEqual(segment, (4, 1))
        self.assertNotEqual(segment, "")
        self.assertNotEqual(segment, 3)


    def test_move(self):
        """Move a segment"""

        test_segment = Segment(7, 12)

        test_segment.move(10, 15)

        self.assertEqual(test_segment, Segment(10, 15))


class TestCurses(unittest.TestCase):
    """Test curses functions"""

    def setUp(self):
        """initialize curses screen before tests in this category"""
        curses.initscr()


    def test_draw(self):
        """Draw the segment to a curses window"""

        window = curses.newwin(5, 5)
        window.clear()

        random.seed(1)
        x_pos = 3
        y_pos = 1
        segment = Segment(x_pos, y_pos)

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
        segment.draw(window)

        self.assertListEqual(
            window_to_list(window),
            [
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", "A", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )
