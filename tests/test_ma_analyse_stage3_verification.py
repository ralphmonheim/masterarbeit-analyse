from dataclasses import FrozenInstanceError

import pytest

from ma_analyse.stage_2_optimization import MetricValue
from ma_analyse.stage_3_standards_verification import (
    StandardEvaluationProfile,
    StandardRequirement,
    StandardVerificationEngine,
    validate_profile,
)


def _profile(requirements: tuple[StandardRequirement, ...]) -> StandardEvaluationProfile:
    return StandardEvaluationProfile(
        profile_id="synthetic-profile",
        standard_reference="Synthetic rule set",
        edition="test edition",
        requirements=requirements,
    )


def test_verification_uses_only_profile_values_and_keeps_profile_immutable():
    requirement = StandardRequirement("max-value", "metric", "<=", 10.0, "K")
    profile = _profile((requirement,))
    metrics = {
        "metric": MetricValue("metric", 8.0, "K", "synthetic source", "test period"),
    }

    result = StandardVerificationEngine().verify(profile, metrics)

    assert result.status == "PASS"
    assert result.checks[0].status == "PASS"
    with pytest.raises(FrozenInstanceError):
        profile.edition = "changed"


def test_missing_or_incompatible_metric_unit_is_not_evaluable():
    profile = _profile((StandardRequirement("max-value", "metric", "<=", 10.0, "K"),))

    missing = StandardVerificationEngine().verify(profile, {})
    incompatible = StandardVerificationEngine().verify(
        profile,
        {"metric": MetricValue("metric", 8.0, "W", "synthetic source", "test period")},
    )

    assert missing.status == "NOT_EVALUABLE"
    assert incompatible.status == "NOT_EVALUABLE"


def test_invalid_profile_is_reported_without_evaluating_a_rule():
    invalid = StandardEvaluationProfile(
        profile_id="",
        standard_reference="",
        edition="",
        requirements=(StandardRequirement("duplicated", "", "~", 10.0, None),) * 2,
    )

    validation = validate_profile(invalid)
    result = StandardVerificationEngine().verify(invalid, {})

    assert validation.is_valid is False
    assert result.status == "INVALID"
    assert result.checks == ()
    assert any("Operator" in error for error in validation.errors)


def test_non_finite_limit_is_an_invalid_profile_and_metric_is_not_evaluable():
    invalid = _profile((StandardRequirement("limit", "metric", "<=", float("inf"), "K"),))
    valid = _profile((StandardRequirement("value", "metric", "<=", 10.0, "K"),))

    assert StandardVerificationEngine().verify(invalid, {}).status == "INVALID"
    result = StandardVerificationEngine().verify(
        valid, {"metric": MetricValue("metric", float("nan"), "K", "source", "period")}
    )
    assert result.status == "NOT_EVALUABLE"


def test_optional_requirement_is_reported_but_does_not_fail_verification():
    profile = _profile(
        (
            StandardRequirement("required", "metric", "<=", 10.0, "K"),
            StandardRequirement("optional", "metric", "<", 5.0, "K", mandatory=False),
        )
    )
    metrics = {"metric": MetricValue("metric", 8.0, "K", "synthetic source", "test period")}

    result = StandardVerificationEngine().verify(profile, metrics)

    assert result.status == "PASS"
    assert [check.status for check in result.checks] == ["PASS", "FAIL"]
