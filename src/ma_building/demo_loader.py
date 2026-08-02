"""Loader fuer die versionierte ma_building-Demo."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import BuildingModelSpecification, building_specification_from_dict
from .paths import (
    BUSINESS_INTEGRATION_LOD1_BUILDING_SPEC_PATH,
    DEFAULT_DEMO_BUILDING_SPEC_PATH,
    SMALL_OFFICE_5Z_ENDVARIANT_02_BUILDING_SPEC_PATH,
    SMALL_OFFICE_LOD1_BUILDING_SPEC_PATH,
)

BUILDING_SPECIFICATION_OPTIONS = (
    ("demo", "Demo-Gebaeudespezifikation", DEFAULT_DEMO_BUILDING_SPEC_PATH),
    ("business_integration_lod1", "BusinessIntegration LoD-1", BUSINESS_INTEGRATION_LOD1_BUILDING_SPEC_PATH),
    (
        "small_office_5z_endvariant_02",
        "SmallOffice Endvariante 02",
        SMALL_OFFICE_5Z_ENDVARIANT_02_BUILDING_SPEC_PATH,
    ),
)


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


def load_business_integration_lod1_building_spec() -> BuildingModelSpecification:
    """Laedt die LoD-1-Spezifikation des BusinessIntegration-Testgebaeudes."""
    return load_building_spec(BUSINESS_INTEGRATION_LOD1_BUILDING_SPEC_PATH)


def load_small_office_lod1_building_spec() -> BuildingModelSpecification:
    """Laedt den rein synthetischen SmallOffice-LoD-1-Referenzfall."""
    return load_building_spec(SMALL_OFFICE_LOD1_BUILDING_SPEC_PATH)


def load_small_office_5z_endvariant_02_building_spec() -> BuildingModelSpecification:
    """Laedt die normalisierte V1-Geometrie der SmallOffice-Endvariante 02."""
    return load_building_spec(SMALL_OFFICE_5Z_ENDVARIANT_02_BUILDING_SPEC_PATH)


def load_named_building_specification(selection_key: str) -> BuildingModelSpecification:
    """Laedt einen in der direkten UI ausdruecklich auswaehlbaren Building-Stand."""
    for key, _label, source_path in BUILDING_SPECIFICATION_OPTIONS:
        if key == selection_key:
            return load_building_spec(source_path)
    raise ValueError(f"Unbekannte Gebaeudespezifikation: {selection_key}")
