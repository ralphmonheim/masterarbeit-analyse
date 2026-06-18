"""Geplante View fuer den IDA-Import."""

from __future__ import annotations

from ma_ui.shared.layout import render_page_header
from ma_ui.shared.widgets import render_placeholder


def render() -> None:
    """Zeigt den geplanten IDA-Importbereich ohne eigene Fachlogik."""
    render_page_header("IDA Import", "Zuordnung und Standardisierung von Ergebnisordnern")
    render_placeholder(
        "Ergebnisadapter und Aufbereitung sind teilweise vorhanden. "
        "Das eigenstaendige Zielmodul ma_import_ida ist noch nicht umgesetzt."
    )
