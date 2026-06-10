"""Geplante Gebaeude- und Zonen-View."""

from __future__ import annotations

from ma_ui.shared.layout import render_page_header
from ma_ui.shared.widgets import render_placeholder
from ma_ui.shared.workflow_context import render_workflow_context


def render() -> None:
    """Zeigt den geplanten Gebaeudebereich ohne eigene Fachlogik."""
    render_page_header("Gebaeude und Zonen", "Gebaeude- und Modellrandbedingungen")
    render_placeholder("Das Zielmodul ma_building ist geplant und noch nicht fachlich umgesetzt.")
    render_workflow_context(("building",))
