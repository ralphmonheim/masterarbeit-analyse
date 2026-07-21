"""UI-neutrale Daten fuer das grafische Workflow-Dashboard."""

from __future__ import annotations

from dataclasses import dataclass

from ma_workflow import (
    get_module_definition,
    get_workflow_step,
    list_cross_cutting_steps,
    list_workflow_phases,
    list_workflow_steps,
)
from ma_workflow.models import WorkflowStep

VISUAL_PHASES = tuple(phase.label for phase in list_workflow_phases())
TECHNICAL_PLATFORM_LABEL = "Technische Plattform"
CROSS_CUTTING_LABEL = "Phasenuebergreifend"

STATUS_STYLES = {
    "available": {"label": "Verfuegbar", "color": "#1F8F4D", "background": "#E7F6EC"},
    "partial": {"label": "Teilweise", "color": "#8A5A00", "background": "#FFF3D8"},
    "planned": {"label": "Geplant", "color": "#315FAD", "background": "#EAF1FF"},
    "manual": {"label": "Manuell", "color": "#6B7280", "background": "#F3F4F6"},
}
DEFAULT_STATUS_STYLE = {"label": "Unklar", "color": "#4B5563", "background": "#F3F4F6"}

@dataclass(frozen=True, slots=True)
class WorkflowCard:
    """Beschreibt eine grafische Workflow-Karte fuer die Startseite."""

    step_key: str
    label: str
    visual_phase: str
    module_key: str
    status: str
    status_label: str
    status_color: str
    status_background: str
    description: str
    target_page_key: str | None


def status_style(status: str) -> dict[str, str]:
    """Gibt Label und Farben fuer einen Workflow-Status zurueck."""
    return STATUS_STYLES.get(status, DEFAULT_STATUS_STYLE)


def visual_phase_for_step(step: WorkflowStep) -> str:
    """Ordnet Workflow-Schritte dem visuellen Dashboard-Phasenmodell zu."""
    return step.phase


def target_page_for_step(step_key: str, available_page_keys: tuple[str, ...]) -> str | None:
    """Leitet die Zielseite fuer einen Workflow-Schritt ab."""
    try:
        step = get_workflow_step(step_key)
    except KeyError:
        return None
    page_key = get_module_definition(step.module_key).page_key
    return page_key if page_key in available_page_keys else None


def workflow_card_rows(
    *,
    steps: tuple[WorkflowStep, ...] | None = None,
    available_page_keys: tuple[str, ...] = (),
) -> list[WorkflowCard]:
    """Bereitet Workflow-Schritte als Karten fuer das grafische Dashboard auf."""
    workflow_steps = steps if steps is not None else tuple(
        step for step in list_workflow_steps() if step.phase_key != "cross_cutting"
    )
    cards: list[WorkflowCard] = []
    for step in workflow_steps:
        style = status_style(step.status)
        cards.append(
            WorkflowCard(
                step_key=step.step_key,
                label=step.label,
                visual_phase=visual_phase_for_step(step),
                module_key=step.module_key,
                status=step.status,
                status_label=style["label"],
                status_color=style["color"],
                status_background=style["background"],
                description=step.description,
                target_page_key=target_page_for_step(step.step_key, available_page_keys),
            )
        )
    return cards


def workflow_cards_by_phase(cards: list[WorkflowCard] | None = None) -> dict[str, list[WorkflowCard]]:
    """Gruppiert Workflow-Karten nach der visuellen Prozessphase."""
    resolved_cards = cards if cards is not None else workflow_card_rows()
    grouped = {phase: [] for phase in VISUAL_PHASES}
    for card in resolved_cards:
        grouped.setdefault(card.visual_phase, []).append(card)
    return grouped


def cross_cutting_card_rows(*, available_page_keys: tuple[str, ...] = ()) -> list[WorkflowCard]:
    """Bereitet Validierung und Feedback als eigenen Dashboard-Bereich auf."""
    return workflow_card_rows(
        steps=list_cross_cutting_steps(),
        available_page_keys=available_page_keys,
    )


def technical_platform_card_rows(*, available_page_keys: tuple[str, ...] = ()) -> list[WorkflowCard]:
    """Bereitet die technischen Grundlagen als eigenen Dashboard-Bereich auf."""
    platform_steps = tuple(
        step
        for step in list_workflow_steps()
        if step.phase_key == "cross_cutting" and not step.is_cross_cutting
    )
    return workflow_card_rows(
        steps=platform_steps,
        available_page_keys=available_page_keys,
    )


def feedback_path_rows() -> list[dict[str, str]]:
    """Gibt die Iterationspfade aus dem grafischen Workflow als UI-Daten zurueck."""
    return [
        {
            "Frage": "Model good?",
            "Ruecksprung": "Eingaben pruefen, Parameter und Varianten anpassen",
            "Zielseite": "parameters",
        },
        {
            "Frage": "Data good?",
            "Ruecksprung": "Simulationsergebnisimport und Datenanalyse pruefen",
            "Zielseite": "import_simulation",
        },
        {
            "Frage": "Room for Optimization?",
            "Ruecksprung": "Variantenbildung oder Simulation Setup anpassen",
            "Zielseite": "variants",
        },
    ]
