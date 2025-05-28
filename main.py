#!/usr/bin/env python
"""Pure Python command line Snake game."""

import curses
import argparse
import signal
import sys

from state import Game
from state import StateTest
from state.hiscore import HighScore
from utils.curses import (
    check_boundaries,
    get_old_cursor_visibility
)
from utils.errors import WindowSizeError
from utils.files import get_savedir

WIDTH = 80
HEIGHT = 24

SAVE_FOLDER = "snakey"


def run(
    window: curses.window,
    width: int = WIDTH,
    height: int = HEIGHT,
    test: bool = False
):
    """The core game function that runs in a curses wrapper.

    :param window: The game window.
    :param width: Width of the game window.
    :param height: Height of the game window.
    :param test: Whether or not to launch the test state.
    """
    check_boundaries(window, height, width)

    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    if sys.platform != "win32":
        signal.signal(
            signal.SIGWINCH,
            lambda *_: window.resize(height, width)
        )

    # run the tests and immediately quit
    if test:
        StateTest(width, height, fps=10).run()
        StateTest(width, height, no_delay=False).run()
        return

    replay = True
    while replay:
        game = Game(width, height, 10)
        game.run()

        high_score = HighScore(
            width,
            height,
            game.score,
            get_savedir(SAVE_FOLDER)
        )
        high_score.run()
        replay = high_score.replay


def main():
    """Main command line entrypoint"""
    # capture and save the default cursor visibility
    old_cursor = curses.wrapper(get_old_cursor_visibility)

    # command line options
    parser = argparse.ArgumentParser("Snake game.")
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()

    try:
        curses.wrapper(
            run,
            **vars(args)
        )
    except WindowSizeError as err:
        print(err)
    finally:
        curses.curs_set(old_cursor)


if __name__ == "__main__":
    main()
