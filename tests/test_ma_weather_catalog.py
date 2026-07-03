import importlib
import json
from dataclasses import replace
from pathlib import Path

import pandas as pd
import pytest
from ma_ui.pages.weather import (
    release_decision_matches_result,
    weather_diagnostic_rows,
    weather_source_rows,
)

from ma_core import InputSourceKind
from ma_validation import DiagnosticSeverity, ReleaseChoice, ReleaseStatus
from ma_weather import (
    ALL_WEATHER_PLOTS,
    WEATHER_PLOT_CHOICES,
    WEATHER_PLOT_SPECS,
    WeatherCatalog,
    WeatherDataset,
    WeatherDatasetImportDraft,
    WeatherDiscoveryStatus,
    WeatherLocationMappingSuggestion,
    WeatherLocationResolutionStatus,
    build_weather_output_paths,
    build_weather_plot,
    discover_weather_input_files,
    import_local_weather_dataset,
    import_weather_catalog,
    import_weather_location_catalog,
    register_discovered_weather_dataset,
    resolve_weather_file_location,
    stage_weather_input_file,
    suggest_weather_key,
    suggest_weather_location_mapping,
    transform_try_coordinates,
    update_weather_file_discovery,
    validate_weather_file_discovery,
    weather_discovery_rows,
)
from ma_weather.run_weather_analysis import plot_template_weather, record_weather_release_decision, run_weather_analysis
from ma_weather.try_importer import import_try_weather_file
from ma_weather.weather_catalog import DATASET_ROLE_SITE_SPECIFIC, DATASET_ROLE_TRY_REFERENCE
from ma_weather.weather_events import detect_critical_weather_events, weather_event_rows
from ma_weather.weather_file_discovery import _read_try_header_metadata
from ma_weather.weather_metrics import calculate_weather_metrics
from ma_weather.weather_plots import build_weather_plots
from ma_weather.weather_report import write_weather_report
from ma_weather.weather_selection import (
    WeatherSelectionState,
    activate_weather_dataset,
    load_weather_selection_state,
    project_default_weather_dataset,
    save_weather_selection_state,
    set_project_default_weather_dataset,
)
from ma_weather.weather_status import (
    WeatherImportCheckStatus,
    inspect_weather_dataset_status,
    stale_weather_status,
    weather_status_file_changed,
    weather_status_from_analysis_result,
)
from ma_weather.weather_validation import validate_weather_dataframe


def test_weather_catalog_imports_example_dataset():
    catalog = import_weather_catalog(include_local=False)

    assert len(catalog.datasets) == 18
    assert len(catalog.active_datasets()) == 18
    assert {dataset.weather_key for dataset in catalog.datasets} == {
        "TRY_FFM_2015_JAHR",
        "TRY_FFM_2015_SOMM",
        "TRY_FFM_2015_WINT",
        "TRY_FFM_2045_JAHR",
        "TRY_FFM_2045_SOMM",
        "TRY_FFM_2045_WINT",
        "TRY_MUC_2015_JAHR",
        "TRY_MUC_2015_SOMM",
        "TRY_MUC_2015_WINT",
        "TRY_MUC_2045_JAHR",
        "TRY_MUC_2045_SOMM",
        "TRY_MUC_2045_WINT",
        "TRY_HAM_2015_JAHR",
        "TRY_HAM_2015_SOMM",
        "TRY_HAM_2015_WINT",
        "TRY_HAM_2045_JAHR",
        "TRY_HAM_2045_SOMM",
        "TRY_HAM_2045_WINT",
    }

    frankfurt_dataset = catalog.get("TRY_FFM_2015_JAHR")
    frankfurt_2045_dataset = catalog.get("TRY_FFM_2045_JAHR")
    frankfurt_summer_dataset = catalog.get("TRY_FFM_2015_SOMM")
    frankfurt_winter_dataset = catalog.get("TRY_FFM_2015_WINT")
    munich_dataset = catalog.get("TRY_MUC_2015_JAHR")
    munich_2045_dataset = catalog.get("TRY_MUC_2045_JAHR")
    hamburg_dataset = catalog.get("TRY_HAM_2015_JAHR")
    hamburg_2045_dataset = catalog.get("TRY_HAM_2045_JAHR")

    assert isinstance(frankfurt_dataset, WeatherDataset)
    assert frankfurt_dataset.file_path == Path("data/ma_weather/input/TRY_501262086894/TRY2015_501262086894_Jahr.dat")
    assert frankfurt_2045_dataset.file_path == Path("data/ma_weather/input/TRY_501262086894/TRY2045_501262086894_Jahr.dat")
    assert frankfurt_summer_dataset.file_path == Path("data/ma_weather/input/TRY_501262086894/TRY2015_501262086894_Somm.dat")
    assert frankfurt_winter_dataset.file_path == Path("data/ma_weather/input/TRY_501262086894/TRY2015_501262086894_Wint.dat")
    assert munich_dataset.file_path == Path("data/ma_weather/input/TRY_481399115778/TRY2015_481399115778_Jahr.dat")
    assert munich_2045_dataset.file_path == Path("data/ma_weather/input/TRY_481399115778/TRY2045_481399115778_Jahr.dat")
    assert hamburg_dataset.file_path == Path("data/ma_weather/input/TRY_535578099766/TRY2015_535578099766_Jahr.dat")
    assert hamburg_2045_dataset.file_path == Path("data/ma_weather/input/TRY_535578099766/TRY2045_535578099766_Jahr.dat")
    assert frankfurt_dataset.dataset_role == DATASET_ROLE_SITE_SPECIFIC
    assert frankfurt_dataset.location_id == "LOC_049"
    assert frankfurt_dataset.reference_location_id == "LOC_053"
    assert munich_dataset.reference_location_id == "LOC_061"
    assert munich_2045_dataset.reference_location_id == "LOC_061"
    assert frankfurt_summer_dataset.year_type == "summer_extreme"
    assert frankfurt_winter_dataset.year_type == "winter_extreme"
    assert hamburg_dataset.dataset_role == DATASET_ROLE_TRY_REFERENCE
    assert hamburg_dataset.location_id == "LOC_009"
    assert hamburg_dataset.reference_location_id == "LOC_009"
    assert all(dataset.is_active for dataset in catalog.datasets)


def test_weather_catalog_allows_local_file_to_be_missing_by_default():
    catalog = import_weather_catalog(include_local=False)
    dataset = catalog.get("TRY_FFM_2015_JAHR")

    assert dataset.resolved_file_path().name == "TRY2015_501262086894_Jahr.dat"


def test_weather_catalog_imports_optional_location_resolution_fields(tmp_path):
    config_file = tmp_path / "weather_datasets.yaml"
    config_file.write_text(
        "weather_datasets:\n"
        "  - weather_key: TRY_TEST_2015_JAHR\n"
        "    display_name: TRY Test 2015 Jahr\n"
        "    file_path: data/ma_weather/input/TRY_000/TRY2015_000_Jahr.dat\n"
        "    file_format: TRY\n"
        "    source: DWD TRY\n"
        "    location: Testort\n"
        "    year_type: reference_year\n"
        "    climate_scenario: present\n"
        "    dataset_role: site_specific\n"
        "    location_id: LOC_TEST\n"
        "    reference_location_id: LOC_REF\n"
        "    source_easting: 4201500\n"
        "    source_northing: 2847500\n"
        "    source_crs_epsg: 3034\n"
        "    resolved_latitude: 52.4\n"
        "    resolved_longitude: 13.0\n"
        "    elevation_m: 34\n"
        "    detected_municipality_name: Potsdam\n"
        "    detected_municipality_code: '12054000'\n"
        "    detected_federal_state: Brandenburg\n"
        "    detected_postal_code: '14467'\n"
        "    location_resolution_status: matched\n"
        "    location_resolution_method: point_in_polygon\n"
        "    geodata_source_id: test_municipalities\n",
        encoding="utf-8",
    )

    dataset = import_weather_catalog(config_file, include_local=False).get("TRY_TEST_2015_JAHR")

    assert dataset.source_easting == 4201500
    assert dataset.source_crs_epsg == 3034
    assert dataset.detected_municipality_name == "Potsdam"
    assert dataset.detected_postal_code == "14467"
    assert dataset.location_resolution_status == "matched"


