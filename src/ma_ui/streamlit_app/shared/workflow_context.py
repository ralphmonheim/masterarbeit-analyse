"""Workflow-Kontext fuer Modulansichten der zentralen UI."""

from __future__ import annotations

import streamlit as st

from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_workflow import get_workflow_step, list_dashboard_actions


def workflow_context_rows(step_keys: tuple[str, ...]) -> list[dict[str, str]]:
    """Bereitet Workflow-Metadaten fuer eine UI-Tabelle auf."""
    actions_by_step = {action.step_key: action.label for action in list_dashboard_actions()}
    rows: list[dict[str, str]] = []
    for step_key in step_keys:
        step = get_workflow_step(step_key)
        rows.append(
            {
                "Schritt": step.label,
                "Phase": step.phase,
                "Modul": step.module_key,
                "Status": step.status,
                "Dashboard-Aktion": actions_by_step.get(step.step_key, "-"),
                "Beschreibung": step.description,
            }
        )
    return rows


def render_workflow_context(step_keys: tuple[str, ...]) -> None:
    """Zeigt den geplanten Workflow-Kontext fuer eine Modulansicht."""
    st.dataframe(normalize_table_for_streamlit(workflow_context_rows(step_keys)), hide_index=True, width="stretch")
