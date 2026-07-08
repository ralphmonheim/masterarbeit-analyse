"""Standardpfade fuer ma_zones."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ZONES_CONFIG_DIR = PROJECT_ROOT / "config" / "ma_zones"
BUSINESS_INTEGRATION_LOD1_ZONE_SPEC_PATH = (
    ZONES_CONFIG_DIR / "examples" / "business_integration_lod1_zone_spec.yaml"
)
