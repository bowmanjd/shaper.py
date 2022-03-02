import os
import pathlib
import subprocess
import tempfile


HOME = pathlib.Path.home()
DOTFILES = HOME / ".dotfiles"


def ssh_agent_info() -> dict:
    info_file = HOME / ".ssh-agent-info"
    agent_socket = HOME / ".ssh-agent.sock"
    shell_script = ""
    try:
        subprocess.check_call(
            ["pidof", "-s", "ssh-agent"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        shell_script = subprocess.check_output(
            ["ssh-agent", "-t", "3d", "-a", agent_socket], text=True
        )
        info_file.write_text(shell_script)
    if not shell_script:
        shell_script = info_file.read_text()
    agent_vars = dict(
        s.strip().split("=")
        for s in shell_script.split(";")
        if s.strip().startswith("SSH")
    )
    return agent_vars


def ssh_ensure_agent_loaded() -> None:
    try:
        subprocess.check_call(
            ["ssh-add", "-l"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        os.environ.update(ssh_agent_info())
        subprocess.check_call(["ssh-add"])


def dotfiles_ssh(
    repo: str,
    ssh_prefix: str = "git@github.com:",
    http_prefix: str = "https://github.com/",
) -> None:
    """Get SSH dotfiles.

    Args:
        repo: name of this git repo
        http_prefix: HTTPS URL to prepend to repo
        ssh_prefix: SSH URL to prepend to repo
    """
    ssh_dir = HOME / ".ssh"
    if not (ssh_dir / "id_ed25519").is_file():
        dotfile_git_restore("ssh", http_prefix + repo)
        ssh_dir.chmod(0o700)
        for node in ssh_dir.glob("**/*"):
            if node.is_dir():
                node.chmod(0o700)
            else:
                node.chmod(0o600)
    dotfile_git("ssh", ["remote", "set-url", "origin", ssh_prefix + repo])


def dotfile_git(module: str, command: list) -> None:
    """Run git command using specified bare repo.

    Args:
        module: name of bare repo, such as base, or wayland
    """
    git_dir = DOTFILES / module
    DOTFILES.mkdir(parents=True, exist_ok=True)
    module_git = ["git", f"--git-dir={git_dir}", f"--work-tree={HOME}", *command]
    subprocess.check_call(module_git)


def dotfile_git_clone(module: str, url: str) -> None:
    """Clone using specified bare git repo.

    Args:
        module: name of bare repo, such as base, or wayland
        url: repo URL
    """
    git_dir = DOTFILES / module
    DOTFILES.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dtf-") as tmpdirname:
        subprocess.check_call(
            [
                "git",
                "clone",
                "-c",
                "status.showUntrackedFiles=no",
                "-n",
                "--separate-git-dir",
                git_dir,
                url,
                tmpdirname,
            ]
        )


def dotfile_git_restore(module: str, url: str) -> None:
    """Clone and restore using specified bare git repo.

    Args:
        module: name of bare repo, such as base, or wayland
        url: repo URL
    """
    git_dir = DOTFILES / module
    if not git_dir.is_dir():
        try:
            dotfile_git_clone(module, url)
            dotfile_git(module, ["checkout"])
        except subprocess.CalledProcessError:
            print(
                "Deal with conflicting files, then run (possibly with -f "
                f"flag if you are OK with overwriting)\ndtf {module} checkout"
            )
