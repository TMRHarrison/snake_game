"""Test segment objects"""

import curses
import random
import unittest

from entities.pellet import Pellet
from entities.segment import Segment


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
        # these don't need to be the same
        self.assertNotEqual(segment.icon, pellet.icon)


    def test_move(self):
        """Move a segment"""

        test_segment = Segment(7, 12)

        test_segment.move(10, 15)

        self.assertEqual(test_segment, Segment(10, 15))


    def test_draw(self):
        """Draw the segment to a curses window"""

        def temp_func(window: curses.window):
            window.resize(5, 5)
            window.clear()

            random.seed(1)
            x_pos = 3
            y_pos = 1
            segment = Segment(x_pos, y_pos)

            self.assertListEqual(
                [[chr(window.inch(y, x)) for x in range(0, 5)] for y in range(0, 5)],
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
                [[chr(window.inch(y, x)) for x in range(0, 5)] for y in range(0, 5)],
                [
                    [" ", " ", " ", " ", " "],
                    [" ", " ", " ", "A", " "],
                    [" ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " "]
                ]
            )

        curses.wrapper(temp_func)
