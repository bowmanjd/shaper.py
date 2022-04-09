"""Utility functions for managing local Rust packages with Cargo."""
import subprocess

import shaper.util


def existing_rust() -> set:
    """Obtain list of installed rust packages.

    Returns:
        a set of package names
    """
    cmd = ["cargo", "install", "--list"]
    packages = shaper.util.get_set_from_output(cmd)
    return {l.strip() for l in packages if l.startswith("  ")}


def install_rust_packages(filename: str) -> None:
    """Install rust packages from text file.

    Args:
        filename: path to text file listing packages
    """
    existing = existing_rust()
    to_install = shaper.util.get_set_from_file(filename)
    new_packages = to_install - existing

    for package in new_packages:
        cmd = ["cargo", "install", package]
        subprocess.check_call(cmd)


if __name__ == "__main__":
    import sys

    install_rust_packages(sys.argv[1])
