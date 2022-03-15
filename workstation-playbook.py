#!/usr/bin/python3
"""Script for full Linux graphical workstation."""
import shaper.dnf
import shaper.dotfiles
import shaper.download
import shaper.fonts
import shaper.golang
import shaper.localpy
import shaper.minecraft
import shaper.npm
import shaper.rust


def run() -> None:
    """Run commands in order."""
    shaper.dnf.install_rpm_keys("packages/rpm_keys.json")
    shaper.dnf.install_dnf_repos("repos/workstation_repos.txt")
    shaper.dnf.install_copr_repos("repos/workstation_copr_repos.txt")
    shaper.dnf.install_rpmfusion()
    shaper.dnf.install_dnf_packages("packages/base_dnf.txt")
    shaper.dnf.install_dnf_packages("packages/workstation_dnf.txt")
    shaper.localpy.install_pip_packages("packages/base_pip.txt")
    shaper.fonts.install_fonts("fonts/workstation-fonts.txt")
    shaper.download.install_with_remote_script(
        "rustup", "https://sh.rustup.rs", ["-y", "--no-modify-path"]
    )
    shaper.dotfiles.dotfile_git_restore(
        "base", "git@github.com:bowmanjd/dotfiles-base.git"
    )
    shaper.dotfiles.dotfile_git_restore(
        "headless", "git@github.com:bowmanjd/dotfiles-headless.git"
    )
    shaper.dotfiles.dotfile_git_restore(
        "workstation", "git@github.com:bowmanjd/dotfiles-workstation.git"
    )
    shaper.npm.install_npm_packages("packages/base_npm.txt")
    shaper.golang.install_go_packages("packages/base_go.txt")
    shaper.rust.install_rust_packages("packages/base_rust.txt")
    shaper.minecraft.multimc_update()


if __name__ == "__main__":
    run()
