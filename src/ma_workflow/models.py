"""Datenmodelle fuer die moduluebergreifende Workflow-Steuerung."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowPhase:
    """Beschreibt eine verbindliche Phase des Gesamtworkflows."""

    phase_key: str
    label: str
    order: int
    description: str


@dataclass(frozen=True, slots=True)
class ModuleDefinition:
    """Beschreibt Rolle, Grenzen und Status eines Projektmoduls."""

    module_key: str
    label: str
    page_key: str
    status: str
    category: str
    purpose: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    boundaries: tuple[str, ...]
    dependencies: tuple[str, ...]
    next_step: str
    python_package: str | None = None


@dataclass(frozen=True, slots=True)
class WorkflowStep:
    """Beschreibt einen Schritt im Gesamtworkflow der Masterarbeit."""

    step_key: str
    label: str
    phase: str
    module_key: str
    status: str
    description: str
    phase_key: str = ""
    is_cross_cutting: bool = False
    is_external: bool = False


@dataclass(frozen=True, slots=True)
class WorkflowAction:
    """Beschreibt eine UI-Aktion, die auf einen Workflow-Schritt verweist."""

    action_key: str
    label: str
    step_key: str
    module_key: str
    status: str
    description: str
