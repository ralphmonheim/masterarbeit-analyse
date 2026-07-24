from dataclasses import replace

from ma_building import load_small_office_lod1_building_spec, validate_building_spec
from ma_parameters import (
    build_lod1_parameter_snapshot,
    build_small_office_lod1_parameter_snapshot,
    validate_parameter_snapshot,
)
from ma_technical import load_small_office_lod1_technical_spec, validate_technical_spec
from ma_validation import ReleaseStatus
from ma_zones import load_small_office_lod1_zone_spec, validate_zone_spec


def test_synthetic_small_office_lod1_chain_is_released_and_linked():
    building_spec = load_small_office_lod1_building_spec()
    zone_spec = load_small_office_lod1_zone_spec()
    technical_spec = load_small_office_lod1_technical_spec()
    snapshot = build_small_office_lod1_parameter_snapshot()

    assert validate_building_spec(building_spec).release_status is ReleaseStatus.RELEASED
    assert validate_zone_spec(zone_spec, building_spec=building_spec).release_status is ReleaseStatus.RELEASED
    assert validate_technical_spec(technical_spec, zone_spec=zone_spec).release_status is ReleaseStatus.RELEASED
    snapshot_validation = validate_parameter_snapshot(snapshot)
    assert snapshot_validation.release_status is ReleaseStatus.RELEASED
    assert building_spec.project.project_id == "PROJECT-SYNTHETIC-SMALL-OFFICE"
    assert building_spec.building.building_id == zone_spec.building_id == technical_spec.building_id
    assert zone_spec.source_building_version_id == building_spec.model_version.version_id
    assert technical_spec.source_zone_model_id == zone_spec.zone_model_id
    assert building_spec.simple_envelope is not None
    assert building_spec.simple_envelope.external_wall_area_m2 == 270.0
    assert building_spec.simple_envelope.window_area_m2 == 67.5
    assert zone_spec.zones[0].floor_area_m2 == 500.0
    assert zone_spec.zones[0].minimum_air_change_rate_1_h == 1.0
    assert {system.system_type for system in technical_spec.systems} == {"heating", "cooling", "ventilation"}
    assert {value.status for value in snapshot.values} == {"provisional_assumption"}
    assert all("BusinessIntegration" not in source.label for source in snapshot.source_references)


def test_synthetic_small_office_assumptions_are_marked_and_traceable():
    building_spec = load_small_office_lod1_building_spec()
    zone_spec = load_small_office_lod1_zone_spec()
    technical_spec = load_small_office_lod1_technical_spec()

    assumption_text = " ".join(
        assumption.text for assumption in (*building_spec.assumptions, *zone_spec.assumptions, *technical_spec.assumptions)
    )

    assert "Strikt synthetischer" in assumption_text
    assert "vorlaeufig" in assumption_text
    assert "GEG Anlage 2" in assumption_text
    assert "ASR A3.5" in assumption_text
    assert "ASR A3.6" in assumption_text


def test_source_hash_changes_when_spec_content_changes_without_version_change():
    building_spec = load_small_office_lod1_building_spec()
    zone_spec = load_small_office_lod1_zone_spec()
    technical_spec = load_small_office_lod1_technical_spec()
    original_snapshot = build_lod1_parameter_snapshot(
        building_spec,
        zone_spec,
        technical_spec,
        snapshot_id="PARAM-SMALL-OFFICE-HASH-TEST",
        snapshot_version="PARAM-SMALL-OFFICE-HASH-TEST-V1",
    )
    changed_building = replace(
        building_spec,
        building=replace(building_spec.building, name="Geaenderter synthetischer Name"),
    )
    changed_snapshot = build_lod1_parameter_snapshot(
        changed_building,
        zone_spec,
        technical_spec,
        snapshot_id="PARAM-SMALL-OFFICE-HASH-TEST",
        snapshot_version="PARAM-SMALL-OFFICE-HASH-TEST-V1",
    )

    original_hash = next(
        source.content_hash
        for source in original_snapshot.source_references
        if source.module_key == "ma_building"
    )
    changed_hash = next(
        source.content_hash
        for source in changed_snapshot.source_references
        if source.module_key == "ma_building"
    )

    assert original_hash != changed_hash
