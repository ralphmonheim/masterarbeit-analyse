from ma_building import (
    BuildingInputDetailLevel,
    load_business_integration_lod1_building_spec,
    load_demo_building_spec,
    validate_building_spec,
)
from ma_validation import ReleaseStatus


def test_demo_building_spec_loads_and_is_released():
    spec = load_demo_building_spec()

    result = validate_building_spec(spec)

    assert spec.schema_version == "1.0"
    assert spec.building.building_id == "BUILDING-DEMO-0001"
    assert len(spec.storeys) == 1
    assert len(spec.spaces) == 2
    assert result.release_status is ReleaseStatus.RELEASED
    assert result.messages == ()


def test_business_integration_lod1_building_spec_loads_and_is_released():
    spec = load_business_integration_lod1_building_spec()

    result = validate_building_spec(spec)

    assert spec.input_detail_level is BuildingInputDetailLevel.LOD_1
    assert spec.building.building_id == "BUILDING-BI-LOD1-0001"
    assert spec.simple_envelope is not None
    assert spec.simple_envelope.window_area_ratio_percent == 25.0
    assert len(spec.spaces) == 0
    assert len(spec.openings) == 0
    assert result.release_status is ReleaseStatus.RELEASED
    assert result.messages == ()
