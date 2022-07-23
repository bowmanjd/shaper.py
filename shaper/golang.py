"""Utility functions for managing local Go packages."""
import platform
import subprocess
import tempfile
from pathlib import Path

import shaper.download
import shaper.util

GOPATH = Path.home() / "go" / "bin"
GOROOT = Path("/usr/local/go")

ARCHES = {
    "aarch64": "arm64",
    "x86_64": "amd64",
    "i686": "386",
    "armv7l": "armv6l",
}


def go_update() -> None:
    current_version = subprocess.check_output(["go", "version"], text=True).split()[2]
    latest_go: dict = shaper.download.json_get("https://go.dev/dl/?mode=json")[0]
    latest_version = latest_go["version"]
    arch = ARCHES.get(platform.machine(), platform.machine())
    downloads = {
        f["arch"]: (f["filename"], f["sha256"])
        for f in latest_go["files"]
        if f["os"] == "linux" and f["kind"] == "archive"
    }
    if current_version == latest_version:
        print(f"Go is already at version {latest_version}")
    else:
        filename = downloads[arch][0]
        sha256sum = downloads[arch][1]

        with tempfile.TemporaryDirectory(prefix="golang-") as tmpdirname:
            tmpdir = Path(tmpdirname)
            downloaded_file = shaper.download.download(
                f"https://go.dev/dl/{filename}", tmpdir
            )
            checksum = shaper.download.hashsum(downloaded_file)
            if checksum == sha256sum:
                subprocess.check_call(
                    [
                        "sudo",
                        "tar",
                        "-x",
                        "-C",
                        GOROOT.parent,
                        "--recursive-unlink",
                        "-f",
                        tmpdir / filename,
                    ]
                )
            else:
                print(f"Checksum failure for {filename}")
                print(sha256sum)
                print(checksum)


def existing_go() -> set:
    """Obtain list of installed Go packages.

    Returns:
        a set of package names
    """
    cmd = ["go", "version", "-m", GOPATH]
    packages = shaper.util.get_set_from_output(cmd)
    return {
        line.replace("\tpath\t", "").strip()
        for line in packages
        if line.startswith("\tpath")
    }


def install_go_packages(filename: str) -> None:
    """Install Go packages from text file.

    Args:
        filename: path to text file listing packages
    """
    existing = existing_go()
    to_install = shaper.util.get_set_from_file(filename)
    new_packages = to_install - existing

    for package in new_packages:
        cmd = ["go", "install", f"{package}@latest"]
        subprocess.check_call(cmd)


if __name__ == "__main__":
    go_update()
