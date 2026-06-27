"""Workflow-Tabellen fuer die zentrale Streamlit-Oberflaeche."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from ma_ui.streamlit_app.shared import normalize_table_for_streamlit
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_workflow import list_workflow_steps

WORKFLOW_ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "workflow"
WORKFLOW_IMAGE_PATH = WORKFLOW_ASSET_DIR / "masterarbeit_workflow.png"
WORKFLOW_PDF_PATH = WORKFLOW_ASSET_DIR / "masterarbeit_workflow.pdf"


def workflow_step_rows() -> list[dict[str, object]]:
    """Bereitet den Gesamtworkflow fuer UI-Tabellen auf."""
    return [
        {
            "Phase": step.phase,
            "Schritt": step.label,
            "Modul": step.module_key,
            "Status": step.status,
            "Beschreibung": step.description,
        }
        for step in list_workflow_steps()
    ]


def workflow_reference_asset_rows() -> list[dict[str, object]]:
    """Listet die eingebundenen Workflow-Referenzdateien fuer Tests und UI."""
    return [
        {
            "Datei": WORKFLOW_IMAGE_PATH.name,
            "Typ": "Bild",
            "Pfad": str(WORKFLOW_IMAGE_PATH),
            "Vorhanden": WORKFLOW_IMAGE_PATH.exists(),
        },
        {
            "Datei": WORKFLOW_PDF_PATH.name,
            "Typ": "PDF",
            "Pfad": str(WORKFLOW_PDF_PATH),
            "Vorhanden": WORKFLOW_PDF_PATH.exists(),
        },
    ]


def render_workflow_reference(*, show_title: bool = True) -> None:
    """Zeigt das externe Workflow-Diagramm und verlinkt die PDF-Fassung."""
    if show_title:
        st.subheader("Workflow-Referenzdiagramm")

    if WORKFLOW_IMAGE_PATH.exists():
        st.image(
            str(WORKFLOW_IMAGE_PATH),
            caption="Workflow-Referenz aus der aktuellen Projektplanung",
            width="stretch",
        )
    else:
        st.info(f"Workflow-Bild noch nicht gefunden: `{WORKFLOW_IMAGE_PATH}`")

    if WORKFLOW_PDF_PATH.exists():
        st.download_button(
            "Workflow-PDF herunterladen",
            data=WORKFLOW_PDF_PATH.read_bytes(),
            file_name=WORKFLOW_PDF_PATH.name,
            mime="application/pdf",
            type="secondary",
        )
    else:
        st.caption(f"Workflow-PDF noch nicht gefunden: `{WORKFLOW_PDF_PATH}`")


def render() -> None:
    """Zeigt die ma_workflow-Modulansicht mit Referenzdiagramm und Schritten."""
    render_page_header("Workflow-Steuerung", "Prozessbild, Modulstatus und Workflow-Schritte")
    render_workflow_reference()
    st.subheader("Workflow-Schritte")
    st.dataframe(
        normalize_table_for_streamlit(pd.DataFrame(workflow_step_rows())),
        hide_index=True,
        width="stretch",
    )
