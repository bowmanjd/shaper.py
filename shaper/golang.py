"""Utility functions for managing local Go packages."""
import subprocess
from pathlib import Path

import shaper.util

GOPATH = Path.home() / "go" / "bin"


def existing_go() -> set:
    """Obtain list of installed Go packages.

    Returns:
        a set of package names
    """
    cmd = ["go", "version", "-m", GOPATH]
    packages = shaper.util.get_set_from_output(cmd)
    return {
        line.replace("\tpath\t", "").strip()
        for line in packages
        if line.startswith("\tpath")
    }


def install_go_packages(filename: str) -> None:
    """Install Go packages from text file.

    Args:
        filename: path to text file listing packages
    """
    existing = existing_go()
    to_install = shaper.util.get_set_from_file(filename)
    new_packages = to_install - existing

    if new_packages:
        cmd = ["go", "install", "@latest ".join(new_packages) + "@latest"]
        subprocess.check_call(cmd)


if __name__ == "__main__":
    import sys

    install_go_packages(sys.argv[1])
