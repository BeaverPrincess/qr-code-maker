import os
import sys


def get_base_dir() -> str:
    """
    Returns the folder where outputs should be saved.
    - When running as an .exe (PyInstaller), save next to the exe.
    - When running as .py, save next to the project file.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))