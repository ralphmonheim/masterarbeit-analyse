"""UI-neutrale Verträge für die Vorbereitung fachlicher Nachweise."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ma_analyse.stage_2_optimization.models import CheckResult

VerificationStatus = Literal["PASS", "FAIL", "INVALID", "NOT_EVALUABLE"]
RequirementOperator = Literal["<", "<=", "==", ">=", ">"]


@dataclass(frozen=True, slots=True)
class VerificationReadinessItem:
    """Beschreibt, ob ein fachliches Nachweiskriterium aktiviert werden darf."""

    criterion_id: str
    criterion: str
    standard_reference: str
    edition: str
    required_inputs: tuple[str, ...]
    method_status: str
    metadata_basis: str
    rights_status: str
    content_access_status: str
    test_status: str
    stage3_status: str
    reason: str
    next_gate: str


@dataclass(frozen=True, slots=True)
class StandardRequirement:
    """Eine von außen konfigurierte Nachweisbedingung ohne hinterlegte Normwerte."""

    requirement_id: str
    metric_id: str
    operator: RequirementOperator
    limit: float
    unit: str | None
    mandatory: bool = True
    description: str = ""


@dataclass(frozen=True, slots=True)
class StandardEvaluationProfile:
    """Unveränderliches Profil mit referenzierten, aber nicht eingebetteten Regeln."""

    profile_id: str
    standard_reference: str
    edition: str
    requirements: tuple[StandardRequirement, ...]
    description: str = ""


@dataclass(frozen=True, slots=True)
class ProfileValidation:
    """Ergebnis der strukturellen Profilprüfung vor jeder Auswertung."""

    is_valid: bool
    errors: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class StandardVerificationResult:
    """Nachweisergebnis mit Einzelprüfungen und einer expliziten Profilvalidierung."""

    status: VerificationStatus
    profile_id: str
    validation: ProfileValidation
    checks: tuple[CheckResult, ...]


def readiness_item_row(item: VerificationReadinessItem) -> dict[str, str]:
    """Bereitet einen Readiness-Eintrag für UI und Excel auf."""

    return {
        "Kriterium": item.criterion,
        "Regelwerk": item.standard_reference,
        "Ausgabe": item.edition,
        "Erforderliche Daten": ", ".join(item.required_inputs),
        "Methodenstatus": item.method_status,
        "Metadatenbasis": item.metadata_basis,
        "Rechtestatus": item.rights_status,
        "Inhaltszugriff": item.content_access_status,
        "Teststatus": item.test_status,
        "Stage-3-Status": item.stage3_status,
        "Begründung": item.reason,
        "Nächstes Gate": item.next_gate,
    }
