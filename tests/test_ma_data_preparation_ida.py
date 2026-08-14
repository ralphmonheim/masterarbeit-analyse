from pathlib import Path

import pytest

from ma_data_preparation.ida_ice import (
    IdaSeriesSelection,
    discover_known_ida_prn,
    prepare_known_ida_results,
    project_ida_records_for_display,
    read_prn_as_standardized_series,
)


def _write_prn(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# time order relhum q_heat\n0 1 0.40 1000\n0.5 1 0.50 2000\n1 1 0.60 0\n",
        encoding="utf-8",
    )


def test_prn_bridge_preserves_variable_time_and_normalizes_relative_humidity(tmp_path):
    source = tmp_path / "EG Ost.IAQ.prn"
    _write_prn(source)
    selection = IdaSeriesSelection("5Z", "model", "run", "variant", "EG Ost", "energy", source)

    series = read_prn_as_standardized_series(selection)

    relhum = next(item for item in series if item.metric == "iaq.relhum")
    heat = next(item for item in series if item.metric == "iaq.q_heat")
    assert [record.time_hours for record in relhum.records] == [0.0, 0.5, 1.0]
    assert [record.value for record in relhum.records] == [40.0, 50.0, 60.0]
    assert relhum.unit == "%"
    assert heat.unit == "W"


def test_known_discovery_ignores_idm_and_unknown_directories(tmp_path):
    known = tmp_path / "Masterthesis_Dimensionierung_5Z" / "energy" / "EG Ost.IAQ.prn"
    _write_prn(known)
    known.with_suffix(".idm").write_text("must not be read", encoding="utf-8")
    _write_prn(tmp_path / "unknown" / "room.IAQ.prn")

    selections = discover_known_ida_prn(tmp_path)

    assert [item.path for item in selections] == [known]
    assert selections[0].cohort == "5Z"


def test_prn_without_time_is_rejected(tmp_path):
    source = tmp_path / "bad.prn"
    source.write_text("# order value\n1 2\n", encoding="utf-8")
    selection = IdaSeriesSelection("5Z", "model", "run", "variant", None, "energy", source)

    with pytest.raises(ValueError, match="time-Spalte"):
        read_prn_as_standardized_series(selection)


def test_repeated_ida_support_points_remain_blocking_in_the_standard_contract(tmp_path):
    source = tmp_path / "repeat.TEMPERATURES.prn"
    source.write_text(
        "# time order top\n0 1 20\n0.5000000000 1 21\n0.5000000001 1 23\n1 1 22\n",
        encoding="utf-8",
    )
    selection = IdaSeriesSelection("29Z", "model", "run", "variant", "zone", "energy", source)

    series = read_prn_as_standardized_series(selection)[0]

    assert [record.time_hours for record in series.records] == [0.0, 0.5, 0.5000000001, 1.0]
    assert not series.normalization_notes
    display, notes = project_ida_records_for_display(series.records)
    assert [record.value for record in display] == [20.0, 23.0, 22.0]
    assert notes


def test_prepare_can_resume_an_explicitly_interrupted_local_run(tmp_path):
    source = tmp_path / "Masterthesis_Dimensionierung_5Z" / "energy" / "EG Ost.IAQ.prn"
    _write_prn(source)
    output = tmp_path / "database"

    first = prepare_known_ida_results(tmp_path, output, cohorts=("5Z",))
    resumed = prepare_known_ida_results(tmp_path, output, cohorts=("5Z",), resume_existing=True)

    assert len(first) == 1
    assert resumed == {}

    source.write_text(source.read_text(encoding="utf-8") + "2 1 0.70 500\n", encoding="utf-8")
    refreshed = prepare_known_ida_results(tmp_path, output, cohorts=("5Z",), resume_existing=True)
    assert len(refreshed) == 1
