"""Kompatibilitaetsliste fuer Schritte nach der externen Simulation."""

from __future__ import annotations

from .actions import list_workflow_steps
from .models import WorkflowStep

POST_PROCESS_PHASE_KEYS = {"post_process"}


def list_post_process_steps() -> tuple[WorkflowStep, ...]:
    """Gibt die Schritte ab Datenvorbereitung zurueck."""
    return tuple(
        step
        for step in list_workflow_steps()
        if step.phase_key in POST_PROCESS_PHASE_KEYS and not step.is_external
    )
