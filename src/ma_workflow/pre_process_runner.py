"""Kompatibilitaetsliste fuer vorbereitende Workflow-Schritte."""

from __future__ import annotations

from .actions import list_workflow_steps
from .models import WorkflowStep

PRE_PROCESS_PHASE_KEYS = {"phase_2", "phase_3"}


def list_pre_process_steps() -> tuple[WorkflowStep, ...]:
    """Gibt die Schritte der P007-Phasen 2 und 3 zurueck."""
    return tuple(step for step in list_workflow_steps() if step.phase_key in PRE_PROCESS_PHASE_KEYS)
