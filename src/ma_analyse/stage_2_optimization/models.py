"""UI-neutrale Verträge für die Machbarkeitsprüfung von Varianten."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ComparisonOperator = Literal["<", "<=", "==", ">=", ">"]
ConstraintSourceType = Literal["project_requirement", "standard_informed"]
FeasibilityStatus = Literal["PASS", "FAIL", "NOT_EVALUABLE"]

_COMPARISON_OPERATORS = {"<", "<=", "==", ">=", ">"}
_SOURCE_TYPES = {"project_requirement", "standard_informed"}


@dataclass(frozen=True, slots=True)
class MetricValue:
    """Ein gemessener Kennwert mitsamt seiner Herkunft und Auswerteperiode."""

    metric_id: str
    value: float
    unit: str | None
    provenance: str
    evaluation_period: str


@dataclass(frozen=True, slots=True)
class OptimizationObjective:
    """Beschreibt ein Ziel, ohne Varianten zu bewerten oder auszuwählen."""

    objective_id: str
    metric_id: str
    direction: Literal["minimize", "maximize"]
    description: str = ""


@dataclass(frozen=True, slots=True)
class OptimizationConstraint:
    """Eine konfigurierbare Bedingung für eine Machbarkeitsprüfung."""

    constraint_id: str
    metric_id: str
    operator: ComparisonOperator
    limit: float
    unit: str | None
    mandatory: bool
    source_type: ConstraintSourceType
    description: str = ""

    def __post_init__(self) -> None:
        if self.operator not in _COMPARISON_OPERATORS:
            raise ValueError(f"Unsupported comparison operator: {self.operator}")
        if self.source_type not in _SOURCE_TYPES:
            raise ValueError(f"Unsupported constraint source type: {self.source_type}")


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Das nachvollziehbare Ergebnis einer einzelnen Bedingungsprüfung."""

    check_id: str
    status: FeasibilityStatus
    reason: str
    metric: MetricValue | None = None
    limit: float | None = None
    operator: ComparisonOperator | None = None


@dataclass(frozen=True, slots=True)
class FeasibilityResult:
    """Zusammenfassung einer Prüfung; sie trifft keine Bestvariantenauswahl."""

    status: FeasibilityStatus
    checks: tuple[CheckResult, ...]
