"""Test the base state"""

import curses
import time
import unittest

from state.state import State
from tests import MockWindow, timeout_wrapper, window_to_list


# we are deliberately accesssing protected members to test their functionality
#pylint: disable=protected-access
class TestState(unittest.TestCase):
    """Test state methods"""

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

        class MockWindowGetch(MockWindow): #pylint: disable=too-few-public-methods
            """Mock a window object with getch's functionality changed."""

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
        """Make sure the draw function renders to the window"""

        state = State(5, 5, 10, True)

        self.assertListEqual(
            window_to_list(state.window), #type: ignore
            [
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )

        state.draw()
        self.assertListEqual(
            window_to_list(state.window),
            [ # the chr() are box-drawing characters
                [chr(0x250C), chr(0x2500), chr(0x2500), chr(0x2500), chr(0x2510)],
                [chr(0x2502), " ",         " ",         " ",         chr(0x2502)],
                ["f",         "u",         "n",         "c",         "t"        ],
                [chr(0x2502), " ",         " ",         " ",         chr(0x2502)],
                [chr(0x2514), chr(0x2500), chr(0x2500), chr(0x2500), chr(0x2518)]
            ]
        )


    def test_done(self):
        """Check that done sets the flag properly"""

        state = State(5, 5, 10, True)

        self.assertFalse(state.done)

        state.end()

        self.assertTrue(state.done)


    def test_scankeys_no_delay_state(self):
        """Scan keys on a state with no delay set"""

        class MockWindowGetch(MockWindow): #pylint: disable=too-few-public-methods
            """Mock a window object with getch's functionality changed."""

            def __init__(self, window):
                super().__init__(window)
                self.__calls = 0

            def getch(self) -> int:
                """Simulate 5 frames of no key pressed, then press 'q' once every frame."""
                self.__calls += 1
                keys = {
                    1: ord("a"),
                    2: ord("s"),
                    3: ord("d"),
                    4: ord("f")
                }
                return keys.get(self.__calls, -1)

        state = State(5, 5, 10, True)

        # the mock isn't technically a window object, but the MockWindow is
        # explicitly compatible
        state.window = ( #type: ignore
            MockWindowGetch(state.window)
        )

        self.assertEqual(state._keys_pressed, [])

        state._scankeys()
        self.assertEqual(state._keys_pressed, [ord("a"), ord("s"), ord("d"), ord("f")])

        state._scankeys()
        self.assertEqual(state._keys_pressed, [])


    def test_scankeys_delay_state(self):
        """Scan keys on a state with no delay unset"""

        class MockWindowGetch(MockWindow): #pylint: disable=too-few-public-methods
            """Mock a window object with getch's functionality changed."""

            def __init__(self, window):
                super().__init__(window)
                self.__calls = 0

            def getch(self) -> int:
                """Simulate 5 frames of no key pressed, then press 'q' once every frame."""
                self.__calls += 1
                keys = {
                    1: ord("a"),
                    2: ord("s"),
                    3: ord("d"),
                    4: ord("f")
                }
                return keys.get(self.__calls, -1)

        state = State(5, 5, 10, False)

        # the mock isn't technically a window object, but the MockWindow is
        # explicitly compatible
        state.window = ( #type: ignore
            MockWindowGetch(state.window)
        )

        self.assertEqual(state._keys_pressed, [])

        state._scankeys()
        self.assertEqual(state._keys_pressed, [ord("a")])
        state._scankeys()
        self.assertEqual(state._keys_pressed, [ord("s")])
        state._scankeys()
        self.assertEqual(state._keys_pressed, [ord("d")])
        state._scankeys()
        self.assertEqual(state._keys_pressed, [ord("f")])

        state._scankeys()
        self.assertEqual(state._keys_pressed, [])


    def test_scankeys_no_delay(self):
        """Scan keys in the nodelay method"""

        class MockWindowGetch(MockWindow): #pylint: disable=too-few-public-methods
            """Mock a window object with getch's functionality changed."""

            def __init__(self, window):
                super().__init__(window)
                self.__calls = 0

            def getch(self) -> int:
                """Simulate 5 frames of no key pressed, then press 'q' once every frame."""
                self.__calls += 1
                keys = {
                    1: ord("a"),
                    2: ord("s"),
                    4: ord("f")
                }
                return keys.get(self.__calls, -1)

        state = State(5, 5, 10, True)

        # the mock isn't technically a window object, but the MockWindow is
        # explicitly compatible
        state.window = ( #type: ignore
            MockWindowGetch(state.window)
        )

        self.assertEqual(state._keys_pressed, [])

        state._scankeys_no_delay()
        self.assertEqual(state._keys_pressed, [ord("a"), ord("s")])

        state._scankeys_no_delay()
        self.assertEqual(state._keys_pressed, [ord("a"), ord("s"), ord("f")])


    def test_scankeys_with_delay(self):
        """Scan keys in the nodelay method"""

        class MockWindowGetch(MockWindow): #pylint: disable=too-few-public-methods
            """Mock a window object with getch's functionality changed."""

            def __init__(self, window):
                super().__init__(window)
                self.__calls = 0

            def getch(self) -> int:
                """Simulate 5 frames of no key pressed, then press 'q' once every frame."""
                self.__calls += 1
                keys = {
                    1: ord("a"),
                    2: ord("s"),
                    4: ord("f")
                }
                return keys.get(self.__calls, -1)

        state = State(5, 5, 10, True)

        # the mock isn't technically a window object, but the MockWindow is
        # explicitly compatible
        state.window = ( #type: ignore
            MockWindowGetch(state.window)
        )

        self.assertEqual(state._keys_pressed, [])

        state._scankeys_with_delay()
        self.assertEqual(state._keys_pressed, [ord("a")])
        state._scankeys_with_delay()
        self.assertEqual(state._keys_pressed, [ord("a"), ord("s")])
        state._scankeys_with_delay()
        self.assertEqual(state._keys_pressed, [ord("a"), ord("s")])
        state._scankeys_with_delay()
        self.assertEqual(state._keys_pressed, [ord("a"), ord("s"), ord("f")])


    def test_frame(self):
        """clear, draw, present, wait"""

        state = State(5, 5, 10, True)

        state.window.addstr(1, 1, "abc")
        self.assertListEqual(
            window_to_list(state.window), #type: ignore
            [
                [" ", " ", " ", " ", " "],
                [" ", "a", "b", "c", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )

        start = time.time_ns()
        state._frame()
        self.assertListEqual(
            window_to_list(state.window), #type: ignore
            [ # the chr() are box-drawing characters
                [chr(0x250C), chr(0x2500), chr(0x2500), chr(0x2500), chr(0x2510)],
                [chr(0x2502), " ",         " ",         " ",         chr(0x2502)],
                ["f",         "u",         "n",         "c",         "t"        ],
                [chr(0x2502), " ",         " ",         " ",         chr(0x2502)],
                [chr(0x2514), chr(0x2500), chr(0x2500), chr(0x2500), chr(0x2518)]
            ]
        )
        # waited at least 99 miliseconds
        self.assertGreaterEqual(
            time.time_ns() - start,
            99_000_000
        )


    def test_preframe(self):
        """clear"""
        state = State(5, 5, 10, True)

        state.window.addstr(1, 1, "abc")
        self.assertListEqual(
            window_to_list(state.window), #type: ignore
            [
                [" ", " ", " ", " ", " "],
                [" ", "a", "b", "c", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )

        state._preframe()
        self.assertListEqual(
            window_to_list(state.window), #type: ignore
            [
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )


    def test_postframe(self):
        """present, wait"""

        state = State(5, 5, 10, True)

        state.window.addstr(1, 1, "abc")
        self.assertListEqual(
            window_to_list(state.window), #type: ignore
            [
                [" ", " ", " ", " ", " "],
                [" ", "a", "b", "c", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )

        start = time.time_ns()
        state._postframe()
        self.assertListEqual(
            window_to_list(state.window), #type: ignore
            [
                [" ", " ", " ", " ", " "],
                [" ", "a", "b", "c", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )
        # waited at least 99 miliseconds
        self.assertGreaterEqual(
            time.time_ns() - start,
            99_000_000
        )
