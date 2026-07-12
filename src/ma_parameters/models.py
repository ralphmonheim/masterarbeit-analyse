"""Fachmodelle fuer Parameteroptionen und Parameter-Snapshots."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from ma_core import ConfigurationSource, utc_now

SNAPSHOT_SCHEMA_VERSION = "1.0"
INPUT_PACKAGE_SCHEMA_VERSION = "1.0"
BASELINE_SNAPSHOT_SCHEMA_VERSION = "2.0"


class ParameterScopeType(StrEnum):
    """Fachlicher Gueltigkeitsbereich eines Parameters."""

    PROJECT = "project"
    BUILDING = "building"
    ZONE_GROUP = "zone_group"
    ZONE = "zone"
    TECHNICAL_SYSTEM = "technical_system"


class ParameterClass(StrEnum):
    """Rolle eines Parameterwerts im zentralen Parameterstand."""

    PRIMARY_DIRECT = "primary_direct"
    PRIMARY_REFERENCE = "primary_reference"
    PRIMARY_DERIVED = "primary_derived"
    SECONDARY = "secondary"
    VARIATION = "variation"
    DERIVED_VARIANT_VALUE = "derived_variant_value"
    RESULT_PARAMETER = "result_parameter"


class ParameterVariability(StrEnum):
    """Beschreibt, ob und wie ein Wert spaeter variiert werden darf."""

    NOT_VARIABLE = "not_variable"
    DIRECT_VARIABLE = "direct_variable"
    REFERENCE_VARIABLE = "reference_variable"
    FACTOR_VARIABLE = "factor_variable"
    STRUCTURAL_VARIABLE = "structural_variable"


class BuildingDetailMode(StrEnum):
    """Detailmodus eines Baseline-Snapshots."""

    SIMPLIFIED = "simplified"
    COMPLETE = "complete"


class FreshnessStatus(StrEnum):
    """Aktualitaetsstatus gegenueber den referenzierten Quellen."""

    CURRENT = "current"
    OUTDATED = "outdated"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ParameterOptionSelection:
    """Speichert die aktiven Optionswerte je Optionsgruppe."""

    active_option_keys_by_set: dict[str, tuple[str, ...]]
    source: ConfigurationSource


@dataclass(frozen=True, slots=True)
class ParameterPreviewRow:
    """Lesbare Vorschau eines spaeteren zentralen Parameters."""

    module_key: str
    parameter_key: str
    label: str
    value: object
    unit: str
    source: str
    status: str = "preview"


@dataclass(frozen=True, slots=True)
class ParameterSourceReference:
    """Nachvollziehbare Quelle eines Parameterwerts."""

    source_reference_id: str
    module_key: str
    dataset_key: str
    version_id: str
    validation_status: str
    label: str = ""
    reference_id: str = ""
    reference_version: str = ""
    content_hash: str = ""
    freshness_status: str = FreshnessStatus.CURRENT.value


@dataclass(frozen=True, slots=True)
class ParameterValue:
    """Ein einzelner zentraler Parameterwert mit Einheit und Herkunft."""

    parameter_key: str
    label: str
    value: object
    unit: str
    source_reference_id: str
    status: str = "released"


@dataclass(frozen=True, slots=True)
class ParameterScope:
    """Stabiler Scope fuer einen konkreten Parameterwert."""

    scope_type: ParameterScopeType | str
    scope_id: str
    label: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.scope_type, ParameterScopeType):
            object.__setattr__(self, "scope_type", ParameterScopeType(self.scope_type))


@dataclass(frozen=True, slots=True)
class ParameterReferenceVersion:
    """Versionierte Referenz auf ein komplexeres Fachobjekt."""

    reference_id: str
    reference_version: str
    content_hash: str
    source_reference_id: str
    label: str = ""


@dataclass(frozen=True, slots=True)
class BaselineParameterValue:
    """Ein konkreter Parameterwert mit Scope, Klasse und Variierbarkeit."""

    parameter_value_id: str
    parameter_key: str
    label: str
    value: object
    unit: str
    scope: ParameterScope
    parameter_class: ParameterClass | str
    variability: ParameterVariability | str
    source_reference_id: str
    reference_id: str = ""
    reference_version: str = ""
    content_hash: str = ""
    status: str = "released"

    def __post_init__(self) -> None:
        if not isinstance(self.scope, ParameterScope):
            raise TypeError("scope muss ein ParameterScope sein.")
        if not isinstance(self.parameter_class, ParameterClass):
            object.__setattr__(self, "parameter_class", ParameterClass(self.parameter_class))
        if not isinstance(self.variability, ParameterVariability):
            object.__setattr__(self, "variability", ParameterVariability(self.variability))


@dataclass(frozen=True, slots=True)
class ParameterSnapshot:
    """Versionierter Eingabestand fuer nachgelagerte Module."""

    snapshot_id: str
    snapshot_version: str
    project_id: str
    building_id: str
    input_detail_level: str
    values: tuple[ParameterValue, ...]
    source_references: tuple[ParameterSourceReference, ...]
    schema_version: str = SNAPSHOT_SCHEMA_VERSION
    created_at: datetime = field(default_factory=utc_now)
    description: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", tuple(self.values))
        object.__setattr__(self, "source_references", tuple(self.source_references))
        if self.created_at.tzinfo is None:
            raise ValueError("created_at muss eine Zeitzone enthalten.")

    @property
    def parameter_keys(self) -> set[str]:
        return {value.parameter_key for value in self.values}

    @property
    def source_reference_ids(self) -> set[str]:
        return {source.source_reference_id for source in self.source_references}

    def object_id_locations(self) -> tuple[tuple[str, str], ...]:
        """Liefert IDs mit Fundstelle fuer die Validierung."""
        rows: list[tuple[str, str]] = [(self.snapshot_id, "snapshot_id")]
        rows.extend(
            (source.source_reference_id, f"source_references.{index}.source_reference_id")
            for index, source in enumerate(self.source_references)
        )
        rows.extend((value.parameter_key, f"values.{index}.parameter_key") for index, value in enumerate(self.values))
        return tuple(rows)


@dataclass(frozen=True, slots=True)
class ParameterInputPackage:
    """Geprueftes Eingangspaket fuer den naechsten Parameteraufbau."""

    package_id: str
    package_version: str
    project_id: str
    building_id: str
    input_detail_level: str
    values: tuple[ParameterValue, ...]
    source_references: tuple[ParameterSourceReference, ...]
    source_snapshot_id: str = ""
    source_snapshot_version: str = ""
    requires_weather: bool = True
    weather_activated: bool = False
    schema_version: str = INPUT_PACKAGE_SCHEMA_VERSION
    created_at: datetime = field(default_factory=utc_now)
    description: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", tuple(self.values))
        object.__setattr__(self, "source_references", tuple(self.source_references))
        if self.created_at.tzinfo is None:
            raise ValueError("created_at muss eine Zeitzone enthalten.")

    @property
    def parameter_keys(self) -> set[str]:
        return {value.parameter_key for value in self.values}

    @property
    def source_reference_ids(self) -> set[str]:
        return {source.source_reference_id for source in self.source_references}

    @property
    def source_modules(self) -> set[str]:
        return {source.module_key for source in self.source_references}

    def object_id_locations(self) -> tuple[tuple[str, str], ...]:
        """Liefert IDs mit Fundstelle fuer die Validierung."""
        rows: list[tuple[str, str]] = [(self.package_id, "package_id")]
        rows.extend(
            (source.source_reference_id, f"source_references.{index}.source_reference_id")
            for index, source in enumerate(self.source_references)
        )
        rows.extend((value.parameter_key, f"values.{index}.parameter_key") for index, value in enumerate(self.values))
        return tuple(rows)


@dataclass(frozen=True, slots=True)
class BaselineParameterSnapshot:
    """Versionierter Baseline-Stand fuer Varianten und Folgeprozesse."""

    snapshot_id: str
    snapshot_version: str
    project_id: str
    building_id: str
    building_detail_mode: BuildingDetailMode | str
    parameter_values: tuple[BaselineParameterValue, ...]
    source_references: tuple[ParameterSourceReference, ...]
    reference_versions: tuple[ParameterReferenceVersion, ...]
    source_snapshot_id: str = ""
    source_snapshot_version: str = ""
    schema_version: str = BASELINE_SNAPSHOT_SCHEMA_VERSION
    content_hash: str = ""
    release_status: str = "released"
    freshness_status: FreshnessStatus | str = FreshnessStatus.CURRENT
    created_at: datetime = field(default_factory=utc_now)
    description: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "parameter_values", tuple(self.parameter_values))
        object.__setattr__(self, "source_references", tuple(self.source_references))
        object.__setattr__(self, "reference_versions", tuple(self.reference_versions))
        if not isinstance(self.building_detail_mode, BuildingDetailMode):
            object.__setattr__(self, "building_detail_mode", BuildingDetailMode(self.building_detail_mode))
        if not isinstance(self.freshness_status, FreshnessStatus):
            object.__setattr__(self, "freshness_status", FreshnessStatus(self.freshness_status))
        if self.created_at.tzinfo is None:
            raise ValueError("created_at muss eine Zeitzone enthalten.")

    @property
    def parameter_value_ids(self) -> set[str]:
        return {value.parameter_value_id for value in self.parameter_values}

    @property
    def source_reference_ids(self) -> set[str]:
        return {source.source_reference_id for source in self.source_references}

    @property
    def scoped_parameter_keys(self) -> set[tuple[str, str, str]]:
        return {
            (value.parameter_key, value.scope.scope_type.value, value.scope.scope_id)
            for value in self.parameter_values
        }

    def object_id_locations(self) -> tuple[tuple[str, str], ...]:
        """Liefert ID-Felder mit Fundstelle fuer die Validierung."""
        rows: list[tuple[str, str]] = [(self.snapshot_id, "snapshot_id")]
        rows.extend(
            (source.source_reference_id, f"source_references.{index}.source_reference_id")
            for index, source in enumerate(self.source_references)
        )
        rows.extend(
            (reference.reference_id, f"reference_versions.{index}.reference_id")
            for index, reference in enumerate(self.reference_versions)
        )
        rows.extend(
            (value.parameter_value_id, f"parameter_values.{index}.parameter_value_id")
            for index, value in enumerate(self.parameter_values)
        )
        return tuple(rows)
