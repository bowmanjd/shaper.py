#!/usr/bin/env python3
"""Sample script for configuring a system. Copy to playbook.py and customize."""

import shaper.dotfiles
import shaper.dnf
import shaper.fonts
import shaper.npm

SSH_SECRET_REPO = "bowmanjd/sshsecrets.git"


def run() -> None:
    """Run commands in order."""
    shaper.dotfiles.dotfiles_ssh(SSH_SECRET_REPO)
    #shaper.npm.install_npm_packages()
    shaper.fonts.install_fonts()


if __name__ == "__main__":
    run()

