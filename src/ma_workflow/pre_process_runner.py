"""Vorbereitende Workflow-Schritte vor der IDA-ICE-Simulation."""

from __future__ import annotations

from .actions import list_workflow_steps
from .models import WorkflowStep

PRE_PROCESS_PHASE = "Pre-Process"


def list_pre_process_steps() -> tuple[WorkflowStep, ...]:
    """Gibt alle geplanten Pre-Process-Schritte zurueck."""
    return tuple(step for step in list_workflow_steps() if step.phase == PRE_PROCESS_PHASE)
