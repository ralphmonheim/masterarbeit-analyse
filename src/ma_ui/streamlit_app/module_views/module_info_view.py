"""Generische Informationsseite fuer Projektmodule ohne eigene Fachansicht."""

from __future__ import annotations

import streamlit as st

from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_workflow import ModuleDefinition, get_module_definition

STATUS_LABELS = {
    "available": "Verfuegbar",
    "partial": "Teilweise umgesetzt",
    "planned": "Geplant",
    "manual": "Manuell / extern",
}


def _render_text_list(title: str, values: tuple[str, ...]) -> None:
    if not values:
        return
    st.subheader(title)
    for value in values:
        st.markdown(f"- {value}")


def render_module_definition(module: ModuleDefinition) -> None:
    """Zeigt die zentrale Moduldefinition ohne funktionslose Bedienelemente."""
    render_page_header(module.label, module.purpose)
    status_label = STATUS_LABELS.get(module.status, module.status)
    metric_columns = st.columns(3)
    metric_columns[0].metric("Status", status_label)
    metric_columns[1].metric("Bereich", module.category)
    metric_columns[2].metric("Python-Paket", module.python_package or "kein Paket")

    _render_text_list("Eingaben", module.inputs)
    _render_text_list("Ausgaben", module.outputs)
    _render_text_list("Abgrenzung", module.boundaries)
    _render_text_list("Abhaengigkeiten", module.dependencies)

    st.subheader("Naechster Schritt")
    st.info(module.next_step)


def render(module_key: str) -> None:
    """Laedt und zeigt eine Moduldefinition aus dem zentralen Katalog."""
    render_module_definition(get_module_definition(module_key))
