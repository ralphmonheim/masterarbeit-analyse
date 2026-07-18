"""Read-only access to local, non-versioned building reference catalogs."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

DEFAULT_BUILDING_CATALOG_DIRECTORY = Path("config/ma_database/catalogs/v0.1.0")


class LocalCatalogValidationError(ValueError):
    """Raised when an available local catalog does not meet its small schema."""


@dataclass(frozen=True)
class LocalCatalog:
    """A validated local catalog with records protected from UI mutation."""

    catalog_type: str
    id_field: str
    records: tuple[Mapping[str, Any], ...]


_CATALOG_SPECS = {
    "materials": ("building_materials.yaml", "building_materials", "material_id"),
    "wall_constructions": ("building_wall_constructions.yaml", "building_wall_constructions", "wall_construction_id"),
    "surfaces": ("building_surfaces.yaml", "building_surfaces", "surface_id"),
}


def load_local_building_catalog(
    catalog_key: str, catalog_directory: str | Path = DEFAULT_BUILDING_CATALOG_DIRECTORY
) -> LocalCatalog:
    """Loads one catalog; a missing file remains distinguishable from invalid data."""
    try:
        filename, expected_type, id_field = _CATALOG_SPECS[catalog_key]
    except KeyError as exc:
        raise ValueError(f"Unbekannter lokaler Gebaeudekatalog: {catalog_key}") from exc

    path = Path(catalog_directory) / filename
    if not path.is_file():
        raise FileNotFoundError(path)
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise LocalCatalogValidationError(f"{path.name}: YAML kann nicht gelesen werden.") from exc
    return _validate_catalog(payload, path.name, expected_type, id_field)


def _validate_catalog(payload: object, filename: str, expected_type: str, id_field: str) -> LocalCatalog:
    if not isinstance(payload, dict):
        raise LocalCatalogValidationError(f"{filename}: Katalog muss ein Objekt sein.")
    if payload.get("schema_version") != "1.0":
        raise LocalCatalogValidationError(f"{filename}: schema_version 1.0 fehlt.")
    if payload.get("catalog_type") != expected_type:
        raise LocalCatalogValidationError(f"{filename}: catalog_type stimmt nicht.")
    records = payload.get("records")
    if not isinstance(records, list):
        raise LocalCatalogValidationError(f"{filename}: records muss eine Liste sein.")

    seen_ids: set[str] = set()
    validated_records: list[Mapping[str, Any]] = []
    for position, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise LocalCatalogValidationError(f"{filename}: Datensatz {position} muss ein Objekt sein.")
        name = record.get("name")
        record_id = record.get(id_field)
        if not isinstance(name, str) or not name.strip():
            raise LocalCatalogValidationError(f"{filename}: Datensatz {position} braucht einen Namen.")
        if not isinstance(record_id, str) or not record_id.strip():
            raise LocalCatalogValidationError(f"{filename}: Datensatz {position} braucht {id_field}.")
        if record_id in seen_ids:
            raise LocalCatalogValidationError(f"{filename}: doppelte ID {record_id}.")
        if expected_type == "building_wall_constructions" and "layers" in record:
            layers = record["layers"]
            if not isinstance(layers, list) or not all(isinstance(layer, dict) for layer in layers):
                raise LocalCatalogValidationError(f"{filename}: layers muss eine Liste von Objekten sein.")
        seen_ids.add(record_id)
        validated_records.append(MappingProxyType(dict(record)))
    return LocalCatalog(expected_type, id_field, tuple(validated_records))
