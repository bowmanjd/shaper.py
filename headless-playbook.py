#!/usr/bin/python3
"""Sample script for configuring a system. Copy to playbook.py and customize."""

import shaper.dotfiles
import shaper.dnf
import shaper.fonts
import shaper.npm

def run() -> None:
    """Run commands in order."""
    #shaper.dotfiles.dotfiles_ssh(SSH_SECRET_REPO)
    shaper.dnf.install_dnf_packages("packages/base_dnf.txt")
    shaper.npm.install_npm_packages("packages/base_npm.txt")
    shaper.dotfiles.dotfile_git_restore("base", "git@github.com:bowmanjd/dotfiles-base.git")
    shaper.dotfiles.dotfile_git_restore("headless", "git@github.com:bowmanjd/dotfiles-headless.git")

if __name__ == "__main__":
    run()
