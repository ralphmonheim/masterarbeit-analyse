"""Anzeigehelfer fuer ma_analyse-Ergebnisse."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from ma_analyse.models import AnalysisResult
from ma_ui.shared import file_rows


def created_file_rows(paths: list[Path]) -> list[dict[str, object]]:
    """Bereitet erzeugte Dateien fuer eine UI-Tabelle auf."""
    return file_rows(paths)


def render_analysis_result(result: AnalysisResult) -> None:
    """Zeigt ein Analyseergebnis in Streamlit an."""
    if result.success:
        st.success("Analyse abgeschlossen.")
    else:
        st.error("Analyse konnte nicht erfolgreich abgeschlossen werden.")

    if result.errors:
        st.subheader("Fehler")
        st.json(result.errors)

    if result.warnings:
        st.subheader("Hinweise")
        st.json(result.warnings)

    if result.created_files:
        st.subheader("Erzeugte Dateien")
        st.dataframe(created_file_rows(result.created_files), hide_index=True, use_container_width=True)

    if result.log_text:
        st.subheader("Log")
        st.text_area("Ausgabe", value=result.log_text, height=280, label_visibility="collapsed")
