"""Additive Definitionen fuer den hierarchischen Parameterkatalog.

Die bestehenden Snapshot-Klassen beschreiben konkrete, versionierte Werte.
Dieses Modul beschreibt davon getrennt, *welche* Parameter und Gruppen es
fachlich gibt. Die Trennung erlaubt eine schrittweise Migration ohne den
P015-/P017-Handover zu brechen.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ParameterModule(StrEnum):
    """Die vier fachlichen Eingabemodule des Parameterkatalogs."""

    BUILDING = "BUILDING"
    ZONES = "ZONES"
    TECHNOLOGY = "TECHNOLOGY"
    WEATHER = "WEATHER"


class ParameterDataType(StrEnum):
    """Zulaessige Datenarten eines fachlichen Parameterwerts."""

    BOOLEAN = "boolean"
    INTEGER = "integer"
    NUMBER = "number"
    TEXT = "text"
    ENUM = "enum"
    REFERENCE = "reference"
    SCHEDULE_REFERENCE = "schedule_reference"


class ParameterSourceType(StrEnum):
    """Fachliche Herkunft eines konkreten Parameterwerts."""

    USER = "user"
    IFC = "ifc"
    CATALOG = "catalog"
    DERIVED = "derived"
    REFERENCE_MODEL = "reference_model"
    WEATHER_DATASET = "weather_dataset"


class ParameterEditability(StrEnum):
    """Beschreibt die Aenderbarkeit unabhaengig von Herkunft und Variation."""

    FIXED = "fixed"
    EDITABLE = "editable"
    CONDITIONAL = "conditional"


class ParameterVariantCapability(StrEnum):
    """Beschreibt, ob ein editierbarer Wert grundsaetzlich variierbar sein kann."""

    NOT_CAPABLE = "not_capable"
    CAPABLE = "capable"
    CONDITIONAL = "conditional"


class ParameterDerivationStatus(StrEnum):
    """Trennt direkt gefuehrte von abgeleiteten Werten."""

    DIRECT = "direct"
    DERIVED = "derived"


class ParameterActivationStatus(StrEnum):
    """Beschreibt, ob ein Parameter fuer die aktive Konfiguration gilt."""

    REQUIRED = "required"
    OPTIONAL_ACTIVE = "optional_active"
    OPTIONAL_INACTIVE = "optional_inactive"


class ParameterInventoryStatus(StrEnum):
    """Einordnung eines Bestandsfelds gegen das neue Parameterzielbild."""

    EXISTS = "EXISTS"
    MISSING = "MISSING"
    PARTIAL = "PARTIAL"
    REDUNDANT = "REDUNDANT"
    METADATA = "METADATA"
    DERIVED = "DERIVED"


@dataclass(frozen=True, slots=True)
class ParameterGroup:
    """Eine fachlich zusammengehoerige, gegebenenfalls wiederholbare Objektgruppe."""

    group_id: str
    module: ParameterModule | str
    category: str
    group_type: str
    display_name: str
    instance_type: str
    repeatable: bool
    parent_group_id: str = ""
    description: str = ""

    def __post_init__(self) -> None:
        _require_text(self.group_id, "group_id")
        _require_text(self.category, "category")
        _require_text(self.group_type, "group_type")
        _require_text(self.display_name, "display_name")
        _require_text(self.instance_type, "instance_type")
        object.__setattr__(self, "module", _coerce_enum(self.module, ParameterModule, "module"))
        if not isinstance(self.repeatable, bool):
            raise TypeError("repeatable muss ein boolescher Wert sein.")


@dataclass(frozen=True, slots=True)
class ParameterDefinition:
    """Stabile fachliche Definition eines Einzelparameters ohne Projektwert."""

    definition_key: str
    module: ParameterModule | str
    category: str
    group_type: str
    parameter_name: str
    display_name: str
    datatype: ParameterDataType | str
    unit: str
    lod_min: int
    lod_max: int
    allowed_source_types: tuple[ParameterSourceType | str, ...]
    default_editability: ParameterEditability | str
    default_variant_capability: ParameterVariantCapability | str
    derivation_status: ParameterDerivationStatus | str = ParameterDerivationStatus.DIRECT
    required: bool = True
    allowed_values: tuple[object, ...] = ()
    min_value: float | None = None
    max_value: float | None = None
    step: float | None = None
    description: str = ""

    def __post_init__(self) -> None:
        for field_name in (
            "definition_key",
            "category",
            "group_type",
            "parameter_name",
            "display_name",
            "unit",
        ):
            _require_text(getattr(self, field_name), field_name)
        object.__setattr__(self, "module", _coerce_enum(self.module, ParameterModule, "module"))
        object.__setattr__(self, "datatype", _coerce_enum(self.datatype, ParameterDataType, "datatype"))
        object.__setattr__(
            self,
            "default_editability",
            _coerce_enum(self.default_editability, ParameterEditability, "default_editability"),
        )
        object.__setattr__(
            self,
            "default_variant_capability",
            _coerce_enum(
                self.default_variant_capability,
                ParameterVariantCapability,
                "default_variant_capability",
            ),
        )
        object.__setattr__(
            self,
            "derivation_status",
            _coerce_enum(self.derivation_status, ParameterDerivationStatus, "derivation_status"),
        )
        source_types = tuple(
            _coerce_enum(source_type, ParameterSourceType, "allowed_source_types")
            for source_type in self.allowed_source_types
        )
        if not source_types:
            raise ValueError("allowed_source_types darf nicht leer sein.")
        object.__setattr__(self, "allowed_source_types", source_types)
        object.__setattr__(self, "allowed_values", tuple(self.allowed_values))
        _validate_lod_range(self.lod_min, self.lod_max)
        _validate_numeric_range(self.min_value, self.max_value, self.step)
        if not isinstance(self.required, bool):
            raise TypeError("required muss ein boolescher Wert sein.")
        _validate_definition_status_axes(
            self.derivation_status,
            self.default_editability,
            self.default_variant_capability,
        )

    def applies_to_lod(self, lod: int) -> bool:
        """Prueft, ob die Definition fuer einen LoD gilt."""
        return self.lod_min <= lod <= self.lod_max


@dataclass(frozen=True, slots=True)
class ParameterInstance:
    """Ein konkreter Parameterwert mit Herkunft und Bedienstatus."""

    instance_id: str
    definition_key: str
    group_id: str
    value: object
    source_type: ParameterSourceType | str
    editability: ParameterEditability | str
    variant_capability: ParameterVariantCapability | str
    derivation_status: ParameterDerivationStatus | str
    activation_status: ParameterActivationStatus | str
    source_reference_id: str = ""

    def __post_init__(self) -> None:
        for field_name in ("instance_id", "definition_key", "group_id"):
            _require_text(getattr(self, field_name), field_name)
        object.__setattr__(self, "source_type", _coerce_enum(self.source_type, ParameterSourceType, "source_type"))
        object.__setattr__(self, "editability", _coerce_enum(self.editability, ParameterEditability, "editability"))
        object.__setattr__(
            self,
            "variant_capability",
            _coerce_enum(self.variant_capability, ParameterVariantCapability, "variant_capability"),
        )
        object.__setattr__(
            self,
            "derivation_status",
            _coerce_enum(self.derivation_status, ParameterDerivationStatus, "derivation_status"),
        )
        object.__setattr__(
            self,
            "activation_status",
            _coerce_enum(self.activation_status, ParameterActivationStatus, "activation_status"),
        )
        _validate_definition_status_axes(self.derivation_status, self.editability, self.variant_capability)


@dataclass(frozen=True, slots=True)
class ParameterInventoryEntry:
    """Maschinenlesbare Bestandsmatrix fuer die schrittweise P015-Migration."""

    subject: str
    legacy_parameter_key_pattern: str
    source_path: str
    target_module: ParameterModule | str
    target_group_type: str
    target_parameter_key_pattern: str
    unit: str
    source_type: ParameterSourceType | str
    lod_min: int
    lod_max: int
    editability: ParameterEditability | str
    variant_capability: ParameterVariantCapability | str
    derivation_status: ParameterDerivationStatus | str
    status: ParameterInventoryStatus | str
    observed_count: int = 0
    notes: str = ""

    def __post_init__(self) -> None:
        for field_name in ("subject", "target_group_type", "target_parameter_key_pattern", "unit"):
            _require_text(getattr(self, field_name), field_name)
        object.__setattr__(self, "target_module", _coerce_enum(self.target_module, ParameterModule, "target_module"))
        object.__setattr__(self, "source_type", _coerce_enum(self.source_type, ParameterSourceType, "source_type"))
        object.__setattr__(self, "editability", _coerce_enum(self.editability, ParameterEditability, "editability"))
        object.__setattr__(
            self,
            "variant_capability",
            _coerce_enum(self.variant_capability, ParameterVariantCapability, "variant_capability"),
        )
        object.__setattr__(
            self,
            "derivation_status",
            _coerce_enum(self.derivation_status, ParameterDerivationStatus, "derivation_status"),
        )
        object.__setattr__(self, "status", _coerce_enum(self.status, ParameterInventoryStatus, "status"))
        _validate_lod_range(self.lod_min, self.lod_max)
        _validate_definition_status_axes(self.derivation_status, self.editability, self.variant_capability)
        if not isinstance(self.observed_count, int) or self.observed_count < 0:
            raise ValueError("observed_count muss eine nicht negative Ganzzahl sein.")
        if self.status is ParameterInventoryStatus.MISSING and self.observed_count:
            raise ValueError("MISSING-Eintraege duerfen keine beobachteten Parameter zaehlen.")


def _coerce_enum(value: object, enum_type: type[StrEnum], field_name: str) -> StrEnum:
    if isinstance(value, enum_type):
        return value
    try:
        return enum_type(str(value).strip())
    except ValueError as exc:
        raise ValueError(f"{field_name} besitzt keinen gueltigen Wert: {value!r}") from exc


def _require_text(value: object, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} darf nicht leer sein.")


def _validate_lod_range(lod_min: int, lod_max: int) -> None:
    if not isinstance(lod_min, int) or not isinstance(lod_max, int):
        raise TypeError("lod_min und lod_max muessen Ganzzahlen sein.")
    if lod_min < 1 or lod_max < lod_min:
        raise ValueError("LoD muss mindestens 1 sein und lod_max darf nicht kleiner als lod_min sein.")


def _validate_numeric_range(min_value: float | None, max_value: float | None, step: float | None) -> None:
    if min_value is not None and max_value is not None and min_value > max_value:
        raise ValueError("min_value darf nicht groesser als max_value sein.")
    if step is not None and step <= 0:
        raise ValueError("step muss groesser als 0 sein.")


def _validate_definition_status_axes(
    derivation_status: ParameterDerivationStatus,
    editability: ParameterEditability,
    variant_capability: ParameterVariantCapability,
) -> None:
    if derivation_status is ParameterDerivationStatus.DERIVED:
        if editability is not ParameterEditability.FIXED:
            raise ValueError("Abgeleitete Parameter muessen gesperrt sein.")
        if variant_capability is not ParameterVariantCapability.NOT_CAPABLE:
            raise ValueError("Abgeleitete Parameter duerfen nicht direkt variierbar sein.")
    if variant_capability is ParameterVariantCapability.CAPABLE and editability is ParameterEditability.FIXED:
        raise ValueError("Variantenfaehige Parameter muessen editierbar oder bedingt editierbar sein.")
