

import curses
import time

from utils.curses import printf


class State:
    """Base class for game states. This has the base functionality needed for
    control flow etc.

    :param width: Width of the window.
    :param height: Height of the window.
    :param fps: Number of frames per second in no-delay mode. Ignored
        otherwise.
    :param no_delay: Whether to enable no-delay mode in curses. in no-delay
        mode, 0+ keys can be pressed per update, and updates happen on a timer.
    """

    def __init__(
        self,
        width: int,
        height: int,
        fps: float = 10,
        no_delay: bool = True
    ):
        # window properties
        self.width = width
        self.height = height
        self.no_delay = no_delay

        # curses windows
        self.window = curses.newwin(height, width)
        self.window.keypad(True)
        if no_delay:
            self.window.nodelay(True)
        self.windows = [self.window]

        # input and control flow
        self.done = False
        self._keys_pressed = []

        # time and frame information
        self.__frame_time = int(1_000_000_000 // fps)
        self.__last_frame = time.time_ns()


    def run(self):
        """The core loop of the game logic. draw the frame, then capture keys
        and update the state.
        """

        self.done = False

        # Render a frame before any inputs. Otherwise, delay mode won't render any frames
        self._frame()
        while not self.done:
            self._scankeys()
            for key in self._keys_pressed:
                self.key_pressed(key)
            self.update()
            self._frame()


    def key_pressed(self, key: int):
        """Default function when keys are pressed. Press 'q' to quit."""
        if key == ord("q"):
            self.done = True
            return


    def update(self):
        """Game update function. This is a placeholder."""


    def draw(self):
        """Draw the outputs to the window(s). This default function should be
        replaced in other states.
        """

        self.window.border()
        printf(
            self.window, "Default drawing function for States.",
            0,
            self.height // 2,
            self.width,
            "center"
        )


    def end(self):
        """End the game loop on the next iteration."""
        self.done = True


    def _scankeys(self):
        """Empty the list of pressed keys and scan for new inputs."""
        del self._keys_pressed[:]
        if self.no_delay:
            self._scankeys_no_delay()
        else:
            self._scankeys_with_delay()


    def _scankeys_no_delay(self):
        """Scan the keys while no delay mode is on. This captures each keypress
        in the frame.
        """
        while True:
            ch = self.window.getch()
            if ch == -1:
                break
            self._keys_pressed.append(ch)


    def _scankeys_with_delay(self):
        """Captures the keypress while nodelay mode is off. This gets the
        single keypress that is being waited for.
        """
        ch = self.window.getch()
        if ch != -1: # this sometimes shows up in special cases, e.g. resizing
            self._keys_pressed.append(ch)


    def _frame(self):
        """All the graphical updates"""
        self._preframe()
        self.draw()
        self._postframe()


    def _preframe(self):
        """Clears the window buffers before the draw function is called."""
        for window in self.windows:
            window.clear()


    def _postframe(self):
        """Layers the buffered frames onto the output and display it. In
        nodelay mode, wait until it's time for the next frame to be drawn.
        """
        for window in self.windows:
            window.noutrefresh()
        curses.doupdate()

        if self.no_delay:
            expected_frame = self.__last_frame + self.__frame_time
            naptime = (expected_frame - time.time_ns()) // 1_000_000
            if naptime > 0:
                curses.napms(naptime)
            self.__last_frame = time.time_ns()
