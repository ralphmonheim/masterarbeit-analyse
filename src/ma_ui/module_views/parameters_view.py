"""Geplante Parameter-View."""

from __future__ import annotations

from ma_ui.shared.layout import render_page_header
from ma_ui.shared.widgets import render_placeholder


def render() -> None:
    """Zeigt den geplanten Parameterbereich ohne eigene Fachlogik."""
    render_page_header("Parameter", "Parameter- und Optionskatalog")
    render_placeholder(
        "Parameter- und Optionslogik ist teilweise in ma_variants vorhanden. "
        "Das eigenstaendige Zielmodul ma_parameters fehlt noch."
    )
