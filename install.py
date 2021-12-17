#!/usr/bin/env python3
"""Install my desired packages."""


def run() -> None:
    """Run commands in order."""
    install_rpm_keys()
    install_dnf_repos()
    install_copr_repos()
    install_rpmfusion()
    install_dnf_packages()
    install_npm_packages()
    install_fonts()


if __name__ == "__main__":
    run()
