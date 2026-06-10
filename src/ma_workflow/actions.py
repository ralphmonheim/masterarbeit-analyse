"""Workflow-Katalog und einfache Nachschlagefunktionen."""

from __future__ import annotations

from collections import defaultdict

from .models import WorkflowStep

_WORKFLOW_STEPS: tuple[WorkflowStep, ...] = (
    WorkflowStep(
        step_key="parameters",
        label="Parameter",
        phase="Pre-Process",
        module_key="ma_parameters",
        status="planned",
        description="Parameter- und Optionskatalog als spaeteres eigenes Fachmodul.",
    ),
    WorkflowStep(
        step_key="weather",
        label="Wetterdaten",
        phase="Pre-Process",
        module_key="ma_weather",
        status="partial",
        description="Wetterkatalog ist vorbereitet; TRY-Importlogik folgt spaeter.",
    ),
    WorkflowStep(
        step_key="building",
        label="Gebaeude und Zonen",
        phase="Pre-Process",
        module_key="ma_building",
        status="planned",
        description="Gebaeude- und Zonendaten sind Zielmodul, aber noch nicht umgesetzt.",
    ),
    WorkflowStep(
        step_key="variants",
        label="Varianten",
        phase="Pre-Process",
        module_key="ma_variants",
        status="available",
        description="Variantenkern mit Katalogen, Auswahl, Naming und Exporten.",
    ),
    WorkflowStep(
        step_key="simulation_setup",
        label="Simulation vorbereiten",
        phase="Pre-Process",
        module_key="ma_simulation_setup",
        status="planned",
        description="Simulationsrandbedingungen und Run-Metadaten werden spaeter getrennt.",
    ),
    WorkflowStep(
        step_key="ida_export",
        label="IDA Export",
        phase="Pre-Process",
        module_key="ma_export_ida",
        status="partial",
        description="IDA-Uebergabestruktur existiert aktuell im Variantenmodul.",
    ),
    WorkflowStep(
        step_key="simulation",
        label="IDA ICE Simulation",
        phase="Simulation",
        module_key="ida_ice",
        status="manual",
        description="Simulation erfolgt weiterhin manuell oder extern in IDA ICE.",
    ),
    WorkflowStep(
        step_key="ida_import",
        label="IDA Import",
        phase="Post-Process",
        module_key="ma_import_ida",
        status="planned",
        description="Import und Standardisierung der Simulationsergebnisse werden spaeter getrennt.",
    ),
    WorkflowStep(
        step_key="analyse",
        label="Analyse",
        phase="Post-Process",
        module_key="ma_analyse",
        status="available",
        description="Simulationsergebnisanalyse mit erster UI-neutraler Service-Fassade.",
    ),
    WorkflowStep(
        step_key="assessment",
        label="Bewertung",
        phase="Post-Process",
        module_key="ma_assessment",
        status="partial",
        description="Generische Wirtschaftlichkeit existiert aktuell im Variantenmodul.",
    ),
    WorkflowStep(
        step_key="feedback",
        label="Feedback",
        phase="Feedback",
        module_key="ma_feedback",
        status="planned",
        description="Problembehandlung und Rueckfuehrung in fruehere Workflow-Schritte.",
    ),
)


def list_workflow_steps() -> tuple[WorkflowStep, ...]:
    """Gibt den aktuellen geplanten Gesamtworkflow zurueck."""
    return _WORKFLOW_STEPS


def get_workflow_step(step_key: str) -> WorkflowStep:
    """Findet einen Workflow-Schritt ueber seinen technischen Key."""
    for step in _WORKFLOW_STEPS:
        if step.step_key == step_key:
            return step
    raise KeyError(f"Unbekannter Workflow-Schritt: {step_key}")


def steps_by_phase() -> dict[str, tuple[WorkflowStep, ...]]:
    """Gruppiert Workflow-Schritte nach Prozessphase."""
    grouped: defaultdict[str, list[WorkflowStep]] = defaultdict(list)
    for step in _WORKFLOW_STEPS:
        grouped[step.phase].append(step)
    return {phase: tuple(steps) for phase, steps in grouped.items()}
