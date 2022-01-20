"""Utility functions for managing packages and repos with dnf."""

import dnf
import functools
import json
import pathlib
import subprocess

import shaper.util


NPM = ["volta", "run", "--npm", "latest", "npm"]
DNF = ["sudo", "/usr/bin/dnf"]
RPM = ["sudo", "/usr/bin/rpm"]
FEDORA_VERSION = subprocess.check_output(["rpm", "-E", "%fedora"], text=True).strip()


@functools.cache
def dnf_base() -> dnf.Base:
    base = dnf.Base()
    base.read_all_repos()
    return base


def existing_rpm_keys() -> set:
    """Obtain list of packagers of install gpg keys.

    Returns:
        a set of packager names
    """
    command = [*RPM, "-qa", "--qf", r"%{PACKAGER}\n", "gpg-pubkey*"]
    return shaper.util.get_set_from_output(command)


def install_rpm_key(keyword: str, url: str) -> None:
    """Install gpg key for repo if not already there.

    Args:
        keyword: search term that, if present, identfies previously installed key
        url: URL to download key
    """
    if not all(keyword in packager for packager in existing_rpm_keys()):
        command = [*RPM, "--import", url]
        subprocess.check_call(command)


def install_rpm_keys(filename: str) -> None:
    """Install rpm gpg keys from file.

    Args:
        filename: path to text file listing repos
    """
    keys = json.loads(pathlib.Path(filename).read_text())
    for key in keys:
        install_rpm_key(**key)


def existing_copr_repos() -> set:
    """Obtain copr repository names.

    Returns:
        a set of repo names
    """
    return {
        "/".join(k.split(":")[2:])
        for k in dnf_base().repos.keys()
        if k.startswith("copr")
    }


def existing_dnf_repos() -> set:
    """Obtain dnf repository names.

    Returns:
        a set of repo names
    """
    return {r.baseurl[0] for r in dnf_base().repos.values() if r.baseurl}


def install_copr_repos(filename: str) -> None:
    """Install copr repositories from file.

    Args:
        filename: path to text file listing repos
    """
    possible_repositories = shaper.util.get_set_from_file(filename)
    to_install = possible_repositories - existing_copr_repos()
    if to_install:
        subprocess.check_call([*DNF, "copr", "enable", "-y", *to_install])


def install_dnf_repos(filename: str) -> None:
    """Install dnf repositories from file.

    Args:
        filename: path to text file listing repos
    """
    possible_urls = shaper.util.get_set_from_file(filename)
    to_install = possible_urls - existing_dnf_repos()
    if to_install:
        subprocess.check_call(
            [*DNF, "config-manager", "--add-repo", " ".join(to_install)]
        )


def install_rpmfusion() -> None:
    """Install rpmfusion repositories."""
    if not {"rpmfusion-free-release", "rpmfusion-nonfree-release"}.issubset(
        existing_dnf()
    ):
        subprocess.check_call(
            [
                *DNF,
                "install",
                "-y",
                f"https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-{FEDORA_VERSION}.noarch.rpm",
                f"https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{FEDORA_VERSION}.noarch.rpm",
            ]
        )


def existing_dnf() -> set:
    """Obtain list of user installed packages.

    Returns:
        a set of package names
    """
    command = ["dnf", "repoquery", "--userinstalled", "--queryformat", "%{name}"]
    return shaper.util.get_set_from_output(command)


def install_dnf_packages(filename: str) -> None:
    """Install packages from text file using dnf.

    Args:
        filename: path to text file listing repos
    """
    to_install = shaper.util.get_set_from_file(filename)
    existing = existing_dnf()
    new_packages = to_install - existing
    if new_packages:
        cmd = [*DNF, "install", "-y", *new_packages]
        subprocess.check_call(cmd)
