"""Test the base state"""

import curses
import unittest

from state.state_test import StateTest
from tests import window_to_list


# we are deliberately accesssing protected members to test their functionality
#pylint: disable=protected-access
class TestTestState(unittest.TestCase):
    """Test state methods"""

    def setUp(self):
        curses.initscr()


    def test_state_no_delay(self):
        """Test no-delay state"""

        StateTest(10, 10, fps=10)


    def test_state_with_delay(self):
        """Test with-delay state"""

        StateTest(10, 10, no_delay=False)


    def test_key_pressed_no_delay(self):
        """Press q to set the state to done in no-delay"""

        test = StateTest(10, 10, fps=10)
        test.key_pressed(ord("q"))
        self.assertTrue(test.done)


    def test_key_pressed_with_delay(self):
        """Press q to set the state to done with delay mode."""

        test = StateTest(10, 10, no_delay=False)
        test.key_pressed(ord("q"))
        self.assertTrue(test.done)


    def test_draw_with_delay(self):
        """Make sure the draw function renders to the window"""

        test = StateTest(80, 20, fps=10)

        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(test.window)],
            [
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                "
            ]
        )

        test.draw()
        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(test.window)],
            [
                "┌──────────────────────────────────────────────────────────────────────────────┐",
                "│                                                                              │",
                "│                                                                              │",
                "│  Testing no-delay mode. Press 'q' to move to next test.                      │",
                "│                                                                              │",
                "│                                                                              │",
                "│                                                                              │",
                "Extremely long test string that should go off both sides of the screen. Really r",
                "A newline that should be fine.                                                 │",
                "Another                                                                        │",
                "│                                                                              │",
                "t string that should go off both sides of the screen. Really really long, probab",
                "│                        A newline that should be fine.                        │",
                "│                                   Another                                    │",
                "│                                                                              │",
                "ld go off both sides of the screen. Really really long, probably 100 characters.",
                "│                                                 A newline that should be fine.",
                "│                                                                        Another",
                "│                                                                              │",
                "└──────────────────────────────────────────────────────────────────────────────┘"
            ]
        )

        # two button presses to draw
        test._keys_pressed = [ord("f"), ord("r")]
        test.draw()
        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(test.window)],
            [
                "┌──────────────────────────────────────────────────────────────────────────────┐",
                "│102  f                                                                        │",
                "│114  r                                                                        │",
                "│  Testing no-delay mode. Press 'q' to move to next test.                      │",
                "│                                                                              │",
                "│                                                                              │",
                "│                                                                              │",
                "Extremely long test string that should go off both sides of the screen. Really r",
                "A newline that should be fine.                                                 │",
                "Another                                                                        │",
                "│                                                                              │",
                "t string that should go off both sides of the screen. Really really long, probab",
                "│                        A newline that should be fine.                        │",
                "│                                   Another                                    │",
                "│                                                                              │",
                "ld go off both sides of the screen. Really really long, probably 100 characters.",
                "│                                                 A newline that should be fine.",
                "│                                                                        Another",
                "│                                                                              │",
                "└──────────────────────────────────────────────────────────────────────────────┘"
            ]
        )


    def test_draw_no_delay(self):
        """Make sure the draw function renders to the window"""

        test = StateTest(80, 20, no_delay=False)

        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(test.window)],
            [
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                ",
                "                                                                                "
            ]
        )

        test.draw()
        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(test.window)],
            [
                "┌──────────────────────────────────────────────────────────────────────────────┐",
                "│                                                                              │",
                "│                                                                              │",
                "│  Testing delay mode. Press 'q' to quit.                                      │",
                "│                                                                              │",
                "│                                                                              │",
                "│                                                                              │",
                "Extremely long test string that should go off both sides of the screen. Really r",
                "A newline that should be fine.                                                 │",
                "Another                                                                        │",
                "│                                                                              │",
                "t string that should go off both sides of the screen. Really really long, probab",
                "│                        A newline that should be fine.                        │",
                "│                                   Another                                    │",
                "│                                                                              │",
                "ld go off both sides of the screen. Really really long, probably 100 characters.",
                "│                                                 A newline that should be fine.",
                "│                                                                        Another",
                "│                                                                              │",
                "└──────────────────────────────────────────────────────────────────────────────┘"
            ]
        )

        # two button presses to draw
        test._keys_pressed = [ord("f")]
        test.draw()
        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(test.window)],
            [
                "┌──────────────────────────────────────────────────────────────────────────────┐",
                "│102  f                                                                        │",
                "│                                                                              │",
                "│  Testing delay mode. Press 'q' to quit.                                      │",
                "│                                                                              │",
                "│                                                                              │",
                "│                                                                              │",
                "Extremely long test string that should go off both sides of the screen. Really r",
                "A newline that should be fine.                                                 │",
                "Another                                                                        │",
                "│                                                                              │",
                "t string that should go off both sides of the screen. Really really long, probab",
                "│                        A newline that should be fine.                        │",
                "│                                   Another                                    │",
                "│                                                                              │",
                "ld go off both sides of the screen. Really really long, probably 100 characters.",
                "│                                                 A newline that should be fine.",
                "│                                                                        Another",
                "│                                                                              │",
                "└──────────────────────────────────────────────────────────────────────────────┘"
            ]
        )
