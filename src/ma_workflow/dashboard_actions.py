"""Dashboard-Aktionen zwischen Streamlit-UI und Workflow-Schicht."""

from __future__ import annotations

from .actions import get_workflow_step
from .models import WorkflowAction

_ACTION_TO_STEP: tuple[tuple[str, str, str], ...] = (
    ("open_core", "Technische Grundlagen oeffnen", "core"),
    ("open_database", "Datenbank oeffnen", "database"),
    ("open_ui", "Benutzeroberflaeche oeffnen", "ui"),
    ("open_workflow", "Workflow-Steuerung oeffnen", "workflow"),
    ("open_documentation", "Dokumentation oeffnen", "documentation_infrastructure"),
    ("open_project", "Projekt oeffnen", "project"),
    ("open_parameters", "Parameter oeffnen", "parameters"),
    ("open_weather", "Wetterdaten oeffnen", "weather"),
    ("open_building", "Gebaeude oeffnen", "building"),
    ("open_zones", "Zonen oeffnen", "zones"),
    ("open_technical", "Technik oeffnen", "technical"),
    ("open_dimensioning", "Dimensionierung oeffnen", "dimensioning"),
    ("open_variants", "Varianten oeffnen", "variants"),
    ("open_simulation_setup", "Simulation konfigurieren", "simulation_setup"),
    ("run_simulation_export", "Simulationsexport starten", "export_simulation"),
    ("run_simulation_import", "Simulationsergebnisimport starten", "import_simulation"),
    ("run_data_preparation", "Daten vorbereiten", "data_preparation"),
    ("run_optimization", "Optimierung analysieren", "optimization"),
    ("run_standards_compliance", "Norm-Nachweis oeffnen", "standards_compliance"),
    ("run_sensitivity", "Sensitivitaet analysieren", "sensitivity"),
    ("run_economy", "Wirtschaftlichkeit starten", "economy"),
    ("run_sustainability", "Nachhaltigkeit starten", "sustainability"),
    ("run_assessment", "Bewertung starten", "assessment"),
    ("run_reporting", "Reporting starten", "reporting"),
    ("run_data_export", "Datenexport starten", "data_export"),
    ("open_validation", "Validierung oeffnen", "validation"),
    ("open_feedback", "Feedback oeffnen", "feedback"),
)

ACTION_KEY_ALIASES = {
    "run_analysis": "run_optimization",
    "run_analyze_data": "run_data_preparation",
    "run_prepare": "run_data_preparation",
    "run_prepare_data": "run_data_preparation",
    "run_ida_export": "run_simulation_export",
    "run_ida_import": "run_simulation_import",
}


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
    """Findet eine Dashboard-Aktion einschliesslich Uebergangsaliase."""
    canonical_key = ACTION_KEY_ALIASES.get(action_key, action_key)
    for action in list_dashboard_actions():
        if action.action_key == canonical_key:
            return action
    raise KeyError(f"Unbekannte Dashboard-Aktion: {action_key}")
