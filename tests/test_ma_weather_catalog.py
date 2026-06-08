from pathlib import Path

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

    assert len(catalog.datasets) == 1
    dataset = catalog.get("TRY_FFM_2015")

    assert isinstance(dataset, WeatherDataset)
    assert dataset.weather_key == "TRY_FFM_2015"
    assert dataset.file_path == Path("data/ma_weather/input/TRY_501262086894/TRY2015_501262086894_Jahr.dat")
    assert dataset.is_active is True


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
    placeholder_functions = [
        import_try_weather_file,
        validate_weather_dataframe,
        calculate_weather_metrics,
        build_weather_plots,
        write_weather_report,
        run_weather_analysis,
    ]

    for function in placeholder_functions:
        assert callable(function)
