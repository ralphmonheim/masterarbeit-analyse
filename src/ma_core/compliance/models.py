"""Unveraenderliche Anfragen, Preflights und Entscheidungen."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from ma_core.input_sources import utc_now

from .enums import ComplianceLevel, ComplianceOperation, ProcessingEnvironment, SourceType


class ComplianceBlockedError(PermissionError):
    """Signalisiert eine technisch blockierte Compliance-Operation."""


def _create_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


@dataclass(frozen=True, slots=True)
class OperationRequest:
    """Beschreibt genau eine beabsichtigte Datei- oder Systemoperation."""

    source_type: SourceType
    operation: ComplianceOperation
    purpose: str
    environment: ProcessingEnvironment = ProcessingEnvironment.LOCAL
    file_path: Path | None = None
    source_origin: str | None = None
    declared_license: str | None = None
    official_source: bool | None = None
    attribution_present: bool | None = None
    third_party_rights_cleared: bool | None = None
    user_owned: bool = False
    contains_license_or_access_data: bool = False
    request_id: str = field(default_factory=lambda: _create_id("compliance_request"))
    requested_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        for field_name, enum_type in (
            ("source_type", SourceType),
            ("operation", ComplianceOperation),
            ("environment", ProcessingEnvironment),
        ):
            value = getattr(self, field_name)
            if not isinstance(value, enum_type):
                object.__setattr__(self, field_name, enum_type(value))
        if not self.purpose.strip():
            raise ValueError("purpose darf nicht leer sein.")
        if self.file_path is not None and not isinstance(self.file_path, Path):
            object.__setattr__(self, "file_path", Path(self.file_path))
        if self.requested_at.tzinfo is None:
            raise ValueError("requested_at muss eine Zeitzone enthalten.")


@dataclass(frozen=True, slots=True)
class PreflightRecord:
    """Rein technische Metadaten, die vor einer Inhaltsverarbeitung entstehen."""

    request_id: str
    file_name: str | None = None
    file_suffix: str | None = None
    file_size_bytes: int | None = None
    sha256: str | None = None
    file_exists: bool | None = None
    source_origin_known: bool = False
    applicable_license_known: bool = False
    inspected_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id darf nicht leer sein.")
        if self.inspected_at.tzinfo is None:
            raise ValueError("inspected_at muss eine Zeitzone enthalten.")


@dataclass(frozen=True, slots=True)
class ComplianceDecision:
    """Nachvollziehbare und technisch erzwingbare Compliance-Entscheidung."""

    request_id: str
    classification: ComplianceLevel
    processing_allowed: bool
    warning_required: bool
    reason: str
    applicable_rules: tuple[str, ...]
    allowed_scope: tuple[str, ...] = ()
    excluded_scope: tuple[str, ...] = ()
    safe_alternative: str | None = None
    confirmation_required: bool = False
    written_permission_required: bool = False
    university_approval_required: bool = False
    confirmation_reference: str | None = None
    permission_reference: str | None = None
    university_approval_reference: str | None = None
    decision_id: str = field(default_factory=lambda: _create_id("compliance_decision"))
    decided_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not isinstance(self.classification, ComplianceLevel):
            object.__setattr__(self, "classification", ComplianceLevel(self.classification))
        if not self.request_id.strip():
            raise ValueError("request_id darf nicht leer sein.")
        if not self.reason.strip():
            raise ValueError("reason darf nicht leer sein.")
        if not self.applicable_rules:
            raise ValueError("applicable_rules darf nicht leer sein.")
        if self.decided_at.tzinfo is None:
            raise ValueError("decided_at muss eine Zeitzone enthalten.")
        if self.classification in {ComplianceLevel.RED, ComplianceLevel.UNKNOWN} and self.processing_allowed:
            raise ValueError("Rote oder unbekannte Entscheidungen duerfen nicht freigegeben sein.")

    def with_approval(
        self,
        *,
        confirmation_reference: str,
        permission_reference: str | None = None,
        university_approval_reference: str | None = None,
    ) -> ComplianceDecision:
        """Gibt eine gelbe Entscheidung nur mit allen erforderlichen Belegen frei."""
        if self.classification is not ComplianceLevel.YELLOW:
            raise ComplianceBlockedError("Nur gelbe Entscheidungen koennen bestaetigt werden.")
        if not confirmation_reference.strip():
            raise ValueError("confirmation_reference darf nicht leer sein.")
        if self.written_permission_required and not (permission_reference or "").strip():
            raise ComplianceBlockedError("Die erforderliche schriftliche Rechtefreigabe fehlt.")
        if self.university_approval_required and not (university_approval_reference or "").strip():
            raise ComplianceBlockedError("Die erforderliche Hochschulfreigabe fehlt.")
        return replace(
            self,
            processing_allowed=True,
            confirmation_reference=confirmation_reference,
            permission_reference=permission_reference,
            university_approval_reference=university_approval_reference,
            decided_at=utc_now(),
            decision_id=_create_id("compliance_decision"),
        )

    def require_allowed(self) -> None:
        """Stoppt die aufrufende Operation, solange keine gueltige Freigabe vorliegt."""
        if self.processing_allowed:
            return
        alternative = f" Sichere Alternative: {self.safe_alternative}" if self.safe_alternative else ""
        raise ComplianceBlockedError(
            f"Compliance-{self.classification.value.upper()}: {self.reason}{alternative}"
        )
