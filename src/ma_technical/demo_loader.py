"""Loader fuer versionierte ma_technical-Demos."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import TechnicalSystemSpecification, technical_specification_from_any
from .paths import BUSINESS_INTEGRATION_LOD1_TECHNICAL_SPEC_PATH


def load_technical_spec(path: str | Path) -> TechnicalSystemSpecification:
    """Laedt eine TechnicalSystemSpecification aus YAML."""
    source_path = Path(path)
    with source_path.open("r", encoding="utf-8") as source_file:
        raw_data: Any = yaml.safe_load(source_file) or {}
    return technical_specification_from_any(raw_data)


def load_business_integration_lod1_technical_spec() -> TechnicalSystemSpecification:
    """Laedt die LoD-1-Technikspezifikation des BusinessIntegration-Testgebaeudes."""
    return load_technical_spec(BUSINESS_INTEGRATION_LOD1_TECHNICAL_SPEC_PATH)
