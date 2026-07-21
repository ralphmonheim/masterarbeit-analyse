from ma_parameters import (
    build_business_integration_lod1_baseline_parameter_snapshot,
    load_reference_variation_specification,
    variation_area_rows,
    variation_dimension_rows,
)


def test_thesis_reference_locks_all_areas_except_zones():
    baseline = build_business_integration_lod1_baseline_parameter_snapshot()

    specification = load_reference_variation_specification(baseline)

    assert {area.module_key for area in specification.areas if area.is_locked} == {
        "weather",
        "building",
        "technical",
    }
    assert [dimension.module_key for dimension in specification.unlocked_dimensions] == ["zones"]
    assert variation_area_rows(specification)[0]["Werte dieses Bereichs fuer Varianten sperren"] is True


def test_reference_variation_keeps_heating_and_cooling_setpoints_coupled():
    baseline = build_business_integration_lod1_baseline_parameter_snapshot()

    specification = load_reference_variation_specification(baseline)
    dimension = specification.unlocked_dimensions[0]
    rows = variation_dimension_rows(specification)

    assert dimension.value_mode == "coupled_option"
    assert dimension.target_parameter_keys == (
        "ZONE-BI-LOD1-0001.heating_setpoint_c",
        "ZONE-BI-LOD1-0001.cooling_setpoint_c",
    )
    assert "95 Prozent" in rows[0]["Moegliche Werte"]
