"""Speicher und Trinkwarmwasser fuer ma_technical v2."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import ComponentAvailability
from .metadata import ObjectReference, coerce_enum, tuple_of_strings


@dataclass(frozen=True, slots=True)
class ElectricReheater:
    """Elektrischer Nachheizer fuer Speicher oder Trinkwarmwasser."""

    reheater_id: str
    availability: ComponentAvailability | str = ComponentAvailability.UNKNOWN
    capacity_kw: float | None = None
    control: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))


@dataclass(frozen=True, slots=True)
class ThermalStorage:
    """Neutraler thermischer Speicher."""

    storage_id: str
    storage_type: str
    availability: ComponentAvailability | str = ComponentAvailability.UNKNOWN
    volume_m3: float | None = None
    storage_medium: str = ""
    insulation_u_value_w_m2k: float | None = None
    number_of_model_layers: int | None = None
    electric_reheater: ElectricReheater | None = None
    connections: tuple[str, ...] = ()
    adapter_extensions: dict[str, object] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))
        object.__setattr__(self, "connections", tuple_of_strings(self.connections))
        if self.adapter_extensions is not None:
            object.__setattr__(self, "adapter_extensions", dict(self.adapter_extensions))


@dataclass(frozen=True, slots=True)
class DomesticHotWaterGeneration:
    """Trinkwarmwasser-Erzeugung ohne normative Dimensionierung."""

    generation_id: str
    generation_mode: str
    heating_function_reference: ObjectReference | None = None
    separate_generator: ObjectReference | None = None
    storage: ThermalStorage | None = None
    circulation: str = ""
    control: str = ""
    service_interface_reference: str = ""
