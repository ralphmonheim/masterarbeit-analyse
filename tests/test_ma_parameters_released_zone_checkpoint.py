from dataclasses import replace

import pytest

from ma_building import (
    BuildingInfo,
    BuildingInputDetailLevel,
    BuildingMaturityLevel,
    BuildingModelSpecification,
    BuildingModelVersion,
    PhysicalElement,
    ProjectInfo,
    SimpleEnvelopeInput,
    Space,
    Storey,
)
from ma_parameters import (
    FreshnessStatus,
    ParameterInputPackage,
    ParameterSourceReference,
    ParameterValue,
    attach_released_checkpoints_to_parameter_input_package,
    build_baseline_parameter_snapshot_from_input_package,
    parameter_checkpoint_reference_from_released_technical_handover,
    parameter_checkpoint_reference_from_released_zone_handover,
    validate_baseline_parameter_snapshot,
    validate_parameter_input_package,
)
from ma_technical import ReleasedTechnicalHandover
from ma_validation import ReleaseStatus
from ma_zones import (
    ThermalBuildingModel,
    ThermalZone,
    UsageProfile,
    ZoneInputDetailLevel,
    ZoneModelSpecification,
    build_released_zone_handover,
)


def _building_specification() -> BuildingModelSpecification:
    return BuildingModelSpecification(
        schema_version="1.0",
        project=ProjectInfo(project_id="PROJECT-TEST-0001", name="Synthetisches Projekt"),
        building=BuildingInfo(
            building_id="BUILDING-TEST-0001",
            name="Synthetisches Gebaeude",
            unit="m",
            north_angle_deg=0.0,
            length_m=10.0,
            width_m=10.0,
            height_m=3.0,
        ),
        model_version=BuildingModelVersion(
            version_id="BUILDING-REV-0001",
            source_input_level=BuildingMaturityLevel.BIL_1,
            detected_input_level=BuildingMaturityLevel.BIL_1,
            confirmed_input_level=BuildingMaturityLevel.BIL_1,
            current_maturity_level=BuildingMaturityLevel.BIL_1,
            target_maturity_level=BuildingMaturityLevel.BIL_1,
        ),
        storeys=(Storey(storey_id="STOREY-TEST-0001", name="EG", elevation_m=0.0, height_m=3.0),),
        spaces=(
            Space(
                space_id="SPACE-TEST-0001",
                name="Synthetischer Raum",
                storey_id="STOREY-TEST-0001",
                floor_area_m2=100.0,
                volume_m3=300.0,
            ),
        ),
        elements=(
            PhysicalElement(
                element_id="ELEMENT-TEST-0001",
                element_type="wall",
                construction_code="AW",
                storey_id="STOREY-TEST-0001",
                area_m2=100.0,
                orientation_deg=0.0,
                adjacent_space_ids=("SPACE-TEST-0001",),
            ),
        ),
        input_detail_level=BuildingInputDetailLevel.LOD_1,
        simple_envelope=SimpleEnvelopeInput(
            external_wall_u_value_w_m2k=0.2,
            window_u_value_w_m2k=1.0,
            window_area_ratio_percent=25.0,
        ),
    )


def _zone_specification() -> ZoneModelSpecification:
    return ZoneModelSpecification(
        schema_version="1.0",
        zone_model_id="ZONE-MODEL-TEST-0001",
        project_id="PROJECT-TEST-0001",
        building_id="BUILDING-TEST-0001",
        source_building_version_id="BUILDING-REV-0001",
        input_detail_level=ZoneInputDetailLevel.LOD_1,
        usage_profiles=(
            UsageProfile(
                profile_id="USE-TEST-0001",
                name="Synthetisches Nutzungsprofil",
                operation_start_hour=8.0,
                operation_end_hour=18.0,
                operation_days_per_week=5,
                occupancy_density_m2_per_person=20.0,
                lighting_power_w_m2=8.0,
                equipment_power_w_m2=5.0,
            ),
        ),
        zones=(
            ThermalZone(
                zone_id="ZONE-TEST-0001",
                name="Synthetische Zone",
                usage_profile_id="USE-TEST-0001",
                floor_area_m2=100.0,
                volume_m3=300.0,
                source_space_ids=("SPACE-TEST-0001",),
            ),
        ),
    )


def _technical_handover() -> ReleasedTechnicalHandover:
    return ReleasedTechnicalHandover(
        technical_model_id="TECH-TEST-0001",
        revision_id="TECH-REV-0001",
        content_hash="a" * 64,
        release_status=ReleaseStatus.RELEASED,
        service_interface_references=(),
    )


