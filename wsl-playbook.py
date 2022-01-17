#!/usr/bin/python3
"""Script for configuring a WSL system."""

import shaper.dotfiles
import shaper.dnf

def run() -> None:
    """Run commands in order."""
    #shaper.dotfiles.dotfiles_ssh(SSH_SECRET_REPO)
    shaper.dnf.install_dnf_packages("packages/wsl_dnf.txt")
    shaper.dotfiles.dotfile_git_restore("wsl", "git@github.com:bowmanjd/dotfiles-wsl.git")

if __name__ == "__main__":
    run()

