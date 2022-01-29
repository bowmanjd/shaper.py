#!/usr/bin/env python3
"""Utility functions for downloading files."""
import functools
import os
import pathlib
import subprocess
import typing
import urllib.parse
import urllib.request


class SafeOpener(urllib.request.OpenerDirector):
    def __init__(self, handlers: typing.Iterable = None):
        super().__init__()
        handlers = handlers or (
            urllib.request.UnknownHandler,
            urllib.request.HTTPDefaultErrorHandler,
            urllib.request.HTTPRedirectHandler,
            urllib.request.HTTPSHandler,
            urllib.request.HTTPErrorProcessor,
        )

        for handler_class in handlers:
            self.add_handler(handler_class())


opener = SafeOpener()


def download(url: str, destination: os.PathLike) -> None:
    """Copy data from a url to a local file.

    Args:
        url: URL of file to be downloaded
        destination: optional path of destination file
    """
    print(f"Requesting {url}")
    if destination.is_dir() or not destination.suffix:
        destination = destination.joinpath(
            urllib.parse.unquote(pathlib.PurePosixPath(url).name)
        )
    response = opener.open(url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as dest_file:
        for data in iter(functools.partial(response.read, 32768), b""):
            dest_file.write(data)
    print(f"Downloaded {destination}")


def install_with_remote_script(command: str, url: str, extra: list = []) -> None:
    """Install using downloadable script if not installed already.

    Args:
        command: command to try to determine existence
        url: download URL for installation script
        extra: list of extra arguments to pass to script
    """
    try:
        subprocess.check_output(["which", command])
    except subprocess.CalledProcessError:
        print(f"Requesting {url}")
        response = opener.open(url)
        script = response.read()
        #        script = subprocess.check_output(
        #            [
        #                "curl",
        #                "-fsSL",
        #                url,
        #            ]
        #        )
        subprocess.check_call(["/bin/bash", "-c", script, "--", *extra])
