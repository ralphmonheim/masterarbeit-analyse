"""Geplante View fuer Simulationsrandbedingungen."""

from __future__ import annotations

from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.widgets import render_placeholder


def render() -> None:
    """Zeigt den geplanten Simulation-Setup-Bereich ohne eigene Fachlogik."""
    render_page_header("Simulation vorbereiten", "Zeitraum, Zeitschritt, Szenario und Run-Metadaten")
    render_placeholder("ma_simulation_setup wird spaeter zwischen Variantenbildung und IDA-Export umgesetzt.")
