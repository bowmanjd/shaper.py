"""Utility functions for managing local Go packages."""
import re
import subprocess
import tempfile
from pathlib import Path

import shaper.download


def multimc_update() -> None:
    latest_multimc: dict = shaper.download.json_get(
        "https://api.github.com/repos/MultiMC/launcher/releases/latest"
    )
    latest_version = latest_multimc["name"]
    try:
        current_version = subprocess.check_output(
            ["/usr/local/MultiMC/MultiMC", "-V"], text=True
        )
    except FileNotFoundError:
        current_version = ""
    if latest_version not in current_version:
        with tempfile.TemporaryDirectory(prefix="multimc-") as tmpdirname:
            tmpdir = Path(tmpdirname)
            downloaded_file = shaper.download.download(
                "https://files.multimc.org/downloads/mmc-stable-lin64.tar.gz", tmpdir
            )
            shaper.download.untar(downloaded_file, Path("/usr/local/"), sudo=True)


if __name__ == "__main__":
    multimc_update()
