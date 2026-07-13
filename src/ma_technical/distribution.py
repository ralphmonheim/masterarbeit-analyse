"""Verteilungen, Heizkurven und Pumpen fuer ma_technical v2."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import ComponentAvailability
from .metadata import coerce_enum


@dataclass(frozen=True, slots=True)
class HeatingCurvePoint:
    """Stuetzpunkt einer Heizkurve."""

    outdoor_temperature_c: float
    supply_temperature_c: float


@dataclass(frozen=True, slots=True)
class HeatingCurve:
    """Einfache Heizkurve mit dokumentierter Interpolation."""

    points: tuple[HeatingCurvePoint, ...]
    interpolation_method: str = "linear"
    extrapolation_policy: str = "clamp"

    def __post_init__(self) -> None:
        object.__setattr__(self, "points", tuple(self.points))


@dataclass(frozen=True, slots=True)
class PumpConfiguration:
    """Pumpenparameter ohne IDA-spezifische Formeln."""

    pump_id: str
    availability: ComponentAvailability | str = ComponentAvailability.UNKNOWN
    power_method: str = ""
    operation_schedule_reference: str = ""
    maximum_mass_flow_kg_s: float | None = None
    specific_pump_power_w_per_l_s: float | None = None
    design_pressure_pa: float | None = None
    efficiency: float | None = None
    energy_meter_reference: str = ""
    model_specific_coefficients: dict[str, float] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))
        if self.model_specific_coefficients is not None:
            object.__setattr__(self, "model_specific_coefficients", dict(self.model_specific_coefficients))


@dataclass(frozen=True, slots=True)
class HeatingDistribution:
    """Heizungsverteilung und ihr Serviceinterface."""

    distribution_id: str
    availability: ComponentAvailability | str = ComponentAvailability.UNKNOWN
    heating_curve: HeatingCurve | None = None
    design_temperature_drop_k: float | None = None
    ahu_supply_temperature_c: float | None = None
    night_setback_schedule_reference: str = ""
    pump: PumpConfiguration | None = None
    pump_shutdown_outdoor_temperature_c: float | None = None
    service_interface_reference: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))


@dataclass(frozen=True, slots=True)
class CoolingDistribution:
    """Kaelteverteilung und ihr Serviceinterface."""

    distribution_id: str
    availability: ComponentAvailability | str = ComponentAvailability.UNKNOWN
    room_supply_temperature_c: float | None = None
    ahu_supply_temperature_c: float | None = None
    design_temperature_rise_k: float | None = None
    pump: PumpConfiguration | None = None
    service_interface_reference: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))
