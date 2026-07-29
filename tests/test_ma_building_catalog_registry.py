from __future__ import annotations

from pathlib import Path

import pytest
from openpyxl import Workbook

from ma_building.catalog_registry import (
    build_building_catalog_registry,
    create_user_catalog_draft,
)


def _write_source_catalog(path: Path, catalog_type: str, rows: list[list[object]]) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Übersicht"
    id_headers = {"components": "Bauteil-ID", "materials": "Material-ID", "products": "Produkt-ID"}
    prefixes = {"components": "AW", "materials": "MAT", "products": "PROD"}
    sheet.append(["Titel"])
    sheet.append([])
    sheet.append([])
    sheet.append([id_headers[catalog_type], "Name", "Quellen-URL"])
    for index, row in enumerate(rows, start=1):
        sheet.append([f"{prefixes[catalog_type]}-{index:03d}", *row])
    workbook.save(path)


def _source_paths(tmp_path: Path) -> dict[str, Path]:
    paths = {catalog_type: tmp_path / f"{catalog_type}.xlsx" for catalog_type in ("components", "materials", "products")}
    for catalog_type, path in paths.items():
        _write_source_catalog(path, catalog_type, [[f"{catalog_type} source", "https://example.test/source"]])
    return paths


def test_registry_merges_sources_and_local_drafts_without_changing_source(tmp_path: Path) -> None:
    draft = create_user_catalog_draft(
        catalog_type="materials",
        label="Eigener Putz",
        source_reference="Eigene Eingabe vom 2026-07-28",
        details="Nur Entwurf, nicht simulationsfreigegeben.",
    )

    registry = build_building_catalog_registry(
        source_paths=_source_paths(tmp_path),
        user_drafts={"materials": [draft]},
    )

    records = registry.records_for("materials")
    assert [record.source_kind for record in records] == ["excel_source", "user_draft"]
    assert records[1].data["status"] == "user_unverified"
    assert records[1].provenance_status == "source_url_missing_warning"


def test_registry_rejects_id_collisions_instead_of_overwriting(tmp_path: Path) -> None:
    draft = create_user_catalog_draft(
        catalog_type="components",
        label="Eigene Wand",
        source_reference="Eigene Notiz",
    )
    draft["catalog_record_id"] = "AW-001"

    with pytest.raises(ValueError, match="kollidierende Datensatz-IDs"):
        build_building_catalog_registry(
            source_paths=_source_paths(tmp_path),
            user_drafts={"components": [draft]},
        )


def test_user_draft_requires_a_name_and_source_reference() -> None:
    with pytest.raises(ValueError, match="Namen"):
        create_user_catalog_draft(catalog_type="products", label="", source_reference="Eigene Notiz")
    with pytest.raises(ValueError, match="Herkunftsangabe"):
        create_user_catalog_draft(catalog_type="products", label="Eigener Entwurf", source_reference="")
