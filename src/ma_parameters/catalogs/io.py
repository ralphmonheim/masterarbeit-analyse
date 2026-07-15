"""I/O-Helfer fuer einfache JSON- und YAML-Katalogkonfigurationen."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ma_core import load_configuration_file


def load_config_file(config_path: str | Path) -> dict[str, Any]:
    """Laedt eine kleine Katalogkonfiguration ueber den gemeinsamen Loader."""
    return load_configuration_file(config_path)
