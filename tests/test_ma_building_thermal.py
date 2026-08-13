from dataclasses import replace

import pytest

from ma_building import (
    SimpleEnvelopeInput,
    build_thermal_component_rows,
    calculate_thermal_transmission,
    calculate_weighted_u_value,
    load_business_integration_lod1_building_spec,
    load_demo_building_spec,
    load_small_office_5z_endvariant_02_building_spec,
)


def _spec_with_u_values():
    demo = load_demo_building_spec()
    return replace(
        demo,
        simple_envelope=SimpleEnvelopeInput(
            external_wall_u_value_w_m2k=0.20,
            window_u_value_w_m2k=1.20,
            window_area_ratio_percent=25.0,
            roof_u_value_w_m2k=0.15,
            floor_u_value_w_m2k=0.30,
        ),
    )


def test_rows_apply_host_deduction_keep_positive_openings_and_inherit_orientation():
    rows = build_thermal_component_rows(_spec_with_u_values())
    rows_by_id = {row.component_id: row for row in rows}

    assert rows_by_id["WALL-0001"].effective_area_m2 == 35.4
    assert rows_by_id["WALL-0002"].effective_area_m2 == 23.5
    assert rows_by_id["OPENING-0001"].effective_area_m2 == 3.0
    assert rows_by_id["OPENING-0001"].orientation_deg == 0.0
    assert rows_by_id["OPENING-0002"].orientation_deg == 90.0
    assert "WALL-0003" not in rows_by_id
    assert "Demo-Annahme: TA verwendet den U-Wert von FA." in rows_by_id["OPENING-0002"].assumption_notes


def test_weighted_u_value_and_transmission_for_demo_spec():
    result = calculate_thermal_transmission(_spec_with_u_values())
    wall_rows = [row for row in result.rows if row.category == "Waende"]

    assert calculate_weighted_u_value(wall_rows) == pytest.approx(0.20)
    assert result.envelope_area_m2 == pytest.approx(256.0)
    assert result.heat_loss_coefficient_w_k == pytest.approx(72.3)
    assert result.heat_loss_coefficient_per_area_w_m2k == pytest.approx(72.3 / 256.0)


def test_missing_u_values_are_marked_and_excluded_from_final_specific_result():
    result = calculate_thermal_transmission(load_demo_building_spec())

    assert all(not row.is_complete for row in result.rows)
    assert result.envelope_area_m2 == pytest.approx(256.0)
    assert result.heat_loss_coefficient_w_k is None
    assert result.heat_loss_coefficient_per_area_w_m2k is None
    assert not result.is_complete
    assert any("Unvollstaendige" in warning for warning in result.warnings)


def test_host_area_never_becomes_negative_when_openings_are_larger():
    spec = _spec_with_u_values()
    oversized_opening = replace(spec.openings[0], area_m2=100.0)
    rows = build_thermal_component_rows(replace(spec, openings=(oversized_opening, *spec.openings[1:])))

    wall = next(row for row in rows if row.component_id == "WALL-0001")
    assert wall.effective_area_m2 == 0.0
    assert not wall.is_complete
    opening = next(row for row in rows if row.component_id == "OPENING-0001")
    assert opening.effective_area_m2 == 100.0
    assert not opening.is_complete
    assert (
        calculate_thermal_transmission(
            replace(spec, openings=(oversized_opening, *spec.openings[1:]))
        ).heat_loss_coefficient_w_k
        is None
    )


def test_lod1_aggregate_envelope_creates_complete_synthetic_rows_and_transmission():
    result = calculate_thermal_transmission(load_business_integration_lod1_building_spec())

    rows_by_id = {row.component_id: row for row in result.rows}
    assert rows_by_id["LOD1-AW"].effective_area_m2 == 60.0
    assert rows_by_id["LOD1-FA"].effective_area_m2 == 20.0
    assert "LoD-1-Aggregatflaeche" in rows_by_id["LOD1-AW"].assumption_notes[0]
    assert result.envelope_area_m2 == pytest.approx(128.0)
    assert result.heat_loss_coefficient_w_k == pytest.approx(61.6)
    assert result.heat_loss_coefficient_per_area_w_m2k == pytest.approx(0.48125)
    assert result.is_complete


