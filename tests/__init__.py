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


class MockWindow:
    """Dirty subclass of curses.window. Normally, the class can't be subclassed."""

    def __init__(self, window) -> None:
        self.window = window

        defined_funcs = [
            name
            for name in dir(self)
        ]

        # pass all non-protected, non-dunder methods (except getch)
        # through as attributes of this class.
        for attr in dir(window):
            if not attr.startswith("__") and attr not in defined_funcs:
                setattr(self, attr, getattr(window, attr))


    def __instancecheck__(self, instance) -> bool:
        if instance == curses.window:
            return True
        return False


def window_to_list(window: curses.window) -> list[list[str]]:
    """Convert the window object to a list of lists of strings"""
    max_y, max_x = window.getmaxyx()
    return [
        [
            chr(window.inch(y, x))
            for x in range(max_x)
        ]
        for y in range(max_y)
    ]
