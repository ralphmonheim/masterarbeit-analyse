import pytest

from ma_validation import (
    DiagnosticMessage,
    DiagnosticSeverity,
    ReleaseChoice,
    ReleaseStatus,
    build_validation_result,
    create_release_decision,
)


def _message(severity: DiagnosticSeverity) -> DiagnosticMessage:
    return DiagnosticMessage(
        severity=severity,
        code=f"TEST_{severity.value.upper()}",
        message=f"Test {severity.value}",
        location="test.field",
    )


def _decision(validation_result, choice):
    return create_release_decision(
        validation_result,
        choice=choice,
        session_id="session_test",
        run_id="run_test",
        module_key="ma_weather",
        dataset_key="TRY_TEST",
        note="Testentscheidung",
    )


def test_errors_always_block_and_cannot_be_overridden():
    result = build_validation_result((_message(DiagnosticSeverity.ERROR),))

    assert result.release_status is ReleaseStatus.BLOCKED
    decision = _decision(result, ReleaseChoice.KEEP_BLOCKED)
    assert decision.resulting_status is ReleaseStatus.BLOCKED
    with pytest.raises(ValueError, match="darf nicht freigegeben"):
        _decision(result, ReleaseChoice.RELEASE_WITH_WARNINGS)


def test_warnings_require_explicit_release_choice():
    result = build_validation_result((_message(DiagnosticSeverity.WARNING),))

    assert result.release_status is ReleaseStatus.CONFIRMATION_REQUIRED
    blocked = _decision(result, ReleaseChoice.KEEP_BLOCKED)
    released = _decision(result, ReleaseChoice.RELEASE_WITH_WARNINGS)

    assert blocked.resulting_status is ReleaseStatus.BLOCKED
    assert released.resulting_status is ReleaseStatus.RELEASED
    assert released.diagnostic_ids == (result.messages[0].diagnostic_id,)
    assert released.decision_id.startswith("decision_")


def test_clean_result_is_automatically_released():
    result = build_validation_result(())

    assert result.release_status is ReleaseStatus.RELEASED
    decision = _decision(result, ReleaseChoice.AUTOMATIC_RELEASE)
    assert decision.resulting_status is ReleaseStatus.RELEASED
    with pytest.raises(ValueError, match="automatisch freigegeben"):
        _decision(result, ReleaseChoice.KEEP_BLOCKED)
