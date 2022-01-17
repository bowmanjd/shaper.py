#!/usr/bin/python3
"""Sample script for configuring a system. Copy to playbook.py and customize."""

import shaper.dotfiles
import shaper.dnf
import shaper.fonts
import shaper.npm

def run() -> None:
    """Run commands in order."""
    shaper.dnf.install_rpm_keys("packages/rpm_keys.json")
    shaper.dnf.install_dnf_repos("repos/workstation_repos.txt")
    shaper.dnf.install_copr_repos("repos/workstation_copr_repos.txt")
    shaper.dnf.install_rpmfusion()
    shaper.dnf.install_dnf_packages("packages/base_dnf.txt")
    shaper.npm.install_npm_packages("packages/base_npm.txt")
    shaper.fonts.install_fonts("fonts/workstation-fonts.txt")
    shaper.dotfiles.dotfile_git_restore("base", "git@github.com:bowmanjd/dotfiles-base.git")
    shaper.dotfiles.dotfile_git_restore("headless", "git@github.com:bowmanjd/dotfiles-headless.git")

if __name__ == "__main__":
    run()

