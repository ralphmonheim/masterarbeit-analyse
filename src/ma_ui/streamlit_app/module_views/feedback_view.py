"""Geplante Feedback-View."""

from __future__ import annotations

from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.widgets import render_placeholder


def render() -> None:
    """Zeigt den geplanten Feedbackbereich ohne eigene Fachlogik."""
    render_page_header("Feedback", "Rueckfuehrung von Auffaelligkeiten in fruehere Workflow-Schritte")
    render_placeholder("ma_feedback ist geplant und wird erst nach stabilen Analyse- und Bewertungsdaten umgesetzt.")
