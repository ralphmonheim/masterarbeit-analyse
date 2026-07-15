"""Loads an optional local, explicitly unverified demo catalog."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from ma_core import load_configuration_file, sha256_file

DEMO_CATALOG_DIRECTORY = Path(__file__).resolve().parents[2] / "config" / "ma_database" / "catalogs" / "v0.1.0"

_RECORD_FILES = {
    "materials": ("materials.yaml", "material_id"),
    "constructions": ("constructions.yaml", "construction_id"),
    "heating_generators": ("heating_generators.yaml", "heating_generator_id"),
    "cooling_generators": ("cooling_generators.yaml", "cooling_generator_id"),
    "thermal_storages": ("thermal_storages.yaml", "storage_id"),
}


@dataclass(frozen=True, slots=True)
class DemoCatalogRecord:
    """One catalog record together with its source category."""

    category: str
    record_id: str
    label: str
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class DemoCatalog:
    """Read-only local catalog; values are never simulation-ready by default."""

    catalog_id: str
    catalog_version: str
    records_by_category: Mapping[str, tuple[DemoCatalogRecord, ...]]
    construction_layers: tuple[Mapping[str, Any], ...]

    def records_for(self, category: str) -> tuple[DemoCatalogRecord, ...]:
        """Returns a category in the stable order defined by the seed file."""
        try:
            return self.records_by_category[category]
        except KeyError as exc:
            raise ValueError(f"Unbekannte Demo-Katalogkategorie: {category}") from exc

    def layers_for(self, construction_id: str) -> tuple[Mapping[str, Any], ...]:
        """Returns the ordered demo layers for one selected construction."""
        return tuple(layer for layer in self.construction_layers if layer["construction_id"] == construction_id)


@dataclass(frozen=True, slots=True)
class CatalogSelection:
    """A UI selection that is deliberately not a technical model change."""

    category: str
    record_id: str
    label: str
    catalog_id: str
    catalog_version: str
    selection_status: str = "demo_unverified"


def load_demo_catalog(catalog_directory: str | Path = DEMO_CATALOG_DIRECTORY) -> DemoCatalog:
    """Loads a local catalog without turning it into versioned model input."""
    directory = Path(catalog_directory)
    manifest = load_configuration_file(directory / "manifest.yaml")
    if manifest.get("status") != "draft":
        raise ValueError("Der Demo-Katalog muss den Status 'draft' haben.")
    if not isinstance(manifest.get("catalog_id"), str) or not isinstance(manifest.get("catalog_version"), str):
        raise ValueError("Der Demo-Katalog braucht catalog_id und catalog_version.")

    expected_hashes = manifest.get("files")
    if not isinstance(expected_hashes, dict):
        raise ValueError("Das Demo-Katalogmanifest braucht Dateipruefsummen.")

    records_by_category: dict[str, tuple[DemoCatalogRecord, ...]] = {}
    for category, (file_name, identifier_field) in _RECORD_FILES.items():
        _verify_file_hash(directory / file_name, expected_hashes.get(file_name))
        payload = load_configuration_file(directory / file_name)
        records = payload.get("records")
        if not isinstance(records, list):
            raise ValueError(f"{file_name} braucht eine records-Liste.")
        catalog_records = tuple(
            _build_record(category, record, identifier_field, file_name)
            for record in records
        )
        expected_count = manifest.get("record_counts", {}).get(category)
        if expected_count != len(catalog_records):
            raise ValueError(f"{file_name} hat nicht die erwartete Anzahl Demo-Datensaetze.")
        records_by_category[category] = catalog_records

    layer_file_name = "construction_layers.yaml"
    _verify_file_hash(directory / layer_file_name, expected_hashes.get(layer_file_name))
    layer_payload = load_configuration_file(directory / layer_file_name)
    raw_layers = layer_payload.get("records")
    if not isinstance(raw_layers, list) or not all(isinstance(layer, dict) for layer in raw_layers):
        raise ValueError("construction_layers.yaml braucht eine records-Liste mit Objekten.")
    if manifest.get("record_counts", {}).get("construction_layers") != len(raw_layers):
        raise ValueError("construction_layers.yaml hat nicht die erwartete Anzahl Demo-Datensaetze.")
    construction_layers = tuple(_build_construction_layer(layer) for layer in raw_layers)

    return DemoCatalog(
        catalog_id=manifest["catalog_id"],
        catalog_version=manifest["catalog_version"],
        records_by_category=MappingProxyType(records_by_category),
        construction_layers=construction_layers,
    )


def select_demo_record(catalog: DemoCatalog, *, category: str, record_id: str) -> CatalogSelection:
    """Creates a session-safe selection reference for one demo record."""
    for record in catalog.records_for(category):
        if record.record_id == record_id:
            return CatalogSelection(
                category=category,
                record_id=record.record_id,
                label=record.label,
                catalog_id=catalog.catalog_id,
                catalog_version=catalog.catalog_version,
            )
    raise ValueError(f"Demo-Datensatz nicht gefunden: {category}/{record_id}")


def _verify_file_hash(path: Path, expected_hash: object) -> None:
    if not isinstance(expected_hash, str):
        raise ValueError(f"Keine Pruefsumme fuer {path.name} im Demo-Katalogmanifest.")
    if sha256_file(path) != expected_hash:
        raise ValueError(f"Pruefsumme von {path.name} stimmt nicht mit dem Demo-Katalogmanifest ueberein.")


def _build_record(
    category: str,
    record: object,
    identifier_field: str,
    file_name: str,
) -> DemoCatalogRecord:
    if not isinstance(record, dict):
        raise ValueError(f"{file_name} enthaelt keinen Objekt-Datensatz.")
    record_id = record.get(identifier_field)
    label = record.get("name_de")
    if not isinstance(record_id, str) or not isinstance(label, str):
        raise ValueError(f"{file_name} braucht {identifier_field} und name_de.")
    if record.get("verification_status") != "draft_unverified":
        raise ValueError(f"{file_name} darf nur draft_unverified-Datensaetze enthalten.")
    if record.get("confirmation_status") != "unconfirmed":
        raise ValueError(f"{file_name} darf nur unconfirmed-Datensaetze enthalten.")
    return DemoCatalogRecord(
        category=category,
        record_id=record_id,
        label=label,
        data=MappingProxyType(dict(record)),
    )


def _build_construction_layer(layer: Mapping[str, Any]) -> Mapping[str, Any]:
    construction_id = layer.get("construction_id")
    material_ref = layer.get("material_ref")
    layer_no = layer.get("layer_no")
    if not isinstance(construction_id, str) or not isinstance(material_ref, str) or not isinstance(layer_no, int):
        raise ValueError("Eine Demo-Konstruktionsschicht braucht construction_id, material_ref und layer_no.")
    return MappingProxyType(dict(layer))
