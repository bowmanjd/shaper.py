#!/usr/bin/env python3
"""Sample script for configuring a system. Copy to playbook.py and customize."""

import shaper.dnf
import shaper.npm
import shaper.fonts
import mysecrets.py

shaper.dnf.install_rpm_keys()
shaper.dnf.install_dnf_repos()
shaper.dnf.install_copr_repos()
shaper.dnf.install_rpmfusion()
shaper.dnf.install_dnf_packages()
shaper.npm.install_npm_packages()
shaper.fonts.install_fonts()
