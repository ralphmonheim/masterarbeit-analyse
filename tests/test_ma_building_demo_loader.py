from ma_building import load_demo_building_spec, validate_building_spec
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
