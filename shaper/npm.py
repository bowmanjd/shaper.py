"""Utility functions for managing node packages."""

import subprocess
import shaper.download
import shaper.util

NPM = ["volta", "run", "--npm", "latest", "npm"]

def install_volta() -> None:
    """Install volta if missing, and set up node and npm."""
    shaper.download.install_with_remote_script("volta", "https://get.volta.sh", ["--skip-setup"])
    try:
        subprocess.check_output(["node", "-v"])
    except (subprocess.CalledProcessError, FileNotFoundError):
        subprocess.check_call(["volta", "install", "node"])

def existing_npm() -> set:
    """Obtain list of globally-installed npm packages.

    Returns:
        a set of package names
    """
    command = ["volta", "list", "--format", "plain"]

    try:
        lines = shaper.util.get_set_from_output(command)
    except (subprocess.CalledProcessError, FileNotFoundError):
        lines = set()

    return {l.split()[1].split("@")[0] for l in lines if l.startswith("package")}


def install_npm_packages() -> None:
    """Install npm packages from text file."""
    install_volta()
    to_install = shaper.util.get_set_from_file("npm.txt")
    existing = existing_npm()
    cmd = [*NPM, "install", "--global"]
    new_packages = to_install - existing
    for line in new_packages:
        subprocess.check_call(cmd + shlex.split(line))