def test_lod1_derives_window_area_from_the_ratio_when_no_explicit_window_area_exists():
    spec = load_business_integration_lod1_building_spec()
    aggregate_only = replace(spec, simple_envelope=replace(spec.simple_envelope, window_area_m2=None))

    result = calculate_thermal_transmission(aggregate_only)
    rows_by_id = {row.component_id: row for row in result.rows}

    assert rows_by_id["LOD1-AW"].effective_area_m2 == pytest.approx(60.0)
    assert rows_by_id["LOD1-FA"].effective_area_m2 == pytest.approx(20.0)
    assert result.heat_loss_coefficient_w_k == pytest.approx(61.6)
    assert result.is_complete


def test_lod1_inconsistent_window_area_and_ratio_block_the_transmission_result():
    spec = load_business_integration_lod1_building_spec()
    inconsistent = replace(spec, simple_envelope=replace(spec.simple_envelope, window_area_m2=10.0))

    result = calculate_thermal_transmission(inconsistent)

    assert result.heat_loss_coefficient_w_k is None
    assert result.heat_loss_coefficient_per_area_w_m2k is None
    assert not result.is_complete
    assert any("BUILDING_LOD1_WINDOW_AREA_RATIO_INCONSISTENT" in warning for warning in result.warnings)


def test_invalid_or_non_finite_u_values_block_the_transmission_result():
    spec = load_business_integration_lod1_building_spec()
    invalid = replace(spec, simple_envelope=replace(spec.simple_envelope, external_wall_u_value_w_m2k=-0.24))
    non_finite = replace(spec, simple_envelope=replace(spec.simple_envelope, external_wall_u_value_w_m2k=float("nan")))

    for invalid_spec in (invalid, non_finite):
        result = calculate_thermal_transmission(invalid_spec)

        assert result.heat_loss_coefficient_w_k is None
        assert result.heat_loss_coefficient_per_area_w_m2k is None
        assert not result.is_complete
        assert all(not row.is_complete for row in result.rows)
        assert any("BUILDING_SIMPLE_ENVELOPE_U_VALUE_INVALID" in warning for warning in result.warnings)


def test_partial_explicit_envelope_is_not_reported_as_a_complete_building_hull():
    spec = _spec_with_u_values()
    partial = replace(spec, elements=(spec.elements[0],), openings=())

    result = calculate_thermal_transmission(partial)

    assert result.heat_loss_coefficient_w_k is None
    assert not result.is_complete
    assert any("Explizite Huelle ist unvollstaendig" in warning for warning in result.warnings)


def test_explicit_envelope_requires_a_confirmed_completeness_statement():
    spec = _spec_with_u_values()

    result = calculate_thermal_transmission(replace(spec, thermal_envelope_complete=False))

    assert result.heat_loss_coefficient_w_k is None
    assert not result.is_complete
    assert any("Vollstaendigkeitsnachweis" in warning for warning in result.warnings)


def test_explicit_envelope_must_match_confirmed_aggregate_areas_when_available():
    spec = load_small_office_5z_endvariant_02_building_spec()
    incomplete = replace(
        spec,
        elements=tuple(replace(element, area_m2=1.0) for element in spec.elements if element.construction_code != "GD"),
        openings=(),
    )

    result = calculate_thermal_transmission(incomplete)

    assert result.heat_loss_coefficient_w_k is None
    assert not result.is_complete
    assert any("bestaetigten Aggregatflaeche" in warning for warning in result.warnings)


def test_explicit_envelope_aggregate_coverage_uses_the_confirmed_tolerance():
    spec = load_small_office_5z_endvariant_02_building_spec()
    within_tolerance = replace(
        spec,
        elements=tuple(
            replace(element, area_m2=element.area_m2 + 0.05) if element.construction_code == "DA" else element
            for element in spec.elements
        ),
    )
    outside_tolerance = replace(
        spec,
        elements=tuple(
            replace(element, area_m2=element.area_m2 + 2.5) if element.construction_code == "DA" else element
            for element in spec.elements
        ),
    )

    assert calculate_thermal_transmission(within_tolerance).is_complete
    assert not calculate_thermal_transmission(outside_tolerance).is_complete


def test_small_office_openings_redistribute_the_gross_facade_without_double_counting():
    spec = load_small_office_5z_endvariant_02_building_spec()

    result = calculate_thermal_transmission(spec)
    rows_by_id = {row.component_id: row for row in result.rows}

    assert rows_by_id["ELEMENT-SYNTH-EXTERNAL-WALLS"].effective_area_m2 == pytest.approx(
        748.033605 - 206.612894 - 28.255
    )
    assert result.envelope_area_m2 == pytest.approx(748.033605 + 358.917805 + 243.2645)
