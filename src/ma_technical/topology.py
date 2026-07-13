"""Topologie und Serviceinterfaces fuer ma_technical v2."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import CapacityMode, ComponentAvailability, TechnicalMedium, TechnicalServiceType
from .metadata import ObjectReference, coerce_enum, tuple_of_strings


@dataclass(frozen=True, slots=True)
class TechnicalPort:
    """Port eines technischen Objekts fuer gefuehrte Verschaltung."""

    port_id: str
    owner_object_reference: ObjectReference
    port_type: str
    medium: TechnicalMedium | str
    direction: str
    service_type: TechnicalServiceType | str

    def __post_init__(self) -> None:
        object.__setattr__(self, "medium", coerce_enum(self.medium, TechnicalMedium))
        object.__setattr__(self, "service_type", coerce_enum(self.service_type, TechnicalServiceType))


@dataclass(frozen=True, slots=True)
class TechnicalConnection:
    """Verbindung zwischen zwei Ports."""

    connection_id: str
    source_port_reference: ObjectReference
    target_port_reference: ObjectReference
    medium: TechnicalMedium | str
    connection_role: str
    generated_from_user_relation: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "medium", coerce_enum(self.medium, TechnicalMedium))


@dataclass(frozen=True, slots=True)
class TechnicalTopology:
    """Sammlung der manuell gefuehrten Ports und Verbindungen."""

    ports: tuple[TechnicalPort, ...] = ()
    connections: tuple[TechnicalConnection, ...] = ()
    generation_metadata: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "ports", tuple(self.ports))
        object.__setattr__(self, "connections", tuple(self.connections))


@dataclass(frozen=True, slots=True)
class TechnicalServiceInterface:
    """Freigegebene Schnittstelle von ma_technical zu ma_zones."""

    interface_id: str
    service_type: TechnicalServiceType | str
    source_system_reference: ObjectReference
    medium: TechnicalMedium | str
    supply_temperature_definition: str = ""
    return_temperature_definition: str = ""
    capacity_mode: CapacityMode | str = CapacityMode.ASSUMED
    compatible_terminal_types: tuple[str, ...] = ()
    availability: ComponentAvailability | str = ComponentAvailability.PLANNED
    revision_id: str = ""
    content_hash: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "service_type", coerce_enum(self.service_type, TechnicalServiceType))
        object.__setattr__(self, "medium", coerce_enum(self.medium, TechnicalMedium))
        object.__setattr__(self, "capacity_mode", coerce_enum(self.capacity_mode, CapacityMode))
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))
        object.__setattr__(self, "compatible_terminal_types", tuple_of_strings(self.compatible_terminal_types))
