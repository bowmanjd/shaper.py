"""Utility functions for managing local Python virtual environment."""
import json
import subprocess
import venv
from pathlib import Path

import shaper.util

VENV = Path.home() / ".venv"
PIP = VENV / "bin" / "pip"


def create_venv() -> None:
    """Install local virtual env if missing, and update."""
    if not VENV.exists():
        venv.create(VENV, system_site_packages=True, with_pip=True, upgrade_deps=True)


def existing_pip() -> set:
    """Obtain list of installed python packages.

    Returns:
        a set of package names
    """
    command = [PIP, "list", "--format", "json"]
    packages = subprocess.check_output(command)
    return {p["name"] for p in json.loads(packages)}


def install_pip_packages(filename: str) -> None:
    """Install python packages from text file.

    Args:
        filename: path to text file listing packages
    """
    create_venv()
    cmd = [PIP, "install", "-Ur", filename]
    subprocess.check_call(cmd)


if __name__ == "__main__":
    import sys

    install_pip_packages(sys.argv[1])
