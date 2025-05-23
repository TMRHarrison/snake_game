"""The core state of the game, with the snake and the pellets."""

import curses
import random
from entities import Pellet
from entities import Facing, Player
from state.state import State
from utils.curses import printf


class Game(State):
    """Core game state. This initializes the field, the snake, the header, etc.

    The game ends when the snake has hit a wall or overlapped itself, when the
    snake has filled the entire screen, or when the player presses the quit
    button.

    :param width: Width of the window.
    :param height: Height of the window.
    :param fps: The target number of updates per second.
    """

    def __init__(self, width: int, height: int, fps: float):
        super().__init__(width, height, fps, True)

        self.border = 1
        """Width of the border around the play field."""
        self.header = 1
        """Height of the header with the score readout and help."""
        self.canvas = curses.newwin(
            height - self.header,
            width,
            self.header,
            0
        )
        """Canvas the game field is rendered to."""
        self.windows.append(self.canvas)

        self.player = Player(width // 2, (height - self.header) // 2, 5)
        """Player object for the snake that moves around."""
        self.score = 0
        """Number of pellets that the player has picked up."""

        self.pellets: list[Pellet] = []
        """The pellets currently on the field."""
        self._new_pellet()

        self.paused = False
        """Whether or not the game is paused."""


    def key_pressed(self, key: int):
        """End the game if 'q' is pressed, pauses if 'p' is pressed, and
        changes the snake's direction if WASD or arrow keys are pressed.

        :param key: The key that has been pressed and needs to be processed.
        """
        if key == ord("q"):
            self.end()
            return

        if key == ord("p"):
            self.paused = not self.paused

        # Don't try to turn the snake if the game is paused
        if self.paused:
            return

        if key in [ord("a"), curses.KEY_LEFT]:
            self.player.add_facing_to_buffer(Facing.LEFT)
        elif key in [ord("d"), curses.KEY_RIGHT]:
            self.player.add_facing_to_buffer(Facing.RIGHT)
        elif key in [ord("w"), curses.KEY_UP]:
            self.player.add_facing_to_buffer(Facing.UP)
        elif key in [ord("s"), curses.KEY_DOWN]:
            self.player.add_facing_to_buffer(Facing.DOWN)


    def update(self):
        """Update the game's state. Move the snake, check if it's out of bounds
        or overlapped itself, remove any eaten pellets, generate new pellets.
        """

        # Don't update when the game is paused
        if self.paused:
            return

        self.player.move()

        # end when the snake is out of bounds, or overlapping itself
        if self.player.check_out_of_bounds(*self._bounds()):
            self.end()
            return

        if self.player.check_body_hit():
            self.end()
            return

        # consume and generate new pellets
        for pellet in self.pellets:
            if self.player.check_pellet(pellet):
                self.score += 1
                self.pellets.remove(pellet)
                self._new_pellet()

        # end if no pellets could be generated
        if not self.pellets:
            self.end()
            return


    def draw(self):
        """Draw the game screen."""

        # score readout and help
        printf(self.window, f"Score: {self.score}", 0, 0, self.width, "left")
        printf(self.window, "'p' to pause; 'q' to quit", 0, 0, self.width, "right")

        # game screen border
        self.canvas.border()

        # pause screen
        if self.paused:
            printf(
                self.canvas,
                "~~PAUSED~~",
                0,
                (self.height - self.header) // 2,
                self.width,
                "center"
            )

        # Draw the player and pellets
        else:
            self.player.draw(self.canvas)

            for pellet in self.pellets:
                pellet.draw(self.canvas)


    def _bounds(self) -> tuple[int, int, int, int]:
        """Get the bounds of the playable game field.

        :return: left, right, upper, and lower bounds of the playable field.
        """
        max_y, max_x = self.canvas.getmaxyx()

        return (
            self.border,
            max_x - self.border,
            self.border,
            max_y - self.border
        )


    def _new_pellet(self):
        """Adds a new pellet to the game field, if there are unoccupied spaces.
        """
        left, right, upper, lower = self._bounds()

        # this is slower than picking a random space and checking if it's
        # valid, but it always results in a valid space, if there is one.
        empty_spaces = [
            (x_pos, y_pos)
            for x_pos in range(left, right)
            for y_pos in range(upper, lower)
            if not self.player.space_occupied(x_pos, y_pos)
            if not any(
                pellet.x_pos == x_pos and pellet.y_pos == y_pos
                for pellet in self.pellets
            )
        ]

        # don't try to add a pellet if there are no valid spaces
        if not empty_spaces:
            return

        self.pellets.append(
            Pellet(
                *random.choice(empty_spaces)
            )
        )
