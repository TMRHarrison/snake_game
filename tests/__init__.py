"""Test functionality"""

import curses
import signal
import threading
import time
from contextlib import contextmanager


@contextmanager
def timeout_wrapper(timeout_seconds: float):
    """When used in a with statement, this will interrupt the given process after"""

    complete = False

    old_handler = signal.getsignal(signal.SIGUSR1)

    def timeout(sec):
        time.sleep(sec)
        if not complete:
            signal.raise_signal(signal.SIGUSR1)

    def sig_handler(*_):
        raise TimeoutError()

    try:
        signal.signal(signal.SIGUSR1, sig_handler)
        interrupt = threading.Thread(target=timeout, args=[timeout_seconds])
        interrupt.start()

        yield None

        complete = True
    finally:
        signal.signal(signal.SIGUSR1, old_handler)


class MockWindow: #pylint: disable=too-few-public-methods
    """Dirty subclass of curses.window. Normally, the class can't be subclassed."""

    def __init__(self, window) -> None:
        self.window = window

        defined_funcs = dir(self)

        # pass all non-protected, non-dunder methods (except getch)
        # through as attributes of this class.
        for attr in dir(window):
            if not attr.startswith("__") and attr not in defined_funcs:
                setattr(self, attr, getattr(window, attr))


def window_to_list(window: curses.window, no_chr: bool = False) -> list[list[str | int]]:
    """Convert the window object to a list of lists of strings"""
    border_chr_map = {
        curses.ACS_VLINE: 0x2502,
        curses.ACS_HLINE: 0x2500,
        curses.ACS_ULCORNER: 0x250C,
        curses.ACS_URCORNER: 0x2510,
        curses.ACS_LLCORNER: 0x2514,
        curses.ACS_LRCORNER: 0x2518
    }

    max_y, max_x = window.getmaxyx()
    if no_chr:
        return [
            [
                border_chr_map.get(window.inch(y, x), window.inch(y, x))
                for x in range(max_x)
            ]
            for y in range(max_y)
        ]

    return [
        [
            chr(border_chr_map.get(window.inch(y, x), window.inch(y, x)))
            for x in range(max_x)
        ]
        for y in range(max_y)
    ]
