from dataclasses import FrozenInstanceError, replace

import pytest

from ma_technical import (
    AirHandlingUnit,
    CapacityDefinition,
    CapacityMode,
    ComponentAvailability,
    CoolingDistribution,
    DomesticHotWaterGeneration,
    ElectricalSystem,
    HeatingConfigurationMode,
    HeatingDistribution,
    HeatingFunction,
    HeatingFunctionalRole,
    HeatingGeneration,
    ObjectReference,
    PhysicalEquipment,
    ReleasedTechnicalHandover,
    TechnicalInputDetailLevel,
    TechnicalMedium,
    TechnicalModelSchemaVersion,
    TechnicalModelSpecification,
    TechnicalPlant,
    TechnicalServiceInterface,
    TechnicalServiceType,
    ThermalStorage,
    build_released_technical_handover,
    load_business_integration_lod1_technical_spec,
    load_technical_model_revision,
    release_technical_model,
    technical_model_specification_from_dict,
    validate_technical_model,
)
from ma_technical.revisions import _content_hash, _to_payload
from ma_validation import ReleaseStatus


def _codes(result):
    return {message.code for message in result.messages}


def test_schema_v2_minimal_model_collects_object_ids():
    spec = _minimal_v2_spec()

    object_locations = dict(spec.object_id_locations())

    assert spec.schema_version == TechnicalModelSchemaVersion.V2.value
    assert spec.declared_detail_level is TechnicalInputDetailLevel.LOD_1
    assert object_locations["TECH-V2-0001"] == "technical_model_id"
    assert object_locations["PLANT-0001"] == "plant.plant_id"
    assert object_locations["HEAT-BASE-0001"] == "plant.heating_generation.base_heating.function_id"
    assert object_locations["AHU-0001"] == "air_handling_unit.ahu_id"
    assert object_locations["EL-0001"] == "electrical_system.electrical_system_id"
    assert object_locations["SI-HEAT-0001"] == "service_interfaces.0.interface_id"


def test_schema_v2_dataclasses_are_immutable():
    spec = _minimal_v2_spec()

    with pytest.raises(FrozenInstanceError):
        spec.technical_model_id = "CHANGED"


def test_capacity_modes_keep_capacity_sufficiency_out_of_structural_model():
    unlimited = CapacityDefinition(mode=CapacityMode.IDEAL_UNLIMITED)
    specified = CapacityDefinition(mode=CapacityMode.SPECIFIED, maximum_capacity_kw=12.5)

    assert unlimited.is_ideal_unlimited is True
    assert unlimited.requires_capacity_value is False
    assert specified.is_ideal_unlimited is False
    assert specified.requires_capacity_value is True


def test_service_interface_replaces_direct_zone_reference():
    interface = _minimal_v2_spec().service_interfaces[0]

    assert interface.service_type is TechnicalServiceType.HEATING
    assert interface.medium is TechnicalMedium.WATER
    assert not hasattr(interface, "served_zone_ids")


def test_schema_v2_collects_all_technical_registers():
    spec = _minimal_v2_spec()

    object_locations = dict(spec.object_id_locations())

    assert object_locations["EQ-HEATPUMP-0001"] == "equipment_register.0.equipment_id"
    assert object_locations["HEAT-DIST-0001"] == "heating_distribution_register.0.distribution_id"
    assert object_locations["COOL-DIST-0001"] == "cooling_distribution_register.0.distribution_id"
    assert object_locations["STORE-0001"] == "storage_register.0.storage_id"
    assert object_locations["DHW-0001"] == "domestic_hot_water_register.0.generation_id"


def test_schema_v2_allows_missing_optional_primary_areas():
    spec = TechnicalModelSpecification(
        schema_version=TechnicalModelSchemaVersion.V2.value,
        technical_model_id="TECH-V2-MINIMAL-0001",
        project_id="PROJECT-BI-TEST-BUILDING",
        building_reference=ObjectReference(
            object_id="BUILDING-BI-LOD1-0001",
            object_type="BuildingModelSpecification",
        ),
        declared_detail_level=TechnicalInputDetailLevel.LOD_1,
    )

    assert spec.plant is None
    assert spec.air_handling_unit is None
    assert spec.electrical_system is None


def test_schema_v2_validation_accepts_complete_minimal_aggregate():
    result = validate_technical_model(_minimal_v2_spec())

    assert result.release_status is ReleaseStatus.RELEASED


