from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ma_building import LocalCatalogValidationError, load_local_building_catalog

_SPECS = {
    "materials": ("building_materials.yaml", "building_materials", "material_id"),
    "wall_constructions": ("building_wall_constructions.yaml", "building_wall_constructions", "wall_construction_id"),
    "surfaces": ("building_surfaces.yaml", "building_surfaces", "surface_id"),
}


def _write_catalog(directory: Path, key: str, records: list[dict[str, object]]) -> None:
    filename, catalog_type, _id_field = _SPECS[key]
    directory.mkdir(parents=True, exist_ok=True)
    (directory / filename).write_text(
        yaml.safe_dump({"schema_version": "1.0", "catalog_type": catalog_type, "records": records}, sort_keys=False),
        encoding="utf-8",
    )


@pytest.mark.parametrize("key", _SPECS)
def test_loads_valid_local_catalog(key: str, tmp_path: Path):
    _filename, _catalog_type, id_field = _SPECS[key]
    record = {"name": "Synthetischer Datensatz", id_field: "TEST-001"}
    if key == "wall_constructions":
        record["layers"] = [{"layer_no": 1, "material_name": "Synthetisch", "thickness_m": 0.1}]
    _write_catalog(tmp_path, key, [record])

    catalog = load_local_building_catalog(key, tmp_path)

    assert catalog.records[0]["name"] == "Synthetischer Datensatz"
    assert catalog.records[0][id_field] == "TEST-001"


def test_missing_catalog_remains_distinguishable(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_local_building_catalog("materials", tmp_path)


@pytest.mark.parametrize("key", _SPECS)
def test_rejects_duplicate_or_incomplete_ids(key: str, tmp_path: Path):
    _filename, _catalog_type, id_field = _SPECS[key]
    records = [{"name": "A", id_field: "DUP"}, {"name": "B", id_field: "DUP"}]
    _write_catalog(tmp_path, key, records)
    with pytest.raises(LocalCatalogValidationError, match="doppelte ID"):
        load_local_building_catalog(key, tmp_path)

    _write_catalog(tmp_path, key, [{"name": "A"}])
    with pytest.raises(LocalCatalogValidationError, match=id_field):
        load_local_building_catalog(key, tmp_path)


def test_rejects_invalid_wall_layers(tmp_path: Path):
    _write_catalog(
        tmp_path,
        "wall_constructions",
        [{"name": "A", "wall_construction_id": "BWCON-001", "layers": ["not-an-object"]}],
    )
    with pytest.raises(LocalCatalogValidationError, match="layers"):
        load_local_building_catalog("wall_constructions", tmp_path)


def test_rejects_present_invalid_yaml(tmp_path: Path):
    (tmp_path / "building_materials.yaml").write_text("records: [", encoding="utf-8")
    with pytest.raises(LocalCatalogValidationError, match="YAML"):
        load_local_building_catalog("materials", tmp_path)
