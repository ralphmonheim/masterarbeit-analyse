"""Fachmodelle fuer die einfache Referenzdimensionierung."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ma_validation import DiagnosticMessage


class DimensioningStatus(StrEnum):
    """Bewertungsstatus eines Dimensionierungslaufs."""

    EVALUATED = "evaluated"
    NOT_EVALUABLE = "not_evaluable"


@dataclass(frozen=True, slots=True)
class DimensioningStep:
    """Ein nachvollziehbarer Rechenschritt mit Quellenbezug."""

    step_key: str
    label: str
    value: float
    unit: str
    formula: str
    source_parameter_keys: tuple[str, ...]
    note: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_parameter_keys", tuple(self.source_parameter_keys))


@dataclass(frozen=True, slots=True)
class ReferenceDimensioningResult:
    """Ergebnis der LoD-1-Referenzdimensionierung."""

    result_id: str
    source_snapshot_id: str
    source_snapshot_version: str
    status: DimensioningStatus | str
    heating_transmission_load_w: float | None
    heating_ventilation_load_w: float | None
    heating_total_load_w: float | None
    cooling_internal_load_w: float | None
    ventilation_volume_flow_m3_h: float | None
    steps: tuple[DimensioningStep, ...]
    messages: tuple[DiagnosticMessage, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.status, DimensioningStatus):
            object.__setattr__(self, "status", DimensioningStatus(self.status))
        object.__setattr__(self, "steps", tuple(self.steps))
        object.__setattr__(self, "messages", tuple(self.messages))
