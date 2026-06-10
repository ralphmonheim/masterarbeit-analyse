"""Zentraler Zugriff auf den geplanten Gesamtworkflow."""

from __future__ import annotations

from .actions import get_workflow_step, list_workflow_steps, steps_by_phase
from .models import WorkflowStep


def list_steps() -> tuple[WorkflowStep, ...]:
    """Gibt alle bekannten Workflow-Schritte zurueck."""
    return list_workflow_steps()


def get_step(step_key: str) -> WorkflowStep:
    """Findet einen Workflow-Schritt ueber seinen technischen Key."""
    return get_workflow_step(step_key)


def group_steps_by_phase() -> dict[str, tuple[WorkflowStep, ...]]:
    """Gruppiert Workflow-Schritte nach Prozessphase."""
    return steps_by_phase()
