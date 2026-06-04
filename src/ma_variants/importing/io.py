"""I/O-Helfer fuer einfache JSON- und YAML-Konfigurationsdateien."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_config_file(config_path: str | Path) -> dict[str, Any]:
    """Laedt eine kleine JSON- oder YAML-Konfiguration als Dictionary."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {path}")

    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
    elif path.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        raise ValueError(f"Nicht unterstuetztes Konfigurationsformat: {path.suffix}")

    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Konfigurationsdatei muss ein Objekt enthalten: {path}")
    return data
