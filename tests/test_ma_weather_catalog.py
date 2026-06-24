from dataclasses import replace
from pathlib import Path

import pandas as pd
import pytest

from ma_core import InputSourceKind
from ma_ui.pages.weather import (
    release_decision_matches_result,
    weather_diagnostic_rows,
    weather_source_rows,
)
from ma_validation import DiagnosticSeverity, ReleaseChoice, ReleaseStatus
from ma_weather import (
    WeatherDataset,
    WeatherDatasetImportDraft,
    import_local_weather_dataset,
    import_weather_catalog,
    import_weather_location_catalog,
    suggest_weather_key,
)
from ma_weather.run_weather_analysis import record_weather_release_decision, run_weather_analysis
from ma_weather.try_importer import import_try_weather_file
from ma_weather.weather_catalog import DATASET_ROLE_SITE_SPECIFIC, DATASET_ROLE_TRY_REFERENCE
from ma_weather.weather_events import detect_critical_weather_events, weather_event_rows
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


def test_weather_dataset_selection_prioritizes_reference_then_site_specific():
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
    assert result.processed_data_path.exists()
    assert result.report_path.exists()
    assert result.session_id == "session_weather_test"
    assert result.run_id == "weather_run_test"
    assert result.import_id == "weather_import_test"
    assert result.release_decision is None
    assert result.validation_report.validation_result.release_status is ReleaseStatus.CONFIRMATION_REQUIRED
    assert result.session_log_path.exists()

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