def test_v2_loader_roundtrips_the_complete_existing_aggregate_payload():
    specification = _minimal_v2_spec()
    payload = _to_payload(specification)

    reloaded = technical_model_specification_from_dict(payload)

    assert _to_payload(reloaded) == payload


def test_schema_v2_validation_blocks_duplicate_object_ids():
    spec = _minimal_v2_spec()
    duplicate_equipment = PhysicalEquipment(
        equipment_id="EQ-HEATPUMP-0001",
        equipment_type="backup_heat_pump",
    )

    result = validate_technical_model(replace(spec, equipment_register=(*spec.equipment_register, duplicate_equipment)))

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "TECHNICAL_V2_OBJECT_ID_DUPLICATE" in _codes(result)


def test_schema_v2_validation_blocks_unknown_internal_references():
    spec = _minimal_v2_spec()
    interface = replace(
        spec.service_interfaces[0],
        source_system_reference=ObjectReference("UNKNOWN-HEAT", object_type="HeatingFunction"),
    )

    result = validate_technical_model(replace(spec, service_interfaces=(interface,)))

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "TECHNICAL_V2_REFERENCE_UNKNOWN" in _codes(result)


def test_released_v2_technical_revision_roundtrips_with_stable_hash(tmp_path):
    revision = release_technical_model(
        _minimal_v2_spec(),
        revision_id="TECH-V2-REV-0001",
        target_dir=tmp_path,
    )
    loaded = load_technical_model_revision(tmp_path / "TECH-V2-REV-0001.yaml")

    assert loaded.technical_model_id == "TECH-V2-0001"
    assert loaded.revision_id == revision.revision_id
    assert loaded.content_hash == revision.content_hash
    assert loaded.release_status is ReleaseStatus.RELEASED
    assert loaded.specification_payload["technical_model_id"] == "TECH-V2-0001"


def test_releasing_same_technical_revision_never_overwrites_existing_file(tmp_path):
    release_technical_model(_minimal_v2_spec(), revision_id="TECH-V2-REV-0001", target_dir=tmp_path)

    with pytest.raises(FileExistsError):
        release_technical_model(_minimal_v2_spec(), revision_id="TECH-V2-REV-0001", target_dir=tmp_path)


def test_technical_revision_hash_ignores_creation_timestamps(tmp_path):
    first = release_technical_model(_minimal_v2_spec(), revision_id="TECH-V2-REV-0001", target_dir=tmp_path)
    second = release_technical_model(_minimal_v2_spec(), revision_id="TECH-V2-REV-0002", target_dir=tmp_path)

    assert first.content_hash == second.content_hash


def test_released_technical_handover_contains_only_stable_reference_metadata(tmp_path):
    revision = release_technical_model(_minimal_v2_spec(), revision_id="TECH-V2-REV-0001", target_dir=tmp_path)

    handover = build_released_technical_handover(revision)

    assert isinstance(handover, ReleasedTechnicalHandover)
    assert handover.technical_model_id == "TECH-V2-0001"
    assert handover.revision_id == "TECH-V2-REV-0001"
    assert handover.content_hash == revision.content_hash
    assert handover.release_status is ReleaseStatus.RELEASED
    assert not hasattr(handover, "specification_payload")
    assert tuple(reference.interface_id for reference in handover.service_interface_references) == ("SI-HEAT-0001",)
    assert handover.service_interface_references[0].source_object_reference == ObjectReference(
        object_id="HEAT-BASE-0001",
        object_type="HeatingFunction",
    )

    with pytest.raises(FrozenInstanceError):
        handover.revision_id = "CHANGED"


def test_released_technical_handover_rejects_unreleased_revision(tmp_path):
    revision = release_technical_model(_minimal_v2_spec(), revision_id="TECH-V2-REV-0001", target_dir=tmp_path)

    with pytest.raises(ValueError, match="freigegebene Technikrevision"):
        build_released_technical_handover(replace(revision, release_status=ReleaseStatus.BLOCKED))


def test_released_technical_handover_rejects_tampered_hash(tmp_path):
    revision = release_technical_model(_minimal_v2_spec(), revision_id="TECH-V2-REV-0001", target_dir=tmp_path)

    with pytest.raises(ValueError, match="Content-Hash"):
        build_released_technical_handover(replace(revision, content_hash="0" * 64))


def test_released_technical_handover_rejects_inconsistent_payload_model_id(tmp_path):
    revision = release_technical_model(_minimal_v2_spec(), revision_id="TECH-V2-REV-0001", target_dir=tmp_path)

    with pytest.raises(ValueError, match="technical_model_id"):
        build_released_technical_handover(replace(revision, technical_model_id="TECH-V2-OTHER-0001"))


