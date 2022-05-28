#!/usr/bin/python3
"""Script for full Linux graphical workstation."""
from pathlib import Path

import shaper.dnf
import shaper.dotfiles
import shaper.download
import shaper.fonts
import shaper.golang
import shaper.localpy
import shaper.minecraft
import shaper.npm
import shaper.rust

BASE = Path.home() / "shaper"


def run() -> None:
    """Run commands in order."""
    shaper.dnf.install_rpm_keys(f"{BASE}/packages/rpm_keys.json")
    shaper.dnf.install_dnf_repos(f"{BASE}/repos/workstation_repos.txt")
    shaper.dnf.install_copr_repos(f"{BASE}/repos/workstation_copr_repos.txt")
    shaper.dnf.install_rpmfusion()
    shaper.dnf.install_dnf_packages(f"{BASE}/packages/base_dnf.txt")
    shaper.npm.install_npm_packages(f"{BASE}/packages/base_npm.txt")
    print("Installing Python packages...")
    shaper.localpy.install_pip_packages(f"{BASE}/packages/base_pip.txt")
    print("Installing fonts...")
    shaper.fonts.install_fonts(f"{BASE}/fonts/workstation-fonts.txt")
    print("Installing Rust...")
    shaper.download.install_with_remote_script(
        "rustup", "https://sh.rustup.rs", ["-y", "--no-modify-path"]
    )
    print("Dotfiles...")
    shaper.dotfiles.dotfile_git_restore(
        "base", "git@github.com:bowmanjd/dotfiles-base.git"
    )
    shaper.dotfiles.dotfile_git_restore(
        "headless", "git@github.com:bowmanjd/dotfiles-headless.git"
    )
    shaper.dotfiles.dotfile_git_restore(
        "workstation", "git@github.com:bowmanjd/dotfiles-workstation.git"
    )
    print("Installing Go...")
    shaper.golang.go_update()
    shaper.golang.install_go_packages(f"{BASE}/packages/base_go.txt")
    print("Installing Cargo (Rust) packages...")
    shaper.rust.install_rust_packages(f"{BASE}/packages/base_rust.txt")
    shaper.minecraft.multimc_update()


if __name__ == "__main__":
    run()
