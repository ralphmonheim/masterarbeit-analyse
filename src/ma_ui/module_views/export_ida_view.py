"""Geplante View fuer den IDA-Export."""

from __future__ import annotations

from ma_ui.shared.layout import render_page_header
from ma_ui.shared.widgets import render_placeholder
from ma_ui.shared.workflow_context import render_workflow_context


def render() -> None:
    """Zeigt den geplanten IDA-Exportbereich ohne eigene Fachlogik."""
    render_page_header("IDA Export", "Vorbereitung der IDA-ICE-Uebergabe")
    render_placeholder("IDA-Exportlogik liegt aktuell im Variantenmodul und wird spaeter getrennt geplant.")
    render_workflow_context(("ida_export",))