def test_weather_catalog_validates_required_fields(tmp_path):
    config_file = tmp_path / "weather_datasets.yaml"
    config_file.write_text(
        "weather_datasets:\n"
        "  - weather_key: ''\n"
        "    display_name: Test\n"
        "    file_path: data/ma_weather/input/missing.dat\n"
        "    file_format: TRY\n"
        "    source: DWD TRY\n"
        "    location: Frankfurt\n"
        "    year_type: reference_year\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="weather_key"):
        import_weather_catalog(config_file)


def test_weather_catalog_rejects_duplicate_weather_keys(tmp_path):
    config_file = tmp_path / "weather_datasets.yaml"
    config_file.write_text(
        "weather_datasets:\n"
        "  - weather_key: TRY_DUP\n"
        "    display_name: Test A\n"
        "    file_path: data/ma_weather/input/a.dat\n"
        "    file_format: TRY\n"
        "    source: DWD TRY\n"
        "    location: Frankfurt\n"
        "    year_type: reference_year\n"
        "  - weather_key: TRY_DUP\n"
        "    display_name: Test B\n"
        "    file_path: data/ma_weather/input/b.dat\n"
        "    file_format: TRY\n"
        "    source: DWD TRY\n"
        "    location: Frankfurt\n"
        "    year_type: reference_year\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="doppelt"):
        import_weather_catalog(config_file)


def test_weather_catalog_merges_local_import_catalog(tmp_path):
    base_config = tmp_path / "base_weather_datasets.yaml"
    local_config = tmp_path / "weather_datasets_local.yaml"
    base_config.write_text(
        "weather_datasets:\n"
        "  - weather_key: TRY_BASE\n"
        "    display_name: Base TRY\n"
        "    file_path: data/ma_weather/input/base.dat\n"
        "    file_format: TRY\n"
        "    source: Test\n"
        "    location: Base\n"
        "    year_type: reference_year\n",
        encoding="utf-8",
    )
    local_config.write_text(
        "weather_datasets:\n"
        "  - weather_key: TRY_LOCAL\n"
        "    display_name: Local TRY\n"
        "    file_path: data/ma_weather/input/custom/TRY_LOCAL/local.dat\n"
        "    file_format: TRY\n"
        "    source: Lokaler Import\n"
        "    location: Local\n"
        "    year_type: reference_year\n",
        encoding="utf-8",
    )

    catalog = import_weather_catalog(base_config, local_config_path=local_config, include_local=True)

    assert [dataset.weather_key for dataset in catalog.datasets] == ["TRY_BASE", "TRY_LOCAL"]


def test_weather_catalog_rejects_invalid_dataset_role(tmp_path):
    config_file = tmp_path / "weather_datasets.yaml"
    config_file.write_text(
        "weather_datasets:\n"
        "  - weather_key: TRY_TEST\n"
        "    display_name: Test\n"
        "    file_path: data/ma_weather/input/missing.dat\n"
        "    file_format: TRY\n"
        "    source: DWD TRY\n"
        "    location: Frankfurt\n"
        "    year_type: reference_year\n"
        "    dataset_role: unclear\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="dataset_role"):
        import_weather_catalog(config_file)


def test_weather_key_suggestion_uses_type_suffix():
    assert suggest_weather_key(location_code="FFM", year=2015, year_type="reference_year") == "TRY_FFM_2015_JAHR"
    assert suggest_weather_key(location_code="Muenchen", year=2045, year_type="summer_extreme") == "TRY_MUENCHEN_2045_SOMM"


def test_weather_file_discovery_finds_mannheim_try_files():
    mannheim_dir = Path("data/ma_weather/input/TRY_494997084777")
    if not mannheim_dir.exists():
        pytest.skip(f"Lokaler Mannheim-TRY-Ordner nicht vorhanden: {mannheim_dir}")

    discoveries = discover_weather_input_files(
        existing_catalog=import_weather_catalog(include_local=False),
        location_catalog=import_weather_location_catalog(),
    )
    discoveries_by_key = {discovery.weather_key: discovery for discovery in discoveries}

    assert set(discoveries_by_key) >= {
        "TRY_MA_2015_JAHR",
        "TRY_MA_2015_SOMM",
        "TRY_MA_2015_WINT",
        "TRY_MA_2045_JAHR",
        "TRY_MA_2045_SOMM",
        "TRY_MA_2045_WINT",
    }
    mannheim_discoveries = [
        discovery
        for discovery in discoveries
        if discovery.try_folder_key == "TRY_494997084777"
    ]
    assert len(mannheim_discoveries) == 6
    assert all(discovery.status is WeatherDiscoveryStatus.READY for discovery in mannheim_discoveries)
    assert all(discovery.location_id == "LOC_053" for discovery in mannheim_discoveries)
    assert all(discovery.reference_location_id == "LOC_053" for discovery in mannheim_discoveries)
    assert all(discovery.dataset_role == DATASET_ROLE_TRY_REFERENCE for discovery in mannheim_discoveries)
    assert {discovery.dataset_type for discovery in mannheim_discoveries} == {"Jahr", "Sommer", "Winter"}
    assert {discovery.climate_scenario for discovery in mannheim_discoveries} == {"present", "future_2045"}
    assert "TRY_501262086894" not in {discovery.try_folder_key for discovery in discoveries}
    assert weather_discovery_rows(mannheim_discoveries)[0]["TRY-Ordner"] == "TRY_494997084777"


def test_weather_file_discovery_creates_open_draft_without_location_mapping(tmp_path):
    try_file = tmp_path / "data" / "ma_weather" / "input" / "TRY_000000000000" / "TRY2015_000000000000_Jahr.dat"
    _write_try_header_file(try_file)

    discoveries = discover_weather_input_files(
        existing_catalog=WeatherCatalog([]),
        location_catalog=import_weather_location_catalog(),
        project_root=tmp_path,
    )

    assert len(discoveries) == 1
    discovery = discoveries[0]
    assert discovery.status is WeatherDiscoveryStatus.OPEN
    assert "location_id" in discovery.missing_fields
    assert discovery.is_complete is False
    assert discovery.metadata["location_resolution_status"] == "missing"


def test_weather_file_discovery_keeps_candidate_mapping_open(tmp_path):
    try_file = tmp_path / "data" / "ma_weather" / "input" / "TRY_000000000000" / "TRY2015_000000000000_Jahr.dat"
    mapping_file = tmp_path / "config" / "ma_weather" / "try_locations" / "example_try_file_locations.yaml"
    _write_try_header_file(try_file)
    mapping_file.parent.mkdir(parents=True)
    mapping_file.write_text(
        "try_file_locations:\n"
        "  - try_folder_key: TRY_000000000000\n"
        "    location_id: LOC_053\n"
        "    mapping_status: candidate\n"
        "    mapping_source: Koordinatenabschaetzung\n",
        encoding="utf-8",
    )

    discovery = discover_weather_input_files(
        existing_catalog=WeatherCatalog([]),
        location_catalog=import_weather_location_catalog(),
        mapping_path=mapping_file.relative_to(tmp_path),
        project_root=tmp_path,
    )[0]

    assert discovery.status is WeatherDiscoveryStatus.OPEN
    assert discovery.location_id == ""
    assert discovery.metadata["mapping_status"] == "candidate"
    assert discovery.metadata["location_resolution_source"] == "file_reference"
    assert discovery.metadata["location_resolution_status"] == "suggested"
    assert "location_id" in discovery.missing_fields


def test_weather_file_discovery_suggests_location_from_coordinates_without_auto_assignment(tmp_path):
    known_file = tmp_path / "data" / "ma_weather" / "input" / "TRY_494997084777" / "TRY2015_494997084777_Jahr.dat"
    unknown_file = tmp_path / "data" / "ma_weather" / "input" / "TRY_000000000000" / "TRY2015_000000000000_Jahr.dat"
    mapping_file = tmp_path / "config" / "ma_weather" / "try_locations" / "example_try_file_locations.yaml"
    _write_try_header_file(known_file)
    _write_try_header_file(unknown_file)
    mapping_file.parent.mkdir(parents=True)
    mapping_file.write_text(
        "try_file_locations:\n"
        "  - try_folder_key: TRY_494997084777\n"
        "    location_id: LOC_053\n"
        "    mapping_status: confirmed\n",
        encoding="utf-8",
    )
    location_catalog = import_weather_location_catalog()

    discoveries = discover_weather_input_files(
        existing_catalog=WeatherCatalog([]),
        location_catalog=location_catalog,
        mapping_path=mapping_file.relative_to(tmp_path),
        project_root=tmp_path,
    )
    known_discovery = next(discovery for discovery in discoveries if discovery.try_folder_key == "TRY_494997084777")
    unknown_discovery = next(discovery for discovery in discoveries if discovery.try_folder_key == "TRY_000000000000")

    assert unknown_discovery.location_id == ""
    assert unknown_discovery.metadata["suggested_location_id"] == "LOC_053"
    assert unknown_discovery.metadata["suggested_confidence"] == "hoch"
    assert unknown_discovery.metadata["location_resolution_source"] == "try_coordinates"
    assert unknown_discovery.metadata["location_resolution_status"] == "suggested"
    assert "location_id" in unknown_discovery.missing_fields
    suggestion = suggest_weather_location_mapping(
        unknown_discovery,
        location_catalog=location_catalog,
        reference_discoveries=[known_discovery],
    )
    assert isinstance(suggestion, WeatherLocationMappingSuggestion)
    assert suggestion.location_id == "LOC_053"


def test_weather_file_discovery_uses_explicit_header_location_reference(tmp_path):
    try_file = tmp_path / "data" / "ma_weather" / "input" / "TRY_111111111111" / "TRY2015_111111111111_Jahr.dat"
    try_file.parent.mkdir(parents=True, exist_ok=True)
    try_file.write_text(
        "Kopfbereich\n"
        "Standort          : Mannheim\n"
        "Rechtswert        : 3893500 Meter\n"
        "Hochwert          : 2532500 Meter\n"
        "Hoehenlage        : 97 Meter ueber NN\n"
        "***\n"
        "MM DD HH t RF WR WG B D\n",
        encoding="latin-1",
    )

    discovery = discover_weather_input_files(
        existing_catalog=WeatherCatalog([]),
        location_catalog=import_weather_location_catalog(),
        project_root=tmp_path,
    )[0]

    assert discovery.location_id == "LOC_053"
    assert discovery.metadata["location_resolution_source"] == "file_reference"
    assert discovery.metadata["location_resolution_status"] == "confirmed"
    assert "location_id" not in discovery.missing_fields


def test_weather_file_discovery_blocks_conflicting_header_and_mapping_location(tmp_path):
    try_file = tmp_path / "data" / "ma_weather" / "input" / "TRY_111111111111" / "TRY2015_111111111111_Jahr.dat"
    mapping_file = tmp_path / "config" / "ma_weather" / "try_locations" / "example_try_file_locations.yaml"
    try_file.parent.mkdir(parents=True, exist_ok=True)
    try_file.write_text(
        "Kopfbereich\n"
        "Standort          : Mannheim\n"
        "Rechtswert        : 3893500 Meter\n"
        "Hochwert          : 2532500 Meter\n"
        "***\n"
        "MM DD HH t RF WR WG B D\n",
        encoding="latin-1",
    )
    mapping_file.parent.mkdir(parents=True)
    mapping_file.write_text(
        "try_file_locations:\n"
        "  - try_folder_key: TRY_111111111111\n"
        "    location_id: LOC_049\n"
        "    mapping_status: confirmed\n",
        encoding="utf-8",
    )

    discovery = discover_weather_input_files(
        existing_catalog=WeatherCatalog([]),
        location_catalog=import_weather_location_catalog(),
        mapping_path=mapping_file.relative_to(tmp_path),
        project_root=tmp_path,
    )[0]

    assert discovery.location_id == ""
    assert discovery.metadata["location_resolution_status"] == "conflict"
    assert "location_resolution" in discovery.missing_fields


def test_weather_location_resolution_is_optional_without_geodata_config(tmp_path):
    result = resolve_weather_file_location(
        {"rechtswert_m": "4201500 Meter", "hochwert_m": "2847500 Meter"},
        project_root=tmp_path,
    )

    assert result.status is WeatherLocationResolutionStatus.NOT_CONFIGURED
    assert result.is_blocking is False


def test_weather_location_resolution_blocks_enabled_config_without_municipality_source(tmp_path):
    config = tmp_path / "config" / "ma_weather" / "geodata" / "example_weather_geodata_sources.yaml"
    config.parent.mkdir(parents=True)
    config.write_text("enabled: true\ngeodata_sources: []\n", encoding="utf-8")

    result = resolve_weather_file_location(
        {"rechtswert_m": "4201500 Meter", "hochwert_m": "2847500 Meter"},
        geodata_config_path=config.relative_to(tmp_path),
        project_root=tmp_path,
    )

    assert result.status is WeatherLocationResolutionStatus.GEODATA_MISSING
    assert result.is_blocking is True


def test_transform_try_coordinates_uses_epsg_3034():
    pytest.importorskip("pyproj")

    longitude, latitude = transform_try_coordinates(4201500, 2847500)

    assert 5.0 < longitude < 16.0
    assert 47.0 < latitude < 56.0


def test_weather_location_resolution_blocks_implausible_try_coordinates(tmp_path):
    config = tmp_path / "config" / "ma_weather" / "geodata" / "example_weather_geodata_sources.yaml"
    config.parent.mkdir(parents=True)
    config.write_text(
        "enabled: true\n"
        "geodata_sources:\n"
        "  - source_id: test_municipalities\n"
        "    kind: municipality\n"
        "    path: data/ma_weather/geodata/administrative/municipalities.geojson\n"
        "    crs_epsg: 4326\n"
        "    name_field: municipality_name\n"
        "    code_field: municipality_code\n"
        "    state_field: federal_state\n",
        encoding="utf-8",
    )

    result = resolve_weather_file_location(
        {"rechtswert_m": "130658 Meter", "hochwert_m": "524031 Meter"},
        geodata_config_path=config.relative_to(tmp_path),
        project_root=tmp_path,
    )

    assert result.status is WeatherLocationResolutionStatus.INVALID_COORDINATES
    assert result.is_blocking is True
    assert any("Rechtswert" in message for message in result.messages)


def test_weather_location_resolution_matches_municipality_geojson(tmp_path):
    pytest.importorskip("pyproj")
    pytest.importorskip("shapely")

    longitude, latitude = transform_try_coordinates(4201500, 2847500)
    geodata = tmp_path / "data" / "ma_weather" / "geodata" / "administrative" / "municipalities.geojson"
    config = tmp_path / "config" / "ma_weather" / "geodata" / "example_weather_geodata_sources.yaml"
    geodata.parent.mkdir(parents=True)
    config.parent.mkdir(parents=True)
    geodata.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {
                            "municipality_name": "Potsdam",
                            "municipality_code": "12054000",
                            "federal_state": "Brandenburg",
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [longitude - 0.1, latitude - 0.1],
                                    [longitude + 0.1, latitude - 0.1],
                                    [longitude + 0.1, latitude + 0.1],
                                    [longitude - 0.1, latitude + 0.1],
                                    [longitude - 0.1, latitude - 0.1],
                                ]
                            ],
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    config.write_text(
        "enabled: true\n"
        "geodata_sources:\n"
        "  - source_id: test_municipalities\n"
        "    kind: municipality\n"
        "    path: data/ma_weather/geodata/administrative/municipalities.geojson\n"
        "    crs_epsg: 4326\n"
        "    name_field: municipality_name\n"
        "    code_field: municipality_code\n"
        "    state_field: federal_state\n",
        encoding="utf-8",
    )

    result = resolve_weather_file_location(
        {
            "rechtswert_m": "4201500 Meter",
            "hochwert_m": "2847500 Meter",
            "hoehenlage_m": "34 Meter ueber NN",
        },
        geodata_config_path=config.relative_to(tmp_path),
        project_root=tmp_path,
    )

    assert result.status is WeatherLocationResolutionStatus.MATCHED
    assert result.is_blocking is False
    assert result.municipality_name == "Potsdam"
    assert result.municipality_code == "12054000"
    assert result.federal_state == "Brandenburg"
    assert result.elevation_m == 34


def test_bkg_vg250_geodata_source_config_is_active():
    config_text = Path("config/ma_weather/geodata/example_weather_geodata_sources.yaml").read_text(encoding="utf-8")

    assert "enabled: true" in config_text
    assert "path: data/ma_weather/geodata/germany/germany_municipalities.geojson" in config_text
    assert "crs_epsg: 4326" in config_text
    assert "name_field: GEN" in config_text
    assert "code_field: AGS" in config_text
    assert "state_field: LKZ" in config_text
    assert "filter_field: GF" in config_text
    assert 'filter_value: "4"' in config_text


def test_local_bkg_vg250_geodata_resolves_potsdam_and_berlin_when_available():
    pytest.importorskip("pyproj")
    pytest.importorskip("shapely")

    geodata_path = Path("data/ma_weather/geodata/germany/germany_municipalities.geojson")
    if not geodata_path.exists():
        pytest.skip("Lokale BKG-VG250-Gemeinde-GeoJSON-Datei ist nicht vorhanden.")

    cases = (
        (
            Path("data/ma_weather/input/TRY_524031130658/TRY2015_524031130658_Jahr.dat"),
            "Potsdam",
            "12054000",
            "BB",
        ),
        (
            Path("data/ma_weather/input/TRY_525331134258/TRY2045_525331134258_Jahr.dat"),
            "Berlin",
            "11000000",
            "BE",
        ),
    )
    missing_files = [path for path, *_ in cases if not path.exists()]
    if missing_files:
        pytest.skip(f"Lokale Berlin-/Potsdam-TRY-Testdateien fehlen: {missing_files}")

    for path, expected_name, expected_ags, expected_state in cases:
        result = resolve_weather_file_location(_read_try_header_metadata(path))

        assert result.status is WeatherLocationResolutionStatus.MATCHED
        assert result.is_blocking is False
        assert result.municipality_name == expected_name
        assert result.municipality_code == expected_ags
        assert result.federal_state == expected_state


def test_local_discovery_uses_bkg_vg250_locations_when_available(tmp_path):
    pytest.importorskip("pyproj")
    pytest.importorskip("shapely")

    geodata_path = Path("data/ma_weather/geodata/germany/germany_municipalities.geojson")
    if not geodata_path.exists():
        pytest.skip("Lokale BKG-VG250-Gemeinde-GeoJSON-Datei ist nicht vorhanden.")

    expected_files = {
        "data/ma_weather/input/TRY_524031130658/TRY2015_524031130658_Jahr.dat": (
            "LOC_020",
            "Potsdam",
            DATASET_ROLE_TRY_REFERENCE,
        ),
        "data/ma_weather/input/TRY_525331134258/TRY2045_525331134258_Jahr.dat": (
            "LOC_013",
            "Berlin",
            DATASET_ROLE_SITE_SPECIFIC,
        ),
    }
    missing_files = [Path(path) for path in expected_files if not Path(path).exists()]
    if missing_files:
        pytest.skip(f"Lokale Berlin-/Potsdam-TRY-Testdateien fehlen: {missing_files}")
    empty_mapping = tmp_path / "empty_try_file_locations.yaml"
    empty_mapping.write_text("try_file_locations: []\n", encoding="utf-8")

    discoveries = discover_weather_input_files(
        existing_catalog=WeatherCatalog([]),
        location_catalog=import_weather_location_catalog(),
        mapping_path=empty_mapping,
    )
    discoveries_by_path = {discovery.file_path.as_posix(): discovery for discovery in discoveries}

    for path, (expected_location_id, expected_name, expected_role) in expected_files.items():
        discovery = discoveries_by_path[path]

        assert discovery.location_id == expected_location_id
        assert discovery.location_name == expected_name
        assert discovery.dataset_role == expected_role
        assert discovery.metadata["location_resolution_source"] == "try_coordinates"
        assert discovery.metadata["location_resolution_status"] == "confirmed"


def test_local_discovery_maps_vg250_places_to_confirmed_climate_map_points_when_available():
    pytest.importorskip("pyproj")
    pytest.importorskip("shapely")

    geodata_path = Path("data/ma_weather/geodata/germany/germany_municipalities.geojson")
    if not geodata_path.exists():
        pytest.skip("Lokale BKG-VG250-Gemeinde-GeoJSON-Datei ist nicht vorhanden.")

    expected_files = {
        "data/ma_weather/input/TRY_486536098525/TRY2015_486536098525_Jahr.dat": (
            "Geislingen an der Steige",
            "LOC_064",
            "Stoetten",
            DATASET_ROLE_TRY_REFERENCE,
            "TRY_OAL_2015_JAHR",
        ),
        "data/ma_weather/input/TRY_504215129662/TRY2015_504215129662_Jahr.dat": (
            "Oberwiesenthal",
            "LOC_048",
            "Fichtelberg",
            DATASET_ROLE_TRY_REFERENCE,
            "TRY_FBG_2015_JAHR",
        ),
        "data/ma_weather/input/TRY_506557079568/TRY2015_506557079568_Jahr.dat": (
            "Bad Marienberg (Westerwald)",
            "LOC_033",
            "Bad Marienberg",
            DATASET_ROLE_TRY_REFERENCE,
            "TRY_WW_2015_JAHR",
        ),
        "data/ma_weather/input/TRY_485721134578/TRY2015_485721134578_Jahr.dat": (
            "Passau",
            "LOC_061",
            "Passau",
            DATASET_ROLE_TRY_REFERENCE,
            "TRY_PA_2015_JAHR",
        ),
    }
    missing_files = [Path(path) for path in expected_files if not Path(path).exists()]
    if missing_files:
        pytest.skip(f"Lokale TRY-Testdateien fuer Klimakartenpunkte fehlen: {missing_files}")

    discoveries = discover_weather_input_files(
        existing_catalog=import_weather_catalog(),
        location_catalog=import_weather_location_catalog(),
    )
    discoveries_by_path = {discovery.file_path.as_posix(): discovery for discovery in discoveries}

    for path, (detected_name, expected_location_id, expected_name, expected_role, expected_key) in expected_files.items():
        discovery = discoveries_by_path[path]

        assert discovery.metadata["detected_municipality_name"] == detected_name
        assert discovery.location_id == expected_location_id
        assert discovery.location_name == expected_name
        assert discovery.reference_location_id == expected_location_id
        assert discovery.dataset_role == expected_role
        assert discovery.weather_key == expected_key
        assert discovery.is_complete is True


def test_stage_weather_input_file_writes_try_file_without_catalog_entry(tmp_path):
    staged_file = stage_weather_input_file(
        _small_try_file_content(),
        original_filename="TRY2015_494997084777_Jahr.dat",
        project_root=tmp_path,
    )

    assert staged_file.file_path == Path("data/ma_weather/input/TRY_494997084777/TRY2015_494997084777_Jahr.dat")
    assert staged_file.try_folder_key == "TRY_494997084777"
    assert (tmp_path / staged_file.file_path).exists()
    assert not (tmp_path / "data" / "ma_weather" / "config" / "datasets" / "weather_datasets_local.yaml").exists()


def test_stage_weather_input_file_rejects_unclear_filename(tmp_path):
    with pytest.raises(ValueError, match="TRY-Muster"):
        stage_weather_input_file(
            _small_try_file_content(),
            original_filename="mannheim.dat",
            project_root=tmp_path,
        )


def test_update_weather_file_discovery_adjusts_location_and_reference(tmp_path):
    try_file = tmp_path / "data" / "ma_weather" / "input" / "TRY_494997084777" / "TRY2015_494997084777_Jahr.dat"
    mapping_file = tmp_path / "config" / "ma_weather" / "try_locations" / "example_try_file_locations.yaml"
    _write_try_header_file(try_file)
    mapping_file.parent.mkdir(parents=True)
    mapping_file.write_text(
        "try_file_locations:\n"
        "  - try_folder_key: TRY_494997084777\n"
        "    location_id: LOC_053\n",
        encoding="utf-8",
    )
    location_catalog = import_weather_location_catalog()
    discovery = discover_weather_input_files(
        existing_catalog=WeatherCatalog([]),
        location_catalog=location_catalog,
        mapping_path=mapping_file.relative_to(tmp_path),
        project_root=tmp_path,
    )[0]

    updated_discovery = update_weather_file_discovery(
        discovery,
        location_catalog=location_catalog,
        location_id="LOC_049",
        dataset_type="Sommer",
        climate_scenario="future_2045",
        dataset_role="",
        year=2045,
        weather_key="",
        display_name="",
    )

    assert updated_discovery.location_id == "LOC_049"
    assert updated_discovery.reference_location_id == "LOC_053"
    assert updated_discovery.year_type == "summer_extreme"
    assert updated_discovery.climate_scenario == "future_2045"
    assert updated_discovery.dataset_role == DATASET_ROLE_SITE_SPECIFIC
    assert updated_discovery.weather_key == "TRY_FFM_2045_SOMM"
    assert updated_discovery.display_name == "TRY Frankfurt (Main) 2045 Sommer"
    assert updated_discovery.metadata["location_resolution_source"] == "manual"
    assert updated_discovery.metadata["location_resolution_status"] == "confirmed"
    assert updated_discovery.is_complete is True


def test_validate_weather_file_discovery_blocks_duplicate_key(tmp_path):
    try_file = tmp_path / "data" / "ma_weather" / "input" / "TRY_494997084777" / "TRY2015_494997084777_Jahr.dat"
    mapping_file = tmp_path / "config" / "ma_weather" / "try_locations" / "example_try_file_locations.yaml"
    try_file.parent.mkdir(parents=True)
    try_file.write_bytes(_small_try_file_content())
    mapping_file.parent.mkdir(parents=True)
    mapping_file.write_text(
        "try_file_locations:\n"
        "  - try_folder_key: TRY_494997084777\n"
        "    location_id: LOC_053\n",
        encoding="utf-8",
    )
    location_catalog = import_weather_location_catalog()
    discovery = discover_weather_input_files(
        existing_catalog=WeatherCatalog([]),
        location_catalog=location_catalog,
        mapping_path=mapping_file.relative_to(tmp_path),
        project_root=tmp_path,
    )[0]
    duplicate_catalog = WeatherCatalog([
        WeatherDataset(
            weather_key=discovery.weather_key,
            display_name="Duplicate",
            file_path=Path("data/ma_weather/input/duplicate.dat"),
            file_format="TRY",
            source="DWD TRY",
            location="Mannheim",
            year_type="reference_year",
        )
    ])

    result = validate_weather_file_discovery(
        discovery,
        existing_catalog=duplicate_catalog,
        project_root=tmp_path,
        warnings_released=True,
    )

    assert result.can_register is False
    assert any("weather_key ist bereits vorhanden" in message for message in result.messages)


def test_register_discovered_weather_dataset_writes_relative_local_catalog(tmp_path):
    try_file = tmp_path / "data" / "ma_weather" / "input" / "TRY_494997084777" / "TRY2015_494997084777_Jahr.dat"
    mapping_file = tmp_path / "config" / "ma_weather" / "try_locations" / "example_try_file_locations.yaml"
    _write_try_header_file(try_file)
    mapping_file.parent.mkdir(parents=True)
    mapping_file.write_text(
        "try_file_locations:\n"
        "  - try_folder_key: TRY_494997084777\n"
        "    location_id: LOC_053\n",
        encoding="utf-8",
    )
    discoveries = discover_weather_input_files(
        existing_catalog=WeatherCatalog([]),
        location_catalog=import_weather_location_catalog(),
        mapping_path=mapping_file.relative_to(tmp_path),
        project_root=tmp_path,
    )

    dataset = register_discovered_weather_dataset(
        discoveries[0],
        existing_catalog=WeatherCatalog([]),
        local_catalog_path=Path("data/ma_weather/config/datasets/weather_datasets_local.yaml"),
        project_root=tmp_path,
    )

    assert dataset.weather_key == "TRY_MA_2015_JAHR"
    assert dataset.file_path == Path("data/ma_weather/input/TRY_494997084777/TRY2015_494997084777_Jahr.dat")
    assert dataset.file_path.is_absolute() is False
    assert dataset.dataset_role == DATASET_ROLE_TRY_REFERENCE
    assert dataset.is_active is True
    assert dataset.location_resolution_source == "file_reference"
    assert dataset.location_resolution_status == "confirmed"
    local_catalog = tmp_path / "data" / "ma_weather" / "config" / "datasets" / "weather_datasets_local.yaml"
    catalog_text = local_catalog.read_text(encoding="utf-8")
    assert "TRY_MA_2015_JAHR" in catalog_text
    assert "data/ma_weather/input/TRY_494997084777/TRY2015_494997084777_Jahr.dat" in catalog_text
    assert "is_active: true" in catalog_text


def test_local_weather_import_copies_file_and_writes_relative_catalog(tmp_path):
    existing_catalog = import_weather_catalog(include_local=False)
    draft = WeatherDatasetImportDraft(
        weather_key="TRY_LOCAL_TEST",
        display_name="TRY Local Test",
        original_filename="local_test.dat",
        location="Testort",
        year_type="reference_year",
        climate_scenario="present",
        dataset_role=DATASET_ROLE_SITE_SPECIFIC,
        location_id="LOC_TEST",
        reference_location_id="LOC_REF",
    )

    result = import_local_weather_dataset(
        _small_try_file_content(),
        draft=draft,
        existing_catalog=existing_catalog,
        project_root=tmp_path,
        local_catalog_path=Path("data/ma_weather/config/datasets/weather_datasets_local.yaml"),
        input_dir=Path("data/ma_weather/input/custom"),
        session_id="session_test",
        run_id="run_test",
        import_id="import_test",
    )

    assert result.copied_file_path.exists()
    assert result.dataset.file_path == Path("data/ma_weather/input/custom/TRY_LOCAL_TEST/local_test.dat")
    assert result.dataset.file_path.is_absolute() is False
    assert result.status.import_id == "import_test"
    assert result.status.session_id == "session_test"
    assert result.status.run_id == "run_test"
    assert result.status.is_open is True
    catalog_text = result.catalog_path.read_text(encoding="utf-8")
    assert "TRY_LOCAL_TEST" in catalog_text
    assert "data/ma_weather/input/custom/TRY_LOCAL_TEST/local_test.dat" in catalog_text


def test_local_weather_import_rejects_duplicate_weather_key(tmp_path):
    existing_catalog = import_weather_catalog(include_local=False)
    draft = WeatherDatasetImportDraft(
        weather_key="TRY_FFM_2015_JAHR",
        display_name="TRY Duplicate",
        original_filename="duplicate.dat",
        location="Frankfurt am Main",
        year_type="reference_year",
        climate_scenario="present",
        dataset_role=DATASET_ROLE_SITE_SPECIFIC,
        location_id="LOC_049",
        reference_location_id="LOC_053",
    )

    with pytest.raises(ValueError, match="bereits vorhanden"):
        import_local_weather_dataset(
            _small_try_file_content(),
            draft=draft,
            existing_catalog=existing_catalog,
            project_root=tmp_path,
        )


def test_local_weather_import_rejects_invalid_metadata(tmp_path):
    existing_catalog = import_weather_catalog(include_local=False)
    draft = WeatherDatasetImportDraft(
        weather_key="TRY BAD",
        display_name="TRY Bad",
        original_filename="bad.txt",
        location="Testort",
        year_type="unknown",
        climate_scenario="present",
        dataset_role=DATASET_ROLE_SITE_SPECIFIC,
        location_id="LOC_TEST",
        reference_location_id="LOC_REF",
    )

    with pytest.raises(ValueError, match="weather_key"):
        import_local_weather_dataset(
            b"not relevant",
            draft=draft,
            existing_catalog=existing_catalog,
            project_root=tmp_path,
        )


def test_local_weather_import_reports_open_status_for_invalid_file(tmp_path):
    existing_catalog = import_weather_catalog(include_local=False)
    draft = WeatherDatasetImportDraft(
        weather_key="TRY_LOCAL_BROKEN",
        display_name="TRY Local Broken",
        original_filename="broken.dat",
        location="Testort",
        year_type="reference_year",
        climate_scenario="present",
        dataset_role=DATASET_ROLE_SITE_SPECIFIC,
        location_id="LOC_TEST",
        reference_location_id="LOC_REF",
    )

    result = import_local_weather_dataset(
        b"keine TRY Daten",
        draft=draft,
        existing_catalog=existing_catalog,
        project_root=tmp_path,
    )

    assert result.status.is_open is True
    assert result.status.error_count == 1
    assert result.status.is_regularly_selectable is False


def test_weather_location_catalog_resolves_city_region_and_reference():
    catalog = import_weather_location_catalog()

    assert len(catalog.regions) == 15
    frankfurt = catalog.get_location_by_name("Frankfurt (Main)")
    region = catalog.region_for_location(frankfurt.location_id)
    reference_location = catalog.reference_location_for_city(frankfurt.location_id)

    assert frankfurt.location_id == "LOC_049"
    assert region.region_code == "TRY12"
    assert reference_location.location_name == "Mannheim"
    assert reference_location.is_reference_location is True

    passau = catalog.get_location_by_name("Passau")
    munich = catalog.get_location_by_name("Muenchen")
    region13 = catalog.region_for_location(passau.location_id)
    munich_reference = catalog.reference_location_for_city(munich.location_id)
    legacy_codes = [location.legacy_code for location in catalog.locations if location.legacy_code]

    assert region13.region_code == "TRY13"
    assert region13.reference_location_id == passau.location_id
    assert passau.is_reference_location is True
    assert munich_reference.location_name == "Passau"
    assert len(legacy_codes) == len(set(legacy_codes))


def test_weather_dataset_selection_prioritizes_site_specific_then_reference_for_city():
    weather_catalog = import_weather_catalog(include_local=False)
    location_catalog = import_weather_location_catalog()

    hamburg = location_catalog.get_location_by_name("Hamburg")
    hamburg_reference = location_catalog.reference_location_for_city(hamburg.location_id)
    hamburg_datasets = weather_catalog.datasets_for_location(
        location_id=hamburg.location_id,
        reference_location_id=hamburg_reference.location_id,
    )

    assert [dataset.weather_key for dataset in hamburg_datasets] == [
        "TRY_HAM_2015_JAHR",
        "TRY_HAM_2015_SOMM",
        "TRY_HAM_2015_WINT",
        "TRY_HAM_2045_JAHR",
        "TRY_HAM_2045_SOMM",
        "TRY_HAM_2045_WINT",
    ]
    assert all(dataset.dataset_role == DATASET_ROLE_TRY_REFERENCE for dataset in hamburg_datasets)

    frankfurt = location_catalog.get_location_by_name("Frankfurt (Main)")
    frankfurt_reference = location_catalog.reference_location_for_city(frankfurt.location_id)
    frankfurt_datasets = weather_catalog.datasets_for_location(
        location_id=frankfurt.location_id,
        reference_location_id=frankfurt_reference.location_id,
    )

    assert [dataset.weather_key for dataset in frankfurt_datasets] == [
        "TRY_FFM_2015_JAHR",
        "TRY_FFM_2015_SOMM",
        "TRY_FFM_2015_WINT",
        "TRY_FFM_2045_JAHR",
        "TRY_FFM_2045_SOMM",
        "TRY_FFM_2045_WINT",
    ]
    assert all(dataset.dataset_role == DATASET_ROLE_SITE_SPECIFIC for dataset in frankfurt_datasets)
    assert not any(dataset.dataset_role == DATASET_ROLE_TRY_REFERENCE for dataset in frankfurt_datasets)

    synthetic_catalog = WeatherCatalog(
        [
            WeatherDataset(
                weather_key="TRY_REF",
                display_name="TRY Referenz",
                file_path=Path("data/ma_weather/input/ref.dat"),
                file_format="TRY",
                source="DWD TRY",
                location="Referenz",
                year_type="reference_year",
                dataset_role=DATASET_ROLE_TRY_REFERENCE,
                reference_location_id="LOC_REF",
                selection_priority=10,
            ),
            WeatherDataset(
                weather_key="TRY_CITY",
                display_name="TRY Stadt",
                file_path=Path("data/ma_weather/input/city.dat"),
                file_format="TRY",
                source="DWD TRY",
                location="Stadt",
                year_type="reference_year",
                dataset_role=DATASET_ROLE_SITE_SPECIFIC,
                location_id="LOC_CITY",
                reference_location_id="LOC_REF",
                selection_priority=20,
            ),
        ]
    )

    city_datasets = synthetic_catalog.datasets_for_location(
        location_id="LOC_CITY",
        reference_location_id="LOC_REF",
    )
    reference_datasets = synthetic_catalog.datasets_for_reference_location(reference_location_id="LOC_REF")

    assert [dataset.weather_key for dataset in city_datasets] == ["TRY_CITY", "TRY_REF"]
    assert [dataset.weather_key for dataset in reference_datasets] == ["TRY_REF"]


def test_weather_placeholder_modules_are_importable():
    weather_functions = [
        import_try_weather_file,
        validate_weather_dataframe,
        calculate_weather_metrics,
        build_weather_plots,
        write_weather_report,
        run_weather_analysis,
    ]

    for function in weather_functions:
        assert callable(function)


def test_weather_plot_catalog_lists_existing_diagrams():
    assert ALL_WEATHER_PLOTS == "all"
    assert WEATHER_PLOT_CHOICES == tuple(spec.plot_key for spec in WEATHER_PLOT_SPECS)
    assert WEATHER_PLOT_CHOICES == (
        "temperature_year",
        "temperature_heatmap",
        "monthly_radiation",
        "monthly_degree_hours",
        "wind_rose",
        "temperature_humidity_scatter",
    )


def test_try_importer_reads_data_block_and_calculates_global_radiation(tmp_path):
    try_file = _write_small_try_file(tmp_path)

    result = import_try_weather_file(try_file, weather_key="TRY_TEST", start_year=2015)

    assert result.weather_key == "TRY_TEST"
    assert result.row_count == 4
    assert result.data.index[0] == pd.Timestamp("2015-01-01 00:00:00")
    assert result.data.index[-1] == pd.Timestamp("2015-01-01 03:00:00")
    assert "global_radiation_w_m2" in result.data.columns
    assert result.data["global_radiation_w_m2"].tolist() == [0, 15, 50, 80]
    assert result.source.source_kind is InputSourceKind.IMPORT
    assert result.source.adapter_key == "ma_weather.try_importer"
    assert result.source.file_size_bytes == try_file.stat().st_size
    assert len(result.source.sha256 or "") == 64
    assert result.import_diagnostic.record_count == 4
    assert result.import_diagnostic.accepted_count == 4


def test_weather_validation_reports_warnings_and_errors(tmp_path):
    result = import_try_weather_file(_write_small_try_file(tmp_path), start_year=2015)
    invalid_data = result.data.copy()
    invalid_data.loc[invalid_data.index[0], "relative_humidity_pct"] = 120
    invalid_data = pd.concat([invalid_data, invalid_data.iloc[[0]]])

    report = validate_weather_dataframe(invalid_data, expected_hours=8760)

    assert report.status == "error"
    assert report.row_count == 5
    assert report.duplicate_timestamps == 1
    assert any("8760" in warning for warning in report.warnings)
    assert any("Relative Feuchte" in warning for warning in report.warnings)
    assert report.validation_result.release_status is ReleaseStatus.BLOCKED
    assert any(
        message.code == "WEATHER_DUPLICATE_TIMESTAMPS"
        and message.severity is DiagnosticSeverity.ERROR
        for message in report.validation_result.messages
    )


def test_weather_metrics_are_structured_and_non_negative(tmp_path):
    result = import_try_weather_file(_write_small_try_file(tmp_path), start_year=2015)

    metrics = calculate_weather_metrics(result.data, heating_base_c=20, cooling_base_c=26)

    assert metrics.mean_temperature_c == pytest.approx(20.25)
    assert metrics.max_temperature_c == 31
    assert metrics.hours_above_25c == 2
    assert metrics.hours_above_30c == 1
    assert metrics.heating_degree_hours_kh is not None
    assert metrics.heating_degree_hours_kh >= 0
    assert metrics.cooling_degree_hours_kh is not None
    assert metrics.cooling_degree_hours_kh >= 0
    assert metrics.global_radiation_kwh_m2a == pytest.approx(0.145)


def test_critical_weather_events_detect_days_and_periods():
    index = pd.date_range("2045-07-01 00:00:00", periods=120, freq="h")
    data = pd.DataFrame(
        {
            "temperature_c": [10] * 24 + [20] * 24 + [30] * 24 + [25] * 24 + [5] * 24,
            "global_radiation_w_m2": [100] * 24 + [200] * 24 + [500] * 24 + [300] * 24 + [50] * 24,
            "wind_speed_m_s": [1] * 24 + [2] * 24 + [3] * 24 + [9] * 24 + [4] * 24,
        },
        index=index,
    )

    events = detect_critical_weather_events(data, weather_key="TRY_TEST_SOMM")
    event_by_type = {event.event_type: event for event in events}

    assert event_by_type["hottest_day"].weather_key == "TRY_TEST_SOMM"
    assert event_by_type["hottest_day"].start_time == pd.Timestamp("2045-07-03").to_pydatetime()
    assert event_by_type["coldest_day"].start_time == pd.Timestamp("2045-07-05").to_pydatetime()
    assert event_by_type["hottest_3day_period"].start_time == pd.Timestamp("2045-07-02").to_pydatetime()
    assert event_by_type["hottest_3day_period"].end_time == pd.Timestamp("2045-07-04 23:00").to_pydatetime()
    assert event_by_type["highest_radiation_day"].value == pytest.approx(12.0)
    assert event_by_type["strongest_wind_day"].value == pytest.approx(9.0)
    assert weather_event_rows(events)[0]["weather_key"] == "TRY_TEST_SOMM"


def test_critical_weather_events_skip_missing_optional_columns():
    index = pd.date_range("2045-01-01 00:00:00", periods=72, freq="h")
    data = pd.DataFrame({"temperature_c": [0] * 24 + [-5] * 24 + [3] * 24}, index=index)

    event_types = {
        event.event_type
        for event in detect_critical_weather_events(data, weather_key="TRY_TEST_WINT")
    }

    assert "coldest_day" in event_types
    assert "highest_radiation_day" not in event_types
    assert "strongest_wind_day" not in event_types


def test_weather_plots_and_report_are_written(tmp_path):
    dataset = WeatherDataset(
        weather_key="TRY_TEST",
        display_name="Test TRY",
        file_path=Path("test_try.dat"),
        file_format="TRY",
        source="Test",
        location="Testort",
        year_type="test_year",
    )
    import_result = import_try_weather_file(_write_small_try_file(tmp_path), weather_key=dataset.weather_key)
    validation_report = validate_weather_dataframe(import_result.data, expected_hours=4)
    metrics = calculate_weather_metrics(import_result.data)

    plot_results = build_weather_plots(import_result.data, weather_key=dataset.weather_key, output_dir=tmp_path / "plots")
    report_path = write_weather_report(
        dataset=dataset,
        import_result=import_result,
        validation_report=validation_report,
        metrics=metrics,
        plot_results=plot_results,
        output_dir=tmp_path / "reports",
    )

    assert any(plot.path and plot.path.exists() for plot in plot_results)
    assert report_path.exists()
    assert "Wetterbericht TRY_TEST" in report_path.read_text(encoding="utf-8")


def test_weather_output_paths_build_run_folder_structure(tmp_path):
    output_paths = build_weather_output_paths(
        "TRY TEST/2015",
        "run 01",
        output_root=tmp_path / "weather_output",
    )

    assert output_paths.run_output_dir == tmp_path / "weather_output" / "TRY_TEST_2015" / "run_01"
    assert output_paths.data_dir == output_paths.run_output_dir / "data"
    assert output_paths.plots_dir == output_paths.run_output_dir / "plots"
    assert output_paths.reports_dir == output_paths.run_output_dir / "reports"
    assert output_paths.processed_data_path.name == "TRY_TEST_2015_weather_data.csv"
    assert output_paths.report_path.name == "TRY_TEST_2015_weather_report.md"
    assert output_paths.manifest_path == output_paths.run_output_dir / "weather_run_manifest.json"


def test_weather_plot_builder_allows_single_plot_and_all(tmp_path):
    import_result = import_try_weather_file(_write_small_try_file(tmp_path), weather_key="TRY_TEST")

    single_result = build_weather_plot(
        import_result.data,
        weather_key="TRY_TEST",
        output_dir=tmp_path / "single_plot",
        plot_key="temperature_year",
    )
    selected_results = build_weather_plots(
        import_result.data,
        weather_key="TRY_TEST",
        output_dir=tmp_path / "selected_plots",
        plot_keys=("temperature_year",),
    )
    all_results = build_weather_plots(
        import_result.data,
        weather_key="TRY_TEST",
        output_dir=tmp_path / "all_plots",
        plot_keys=ALL_WEATHER_PLOTS,
    )

    assert single_result.plot_key == "temperature_year"
    assert single_result.path is not None
    assert single_result.path.exists()
    assert [result.plot_key for result in selected_results] == ["temperature_year"]
    assert tuple(result.plot_key for result in all_results) == WEATHER_PLOT_CHOICES
    with pytest.raises(ValueError, match="Unbekanntes Wetterdiagramm"):
        build_weather_plot(
            import_result.data,
            weather_key="TRY_TEST",
            output_dir=tmp_path / "invalid_plot",
            plot_key="unknown",
        )


def test_weather_runner_processes_catalog_dataset(tmp_path):
    input_dir = tmp_path / "data" / "ma_weather" / "input"
    input_dir.mkdir(parents=True)
    try_file = _write_small_try_file(input_dir)
    catalog_file = tmp_path / "weather_datasets.yaml"
    catalog_file.write_text(
        "weather_datasets:\n"
        "  - weather_key: TRY_TEST\n"
        "    display_name: Test TRY\n"
        f"    file_path: {try_file.relative_to(tmp_path).as_posix()}\n"
        "    file_format: TRY\n"
        "    source: Test\n"
        "    location: Testort\n"
        "    year_type: test_year\n",
        encoding="utf-8",
    )

    result = run_weather_analysis(
        "TRY_TEST",
        catalog_path=catalog_file,
        project_root=tmp_path,
        session_id="session_weather_test",
        run_id="weather_run_test",
        import_id="weather_import_test",
        print_summary=False,
    )

    assert result.import_result.row_count == 4
    assert result.run_output_dir == tmp_path / "data" / "ma_weather" / "output" / "TRY_TEST" / "weather_run_test"
    assert result.processed_data_path.exists()
    assert result.processed_data_path.parent == result.run_output_dir / "data"
    assert result.report_path.exists()
    assert result.report_path.parent == result.run_output_dir / "reports"
    assert result.manifest_path.exists()
    assert result.manifest_path == result.run_output_dir / "weather_run_manifest.json"
    assert result.session_id == "session_weather_test"
    assert result.run_id == "weather_run_test"
    assert result.import_id == "weather_import_test"
    assert result.release_decision is None
    assert result.validation_report.validation_result.release_status is ReleaseStatus.CONFIRMATION_REQUIRED
    assert result.session_log_path.exists()
    assert all(plot.path is None or plot.path.parent == result.run_output_dir / "plots" for plot in result.plot_results)
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["dataset"]["weather_key"] == "TRY_TEST"
    assert manifest["ids"] == {
        "session_id": "session_weather_test",
        "run_id": "weather_run_test",
        "import_id": "weather_import_test",
    }
    assert manifest["artifacts"]["processed_data"].endswith("TRY_TEST_weather_data.csv")
    assert manifest["artifacts"]["processed_data"] == (
        "data/ma_weather/output/TRY_TEST/weather_run_test/data/TRY_TEST_weather_data.csv"
    )
    assert manifest["artifacts"]["report"].endswith("TRY_TEST_weather_report.md")
    assert manifest["artifacts"]["run_output_dir"] == "data/ma_weather/output/TRY_TEST/weather_run_test"
    assert manifest["artifacts"]["plots"]

    second_result = run_weather_analysis(
        "TRY_TEST",
        catalog_path=catalog_file,
        project_root=tmp_path,
        session_id="session_weather_test",
        run_id="weather_run_test_2",
        import_id="weather_import_test_2",
        print_summary=False,
    )
    assert second_result.run_output_dir != result.run_output_dir
    assert second_result.processed_data_path != result.processed_data_path
    assert second_result.manifest_path.exists()

    blocked_decision = record_weather_release_decision(
        result,
        choice=ReleaseChoice.KEEP_BLOCKED,
        note="Testlauf bleibt zunaechst blockiert.",
    )
    decision = record_weather_release_decision(
        result,
        choice=ReleaseChoice.RELEASE_WITH_WARNINGS,
        note="Vier Stunden sind fuer diesen Test beabsichtigt.",
    )
    assert blocked_decision.resulting_status is ReleaseStatus.BLOCKED
    assert decision.resulting_status is ReleaseStatus.RELEASED
    assert weather_source_rows(result)[0]["Quellen-ID"] == result.import_result.source.source_id
    assert any(row["Code"] == "WEATHER_HOUR_COUNT_MISMATCH" for row in weather_diagnostic_rows(result))
    assert release_decision_matches_result(decision, result) is True
    assert release_decision_matches_result(decision, replace(result, run_id="other_run")) is False
    log_text = result.session_log_path.read_text(encoding="utf-8")
    assert '"event_type": "run_started"' in log_text
    assert '"event_type": "input_source_loaded"' in log_text
    assert '"event_type": "diagnostic_recorded"' in log_text
    assert '"event_type": "run_completed"' in log_text
    assert '"event_type": "release_decided"' in log_text
    assert "weather_import_test" in log_text
    assert decision.decision_id in log_text


def test_plot_template_weather_runner_allows_single_plot(tmp_path):
    input_dir = tmp_path / "data" / "ma_weather" / "input"
    input_dir.mkdir(parents=True)
    try_file = _write_small_try_file(input_dir)
    catalog_file = tmp_path / "weather_datasets.yaml"
    catalog_file.write_text(
        "weather_datasets:\n"
        "  - weather_key: TRY_TEST\n"
        "    display_name: Test TRY\n"
        f"    file_path: {try_file.relative_to(tmp_path).as_posix()}\n"
        "    file_format: TRY\n"
        "    source: Test\n"
        "    location: Testort\n"
        "    year_type: test_year\n",
        encoding="utf-8",
    )

    result = plot_template_weather(
        "TRY_TEST",
        catalog_path=catalog_file,
        project_root=tmp_path,
        run_id="plot_weather_run_test",
        plot_key="temperature_year",
        print_summary=False,
    )

    assert [plot.plot_key for plot in result.plot_results] == ["temperature_year"]
    assert result.run_output_dir == tmp_path / "data" / "ma_weather" / "output" / "TRY_TEST" / "plot_weather_run_test"
    assert result.plot_results[0].path is not None
    assert result.plot_results[0].path.exists()
    assert result.plot_results[0].path.parent == result.run_output_dir / "plots"
    assert result.manifest_path.exists()


def test_plot_template_weather_cli_forwards_diagram(monkeypatch):
    weather_runner = importlib.import_module("ma_weather.run_weather_analysis")
    calls: dict[str, object] = {}

    def fake_plot_template_weather(weather_key, **kwargs):
        calls["weather_key"] = weather_key
        calls.update(kwargs)

    monkeypatch.setattr(weather_runner, "plot_template_weather", fake_plot_template_weather)

    weather_runner.main_plot_template_weather(
        [
            "temperature_year",
            "--weather-key",
            "TRY_TEST",
            "--catalog",
            "weather_datasets.yaml",
            "--start-year",
            "2045",
            "--output-root",
            "data/test_weather_output",
        ]
    )

    assert calls["weather_key"] == "TRY_TEST"
    assert calls["catalog_path"] == "weather_datasets.yaml"
    assert calls["start_year"] == 2045
    assert calls["output_dir"] == "data/test_weather_output"
    assert calls["plot_key"] == "temperature_year"


def test_weather_dataset_status_reports_missing_and_warning(tmp_path):
    missing_dataset = WeatherDataset(
        weather_key="TRY_MISSING",
        display_name="Missing TRY",
        file_path=Path("data/ma_weather/input/missing.dat"),
        file_format="TRY",
        source="Test",
        location="Testort",
        year_type="test_year",
    )
    missing_status = inspect_weather_dataset_status(missing_dataset, project_root=tmp_path)

    assert missing_status.file_exists is False
    assert missing_status.is_open is True
    assert missing_status.is_regularly_selectable is False

    try_file = _write_small_try_file(tmp_path)
    checked_dataset = WeatherDataset(
        weather_key="TRY_TEST",
        display_name="Test TRY",
        file_path=try_file.relative_to(tmp_path),
        file_format="TRY",
        source="Test",
        location="Testort",
        year_type="test_year",
    )
    checked_status = inspect_weather_dataset_status(checked_dataset, project_root=tmp_path, validate_file=True)

    assert checked_status.file_exists is True
    assert checked_status.import_status is WeatherImportCheckStatus.WARNING
    assert checked_status.release_status is ReleaseStatus.CONFIRMATION_REQUIRED
    assert checked_status.is_open is True
    assert checked_status.is_regularly_selectable is False


def test_weather_dataset_status_marks_changed_file_as_stale(tmp_path):
    try_file = _write_small_try_file(tmp_path)
    dataset = WeatherDataset(
        weather_key="TRY_TEST",
        display_name="Test TRY",
        file_path=try_file.relative_to(tmp_path),
        file_format="TRY",
        source="Test",
        location="Testort",
        year_type="test_year",
    )
    previous_status = inspect_weather_dataset_status(dataset, project_root=tmp_path, validate_file=True)
    try_file.write_bytes(_small_try_file_content() + b"\n")
    current_status = inspect_weather_dataset_status(dataset, project_root=tmp_path, validate_file=False)

    stale_status = stale_weather_status(current_status, previous_status)

    assert weather_status_file_changed(previous_status, current_status) is True
    assert stale_status.import_status is WeatherImportCheckStatus.STALE
    assert stale_status.status_label == "Pruefung veraltet"
    assert stale_status.is_open is True
    assert stale_status.is_regularly_selectable is False


def test_weather_selection_state_requires_release_before_activation(tmp_path):
    state = WeatherSelectionState()

    with pytest.raises(ValueError, match="freigegebene"):
        activate_weather_dataset(
            state,
            "TRY_TEST",
            release_status=ReleaseStatus.CONFIRMATION_REQUIRED,
            import_id="weather_import_test",
        )

    state = activate_weather_dataset(
        state,
        "TRY_TEST",
        release_status=ReleaseStatus.RELEASED,
        import_id="weather_import_test",
    )
    assert state.is_activated("TRY_TEST") is True

    with pytest.raises(ValueError, match="aktivierte"):
        set_project_default_weather_dataset(state, "TRY_OTHER")

    state = set_project_default_weather_dataset(state, "TRY_TEST")
    assert state.project_default_weather_key == "TRY_TEST"

    state_path = tmp_path / "weather_selection_state.yaml"
    save_weather_selection_state(state, state_path)
    loaded_state = load_weather_selection_state(state_path)
    assert loaded_state.project_default_weather_key == "TRY_TEST"
    assert loaded_state.activation_for("TRY_TEST").import_id == "weather_import_test"


def test_project_default_weather_dataset_returns_only_activated_default(tmp_path):
    try_file = _write_small_try_file(tmp_path)
    catalog_file = tmp_path / "weather_datasets.yaml"
    catalog_file.write_text(
        "weather_datasets:\n"
        "  - weather_key: TRY_TEST\n"
        "    display_name: Test TRY\n"
        f"    file_path: {try_file.relative_to(tmp_path).as_posix()}\n"
        "    file_format: TRY\n"
        "    source: Test\n"
        "    location: Testort\n"
        "    year_type: test_year\n",
        encoding="utf-8",
    )
    catalog = import_weather_catalog(catalog_file)
    state = activate_weather_dataset(
        WeatherSelectionState(),
        "TRY_TEST",
        release_status=ReleaseStatus.RELEASED,
        import_id="weather_import_test",
    )

    assert project_default_weather_dataset(catalog, state) is None

    state = set_project_default_weather_dataset(state, "TRY_TEST")
    assert project_default_weather_dataset(catalog, state).weather_key == "TRY_TEST"


def test_weather_status_from_analysis_result_uses_release_decision(tmp_path):
    input_dir = tmp_path / "data" / "ma_weather" / "input"
    input_dir.mkdir(parents=True)
    try_file = _write_small_try_file(input_dir)
    catalog_file = tmp_path / "weather_datasets.yaml"
    catalog_file.write_text(
        "weather_datasets:\n"
        "  - weather_key: TRY_TEST\n"
        "    display_name: Test TRY\n"
        f"    file_path: {try_file.relative_to(tmp_path).as_posix()}\n"
        "    file_format: TRY\n"
        "    source: Test\n"
        "    location: Testort\n"
        "    year_type: test_year\n",
        encoding="utf-8",
    )
    result = run_weather_analysis(
        "TRY_TEST",
        catalog_path=catalog_file,
        project_root=tmp_path,
        session_id="session_weather_status_test",
        run_id="weather_status_test",
        import_id="weather_import_status_test",
        print_summary=False,
    )
    decision = record_weather_release_decision(
        result,
        choice=ReleaseChoice.RELEASE_WITH_WARNINGS,
        note="Testwarnung bewusst freigegeben.",
    )

    status = weather_status_from_analysis_result(result, decision=decision)

    assert status.import_id == "weather_import_status_test"
    assert status.release_status is ReleaseStatus.RELEASED
    assert status.can_be_activated is True


def test_real_try_file_integration_if_local_file_exists():
    catalog = import_weather_catalog()
    dataset = catalog.get("TRY_FFM_2015_JAHR")
    file_path = dataset.resolved_file_path()
    if not file_path.exists():
        pytest.skip(f"Lokale TRY-Datei nicht vorhanden: {file_path}")

    result = import_try_weather_file(file_path, weather_key=dataset.weather_key)
    report = validate_weather_dataframe(result.data)

    assert result.row_count == 8760
    assert report.duplicate_timestamps == 0


def _write_small_try_file(directory: Path) -> Path:
    try_file = directory / "TRY_TEST.dat"
    try_file.write_text(
        "Kopfbereich\n"
        "***\n"
        "MM DD HH t RF WR WG B D\n"
        "1 1 1 5 80 180 2 0 0\n"
        "1 1 2 15 70 190 3 10 5\n"
        "1 1 3 30 55 200 4 30 20\n"
        "1 1 4 31 50 210 5 50 30\n",
        encoding="utf-8",
    )
    return try_file


def _write_try_header_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "Kopfbereich\n"
        "Rechtswert        : 3893500 Meter\n"
        "Hochwert          : 2532500 Meter\n"
        "Hoehenlage        : 97 Meter ueber NN\n"
        "Art des TRY       : mittleres Jahr\n"
        "Bezugszeitraum    : 1995-2012\n"
        "***\n"
        "MM DD HH t RF WR WG B D\n",
        encoding="latin-1",
    )


def _small_try_file_content() -> bytes:
    return (
        "Kopfbereich\n"
        "***\n"
        "MM DD HH t RF WR WG B D\n"
        "1 1 1 5 80 180 2 0 0\n"
        "1 1 2 15 70 190 3 10 5\n"
        "1 1 3 30 55 200 4 30 20\n"
        "1 1 4 31 50 210 5 50 30\n"
    ).encode("utf-8")
