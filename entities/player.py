"""Player object and Facing"""

from collections import deque
import curses
from enum import Enum

from entities.pellet import Pellet
from entities.segment import Segment


class Facing(Enum):
    """Direction the Player is facing.

    :param value: The name of the position.
    :param x: Change in X position when the player moves when facing this
        direction.
    :param y: Change in Y position when the player moves when facing this
        direction.
    """

    def __new__(cls, value: str, x: int, y: int):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.x = x
        obj.y = y

        return obj

    LEFT = "left", -1, 0
    RIGHT = "right", 1, 0
    UP = "up", 0, -1
    DOWN = "down", 0, 1


class Player:
    """The player's snake that moves around the field and picks up pellets to
    get longer.

    :param head_x_pos: the X position of the player's head segment.
    :param head_y_pos: the Y position of the player's head segment.
    :param num_segments: number of segments the player starts with.
    """

    def __init__(self, head_x_pos: int, head_y_pos: int, num_segments: int):

        self.facing = Facing.LEFT
        self._facing_buffer = deque(maxlen=2)
        """FIFO queue with the directions the snake will turn before moving.
        When empty, the snake stays facing the same direction."""

        self.segments = [
            Segment(head_x_pos + num, head_y_pos)
            for num in range(0, num_segments)
        ]


    def head(self) -> Segment:
        """Gets the snake's head segment.

        :return: The snake's head segment.
        """
        return self.segments[0]


    def tail(self) -> Segment:
        """Gets the snake's tail segment.

        :return: The snake's tail segment.
        """
        return self.segments[-1]


    def add_facing_to_buffer(self, facing: Facing):
        """Adds a new facing the the buffer. This will add a new facing to the
        buffer if:
         * The buffer isn't full.
         * The new facing won't make the snake turn directly back on itself.
         * The facing will change.
        This is compared against the current facing if the buffer is full, or
        against the most recent buffered facing otherwise.

        :param facing: The new facing to potentially add to the buffer.
        """
        if (
            self._facing_buffer.maxlen
            and len(self._facing_buffer) >= self._facing_buffer.maxlen
        ):
            return

        if len(self._facing_buffer) == 0:
            prev_facing = self.facing
        else:
            prev_facing = self._facing_buffer[-1]

        # Don't add facings that are directly backward, or the same direction.
        if (
            abs(prev_facing.x) != abs(facing.x)
            and abs(prev_facing.y) != abs(facing.y)
        ):
            self._facing_buffer.append(facing)


    def move(self):
        """Move the snake forward one position, based on the direction it is
        facing. If the buffer isn't empty, pop the least recent facing before
        moving."""
        if self._facing_buffer:
            self.facing = self._facing_buffer.popleft()

        head = self.head()

        new_x = head.x_pos + self.facing.x
        new_y = head.y_pos + self.facing.y
        for segment in self.segments:
            old_x = segment.x_pos
            old_y = segment.y_pos
            segment.move(new_x, new_y)
            new_x = old_x
            new_y = old_y


    def draw(self, window: curses.window):
        """Draw each segment of the snake.

        :param window: The curses window to draw the segments to.
        """
        for segment in self.segments:
            segment.draw(window)


    def space_occupied(self, x_pos: int, y_pos: int) -> bool:
        """Check if the given position is occupied by any of the snake's
        segments.

        :param x_pos: X position to check.
        :param y_pos: Y position to check.

        :return: True if the coordinate is occupied by any of the snake's
            segments. False otherwise.
        """

        return any(
            segment.x_pos == x_pos and segment.y_pos == y_pos
            for segment in self.segments
        )


    def check_pellet(self, pellet: Pellet) -> bool:
        """Check if the given pellet is on the same space as the snake's head.

        :param pellet: The pellet to check.

        :return: True if the pellet is on the same space as the head. False
            otherwise.
        """

        head = self.head()
        if head == pellet:
            self._new_segment()
            return True

        return False


    def _new_segment(self):
        """Add a new segment to the snake's tail. This is placed under the last
        segment.
        """
        tail = self.tail()
        self.segments.append(Segment(tail.x_pos, tail.y_pos))


    def check_out_of_bounds(
        self,
        left: int,
        right: int,
        upper: int,
        lower: int
    ) -> bool:
        """Check if the snake's head is out of the given boundaries.

        :param left: Position of the leftmost boundary.
        :param right: Position of the rightmost boundary.
        :param upper: Position of the uppermost boundary.
        :param lower: Position of the lowermost boundary.

        :return: True if the player's head has moved out of bounds. False
            otherwise.
        """
        head = self.head()
        return (
            head.x_pos < left
            or head.x_pos >= right
            or head.y_pos < upper
            or head.y_pos >= lower
        )


    def check_body_hit(self) -> bool:
        """Check if the snake's head is overlapping any of the other segments.

        :return: True if the head is on the same space as any of the segments.
            False otherwise.
        """
        head = self.head()
        return any(
            head == segment
            for segment in self.segments[1:]
        )
