"""Dashboard-Aktionen zwischen Streamlit-UI und Workflow-Schicht."""

from __future__ import annotations

from .actions import get_workflow_step
from .models import WorkflowAction

_ACTION_TO_STEP: tuple[tuple[str, str, str], ...] = (
    ("open_parameters", "Parameter oeffnen", "parameters"),
    ("open_weather", "Wetterdaten oeffnen", "weather"),
    ("open_building", "Gebaeude oeffnen", "building"),
    ("open_variants", "Varianten oeffnen", "variants"),
    ("open_simulation_setup", "Simulation konfigurieren", "simulation_setup"),
    ("run_ida_export", "IDA-Export starten", "ida_export"),
    ("run_ida_import", "IDA-Import starten", "ida_import"),
    ("run_analysis", "Analyse starten", "analyse"),
    ("run_assessment", "Bewertung starten", "assessment"),
    ("open_feedback", "Feedback oeffnen", "feedback"),
)


def list_dashboard_actions() -> tuple[WorkflowAction, ...]:
    """Gibt die geplanten Dashboard-Aktionen zurueck."""
    actions: list[WorkflowAction] = []
    for action_key, label, step_key in _ACTION_TO_STEP:
        step = get_workflow_step(step_key)
        actions.append(
            WorkflowAction(
                action_key=action_key,
                label=label,
                step_key=step.step_key,
                module_key=step.module_key,
                status=step.status,
                description=step.description,
            )
        )
    return tuple(actions)


def get_dashboard_action(action_key: str) -> WorkflowAction:
    """Findet eine Dashboard-Aktion ueber ihren technischen Key."""
    for action in list_dashboard_actions():
        if action.action_key == action_key:
            return action
    raise KeyError(f"Unbekannte Dashboard-Aktion: {action_key}")
