import json

import pytest

from ma_data_preparation.models import (
    DataSuitability,
    SeriesProvenance,
    StandardizedRecord,
    StandardizedSeries,
    TimeSemantics,
)
from ma_data_preparation.quality import assess_series
from ma_data_preparation.services import prepare_dataset
from ma_data_preparation.time_series import integrate_power_kwh, prepare_series


def _series(records, *, semantics=TimeSemantics.INTERVAL_AVERAGE, expected_step_hours=None):
    return StandardizedSeries(
        "heating_power",
        "heating_power",
        "W",
        semantics,
        SeriesProvenance("synthetic", "case-1"),
        tuple(StandardizedRecord(time, value) for time, value in records),
        expected_step_hours,
    )


def test_variable_time_steps_are_weighted_when_prepared_and_integrated():
    series = _series(((0.0, 1000.0), (0.5, 1000.0), (2.0, 2000.0)))

    prepared = prepare_series(series)

    assert [record.value for record in prepared.records] == [1000.0, 1000.0]
    assert integrate_power_kwh(series) == pytest.approx(2.0)


def test_duplicates_block_preparation_and_gaps_are_reported():
    duplicate = _series(((0.0, 1.0), (0.0, 2.0), (1.0, 3.0)))
    gapped = _series(((0.0, 1.0), (1.0, 2.0), (3.0, 3.0)), expected_step_hours=1.0)

    assert assess_series(duplicate).suitability is DataSuitability.NOT_READY
    assert prepare_series(duplicate).records == ()
    with pytest.raises(ValueError, match="nicht eindeutig"):
        integrate_power_kwh(duplicate)
    report = assess_series(gapped)
    assert report.suitability is DataSuitability.PARTIAL
    assert report.time_axis.gap_starts == (1.0,)
    prepared_gap = prepare_series(gapped)
    assert prepared_gap.records[1].value is None
    assert prepared_gap.records[1].coverage_hours == 0.0
    assert integrate_power_kwh(gapped) == pytest.approx(0.001)


def test_instantaneous_values_use_linear_energy_integration():
    series = _series(((0.0, 0.0), (2.0, 2000.0)), semantics=TimeSemantics.INSTANTANEOUS)

    assert integrate_power_kwh(series) == pytest.approx(2.0)
    assert [item.value for item in prepare_series(series).records] == [500.0, 1500.0]


def test_prepare_dataset_writes_csv_and_json_manifest_without_8760_limit(tmp_path):
    series = _series(((0.0, 1.0), (1.0, 2.0), (8762.0, 3.0)), expected_step_hours=1.0)

    result = prepare_dataset("case 1", (series,), tmp_path)

    manifest = json.loads((tmp_path / "case_1" / "preparation_manifest.json").read_text(encoding="utf-8"))
    assert len(result.package.series[0].records) == 8762
    assert result.package.series[0].records[1].value is None
    assert manifest["series"][0]["suitability"] == "partial"
    assert (tmp_path / "case_1" / "heating_power.csv").is_file()
