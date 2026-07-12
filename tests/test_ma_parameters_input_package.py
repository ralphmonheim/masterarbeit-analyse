from pathlib import Path

from ma_parameters import (
    BUSINESS_INTEGRATION_LOD1_INPUT_PACKAGE_ID,
    BUSINESS_INTEGRATION_LOD1_INPUT_PACKAGE_VERSION,
    build_baseline_parameter_snapshot_from_input_package,
    build_business_integration_lod1_parameter_snapshot,
    build_lod1_parameter_input_package,
    build_lod1_parameter_input_package_from_selection,
    parameter_input_package_source_rows,
    parameter_input_package_summary_rows,
    parameter_input_package_value_rows,
    validate_baseline_parameter_snapshot,
    validate_parameter_input_package,
)
from ma_validation import ReleaseStatus
from ma_weather import (
    WeatherCatalog,
    WeatherDataset,
    WeatherDatasetStatus,
    WeatherFileStatus,
    WeatherImportCheckStatus,
    WeatherSelectionState,
    activate_weather_dataset,
    set_project_default_weather_dataset,
)


def _codes(result):
    return {message.code for message in result.messages}


def _weather_dataset() -> WeatherDataset:
    return WeatherDataset(
        weather_key="TRY_TEST_PASSAU",
        display_name="TRY Test Passau",
        file_path=Path("data/ma_weather/input/TRY_TEST_PASSAU.dat"),
        file_format="try",
        source="DWD TRY",
        location="Passau",
        year_type="TRY2015",
        climate_scenario="reference",
        dataset_role="try_reference",
        reference_location_id="TRY-PASSAU",
    )


def _weather_status(
    dataset: WeatherDataset,
    *,
    release_status: ReleaseStatus = ReleaseStatus.RELEASED,
) -> WeatherDatasetStatus:
    return WeatherDatasetStatus(
        weather_key=dataset.weather_key,
        display_name=dataset.display_name,
        file_path=dataset.file_path,
        file_exists=True,
        file_status=WeatherFileStatus.AVAILABLE,
        import_status=WeatherImportCheckStatus.SUCCESS,
        release_status=release_status,
        import_id="weather_import_test",
        source_id="weather_source_test",
        row_count=8760,
        file_size_bytes=12345,
        modified_ns=67890,
    )


def _activated_selection_state(dataset: WeatherDataset, status: WeatherDatasetStatus) -> WeatherSelectionState:
    state = activate_weather_dataset(
        WeatherSelectionState(),
        dataset.weather_key,
        release_status=ReleaseStatus.RELEASED,
        import_id=status.import_id,
    )
    return set_project_default_weather_dataset(state, dataset.weather_key)


def test_parameter_input_package_requires_weather_source():
    source_snapshot = build_business_integration_lod1_parameter_snapshot()
    input_package = build_lod1_parameter_input_package(
        source_snapshot,
        package_id=BUSINESS_INTEGRATION_LOD1_INPUT_PACKAGE_ID,
        package_version=BUSINESS_INTEGRATION_LOD1_INPUT_PACKAGE_VERSION,
    )

    result = validate_parameter_input_package(input_package)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "PARAMETER_INPUT_WEATHER_SOURCE_MISSING" in _codes(result)
    assert "PARAMETER_INPUT_WEATHER_KEY_MISSING" in _codes(result)


def test_baseline_from_invalid_input_package_is_not_released():
    source_snapshot = build_business_integration_lod1_parameter_snapshot()
    input_package = build_lod1_parameter_input_package(
        source_snapshot,
        package_id="PARAM-INPUT-MISSING-WEATHER",
        package_version="PARAM-INPUT-MISSING-WEATHER-V1",
    )

    baseline = build_baseline_parameter_snapshot_from_input_package(
        input_package,
        snapshot_id="PARAM-BASELINE-MISSING-WEATHER",
        snapshot_version="PARAM-BASELINE-MISSING-WEATHER-V2",
    )
    result = validate_baseline_parameter_snapshot(baseline)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BASELINE_RELEASE_STATUS_BLOCKED" in _codes(result)


def test_parameter_input_package_rejects_unactivated_weather_source():
    source_snapshot = build_business_integration_lod1_parameter_snapshot()
    dataset = _weather_dataset()
    status = _weather_status(dataset)
    input_package = build_lod1_parameter_input_package(
        source_snapshot,
        package_id="PARAM-INPUT-UNACTIVATED",
        package_version="PARAM-INPUT-UNACTIVATED-V1",
        weather_dataset=dataset,
        weather_status=status,
        weather_is_activated=False,
    )

    result = validate_parameter_input_package(input_package)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "PARAMETER_INPUT_WEATHER_NOT_ACTIVATED" in _codes(result)


def test_parameter_input_package_rejects_unreleased_weather_source():
    source_snapshot = build_business_integration_lod1_parameter_snapshot()
    dataset = _weather_dataset()
    status = _weather_status(dataset, release_status=ReleaseStatus.BLOCKED)
    input_package = build_lod1_parameter_input_package(
        source_snapshot,
        package_id="PARAM-INPUT-BLOCKED-WEATHER",
        package_version="PARAM-INPUT-BLOCKED-WEATHER-V1",
        weather_dataset=dataset,
        weather_status=status,
        weather_is_activated=True,
    )

    result = validate_parameter_input_package(input_package)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "PARAMETER_INPUT_SOURCE_NOT_RELEASED" in _codes(result)


def test_parameter_input_package_accepts_activated_released_project_default():
    source_snapshot = build_business_integration_lod1_parameter_snapshot()
    dataset = _weather_dataset()
    status = _weather_status(dataset)
    selection_state = _activated_selection_state(dataset, status)

    input_package = build_lod1_parameter_input_package_from_selection(
        source_snapshot,
        WeatherCatalog([dataset]),
        selection_state,
        weather_statuses_by_key={dataset.weather_key: status},
        package_id="PARAM-INPUT-WEATHER-OK",
        package_version="PARAM-INPUT-WEATHER-OK-V1",
    )
    result = validate_parameter_input_package(input_package)
    value_rows = parameter_input_package_value_rows(input_package)
    source_rows = parameter_input_package_source_rows(input_package)
    summary_rows = parameter_input_package_summary_rows(input_package)

    assert result.release_status is ReleaseStatus.RELEASED
    assert result.messages == ()
    assert input_package.weather_activated is True
    assert "ma_weather" in {row["Modul"] for row in source_rows}
    assert {"weather.weather_key", "weather.location", "weather.year_type"} <= {
        row["Parameter"] for row in value_rows
    }
    assert {row["Kennwert"] for row in summary_rows} >= {"Eingangspaket", "Wetter aktiviert"}

    baseline = build_baseline_parameter_snapshot_from_input_package(
        input_package,
        snapshot_id="PARAM-BASELINE-FROM-INPUT-PACKAGE",
        snapshot_version="PARAM-BASELINE-FROM-INPUT-PACKAGE-V2",
    )
    baseline_result = validate_baseline_parameter_snapshot(baseline)

    assert baseline_result.release_status is ReleaseStatus.RELEASED
    assert baseline_result.messages == ()
    assert "ma_weather" in {source.module_key for source in baseline.source_references}
