from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from ma_building import (
    BuildingInfo,
    BuildingInputDetailLevel,
    BuildingMaturityLevel,
    BuildingModelSpecification,
    BuildingModelVersion,
    PhysicalElement,
    ProjectInfo,
    Space,
    Storey,
)
from ma_technical import ReleasedTechnicalHandover, TechnicalModelRevision
from ma_validation import ReleaseStatus
from ma_zones import (
    ReleasedZoneHandover,
    ThermalBuildingModel,
    ThermalZone,
    UsageProfile,
    ZoneAssumption,
    ZoneInputDetailLevel,
    ZoneModelSpecification,
    build_released_zone_handover,
)


def _building_spec() -> BuildingModelSpecification:
    return BuildingModelSpecification(
        schema_version="1.0",
        project=ProjectInfo(project_id="PROJECT-0001", name="Synthetisches Testprojekt"),
        building=BuildingInfo(
            building_id="BUILDING-0001",
            name="Synthetisches Testgebaeude",
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
        storeys=(Storey("STOREY-0001", "EG", 0.0, 3.0),),
        spaces=(
            Space("SPACE-0001", "Raum 1", "STOREY-0001", 25.0, 75.0),
            Space("SPACE-0002", "Raum 2", "STOREY-0001", 25.0, 75.0),
            Space("SPACE-0003", "Raum 3", "STOREY-0001", 25.0, 75.0),
            Space("SPACE-0004", "Raum 4", "STOREY-0001", 25.0, 75.0),
        ),
        elements=(PhysicalElement("ELEMENT-0001", "wall", "AW", "STOREY-0001", 30.0),),
        input_detail_level=BuildingInputDetailLevel.LOD_2,
    )


def _zone_spec(*, reverse_order: bool = False) -> ZoneModelSpecification:
    profile_a = UsageProfile("PROFILE-0001", "Buero", 8.0, 18.0, 5, 20.0, 8.0, 10.0)
    profile_b = UsageProfile("PROFILE-0002", "Besprechung", 9.0, 17.0, 5, 15.0, 9.0, 11.0)
    zone_a = ThermalZone(
        "ZONE-0001",
        "Zone A",
        "PROFILE-0001",
        50.0,
        150.0,
        ("SPACE-0001", "SPACE-0002"),
    )
    zone_b = ThermalZone(
        "ZONE-0002",
        "Zone B",
        "PROFILE-0002",
        50.0,
        150.0,
        ("SPACE-0003", "SPACE-0004"),
    )
    assumption_a = ZoneAssumption("ASSUMPTION-0001", "Synthetische Annahme A")
    assumption_b = ZoneAssumption("ASSUMPTION-0002", "Synthetische Annahme B", "tests")
    if reverse_order:
        zone_a = replace(zone_a, source_space_ids=list(reversed(zone_a.source_space_ids)))
        zone_b = replace(zone_b, source_space_ids=list(reversed(zone_b.source_space_ids)))
        zones: tuple[ThermalZone, ...] | list[ThermalZone] = [zone_b, zone_a]
        profiles: tuple[UsageProfile, ...] | list[UsageProfile] = [profile_b, profile_a]
        assumptions: tuple[ZoneAssumption, ...] | list[ZoneAssumption] = [assumption_b, assumption_a]
    else:
        zones = (zone_a, zone_b)
        profiles = (profile_a, profile_b)
        assumptions = (assumption_a, assumption_b)
    return ZoneModelSpecification(
        schema_version="1.0",
        zone_model_id="ZONE-MODEL-0001",
        project_id="PROJECT-0001",
        building_id="BUILDING-0001",
        source_building_version_id="BUILDING-REV-0001",
        input_detail_level=ZoneInputDetailLevel.LOD_2,
        zones=zones,
        usage_profiles=profiles,
        assumptions=assumptions,
    )


def _technical_handover(*, release_status: ReleaseStatus = ReleaseStatus.RELEASED) -> ReleasedTechnicalHandover:
    return ReleasedTechnicalHandover(
        technical_model_id="TECHNICAL-0001",
        revision_id="TECHNICAL-REV-0001",
        content_hash="a" * 64,
        release_status=release_status,
        service_interface_references=(),
    )


def _thermal_building_model(
    *,
    reverse_order: bool = False,
    release_status: ReleaseStatus = ReleaseStatus.RELEASED,
) -> ThermalBuildingModel:
    assignments = (
        ("SPACE-0001", "ZONE-0001"),
        ("SPACE-0002", "ZONE-0001"),
        ("SPACE-0003", "ZONE-0002"),
        ("SPACE-0004", "ZONE-0002"),
    )
    if reverse_order:
        assignments = list(reversed(assignments))
    return ThermalBuildingModel(
        thermal_building_model_id="THERMAL-BUILDING-0001",
        project_id="PROJECT-0001",
        building_id="BUILDING-0001",
        building_revision_id="BUILDING-REV-0001",
        zone_model_id="ZONE-MODEL-0001",
        technical_model_id="TECHNICAL-0001",
        technical_revision_id="TECHNICAL-REV-0001",
        technical_content_hash="a" * 64,
        room_zone_assignments=assignments,
        release_status=release_status,
    )


def _handover(**overrides: object) -> ReleasedZoneHandover:
    values = {
        "building_spec": _building_spec(),
        "zone_spec": _zone_spec(),
        "thermal_building_model": _thermal_building_model(),
        "technical_handover": _technical_handover(),
    }
    values.update(overrides)
    return build_released_zone_handover(**values)


def test_released_zone_handover_exposes_only_reproducible_reference_metadata():
    handover = _handover()

    assert handover.zone_handover_id == f"ma_zones:ZONE-MODEL-0001:{handover.revision_id}"
    assert handover.revision_id == f"ZONE-HANDOVER-{handover.content_hash[:16]}"
    assert handover.zone_model_id == "ZONE-MODEL-0001"
    assert handover.project_id == "PROJECT-0001"
    assert handover.building_id == "BUILDING-0001"
    assert handover.building_revision_id == "BUILDING-REV-0001"
    assert handover.technical_model_id == "TECHNICAL-0001"
    assert handover.technical_revision_id == "TECHNICAL-REV-0001"
    assert handover.technical_content_hash == "a" * 64
    assert handover.release_status is ReleaseStatus.RELEASED
    assert not hasattr(handover, "room_zone_assignments")
    assert not hasattr(handover, "zones")
    assert not hasattr(handover, "specification_payload")


def test_zone_handover_hash_is_stable_for_tuple_and_list_order_only():
    first = _handover()
    reordered = _handover(
        zone_spec=_zone_spec(reverse_order=True),
        thermal_building_model=_thermal_building_model(reverse_order=True),
    )

    assert reordered.content_hash == first.content_hash
    assert reordered.revision_id == first.revision_id
    assert reordered.zone_handover_id == first.zone_handover_id


def test_zone_handover_hash_changes_for_semantic_zone_mutation():
    zone_spec = _zone_spec()
    changed_zone = replace(zone_spec.zones[0], heating_setpoint_c=21.0)

    original = _handover(zone_spec=zone_spec)
    changed = _handover(zone_spec=replace(zone_spec, zones=(changed_zone, *zone_spec.zones[1:])))

    assert changed.content_hash != original.content_hash
    assert changed.revision_id != original.revision_id


def test_zone_handover_hash_changes_for_semantic_room_zone_assignment():
    original = _handover()
    reassigned_thermal_model = replace(
        _thermal_building_model(),
        room_zone_assignments=(
            ("SPACE-0001", "ZONE-0002"),
            ("SPACE-0002", "ZONE-0002"),
            ("SPACE-0003", "ZONE-0001"),
            ("SPACE-0004", "ZONE-0001"),
        ),
    )

    changed = _handover(thermal_building_model=reassigned_thermal_model)

    assert changed.content_hash != original.content_hash
    assert changed.revision_id != original.revision_id


def test_zone_handover_hash_changes_for_matching_new_building_id_and_revision():
    original = _handover()
    building_spec = _building_spec()
    changed_building = replace(
        building_spec,
        building=replace(building_spec.building, building_id="BUILDING-0002"),
        model_version=replace(building_spec.model_version, version_id="BUILDING-REV-0002"),
    )
    changed_zone_spec = replace(
        _zone_spec(),
        building_id="BUILDING-0002",
        source_building_version_id="BUILDING-REV-0002",
    )
    changed_thermal_model = replace(
        _thermal_building_model(),
        building_id="BUILDING-0002",
        building_revision_id="BUILDING-REV-0002",
    )

    changed = _handover(
        building_spec=changed_building,
        zone_spec=changed_zone_spec,
        thermal_building_model=changed_thermal_model,
    )

    assert changed.content_hash != original.content_hash
    assert changed.revision_id != original.revision_id


def test_zone_handover_hash_changes_for_matching_new_technical_triple():
    original = _handover()
    changed_technical_handover = ReleasedTechnicalHandover(
        technical_model_id="TECHNICAL-0002",
        revision_id="TECHNICAL-REV-0002",
        content_hash="b" * 64,
        release_status=ReleaseStatus.RELEASED,
        service_interface_references=(),
    )
    changed_thermal_model = replace(
        _thermal_building_model(),
        technical_model_id="TECHNICAL-0002",
        technical_revision_id="TECHNICAL-REV-0002",
        technical_content_hash="b" * 64,
    )

    changed = _handover(
        thermal_building_model=changed_thermal_model,
        technical_handover=changed_technical_handover,
    )

    assert changed.content_hash != original.content_hash
    assert changed.revision_id != original.revision_id


def test_zone_handover_rejects_mismatched_technical_triple():
    with pytest.raises(ValueError, match="Technikreferenzen"):
        _handover(technical_handover=replace(_technical_handover(), revision_id="TECHNICAL-REV-OTHER"))


def test_zone_handover_rejects_raw_technical_revision_outside_the_p014_gateway():
    raw_revision = TechnicalModelRevision(
        technical_model_id="TECHNICAL-0001",
        revision_id="TECHNICAL-REV-0001",
        content_hash="a" * 64,
        release_status=ReleaseStatus.RELEASED,
        specification_payload={"schema_version": "1.0"},
        released_at=datetime.now(timezone.utc),
    )

    with pytest.raises(TypeError, match="ReleasedTechnicalHandover"):
        _handover(technical_handover=raw_revision)


def test_zone_handover_rejects_duck_typed_technical_handover():
    duck_typed_handover = SimpleNamespace(
        technical_model_id="TECHNICAL-0001",
        revision_id="TECHNICAL-REV-0001",
        content_hash="a" * 64,
        release_status=ReleaseStatus.RELEASED,
    )

    with pytest.raises(TypeError, match="ReleasedTechnicalHandover"):
        _handover(technical_handover=duck_typed_handover)


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        (
            {"building_spec": replace(_building_spec(), building=replace(_building_spec().building, unit="cm"))},
            "Building",
        ),
        ({"zone_spec": replace(_zone_spec(), input_detail_level="LOD-UNKNOWN")}, "Zonenspezifikation"),
        (
            {"thermal_building_model": _thermal_building_model(release_status=ReleaseStatus.BLOCKED)},
            "ThermalBuildingModel",
        ),
        ({"technical_handover": _technical_handover(release_status=ReleaseStatus.BLOCKED)}, "Technik-Handover"),
        ({"technical_handover": replace(_technical_handover(), content_hash="")}, "content_hash"),
    ],
)
def test_zone_handover_rejects_invalid_or_unreleased_inputs(overrides: dict[str, object], message: str):
    with pytest.raises(ValueError, match=message):
        _handover(**overrides)


def test_released_zone_handover_is_immutable():
    handover = _handover()

    with pytest.raises(FrozenInstanceError):
        handover.content_hash = "b" * 64
