"""Lesen und Auswerten der versionierten Parameter-Bestandsmatrix."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from ma_core import load_configuration_file

from .definitions import ParameterInventoryEntry, ParameterInventoryStatus

DEFAULT_PARAMETER_INVENTORY_PATH = Path("config/ma_parameters/inventory/parameter_inventory_v1.yaml")


def load_parameter_inventory(
    inventory_path: str | Path = DEFAULT_PARAMETER_INVENTORY_PATH,
) -> tuple[ParameterInventoryEntry, ...]:
    """Laedt die P015-S5A-Bestandsmatrix ohne Projektwerte zu veraendern."""
    raw = load_configuration_file(inventory_path)
    entries = raw.get("entries")
    if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
        raise ValueError("Parameterinventar benoetigt eine Liste 'entries'.")
    return tuple(_entry_from_raw(entry) for entry in entries)


def parameter_inventory_summary(entries: tuple[ParameterInventoryEntry, ...]) -> dict[str, int]:
    """Verdichtet Status und beobachtete Zeilen fuer Dokumentation und Tests."""
    status_counts = Counter(entry.status.value for entry in entries)
    return {
        **{status.value: status_counts[status.value] for status in ParameterInventoryStatus},
        "observed_current_entries": sum(entry.observed_count for entry in entries),
    }


def parameter_inventory_table_rows(entries: tuple[ParameterInventoryEntry, ...]) -> list[dict[str, object]]:
    """Erzeugt eine lesbare Matrix, ohne das Inventar zu einer UI-Quelle zu machen."""
    return [
        {
            "Bestand": entry.subject,
            "Bestehender Parameter": entry.legacy_parameter_key_pattern,
            "Zielmodul": entry.target_module.value,
            "Zielgruppe": entry.target_group_type,
            "Zielparameter": entry.target_parameter_key_pattern,
            "Einheit": entry.unit,
            "Quelle": entry.source_type.value,
            "LoD": f"{entry.lod_min}-{entry.lod_max}",
            "Editierbarkeit": entry.editability.value,
            "Variantenfaehigkeit": entry.variant_capability.value,
            "Ableitung": entry.derivation_status.value,
            "Inventarstatus": entry.status.value,
            "Beobachtete Zeilen": entry.observed_count,
            "Hinweis": entry.notes,
        }
        for entry in entries
    ]


def _entry_from_raw(raw: dict[str, Any]) -> ParameterInventoryEntry:
    required_keys = {
        "subject",
        "legacy_parameter_key_pattern",
        "source_path",
        "target_module",
        "target_group_type",
        "target_parameter_key_pattern",
        "unit",
        "source_type",
        "lod_min",
        "lod_max",
        "editability",
        "variant_capability",
        "derivation_status",
        "status",
    }
    missing_keys = sorted(key for key in required_keys if key not in raw)
    if missing_keys:
        raise ValueError(f"Parameterinventar-Eintrag enthaelt Pflichtfelder nicht: {', '.join(missing_keys)}")
    return ParameterInventoryEntry(
        subject=str(raw["subject"]),
        legacy_parameter_key_pattern=str(raw["legacy_parameter_key_pattern"]),
        source_path=str(raw["source_path"]),
        target_module=str(raw["target_module"]),
        target_group_type=str(raw["target_group_type"]),
        target_parameter_key_pattern=str(raw["target_parameter_key_pattern"]),
        unit=str(raw["unit"]),
        source_type=str(raw["source_type"]),
        lod_min=int(raw["lod_min"]),
        lod_max=int(raw["lod_max"]),
        editability=str(raw["editability"]),
        variant_capability=str(raw["variant_capability"]),
        derivation_status=str(raw["derivation_status"]),
        status=str(raw["status"]),
        observed_count=int(raw.get("observed_count", 0)),
        notes=str(raw.get("notes", "")),
    )
