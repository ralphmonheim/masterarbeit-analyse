from pathlib import Path

import pandas as pd
import pytest

from ma_weather import WeatherDataset, import_weather_catalog
from ma_weather.run_weather_analysis import run_weather_analysis
from ma_weather.try_importer import import_try_weather_file
from ma_weather.weather_metrics import calculate_weather_metrics
from ma_weather.weather_plots import build_weather_plots
from ma_weather.weather_report import write_weather_report
from ma_weather.weather_validation import validate_weather_dataframe


def test_weather_catalog_imports_example_dataset():
    catalog = import_weather_catalog()

    assert len(catalog.datasets) == 6
    assert len(catalog.active_datasets()) == 6
    assert {dataset.weather_key for dataset in catalog.datasets} == {
        "TRY_FFM_2015",
        "TRY_FFM_2045",
        "TRY_MUC_2015",
        "TRY_MUC_2045",
        "TRY_HAM_2015",
        "TRY_HAM_2045",
    }

    frankfurt_dataset = catalog.get("TRY_FFM_2015")
    frankfurt_2045_dataset = catalog.get("TRY_FFM_2045")
    munich_dataset = catalog.get("TRY_MUC_2015")
    munich_2045_dataset = catalog.get("TRY_MUC_2045")
    hamburg_dataset = catalog.get("TRY_HAM_2015")
    hamburg_2045_dataset = catalog.get("TRY_HAM_2045")

    assert isinstance(frankfurt_dataset, WeatherDataset)
    assert frankfurt_dataset.file_path == Path("data/ma_weather/input/TRY_501262086894/TRY2015_501262086894_Jahr.dat")
    assert frankfurt_2045_dataset.file_path == Path("data/ma_weather/input/TRY_501262086894/TRY2045_501262086894_Jahr.dat")
    assert munich_dataset.file_path == Path("data/ma_weather/input/TRY_481399115778/TRY2015_481399115778_Jahr.dat")
    assert munich_2045_dataset.file_path == Path("data/ma_weather/input/TRY_481399115778/TRY2045_481399115778_Jahr.dat")
    assert hamburg_dataset.file_path == Path("data/ma_weather/input/TRY_535578099766/TRY2015_535578099766_Jahr.dat")
    assert hamburg_2045_dataset.file_path == Path("data/ma_weather/input/TRY_535578099766/TRY2045_535578099766_Jahr.dat")
    assert all(dataset.is_active for dataset in catalog.datasets)


def test_weather_catalog_allows_local_file_to_be_missing_by_default():
    catalog = import_weather_catalog()
    dataset = catalog.get("TRY_FFM_2015")

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
        print_summary=False,
    )

    assert result.import_result.row_count == 4
    assert result.processed_data_path.exists()
    assert result.report_path.exists()


def test_real_try_file_integration_if_local_file_exists():
    catalog = import_weather_catalog()
    dataset = catalog.get("TRY_FFM_2015")
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
