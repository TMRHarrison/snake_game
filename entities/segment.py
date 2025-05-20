


import curses
import random


class Segment:
    """A single segment of the worm"""
    __icons = [
        "G", "A", "T", "C"
    ]

    def __init__(self, x_pos: int, y_pos: int):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.icon = random.choice(self.__icons)
        """Icon that is shown on the window"""


    def move(self, x_pos: int, y_pos: int):
        """Move the segment to the specified position.

        :param x_pos: X position to move to.
        :param y_pos: Y position to move to.
        """
        self.x_pos = x_pos
        self.y_pos = y_pos


    def draw(self, window: curses.window):
        """Draw the segment to the given window.

        :param window: The window to draw the segments to.
        """
        window.addch(self.y_pos, self.x_pos, self.icon)
