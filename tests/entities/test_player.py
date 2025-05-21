"""Tests for player and facing enum"""

from collections import deque
import curses
import random
import unittest

from entities.pellet import Pellet
from entities.player import Facing, Player
from entities.segment import Segment


class TestFacing(unittest.TestCase):
    """Test the Facing enum"""

    def test_facing_attributes(self):
        """Make sure the facing enum is constructed correctly"""

        self.assertEqual(Facing("left"), Facing.LEFT)
        self.assertEqual(Facing.LEFT.x, -1)
        self.assertEqual(Facing.LEFT.y, 0)

        self.assertEqual(Facing("right"), Facing.RIGHT)
        self.assertEqual(Facing.RIGHT.x, 1)
        self.assertEqual(Facing.RIGHT.y, 0)

        self.assertEqual(Facing("up"), Facing.UP)
        self.assertEqual(Facing.UP.x, 0)
        self.assertEqual(Facing.UP.y, -1)

        self.assertEqual(Facing("down"), Facing.DOWN)
        self.assertEqual(Facing.DOWN.x, 0)
        self.assertEqual(Facing.DOWN.y, 1)


class TestPlayer(unittest.TestCase):
    """Test player methods"""

    def test_creation(self):
        """Make a player object"""
        player = Player(3, 3, 3)

        self.assertEqual(
            player.facing,
            Facing.LEFT
        )
        self.assertEqual(
            player._facing_buffer,
            deque()
        )
        self.assertListEqual(
            player.segments,
            [
                Segment(3, 3),
                Segment(4, 3),
                Segment(5, 3)
            ]
        )


    def test_head(self):
        """Get the snake's head segment"""

        player = Player(3, 3, 3)

        self.assertEqual(
            player.head(),
            Segment(3, 3)
        )


    def test_tail(self):
        """Get the snake's tail segment"""

        player = Player(3, 3, 3)

        self.assertEqual(
            player.tail(),
            Segment(5, 3)
        )


    def test_add_facing_to_buffer(self):
        """Add various facings to the buffer"""

        player = Player(3, 3, 3)

        # these have no effect (already facing that way, and complete reversal)
        player.add_facing_to_buffer(Facing.LEFT)
        player.add_facing_to_buffer(Facing.RIGHT)
        self.assertEqual(
            player._facing_buffer,
            deque()
        )

        # add facing up to the queue
        player.add_facing_to_buffer(Facing.UP)
        self.assertEqual(
            player._facing_buffer,
            deque([Facing.UP])
        )

        # don't add facing down/up
        player.add_facing_to_buffer(Facing.DOWN)
        player.add_facing_to_buffer(Facing.UP)
        self.assertEqual(
            player._facing_buffer,
            deque([Facing.UP])
        )

        # Face left again (not invalid now)
        player.add_facing_to_buffer(Facing.LEFT)
        self.assertEqual(
            player._facing_buffer,
            deque([Facing.UP, Facing.LEFT])
        )

        # Don't add up again, since the buffer is full
        player.add_facing_to_buffer(Facing.UP)
        self.assertEqual(
            player._facing_buffer,
            deque([Facing.UP, Facing.LEFT])
        )


    def test_move(self):
        """Move the snake"""

        player = Player(3, 3, 3)

        # forward once
        player.move()

        self.assertListEqual(
            player.segments,
            [
                Segment(2, 3),
                Segment(3, 3),
                Segment(4, 3)
            ]
        )

        # turn up and move
        player.add_facing_to_buffer(Facing.UP)
        player.move()

        self.assertListEqual(
            player.segments,
            [
                Segment(2, 2),
                Segment(2, 3),
                Segment(3, 3)
            ]
        )
        self.assertEqual(
            player._facing_buffer,
            deque()
        )

        # left and up buffered moves
        player.add_facing_to_buffer(Facing.LEFT)
        player.add_facing_to_buffer(Facing.UP)
        player.move()
        player.move()

        self.assertListEqual(
            player.segments,
            [
                Segment(1, 1),
                Segment(1, 2),
                Segment(2, 2)
            ]
        )
        self.assertEqual(
            player._facing_buffer,
            deque()
        )


    def test_space_occupied(self):
        """Check if the given position is occupied by any of the snake's
        segments
        """

        player = Player(3, 3, 3)

        self.assertFalse(
            player.space_occupied(3, 2)
        )
        self.assertFalse(
            player.space_occupied(3, 4)
        )


    def test_check_pellet(self):
        """Check if the given pellet is on the same space as the snake's head
        """

        player = Player(3, 3, 3)

        # on a segment, but not the head
        self.assertFalse(
            player.check_pellet(Pellet(3, 4))
        )

        # the tail grows, as well
        self.assertTrue(
            player.check_pellet(Pellet(3, 3))
        )
        self.assertListEqual(
            player.segments,
            [
                Segment(3, 3),
                Segment(4, 3),
                Segment(5, 3),
                Segment(5, 3)
            ]
        )


    def test_new_segment(self):
        """Add a new segment to the snake's tail"""

        player = Player(3, 3, 3)

        player._new_segment()

        self.assertListEqual(
            player.segments,
            [
                Segment(3, 3),
                Segment(4, 3),
                Segment(5, 3),
                Segment(5, 3)
            ]
        )


    def test_check_out_of_bounds(self):
        """Check if the snake's head is out of the given boundaries"""

        player = Player(3, 3, 3)

        # The head is not out of the bounds defined
        self.assertFalse(player.check_out_of_bounds(3, 4, 3, 4))

        # all out of bounds, from different directions
        self.assertTrue(player.check_out_of_bounds(4, 5, 0, 5)) # left
        self.assertTrue(player.check_out_of_bounds(0, 3, 0, 5)) # right
        self.assertTrue(player.check_out_of_bounds(0, 5, 4, 5)) # top
        self.assertTrue(player.check_out_of_bounds(0, 5, 0, 3)) # bottom


    def test_check_body_hit(self):
        """Check if the snake's head is overlapping any of the other segments
        """

        player = Player(3, 3, 5)

        self.assertFalse(player.check_body_hit())

        player.add_facing_to_buffer(Facing.UP)
        player.move()
        self.assertFalse(player.check_body_hit())

        player.add_facing_to_buffer(Facing.RIGHT)
        player.move()
        self.assertFalse(player.check_body_hit())

        player.add_facing_to_buffer(Facing.DOWN)
        player.move()
        self.assertTrue(player.check_body_hit())

        # head has moved off a body segment
        player.move()
        self.assertFalse(player.check_body_hit())


class TestCurses(unittest.TestCase):
    """Test methods that use curses."""

    def setUp(self):
        """initialize curses for each test in this category"""
        curses.initscr()


    def test_draw(self):
        """Draw each segment of the snake"""

        window = curses.newwin(5, 5)
        window.clear()

        random.seed(1)
        player = Player(1, 1, 3)

        self.assertListEqual(
            [[chr(window.inch(y, x)) for x in range(0, 5)] for y in range(0, 5)],
            [
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )
        player.draw(window)
        self.assertListEqual(
            [[chr(window.inch(y, x)) for x in range(0, 5)] for y in range(0, 5)],
            [
                [" ", " ", " ", " ", " "],
                [" ", "A", "G", "T", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " "]
            ]
        )
