"""The high score screen, which shows the current score and the list of
historic high scores.
"""

import os
import pathlib
import sys
from state.state import State
from utils.curses import printf


class HighScore(State):
    """The high score state.

    :param width: Width of the window.
    :param height: Height of the window.
    :param score: The current score.
    :param dir_name: The name of the directory the high score file should be
        saved to.
    """

    def __init__(
        self,
        width: int,
        height: int,
        score: int,
        dir_name: str
    ):
        super().__init__(width, height, no_delay=False)

        self.replay = False
        """True when the game should restart after this screen."""

        self.dir_name = dir_name
        """Name of the directory to save the high score file to."""
        self.score = score
        """The score from the previous game."""
        self.scores = []
        """The list of high scores."""
        self.max_highscores = 10
        """The maximum number of high scores to show and save."""

        self.save_dir = None
        """Resolved save directory path."""
        self._get_savedir()
        self.high_score_file = "hiscore.txt"
        """Name of the high score file inside the folder."""
        self.file_path = None
        """Resolved path to the high score file."""
        self._get_file_path()
        self._get_saved_scores()

        self.scores.append(score)

        self._sort_scores()
        self._save_scores()


    def key_pressed(self, key: int):
        """Exit when pressing 'q', restart the game when pressing space.

        :param key: the pressed key.
        """
        super().key_pressed(key)

        if key == ord(" "):
            self.replay = True
            self.end()


    def draw(self):
        """Draw the high score screen."""

        # If the save folder can't be resolved, warn the user.
        if self.file_path is None:
            printf(
                self.window,
                "Unrecognised operating system, unable to save scores.",
                0,
                0,
                self.width,
                "left"
            )

        printf(
            self.window,
            "Press space to replay, 'q' to quit",
            3,
            2,
            self.width,
            "left"
        )

        # score and high score printout
        printf(
            self.window,
            f"This game's score: {self.score}",
            3,
            4,
            self.width - 3,
            "left"
        )

        for num, score in enumerate(self.scores):
            printf(
                self.window,
                f"{num+1:>2}: {score}",
                4,
                6 + num,
                self.width,
                "left"
            )


    def _get_saved_scores(self):
        """Read the high scores from the high score file."""
        # don't operate on a file if the save folder isn't found.
        if self.file_path is None:
            return

        with open(self.file_path, "rt", encoding="UTF-8") as file:
            self.scores = [
                int(line)
                for line in file.readlines()
            ]


    def _save_scores(self):
        """Save the high scores back to the file."""
        if self.file_path is None:
            return

        with open(self.file_path, "wt", encoding="UTF-8") as file:
            file.writelines(
                f"{score}\n"
                for score in self.scores
            )


    def _get_savedir(self):
        """Get the system-dependent save folder. If the operating system is
        unrecognised, don't try to do any file operations.
        """
        home = pathlib.Path.home()

        if sys.platform == "win32":
            subdir = "AppData/Roaming"
        elif sys.platform == "darwin":
            subdir = "Library/Application Support"
        elif sys.platform == "linux":
            subdir = ".local/share"
        else:
            # If the operating system is unrecognised, don't set the save directory.
            return

        self.save_dir = f"{home}/{subdir}/{self.dir_name}"
        os.makedirs(self.save_dir, exist_ok=True)


    def _get_file_path(self):
        """Get the path of the file to save the high scores to, and create it
        if it doesn't exist.
        """
        if self.save_dir is None:
            return

        self.file_path = f"{self.save_dir}/{self.high_score_file}"

        # touch the file if it doesn't exist
        if not os.path.isfile(self.file_path):
            with open(self.file_path, "wt"):
                pass


    def _sort_scores(self):
        """Sort the scores in descending order, and only keep the maximum
        number of them.
        """
        self.scores.sort(reverse=True)
        self.scores = self.scores[:self.max_highscores]
