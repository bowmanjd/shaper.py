#!/usr/bin/python3
"""Script for configuring a non-graphical Fedora Linux system."""
from pathlib import Path

import shaper.dnf
import shaper.dotfiles
import shaper.download
import shaper.fonts
import shaper.golang
import shaper.localpy
import shaper.npm
import shaper.rust

BASE = Path.home() / "devel" / "shaper"


def run() -> None:
    """Run commands in order."""
    shaper.dnf.install_rpm_keys(f"{BASE}/packages/rpm_keys.json")
    shaper.dnf.install_dnf_repos(f"{BASE}/repos/headless_repos.txt")
    shaper.dnf.install_copr_repos(f"{BASE}/repos/headless_copr_repos.txt")
    shaper.dnf.install_dnf_packages(f"{BASE}/packages/base_dnf.txt")
    shaper.npm.install_npm_packages(f"{BASE}/packages/base_npm.txt")
    shaper.golang.go_update()
    shaper.golang.install_go_packages(f"{BASE}/packages/base_go.txt")
    shaper.localpy.install_pip_packages(f"{BASE}/packages/base_pip.txt")
    shaper.download.install_with_remote_script(
        "rustup", "https://sh.rustup.rs", ["-y", "--no-modify-path"]
    )
    shaper.rust.install_rust_packages(f"{BASE}/packages/base_rust.txt")
    shaper.dotfiles.dotfile_git_restore(
        "base", "git@github.com:bowmanjd/dotfiles-base.git"
    )
    shaper.dotfiles.dotfile_git_restore(
        "headless", "git@github.com:bowmanjd/dotfiles-headless.git"
    )


if __name__ == "__main__":
    run()
