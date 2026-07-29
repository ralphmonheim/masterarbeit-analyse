"""Gemeinsame, lesende Sicht auf lokale Gebaeude-Katalogquellen.

Die Quelldateien bleiben die fachliche Inhaltsquelle. Das Register vereinheitlicht
nur ihre Identitaet, Herkunft und den Status fuer Auswahloberflaechen. Eigene
Eingaben werden separat als lokale Entwuerfe gefuehrt und ersetzen nie einen
Quellwert.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any
from uuid import uuid4

from .excel_catalogs import BuildingExcelCatalog, load_building_excel_catalog

BUILDING_CATALOG_TYPES = ("components", "materials", "products")
USER_DRAFT_STATUS = "user_unverified"


@dataclass(frozen=True, slots=True)
class CatalogRecord:
    """Ein unveraenderlicher Auswahl-Datensatz mit Herkunftshinweis."""

    catalog_type: str
    record_id: str
    label: str
    source_kind: str
    provenance_status: str
    source_path: str | None
    source_sha256: str | None
    source_url: str | None
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class BuildingCatalogRegistry:
    """Zusammengefuehrte Sicht auf Quellkataloge und lokale Entwuerfe."""

    records_by_type: Mapping[str, tuple[CatalogRecord, ...]]

    def records_for(self, catalog_type: str) -> tuple[CatalogRecord, ...]:
        try:
            return self.records_by_type[catalog_type]
        except KeyError as exc:
            raise ValueError(f"Unbekannter Katalogtyp: {catalog_type}") from exc


def build_building_catalog_registry(
    *,
    source_paths: Mapping[str, str | Path] | None = None,
    user_drafts: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
) -> BuildingCatalogRegistry:
    """Laedt alle vorhandenen Quellkataloge und ergaenzt lokale Entwuerfe.

    Gleichlautende IDs werden als Konflikt behandelt. Damit kann eine neue
    Kataloglieferung keine vorhandene Identitaet still ueberschreiben.
    """
    records_by_type: dict[str, tuple[CatalogRecord, ...]] = {}
    source_paths = source_paths or {}
    user_drafts = user_drafts or {}
    unknown_types = set(source_paths) - set(BUILDING_CATALOG_TYPES)
    unknown_types |= set(user_drafts) - set(BUILDING_CATALOG_TYPES)
    if unknown_types:
        raise ValueError(f"Unbekannte Katalogtypen: {', '.join(sorted(unknown_types))}")

    for catalog_type in BUILDING_CATALOG_TYPES:
        catalog = load_building_excel_catalog(catalog_type, source_paths.get(catalog_type))
        source_records = tuple(_record_from_excel(catalog, row) for row in catalog.rows)
        draft_records = tuple(
            _record_from_user_draft(catalog_type, draft)
            for draft in user_drafts.get(catalog_type, ())
        )
        _ensure_unique_record_ids((*source_records, *draft_records), catalog_type)
        records_by_type[catalog_type] = (*source_records, *draft_records)
    return BuildingCatalogRegistry(MappingProxyType(records_by_type))


def create_user_catalog_draft(
    *,
    catalog_type: str,
    label: str,
    source_reference: str,
    source_url: str | None = None,
    details: str | None = None,
) -> dict[str, str]:
    """Erstellt einen speicherbaren lokalen Entwurf, ohne Quellwerte zu aendern."""
    if catalog_type not in BUILDING_CATALOG_TYPES:
        raise ValueError(f"Unbekannter Katalogtyp: {catalog_type}")
    if not isinstance(label, str) or not label.strip():
        raise ValueError("Ein eigener Katalogentwurf braucht einen Namen.")
    if not isinstance(source_reference, str) or not source_reference.strip():
        raise ValueError("Ein eigener Katalogentwurf braucht eine Herkunftsangabe.")
    normalized_url = _optional_text(source_url)
    return {
        "catalog_record_id": f"USR-{catalog_type[:3].upper()}-{uuid4().hex[:12].upper()}",
        "label": label.strip(),
        "source_reference": source_reference.strip(),
        "source_url": normalized_url or "",
        "details": _optional_text(details) or "",
        "created_at": datetime.now(UTC).isoformat(),
        "status": USER_DRAFT_STATUS,
    }


def _record_from_excel(catalog: BuildingExcelCatalog, row: Mapping[str, Any]) -> CatalogRecord:
    record_id = str(next(iter(row.values())))
    source_url = _source_url_from_row(row)
    return CatalogRecord(
        catalog_type=catalog.catalog_type,
        record_id=record_id,
        label=_label_from_row(row, record_id),
        source_kind="excel_source",
        provenance_status="source_url_available" if source_url else "source_url_missing_warning",
        source_path=catalog.source_path.as_posix(),
        source_sha256=catalog.source_sha256,
        source_url=source_url,
        data=MappingProxyType(dict(row)),
    )


def _record_from_user_draft(catalog_type: str, draft: Mapping[str, Any]) -> CatalogRecord:
    required = ("catalog_record_id", "label", "source_reference", "created_at", "status")
    if not all(isinstance(draft.get(field), str) and str(draft[field]).strip() for field in required):
        raise ValueError(f"Lokaler Entwurf fuer {catalog_type} ist unvollstaendig.")
    if draft["status"] != USER_DRAFT_STATUS:
        raise ValueError(f"Lokaler Entwurf fuer {catalog_type} hat keinen erlaubten Status.")
    source_url = _optional_text(draft.get("source_url"))
    return CatalogRecord(
        catalog_type=catalog_type,
        record_id=str(draft["catalog_record_id"]),
        label=str(draft["label"]),
        source_kind="user_draft",
        provenance_status="source_url_available" if source_url else "source_url_missing_warning",
        source_path=None,
        source_sha256=None,
        source_url=source_url,
        data=MappingProxyType(dict(draft)),
    )


def _ensure_unique_record_ids(records: Sequence[CatalogRecord], catalog_type: str) -> None:
    record_ids = [record.record_id for record in records]
    if len(record_ids) != len(set(record_ids)):
        raise ValueError(f"Katalogtyp {catalog_type} enthaelt kollidierende Datensatz-IDs.")


def _label_from_row(row: Mapping[str, Any], record_id: str) -> str:
    for key in ("Bezeichnung", "Bauteil", "Material", "Produkt", "Name"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return record_id


def _source_url_from_row(row: Mapping[str, Any]) -> str | None:
    for key in ("Quellen-URL", "Quelle-URL", "Produkt-URL", "URL"):
        value = _optional_text(row.get(key))
        if value:
            return value
    return None


def _optional_text(value: object) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None
