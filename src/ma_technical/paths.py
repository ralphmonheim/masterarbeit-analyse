"""Standardpfade fuer ma_technical."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TECHNICAL_CONFIG_DIR = PROJECT_ROOT / "config" / "ma_technical"
BUSINESS_INTEGRATION_LOD1_TECHNICAL_SPEC_PATH = (
    TECHNICAL_CONFIG_DIR / "examples" / "business_integration_lod1_technical_spec.yaml"
)
