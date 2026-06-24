"""Geplante Gebaeude- und Zonen-View."""

from __future__ import annotations

from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.widgets import render_placeholder


def render() -> None:
    """Zeigt den geplanten Gebaeudebereich ohne eigene Fachlogik."""
    render_page_header("Gebaeude und Zonen", "Gebaeude- und Modellrandbedingungen")
    render_placeholder("Das Zielmodul ma_building ist geplant und noch nicht fachlich umgesetzt.")
