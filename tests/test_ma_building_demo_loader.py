from ma_building import (
    BUILDING_SPECIFICATION_OPTIONS,
    BuildingInputDetailLevel,
    load_business_integration_lod1_building_spec,
    load_demo_building_spec,
    load_named_building_specification,
    validate_building_spec,
)
from ma_validation import ReleaseStatus


def test_named_building_specifications_are_loadable_by_stable_selection_key():
    loaded_ids = {
        key: load_named_building_specification(key).building.building_id
        for key, _label, _source in BUILDING_SPECIFICATION_OPTIONS
    }

    assert loaded_ids["business_integration_lod1"] == "BUILDING-BI-LOD1-0001"
    assert loaded_ids["small_office_5z_endvariant_02"] == "BUILDING-SMALL-OFFICE-5Z-ENDVAR-02"


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
    assert spec.model_version.version_id == "BUILDING-BI-LOD1-V2"
    assert len(spec.storeys) == 1
    assert len(spec.spaces) == 1
    assert spec.spaces[0].space_id == "SPACE-BI-OFFICE-0001"
    assert spec.spaces[0].floor_area_m2 == 24.0
    assert spec.spaces[0].volume_m3 == 96.0
    assert len(spec.openings) == 0
    assert result.release_status is ReleaseStatus.RELEASED
    assert result.messages == ()
