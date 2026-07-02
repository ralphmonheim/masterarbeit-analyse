"""Loader fuer die versionierte ma_building-Demo."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import BuildingModelSpecification, building_specification_from_dict
from .paths import DEFAULT_DEMO_BUILDING_SPEC_PATH


def load_building_spec(path: str | Path) -> BuildingModelSpecification:
    """Laedt eine BuildingModelSpecification aus YAML."""
    source_path = Path(path)
    with source_path.open("r", encoding="utf-8") as source_file:
        raw_data: Any = yaml.safe_load(source_file) or {}
    if not isinstance(raw_data, dict):
        raise ValueError(f"Gebaeudespezifikation muss ein Mapping sein: {source_path}")
    return building_specification_from_dict(raw_data)


def load_demo_building_spec() -> BuildingModelSpecification:
    """Laedt die versionierte kleine Demo-Spezifikation."""
    return load_building_spec(DEFAULT_DEMO_BUILDING_SPEC_PATH)
