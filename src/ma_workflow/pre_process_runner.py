"""Kompatibilitaetsliste fuer vorbereitende Workflow-Schritte."""

from __future__ import annotations

from .actions import list_workflow_steps
from .models import WorkflowStep

PRE_PROCESS_PHASE_KEYS = {"pre_process"}


def list_pre_process_steps() -> tuple[WorkflowStep, ...]:
    """Gibt alle Schritte bis einschliesslich Simulation-Setup zurueck."""
    return tuple(step for step in list_workflow_steps() if step.phase_key in PRE_PROCESS_PHASE_KEYS)
