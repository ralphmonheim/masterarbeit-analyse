"""Elektrisches System fuer ma_technical v2."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import ComponentAvailability
from .metadata import ObjectReference, coerce_enum, tuple_of_strings


@dataclass(frozen=True, slots=True)
class ElectricalSystem:
    """Elektrische Infrastruktur und optionale Erzeuger/Speicher."""

    electrical_system_id: str
    availability: ComponentAvailability | str = ComponentAvailability.UNKNOWN
    grid_connection: str = ""
    meters: tuple[str, ...] = ()
    photovoltaic_system: ObjectReference | None = None
    wind_turbine: ObjectReference | None = None
    battery_system: ObjectReference | None = None
    consumer_references: tuple[ObjectReference, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))
        object.__setattr__(self, "meters", tuple_of_strings(self.meters))
        object.__setattr__(self, "consumer_references", tuple(self.consumer_references))