def _released_handovers():
    building_spec = _building_specification()
    zone_spec = _zone_specification()
    technical_handover = _technical_handover()
    thermal_building_model = ThermalBuildingModel(
        thermal_building_model_id="THERMAL-TEST-0001",
        project_id=building_spec.project.project_id,
        building_id=building_spec.building.building_id,
        building_revision_id=building_spec.model_version.version_id,
        zone_model_id=zone_spec.zone_model_id,
        technical_model_id=technical_handover.technical_model_id,
        technical_revision_id=technical_handover.revision_id,
        technical_content_hash=technical_handover.content_hash,
        room_zone_assignments=(("SPACE-TEST-0001", "ZONE-TEST-0001"),),
        release_status=ReleaseStatus.RELEASED,
    )
    zone_handover = build_released_zone_handover(
        building_spec,
        zone_spec,
        thermal_building_model,
        technical_handover,
    )
    return zone_handover, technical_handover


def _source_reference(
    module_key: str, *, dataset_key: str, version_id: str, content_hash: str
) -> ParameterSourceReference:
    return ParameterSourceReference(
        source_reference_id=f"source:{module_key}",
        module_key=module_key,
        dataset_key=dataset_key,
        version_id=version_id,
        validation_status=ReleaseStatus.RELEASED.value,
        label=f"Synthetische {module_key}-Quelle",
        reference_id=dataset_key,
        reference_version=version_id,
        content_hash=content_hash,
        freshness_status=FreshnessStatus.CURRENT.value,
    )


def _input_package() -> ParameterInputPackage:
    sources = (
        _source_reference(
            "ma_building",
            dataset_key="BUILDING-TEST-0001",
            version_id="BUILDING-REV-0001",
            content_hash="b" * 64,
        ),
        _source_reference(
            "ma_zones",
            dataset_key="ZONE-MODEL-TEST-0001",
            version_id="ZONE-MODEL-TEST-0001",
            content_hash="c" * 64,
        ),
        _source_reference(
            "ma_technical",
            dataset_key="TECH-TEST-0001",
            version_id="TECH-REV-0001",
            content_hash="d" * 64,
        ),
    )
    source_ids_by_module = {source.module_key: source.source_reference_id for source in sources}
    rows = (
        ("building_length_m", 10.0, "ma_building"),
        ("building_width_m", 10.0, "ma_building"),
        ("building_height_m", 3.0, "ma_building"),
        ("external_wall_u_value_w_m2k", 0.2, "ma_building"),
        ("window_u_value_w_m2k", 1.0, "ma_building"),
        ("window_area_ratio_percent", 25.0, "ma_building"),
        ("floor_area_m2", 100.0, "ma_building"),
        ("zone_count", 1, "ma_zones"),
        ("zone_floor_area_m2", 100.0, "ma_zones"),
        ("zone_volume_m3", 300.0, "ma_zones"),
        ("technical_system_count", 1, "ma_technical"),
    )
    values = tuple(
        ParameterValue(
            parameter_key=parameter_key,
            label=parameter_key,
            value=value,
            unit="dimensionless",
            source_reference_id=source_ids_by_module[module_key],
        )
        for parameter_key, value, module_key in rows
    )
    return ParameterInputPackage(
        package_id="PARAMETER-INPUT-TEST-0001",
        package_version="1.0",
        project_id="PROJECT-TEST-0001",
        building_id="BUILDING-TEST-0001",
        input_detail_level="LOD-1",
        values=values,
        source_references=sources,
        source_snapshot_id="PARAMETER-SNAPSHOT-TEST-0001",
        source_snapshot_version="1.0",
        requires_weather=False,
    )


def test_released_checkpoints_propagate_to_baseline_and_bind_its_content_hash():
    input_package = _input_package()
    zone_handover, technical_handover = _released_handovers()

    attached_package = attach_released_checkpoints_to_parameter_input_package(
        input_package,
        zone_handover=zone_handover,
        technical_handover=technical_handover,
    )

    assert attached_package.values == input_package.values
    assert attached_package.source_references == input_package.source_references
    assert attached_package.requires_released_checkpoints is True
    assert validate_parameter_input_package(attached_package).release_status is ReleaseStatus.RELEASED

    references_by_module = {reference.module_key: reference for reference in attached_package.checkpoint_references}
    assert set(references_by_module) == {"ma_zones", "ma_technical"}
    assert references_by_module["ma_zones"] == parameter_checkpoint_reference_from_released_zone_handover(zone_handover)
    assert references_by_module["ma_technical"] == parameter_checkpoint_reference_from_released_technical_handover(
        technical_handover
    )

    baseline = build_baseline_parameter_snapshot_from_input_package(
        attached_package,
        snapshot_id="BASELINE-TEST-0001",
        snapshot_version="2.0",
    )

    assert baseline.checkpoint_references == attached_package.checkpoint_references
    assert baseline.requires_released_checkpoints is True
    assert validate_baseline_parameter_snapshot(baseline).release_status is ReleaseStatus.RELEASED

    changed_checkpoint_package = replace(
        attached_package,
        checkpoint_references=tuple(
            replace(reference, content_hash="e" * 64) if reference.module_key == "ma_zones" else reference
            for reference in attached_package.checkpoint_references
        ),
    )
    changed_baseline = build_baseline_parameter_snapshot_from_input_package(
        changed_checkpoint_package,
        snapshot_id="BASELINE-TEST-0001",
        snapshot_version="2.0",
    )

    assert changed_baseline.content_hash != baseline.content_hash


