"""Expected errors the game can produce. These are meant to be captured."""


class SnakeError(Exception):
    """Generic base error from the snake game"""


class WindowSizeError(SnakeError):
    """Exception for the window being too small to fit the game screen."""
