"""Loader fuer versionierte ma_zones-Demos."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import ZoneModelSpecification, zone_specification_from_any
from .paths import BUSINESS_INTEGRATION_LOD1_ZONE_SPEC_PATH


def load_zone_spec(path: str | Path) -> ZoneModelSpecification:
    """Laedt eine ZoneModelSpecification aus YAML."""
    source_path = Path(path)
    with source_path.open("r", encoding="utf-8") as source_file:
        raw_data: Any = yaml.safe_load(source_file) or {}
    return zone_specification_from_any(raw_data)


def load_business_integration_lod1_zone_spec() -> ZoneModelSpecification:
    """Laedt die LoD-1-Zonenspezifikation des BusinessIntegration-Testgebaeudes."""
    return load_zone_spec(BUSINESS_INTEGRATION_LOD1_ZONE_SPEC_PATH)
