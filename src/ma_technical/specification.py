"""Hauptobjekt fuer ma_technical Schema v2."""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from enum import StrEnum
from typing import Any

from .ahu import AirHandlingUnit
from .distribution import CoolingDistribution, HeatingDistribution
from .domestic_hot_water import DomesticHotWaterGeneration, ThermalStorage
from .electrical import ElectricalSystem
from .enums import TechnicalInputDetailLevel
from .equipment import PhysicalEquipment
from .metadata import ObjectReference, SourceMetadata, TechnicalAssumption, coerce_enum
from .plant import TechnicalPlant
from .schedules import TechnicalScheduleRegistry
from .topology import TechnicalServiceInterface, TechnicalTopology


class TechnicalModelSchemaVersion(StrEnum):
    """Version des ma_technical-Zielschemas."""

    V2 = "2.0"


@dataclass(frozen=True, slots=True)
class TechnicalModelSpecification:
    """Programmneutrales Zielmodell fuer zentrale technische Systeme."""

    schema_version: str
    technical_model_id: str
    project_id: str
    building_reference: ObjectReference
    declared_detail_level: TechnicalInputDetailLevel | str
    equipment_register: tuple[PhysicalEquipment, ...] = ()
    heating_distribution_register: tuple[HeatingDistribution, ...] = ()
    cooling_distribution_register: tuple[CoolingDistribution, ...] = ()
    storage_register: tuple[ThermalStorage, ...] = ()
    domestic_hot_water_register: tuple[DomesticHotWaterGeneration, ...] = ()
    plant: TechnicalPlant | None = None
    air_handling_unit: AirHandlingUnit | None = None
    electrical_system: ElectricalSystem | None = None
    schedules: TechnicalScheduleRegistry = field(default_factory=TechnicalScheduleRegistry)
    topology: TechnicalTopology = field(default_factory=TechnicalTopology)
    service_interfaces: tuple[TechnicalServiceInterface, ...] = ()
    assumptions: tuple[TechnicalAssumption, ...] = ()
    source_metadata: SourceMetadata = field(default_factory=SourceMetadata)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "declared_detail_level",
            coerce_enum(self.declared_detail_level, TechnicalInputDetailLevel),
        )
        object.__setattr__(self, "equipment_register", tuple(self.equipment_register))
        object.__setattr__(self, "heating_distribution_register", tuple(self.heating_distribution_register))
        object.__setattr__(self, "cooling_distribution_register", tuple(self.cooling_distribution_register))
        object.__setattr__(self, "storage_register", tuple(self.storage_register))
        object.__setattr__(self, "domestic_hot_water_register", tuple(self.domestic_hot_water_register))
        object.__setattr__(self, "service_interfaces", tuple(self.service_interfaces))
        object.__setattr__(self, "assumptions", tuple(self.assumptions))

    def object_id_locations(self) -> tuple[tuple[str, str], ...]:
        """Liefert Objekt-IDs mit Fundstelle fuer spaetere Strukturvalidierung."""
        return tuple((object_id, location) for object_id, location in _object_id_locations(self, "") if object_id)


def _object_id_locations(value: Any, location: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    if isinstance(value, ObjectReference):
        return rows
    if is_dataclass(value):
        for field in fields(value):
            field_value = getattr(value, field.name)
            field_location = f"{location}.{field.name}" if location else field.name
            if field.name.endswith("_id") and isinstance(field_value, str) and field_value:
                rows.append((field_value, field_location))
            rows.extend(_object_id_locations(field_value, field_location))
        return rows
    if isinstance(value, tuple):
        for index, item in enumerate(value):
            rows.extend(_object_id_locations(item, f"{location}.{index}"))
    return rows
