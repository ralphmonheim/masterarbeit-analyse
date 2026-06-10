"""Geplante View fuer Simulationsrandbedingungen."""

from __future__ import annotations

from ma_ui.shared.layout import render_page_header
from ma_ui.shared.widgets import render_placeholder
from ma_ui.shared.workflow_context import render_workflow_context


def render() -> None:
    """Zeigt den geplanten Simulation-Setup-Bereich ohne eigene Fachlogik."""
    render_page_header("Simulation vorbereiten", "Zeitraum, Zeitschritt, Szenario und Run-Metadaten")
    render_placeholder("ma_simulation_setup wird spaeter zwischen Variantenbildung und IDA-Export umgesetzt.")
    render_workflow_context(("simulation_setup",))
