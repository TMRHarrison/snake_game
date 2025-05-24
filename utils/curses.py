"""Curses utility functions"""


import curses
from enum import StrEnum


class Alignment(StrEnum):
    """Valid text alignments."""
    @classmethod
    def _missing_(cls, value):
        """Raise a descriptive error when the value isn't found.

        :param value: The given value, for which there is no Enum member.

        :raise ValueError: Always.
        """
        #pylint: disable=no-member
        raise ValueError(
            f"{value} is not a valid value for Alignment. Must be one of"\
            f"{cls._member_names_}"
        )
        #pylint: enable=no-member

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


def printf( #pylint: disable=too-many-arguments,too-many-positional-arguments
    window: curses.window,
    string: str,
    x: int,
    y: int,
    width: int,
    align: str | Alignment
):
    """Print the string, aligned in the specified way. This doesn't scissor, or
    fold the text, it just aligns it to the edges/center. "overflowing" text
    will still be written to the window.

    :param window: Curses window to draw the text to.
    :param string: String to write.
    :param x: Leftmost position to align the text to.
    :param y: Topmost position to align the text to.
    :param width: width of the space to align the text in.
    :param align: One of the memebers of Alignment: "left", "center", or "right"
    """
    align = Alignment(align)

    max_y, max_x = window.getmaxyx()

    for y_offset, line in enumerate(string.split("\n")):
        y_pos = y + y_offset
        if y_pos >= max_y:
            break

        # left alignment is the default
        draw_x = x
        if align == Alignment.CENTER:
            draw_x += (width - len(line)) // 2
        elif align == Alignment.RIGHT:
            draw_x += width - len(line)

        # don't try to draw at indices below 0. If the x position is positive,
        # this makes no changes.
        min_index = max(-draw_x, 0)
        max_index = max(max_x - draw_x, 0)
        drawable_line = line[min_index:max_index]
        draw_x = max(draw_x, 0)

        try:
            window.addstr(y_pos, draw_x, drawable_line)
        except curses.error:
            # curses will always raise an error if writing a character to
            # the bottommost rightmost space, due to curses trying to
            # advance to a space which doesn't exist. This will ignore that.
            pass
