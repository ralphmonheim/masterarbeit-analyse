from dataclasses import replace

from ma_building import load_business_integration_lod1_building_spec
from ma_core import utc_now
from ma_technical import TechnicalModelRevision
from ma_validation import ReleaseStatus
from ma_zones import (
    build_thermal_building_model,
    load_business_integration_lod1_zone_spec,
    validate_thermal_building_model,
)


def _technical_revision() -> TechnicalModelRevision:
    return TechnicalModelRevision(
        technical_model_id="TECH-BI-LOD1-0001",
        revision_id="TECH-BI-LOD1-REV-0001",
        content_hash="a" * 64,
        release_status=ReleaseStatus.RELEASED,
        specification_payload={"schema_version": "2.0"},
        released_at=utc_now(),
    )


def test_one_room_one_zone_thermal_building_model_is_released():
    building_spec = load_business_integration_lod1_building_spec()
    zone_spec = load_business_integration_lod1_zone_spec()
    model = build_thermal_building_model(
        building_spec,
        zone_spec,
        _technical_revision(),
        thermal_building_model_id="THERMAL-BI-LOD1-0001",
    )

    result = validate_thermal_building_model(model, building_spec=building_spec, zone_spec=zone_spec)

    assert model.room_zone_assignments == (("SPACE-BI-OFFICE-0001", "ZONE-BI-LOD1-0001"),)
    assert result.release_status is ReleaseStatus.RELEASED


def test_thermal_building_model_blocks_unassigned_room():
    building_spec = load_business_integration_lod1_building_spec()
    zone_spec = load_business_integration_lod1_zone_spec()
    model = build_thermal_building_model(
        building_spec,
        zone_spec,
        _technical_revision(),
        thermal_building_model_id="THERMAL-BI-LOD1-0001",
    )

    result = validate_thermal_building_model(
        replace(model, room_zone_assignments=()),
        building_spec=building_spec,
        zone_spec=zone_spec,
    )

    assert result.release_status is ReleaseStatus.BLOCKED
    assert {message.code for message in result.messages} == {"THERMAL_BUILDING_ROOM_UNASSIGNED"}
