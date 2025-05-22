""""""

import curses
import unittest

from state.state import State
from tests import MockWindow, timeout_wrapper


class TestState(unittest.TestCase):
    """"""

    def test_state_creation(self):
        """Test basic attributes of the state"""

        state = State(10, 10, 10, True)

        self.assertEqual(state.height, 10)
        self.assertEqual(state.width, 10)
        self.assertEqual(state.no_delay, True)

        self.assertTrue(isinstance(state.window, curses.window))
        self.assertListEqual(state.windows, [state.window])
        self.assertEqual(state.done, False)
        self.assertListEqual(state._keys_pressed, [])

        self.assertEqual(getattr(state, "_State__frame_time"), 100_000_000)
        self.assertTrue(isinstance(getattr(state, "_State__frame_time"), int))


    def test_run(self):
        """Run the base state for 5 frames"""

        class MockWindowGetch(MockWindow):

            def __init__(self, window):
                super().__init__(window)
                self.__calls = 0

            def getch(self) -> int:
                """Simulate 5 frames of no key pressed, then press 'q' once every frame."""
                self.__calls += 1
                # modulo 2 because only -1 breaks the loop.
                if self.__calls >= 5 and self.__calls % 2:
                    return ord("q")
                return -1

        with timeout_wrapper(0.5):
            state = State(5, 5, 1000, True)
            # the mock isn't technically a window object, but the MockWindow is
            # explicitly compatible
            state.window = ( #type: ignore
                MockWindowGetch(state.window)
            )

            state.run()


    def test_key_pressed(self):
        """Press q to set the state to done."""

        state = State(5, 5, 10, True)

        state.key_pressed(ord(" "))
        self.assertFalse(state.done)

        state.key_pressed(ord("q"))
        self.assertTrue(state.done)


    def test_update(self):
        """The update function does nothing"""

        state = State(5, 5, 10, True)

        state.update()


    def test_draw(self):
        """"""