def test_released_technical_handover_rejects_non_v2_payload(tmp_path):
    revision = release_technical_model(_minimal_v2_spec(), revision_id="TECH-V2-REV-0001", target_dir=tmp_path)
    legacy_payload = {**revision.specification_payload, "schema_version": "1.0"}
    legacy_revision = replace(
        revision,
        specification_payload=legacy_payload,
        content_hash=_content_hash(legacy_payload),
    )

    with pytest.raises(ValueError, match="v2-Spezifikation"):
        build_released_technical_handover(legacy_revision)


def test_released_technical_handover_sorts_service_interfaces_deterministically(tmp_path):
    specification = _minimal_v2_spec()
    later_interface = specification.service_interfaces[0]
    earlier_interface = replace(later_interface, interface_id="SI-AIR-0001")
    revision = release_technical_model(
        replace(specification, service_interfaces=(later_interface, earlier_interface)),
        revision_id="TECH-V2-REV-0001",
        target_dir=tmp_path,
    )

    handover = build_released_technical_handover(revision)

    assert tuple(reference.interface_id for reference in handover.service_interface_references) == (
        "SI-AIR-0001",
        "SI-HEAT-0001",
    )


def test_schema_v2_parallel_types_do_not_break_legacy_v1_loader():
    legacy_spec = load_business_integration_lod1_technical_spec()

    assert legacy_spec.input_detail_level is TechnicalInputDetailLevel.LOD_1
    assert legacy_spec.source_zone_model_id == "ZONE-BI-LOD1-MODEL-0001"
    assert legacy_spec.systems[0].served_zone_ids == ("ZONE-BI-LOD1-0001",)


def _minimal_v2_spec() -> TechnicalModelSpecification:
    equipment = PhysicalEquipment(
        equipment_id="EQ-HEATPUMP-0001",
        equipment_type="reversible_heat_pump",
        availability=ComponentAvailability.PLANNED,
        supported_services=("heating", "cooling"),
    )
    base_heating = HeatingFunction(
        function_id="HEAT-BASE-0001",
        slot="base_heating",
        physical_equipment_reference=ObjectReference(equipment.equipment_id, object_type="PhysicalEquipment"),
        functional_role=HeatingFunctionalRole.SOLE_SUPPLY,
        capacity=CapacityDefinition(mode=CapacityMode.IDEAL_UNLIMITED),
        supported_services=("heating",),
    )
    service_interface = TechnicalServiceInterface(
        interface_id="SI-HEAT-0001",
        service_type=TechnicalServiceType.HEATING,
        source_system_reference=ObjectReference(base_heating.function_id, object_type="HeatingFunction"),
        medium=TechnicalMedium.WATER,
        capacity_mode=CapacityMode.IDEAL_UNLIMITED,
        compatible_terminal_types=("radiator", "floor_heating"),
    )
    return TechnicalModelSpecification(
        schema_version=TechnicalModelSchemaVersion.V2.value,
        technical_model_id="TECH-V2-0001",
        project_id="PROJECT-BI-TEST-BUILDING",
        building_reference=ObjectReference(
            object_id="BUILDING-BI-LOD1-0001",
            revision_id="BUILDING-REV-0001",
            object_type="BuildingModelSpecification",
        ),
        declared_detail_level=TechnicalInputDetailLevel.LOD_1,
        equipment_register=(equipment,),
        heating_distribution_register=(HeatingDistribution(distribution_id="HEAT-DIST-0001"),),
        cooling_distribution_register=(CoolingDistribution(distribution_id="COOL-DIST-0001"),),
        storage_register=(ThermalStorage(storage_id="STORE-0001", storage_type="buffer"),),
        domestic_hot_water_register=(
            DomesticHotWaterGeneration(
                generation_id="DHW-0001",
                generation_mode="central",
            ),
        ),
        plant=TechnicalPlant(
            plant_id="PLANT-0001",
            heating_generation=HeatingGeneration(
                configuration_mode=HeatingConfigurationMode.BASE_HEATING_ONLY,
                base_heating=base_heating,
            ),
        ),
        air_handling_unit=AirHandlingUnit(ahu_id="AHU-0001"),
        electrical_system=ElectricalSystem(
            electrical_system_id="EL-0001",
            consumer_references=(ObjectReference(equipment.equipment_id, object_type="PhysicalEquipment"),),
        ),
        service_interfaces=(service_interface,),
    )
