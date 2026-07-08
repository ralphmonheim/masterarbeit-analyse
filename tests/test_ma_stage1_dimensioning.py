from dataclasses import replace

from ma_analyse.stage_1_dimensioning import (
    DimensioningStatus,
    dimensioning_message_rows,
    dimensioning_step_rows,
    dimensioning_summary_rows,
    run_business_integration_lod1_reference_dimensioning,
    run_lod1_reference_dimensioning,
)
from ma_parameters import build_business_integration_lod1_parameter_snapshot


def _codes(result):
    return {message.code for message in result.messages}


def test_business_integration_lod1_reference_dimensioning_is_evaluable():
    result = run_business_integration_lod1_reference_dimensioning()
    summary = {row["Kennwert"]: row["Wert"] for row in dimensioning_summary_rows(result)}
    steps = {row["Schritt"]: row["Wert"] for row in dimensioning_step_rows(result)}

    assert result.status is DimensioningStatus.EVALUATED
    assert result.heating_transmission_load_w == 1212.0
    assert result.heating_ventilation_load_w == 489.6
    assert result.heating_total_load_w == 1701.6
    assert result.cooling_internal_load_w == 582.0
    assert result.ventilation_volume_flow_m3_h == 48.0
    assert summary["Status"] == "evaluated"
    assert steps["heating_total_load_w"] == 1701.6
    assert "DIMENSIONING_LOD1_METHOD_LIMITED" in _codes(result)


def test_dimensioning_missing_snapshot_parameter_is_not_evaluable():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    values = tuple(value for value in snapshot.values if value.parameter_key != "building_height_m")
    invalid_snapshot = replace(snapshot, values=values)

    result = run_lod1_reference_dimensioning(invalid_snapshot)

    assert result.status is DimensioningStatus.NOT_EVALUABLE
    assert result.steps == ()
    assert result.heating_total_load_w is None
    assert "DIMENSIONING_PARAMETER_MISSING" in _codes(result)


def test_dimensioning_reports_heating_capacity_warning_for_lod1_demo():
    result = run_business_integration_lod1_reference_dimensioning()
    message_rows = dimensioning_message_rows(result)

    assert any(row["Code"] == "DIMENSIONING_HEATING_TECH_POWER_LOW" for row in message_rows)
