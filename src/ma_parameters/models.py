"""Fachmodelle fuer Parameteroptionen und Parameter-Snapshots."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ma_core import ConfigurationSource, utc_now

SNAPSHOT_SCHEMA_VERSION = "1.0"


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
