"""Utility functions."""

import pathlib
import subprocess


def get_set_from_file(filename: str) -> set:
    """Build a set from a simple multiline text file.

    Args:
        filename: name of the text file

    Returns:
        a set of the unique lines from the file
    """
    filepath = pathlib.Path(filename)
    lines = filepath.read_text().splitlines()
    return set(lines)


def get_set_from_output(command: list) -> set:
    """Obtain set from lines of command output

    Args:
        command: list with command and arguments

    Returns:
        a set of lines from output
    """
    output_list = subprocess.check_output(command, text=True).splitlines()
    return set(output_list)
