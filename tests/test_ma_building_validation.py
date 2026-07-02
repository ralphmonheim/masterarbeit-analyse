from dataclasses import replace

from ma_building import (
    Opening,
    PhysicalElement,
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


def test_invalid_maturity_level_blocks_release():
    spec = load_demo_building_spec()
    invalid_version = replace(spec.model_version, current_maturity_level="BIL-X")
    invalid_spec = replace(spec, model_version=invalid_version)

    result = validate_building_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BUILDING_MATURITY_LEVEL_INVALID" in _codes(result)
