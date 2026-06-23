"""Freigabelogik fuer gemeinsame Validierungsergebnisse."""

from __future__ import annotations

from .models import (
    DiagnosticMessage,
    DiagnosticSeverity,
    ReleaseChoice,
    ReleaseDecision,
    ReleaseStatus,
    ValidationResult,
)


def determine_release_status(messages: tuple[DiagnosticMessage, ...]) -> ReleaseStatus:
    """Leitet den Status streng aus Fehlern und Warnungen ab."""
    if any(message.severity is DiagnosticSeverity.ERROR for message in messages):
        return ReleaseStatus.BLOCKED
    if any(message.severity is DiagnosticSeverity.WARNING for message in messages):
        return ReleaseStatus.CONFIRMATION_REQUIRED
    return ReleaseStatus.RELEASED


def build_validation_result(messages: tuple[DiagnosticMessage, ...]) -> ValidationResult:
    """Erzeugt ein konsistentes Validierungsergebnis."""
    return ValidationResult(
        messages=messages,
        release_status=determine_release_status(messages),
    )


def create_release_decision(
    validation_result: ValidationResult,
    *,
    choice: ReleaseChoice,
    session_id: str,
    run_id: str,
    module_key: str,
    dataset_key: str,
    note: str | None = None,
) -> ReleaseDecision:
    """Prueft und erzeugt eine zulässige Freigabeentscheidung."""
    choice = ReleaseChoice(choice)
    initial_status = validation_result.release_status

    if initial_status is ReleaseStatus.BLOCKED:
        if choice is not ReleaseChoice.KEEP_BLOCKED:
            raise ValueError("Ein Datenstand mit Fehlern darf nicht freigegeben werden.")
        resulting_status = ReleaseStatus.BLOCKED
    elif initial_status is ReleaseStatus.CONFIRMATION_REQUIRED:
        if choice is ReleaseChoice.RELEASE_WITH_WARNINGS:
            resulting_status = ReleaseStatus.RELEASED
        elif choice is ReleaseChoice.KEEP_BLOCKED:
            resulting_status = ReleaseStatus.BLOCKED
        else:
            raise ValueError("Warnungen benoetigen eine ausdrueckliche Entscheidung.")
    else:
        if choice is not ReleaseChoice.AUTOMATIC_RELEASE:
            raise ValueError("Ein fehlerfreier Datenstand wird automatisch freigegeben.")
        resulting_status = ReleaseStatus.RELEASED

    return ReleaseDecision(
        session_id=session_id,
        run_id=run_id,
        module_key=module_key,
        dataset_key=dataset_key,
        choice=choice,
        resulting_status=resulting_status,
        diagnostic_ids=tuple(message.diagnostic_id for message in validation_result.messages),
        note=note.strip() if note and note.strip() else None,
    )
