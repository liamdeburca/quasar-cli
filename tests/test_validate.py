import subprocess
from pathlib import Path


def test_config(temp_wd: Path):
    assert subprocess.run(
        ["quasar-cli", "validate", "config"],
        cwd=temp_wd,
        check=True,
    ).returncode == 0

def test_linelist(temp_wd: Path):
    assert subprocess.run(
        ["quasar-cli", "validate", "linelist"],
        cwd=temp_wd,
        check=True,
    ).returncode == 0

def test_lookup(temp_wd: Path):
    assert subprocess.run(
        ["quasar-cli", "validate", "lookup"],
        cwd=temp_wd,
        check=True,
    ).returncode == 0

def test_workspace(temp_wd: Path):
    assert subprocess.run(
        ["quasar-cli", "validate", "workspace"],
        cwd=temp_wd,
        check=True,
    ).returncode == 0