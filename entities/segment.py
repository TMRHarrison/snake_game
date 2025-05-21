""""""

import curses
import random

from entities.pellet import Pellet


class Segment:
    """A single segment of the worm"""
    __icons = [
        "G", "A", "T", "C"
    ]

    def __init__(self, x_pos: int, y_pos: int):
        self.x_pos = int(x_pos)
        self.y_pos = int(y_pos)
        self.icon = random.choice(self.__icons)
        """Icon that is shown on the window"""


    def __eq__(self, other: "Segment | Pellet | object") -> bool:
        """Equality operator. We only care about positions, icons are irrelevant."""
        if isinstance(other, (Segment, Pellet)):
            return self.x_pos == other.x_pos and self.y_pos == other.y_pos
        else:
            return super().__eq__(other)


    def __repr__(self) -> str:
        """"""
        return f"<Segment '{self.icon}' at ({self.x_pos},{self.y_pos})>"


    def move(self, x_pos: int, y_pos: int):
        """Move the segment to the specified position.

        :param x_pos: X position to move to.
        :param y_pos: Y position to move to.
        """
        self.x_pos = int(x_pos)
        self.y_pos = int(y_pos)


    def draw(self, window: curses.window):
        """Draw the segment to the given window.

        :param window: The window to draw the segments to.
        """
        window.addch(self.y_pos, self.x_pos, self.icon)
