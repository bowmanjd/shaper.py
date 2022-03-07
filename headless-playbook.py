#!/usr/bin/python3
"""Sample script for configuring a system. Copy to playbook.py and customize."""
import shaper.dnf
import shaper.dotfiles
import shaper.download
import shaper.fonts
import shaper.golang
import shaper.localpy
import shaper.npm
import shaper.rust


def run() -> None:
    """Run commands in order."""
    shaper.dnf.install_dnf_packages("packages/base_dnf.txt")
    shaper.npm.install_npm_packages("packages/base_npm.txt")
    shaper.golang.install_go_packages("packages/base_go.txt")
    shaper.localpy.install_pip_packages("packages/base_pip.txt")
    shaper.rust.install_rust_packages("packages/base_rust.txt")
    shaper.download.install_with_remote_script(
        "rustup", "https://sh.rustup.rs", ["-y", "--no-modify-path"]
    )
    shaper.dotfiles.dotfile_git_restore(
        "base", "git@github.com:bowmanjd/dotfiles-base.git"
    )
    shaper.dotfiles.dotfile_git_restore(
        "headless", "git@github.com:bowmanjd/dotfiles-headless.git"
    )


if __name__ == "__main__":
    run()
