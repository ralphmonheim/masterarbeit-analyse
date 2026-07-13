"""Zentrale Lueftungsanlage fuer ma_technical v2."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import ComponentAvailability, TechnicalInputDetailLevel, TechnicalRepresentationMode
from .metadata import ObjectReference, coerce_enum


@dataclass(frozen=True, slots=True)
class FanConfiguration:
    """Ventilatorparameter ohne Ergebnisgroessen."""

    fan_id: str
    availability: ComponentAvailability | str = ComponentAvailability.UNKNOWN
    design_pressure_pa: float | None = None
    efficiency: float | None = None
    power_method: str = ""
    operation_schedule_reference: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))


@dataclass(frozen=True, slots=True)
class HeatRecoveryConfiguration:
    """Waermerueckgewinnung der AHU."""

    heat_recovery_id: str
    availability: ComponentAvailability | str = ComponentAvailability.UNKNOWN
    efficiency_percent: float | None = None
    operation_schedule_reference: str = ""
    bypass_control: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))


@dataclass(frozen=True, slots=True)
class AirHandlingUnit:
    """Zentrale AHU mit Serviceinterfaces fuer Zuluft und Abluft."""

    ahu_id: str
    availability: ComponentAvailability | str = ComponentAvailability.UNKNOWN
    representation_mode: TechnicalRepresentationMode | str = TechnicalRepresentationMode.ASSUMED
    input_detail_level: TechnicalInputDetailLevel | str = TechnicalInputDetailLevel.LOD_1
    supply_air_temperature_control: str = ""
    supply_fan: FanConfiguration | None = None
    extract_fan: FanConfiguration | None = None
    heat_recovery: HeatRecoveryConfiguration | None = None
    heating_coil: ObjectReference | None = None
    cooling_coil: ObjectReference | None = None
    heating_circuit_reference: ObjectReference | None = None
    cooling_circuit_reference: ObjectReference | None = None
    operation_schedule_reference: str = ""
    supply_air_interface: str = ""
    extract_air_interface: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))
        object.__setattr__(
            self,
            "representation_mode",
            coerce_enum(self.representation_mode, TechnicalRepresentationMode),
        )
        object.__setattr__(
            self,
            "input_detail_level",
            coerce_enum(self.input_detail_level, TechnicalInputDetailLevel),
        )
