"""Anzeigehelfer fuer ma_analyse-Ergebnisse."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from ma_analyse.models import AnalysisResult
from ma_ui.streamlit_app.shared import file_rows, normalize_table_for_streamlit

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}


def created_file_rows(paths: list[Path]) -> list[dict[str, object]]:
    """Bereitet erzeugte Dateien fuer eine UI-Tabelle auf."""
    return file_rows(paths)


def is_preview_image(path: Path) -> bool:
    """Prueft, ob eine erzeugte Datei als Bildvorschau angezeigt werden kann."""
    return path.suffix.lower() in IMAGE_SUFFIXES


def preview_image_paths(paths: list[Path]) -> list[Path]:
    """Filtert erzeugte Dateien auf lokal vorhandene Bilddateien."""
    return [path for path in paths if is_preview_image(path) and path.exists()]


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
        images = preview_image_paths(result.created_files)
        if images:
            st.subheader("Diagrammvorschau")
            for image_path in images:
                st.image(str(image_path), caption=image_path.name)

        st.subheader("Erzeugte Dateien")
        st.dataframe(
            normalize_table_for_streamlit(created_file_rows(result.created_files)),
            hide_index=True,
            width="stretch",
        )

    if result.log_text:
        st.subheader("Log")
        st.text_area("Ausgabe", value=result.log_text, height=280, label_visibility="collapsed")
