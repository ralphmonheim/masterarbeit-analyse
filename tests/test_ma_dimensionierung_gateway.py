from dataclasses import replace

from ma_dimensionierung import (
    LOD1_REFERENCE_METHOD_ID,
    LOD1_REFERENCE_METHOD_VERSION,
    LOD1_RESULT_ROUNDING_RULE,
    execute_lod1_reference_dimensioning,
    prepare_lod1_reference_dimensioning_request,
    run_lod1_reference_dimensioning,
)
from ma_parameters import build_business_integration_lod1_parameter_snapshot


def test_gateway_prepares_validated_lod1_request_and_preserves_legacy_result():
    snapshot = build_business_integration_lod1_parameter_snapshot()

    preparation = prepare_lod1_reference_dimensioning_request(snapshot)

    assert not preparation.validation.errors
    assert preparation.request is not None
    assert preparation.request.method_id == LOD1_REFERENCE_METHOD_ID
    assert preparation.request.method_version == LOD1_REFERENCE_METHOD_VERSION
    assert preparation.request.rounding_rule == LOD1_RESULT_ROUNDING_RULE
    assert len(preparation.request.input_fingerprint) == 64

    execution = execute_lod1_reference_dimensioning(preparation.request)
    legacy = run_lod1_reference_dimensioning(snapshot)

    assert execution.result.heating_total_load_w == legacy.heating_total_load_w
    assert execution.result.cooling_internal_load_w == legacy.cooling_internal_load_w
    assert execution.result.ventilation_volume_flow_m3_h == legacy.ventilation_volume_flow_m3_h
    assert len(execution.result_fingerprint) == 64


def test_gateway_blocks_wrong_global_or_zone_unit_before_calculation():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    changed_values = tuple(
        replace(value, unit="kW") if value.parameter_key == "building_length_m" else value
        for value in snapshot.values
    )
    wrong_global_unit = prepare_lod1_reference_dimensioning_request(replace(snapshot, values=changed_values))

    changed_values = tuple(
        replace(value, unit="K") if value.parameter_key.endswith(".heating_setpoint_c") else value
        for value in snapshot.values
    )
    wrong_zone_unit = prepare_lod1_reference_dimensioning_request(replace(snapshot, values=changed_values))

    assert wrong_global_unit.request is None
    assert wrong_zone_unit.request is None
    assert {message.code for message in wrong_global_unit.validation.errors} == {"DIMENSIONING_INPUT_UNIT_INVALID"}
    assert {message.code for message in wrong_zone_unit.validation.errors} == {"DIMENSIONING_INPUT_UNIT_INVALID"}


def test_gateway_input_fingerprint_is_order_independent_and_binds_inputs_and_assumptions():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    original = prepare_lod1_reference_dimensioning_request(snapshot).request
    reordered = prepare_lod1_reference_dimensioning_request(replace(snapshot, values=tuple(reversed(snapshot.values)))).request
    changed_assumption = prepare_lod1_reference_dimensioning_request(snapshot, person_sensible_gain_w=80.0).request
    changed_value = prepare_lod1_reference_dimensioning_request(
        replace(
            snapshot,
            values=tuple(
                replace(value, value=11.0) if value.parameter_key == "building_length_m" else value
                for value in snapshot.values
            ),
        )
    ).request

    assert original is not None
    assert reordered is not None
    assert changed_assumption is not None
    assert changed_value is not None
    assert original.input_fingerprint == reordered.input_fingerprint
    assert original.input_fingerprint != changed_assumption.input_fingerprint
    assert original.input_fingerprint != changed_value.input_fingerprint


def test_gateway_result_fingerprint_ignores_legacy_diagnostic_ids_and_timestamps():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    preparation = prepare_lod1_reference_dimensioning_request(snapshot)

    assert preparation.request is not None
    first = execute_lod1_reference_dimensioning(preparation.request)
    second = execute_lod1_reference_dimensioning(preparation.request)

    assert first.result.messages != second.result.messages
    assert first.result_fingerprint == second.result_fingerprint


def test_gateway_rejects_a_manipulated_prepared_request():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    preparation = prepare_lod1_reference_dimensioning_request(snapshot)

    assert preparation.request is not None
    manipulated = replace(preparation.request, input_fingerprint="0" * 64)

    try:
        execute_lod1_reference_dimensioning(manipulated)
    except ValueError as error:
        assert "nicht mehr gueltig" in str(error)
    else:
        raise AssertionError("Manipulierte Auftraege muessen blockiert werden.")
