"""Datenmodelle fuer die moduluebergreifende Workflow-Steuerung."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowStep:
    """Beschreibt einen Schritt im Gesamtworkflow der Masterarbeit."""

    step_key: str
    label: str
    phase: str
    module_key: str
    status: str
    description: str


@dataclass(frozen=True, slots=True)
class WorkflowAction:
    """Beschreibt eine UI-Aktion, die auf einen Workflow-Schritt verweist."""

    action_key: str
    label: str
    step_key: str
    module_key: str
    status: str
    description: str
