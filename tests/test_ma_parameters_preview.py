from ma_parameters import (
    build_business_integration_lod1_parameter_preview_rows,
    build_business_integration_lod1_parameter_snapshot,
    parameter_preview_table_rows,
    parameter_snapshot_value_rows,
)


def test_business_integration_lod1_parameter_preview_collects_input_chain():
    preview_rows = build_business_integration_lod1_parameter_preview_rows()
    table_rows = parameter_preview_table_rows(preview_rows)
    parameters = {row["Parameter"] for row in table_rows}
    modules = {row["Modul"] for row in table_rows}

    assert {"ma_building", "ma_zones", "ma_technical"} <= modules
    assert "building_validation_status" in parameters
    assert "zone_validation_status" in parameters
    assert "technical_validation_status" in parameters
    assert "window_area_ratio_percent" in parameters
    assert "zone_floor_area_m2" in parameters
    assert any(str(parameter).endswith(".estimated_design_power_w") for parameter in parameters)


def test_parameter_snapshot_keeps_preview_values_as_released_parameters():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    snapshot_rows = parameter_snapshot_value_rows(snapshot)
    parameters = {row["Parameter"] for row in snapshot_rows}

    assert "window_area_ratio_percent" in parameters
    assert "building_validation_status" not in parameters
    assert all(row["Status"] == "released" for row in snapshot_rows)
