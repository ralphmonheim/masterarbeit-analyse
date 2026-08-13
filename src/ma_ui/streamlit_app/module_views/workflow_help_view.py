"""Nutzungsorientierte Hilfe aus den fachlichen Workflow-Steckbriefen."""

from __future__ import annotations

import streamlit as st

from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_workflow import get_module_definition, load_workflow_module_guide


def _guide_body(markdown: str) -> str:
    """Entfernt nur die bereits als UI-Kopf dargestellte Dokumentüberschrift."""

    return markdown.split("\n", 1)[1] if "\n" in markdown else markdown


def render(module_key: str) -> None:
    """Rendert Hilfe zum Ablauf ohne technische Plan- oder Testinformationen."""

    module = get_module_definition(module_key)
    guide = load_workflow_module_guide(module.module_key)
    render_page_header(
        f"Hilfe zum Ablauf: {module.label}",
        "Fachliche Rolle, Übergaben, Begriffe und Bedienhinweise aus dem zentralen Workflow-Steckbrief.",
    )
    st.caption(f"Quelle: `{guide.path.relative_to(guide.path.parents[3])}`")
    st.markdown(_guide_body(guide.markdown))
