"""Importer fuer Materialkataloge aus YAML, JSON oder CSV."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from ..importing.io import load_config_file
from .models import Material, MaterialCatalogImportResult, MaterialProperty

MATERIAL_REQUIRED_FIELDS = (
    "material_key",
    "material_group",
    "material_name",
    "density",
    "lambda_value",
    "specific_heat_capacity",
    "price",
    "gwp_value",
    "gwp_unit",
    "document_path",
    "source",
    "data_quality",
)
MATERIAL_PROPERTY_REQUIRED_FIELDS = (
    "material_key",
    "property_key",
    "value",
    "unit",
    "source",
    "data_quality",
)
MATERIAL_NUMERIC_FIELDS = {
    "density",
    "lambda_value",
    "specific_heat_capacity",
    "price",
    "gwp_value",
}


def _missing_fields(raw_item: dict[str, Any], required_fields: tuple[str, ...]) -> list[str]:
    return [field for field in required_fields if field not in raw_item]


def _coerce_material_payload(raw_item: dict[str, Any]) -> dict[str, Any]:
    payload = {field: raw_item[field] for field in MATERIAL_REQUIRED_FIELDS}
    for field in MATERIAL_NUMERIC_FIELDS:
        payload[field] = float(payload[field])
    return payload


def _load_raw_materials(config_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    if config_path.suffix.lower() == ".csv":
        with config_path.open(encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file)), [], []

    data = load_config_file(config_path)
    raw_materials = data.get("materials")
    if not isinstance(raw_materials, list):
        return [], [], ["Konfiguration muss eine Liste 'materials' enthalten."]

    raw_properties = data.get("material_properties", [])
    if not isinstance(raw_properties, list):
        return raw_materials, [], ["Konfiguration 'material_properties' muss eine Liste sein."]
    return raw_materials, raw_properties, []


def _import_material_properties(
    raw_items: list[dict[str, Any]],
    known_material_keys: set[str],
) -> tuple[list[MaterialProperty], list[str]]:
    properties: list[MaterialProperty] = []
    errors: list[str] = []
    seen_keys: set[tuple[str, str]] = set()

    for index, raw_item in enumerate(raw_items, start=1):
        item_label = f"material_properties[{index}]"
        if not isinstance(raw_item, dict):
            errors.append(f"{item_label} muss ein Objekt sein.")
            continue

        missing = _missing_fields(raw_item, MATERIAL_PROPERTY_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{item_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue

        material_key = str(raw_item["material_key"]).strip()
        property_key = str(raw_item["property_key"]).strip()
        if material_key not in known_material_keys:
            errors.append(f"{item_label} referenziert unbekannten material_key '{material_key}'.")
            continue
        if (material_key, property_key) in seen_keys:
            errors.append(f"Doppelte MaterialProperty '{material_key}/{property_key}'.")
            continue
        seen_keys.add((material_key, property_key))

        try:
            properties.append(
                MaterialProperty(**{field: raw_item[field] for field in MATERIAL_PROPERTY_REQUIRED_FIELDS})
            )
        except ValueError as exc:
            errors.append(f"{item_label}: {exc}")
    return properties, errors


def import_materials(config_path: str | Path) -> MaterialCatalogImportResult:
    """Laedt Materialien und optionale Materialeigenschaften aus YAML, JSON oder CSV."""
    path = Path(config_path)
    raw_materials, raw_properties, errors = _load_raw_materials(path)
    materials: list[Material] = []
    seen_material_keys: set[str] = set()

    for index, raw_item in enumerate(raw_materials, start=1):
        item_label = f"materials[{index}]"
        if not isinstance(raw_item, dict):
            errors.append(f"{item_label} muss ein Objekt sein.")
            continue

        missing = _missing_fields(raw_item, MATERIAL_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{item_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue

        material_key = str(raw_item["material_key"]).strip()
        if material_key in seen_material_keys:
            errors.append(f"Doppelter material_key '{material_key}'.")
            continue
        seen_material_keys.add(material_key)

        try:
            materials.append(Material(**_coerce_material_payload(raw_item)))
        except (TypeError, ValueError) as exc:
            errors.append(f"{item_label}: {exc}")

    material_properties, property_errors = _import_material_properties(raw_properties, seen_material_keys)
    errors.extend(property_errors)

    return MaterialCatalogImportResult(
        materials=materials,
        material_properties=material_properties,
        errors=errors,
        source_path=path,
    )
