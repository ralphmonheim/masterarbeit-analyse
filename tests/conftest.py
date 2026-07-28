import shutil
from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

import pytest


@pytest.fixture
def tmp_path() -> Iterator[Path]:
    """Liefert lokale Test-Tempordner ohne Pytests globalen Windows-Tempmanager."""
    base_dir = Path("data/test_output/pytest_runs")
    base_dir.mkdir(parents=True, exist_ok=True)
    path = base_dir / uuid4().hex
    path.mkdir()
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
