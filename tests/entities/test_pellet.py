"""Pellet tests"""

import unittest
import curses

from entities.pellet import Pellet


class TestPellet(unittest.TestCase):
    """Test pellet methods"""

    def test_creation(self):
        """Make a pellet and ensure it has the correct attributes"""

        pellet = Pellet(0, 0)

        self.assertEqual(pellet.x_pos, 0)
        self.assertEqual(pellet.y_pos, 0)
        self.assertEqual(pellet.icon, "N")


    def test_draw(self):
        """Draw the pellet to a curses window"""

        def temp_func(window: curses.window):
            window.resize(5, 5)
            window.clear()

            x_pos = 3
            y_pos = 1
            pellet = Pellet(x_pos, y_pos)

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
            pellet.draw(window)
            self.assertListEqual(
                [[chr(window.inch(y, x)) for x in range(0, 5)] for y in range(0, 5)],
                [
                    [" ", " ", " ", " ", " "],
                    [" ", " ", " ", "N", " "],
                    [" ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " "]
                ]
            )

        curses.wrapper(temp_func)
