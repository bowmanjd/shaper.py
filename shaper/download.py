#!/usr/bin/env python3
"""Utility functions for downloading files."""
import functools
import hashlib
import json
import pathlib
import subprocess
import typing
import urllib.parse
import urllib.request


class SafeOpener(urllib.request.OpenerDirector):
    """URL opener with fewer handlers."""

    def __init__(self, handlers: typing.Optional[typing.Iterable] = None):
        """Use only a subset of handlers.

        Args:
            handlers: optional list of handlers
        """
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


def json_get(url: str) -> typing.Union[dict, list, str]:
    """Pull JSON data from a url.

    Args:
        url: URL of JSON response

    Returns:
        JSON object
    """
    response = opener.open(url)
    return json.load(response)


def download(url: str, destination: pathlib.Path) -> pathlib.Path:
    """Copy data from a url to a local file.

    Args:
        url: URL of file to be downloaded
        destination: optional path of destination file

    Returns:
        Downloaded file path
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
    return destination


def install_with_remote_script(
    command: str, url: str, extra: typing.Iterable = ()
) -> None:
    """Install using downloadable script if not installed already.

    Args:
        command: command to try to determine existence
        url: download URL for installation script
        extra: list of extra arguments to pass to script
    """
    try:
        subprocess.check_call(["command", "-v", command])
    except subprocess.CalledProcessError:
        print(f"Requesting {url}")
        response = opener.open(url)
        script = response.read()
        subprocess.check_call(["/bin/bash", "-c", script, "--", *extra])


def hashsum(filepath: pathlib.Path, algorithm: str = "sha256") -> str:
    """Compute hash checksum of file.

    Args:
        filepath: path to file
        algorithm: hashing algorithm

    Returns:
        hexadecimal hash string
    """
    hash = hashlib.new(algorithm)
    with filepath.open("rb") as file_handle:
        while chunk := file_handle.read(8192):
            hash.update(chunk)
    return hash.hexdigest()


if __name__ == "__main__":
    print(json_get("https://go.dev/dl/?mode=json"))
