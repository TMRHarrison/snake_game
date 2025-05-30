"""File and directory manipulation"""

import sys
import pathlib


def get_savedir(dir_name: str) -> str | None:
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
        return None

    save_dir = f"{home}/{subdir}/{dir_name}"
    return save_dir
