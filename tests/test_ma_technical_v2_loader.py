"""Vertragstests fuer den additiven, synthetischen P014-v2-YAML-Einstieg."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

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
from ma_core import InputSource, InputSourceKind
from ma_parameters import (
    ParameterInputPackage,
    ParameterSourceReference,
    ParameterValue,
    attach_released_checkpoints_to_parameter_input_package,
    build_baseline_parameter_snapshot_from_input_package,
    parameter_source_reference_from_released_technical_handover,
    validate_baseline_parameter_snapshot,
    validate_parameter_input_package,
)
from ma_technical import (
    AirHandlingUnit,
    CapacityDefinition,
    CapacityMode,
    ComponentAvailability,
    CoolingDistribution,
    CoolingGeneration,
    DomesticHotWaterGeneration,
    ElectricalSystem,
    ElectricReheater,
    FanConfiguration,
    HeatingConfigurationMode,
    HeatingCurve,
    HeatingCurvePoint,
    HeatingDispatchConfiguration,
    HeatingDispatchStrategy,
    HeatingDistribution,
    HeatingFunction,
    HeatingFunctionalRole,
    HeatingGeneration,
    HeatRecoveryConfiguration,
    ObjectReference,
    PerformanceDefinition,
    PerformanceMetricType,
    PhysicalEquipment,
    PumpConfiguration,
    ReleasedTechnicalHandover,
    SourceMetadata,
    TechnicalConnection,
    TechnicalInputDetailLevel,
    TechnicalMedium,
    TechnicalModelSchemaVersion,
    TechnicalModelSpecification,
    TechnicalPlant,
    TechnicalPort,
    TechnicalRepresentationMode,
    TechnicalSchedule,
    TechnicalScheduleRegistry,
    TechnicalServiceInterface,
    TechnicalServiceType,
    TechnicalTopology,
    TechnicalValueMetadata,
    ThermalStorage,
    build_released_technical_handover,
    load_business_integration_lod1_technical_spec,
    load_technical_model_revision,
    load_technical_model_specification,
    release_technical_model,
    technical_model_specification_from_dict,
    validate_technical_model,
)
from ma_technical.metadata import TechnicalAssumption
from ma_technical.revisions import _to_payload
from ma_validation import ReleaseStatus
from ma_zones import (
    ThermalBuildingModel,
    ThermalZone,
    UsageProfile,
    ZoneInputDetailLevel,
    ZoneModelSpecification,
    build_released_zone_handover,
)

REFERENCE_SPEC_PATH = (
    Path(__file__).resolve().parents[1] / "config" / "ma_technical" / "examples" / "technical_v2_reference_spec.yaml"
)


def test_synthetic_v2_reference_yaml_loads_to_a_released_typed_model():
    specification = load_technical_model_specification(REFERENCE_SPEC_PATH)

    assert specification.technical_model_id == "SYNTHETIC-TECHNICAL-MODEL-0001"
    assert specification.plant is None
    assert specification.air_handling_unit is None
    assert specification.electrical_system is None
    assert specification.service_interfaces[0].interface_id == "SYNTHETIC-SERVICE-HEATING-0001"
    assert not hasattr(specification.service_interfaces[0], "served_zone_ids")
    assert validate_technical_model(specification).release_status is ReleaseStatus.RELEASED


@pytest.mark.parametrize(
    "mutation",
    (
        lambda data: data.update(schema_version="1.0"),
        lambda data: data.pop("building_reference"),
        lambda data: data.update(unexpected_field="SYNTHETIC-UNEXPECTED-0001"),
        lambda data: data["equipment_register"][0].update(unexpected_field="SYNTHETIC-UNEXPECTED-0001"),
        lambda data: data["equipment_register"][0].update(availability="SYNTHETIC-UNKNOWN-STATUS"),
        lambda data: data.update(equipment_register=["SYNTHETIC-MALFORMED-EQUIPMENT-0001"]),
    ),
)
def test_v2_loader_blocks_schema_missing_unknown_and_malformed_nested_data(mutation):
    data = _reference_mapping()

    mutation(data)

    with pytest.raises(ValueError):
        technical_model_specification_from_dict(data)


def test_v2_loader_keeps_unknown_references_for_the_domain_validator_to_block():
    data = _reference_mapping()
    data["service_interfaces"][0]["source_system_reference"]["object_id"] = "SYNTHETIC-UNKNOWN-0001"

    result = validate_technical_model(technical_model_specification_from_dict(data))

    assert result.release_status is ReleaseStatus.BLOCKED
    assert {message.code for message in result.messages} >= {"TECHNICAL_V2_REFERENCE_UNKNOWN"}


@pytest.mark.parametrize(
    "mutation",
    (
        lambda data: data.update(technical_model_id=""),
        lambda data: data["equipment_register"][0].update(equipment_id="   "),
        lambda data: data["service_interfaces"][0].update(interface_id=""),
    ),
)
def test_v2_loader_blocks_empty_required_text_fields(mutation):
    data = _reference_mapping()

    mutation(data)

    with pytest.raises(ValueError):
        technical_model_specification_from_dict(data)


def test_synthetic_v2_reference_release_reloads_with_a_stable_content_hash(tmp_path):
    specification = load_technical_model_specification(REFERENCE_SPEC_PATH)
    first = release_technical_model(
        specification,
        revision_id="SYNTHETIC-TECHNICAL-REVISION-0001",
        target_dir=tmp_path,
    )
    loaded = load_technical_model_revision(tmp_path / "SYNTHETIC-TECHNICAL-REVISION-0001.yaml")
    second = release_technical_model(
        specification,
        revision_id="SYNTHETIC-TECHNICAL-REVISION-0002",
        target_dir=tmp_path,
    )

    assert loaded.content_hash == first.content_hash
    assert loaded.specification_payload["technical_model_id"] == specification.technical_model_id
    assert second.content_hash == first.content_hash


def test_v2_loader_and_revision_roundtrip_a_source_path_as_plain_yaml_text(tmp_path):
    data = _reference_mapping()
    data["source_metadata"] = {
        "source_type": "synthetic",
        "source_reference": "SYNTHETIC-INPUT-0001",
        "source_version": "SYNTHETIC-SOURCE-VERSION-0001",
        "imported_or_entered_at": "2026-07-18T12:00:00+00:00",
        "notes": "SYNTHETIC-SOURCE-METADATA",
        "input_source": {
            "module_key": "ma_technical",
            "source_kind": "demo",
            "data_format": "yaml",
            "source_path": "SYNTHETIC-INPUT/technical.yaml",
            "source_id": "SYNTHETIC-SOURCE-0001",
            "loaded_at": "2026-07-18T12:00:00+00:00",
        },
    }

    specification = technical_model_specification_from_dict(data)
    revision = release_technical_model(
        specification,
        revision_id="SYNTHETIC-TECHNICAL-REVISION-SOURCE-0001",
        target_dir=tmp_path,
    )
    loaded_revision = load_technical_model_revision(tmp_path / "SYNTHETIC-TECHNICAL-REVISION-SOURCE-0001.yaml")
    reloaded_specification = technical_model_specification_from_dict(loaded_revision.specification_payload)

    assert revision.content_hash == loaded_revision.content_hash
    expected_source_path = "SYNTHETIC-INPUT/technical.yaml"
    assert (
        loaded_revision.specification_payload["source_metadata"]["input_source"]["source_path"] == expected_source_path
    )
    assert reloaded_specification.source_metadata.input_source is not None
    assert reloaded_specification.source_metadata.input_source.source_path == Path(expected_source_path)


def test_v2_loader_uses_utc_defaults_and_requires_a_non_empty_persisted_source_id():
    data = _reference_mapping()
    data["source_metadata"] = {}

    specification = technical_model_specification_from_dict(data)

    assert specification.source_metadata.imported_or_entered_at.tzinfo is timezone.utc

    data["source_metadata"]["input_source"] = {
        "module_key": "ma_technical",
        "source_kind": "manual",
        "data_format": "yaml",
    }
    with pytest.raises(ValueError):
        technical_model_specification_from_dict(data)

    data["source_metadata"]["input_source"]["source_id"] = ""
    with pytest.raises(ValueError):
        technical_model_specification_from_dict(data)


def test_v2_loader_roundtrips_a_complete_synthetic_v2_model_payload(tmp_path):
    specification = _synthetic_all_fields_specification()
    payload = _to_payload(specification)
    yaml_payload = deepcopy(payload)
    yaml_payload["source_metadata"]["imported_or_entered_at"] = specification.source_metadata.imported_or_entered_at
    yaml_payload["source_metadata"]["input_source"]["loaded_at"] = specification.source_metadata.input_source.loaded_at
    yaml_path = tmp_path / "SYNTHETIC-all-fields.yaml"
    yaml_path.write_text(yaml.safe_dump(yaml_payload, sort_keys=False), encoding="utf-8")

    reloaded_specification = load_technical_model_specification(yaml_path)
    first_revision = release_technical_model(
        reloaded_specification,
        revision_id="SYNTHETIC-ALL-FIELDS-REVISION-0001",
        target_dir=tmp_path,
    )
    loaded_revision = load_technical_model_revision(tmp_path / "SYNTHETIC-ALL-FIELDS-REVISION-0001.yaml")
    second_revision = release_technical_model(
        load_technical_model_specification(yaml_path),
        revision_id="SYNTHETIC-ALL-FIELDS-REVISION-0002",
        target_dir=tmp_path,
    )

    assert _to_payload(reloaded_specification) == payload
    assert validate_technical_model(reloaded_specification).release_status is ReleaseStatus.RELEASED
    assert loaded_revision.specification_payload == payload
    assert loaded_revision.content_hash == first_revision.content_hash == second_revision.content_hash
    assert payload["source_metadata"]["input_source"]["source_path"] == ("SYNTHETIC-demo/SYNTHETIC-reference-01.yaml")


def test_synthetic_v2_handover_becomes_a_parameter_source_reference(tmp_path):
    revision = _released_revision(tmp_path)
    handover = build_released_technical_handover(revision)

    source = parameter_source_reference_from_released_technical_handover(handover)

    assert isinstance(handover, ReleasedTechnicalHandover)
    assert source.module_key == "ma_technical"
    assert source.reference_id == handover.technical_model_id
    assert source.reference_version == handover.revision_id
    assert source.content_hash == handover.content_hash


def test_synthetic_v2_contract_chain_reaches_p013_and_p015_released_checkpoints(tmp_path):
    revision = _released_revision(tmp_path)
    technical_handover = build_released_technical_handover(revision)
    building_specification = _synthetic_building_specification()
    zone_specification = _synthetic_zone_specification()
    thermal_model = ThermalBuildingModel(
        thermal_building_model_id="SYNTHETIC-THERMAL-BUILDING-0001",
        project_id=building_specification.project.project_id,
        building_id=building_specification.building.building_id,
        building_revision_id=building_specification.model_version.version_id,
        zone_model_id=zone_specification.zone_model_id,
        technical_model_id=technical_handover.technical_model_id,
        technical_revision_id=technical_handover.revision_id,
        technical_content_hash=technical_handover.content_hash,
        room_zone_assignments=(("SYNTHETIC-SPACE-0001", "SYNTHETIC-ZONE-0001"),),
    )
    zone_handover = build_released_zone_handover(
        building_specification,
        zone_specification,
        thermal_model,
        technical_handover,
    )
    input_package = _synthetic_parameter_input_package(technical_handover)

    checkpoint_package = attach_released_checkpoints_to_parameter_input_package(
        input_package,
        zone_handover=zone_handover,
        technical_handover=technical_handover,
    )
    baseline = build_baseline_parameter_snapshot_from_input_package(
        checkpoint_package,
        snapshot_id="SYNTHETIC-BASELINE-0001",
        snapshot_version="2.0",
    )

    assert validate_parameter_input_package(checkpoint_package).release_status is ReleaseStatus.RELEASED
    assert validate_baseline_parameter_snapshot(baseline).release_status is ReleaseStatus.RELEASED
    assert {reference.module_key for reference in baseline.checkpoint_references} == {"ma_zones", "ma_technical"}


def test_v2_loader_does_not_change_the_legacy_v1_technical_loader():
    legacy_specification = load_business_integration_lod1_technical_spec()

    assert legacy_specification.input_detail_level.value == "LOD-1"
    assert legacy_specification.source_zone_model_id == "ZONE-BI-LOD1-MODEL-0001"


def _reference_mapping() -> dict[str, object]:
    return deepcopy(yaml.safe_load(REFERENCE_SPEC_PATH.read_text(encoding="utf-8")))


def _released_revision(tmp_path):
    return release_technical_model(
        load_technical_model_specification(REFERENCE_SPEC_PATH),
        revision_id="SYNTHETIC-TECHNICAL-REVISION-0001",
        target_dir=tmp_path,
    )


def _synthetic_all_fields_specification() -> TechnicalModelSpecification:
    equipment_type = "PhysicalEquipment"
    heating_function_type = "HeatingFunction"
    cooling_generation_type = "CoolingGeneration"
    heating_distribution_type = "HeatingDistribution"
    cooling_distribution_type = "CoolingDistribution"
    storage_type = "ThermalStorage"
    electrical_type = "ElectricalSystem"
    ahu_type = "AirHandlingUnit"
    port_type = "TechnicalPort"

    heating_equipment = PhysicalEquipment(
        equipment_id="SYNTHETIC-EQUIPMENT-HEATING-0001",
        equipment_type="SYNTHETIC-EQUIPMENT-TYPE-HEATING",
        availability=ComponentAvailability.INSTALLED,
        representation_mode=TechnicalRepresentationMode.SPECIFIED,
        input_detail_level=TechnicalInputDetailLevel.LOD_2,
        product_reference=_reference("SYNTHETIC-EQUIPMENT-PRODUCT-0001", equipment_type),
        energy_carrier_reference=_reference("SYNTHETIC-EQUIPMENT-CARRIER-0001", equipment_type),
        supported_services=("SYNTHETIC-SERVICE-HEATING",),
        shared_operating_constraints=("SYNTHETIC-CONSTRAINT-HEATING",),
        electrical_connection_reference=_reference("SYNTHETIC-ELECTRICAL-0001", electrical_type),
        metadata=TechnicalValueMetadata(
            source=_synthetic_source_metadata(2),
            confirmation_status="SYNTHETIC-CONFIRMED",
            variability="SYNTHETIC-FIXED",
            assumption_reference="SYNTHETIC-ASSUMPTION-0001",
            decision_reference="SYNTHETIC-DECISION-0001",
        ),
    )
    cooling_equipment = PhysicalEquipment(
        equipment_id="SYNTHETIC-EQUIPMENT-COOLING-0001",
        equipment_type="SYNTHETIC-EQUIPMENT-TYPE-COOLING",
        availability=ComponentAvailability.PLANNED,
        representation_mode=TechnicalRepresentationMode.ASSUMED,
        input_detail_level=TechnicalInputDetailLevel.LOD_2,
        product_reference=_reference("SYNTHETIC-EQUIPMENT-PRODUCT-0001", equipment_type),
        energy_carrier_reference=_reference("SYNTHETIC-EQUIPMENT-CARRIER-0001", equipment_type),
        supported_services=("SYNTHETIC-SERVICE-COOLING",),
    )
    product_equipment = PhysicalEquipment(
        equipment_id="SYNTHETIC-EQUIPMENT-PRODUCT-0001",
        equipment_type="SYNTHETIC-EQUIPMENT-TYPE-PRODUCT",
    )
    carrier_equipment = PhysicalEquipment(
        equipment_id="SYNTHETIC-EQUIPMENT-CARRIER-0001",
        equipment_type="SYNTHETIC-EQUIPMENT-TYPE-CARRIER",
    )
    dhw_equipment = PhysicalEquipment(
        equipment_id="SYNTHETIC-EQUIPMENT-DHW-0001",
        equipment_type="SYNTHETIC-EQUIPMENT-TYPE-DHW",
    )

    heating_distribution = HeatingDistribution(
        distribution_id="SYNTHETIC-HEATING-DISTRIBUTION-0001",
        availability=ComponentAvailability.INSTALLED,
        heating_curve=HeatingCurve(
            points=(
                HeatingCurvePoint(-5.0, 40.0),
                HeatingCurvePoint(15.0, 25.0),
            ),
            interpolation_method="SYNTHETIC-LINEAR",
            extrapolation_policy="SYNTHETIC-CLAMP",
        ),
        design_temperature_drop_k=5.0,
        ahu_supply_temperature_c=32.0,
        night_setback_schedule_reference="SYNTHETIC-SCHEDULE-0001",
        pump=PumpConfiguration(
            pump_id="SYNTHETIC-PUMP-HEATING-0001",
            availability=ComponentAvailability.INSTALLED,
            power_method="SYNTHETIC-PUMP-METHOD",
            operation_schedule_reference="SYNTHETIC-SCHEDULE-0001",
            maximum_mass_flow_kg_s=0.7,
            specific_pump_power_w_per_l_s=2.0,
            design_pressure_pa=1000.0,
            efficiency=0.7,
            energy_meter_reference="SYNTHETIC-METER-HEATING-0001",
            model_specific_coefficients={"SYNTHETIC-COEFFICIENT-ONE": 1.0},
        ),
        pump_shutdown_outdoor_temperature_c=16.0,
        service_interface_reference="SYNTHETIC-SERVICE-HEATING-0001",
    )
    cooling_distribution = CoolingDistribution(
        distribution_id="SYNTHETIC-COOLING-DISTRIBUTION-0001",
        availability=ComponentAvailability.PLANNED,
        room_supply_temperature_c=16.0,
        ahu_supply_temperature_c=12.0,
        design_temperature_rise_k=4.0,
        pump=PumpConfiguration(
            pump_id="SYNTHETIC-PUMP-COOLING-0001",
            availability=ComponentAvailability.PLANNED,
            power_method="SYNTHETIC-PUMP-METHOD",
            operation_schedule_reference="SYNTHETIC-SCHEDULE-0002",
            maximum_mass_flow_kg_s=0.5,
            specific_pump_power_w_per_l_s=1.0,
            design_pressure_pa=900.0,
            efficiency=0.6,
            energy_meter_reference="SYNTHETIC-METER-COOLING-0001",
            model_specific_coefficients={"SYNTHETIC-COEFFICIENT-TWO": 2.0},
        ),
        service_interface_reference="SYNTHETIC-SERVICE-COOLING-0001",
    )
    heat_storage = ThermalStorage(
        storage_id="SYNTHETIC-STORAGE-HEAT-0001",
        storage_type="SYNTHETIC-STORAGE-TYPE-HEAT",
        availability=ComponentAvailability.INSTALLED,
        volume_m3=1.0,
        storage_medium="SYNTHETIC-STORAGE-MEDIUM",
        insulation_u_value_w_m2k=0.3,
        number_of_model_layers=3,
        electric_reheater=ElectricReheater(
            reheater_id="SYNTHETIC-REHEATER-HEAT-0001",
            availability=ComponentAvailability.INSTALLED,
            capacity_kw=2.0,
            control="SYNTHETIC-REHEATER-CONTROL",
        ),
        connections=("SYNTHETIC-CONNECTION-HEAT-0001",),
        adapter_extensions={
            "SYNTHETIC-EXTENSION-ONE": {"SYNTHETIC-FLAG": True},
            "SYNTHETIC-EXTENSION-TWO": ["SYNTHETIC-VALUE", 1],
        },
    )
    cold_storage = ThermalStorage(
        storage_id="SYNTHETIC-STORAGE-COLD-0001",
        storage_type="SYNTHETIC-STORAGE-TYPE-COLD",
        availability=ComponentAvailability.PLANNED,
        volume_m3=1.0,
    )
    dhw_storage = ThermalStorage(
        storage_id="SYNTHETIC-STORAGE-DHW-0001",
        storage_type="SYNTHETIC-STORAGE-TYPE-DHW",
        electric_reheater=ElectricReheater(
            reheater_id="SYNTHETIC-REHEATER-DHW-0001",
            capacity_kw=1.0,
        ),
    )

    heating_capacity = CapacityDefinition(
        mode=CapacityMode.SPECIFIED,
        nominal_capacity_kw=10.0,
        maximum_capacity_kw=12.0,
        minimum_capacity_kw=2.0,
        reference_conditions="SYNTHETIC-CAPACITY-CONDITIONS-HEATING",
        product_reference=_reference("SYNTHETIC-EQUIPMENT-PRODUCT-0001", equipment_type),
        source_metadata=_synthetic_source_metadata(3),
    )
    cooling_capacity = CapacityDefinition(
        mode=CapacityMode.SPECIFIED,
        nominal_capacity_kw=8.0,
        maximum_capacity_kw=9.0,
        minimum_capacity_kw=1.0,
        reference_conditions="SYNTHETIC-CAPACITY-CONDITIONS-COOLING",
        product_reference=_reference("SYNTHETIC-EQUIPMENT-PRODUCT-0001", equipment_type),
        source_metadata=_synthetic_source_metadata(4),
    )
    base_heating = HeatingFunction(
        function_id="SYNTHETIC-HEATING-FUNCTION-BASE-0001",
        slot="SYNTHETIC-HEATING-SLOT-BASE",
        functional_role=HeatingFunctionalRole.BASE_LOAD,
        capacity=heating_capacity,
        physical_equipment_reference=_reference(heating_equipment.equipment_id, equipment_type),
        availability=ComponentAvailability.INSTALLED,
        representation_mode=TechnicalRepresentationMode.SPECIFIED,
        performance=PerformanceDefinition(
            metric_type=PerformanceMetricType.HEATING_COP,
            value=3.0,
            reference_conditions="SYNTHETIC-PERFORMANCE-CONDITIONS-HEATING",
            source_metadata=_synthetic_source_metadata(5),
        ),
        energy_carrier_reference=_reference(carrier_equipment.equipment_id, equipment_type),
        meter_assignments=("SYNTHETIC-METER-HEATING-0001",),
        supported_services=("SYNTHETIC-SERVICE-HEATING",),
        operating_limits=("SYNTHETIC-LIMIT-HEATING",),
        control="SYNTHETIC-CONTROL-HEATING",
        schedule_reference="SYNTHETIC-SCHEDULE-0001",
    )
    top_up_heating = HeatingFunction(
        function_id="SYNTHETIC-HEATING-FUNCTION-TOP-UP-0001",
        slot="SYNTHETIC-HEATING-SLOT-TOP-UP",
        functional_role=HeatingFunctionalRole.TOP_UP_LOAD,
        capacity=CapacityDefinition(mode=CapacityMode.IDEAL_UNLIMITED),
        physical_equipment_reference=_reference(cooling_equipment.equipment_id, equipment_type),
        supported_services=("SYNTHETIC-SERVICE-HEATING",),
    )
    cooling_generation = CoolingGeneration(
        function_id="SYNTHETIC-COOLING-FUNCTION-0001",
        capacity=cooling_capacity,
        physical_equipment_reference=_reference(cooling_equipment.equipment_id, equipment_type),
        availability=ComponentAvailability.PLANNED,
        representation_mode=TechnicalRepresentationMode.SPECIFIED,
        performance=PerformanceDefinition(
            metric_type=PerformanceMetricType.COOLING_COP,
            value=2.0,
            reference_conditions="SYNTHETIC-PERFORMANCE-CONDITIONS-COOLING",
            source_metadata=_synthetic_source_metadata(6),
        ),
        energy_carrier_reference=_reference(carrier_equipment.equipment_id, equipment_type),
        meter_assignments=("SYNTHETIC-METER-COOLING-0001",),
        operating_limits=("SYNTHETIC-LIMIT-COOLING",),
        control="SYNTHETIC-CONTROL-COOLING",
        schedule_reference="SYNTHETIC-SCHEDULE-0002",
    )
    plant = TechnicalPlant(
        plant_id="SYNTHETIC-PLANT-0001",
        heating_generation=HeatingGeneration(
            configuration_mode=HeatingConfigurationMode.BASE_AND_TOP_UP_HEATING,
            base_heating=base_heating,
            top_up_heating=top_up_heating,
            dispatch=HeatingDispatchConfiguration(
                strategy=HeatingDispatchStrategy.BASE_FIRST,
                notes="SYNTHETIC-DISPATCH-NOTES",
            ),
        ),
        cooling_generation=cooling_generation,
        heat_storage_reference=_reference(heat_storage.storage_id, storage_type),
        cold_storage_reference=_reference(cold_storage.storage_id, storage_type),
    )
    domestic_hot_water = DomesticHotWaterGeneration(
        generation_id="SYNTHETIC-DHW-GENERATION-0001",
        generation_mode="SYNTHETIC-DHW-MODE",
        heating_function_reference=_reference(base_heating.function_id, heating_function_type),
        separate_generator=_reference(dhw_equipment.equipment_id, equipment_type),
        storage=dhw_storage,
        circulation="SYNTHETIC-DHW-CIRCULATION",
        control="SYNTHETIC-DHW-CONTROL",
        service_interface_reference="SYNTHETIC-SERVICE-DHW-0001",
    )
    ahu = AirHandlingUnit(
        ahu_id="SYNTHETIC-AHU-0001",
        availability=ComponentAvailability.INSTALLED,
        representation_mode=TechnicalRepresentationMode.SPECIFIED,
        input_detail_level=TechnicalInputDetailLevel.LOD_2,
        supply_air_temperature_control="SYNTHETIC-AHU-CONTROL",
        supply_fan=FanConfiguration(
            fan_id="SYNTHETIC-FAN-SUPPLY-0001",
            availability=ComponentAvailability.INSTALLED,
            design_pressure_pa=300.0,
            efficiency=0.6,
            power_method="SYNTHETIC-FAN-METHOD",
            operation_schedule_reference="SYNTHETIC-SCHEDULE-0003",
        ),
        extract_fan=FanConfiguration(
            fan_id="SYNTHETIC-FAN-EXTRACT-0001",
            availability=ComponentAvailability.INSTALLED,
            design_pressure_pa=280.0,
            efficiency=0.6,
            power_method="SYNTHETIC-FAN-METHOD",
            operation_schedule_reference="SYNTHETIC-SCHEDULE-0003",
        ),
        heat_recovery=HeatRecoveryConfiguration(
            heat_recovery_id="SYNTHETIC-HEAT-RECOVERY-0001",
            availability=ComponentAvailability.INSTALLED,
            efficiency_percent=70.0,
            operation_schedule_reference="SYNTHETIC-SCHEDULE-0003",
            bypass_control="SYNTHETIC-BYPASS-CONTROL",
        ),
        heating_coil=_reference(base_heating.function_id, heating_function_type),
        cooling_coil=_reference(cooling_generation.function_id, cooling_generation_type),
        heating_circuit_reference=_reference(heating_distribution.distribution_id, heating_distribution_type),
        cooling_circuit_reference=_reference(cooling_distribution.distribution_id, cooling_distribution_type),
        operation_schedule_reference="SYNTHETIC-SCHEDULE-0003",
        supply_air_interface="SYNTHETIC-SERVICE-SUPPLY-AIR-0001",
        extract_air_interface="SYNTHETIC-SERVICE-EXTRACT-AIR-0001",
    )
    electrical_system = ElectricalSystem(
        electrical_system_id="SYNTHETIC-ELECTRICAL-0001",
        availability=ComponentAvailability.INSTALLED,
        grid_connection="SYNTHETIC-GRID-CONNECTION",
        meters=("SYNTHETIC-METER-HEATING-0001", "SYNTHETIC-METER-COOLING-0001"),
        photovoltaic_system=_reference(product_equipment.equipment_id, equipment_type),
        wind_turbine=_reference(carrier_equipment.equipment_id, equipment_type),
        battery_system=_reference(dhw_equipment.equipment_id, equipment_type),
        consumer_references=(
            _reference(heating_equipment.equipment_id, equipment_type),
            _reference(cooling_equipment.equipment_id, equipment_type),
        ),
    )
    topology = TechnicalTopology(
        ports=(
            TechnicalPort(
                port_id="SYNTHETIC-PORT-HEATING-0001",
                owner_object_reference=_reference(base_heating.function_id, heating_function_type),
                port_type="SYNTHETIC-PORT-TYPE-HEATING",
                medium=TechnicalMedium.WATER,
                direction="SYNTHETIC-DIRECTION-OUT",
                service_type=TechnicalServiceType.HEATING,
            ),
            TechnicalPort(
                port_id="SYNTHETIC-PORT-COOLING-0001",
                owner_object_reference=_reference(cooling_generation.function_id, cooling_generation_type),
                port_type="SYNTHETIC-PORT-TYPE-COOLING",
                medium=TechnicalMedium.WATER,
                direction="SYNTHETIC-DIRECTION-IN",
                service_type=TechnicalServiceType.COOLING,
            ),
        ),
        connections=(
            TechnicalConnection(
                connection_id="SYNTHETIC-TOPOLOGY-CONNECTION-0001",
                source_port_reference=_reference("SYNTHETIC-PORT-HEATING-0001", port_type),
                target_port_reference=_reference("SYNTHETIC-PORT-COOLING-0001", port_type),
                medium=TechnicalMedium.WATER,
                connection_role="SYNTHETIC-CONNECTION-ROLE",
                generated_from_user_relation="SYNTHETIC-USER-RELATION-0001",
            ),
        ),
        generation_metadata="SYNTHETIC-TOPOLOGY-METADATA",
    )
    service_interfaces = (
        TechnicalServiceInterface(
            interface_id="SYNTHETIC-SERVICE-HEATING-0001",
            service_type=TechnicalServiceType.HEATING,
            source_system_reference=_reference(base_heating.function_id, heating_function_type),
            medium=TechnicalMedium.WATER,
            supply_temperature_definition="SYNTHETIC-SUPPLY-HEATING",
            return_temperature_definition="SYNTHETIC-RETURN-HEATING",
            capacity_mode=CapacityMode.SPECIFIED,
            compatible_terminal_types=("SYNTHETIC-TERMINAL-HEATING",),
            availability=ComponentAvailability.INSTALLED,
            revision_id="SYNTHETIC-SERVICE-REVISION-HEATING-0001",
            content_hash="a" * 64,
        ),
        TechnicalServiceInterface(
            interface_id="SYNTHETIC-SERVICE-COOLING-0001",
            service_type=TechnicalServiceType.COOLING,
            source_system_reference=_reference(cooling_generation.function_id, cooling_generation_type),
            medium=TechnicalMedium.WATER,
            capacity_mode=CapacityMode.SPECIFIED,
            compatible_terminal_types=("SYNTHETIC-TERMINAL-COOLING",),
            revision_id="SYNTHETIC-SERVICE-REVISION-COOLING-0001",
            content_hash="b" * 64,
        ),
        TechnicalServiceInterface(
            interface_id="SYNTHETIC-SERVICE-DHW-0001",
            service_type=TechnicalServiceType.DOMESTIC_HOT_WATER,
            source_system_reference=_reference(
                domestic_hot_water.generation_id,
                "DomesticHotWaterGeneration",
            ),
            medium=TechnicalMedium.DOMESTIC_HOT_WATER,
            compatible_terminal_types=("SYNTHETIC-TERMINAL-DHW",),
            revision_id="SYNTHETIC-SERVICE-REVISION-DHW-0001",
            content_hash="c" * 64,
        ),
        TechnicalServiceInterface(
            interface_id="SYNTHETIC-SERVICE-SUPPLY-AIR-0001",
            service_type=TechnicalServiceType.SUPPLY_AIR,
            source_system_reference=_reference(ahu.ahu_id, ahu_type),
            medium=TechnicalMedium.AIR,
            compatible_terminal_types=("SYNTHETIC-TERMINAL-SUPPLY-AIR",),
            revision_id="SYNTHETIC-SERVICE-REVISION-SUPPLY-AIR-0001",
            content_hash="d" * 64,
        ),
        TechnicalServiceInterface(
            interface_id="SYNTHETIC-SERVICE-EXTRACT-AIR-0001",
            service_type=TechnicalServiceType.EXTRACT_AIR,
            source_system_reference=_reference(ahu.ahu_id, ahu_type),
            medium=TechnicalMedium.AIR,
            compatible_terminal_types=("SYNTHETIC-TERMINAL-EXTRACT-AIR",),
            revision_id="SYNTHETIC-SERVICE-REVISION-EXTRACT-AIR-0001",
            content_hash="e" * 64,
        ),
    )
    return TechnicalModelSpecification(
        schema_version=TechnicalModelSchemaVersion.V2.value,
        technical_model_id="SYNTHETIC-ALL-FIELDS-TECHNICAL-MODEL-0001",
        project_id="SYNTHETIC-ALL-FIELDS-PROJECT-0001",
        building_reference=ObjectReference(
            object_id="SYNTHETIC-ALL-FIELDS-BUILDING-0001",
            revision_id="SYNTHETIC-ALL-FIELDS-BUILDING-REVISION-0001",
            content_hash="f" * 64,
            object_type="BuildingModelSpecification",
        ),
        declared_detail_level=TechnicalInputDetailLevel.LOD_2,
        equipment_register=(
            heating_equipment,
            cooling_equipment,
            product_equipment,
            carrier_equipment,
            dhw_equipment,
        ),
        heating_distribution_register=(heating_distribution,),
        cooling_distribution_register=(cooling_distribution,),
        storage_register=(heat_storage, cold_storage),
        domestic_hot_water_register=(domestic_hot_water,),
        plant=plant,
        air_handling_unit=ahu,
        electrical_system=electrical_system,
        schedules=TechnicalScheduleRegistry(
            schedules=(
                TechnicalSchedule(
                    schedule_id="SYNTHETIC-SCHEDULE-0001",
                    name="SYNTHETIC-SCHEDULE-HEATING",
                    schedule_type="SYNTHETIC-SCHEDULE-TYPE",
                    values_reference="SYNTHETIC-SCHEDULE-VALUES-0001",
                    notes="SYNTHETIC-SCHEDULE-NOTES-HEATING",
                ),
                TechnicalSchedule(
                    schedule_id="SYNTHETIC-SCHEDULE-0002",
                    name="SYNTHETIC-SCHEDULE-COOLING",
                    schedule_type="SYNTHETIC-SCHEDULE-TYPE",
                    values_reference="SYNTHETIC-SCHEDULE-VALUES-0002",
                    notes="SYNTHETIC-SCHEDULE-NOTES-COOLING",
                ),
                TechnicalSchedule(
                    schedule_id="SYNTHETIC-SCHEDULE-0003",
                    name="SYNTHETIC-SCHEDULE-AHU",
                    schedule_type="SYNTHETIC-SCHEDULE-TYPE",
                    values_reference="SYNTHETIC-SCHEDULE-VALUES-0003",
                    notes="SYNTHETIC-SCHEDULE-NOTES-AHU",
                ),
            ),
            registry_revision="SYNTHETIC-SCHEDULE-REGISTRY-REVISION-0001",
        ),
        topology=topology,
        service_interfaces=service_interfaces,
        assumptions=(
            TechnicalAssumption(
                assumption_id="SYNTHETIC-ASSUMPTION-0001",
                text="SYNTHETIC-ASSUMPTION-TEXT",
                location="SYNTHETIC-ASSUMPTION-LOCATION",
            ),
        ),
        source_metadata=_synthetic_source_metadata(1),
    )


def _reference(object_id: str, object_type: str) -> ObjectReference:
    return ObjectReference(object_id=object_id, object_type=object_type)


def _synthetic_source_metadata(index: int) -> SourceMetadata:
    timestamp = datetime(2026, 7, 18, 12, index, tzinfo=timezone.utc)
    return SourceMetadata(
        source_type="SYNTHETIC-SOURCE-TYPE",
        source_reference=f"SYNTHETIC-SOURCE-REFERENCE-{index:02d}",
        source_version=f"SYNTHETIC-SOURCE-VERSION-{index:02d}",
        imported_or_entered_at=timestamp,
        notes=f"SYNTHETIC-SOURCE-NOTES-{index:02d}",
        input_source=InputSource(
            module_key="ma_technical",
            source_kind=InputSourceKind.DEMO,
            data_format="yaml",
            source_path=Path(f"SYNTHETIC-demo/SYNTHETIC-reference-{index:02d}.yaml"),
            adapter_key=f"SYNTHETIC-ADAPTER-{index:02d}",
            is_template=True,
            file_size_bytes=100 + index,
            sha256="a" * 64,
            source_id=f"SYNTHETIC-INPUT-SOURCE-{index:02d}",
            loaded_at=timestamp,
        ),
    )


def _synthetic_building_specification() -> BuildingModelSpecification:
    return BuildingModelSpecification(
        schema_version="1.0",
        project=ProjectInfo("SYNTHETIC-PROJECT-0001", "SYNTHETIC-BUILDING-PROJECT"),
        building=BuildingInfo("SYNTHETIC-BUILDING-0001", "SYNTHETIC-BUILDING", "m", 0.0, 10.0, 10.0, 3.0),
        model_version=BuildingModelVersion(
            version_id="SYNTHETIC-BUILDING-REV-0001",
            source_input_level=BuildingMaturityLevel.BIL_1,
            detected_input_level=BuildingMaturityLevel.BIL_1,
            confirmed_input_level=BuildingMaturityLevel.BIL_1,
            current_maturity_level=BuildingMaturityLevel.BIL_1,
            target_maturity_level=BuildingMaturityLevel.BIL_1,
        ),
        storeys=(Storey("SYNTHETIC-STOREY-0001", "SYNTHETIC-STOREY", 0.0, 3.0),),
        spaces=(Space("SYNTHETIC-SPACE-0001", "SYNTHETIC-SPACE", "SYNTHETIC-STOREY-0001", 100.0, 300.0),),
        elements=(
            PhysicalElement(
                "SYNTHETIC-ELEMENT-0001",
                "wall",
                "AW",
                "SYNTHETIC-STOREY-0001",
                100.0,
                adjacent_space_ids=("SYNTHETIC-SPACE-0001",),
            ),
        ),
        input_detail_level=BuildingInputDetailLevel.LOD_1,
        simple_envelope=SimpleEnvelopeInput(0.21, 1.01, 24.0),
    )


def _synthetic_zone_specification() -> ZoneModelSpecification:
    return ZoneModelSpecification(
        schema_version="1.0",
        zone_model_id="SYNTHETIC-ZONE-MODEL-0001",
        project_id="SYNTHETIC-PROJECT-0001",
        building_id="SYNTHETIC-BUILDING-0001",
        source_building_version_id="SYNTHETIC-BUILDING-REV-0001",
        input_detail_level=ZoneInputDetailLevel.LOD_1,
        usage_profiles=(UsageProfile("SYNTHETIC-USAGE-0001", "SYNTHETIC-USAGE", 8.0, 18.0, 5, 20.0, 8.0, 5.0),),
        zones=(
            ThermalZone(
                "SYNTHETIC-ZONE-0001",
                "SYNTHETIC-ZONE",
                "SYNTHETIC-USAGE-0001",
                100.0,
                300.0,
                source_space_ids=("SYNTHETIC-SPACE-0001",),
            ),
        ),
    )


def _synthetic_parameter_input_package(technical_handover: ReleasedTechnicalHandover) -> ParameterInputPackage:
    technical_source = parameter_source_reference_from_released_technical_handover(technical_handover)
    sources = (
        _source_reference("ma_building", "SYNTHETIC-BUILDING-0001", "SYNTHETIC-BUILDING-REV-0001", "b" * 64),
        _source_reference("ma_zones", "SYNTHETIC-ZONE-MODEL-0001", "SYNTHETIC-ZONE-MODEL-0001", "c" * 64),
        technical_source,
    )
    source_ids = {source.module_key: source.source_reference_id for source in sources}
    values = tuple(
        ParameterValue(key, key, value, "synthetic", source_ids[module_key])
        for key, value, module_key in (
            ("building_length_m", 10.0, "ma_building"),
            ("building_width_m", 10.0, "ma_building"),
            ("building_height_m", 3.0, "ma_building"),
            ("external_wall_u_value_w_m2k", 0.21, "ma_building"),
            ("window_u_value_w_m2k", 1.01, "ma_building"),
            ("window_area_ratio_percent", 24.0, "ma_building"),
            ("floor_area_m2", 100.0, "ma_building"),
            ("zone_count", 1, "ma_zones"),
            ("zone_floor_area_m2", 100.0, "ma_zones"),
            ("zone_volume_m3", 300.0, "ma_zones"),
            ("technical_system_count", 1, "ma_technical"),
        )
    )
    return ParameterInputPackage(
        package_id="SYNTHETIC-PARAMETER-INPUT-0001",
        package_version="1.0",
        project_id="SYNTHETIC-PROJECT-0001",
        building_id="SYNTHETIC-BUILDING-0001",
        input_detail_level="LOD-1",
        values=values,
        source_references=sources,
        source_snapshot_id="SYNTHETIC-PARAMETER-SNAPSHOT-0001",
        source_snapshot_version="1.0",
        requires_weather=False,
    )


def _source_reference(
    module_key: str, dataset_key: str, version_id: str, content_hash: str
) -> ParameterSourceReference:
    return ParameterSourceReference(
        source_reference_id=f"synthetic:{module_key}",
        module_key=module_key,
        dataset_key=dataset_key,
        version_id=version_id,
        validation_status=ReleaseStatus.RELEASED.value,
        label=f"SYNTHETIC-{module_key}-SOURCE",
        reference_id=dataset_key,
        reference_version=version_id,
        content_hash=content_hash,
    )
