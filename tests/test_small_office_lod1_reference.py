from pathlib import Path

from ma_building import load_building_spec, validate_building_spec
from ma_technical import load_technical_spec, validate_technical_spec
from ma_validation import ReleaseStatus
from ma_zones import load_zone_spec, validate_zone_spec


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BUILDING_PATH = PROJECT_ROOT / "config" / "ma_building" / "examples" / "small_office_lod1_building_spec.yaml"
ZONE_PATH = PROJECT_ROOT / "config" / "ma_zones" / "examples" / "small_office_lod1_zone_spec.yaml"
TECHNICAL_PATH = PROJECT_ROOT / "config" / "ma_technical" / "examples" / "small_office_lod1_technical_spec.yaml"


def test_small_office_lod1_reference_chain_is_loadable_and_released():
    building_spec = load_building_spec(BUILDING_PATH)
    zone_spec = load_zone_spec(ZONE_PATH)
    technical_spec = load_technical_spec(TECHNICAL_PATH)

    building_result = validate_building_spec(building_spec)
    zone_result = validate_zone_spec(zone_spec, building_spec=building_spec)
    technical_result = validate_technical_spec(technical_spec, zone_spec=zone_spec)

    assert building_result.release_status is ReleaseStatus.RELEASED
    assert zone_result.release_status is ReleaseStatus.RELEASED
    assert technical_result.release_status is ReleaseStatus.RELEASED
    assert building_spec.spaces[0].floor_area_m2 == 516.842
    assert zone_spec.zones[0].source_space_ids == ("SPACE-SMALLOFFICE-AGGREGATED",)
    assert {system.system_type for system in technical_spec.systems} == {
        "heating",
        "cooling",
        "ventilation",
    }


def test_small_office_assumptions_keep_sources_and_validation_limits_visible():
    building_spec = load_building_spec(BUILDING_PATH)
    zone_spec = load_zone_spec(ZONE_PATH)
    technical_spec = load_technical_spec(TECHNICAL_PATH)

    assumption_text = " ".join(
        assumption.text
        for assumption in (
            *building_spec.assumptions,
            *zone_spec.assumptions,
            *technical_spec.assumptions,
        )
    )

    assert "GEG" in assumption_text
    assert "ASR" in assumption_text
    assert "validier" in assumption_text.lower()
