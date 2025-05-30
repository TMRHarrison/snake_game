"""State which tests the key press and draw functionality."""


from state.state import State
from utils.curses import printf

class StateTest(State):
    """Test drawing functions and show inputs."""

    def key_pressed(self, key: int):
        """Quit when q is pressed."""
        if key == ord("q"):
            self.done = True


    def draw(self):
        """Draw the outputs to the window(s)."""
        # info
        if self.no_delay:
            self.window.addstr(3, 3, "Testing no-delay mode. Press 'q' to move to next test.")
        else:
            self.window.addstr(3, 3, "Testing delay mode. Press 'q' to quit.")

        # print some text
        self.window.border()
        printf(
            self.window,
            "Extremely long test string that should go off both sides of the "\
                "screen. Really really long, probably 100 characters.\n"\
                "A newline that should be fine.\n"\
                "Another",
            0,
            7,
            80,
            "left"
        )
        printf(
            self.window,
            "Extremely long test string that should go off both sides of the "\
                "screen. Really really long, probably 100 characters.\n"\
                "A newline that should be fine.\n"\
                "Another",
            0,
            11,
            80,
            "center"
        )
        printf(
            self.window,
            "Extremely long test string that should go off both sides of the "\
                "screen. Really really long, probably 100 characters.\n"\
                "A newline that should be fine.\n"\
                "Another",
            0,
            15,
            80,
            "right"
        )

        # Show the keys captured for each frame
        for num, key in enumerate(self._keys_pressed):
            self.window.addstr(1 + num, 1, str(key))
            self.window.addstr(1 + num, 6, chr(key))
