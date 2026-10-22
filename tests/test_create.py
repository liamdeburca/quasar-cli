import subprocess
from pathlib import Path


def _test_helper(temp_wd: Path, command: str):
    assert subprocess.run(
        ["quasar-cli", "create", command],
        cwd=temp_wd,
        check=False,
    ).returncode == 0

    assert subprocess.run(
        ["quasar-cli", "create", command],
        cwd=temp_wd,
        check=False,
    ).returncode != 0

    assert subprocess.run(
        ["quasar-cli", "create", command, "--force"],
        cwd=temp_wd,
        check=False,
    ).returncode == 0


def test_config(temp_wd: Path):
    _test_helper(temp_wd, "config")

def test_linelist(temp_wd: Path):
    _test_helper(temp_wd, "linelist")

def test_lookup(temp_wd: Path):
    _test_helper(temp_wd, "lookup")

def test_workspace(temp_wd: Path):
    _test_helper(temp_wd, "workspace")