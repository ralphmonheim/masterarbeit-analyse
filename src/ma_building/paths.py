"""Standardpfade fuer das Gebaeudemodul."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BUILDING_CONFIG_DIR = PROJECT_ROOT / "config" / "ma_building"
DEFAULT_DEMO_BUILDING_SPEC_PATH = BUILDING_CONFIG_DIR / "examples" / "demo_building_spec.yaml"

BUILDING_DATA_DIR = PROJECT_ROOT / "data" / "ma_building"
BUILDING_IFC_INPUT_DIR = BUILDING_DATA_DIR / "input" / "ifc"
BUILDING_RHINO_INPUT_DIR = BUILDING_DATA_DIR / "input" / "rhino"
BUILDING_CAD_INPUT_DIR = BUILDING_DATA_DIR / "input" / "cad"
BUILDING_DIAGNOSTICS_DIR = BUILDING_DATA_DIR / "diagnostics"

MASTER_THESIS_REFERENCE_IFC_FILENAME = "SmallOffice_d_IFC2x3.ifc"
MASTER_THESIS_REFERENCE_IFC_PATH = BUILDING_IFC_INPUT_DIR / MASTER_THESIS_REFERENCE_IFC_FILENAME

SUPPORTED_BUILDING_SOURCE_SUFFIXES = frozenset({".ifc", ".3dm", ".dwg"})
