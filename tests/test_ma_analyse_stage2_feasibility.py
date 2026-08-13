from dataclasses import FrozenInstanceError

import pytest

from ma_analyse.stage_2_optimization import (
    FeasibilityEngine,
    MetricValue,
    OptimizationConstraint,
    OptimizationObjective,
)


def _metric(value: float = 12.0, unit: str | None = "kWh") -> MetricValue:
    return MetricValue(
        metric_id="annual_energy",
        value=value,
        unit=unit,
        provenance="synthetic simulation result",
        evaluation_period="calendar year 2025",
    )


def test_feasibility_evaluates_configured_project_requirement_without_selecting_a_variant():
    constraint = OptimizationConstraint(
        constraint_id="energy-limit",
        metric_id="annual_energy",
        operator="<=",
        limit=15.0,
        unit="kWh",
        mandatory=True,
        source_type="project_requirement",
    )
    objective = OptimizationObjective("reduce-energy", "annual_energy", "minimize")

    result = FeasibilityEngine().evaluate({"annual_energy": _metric()}, (constraint,))

    assert objective.direction == "minimize"
    assert result.status == "PASS"
    assert result.checks[0].status == "PASS"
    assert result.checks[0].metric.provenance == "synthetic simulation result"
    assert not hasattr(result, "best_variant")


@pytest.mark.parametrize("unit", [None, "W"])
def test_missing_or_incompatible_unit_is_not_evaluable(unit):
    constraint = OptimizationConstraint(
        "energy-limit", "annual_energy", "<=", 15.0, "kWh", True, "standard_informed"
    )

    result = FeasibilityEngine().evaluate({"annual_energy": _metric(unit=unit)}, (constraint,))

    assert result.status == "NOT_EVALUABLE"
    assert result.checks[0].status == "NOT_EVALUABLE"


def test_optional_failure_does_not_make_mandatory_feasibility_fail():
    mandatory = OptimizationConstraint("required", "annual_energy", "<=", 15.0, "kWh", True, "project_requirement")
    optional = OptimizationConstraint("informative", "annual_energy", "<", 10.0, "kWh", False, "standard_informed")

    result = FeasibilityEngine().evaluate({"annual_energy": _metric()}, (mandatory, optional))

    assert result.status == "PASS"
    assert [check.status for check in result.checks] == ["PASS", "FAIL"]


def test_non_finite_metric_is_not_evaluable():
    constraint = OptimizationConstraint(
        "finite", "annual_energy", "<=", 15.0, "kWh", True, "project_requirement"
    )

    result = FeasibilityEngine().evaluate({"annual_energy": _metric(float("nan"))}, (constraint,))

    assert result.status == "NOT_EVALUABLE"


def test_contracts_are_immutable_and_reject_unknown_configuration_values():
    metric = _metric()
    with pytest.raises(FrozenInstanceError):
        metric.unit = "W"
    with pytest.raises(ValueError, match="operator"):
        OptimizationConstraint("invalid", "annual_energy", "~", 1.0, "kWh", True, "project_requirement")
