"""Test the highscore state"""

import os
import tempfile
import unittest

from state.hiscore import HighScore
from tests import window_to_list


# we are deliberately accesssing protected members to test their functionality
#pylint: disable=protected-access
class TestHiscore(unittest.TestCase):
    """Test the high score state"""

    def test_creation_valid_dir(self):
        """make a high score state and check its attributes"""

        with tempfile.TemporaryDirectory() as temp_dir:
            save_dir = f"{temp_dir}/test"

            hiscore = HighScore(5, 5, 15, save_dir)

            self.assertFalse(hiscore.replay)

            self.assertEqual(hiscore.score, 15)
            self.assertListEqual(hiscore.scores, [15])
            self.assertEqual(hiscore.max_highscores, 10)

            self.assertEqual(hiscore.save_dir, save_dir)
            self.assertEqual(hiscore.file_path, f"{save_dir}/hiscore.txt")

            with open(f"{save_dir}/hiscore.txt", "rt", encoding="UTF-8") as save_file:
                self.assertListEqual(save_file.readlines(), ["15\n"])


    def test_creation_invalid_dir(self):
        """make a high score state and check its attributes"""

        hiscore = HighScore(5, 5, 15, None)

        self.assertFalse(hiscore.replay)

        self.assertEqual(hiscore.score, 15)
        self.assertListEqual(hiscore.scores, [15])
        self.assertEqual(hiscore.max_highscores, 10)

        self.assertEqual(hiscore.save_dir, None)
        self.assertEqual(hiscore.file_path, None)


    def test_key_pressed_q(self):
        """press q to quit the state"""

        hiscore = HighScore(5, 5, 15, None)

        hiscore.key_pressed(ord("q"))

        self.assertTrue(hiscore.done)
        self.assertFalse(hiscore.replay)


    def test_key_pressed_space(self):
        """press space to quit the state and set replay to true"""

        hiscore = HighScore(5, 5, 15, None)

        hiscore.key_pressed(ord(" "))

        self.assertTrue(hiscore.done)
        self.assertTrue(hiscore.replay)


    def test_draw_valid_dir(self):
        """Draw the screen when the save directory wasn't None"""

        with tempfile.TemporaryDirectory() as temp_dir:
            save_dir = f"{temp_dir}/test"

            hiscore = HighScore(40, 10, 15, save_dir)
            hiscore.scores = [15, 6, 4] # these can be set, the loading is tested elsewhere

            hiscore.draw()

            self.assertListEqual(
                ["".join(str(char) for char in line) for line in window_to_list(hiscore.window)],
                [
                    "                                        ",
                    "                                        ",
                    "   Press space to replay, 'q' to quit   ",
                    "                                        ",
                    "   This game's score: 15                ",
                    "                                        ",
                    "     1: 15                              ",
                    "     2: 6                               ",
                    "     3: 4                               ",
                    "                                        "
                ]
            )


    def test_draw_invalid_dir(self):
        """Draw the screen when the save directory was None"""

        hiscore = HighScore(55, 10, 15, None)

        hiscore.draw()

        self.assertListEqual(
            ["".join(str(char) for char in line) for line in window_to_list(hiscore.window)],
            [
                "Unrecognised operating system, unable to save scores.  ",
                "                                                       ",
                "   Press space to replay, 'q' to quit                  ",
                "                                                       ",
                "   This game's score: 15                               ",
                "                                                       ",
                "     1: 15                                             ",
                "                                                       ",
                "                                                       ",
                "                                                       "
            ]
        )


    def test_get_saved_scores_valid_dir(self):
        """Get the scores from the score file"""

        with tempfile.TemporaryDirectory() as temp_dir:
            save_dir = f"{temp_dir}/test"

            hiscore = HighScore(40, 10, 15, save_dir)

            # reset the file contents
            with open(f"{save_dir}/hiscore.txt", "wt", encoding="UTF-8") as stream:
                stream.writelines(["20\n", "10\n", "5\n"])

            hiscore._get_saved_scores()

            # current score isn't added yet
            self.assertListEqual(hiscore.scores, [20, 10, 5])


    def test_get_saved_scores_invalid_dir(self):
        """Do nothing when the score file doesn't exist"""

        hiscore = HighScore(40, 10, 15, None)

        self.assertListEqual(hiscore.scores, [15])
        hiscore._get_saved_scores()

        # doesn't try to load the file; this quits immediately since there's no file
        self.assertListEqual(hiscore.scores, [15])


    def test_save_scores_valid_dir(self):
        """Remove the file manually, then rewrite it using the function"""

        with tempfile.TemporaryDirectory() as temp_dir:
            save_dir = f"{temp_dir}/test"
            hiscore_file = f"{save_dir}/hiscore.txt"

            hiscore = HighScore(40, 10, 15, save_dir)
            os.remove(hiscore_file)

            hiscore._save_scores()
            with open(hiscore_file, "rt", encoding="UTF-8") as stream:
                self.assertListEqual(
                    stream.readlines(),
                    ["15\n"]
                )


    def test_save_scores_invalid_dir(self):
        """There's no file to write to, so just don't error out, basically."""

        hiscore = HighScore(40, 10, 15, None)

        self.assertTrue(hiscore.file_path is None)
        hiscore._save_scores()


    def _get_file_path_valid_dir(self):
        """Get the file path when there's a valid save directory"""

        with tempfile.TemporaryDirectory() as temp_dir:
            save_dir = f"{temp_dir}/test"
            expected_file = f"{save_dir}/newfile"

            hiscore = HighScore(40, 10, 15, save_dir)

            self.assertEqual(hiscore.file_path, f"{save_dir}/hiscore.txt")
            self.assertFalse(os.path.isfile(expected_file))

            # set the attribute and make the empty file
            hiscore._get_file_path("newfile")
            self.assertEqual(hiscore.file_path, expected_file)
            self.assertTrue(os.path.isfile(expected_file))
            with open(expected_file, "rt", encoding="UTF-8") as stream:
                self.assertEqual(stream.readlines(), [])

            # Don't empty the file if it already exists
            with open(expected_file, "wt", encoding="UTF-8") as stream:
                stream.writelines(["10\n", "5\n"])

            hiscore._get_file_path("newfile")
            self.assertEqual(hiscore.file_path, expected_file)
            self.assertTrue(os.path.isfile(expected_file))
            with open(expected_file, "rt", encoding="UTF-8") as stream:
                self.assertEqual(stream.readlines(), ["10\n", "5\n"])


    def _get_file_path_invalid_dir(self):
        """Don't change the file path if there's no valid save directory"""

        hiscore = HighScore(40, 10, 15, None)

        self.assertEqual(hiscore.file_path, None)

        hiscore._get_file_path("newfile")
        self.assertEqual(hiscore.file_path, None)


    def test_sort_scores(self):
        """Sort and trim the score list"""
        hiscore = HighScore(40, 10, 15, None)

        hiscore.scores = [
            20,
            23,
            66,
            10,
            5,
            8,
            2,
            5,
            2,
            5,
            14,
            17,
            22
        ]

        hiscore._sort_scores()

        # filter to 10 in descending order
        self.assertListEqual(
            hiscore.scores,
            [
                66,
                23,
                22,
                20,
                17,
                14,
                10,
                8,
                5,
                5
            ]
        )
