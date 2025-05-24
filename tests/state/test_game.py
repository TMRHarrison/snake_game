""""Test the Game substate"""

import curses
import random
import unittest
from collections import deque

from entities.pellet import Pellet
from entities.player import Facing, Player
from entities.segment import Segment
from state.game import Game
from state.state import State
from tests import window_to_list


# we are deliberately accesssing protected members to test their functionality
#pylint: disable=protected-access
class TestGame(unittest.TestCase):
    """Test Game methods"""

    def test_creation(self):
        """Create the object and check its properties"""
        game = Game(5, 5, 10)

        self.assertIsInstance(game, State)

        self.assertEqual(game.border, 1)
        self.assertEqual(game.header, 1)

        self.assertIsInstance(game.canvas, curses.window)
        self.assertListEqual(
            game.windows,
            [game.window, game.canvas]
        )

        self.assertIsInstance(game.player, Player)
        self.assertEqual(game.score,  0)

        self.assertIsInstance(game.pellets, list)
        self.assertEqual(len(game.pellets), 1)
        self.assertIsInstance(game.pellets[0], Pellet)

        self.assertFalse(game.paused)


    def test_key_pressed(self):
        """Press some keys and check for their effects."""
        game = Game(5, 5, 10)

        game.key_pressed(ord("p"))
        self.assertTrue(game.paused)

        # no effect while paused
        for key in [
            ord("a"), curses.KEY_LEFT,
            ord("d"), curses.KEY_RIGHT,
            ord("w"), curses.KEY_UP,
            ord("s"), curses.KEY_DOWN
        ]:
            game.key_pressed(key)
            self.assertEqual(game.player._facing_buffer, deque())

        game.key_pressed(ord("p"))
        self.assertFalse(game.paused)

        for left, right, up, down in [
            (ord("a"), ord("d"), ord("w"), ord("s")),
            (curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN)
        ]:
            # turn left/right starting from facing up
            game.player.facing = Facing.UP
            game.key_pressed(left)
            self.assertEqual(game.player._facing_buffer, deque([Facing.LEFT]))
            game.player._facing_buffer.pop()
            game.key_pressed(right)
            self.assertEqual(game.player._facing_buffer, deque([Facing.RIGHT]))
            game.player._facing_buffer.pop()

            # turn up/down starting from facing left
            game.player.facing = Facing.LEFT
            game.key_pressed(up)
            self.assertEqual(game.player._facing_buffer, deque([Facing.UP]))
            game.player._facing_buffer.pop()
            game.key_pressed(down)
            self.assertEqual(game.player._facing_buffer, deque([Facing.DOWN]))
            game.player._facing_buffer.pop()

        game.key_pressed(ord("q"))
        self.assertTrue(game.done)


    def test_update_pause_move(self):
        """Try to move while paused, then unpause and move"""
        game = Game(5, 5, 10)

        # no updates while paused
        game.paused = True
        self.assertTrue(game.player.head(), Segment(2, 2))
        game.update()
        self.assertTrue(game.player.head(), Segment(2, 2))

        # update moves the snake
        game.paused = False
        game.update()
        self.assertTrue(game.player.head(), Segment(1, 2))


    def test_update_out_of_bounds(self):
        """Update while the player is moving out of bounds"""
        game = Game(5, 5, 10)

        # snake is set to move out of bounds next frame
        game.player.facing = Facing.LEFT
        game.player.segments = [
            Segment(1, 2),
            Segment(2, 2),
            Segment(3, 2)
        ]

        game.update()

        # game has ended
        self.assertTrue(game.done)
        # Head segment is out of bounds
        self.assertListEqual(
            game.player.segments,
            [
                Segment(0, 2),
                Segment(1, 2),
                Segment(2, 2)
            ]
        )


    def test_update_snake_overlapping(self):
        """Make the snake overlap itself and end the game"""
        game = Game(5, 5, 10)

        game.player.facing = Facing.DOWN
        game.player.segments = [
            Segment(3, 1),
            Segment(2, 1),
            Segment(2, 2),
            Segment(3, 2),
            Segment(4, 2)
        ]

        game.update()

        # game has ended
        self.assertTrue(game.done)
        # head now overlaps tail
        self.assertListEqual(
            game.player.segments,
            [
                Segment(3, 2),
                Segment(3, 1),
                Segment(2, 1),
                Segment(2, 2),
                Segment(3, 2)
            ]
        )


    def test_update_eat_pellet(self):
        """Update the snake eating a pellet"""
        game = Game(5, 5, 10)

        # new pellet directly in front of the snake
        game.pellets = [
            Pellet(1, 2)
        ]
        game.player.facing = Facing.LEFT
        game.player.segments = [
            Segment(2, 2),
            Segment(3, 2),
            Segment(4, 2)
        ]

        # move onto the pellet and eat it
        random.seed(0) # make the new pellet show up in the same place
        game.update()

        # snake lengthened
        self.assertListEqual(
            game.player.segments,
            [
                Segment(1, 2),
                Segment(2, 2),
                Segment(3, 2),
                Segment(3, 2)
            ]
        )
        # new pellet generated
        self.assertListEqual(game.pellets, [Pellet(2,1)])
        # score up
        self.assertEqual(game.score, 1)


    def test_update_no_pellets(self):
        """Update the game in a state where no more pellets can be generated"""
        game = Game(4, 5, 10)

        # snake is set to eat the last pellet and fill every space on the field
        game.player.facing = Facing.DOWN
        game.player.segments = [
            Segment(1, 1),
            Segment(2, 1),
            Segment(2, 2),
            Segment(2, 2)
        ]
        game.pellets = [
            Pellet(1, 2)
        ]

        game.update()

        self.assertTrue(game.done)
        self.assertListEqual(game.pellets, [])
        # not self-overlapped
        self.assertFalse(game.player.check_body_hit())
        # not out of bounds
        self.assertFalse(game.player.check_out_of_bounds(*game._bounds()))


    def test_draw_header(self):
        """Make sure the header draws in the window"""

        game = Game(35, 5, 10)

        game.draw()

        # window is just the score and controls header. Everything else is blank
        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(game.window)],
            [
                "Score: 0  'p' to pause; 'q' to quit",
                "                                   ",
                "                                   ",
                "                                   ",
                "                                   "
            ]
        )


    def test_draw_canvas_not_paused(self):
        """Draw the game area"""
        random.seed(0) # make the segment icons the same each time
        game = Game(11, 6, 10)

        game.draw()

        # box characters
        h = chr(0x2500)
        v = chr(0x2502)
        ul = chr(0x250C)
        ur = chr(0x2510)
        ll = chr(0x2514)
        lr = chr(0x2518)
        self.assertEqual(
            window_to_list(game.canvas),
            [
                [ul,  h,   h,   h,   h,   h,   h,   h,   h,   h,   ur],
                [v,   " ", " ", " ", " ", "N", " ", " ", " ", " ", v ],
                [v,   " ", " ", " ", " ", "C", "C", "G", "T", "C", v ],
                [v,   " ", " ", " ", " ", " ", " ", " ", " ", " ", v ],
                [ll,  h,   h,   h,   h,   h,   h,   h,   h,   h,   lr]
            ]
        )


    def test_draw_canvas_paused(self):
        """Draw the game area while paused"""
        game = Game(12, 6, 10)

        game.paused = True
        game.draw()

        # box characters
        h = chr(0x2500)
        v = chr(0x2502)
        ul = chr(0x250C)
        ur = chr(0x2510)
        ll = chr(0x2514)
        lr = chr(0x2518)
        self.assertEqual(
            window_to_list(game.canvas),
            [
                [ul,  h,   h,   h,   h,   h,   h,   h,   h,   h,   h,   ur],
                [v,   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", v ],
                [v,   "~", "~", "P", "A", "U", "S", "E", "D", "~", "~", v ],
                [v,   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", v ],
                [ll,  h,   h,   h,   h,   h,   h,   h,   h,   h,   h,   lr]
            ]
        )


    def test_bounds(self):
        """Get the boundaries of the playable area"""
        game = Game(6, 6, 10)

        self.assertTupleEqual(
            game._bounds(),
            (1, 5, 1, 4)
        )


    def test_new_pellet(self):
        """Make new pellets until you can't"""
        random.seed(0)
        game = Game(4, 5, 10)

        self.assertListEqual(
            game.pellets,
            [Pellet(1, 2)]
        )

        # generate pellets to fill every tile in the game
        game._new_pellet()
        self.assertListEqual(
            game.pellets,
            [
                Pellet(1, 2),
                Pellet(2, 1)
            ]
        )
        game._new_pellet()
        self.assertListEqual(
            game.pellets,
            [
                Pellet(1, 2),
                Pellet(2, 1),
                Pellet(1, 1)
            ]
        )

        # no more room for pellets
        game._new_pellet()
        self.assertListEqual(
            game.pellets,
            [
                Pellet(1, 2),
                Pellet(2, 1),
                Pellet(1, 1)
            ]
        )
