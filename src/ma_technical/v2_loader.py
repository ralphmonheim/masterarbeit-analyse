"""Strikter YAML-/Dict-Lader fuer das programmneutrale Technikmodell v2.

Der Lader ist bewusst von dem bestehenden v1-Demo-Lader getrennt.  Er bildet
die serialisierte Form aus :mod:`ma_technical.revisions` explizit auf die
v2-Dataclasses ab und akzeptiert keine unbekannten Felder.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Any, TypeVar

import yaml

from ma_core import InputSource, InputSourceKind, utc_now

from .ahu import AirHandlingUnit, FanConfiguration, HeatRecoveryConfiguration
from .distribution import CoolingDistribution, HeatingCurve, HeatingCurvePoint, HeatingDistribution, PumpConfiguration
from .domestic_hot_water import DomesticHotWaterGeneration, ElectricReheater, ThermalStorage
from .electrical import ElectricalSystem
from .enums import (
    CapacityMode,
    ComponentAvailability,
    HeatingConfigurationMode,
    HeatingDispatchStrategy,
    HeatingFunctionalRole,
    PerformanceMetricType,
    TechnicalInputDetailLevel,
    TechnicalMedium,
    TechnicalRepresentationMode,
    TechnicalServiceType,
)
from .equipment import PhysicalEquipment
from .metadata import ObjectReference, SourceMetadata, TechnicalAssumption, TechnicalValueMetadata
from .plant import (
    CapacityDefinition,
    CoolingGeneration,
    HeatingDispatchConfiguration,
    HeatingFunction,
    HeatingGeneration,
    PerformanceDefinition,
    TechnicalPlant,
)
from .schedules import TechnicalSchedule, TechnicalScheduleRegistry
from .specification import TechnicalModelSchemaVersion, TechnicalModelSpecification
from .topology import TechnicalConnection, TechnicalPort, TechnicalServiceInterface, TechnicalTopology

EnumT = TypeVar("EnumT")


def load_technical_model_specification(path: str | Path) -> TechnicalModelSpecification:
    """Laedt eine einzelne, strikte v2-Spezifikation aus einer YAML-Datei."""
    source_path = Path(path)
    try:
        data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"Technikmodell-YAML ist ungueltig: {source_path}") from error
    return technical_model_specification_from_dict(data)


def technical_model_specification_from_dict(data: Mapping[str, Any]) -> TechnicalModelSpecification:
    """Erzeugt ein :class:`TechnicalModelSpecification` aus einer v2-Nutzlast.

    Die Funktion akzeptiert die von ``revisions._to_payload`` erzeugte Form.
    Pflichtfelder werden vor der Konstruktion geprueft; unbekannte Felder und
    strukturell falsche YAML-Werte werden mit einem ``ValueError`` abgewiesen.
    Fachliche Plausibilitaet ist weiterhin Aufgabe von ``validate_technical_model``.
    """
    value = _mapping(data, "technical model")
    _keys(
        value,
        "technical model",
        required={"schema_version", "technical_model_id", "project_id", "building_reference", "declared_detail_level"},
        optional={
            "equipment_register",
            "heating_distribution_register",
            "cooling_distribution_register",
            "storage_register",
            "domestic_hot_water_register",
            "plant",
            "air_handling_unit",
            "electrical_system",
            "schedules",
            "topology",
            "service_interfaces",
            "assumptions",
            "source_metadata",
        },
    )
    schema_version = _string(value["schema_version"], "schema_version")
    if schema_version != TechnicalModelSchemaVersion.V2.value:
        raise ValueError("schema_version muss exakt '2.0' sein.")
    return TechnicalModelSpecification(
        schema_version=schema_version,
        technical_model_id=_required_text(value["technical_model_id"], "technical_model_id"),
        project_id=_required_text(value["project_id"], "project_id"),
        building_reference=_object_reference(value["building_reference"], "building_reference"),
        declared_detail_level=_enum(value["declared_detail_level"], TechnicalInputDetailLevel, "declared_detail_level"),
        equipment_register=_tuple(value.get("equipment_register", []), "equipment_register", _physical_equipment),
        heating_distribution_register=_tuple(
            value.get("heating_distribution_register", []), "heating_distribution_register", _heating_distribution
        ),
        cooling_distribution_register=_tuple(
            value.get("cooling_distribution_register", []), "cooling_distribution_register", _cooling_distribution
        ),
        storage_register=_tuple(value.get("storage_register", []), "storage_register", _thermal_storage),
        domestic_hot_water_register=_tuple(
            value.get("domestic_hot_water_register", []), "domestic_hot_water_register", _hot_water_generation
        ),
        plant=_optional(value.get("plant"), "plant", _technical_plant),
        air_handling_unit=_optional(value.get("air_handling_unit"), "air_handling_unit", _air_handling_unit),
        electrical_system=_optional(value.get("electrical_system"), "electrical_system", _electrical_system),
        schedules=_schedule_registry(value.get("schedules", {}), "schedules"),
        topology=_topology(value.get("topology", {}), "topology"),
        service_interfaces=_tuple(value.get("service_interfaces", []), "service_interfaces", _service_interface),
        assumptions=_tuple(value.get("assumptions", []), "assumptions", _assumption),
        source_metadata=_source_metadata(value.get("source_metadata", {}), "source_metadata"),
    )


def _physical_equipment(data: Any, path: str) -> PhysicalEquipment:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"equipment_id", "equipment_type"},
        {
            "availability",
            "representation_mode",
            "input_detail_level",
            "product_reference",
            "energy_carrier_reference",
            "supported_services",
            "shared_operating_constraints",
            "electrical_connection_reference",
            "metadata",
        },
    )
    return PhysicalEquipment(
        equipment_id=_required_text(value["equipment_id"], f"{path}.equipment_id"),
        equipment_type=_required_text(value["equipment_type"], f"{path}.equipment_type"),
        availability=_enum_or_default(
            value, "availability", ComponentAvailability, ComponentAvailability.UNKNOWN, path
        ),
        representation_mode=_enum_or_default(
            value, "representation_mode", TechnicalRepresentationMode, TechnicalRepresentationMode.ASSUMED, path
        ),
        input_detail_level=_enum_or_default(
            value, "input_detail_level", TechnicalInputDetailLevel, TechnicalInputDetailLevel.LOD_1, path
        ),
        product_reference=_optional(value.get("product_reference"), f"{path}.product_reference", _object_reference),
        energy_carrier_reference=_optional(
            value.get("energy_carrier_reference"), f"{path}.energy_carrier_reference", _object_reference
        ),
        supported_services=_strings(value.get("supported_services", []), f"{path}.supported_services"),
        shared_operating_constraints=_strings(
            value.get("shared_operating_constraints", []), f"{path}.shared_operating_constraints"
        ),
        electrical_connection_reference=_optional(
            value.get("electrical_connection_reference"), f"{path}.electrical_connection_reference", _object_reference
        ),
        metadata=_optional(value.get("metadata"), f"{path}.metadata", _value_metadata),
    )


def _heating_distribution(data: Any, path: str) -> HeatingDistribution:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"distribution_id"},
        {
            "availability",
            "heating_curve",
            "design_temperature_drop_k",
            "ahu_supply_temperature_c",
            "night_setback_schedule_reference",
            "pump",
            "pump_shutdown_outdoor_temperature_c",
            "service_interface_reference",
        },
    )
    return HeatingDistribution(
        distribution_id=_required_text(value["distribution_id"], f"{path}.distribution_id"),
        availability=_enum_or_default(
            value, "availability", ComponentAvailability, ComponentAvailability.UNKNOWN, path
        ),
        heating_curve=_optional(value.get("heating_curve"), f"{path}.heating_curve", _heating_curve),
        design_temperature_drop_k=_number_or_none(
            value.get("design_temperature_drop_k"), f"{path}.design_temperature_drop_k"
        ),
        ahu_supply_temperature_c=_number_or_none(
            value.get("ahu_supply_temperature_c"), f"{path}.ahu_supply_temperature_c"
        ),
        night_setback_schedule_reference=_string_or_default(value, "night_setback_schedule_reference", "", path),
        pump=_optional(value.get("pump"), f"{path}.pump", _pump),
        pump_shutdown_outdoor_temperature_c=_number_or_none(
            value.get("pump_shutdown_outdoor_temperature_c"), f"{path}.pump_shutdown_outdoor_temperature_c"
        ),
        service_interface_reference=_string_or_default(value, "service_interface_reference", "", path),
    )


def _cooling_distribution(data: Any, path: str) -> CoolingDistribution:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"distribution_id"},
        {
            "availability",
            "room_supply_temperature_c",
            "ahu_supply_temperature_c",
            "design_temperature_rise_k",
            "pump",
            "service_interface_reference",
        },
    )
    return CoolingDistribution(
        distribution_id=_required_text(value["distribution_id"], f"{path}.distribution_id"),
        availability=_enum_or_default(
            value, "availability", ComponentAvailability, ComponentAvailability.UNKNOWN, path
        ),
        room_supply_temperature_c=_number_or_none(
            value.get("room_supply_temperature_c"), f"{path}.room_supply_temperature_c"
        ),
        ahu_supply_temperature_c=_number_or_none(
            value.get("ahu_supply_temperature_c"), f"{path}.ahu_supply_temperature_c"
        ),
        design_temperature_rise_k=_number_or_none(
            value.get("design_temperature_rise_k"), f"{path}.design_temperature_rise_k"
        ),
        pump=_optional(value.get("pump"), f"{path}.pump", _pump),
        service_interface_reference=_string_or_default(value, "service_interface_reference", "", path),
    )


def _heating_curve(data: Any, path: str) -> HeatingCurve:
    value = _mapping(data, path)
    _keys(value, path, {"points"}, {"interpolation_method", "extrapolation_policy"})
    return HeatingCurve(
        _tuple(value["points"], f"{path}.points", _heating_curve_point),
        _string_or_default(value, "interpolation_method", "linear", path),
        _string_or_default(value, "extrapolation_policy", "clamp", path),
    )


def _heating_curve_point(data: Any, path: str) -> HeatingCurvePoint:
    value = _mapping(data, path)
    _keys(value, path, {"outdoor_temperature_c", "supply_temperature_c"}, set())
    return HeatingCurvePoint(
        _number(value["outdoor_temperature_c"], f"{path}.outdoor_temperature_c"),
        _number(value["supply_temperature_c"], f"{path}.supply_temperature_c"),
    )


def _pump(data: Any, path: str) -> PumpConfiguration:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"pump_id"},
        {
            "availability",
            "power_method",
            "operation_schedule_reference",
            "maximum_mass_flow_kg_s",
            "specific_pump_power_w_per_l_s",
            "design_pressure_pa",
            "efficiency",
            "energy_meter_reference",
            "model_specific_coefficients",
        },
    )
    return PumpConfiguration(
        pump_id=_required_text(value["pump_id"], f"{path}.pump_id"),
        availability=_enum_or_default(
            value, "availability", ComponentAvailability, ComponentAvailability.UNKNOWN, path
        ),
        power_method=_string_or_default(value, "power_method", "", path),
        operation_schedule_reference=_string_or_default(value, "operation_schedule_reference", "", path),
        maximum_mass_flow_kg_s=_number_or_none(value.get("maximum_mass_flow_kg_s"), f"{path}.maximum_mass_flow_kg_s"),
        specific_pump_power_w_per_l_s=_number_or_none(
            value.get("specific_pump_power_w_per_l_s"), f"{path}.specific_pump_power_w_per_l_s"
        ),
        design_pressure_pa=_number_or_none(value.get("design_pressure_pa"), f"{path}.design_pressure_pa"),
        efficiency=_number_or_none(value.get("efficiency"), f"{path}.efficiency"),
        energy_meter_reference=_string_or_default(value, "energy_meter_reference", "", path),
        model_specific_coefficients=_number_mapping_or_none(
            value.get("model_specific_coefficients"), f"{path}.model_specific_coefficients"
        ),
    )


def _thermal_storage(data: Any, path: str) -> ThermalStorage:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"storage_id", "storage_type"},
        {
            "availability",
            "volume_m3",
            "storage_medium",
            "insulation_u_value_w_m2k",
            "number_of_model_layers",
            "electric_reheater",
            "connections",
            "adapter_extensions",
        },
    )
    return ThermalStorage(
        storage_id=_required_text(value["storage_id"], f"{path}.storage_id"),
        storage_type=_required_text(value["storage_type"], f"{path}.storage_type"),
        availability=_enum_or_default(
            value, "availability", ComponentAvailability, ComponentAvailability.UNKNOWN, path
        ),
        volume_m3=_number_or_none(value.get("volume_m3"), f"{path}.volume_m3"),
        storage_medium=_string_or_default(value, "storage_medium", "", path),
        insulation_u_value_w_m2k=_number_or_none(
            value.get("insulation_u_value_w_m2k"), f"{path}.insulation_u_value_w_m2k"
        ),
        number_of_model_layers=_integer_or_none(value.get("number_of_model_layers"), f"{path}.number_of_model_layers"),
        electric_reheater=_optional(value.get("electric_reheater"), f"{path}.electric_reheater", _electric_reheater),
        connections=_strings(value.get("connections", []), f"{path}.connections"),
        adapter_extensions=_plain_mapping_or_none(value.get("adapter_extensions"), f"{path}.adapter_extensions"),
    )


def _electric_reheater(data: Any, path: str) -> ElectricReheater:
    value = _mapping(data, path)
    _keys(value, path, {"reheater_id"}, {"availability", "capacity_kw", "control"})
    return ElectricReheater(
        _required_text(value["reheater_id"], f"{path}.reheater_id"),
        _enum_or_default(value, "availability", ComponentAvailability, ComponentAvailability.UNKNOWN, path),
        _number_or_none(value.get("capacity_kw"), f"{path}.capacity_kw"),
        _string_or_default(value, "control", "", path),
    )


def _hot_water_generation(data: Any, path: str) -> DomesticHotWaterGeneration:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"generation_id", "generation_mode"},
        {
            "heating_function_reference",
            "separate_generator",
            "storage",
            "circulation",
            "control",
            "service_interface_reference",
        },
    )
    return DomesticHotWaterGeneration(
        generation_id=_required_text(value["generation_id"], f"{path}.generation_id"),
        generation_mode=_required_text(value["generation_mode"], f"{path}.generation_mode"),
        heating_function_reference=_optional(
            value.get("heating_function_reference"), f"{path}.heating_function_reference", _object_reference
        ),
        separate_generator=_optional(value.get("separate_generator"), f"{path}.separate_generator", _object_reference),
        storage=_optional(value.get("storage"), f"{path}.storage", _thermal_storage),
        circulation=_string_or_default(value, "circulation", "", path),
        control=_string_or_default(value, "control", "", path),
        service_interface_reference=_string_or_default(value, "service_interface_reference", "", path),
    )


def _technical_plant(data: Any, path: str) -> TechnicalPlant:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"plant_id"},
        {"heating_generation", "cooling_generation", "heat_storage_reference", "cold_storage_reference"},
    )
    return TechnicalPlant(
        _required_text(value["plant_id"], f"{path}.plant_id"),
        _optional(value.get("heating_generation"), f"{path}.heating_generation", _heating_generation),
        _optional(value.get("cooling_generation"), f"{path}.cooling_generation", _cooling_generation),
        _optional(value.get("heat_storage_reference"), f"{path}.heat_storage_reference", _object_reference),
        _optional(value.get("cold_storage_reference"), f"{path}.cold_storage_reference", _object_reference),
    )


def _heating_generation(data: Any, path: str) -> HeatingGeneration:
    value = _mapping(data, path)
    _keys(value, path, {"configuration_mode"}, {"base_heating", "top_up_heating", "dispatch"})
    return HeatingGeneration(
        _enum(value["configuration_mode"], HeatingConfigurationMode, f"{path}.configuration_mode"),
        _optional(value.get("base_heating"), f"{path}.base_heating", _heating_function),
        _optional(value.get("top_up_heating"), f"{path}.top_up_heating", _heating_function),
        _optional(value.get("dispatch"), f"{path}.dispatch", _heating_dispatch),
    )


def _heating_function(data: Any, path: str) -> HeatingFunction:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"function_id", "slot", "functional_role", "capacity"},
        {
            "physical_equipment_reference",
            "availability",
            "representation_mode",
            "performance",
            "energy_carrier_reference",
            "meter_assignments",
            "supported_services",
            "operating_limits",
            "control",
            "schedule_reference",
        },
    )
    return HeatingFunction(
        function_id=_required_text(value["function_id"], f"{path}.function_id"),
        slot=_required_text(value["slot"], f"{path}.slot"),
        functional_role=_enum(value["functional_role"], HeatingFunctionalRole, f"{path}.functional_role"),
        capacity=_capacity(value["capacity"], f"{path}.capacity"),
        physical_equipment_reference=_optional(
            value.get("physical_equipment_reference"), f"{path}.physical_equipment_reference", _object_reference
        ),
        availability=_enum_or_default(
            value, "availability", ComponentAvailability, ComponentAvailability.PLANNED, path
        ),
        representation_mode=_enum_or_default(
            value, "representation_mode", TechnicalRepresentationMode, TechnicalRepresentationMode.ASSUMED, path
        ),
        performance=_optional(value.get("performance"), f"{path}.performance", _performance),
        energy_carrier_reference=_optional(
            value.get("energy_carrier_reference"), f"{path}.energy_carrier_reference", _object_reference
        ),
        meter_assignments=_strings(value.get("meter_assignments", []), f"{path}.meter_assignments"),
        supported_services=_strings(value.get("supported_services", []), f"{path}.supported_services"),
        operating_limits=_strings(value.get("operating_limits", []), f"{path}.operating_limits"),
        control=_string_or_default(value, "control", "", path),
        schedule_reference=_string_or_default(value, "schedule_reference", "", path),
    )


def _cooling_generation(data: Any, path: str) -> CoolingGeneration:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"function_id", "capacity"},
        {
            "physical_equipment_reference",
            "availability",
            "representation_mode",
            "performance",
            "energy_carrier_reference",
            "meter_assignments",
            "operating_limits",
            "control",
            "schedule_reference",
        },
    )
    return CoolingGeneration(
        function_id=_required_text(value["function_id"], f"{path}.function_id"),
        capacity=_capacity(value["capacity"], f"{path}.capacity"),
        physical_equipment_reference=_optional(
            value.get("physical_equipment_reference"), f"{path}.physical_equipment_reference", _object_reference
        ),
        availability=_enum_or_default(
            value, "availability", ComponentAvailability, ComponentAvailability.PLANNED, path
        ),
        representation_mode=_enum_or_default(
            value, "representation_mode", TechnicalRepresentationMode, TechnicalRepresentationMode.ASSUMED, path
        ),
        performance=_optional(value.get("performance"), f"{path}.performance", _performance),
        energy_carrier_reference=_optional(
            value.get("energy_carrier_reference"), f"{path}.energy_carrier_reference", _object_reference
        ),
        meter_assignments=_strings(value.get("meter_assignments", []), f"{path}.meter_assignments"),
        operating_limits=_strings(value.get("operating_limits", []), f"{path}.operating_limits"),
        control=_string_or_default(value, "control", "", path),
        schedule_reference=_string_or_default(value, "schedule_reference", "", path),
    )


def _capacity(data: Any, path: str) -> CapacityDefinition:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"mode"},
        {
            "nominal_capacity_kw",
            "maximum_capacity_kw",
            "minimum_capacity_kw",
            "reference_conditions",
            "product_reference",
            "source_metadata",
        },
    )
    return CapacityDefinition(
        _enum(value["mode"], CapacityMode, f"{path}.mode"),
        _number_or_none(value.get("nominal_capacity_kw"), f"{path}.nominal_capacity_kw"),
        _number_or_none(value.get("maximum_capacity_kw"), f"{path}.maximum_capacity_kw"),
        _number_or_none(value.get("minimum_capacity_kw"), f"{path}.minimum_capacity_kw"),
        _string_or_default(value, "reference_conditions", "", path),
        _optional(value.get("product_reference"), f"{path}.product_reference", _object_reference),
        _optional(value.get("source_metadata"), f"{path}.source_metadata", _source_metadata),
    )


def _performance(data: Any, path: str) -> PerformanceDefinition:
    value = _mapping(data, path)
    _keys(value, path, {"metric_type"}, {"value", "reference_conditions", "source_metadata"})
    return PerformanceDefinition(
        _enum(value["metric_type"], PerformanceMetricType, f"{path}.metric_type"),
        _number_or_none(value.get("value"), f"{path}.value"),
        _string_or_default(value, "reference_conditions", "", path),
        _optional(value.get("source_metadata"), f"{path}.source_metadata", _source_metadata),
    )


def _heating_dispatch(data: Any, path: str) -> HeatingDispatchConfiguration:
    value = _mapping(data, path)
    _keys(value, path, {"strategy"}, {"notes"})
    return HeatingDispatchConfiguration(
        _enum(value["strategy"], HeatingDispatchStrategy, f"{path}.strategy"),
        _string_or_default(value, "notes", "", path),
    )


def _air_handling_unit(data: Any, path: str) -> AirHandlingUnit:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"ahu_id"},
        {
            "availability",
            "representation_mode",
            "input_detail_level",
            "supply_air_temperature_control",
            "supply_fan",
            "extract_fan",
            "heat_recovery",
            "heating_coil",
            "cooling_coil",
            "heating_circuit_reference",
            "cooling_circuit_reference",
            "operation_schedule_reference",
            "supply_air_interface",
            "extract_air_interface",
        },
    )
    return AirHandlingUnit(
        ahu_id=_required_text(value["ahu_id"], f"{path}.ahu_id"),
        availability=_enum_or_default(
            value, "availability", ComponentAvailability, ComponentAvailability.UNKNOWN, path
        ),
        representation_mode=_enum_or_default(
            value, "representation_mode", TechnicalRepresentationMode, TechnicalRepresentationMode.ASSUMED, path
        ),
        input_detail_level=_enum_or_default(
            value, "input_detail_level", TechnicalInputDetailLevel, TechnicalInputDetailLevel.LOD_1, path
        ),
        supply_air_temperature_control=_string_or_default(value, "supply_air_temperature_control", "", path),
        supply_fan=_optional(value.get("supply_fan"), f"{path}.supply_fan", _fan),
        extract_fan=_optional(value.get("extract_fan"), f"{path}.extract_fan", _fan),
        heat_recovery=_optional(value.get("heat_recovery"), f"{path}.heat_recovery", _heat_recovery),
        heating_coil=_optional(value.get("heating_coil"), f"{path}.heating_coil", _object_reference),
        cooling_coil=_optional(value.get("cooling_coil"), f"{path}.cooling_coil", _object_reference),
        heating_circuit_reference=_optional(
            value.get("heating_circuit_reference"), f"{path}.heating_circuit_reference", _object_reference
        ),
        cooling_circuit_reference=_optional(
            value.get("cooling_circuit_reference"), f"{path}.cooling_circuit_reference", _object_reference
        ),
        operation_schedule_reference=_string_or_default(value, "operation_schedule_reference", "", path),
        supply_air_interface=_string_or_default(value, "supply_air_interface", "", path),
        extract_air_interface=_string_or_default(value, "extract_air_interface", "", path),
    )


def _fan(data: Any, path: str) -> FanConfiguration:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"fan_id"},
        {"availability", "design_pressure_pa", "efficiency", "power_method", "operation_schedule_reference"},
    )
    return FanConfiguration(
        _required_text(value["fan_id"], f"{path}.fan_id"),
        _enum_or_default(value, "availability", ComponentAvailability, ComponentAvailability.UNKNOWN, path),
        _number_or_none(value.get("design_pressure_pa"), f"{path}.design_pressure_pa"),
        _number_or_none(value.get("efficiency"), f"{path}.efficiency"),
        _string_or_default(value, "power_method", "", path),
        _string_or_default(value, "operation_schedule_reference", "", path),
    )


def _heat_recovery(data: Any, path: str) -> HeatRecoveryConfiguration:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"heat_recovery_id"},
        {"availability", "efficiency_percent", "operation_schedule_reference", "bypass_control"},
    )
    return HeatRecoveryConfiguration(
        _required_text(value["heat_recovery_id"], f"{path}.heat_recovery_id"),
        _enum_or_default(value, "availability", ComponentAvailability, ComponentAvailability.UNKNOWN, path),
        _number_or_none(value.get("efficiency_percent"), f"{path}.efficiency_percent"),
        _string_or_default(value, "operation_schedule_reference", "", path),
        _string_or_default(value, "bypass_control", "", path),
    )


def _electrical_system(data: Any, path: str) -> ElectricalSystem:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"electrical_system_id"},
        {
            "availability",
            "grid_connection",
            "meters",
            "photovoltaic_system",
            "wind_turbine",
            "battery_system",
            "consumer_references",
        },
    )
    return ElectricalSystem(
        _required_text(value["electrical_system_id"], f"{path}.electrical_system_id"),
        _enum_or_default(value, "availability", ComponentAvailability, ComponentAvailability.UNKNOWN, path),
        _string_or_default(value, "grid_connection", "", path),
        _strings(value.get("meters", []), f"{path}.meters"),
        _optional(value.get("photovoltaic_system"), f"{path}.photovoltaic_system", _object_reference),
        _optional(value.get("wind_turbine"), f"{path}.wind_turbine", _object_reference),
        _optional(value.get("battery_system"), f"{path}.battery_system", _object_reference),
        _tuple(value.get("consumer_references", []), f"{path}.consumer_references", _object_reference),
    )


def _schedule_registry(data: Any, path: str) -> TechnicalScheduleRegistry:
    value = _mapping(data, path)
    _keys(value, path, set(), {"schedules", "registry_revision"})
    return TechnicalScheduleRegistry(
        _tuple(value.get("schedules", []), f"{path}.schedules", _schedule),
        _string_or_default(value, "registry_revision", "", path),
    )


def _schedule(data: Any, path: str) -> TechnicalSchedule:
    value = _mapping(data, path)
    _keys(value, path, {"schedule_id", "name", "schedule_type"}, {"values_reference", "notes"})
    return TechnicalSchedule(
        _required_text(value["schedule_id"], f"{path}.schedule_id"),
        _required_text(value["name"], f"{path}.name"),
        _required_text(value["schedule_type"], f"{path}.schedule_type"),
        _string_or_default(value, "values_reference", "", path),
        _string_or_default(value, "notes", "", path),
    )


def _topology(data: Any, path: str) -> TechnicalTopology:
    value = _mapping(data, path)
    _keys(value, path, set(), {"ports", "connections", "generation_metadata"})
    return TechnicalTopology(
        _tuple(value.get("ports", []), f"{path}.ports", _port),
        _tuple(value.get("connections", []), f"{path}.connections", _connection),
        _string_or_default(value, "generation_metadata", "", path),
    )


def _port(data: Any, path: str) -> TechnicalPort:
    value = _mapping(data, path)
    _keys(value, path, {"port_id", "owner_object_reference", "port_type", "medium", "direction", "service_type"}, set())
    return TechnicalPort(
        _required_text(value["port_id"], f"{path}.port_id"),
        _object_reference(value["owner_object_reference"], f"{path}.owner_object_reference"),
        _required_text(value["port_type"], f"{path}.port_type"),
        _enum(value["medium"], TechnicalMedium, f"{path}.medium"),
        _required_text(value["direction"], f"{path}.direction"),
        _enum(value["service_type"], TechnicalServiceType, f"{path}.service_type"),
    )


def _connection(data: Any, path: str) -> TechnicalConnection:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"connection_id", "source_port_reference", "target_port_reference", "medium", "connection_role"},
        {"generated_from_user_relation"},
    )
    return TechnicalConnection(
        _required_text(value["connection_id"], f"{path}.connection_id"),
        _object_reference(value["source_port_reference"], f"{path}.source_port_reference"),
        _object_reference(value["target_port_reference"], f"{path}.target_port_reference"),
        _enum(value["medium"], TechnicalMedium, f"{path}.medium"),
        _required_text(value["connection_role"], f"{path}.connection_role"),
        _string_or_default(value, "generated_from_user_relation", "", path),
    )


def _service_interface(data: Any, path: str) -> TechnicalServiceInterface:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"interface_id", "service_type", "source_system_reference", "medium"},
        {
            "supply_temperature_definition",
            "return_temperature_definition",
            "capacity_mode",
            "compatible_terminal_types",
            "availability",
            "revision_id",
            "content_hash",
        },
    )
    return TechnicalServiceInterface(
        interface_id=_required_text(value["interface_id"], f"{path}.interface_id"),
        service_type=_enum(value["service_type"], TechnicalServiceType, f"{path}.service_type"),
        source_system_reference=_object_reference(value["source_system_reference"], f"{path}.source_system_reference"),
        medium=_enum(value["medium"], TechnicalMedium, f"{path}.medium"),
        supply_temperature_definition=_string_or_default(value, "supply_temperature_definition", "", path),
        return_temperature_definition=_string_or_default(value, "return_temperature_definition", "", path),
        capacity_mode=_enum_or_default(value, "capacity_mode", CapacityMode, CapacityMode.ASSUMED, path),
        compatible_terminal_types=_strings(
            value.get("compatible_terminal_types", []), f"{path}.compatible_terminal_types"
        ),
        availability=_enum_or_default(
            value, "availability", ComponentAvailability, ComponentAvailability.PLANNED, path
        ),
        revision_id=_string_or_default(value, "revision_id", "", path),
        content_hash=_string_or_default(value, "content_hash", "", path),
    )


def _assumption(data: Any, path: str) -> TechnicalAssumption:
    value = _mapping(data, path)
    _keys(value, path, {"assumption_id", "text"}, {"location"})
    location = value.get("location")
    return TechnicalAssumption(
        _required_text(value["assumption_id"], f"{path}.assumption_id"),
        _required_text(value["text"], f"{path}.text"),
        None if location is None else _string(location, f"{path}.location"),
    )


def _object_reference(data: Any, path: str) -> ObjectReference:
    value = _mapping(data, path)
    _keys(value, path, {"object_id"}, {"revision_id", "content_hash", "object_type"})
    return ObjectReference(
        _required_text(value["object_id"], f"{path}.object_id"),
        _string_or_default(value, "revision_id", "", path),
        _string_or_default(value, "content_hash", "", path),
        _string_or_default(value, "object_type", "", path),
    )


def _source_metadata(data: Any, path: str) -> SourceMetadata:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        set(),
        {"source_type", "source_reference", "source_version", "imported_or_entered_at", "notes", "input_source"},
    )
    timestamp = value.get("imported_or_entered_at")
    return SourceMetadata(
        _string_or_default(value, "source_type", "manual", path),
        _string_or_default(value, "source_reference", "", path),
        _string_or_default(value, "source_version", "", path),
        _datetime(timestamp, f"{path}.imported_or_entered_at") if timestamp is not None else utc_now(),
        _string_or_default(value, "notes", "", path),
        _optional(value.get("input_source"), f"{path}.input_source", _input_source),
    )


def _input_source(data: Any, path: str) -> InputSource:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        {"module_key", "source_kind", "data_format", "source_id"},
        {"source_path", "adapter_key", "is_template", "file_size_bytes", "sha256", "loaded_at"},
    )
    source_path = value.get("source_path")
    arguments: dict[str, Any] = {
        "module_key": _required_text(value["module_key"], f"{path}.module_key"),
        "source_kind": _enum(value["source_kind"], InputSourceKind, f"{path}.source_kind"),
        "data_format": _required_text(value["data_format"], f"{path}.data_format"),
        "source_path": None if source_path is None else Path(_string(source_path, f"{path}.source_path")),
        "adapter_key": _optional(value.get("adapter_key"), f"{path}.adapter_key", _string),
        "is_template": _boolean_or_default(value, "is_template", False, path),
        "file_size_bytes": _integer_or_none(value.get("file_size_bytes"), f"{path}.file_size_bytes"),
        "sha256": _optional(value.get("sha256"), f"{path}.sha256", _string),
        "source_id": _required_text(value["source_id"], f"{path}.source_id"),
        "loaded_at": _datetime(value["loaded_at"], f"{path}.loaded_at") if "loaded_at" in value else utc_now(),
    }
    return InputSource(**arguments)


def _value_metadata(data: Any, path: str) -> TechnicalValueMetadata:
    value = _mapping(data, path)
    _keys(
        value,
        path,
        set(),
        {"source", "confirmation_status", "variability", "assumption_reference", "decision_reference"},
    )
    return TechnicalValueMetadata(
        _optional(value.get("source"), f"{path}.source", _source_metadata),
        _string_or_default(value, "confirmation_status", "unconfirmed", path),
        _string_or_default(value, "variability", "fixed", path),
        _string_or_default(value, "assumption_reference", "", path),
        _string_or_default(value, "decision_reference", "", path),
    )


def _mapping(data: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(data, Mapping) or not all(isinstance(key, str) for key in data):
        raise ValueError(f"{path} muss eine Zuordnung mit String-Schluesseln sein.")
    return data


def _keys(value: Mapping[str, Any], path: str, required: set[str], optional: set[str]) -> None:
    missing = required - value.keys()
    unknown = value.keys() - required - optional
    if missing:
        raise ValueError(f"{path} fehlen Pflichtfelder: {', '.join(sorted(missing))}.")
    if unknown:
        raise ValueError(f"{path} enthaelt unbekannte Felder: {', '.join(sorted(unknown))}.")


def _string(value: Any, path: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{path} muss ein String sein.")
    return value


def _required_text(value: Any, path: str) -> str:
    """Liest ein verpflichtendes Textfeld ohne leere Kennungen oder Namen zuzulassen."""
    text = _string(value, path)
    if not text.strip():
        raise ValueError(f"{path} darf nicht leer sein.")
    return text


def _string_or_default(value: Mapping[str, Any], key: str, default: str, path: str) -> str:
    return default if key not in value else _string(value[key], f"{path}.{key}")


def _number(value: Any, path: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{path} muss eine Zahl sein.")
    return float(value)


def _number_or_none(value: Any, path: str) -> float | None:
    return None if value is None else _number(value, path)


def _integer_or_none(value: Any, path: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{path} muss eine Ganzzahl sein.")
    return value


def _boolean_or_default(value: Mapping[str, Any], key: str, default: bool, path: str) -> bool:
    if key not in value:
        return default
    if not isinstance(value[key], bool):
        raise ValueError(f"{path}.{key} muss ein Boolean sein.")
    return value[key]


def _enum(value: Any, enum_type: type[EnumT], path: str) -> EnumT:
    try:
        return enum_type(_string(value, path))
    except ValueError as error:
        raise ValueError(f"{path} enthaelt keinen bekannten Wert: {value!r}.") from error


def _enum_or_default(value: Mapping[str, Any], key: str, enum_type: type[EnumT], default: EnumT, path: str) -> EnumT:
    return default if key not in value else _enum(value[key], enum_type, f"{path}.{key}")


def _tuple(data: Any, path: str, factory: Any) -> tuple[Any, ...]:
    if not isinstance(data, list):
        raise ValueError(f"{path} muss eine YAML-Liste sein.")
    return tuple(factory(item, f"{path}[{index}]") for index, item in enumerate(data))


def _strings(data: Any, path: str) -> tuple[str, ...]:
    if not isinstance(data, list):
        raise ValueError(f"{path} muss eine YAML-Liste sein.")
    return tuple(_string(item, f"{path}[{index}]") for index, item in enumerate(data))


def _optional(data: Any, path: str, factory: Any) -> Any:
    return None if data is None else factory(data, path)


def _datetime(value: Any, path: str) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    else:
        try:
            parsed = datetime.fromisoformat(_string(value, path))
        except ValueError as error:
            raise ValueError(f"{path} muss ein ISO-8601-Zeitpunkt sein.") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{path} muss eine Zeitzone enthalten.")
    return parsed


def _number_mapping_or_none(data: Any, path: str) -> dict[str, float] | None:
    if data is None:
        return None
    return {key: _number(value, f"{path}.{key}") for key, value in _mapping(data, path).items()}


def _plain_mapping_or_none(data: Any, path: str) -> dict[str, object] | None:
    if data is None:
        return None
    return {key: _plain_value(value, f"{path}.{key}") for key, value in _mapping(data, path).items()}


def _plain_value(value: Any, path: str) -> object:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_plain_value(item, f"{path}[]") for item in value]
    if isinstance(value, Mapping):
        return {key: _plain_value(item, f"{path}.{key}") for key, item in _mapping(value, path).items()}
    raise ValueError(f"{path} enthaelt keinen YAML-Grundwert.")
