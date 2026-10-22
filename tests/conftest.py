from collections.abc import Generator
from pathlib import Path
from shutil import rmtree

import pytest

_this_file: Path = Path(__file__).resolve()

@pytest.fixture(scope="session")
def temp_wd() -> Generator[Path, None, None]:
    path = _this_file.parent / "temp_wd"
    path.mkdir(exist_ok=True)
    yield path
    rmtree(path, ignore_errors=True)
    path.unlink(missing_ok=True)