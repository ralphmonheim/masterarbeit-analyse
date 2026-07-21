"""Kompatibilitaetsliste fuer den manuellen Hauptprozess."""

from __future__ import annotations

from .actions import list_workflow_steps
from .models import WorkflowStep

MAIN_PROCESS_PHASE_KEYS = {"main_process"}


def list_main_process_steps() -> tuple[WorkflowStep, ...]:
    """Gibt Export, manuelle Simulation und Ergebnisimport zurueck."""
    return tuple(step for step in list_workflow_steps() if step.phase_key in MAIN_PROCESS_PHASE_KEYS)
