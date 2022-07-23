#!/usr/bin/env python3
"""Utility functions for downloading files."""
import hashlib
import json
import pathlib
import subprocess
import typing
import urllib.parse
import urllib.request

CHUNK_SIZE = 32768


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
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        },
    )
    response = opener.open(request)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as dest_file:
        while chunk := response.read(CHUNK_SIZE):
            dest_file.write(chunk)
    print(f"Downloaded {destination}")
    return destination


def untar(
    filepath: pathlib.Path,
    destination: pathlib.Path,
    sudo: bool = False,
    overwrite: bool = True,
) -> None:
    """Unpack file path using GNU tar.

    Args:
        filepath: path to tar file
        destination: directory to unpack into
        sudo: will elevate if True
        overwrite: delete files/directories first if True
    """
    cmd = [
        "tar",
        "-x",
        "-C",
        destination,
        "-f",
        filepath,
    ]
    if sudo:
        cmd.insert(0, "sudo")
    if overwrite:
        cmd.append("--recursive-unlink")
    subprocess.check_call(cmd)


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
        while chunk := file_handle.read(CHUNK_SIZE):
            hash.update(chunk)
    return hash.hexdigest()


if __name__ == "__main__":
    print(json_get("https://go.dev/dl/?mode=json"))
