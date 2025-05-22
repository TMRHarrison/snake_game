"""Pellet class"""

import curses


class Pellet:
    """Pellets can be picked up by the player to increase score and snake
    length.

    :param x_pos: X position of the pellet
    :param y_pos: Y position of the pellet
    """

    def __init__(self, x_pos: int, y_pos: int):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.icon = "N"
        """Icon that is shown on the window"""


    def __eq__(self, other) -> bool:
        """Pellets can be equal to other pellets"""
        if isinstance(other, Pellet):
            return self.x_pos == other.x_pos and self.y_pos == other.y_pos
        return super().__eq__(other)


    def draw(self, window: curses.window):
        """Draw the pellet to the specified window.

        :param window: Curses window to draw the pellet to.
        """
        window.addch(self.y_pos, self.x_pos, self.icon)
