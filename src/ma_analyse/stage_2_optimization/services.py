"""Generische, einheitenbewusste Machbarkeitsprüfung ohne Grenzwerte."""

from __future__ import annotations

from collections.abc import Mapping
from math import isfinite

from .models import CheckResult, FeasibilityResult, MetricValue, OptimizationConstraint


class FeasibilityEngine:
    """Prüft übergebene Bedingungen, ohne Ziele zu gewichten oder Varianten zu wählen."""

    def evaluate(
        self,
        metrics: Mapping[str, MetricValue],
        constraints: tuple[OptimizationConstraint, ...],
    ) -> FeasibilityResult:
        checks = tuple(self._evaluate_constraint(metrics, constraint) for constraint in constraints)
        return FeasibilityResult(status=_overall_status(checks, constraints), checks=checks)

    @staticmethod
    def _evaluate_constraint(
        metrics: Mapping[str, MetricValue], constraint: OptimizationConstraint
    ) -> CheckResult:
        metric = metrics.get(constraint.metric_id)
        if metric is None:
            return CheckResult(constraint.constraint_id, "NOT_EVALUABLE", "Kennwert fehlt.", limit=constraint.limit,
                               operator=constraint.operator)
        if not _units_match(metric.unit, constraint.unit):
            return CheckResult(
                constraint.constraint_id,
                "NOT_EVALUABLE",
                "Einheit fehlt oder ist nicht kompatibel.",
                metric,
                constraint.limit,
                constraint.operator,
            )
        if not isfinite(metric.value) or not isfinite(constraint.limit):
            return CheckResult(
                constraint.constraint_id,
                "NOT_EVALUABLE",
                "Kennwert oder Grenzwert ist nicht endlich.",
                metric,
                constraint.limit,
                constraint.operator,
            )

        passed = _compare(metric.value, constraint.operator, constraint.limit)
        return CheckResult(
            constraint.constraint_id,
            "PASS" if passed else "FAIL",
            "Bedingung erfüllt." if passed else "Bedingung nicht erfüllt.",
            metric,
            constraint.limit,
            constraint.operator,
        )


def evaluate_feasibility(
    metrics: Mapping[str, MetricValue], constraints: tuple[OptimizationConstraint, ...]
) -> FeasibilityResult:
    """Praktische Funktion für eine einmalige Machbarkeitsprüfung."""

    return FeasibilityEngine().evaluate(metrics, constraints)


def _overall_status(checks: tuple[CheckResult, ...], constraints: tuple[OptimizationConstraint, ...]) -> str:
    mandatory_checks = (check for check, constraint in zip(checks, constraints, strict=True) if constraint.mandatory)
    statuses = {check.status for check in mandatory_checks}
    if "FAIL" in statuses:
        return "FAIL"
    if "NOT_EVALUABLE" in statuses:
        return "NOT_EVALUABLE"
    return "PASS"


def _units_match(metric_unit: str | None, constraint_unit: str | None) -> bool:
    if not metric_unit or not constraint_unit:
        return False
    return metric_unit.strip().casefold() == constraint_unit.strip().casefold()


def _compare(value: float, operator: str, limit: float) -> bool:
    return {
        "<": value < limit,
        "<=": value <= limit,
        "==": value == limit,
        ">=": value >= limit,
        ">": value > limit,
    }[operator]
