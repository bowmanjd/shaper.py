"""Utility functions for managing fonts."""

import pathlib
import urllib.parse
import shaper.download
import shaper.util


HOME = pathlib.Path.home()


def existing_fonts() -> set:
    """Obtain list of currently installed fonts.

    Returns:
        a set of font names
    """
    command = ["fc-list", "-f", "%{fullname[0]}\n"]
    fonts = shaper.util.get_set_from_output(command)
    fonts.remove("")
    return fonts


def install_font(url: str) -> None:
    """Download and install font from URL.

    Args:
        url: URL of font to be downloaded
    """
    shaper.download.download(url, HOME / ".local/share/fonts")


def install_fonts() -> None:
    """Install font URLs from file."""
    possible_fonts = {urllib.parse.unquote(pathlib.Path(f).stem): f for f in shaper.util.get_set_from_file('fonts.txt')}
    to_install = set(possible_fonts) - existing_fonts()
    for font in to_install:
        install_font(possible_fonts[font])
    if to_install:
        subprocess.check_call(["fc-cache", "-f"])
