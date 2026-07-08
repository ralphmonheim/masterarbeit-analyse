from dataclasses import replace

from ma_technical import (
    TechnicalInputDetailLevel,
    load_business_integration_lod1_technical_spec,
    validate_technical_spec,
)
from ma_validation import ReleaseStatus
from ma_zones import load_business_integration_lod1_zone_spec


def _codes(result):
    return {message.code for message in result.messages}


def test_business_integration_lod1_technical_spec_loads_and_is_released():
    zone_spec = load_business_integration_lod1_zone_spec()
    technical_spec = load_business_integration_lod1_technical_spec()

    result = validate_technical_spec(technical_spec, zone_spec=zone_spec)

    assert technical_spec.input_detail_level is TechnicalInputDetailLevel.LOD_1
    assert technical_spec.technical_model_id == "TECH-BI-LOD1-MODEL-0001"
    assert {system.system_type for system in technical_spec.systems} == {"heating", "cooling", "ventilation"}
    assert result.release_status is ReleaseStatus.RELEASED
    assert result.messages == ()


def test_technical_system_with_unknown_zone_blocks_release():
    zone_spec = load_business_integration_lod1_zone_spec()
    technical_spec = load_business_integration_lod1_technical_spec()
    invalid_system = replace(technical_spec.systems[0], served_zone_ids=("ZONE-MISSING",))
    invalid_spec = replace(technical_spec, systems=(invalid_system, *technical_spec.systems[1:]))

    result = validate_technical_spec(invalid_spec, zone_spec=zone_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "TECHNICAL_SERVED_ZONE_UNKNOWN" in _codes(result)


def test_technical_system_with_invalid_type_blocks_release():
    technical_spec = load_business_integration_lod1_technical_spec()
    invalid_system = replace(technical_spec.systems[0], system_type="unknown")
    invalid_spec = replace(technical_spec, systems=(invalid_system, *technical_spec.systems[1:]))

    result = validate_technical_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "TECHNICAL_SYSTEM_TYPE_INVALID" in _codes(result)


def test_missing_ventilation_system_blocks_release():
    technical_spec = load_business_integration_lod1_technical_spec()
    without_ventilation = tuple(system for system in technical_spec.systems if system.system_type != "ventilation")
    invalid_spec = replace(technical_spec, systems=without_ventilation)

    result = validate_technical_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "TECHNICAL_VENTILATION_SYSTEM_MISSING" in _codes(result)


def test_missing_control_strategy_requires_confirmation():
    technical_spec = load_business_integration_lod1_technical_spec()
    warning_system = replace(technical_spec.systems[0], control_strategy="")
    warning_spec = replace(technical_spec, systems=(warning_system, *technical_spec.systems[1:]))

    result = validate_technical_spec(warning_spec)

    assert result.release_status is ReleaseStatus.CONFIRMATION_REQUIRED
    assert "TECHNICAL_CONTROL_STRATEGY_MISSING" in _codes(result)
