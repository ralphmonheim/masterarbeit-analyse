from dataclasses import replace

from ma_building import (
    Opening,
    PhysicalElement,
    SimpleEnvelopeInput,
    load_business_integration_lod1_building_spec,
    load_demo_building_spec,
    validate_building_spec,
)
from ma_validation import ReleaseStatus


def _codes(result):
    return {message.code for message in result.messages}


def test_duplicate_object_ids_block_release():
    spec = load_demo_building_spec()
    duplicate_space = replace(spec.spaces[1], space_id=spec.spaces[0].space_id)
    invalid_spec = replace(spec, spaces=(spec.spaces[0], duplicate_space))

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_OBJECT_ID_DUPLICATE" in _codes(result)


def test_space_with_unknown_storey_blocks_release():
    spec = load_demo_building_spec()
    invalid_space = replace(spec.spaces[0], storey_id="STOREY-MISSING")
    invalid_spec = replace(spec, spaces=(invalid_space, *spec.spaces[1:]))

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_SPACE_STOREY_UNKNOWN" in _codes(result)


def test_opening_with_unknown_host_blocks_release():
    spec = load_demo_building_spec()
    invalid_opening = replace(spec.openings[0], host_element_id="WALL-MISSING")
    invalid_spec = replace(spec, openings=(invalid_opening, *spec.openings[1:]))

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_OPENING_HOST_UNKNOWN" in _codes(result)


def test_invalid_construction_codes_block_release():
    spec = load_demo_building_spec()
    invalid_element = PhysicalElement(
        element_id="WALL-9999",
        element_type="external_wall",
        construction_code="BAD",
        storey_id=spec.storeys[0].storey_id,
        area_m2=12,
    )
    invalid_opening = Opening(
        opening_id="OPENING-9999",
        opening_type="window",
        host_element_id=spec.elements[0].element_id,
        construction_code="BAD",
        area_m2=1,
    )
    invalid_spec = replace(spec, elements=(*spec.elements, invalid_element), openings=(*spec.openings, invalid_opening))

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert {"BUILDING_CONSTRUCTION_CODE_INVALID", "BUILDING_OPENING_CODE_INVALID"} <= _codes(result)


def test_unknown_adjacent_space_blocks_release():
    spec = load_demo_building_spec()
    invalid_element = replace(spec.elements[0], adjacent_space_ids=("SPACE-MISSING",))
    invalid_spec = replace(spec, elements=(invalid_element, *spec.elements[1:]))

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_ELEMENT_SPACE_UNKNOWN" in _codes(result)


def test_empty_space_list_blocks_release():
    spec = load_demo_building_spec()
    invalid_spec = replace(spec, spaces=())

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_SPACES_MISSING" in _codes(result)


def test_lod1_allows_empty_space_element_and_opening_lists():
    spec = load_business_integration_lod1_building_spec()

    result = validate_building_spec(spec)

    assert spec.spaces == ()
    assert spec.elements == ()
    assert spec.openings == ()
    assert result.release_status is ReleaseStatus.RELEASED
    assert result.messages == ()


def test_lod1_missing_simple_envelope_blocks_release():
    spec = load_business_integration_lod1_building_spec()
    invalid_spec = replace(spec, simple_envelope=None)

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_SIMPLE_ENVELOPE_MISSING" in _codes(result)


def test_lod1_invalid_u_value_blocks_release():
    spec = load_business_integration_lod1_building_spec()
    invalid_envelope = replace(spec.simple_envelope, external_wall_u_value_w_m2k=0.0)
    invalid_spec = replace(spec, simple_envelope=invalid_envelope)

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_SIMPLE_ENVELOPE_U_VALUE_INVALID" in _codes(result)


def test_lod1_invalid_window_area_ratio_blocks_release():
    spec = load_business_integration_lod1_building_spec()
    invalid_envelope = replace(spec.simple_envelope, window_area_ratio_percent=120.0)
    invalid_spec = replace(spec, simple_envelope=invalid_envelope)

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_WINDOW_AREA_RATIO_INVALID" in _codes(result)


def test_lod1_invalid_optional_area_blocks_release():
    spec = load_business_integration_lod1_building_spec()
    invalid_envelope = SimpleEnvelopeInput(
        external_wall_u_value_w_m2k=0.24,
        window_u_value_w_m2k=1.3,
        window_area_ratio_percent=25.0,
        roof_area_m2=-1.0,
    )
    invalid_spec = replace(spec, simple_envelope=invalid_envelope)

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_SIMPLE_ENVELOPE_AREA_INVALID" in _codes(result)


def test_invalid_maturity_level_blocks_release():
    spec = load_demo_building_spec()
    invalid_version = replace(spec.model_version, current_maturity_level="BIL-X")
    invalid_spec = replace(spec, model_version=invalid_version)

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_MATURITY_LEVEL_INVALID" in _codes(result)
