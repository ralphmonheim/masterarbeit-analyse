"""Neutrale Diagnose-, Validierungs- und Freigabemodelle."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from ma_core import InputSource, utc_now


def _create_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


class DiagnosticSeverity(StrEnum):
    """Schweregrad einer strukturierten Meldung."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ReleaseStatus(StrEnum):
    """Freigabestatus eines validierten Datenstands."""

    BLOCKED = "blocked"
    CONFIRMATION_REQUIRED = "confirmation_required"
    RELEASED = "released"


class ReleaseChoice(StrEnum):
    """Moegliche Entscheidungen fuer einen Freigabestand."""

    KEEP_BLOCKED = "keep_blocked"
    RELEASE_WITH_WARNINGS = "release_with_warnings"
    AUTOMATIC_RELEASE = "automatic_release"


@dataclass(frozen=True, slots=True)
class DiagnosticMessage:
    """Strukturierte, referenzierbare Warnung, Information oder Fehlermeldung."""

    severity: DiagnosticSeverity
    code: str
    message: str
    location: str | None = None
    diagnostic_id: str = field(default_factory=lambda: _create_id("diagnostic"))
    occurred_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not isinstance(self.severity, DiagnosticSeverity):
            object.__setattr__(self, "severity", DiagnosticSeverity(self.severity))
        if not self.code.strip():
            raise ValueError("code darf nicht leer sein.")
        if not self.message.strip():
            raise ValueError("message darf nicht leer sein.")
        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at muss eine Zeitzone enthalten.")


@dataclass(frozen=True, slots=True)
class ImportDiagnostic:
    """Zusammenfassung eines Importvorgangs und seiner Meldungen."""

    source: InputSource
    messages: tuple[DiagnosticMessage, ...] = ()
    record_count: int = 0
    accepted_count: int = 0
    rejected_count: int = 0

    def __post_init__(self) -> None:
        if min(self.record_count, self.accepted_count, self.rejected_count) < 0:
            raise ValueError("Datensatzanzahlen duerfen nicht negativ sein.")
        if self.accepted_count + self.rejected_count > self.record_count:
            raise ValueError("Akzeptierte und abgelehnte Datensaetze ueberschreiten record_count.")


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Gemeinsames Ergebnis lokaler Fachvalidierungen."""

    messages: tuple[DiagnosticMessage, ...]
    release_status: ReleaseStatus

    @property
    def errors(self) -> tuple[DiagnosticMessage, ...]:
        return tuple(message for message in self.messages if message.severity is DiagnosticSeverity.ERROR)

    @property
    def warnings(self) -> tuple[DiagnosticMessage, ...]:
        return tuple(message for message in self.messages if message.severity is DiagnosticSeverity.WARNING)


@dataclass(frozen=True, slots=True)
class ReleaseDecision:
    """Nachvollziehbare Entscheidung ueber einen validierten Datenstand."""

    session_id: str
    run_id: str
    module_key: str
    dataset_key: str
    choice: ReleaseChoice
    resulting_status: ReleaseStatus
    diagnostic_ids: tuple[str, ...]
    note: str | None = None
    decision_id: str = field(default_factory=lambda: _create_id("decision"))
    decided_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not isinstance(self.choice, ReleaseChoice):
            object.__setattr__(self, "choice", ReleaseChoice(self.choice))
        if not isinstance(self.resulting_status, ReleaseStatus):
            object.__setattr__(self, "resulting_status", ReleaseStatus(self.resulting_status))
        for field_name in ("session_id", "run_id", "module_key", "dataset_key"):
            if not str(getattr(self, field_name)).strip():
                raise ValueError(f"{field_name} darf nicht leer sein.")
        if self.decided_at.tzinfo is None:
            raise ValueError("decided_at muss eine Zeitzone enthalten.")
