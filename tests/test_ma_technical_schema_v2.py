from dataclasses import FrozenInstanceError

import pytest

from ma_technical import (
    AirHandlingUnit,
    CapacityDefinition,
    CapacityMode,
    ComponentAvailability,
    ElectricalSystem,
    HeatingConfigurationMode,
    HeatingFunction,
    HeatingFunctionalRole,
    HeatingGeneration,
    ObjectReference,
    PhysicalEquipment,
    TechnicalInputDetailLevel,
    TechnicalMedium,
    TechnicalModelSchemaVersion,
    TechnicalModelSpecification,
    TechnicalPlant,
    TechnicalServiceInterface,
    TechnicalServiceType,
    load_business_integration_lod1_technical_spec,
)


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
