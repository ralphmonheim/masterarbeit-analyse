"""Kompatibilitaetsview fuer den allgemeinen Simulationsergebnisimport."""

from __future__ import annotations

from ma_ui.streamlit_app.module_views.module_info_view import render as render_module_info


def render() -> None:
    """Leitet den historischen View-Namen auf die kanonische Infoseite."""
    render_module_info("ma_import_simulation")
