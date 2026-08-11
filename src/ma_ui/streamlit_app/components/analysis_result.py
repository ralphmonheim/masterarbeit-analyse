"""Anzeigehelfer fuer ma_analyse-Ergebnisse."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from ma_analyse.models import AnalysisResult
from ma_analyse.stage_views import AnalysisStageView
from ma_ui.streamlit_app.shared import file_rows, normalize_table_for_streamlit

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
STAGE_STATUS_LABELS = {
    "completed": "abgeschlossen",
    "failed": "fehlerhaft",
    "not_run": "noch nicht ausgefuehrt",
    "separate_owner": "separates Fachmodul",
    "not_evaluable": "noch nicht auswertbar",
}


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

    if result.summary_table is not None:
        st.subheader("Ergebnisuebersicht")
        st.dataframe(
            normalize_table_for_streamlit(result.summary_table),
            hide_index=True,
            width="stretch",
        )

    for table_name, detail_table in result.detail_tables.items():
        st.subheader(str(table_name))
        st.dataframe(
            normalize_table_for_streamlit(detail_table),
            hide_index=True,
            width="stretch",
        )

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


def render_analysis_stage_view(view: AnalysisStageView) -> None:
    """Zeigt Zweck, Reifegrad, Grenzen und vorhandene Ergebnisse einer Stufe."""

    st.markdown(f"**Status:** {STAGE_STATUS_LABELS.get(view.status, view.status)}")
    st.write(view.purpose)

    st.markdown("**Verfuegbarer Umfang**")
    for item in view.available_functions:
        st.markdown(f"- {item}")

    st.markdown("**Aktuelle Grenzen**")
    for item in view.limits:
        st.markdown(f"- {item}")

    if view.stage_key == "optimization" and view.result is not None:
        st.divider()
        render_analysis_result(view.result)
    elif view.stage_key == "standards_verification" and view.result is not None:
        st.divider()
        st.subheader("Nachweisbereitschaft")
        if view.result.warnings:
            st.info(" ".join(view.result.warnings))
        st.dataframe(
            normalize_table_for_streamlit(view.result.summary_table),
            hide_index=True,
            width="stretch",
        )
    elif view.status == "not_run":
        st.info("Fuehre im Tab 'Auswahl & Lauf' eine Analyse aus, um hier Ergebnisse anzuzeigen.")
    elif view.status == "not_evaluable":
        st.info("Diese Stufe zeigt erst Ergebnisse, wenn ein fachlich gepruefter Ergebnisvertrag vorliegt.")
