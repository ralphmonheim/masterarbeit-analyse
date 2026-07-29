"""Startseite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

from collections import Counter
from html import escape

import pandas as pd
import streamlit as st

from ma_ui.streamlit_app.main_dashboard import dashboard_action_rows
from ma_ui.streamlit_app.navigation import (
    get_navigation_pages,
    select_page,
)
from ma_ui.streamlit_app.shared import normalize_table_for_streamlit
from ma_ui.streamlit_app.workflow_graph import (
    CROSS_CUTTING_LABEL,
    TECHNICAL_PLATFORM_LABEL,
    VISUAL_PHASES,
    WorkflowCard,
    cross_cutting_card_rows,
    feedback_path_rows,
    status_style,
    technical_platform_card_rows,
    workflow_card_rows,
    workflow_cards_by_phase,
)
from ma_ui.streamlit_app.workflow_view import workflow_step_rows
from ma_workflow import ModuleDefinition, list_module_definitions

STATUS_LABELS = {
    "available": "Verfuegbar",
    "partial": "Teilweise",
    "planned": "Geplant",
    "manual": "Manuell",
}
CARDS_PER_ROW = 4
_SECONDARY_STATUS_PILLS = {"weather": ("Diagramme", "partial")}
CATEGORY_LABELS = {
    "workflow": "Fachmodule",
    "cross_cutting": "Querschnittsmodule",
    "infrastructure": "Technische Plattform",
    "documentation": "Dokumentation",
    "external": "Externe Werkzeuge",
}


def workflow_status_counts(rows: list[dict[str, object]] | None = None) -> dict[str, int]:
    """Zaehlt Workflow-Schritte nach Umsetzungsstatus."""
    workflow_rows = rows if rows is not None else workflow_step_rows()
    return dict(Counter(str(row["Status"]) for row in workflow_rows))


def workflow_phase_summary_rows(rows: list[dict[str, object]] | None = None) -> list[dict[str, object]]:
    """Fasst Workflow-Schritte nach Prozessphase zusammen."""
    workflow_rows = rows if rows is not None else workflow_step_rows()
    summary: dict[str, dict[str, object]] = {}

    for row in workflow_rows:
        phase = str(row["Phase"])
        entry = summary.setdefault(
            phase,
            {
                "Phase": phase,
                "Schritte": 0,
                "Module": [],
            },
        )
        entry["Schritte"] = int(entry["Schritte"]) + 1
        modules = entry["Module"]
        if isinstance(modules, list):
            modules.append(str(row["Modul"]))

    return [
        {
            "Phase": entry["Phase"],
            "Schritte": entry["Schritte"],
            "Module": ", ".join(entry["Module"]) if isinstance(entry["Module"], list) else "",
        }
        for entry in summary.values()
    ]


def module_overview_rows(
    modules: tuple[ModuleDefinition, ...] | None = None,
) -> list[dict[str, object]]:
    """Bereitet den Modulkatalog ohne Workflow-Reihenfolge fuer die Bearbeitungsansicht auf."""
    module_definitions = modules if modules is not None else list_module_definitions()
    return [
        {
            "Modul": module.label,
            "Modul-Key": module.module_key,
            "Kategorie": CATEGORY_LABELS.get(module.category, module.category),
            "Status": module.status,
            "Beschreibung": module.purpose,
            "Zielseite": module.page_key,
        }
        for module in module_definitions
    ]


def _available_page_keys() -> tuple[str, ...]:
    return tuple(page.page_key for page in get_navigation_pages())


def _navigate_to(page_key: str) -> None:
    select_page(st.session_state, page_key)
    st.rerun()


def _render_dashboard_styles() -> None:
    st.markdown(
        """
        <style>
        .workflow-card {
            border: 1px solid rgba(49, 95, 173, 0.18);
            border-radius: 8px;
            padding: 0.75rem;
            margin: 0.45rem 0;
            background: #ffffff;
            min-height: 9.5rem;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
        }
        .workflow-card-title {
            font-weight: 700;
            margin-bottom: 0.25rem;
            color: #111827;
        }
        .workflow-card-module {
            font-size: 0.78rem;
            color: #4B5563;
            margin-bottom: 0.45rem;
        }
        .workflow-card-description {
            color: #374151;
            font-size: 0.84rem;
            line-height: 1.3;
            min-height: 2.8rem;
        }
        .workflow-status-pill {
            display: inline-block;
            border-radius: 999px;
            padding: 0.12rem 0.48rem;
            font-size: 0.74rem;
            font-weight: 650;
            margin-bottom: 0.4rem;
        }
        .feedback-card {
            border-left: 4px solid #F59E0B;
            background: #FFFBEB;
            border-radius: 6px;
            padding: 0.65rem;
            min-height: 7rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _workflow_card_html(card: WorkflowCard) -> str:
    secondary_status = _SECONDARY_STATUS_PILLS.get(card.step_key)
    secondary_pill = ""
    if secondary_status:
        label, status = secondary_status
        style = status_style(status)
        secondary_pill = f"""
      <div class="workflow-status-pill" style="background:{style["background"]}; color:{style["color"]};">
        {escape(label)} – {escape(style["label"])}
      </div>"""
    return f"""
    <div class="workflow-card">
      <div class="workflow-status-pill" style="background:{card.status_background}; color:{card.status_color};">
        {escape(card.status_label)}
      </div>{secondary_pill}
      <div class="workflow-card-title">{escape(card.label)}</div>
      <div class="workflow-card-module">{escape(card.module_key)}</div>
      <div class="workflow-card-description">{escape(card.description)}</div>
    </div>
    """


def _module_card_html(module: ModuleDefinition) -> str:
    style = status_style(module.status)
    return f"""
    <div class="workflow-card">
      <div class="workflow-status-pill" style="background:{style["background"]}; color:{style["color"]};">
        {escape(style["label"])}
      </div>
      <div class="workflow-card-title">{escape(module.label)}</div>
      <div class="workflow-card-module">{escape(module.module_key)}</div>
      <div class="workflow-card-description">{escape(module.purpose)}</div>
    </div>
    """


def _render_module_card(module: ModuleDefinition, available_page_keys: tuple[str, ...]) -> None:
    st.markdown(_module_card_html(module), unsafe_allow_html=True)
    if module.page_key in available_page_keys:
        if st.button("Oeffnen", key=f"module_card_open_{module.module_key}", width="stretch"):
            _navigate_to(module.page_key)
    else:
        st.caption("Noch keine eigene Modulansicht.")


def _render_module_category(
    category: str,
    modules: list[ModuleDefinition],
    available_page_keys: tuple[str, ...],
) -> None:
    st.markdown(f"### {CATEGORY_LABELS.get(category, category)}")
    for start_index in range(0, len(modules), CARDS_PER_ROW):
        row_modules = modules[start_index : start_index + CARDS_PER_ROW]
        columns = st.columns(len(row_modules))
        for column, module in zip(columns, row_modules, strict=False):
            with column:
                _render_module_card(module, available_page_keys)


def _render_workflow_card(card: WorkflowCard) -> None:
    st.markdown(_workflow_card_html(card), unsafe_allow_html=True)
    if card.target_page_key:
        if st.button("Oeffnen", key=f"workflow_card_open_{card.step_key}", width="stretch"):
            _navigate_to(card.target_page_key)
    else:
        st.caption("Manueller oder externer Schritt.")


def _render_phase_cards(phase: str, phase_cards: list[WorkflowCard]) -> None:
    st.markdown(f"### {phase}")
    if not phase_cards:
        st.caption("Noch keine Schritte.")
        return

    for start_index in range(0, len(phase_cards), CARDS_PER_ROW):
        row_cards = phase_cards[start_index : start_index + CARDS_PER_ROW]
        columns = st.columns(len(row_cards))
        for column, card in zip(columns, row_cards, strict=False):
            with column:
                _render_workflow_card(card)


def _render_feedback_paths() -> None:
    st.subheader("Iterationspfade")
    feedback_columns = st.columns(3)
    for column, row in zip(feedback_columns, feedback_path_rows(), strict=False):
        with column:
            st.markdown(
                f"""
                <div class="feedback-card">
                  <strong>{escape(row["Frage"])}</strong><br>
                  <span>{escape(row["Ruecksprung"])}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Ziel oeffnen", key=f"feedback_open_{row['Zielseite']}", width="stretch"):
                _navigate_to(row["Zielseite"])


def render_workflow_overview() -> None:
    """Zeigt die gefuehrte Reihenfolge als eigenstaendige Workflowansicht."""
    _render_dashboard_styles()
    st.title("Masterarbeit Workflowansicht")
    st.caption("Gefuehrte Reihenfolge, Umsetzungsstand und fachliche Einstiegspunkte.")

    workflow_rows = workflow_step_rows()
    status_counts = workflow_status_counts(workflow_rows)
    status_columns = st.columns(len(STATUS_LABELS))
    for column, (status_key, label) in zip(status_columns, STATUS_LABELS.items(), strict=False):
        column.metric(label, status_counts.get(status_key, 0))

    st.subheader("Modul-Ansicht")
    cards = workflow_card_rows(available_page_keys=_available_page_keys())
    cards_by_phase = workflow_cards_by_phase(cards)
    for phase in VISUAL_PHASES:
        _render_phase_cards(phase, cards_by_phase.get(phase, []))

    _render_phase_cards(
        CROSS_CUTTING_LABEL,
        cross_cutting_card_rows(available_page_keys=_available_page_keys()),
    )

    _render_phase_cards(
        TECHNICAL_PLATFORM_LABEL,
        technical_platform_card_rows(available_page_keys=_available_page_keys()),
    )

    with st.expander("Technische Detailtabellen", expanded=False):
        st.subheader("Workflow-Phasen")
        st.dataframe(
            normalize_table_for_streamlit(pd.DataFrame(workflow_phase_summary_rows(workflow_rows))),
            hide_index=True,
            width="stretch",
        )

        st.subheader("Workflow-Schritte")
        st.dataframe(normalize_table_for_streamlit(pd.DataFrame(workflow_rows)), hide_index=True, width="stretch")

        st.subheader("Dashboard-Aktionen")
        st.dataframe(
            normalize_table_for_streamlit(pd.DataFrame(dashboard_action_rows())),
            hide_index=True,
            width="stretch",
        )


def render() -> None:
    """Zeigt die Module unabhaengig von ihrer Reihenfolge im Workflow."""
    _render_dashboard_styles()
    st.title("Masterarbeit Bearbeitungsansicht")
    st.caption("Fachmodule und unterstuetzende Projektmodule als direkte Bearbeitungseinstiege.")

    modules = list_module_definitions()
    status_counts = Counter(module.status for module in modules)
    status_columns = st.columns(len(STATUS_LABELS))
    for column, (status_key, label) in zip(status_columns, STATUS_LABELS.items(), strict=False):
        column.metric(label, status_counts.get(status_key, 0))

    available_page_keys = _available_page_keys()
    modules_by_category: dict[str, list[ModuleDefinition]] = {}
    for module in modules:
        modules_by_category.setdefault(module.category, []).append(module)

    for category in CATEGORY_LABELS:
        category_modules = modules_by_category.get(category, [])
        if category_modules:
            _render_module_category(category, category_modules, available_page_keys)

    with st.expander("Modulkatalog", expanded=False):
        st.dataframe(
            normalize_table_for_streamlit(pd.DataFrame(module_overview_rows(modules))),
            hide_index=True,
            width="stretch",
        )
