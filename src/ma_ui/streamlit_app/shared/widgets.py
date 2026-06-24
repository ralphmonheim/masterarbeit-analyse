"""Kleine UI-Widgets ohne Fachlogik."""

from __future__ import annotations

import streamlit as st

from ma_ui.streamlit_app.resource_status import resource_status_rows
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit


def render_placeholder(message: str) -> None:
    """Zeigt einen neutralen Platzhalter fuer geplante Funktionen."""
    st.info(message)


def render_resource_status(step_key: str) -> None:
    """Zeigt vorhandene Projektressourcen fuer einen geplanten Workflow-Schritt."""
    rows = resource_status_rows(step_key)
    if not rows:
        return
    st.subheader("Vorhandene Projektressourcen")
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")