def test_legacy_parameter_input_and_baseline_remain_without_released_checkpoints():
    input_package = _input_package()

    assert input_package.checkpoint_references == ()
    assert input_package.requires_released_checkpoints is False
    assert validate_parameter_input_package(input_package).release_status is ReleaseStatus.RELEASED

    baseline = build_baseline_parameter_snapshot_from_input_package(
        input_package,
        snapshot_id="BASELINE-LEGACY-TEST-0001",
        snapshot_version="2.0",
    )

    assert baseline.checkpoint_references == ()
    assert baseline.requires_released_checkpoints is False
    assert validate_baseline_parameter_snapshot(baseline).release_status is ReleaseStatus.RELEASED


@pytest.mark.parametrize(
    ("zone_mutation", "technical_mutation"),
    (
        (lambda zone: replace(zone, release_status=ReleaseStatus.BLOCKED), lambda technical: technical),
        (lambda zone: zone, lambda technical: replace(technical, release_status=ReleaseStatus.BLOCKED)),
        (lambda zone: zone, lambda technical: replace(technical, technical_model_id="TECH-OTHER-0001")),
    ),
)
def test_checkpoint_factory_blocks_unreleased_or_unrelated_handover_pairs(zone_mutation, technical_mutation):
    zone_handover, technical_handover = _released_handovers()

    with pytest.raises(ValueError):
        attach_released_checkpoints_to_parameter_input_package(
            _input_package(),
            zone_handover=zone_mutation(zone_handover),
            technical_handover=technical_mutation(technical_handover),
        )


def test_checkpoint_factory_blocks_a_missing_handover():
    _, technical_handover = _released_handovers()

    with pytest.raises((TypeError, ValueError)):
        attach_released_checkpoints_to_parameter_input_package(
            _input_package(),
            zone_handover=None,
            technical_handover=technical_handover,
        )


def test_checkpoint_validators_block_stale_or_incomplete_pairs():
    zone_handover, technical_handover = _released_handovers()
    attached_package = attach_released_checkpoints_to_parameter_input_package(
        _input_package(),
        zone_handover=zone_handover,
        technical_handover=technical_handover,
    )
    baseline = build_baseline_parameter_snapshot_from_input_package(
        attached_package,
        snapshot_id="BASELINE-VALIDATION-TEST-0001",
        snapshot_version="2.0",
    )

    stale_references = tuple(
        replace(reference, freshness_status=FreshnessStatus.OUTDATED.value)
        if reference.module_key == "ma_zones"
        else reference
        for reference in attached_package.checkpoint_references
    )
    stale_package = replace(attached_package, checkpoint_references=stale_references)
    stale_baseline = replace(baseline, checkpoint_references=stale_references)
    incomplete_package = replace(attached_package, checkpoint_references=())
    incomplete_baseline = replace(baseline, checkpoint_references=())

    assert validate_parameter_input_package(stale_package).release_status is ReleaseStatus.BLOCKED
    assert validate_baseline_parameter_snapshot(stale_baseline).release_status is ReleaseStatus.BLOCKED
    assert validate_parameter_input_package(incomplete_package).release_status is ReleaseStatus.BLOCKED
    assert validate_baseline_parameter_snapshot(incomplete_baseline).release_status is ReleaseStatus.BLOCKED


def test_populated_stale_checkpoints_block_even_without_required_checkpoint_mode():
    zone_handover, technical_handover = _released_handovers()
    attached_package = attach_released_checkpoints_to_parameter_input_package(
        _input_package(),
        zone_handover=zone_handover,
        technical_handover=technical_handover,
    )
    baseline = build_baseline_parameter_snapshot_from_input_package(
        attached_package,
        snapshot_id="BASELINE-OPTIONAL-CHECKPOINT-TEST-0001",
        snapshot_version="2.0",
    )
    stale_references = tuple(
        replace(reference, freshness_status=FreshnessStatus.OUTDATED.value)
        if reference.module_key == "ma_zones"
        else reference
        for reference in attached_package.checkpoint_references
    )

    optional_stale_package = replace(
        attached_package,
        checkpoint_references=stale_references,
        requires_released_checkpoints=False,
    )
    optional_stale_baseline = replace(
        baseline,
        checkpoint_references=stale_references,
        requires_released_checkpoints=False,
    )

    assert validate_parameter_input_package(optional_stale_package).release_status is ReleaseStatus.BLOCKED
    assert validate_baseline_parameter_snapshot(optional_stale_baseline).release_status is ReleaseStatus.BLOCKED
