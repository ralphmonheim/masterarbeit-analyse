from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ma_core import sha256_file
from ma_database import load_demo_catalog, select_demo_record
from ma_ui.streamlit_app.module_views.technical_view import _demo_label, _demo_record_rows

_TEST_RECORD_FILES = {
    "materials": ("materials.yaml", "material_id", "MAT-TEST-0001"),
    "constructions": ("constructions.yaml", "construction_id", "CON-TEST-0001"),
    "heating_generators": ("heating_generators.yaml", "heating_generator_id", "HEAT-TEST-0001"),
    "cooling_generators": ("cooling_generators.yaml", "cooling_generator_id", "COOL-TEST-0001"),
    "thermal_storages": ("thermal_storages.yaml", "storage_id", "STORE-TEST-0001"),
}


def _write_test_catalog(target: Path) -> Path:
    """Creates a neutral catalog fixture without using the local catalog data."""
    target.mkdir()
    record_counts: dict[str, int] = {}
    file_hashes: dict[str, str] = {}

    for category, (file_name, identifier_field, record_id) in _TEST_RECORD_FILES.items():
        path = target / file_name
        path.write_text(
            yaml.safe_dump(
                {
                    "records": [
                        {
                            identifier_field: record_id,
                            "name_de": "Neutraler Testeintrag",
                            "verification_status": "draft_unverified",
                            "confirmation_status": "unconfirmed",
                        }
                    ]
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        record_counts[category] = 1
        file_hashes[file_name] = sha256_file(path)

    layer_path = target / "construction_layers.yaml"
    layer_path.write_text(
        yaml.safe_dump(
            {
                "records": [
                    {
                        "construction_id": "CON-TEST-0001",
                        "material_ref": "MAT-TEST-0001",
                        "layer_no": 1,
                        "thickness_m": 0.1,
                        "layer_function": "test_only",
                    }
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    record_counts["construction_layers"] = 1
    file_hashes[layer_path.name] = sha256_file(layer_path)

    (target / "manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "catalog_id": "CAT-TEST-0001",
                "catalog_version": "test",
                "status": "draft",
                "files": file_hashes,
                "record_counts": record_counts,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return target


def test_catalog_loader_uses_neutral_generated_fixture(tmp_path: Path) -> None:
    catalog = load_demo_catalog(_write_test_catalog(tmp_path / "catalog"))

    assert catalog.catalog_id == "CAT-TEST-0001"
    assert {category: len(catalog.records_for(category)) for category in catalog.records_by_category} == {
        category: 1 for category in _TEST_RECORD_FILES
    }
    assert all(
        record.data["verification_status"] == "draft_unverified"
        for records in catalog.records_by_category.values()
        for record in records
    )
    assert len(catalog.layers_for("CON-TEST-0001")) == 1


def test_catalog_selection_is_unverified_and_does_not_mutate_record(tmp_path: Path) -> None:
    catalog = load_demo_catalog(_write_test_catalog(tmp_path / "catalog"))
    record = catalog.records_for("heating_generators")[0]

    selection = select_demo_record(catalog, category="heating_generators", record_id=record.record_id)

    assert selection.record_id == record.record_id
    assert selection.selection_status == "demo_unverified"
    with pytest.raises(TypeError):
        record.data["name_de"] = "Andere Bezeichnung"


def test_catalog_rejects_changed_local_file(tmp_path: Path) -> None:
    catalog_directory = _write_test_catalog(tmp_path / "catalog")
    (catalog_directory / "materials.yaml").write_text("records: []\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Pruefsumme"):
        load_demo_catalog(catalog_directory)


def test_missing_local_catalog_is_reported_as_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_demo_catalog(tmp_path / "not-present")


def test_demo_ui_rows_keep_unverified_status_visible(tmp_path: Path) -> None:
    catalog = load_demo_catalog(_write_test_catalog(tmp_path / "catalog"))
    record = catalog.records_for("thermal_storages")[0]
    selection = select_demo_record(catalog, category=record.category, record_id=record.record_id)

    rows = {row["Merkmal"]: row["Wert"] for row in _demo_record_rows(record, selection)}

    assert _demo_label(catalog.records_for(record.category), record.record_id).startswith(record.label)
    assert rows["Auswahlstatus"] == "demo_unverified"
    assert rows["Pruefstatus"] == "draft_unverified"
