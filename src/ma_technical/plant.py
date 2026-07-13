"""Plant-, Heizungs- und Kuehlungsobjekte fuer ma_technical v2."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import (
    CapacityMode,
    ComponentAvailability,
    HeatingConfigurationMode,
    HeatingDispatchStrategy,
    HeatingFunctionalRole,
    PerformanceMetricType,
    TechnicalRepresentationMode,
)
from .metadata import ObjectReference, SourceMetadata, coerce_enum, tuple_of_strings


@dataclass(frozen=True, slots=True)
class CapacityDefinition:
    """Technische Leistung mit bewusstem Modus statt pauschaler Pflichtzahl."""

    mode: CapacityMode | str
    nominal_capacity_kw: float | None = None
    maximum_capacity_kw: float | None = None
    minimum_capacity_kw: float | None = None
    reference_conditions: str = ""
    product_reference: ObjectReference | None = None
    source_metadata: SourceMetadata | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "mode", coerce_enum(self.mode, CapacityMode))

    @property
    def is_ideal_unlimited(self) -> bool:
        return self.mode == CapacityMode.IDEAL_UNLIMITED

    @property
    def requires_capacity_value(self) -> bool:
        return self.mode in {CapacityMode.SPECIFIED, CapacityMode.DIMENSIONING_RESULT, CapacityMode.PRODUCT_BASED}


@dataclass(frozen=True, slots=True)
class PerformanceDefinition:
    """Leistungskennzahl wie COP, EER oder Wirkungsgrad."""

    metric_type: PerformanceMetricType | str
    value: float | None = None
    reference_conditions: str = ""
    source_metadata: SourceMetadata | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "metric_type", coerce_enum(self.metric_type, PerformanceMetricType))


@dataclass(frozen=True, slots=True)
class HeatingDispatchConfiguration:
    """Betriebsstrategie mehrerer Heizfunktionen."""

    strategy: HeatingDispatchStrategy | str
    notes: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "strategy", coerce_enum(self.strategy, HeatingDispatchStrategy))


@dataclass(frozen=True, slots=True)
class HeatingFunction:
    """Fachliche Heizfunktion, die optional auf ein physisches Geraet verweist."""

    function_id: str
    slot: str
    functional_role: HeatingFunctionalRole | str
    capacity: CapacityDefinition
    physical_equipment_reference: ObjectReference | None = None
    availability: ComponentAvailability | str = ComponentAvailability.PLANNED
    representation_mode: TechnicalRepresentationMode | str = TechnicalRepresentationMode.ASSUMED
    performance: PerformanceDefinition | None = None
    energy_carrier_reference: ObjectReference | None = None
    meter_assignments: tuple[str, ...] = ()
    supported_services: tuple[str, ...] = ()
    operating_limits: tuple[str, ...] = ()
    control: str = ""
    schedule_reference: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "functional_role", coerce_enum(self.functional_role, HeatingFunctionalRole))
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))
        object.__setattr__(
            self,
            "representation_mode",
            coerce_enum(self.representation_mode, TechnicalRepresentationMode),
        )
        object.__setattr__(self, "meter_assignments", tuple_of_strings(self.meter_assignments))
        object.__setattr__(self, "supported_services", tuple_of_strings(self.supported_services))
        object.__setattr__(self, "operating_limits", tuple_of_strings(self.operating_limits))


@dataclass(frozen=True, slots=True)
class HeatingGeneration:
    """Heizungserzeugung mit optionaler Basis- und Spitzenlastfunktion."""

    configuration_mode: HeatingConfigurationMode | str
    base_heating: HeatingFunction | None = None
    top_up_heating: HeatingFunction | None = None
    dispatch: HeatingDispatchConfiguration | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "configuration_mode", coerce_enum(self.configuration_mode, HeatingConfigurationMode))


@dataclass(frozen=True, slots=True)
class CoolingGeneration:
    """Zentrale Kuehlfunktion."""

    function_id: str
    capacity: CapacityDefinition
    physical_equipment_reference: ObjectReference | None = None
    availability: ComponentAvailability | str = ComponentAvailability.PLANNED
    representation_mode: TechnicalRepresentationMode | str = TechnicalRepresentationMode.ASSUMED
    performance: PerformanceDefinition | None = None
    energy_carrier_reference: ObjectReference | None = None
    meter_assignments: tuple[str, ...] = ()
    operating_limits: tuple[str, ...] = ()
    control: str = ""
    schedule_reference: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "availability", coerce_enum(self.availability, ComponentAvailability))
        object.__setattr__(
            self,
            "representation_mode",
            coerce_enum(self.representation_mode, TechnicalRepresentationMode),
        )
        object.__setattr__(self, "meter_assignments", tuple_of_strings(self.meter_assignments))
        object.__setattr__(self, "operating_limits", tuple_of_strings(self.operating_limits))


@dataclass(frozen=True, slots=True)
class TechnicalPlant:
    """Zentrale technische Anlage eines Technikmodells."""

    plant_id: str
    heating_generation: HeatingGeneration | None = None
    cooling_generation: CoolingGeneration | None = None
    heat_storage_reference: ObjectReference | None = None
    cold_storage_reference: ObjectReference | None = None
