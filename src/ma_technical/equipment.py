"""Physische Geraete fuer ma_technical v2."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import ComponentAvailability, TechnicalInputDetailLevel, TechnicalRepresentationMode
from .metadata import ObjectReference, TechnicalValueMetadata, coerce_enum, tuple_of_strings


@dataclass(frozen=True, slots=True)
class PhysicalEquipment:
    """Physisches Geraet, das von einer oder mehreren technischen Funktionen genutzt werden kann."""

    equipment_id: str
    equipment_type: str
    availability: ComponentAvailability | str = ComponentAvailability.UNKNOWN
    representation_mode: TechnicalRepresentationMode | str = TechnicalRepresentationMode.ASSUMED
    input_detail_level: TechnicalInputDetailLevel | str = TechnicalInputDetailLevel.LOD_1
    product_reference: ObjectReference | None = None
    energy_carrier_reference: ObjectReference | None = None
    supported_services: tuple[str, ...] = ()
    shared_operating_constraints: tuple[str, ...] = ()
    electrical_connection_reference: ObjectReference | None = None
    metadata: TechnicalValueMetadata | None = None

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
        object.__setattr__(self, "supported_services", tuple_of_strings(self.supported_services))
        object.__setattr__(
            self,
            "shared_operating_constraints",
            tuple_of_strings(self.shared_operating_constraints),
        )
