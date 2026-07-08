from dataclasses import replace

from ma_building import load_business_integration_lod1_building_spec
from ma_validation import ReleaseStatus
from ma_zones import (
    ZoneInputDetailLevel,
    load_business_integration_lod1_zone_spec,
    validate_zone_spec,
    zone_specification_to_dict,
)


def _codes(result):
    return {message.code for message in result.messages}


def test_business_integration_lod1_zone_spec_loads_and_is_released():
    building_spec = load_business_integration_lod1_building_spec()
    zone_spec = load_business_integration_lod1_zone_spec()

    result = validate_zone_spec(zone_spec, building_spec=building_spec)

    assert zone_spec.input_detail_level is ZoneInputDetailLevel.LOD_1
    assert zone_spec.zone_model_id == "ZONE-BI-LOD1-MODEL-0001"
    assert len(zone_spec.zones) == 1
    assert zone_spec.zones[0].floor_area_m2 == 24.0
    assert zone_spec.usage_profiles[0].operation_start_hour == 8.0
    assert result.release_status is ReleaseStatus.RELEASED
    assert result.messages == ()


def test_zone_specification_to_dict_is_slot_safe():
    zone_spec = load_business_integration_lod1_zone_spec()

    payload = zone_specification_to_dict(zone_spec)

    assert payload["zone_model_id"] == "ZONE-BI-LOD1-MODEL-0001"
    assert payload["zones"][0]["zone_id"] == "ZONE-BI-LOD1-0001"


def test_zone_with_unknown_usage_profile_blocks_release():
    zone_spec = load_business_integration_lod1_zone_spec()
    invalid_zone = replace(zone_spec.zones[0], usage_profile_id="USE-MISSING")
    invalid_spec = replace(zone_spec, zones=(invalid_zone,))

    result = validate_zone_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "ZONE_USAGE_PROFILE_UNKNOWN" in _codes(result)


def test_zone_with_invalid_operation_hours_blocks_release():
    zone_spec = load_business_integration_lod1_zone_spec()
    invalid_profile = replace(zone_spec.usage_profiles[0], operation_end_hour=7.0)
    invalid_spec = replace(zone_spec, usage_profiles=(invalid_profile,))

    result = validate_zone_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "ZONE_OPERATION_END_INVALID" in _codes(result)


def test_zone_building_reference_mismatch_blocks_release():
    building_spec = load_business_integration_lod1_building_spec()
    zone_spec = load_business_integration_lod1_zone_spec()
    invalid_spec = replace(zone_spec, building_id="BUILDING-MISSING")

    result = validate_zone_spec(invalid_spec, building_spec=building_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "ZONE_BUILDING_REFERENCE_MISMATCH" in _codes(result)


def test_lod1_multiple_zones_requires_confirmation():
    zone_spec = load_business_integration_lod1_zone_spec()
    second_zone = replace(zone_spec.zones[0], zone_id="ZONE-BI-LOD1-0002")
    warning_spec = replace(zone_spec, zones=(zone_spec.zones[0], second_zone))

    result = validate_zone_spec(warning_spec)

    assert result.release_status is ReleaseStatus.CONFIRMATION_REQUIRED
    assert "ZONE_LOD1_MULTIPLE_ZONES" in _codes(result)
