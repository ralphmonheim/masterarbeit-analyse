"""Workflow-Schritte nach der IDA-ICE-Simulation."""

from __future__ import annotations

from .actions import list_workflow_steps
from .models import WorkflowStep

POST_PROCESS_PHASE = "Post-Process"


def list_post_process_steps() -> tuple[WorkflowStep, ...]:
    """Gibt alle geplanten Post-Process-Schritte zurueck."""
    return tuple(step for step in list_workflow_steps() if step.phase == POST_PROCESS_PHASE)
