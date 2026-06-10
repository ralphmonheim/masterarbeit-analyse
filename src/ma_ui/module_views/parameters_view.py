"""Geplante Parameter-View."""

from __future__ import annotations

from ma_ui.shared.layout import render_page_header
from ma_ui.shared.widgets import render_placeholder
from ma_ui.shared.workflow_context import render_workflow_context


def render() -> None:
    """Zeigt den geplanten Parameterbereich ohne eigene Fachlogik."""
    render_page_header("Parameter", "Parameter- und Optionskatalog")
    render_placeholder("Das Zielmodul ma_parameters ist geplant. Aktuelle Parameterlogik liegt noch in ma_variants.")
    render_workflow_context(("parameters",))
