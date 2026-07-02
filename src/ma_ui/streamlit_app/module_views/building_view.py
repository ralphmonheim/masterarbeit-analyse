"""Pruefansicht fuer das Gebaeudemodul."""

from __future__ import annotations

from collections.abc import Sequence

import streamlit as st

from ma_building import (
    BUILDING_CAD_INPUT_DIR,
    BUILDING_IFC_INPUT_DIR,
    BUILDING_RHINO_INPUT_DIR,
    MASTER_THESIS_REFERENCE_IFC_FILENAME,
    diagnose_building_source,
    load_demo_building_spec,
    scan_default_building_input_files,
    validate_building_spec,
)
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_validation import DiagnosticMessage, DiagnosticSeverity


def render() -> None:
    """Zeigt Demo-Spezifikation und lokale Quelldiagnosen."""
    render_page_header("Gebaeude und Zonen", "Gebaeude- und Modellrandbedingungen")
    _render_demo_spec_section()
    _render_local_sources_section()


def _render_demo_spec_section() -> None:
    st.subheader("Demo-Gebaeudespezifikation")
    try:
        spec = load_demo_building_spec()
    except (OSError, ValueError) as exc:
        st.error(f"Demo-Spezifikation konnte nicht geladen werden: {exc}")
        return

    validation_result = validate_building_spec(spec)
    st.metric("Freigabestatus", validation_result.release_status.value)
    st.dataframe(
        normalize_table_for_streamlit(
            [
                {"Kennwert": "Gebaeude", "Wert": spec.building.name},
                {"Kennwert": "Geschosse", "Wert": len(spec.storeys)},
                {"Kennwert": "Raeume", "Wert": len(spec.spaces)},
                {"Kennwert": "Bauteile", "Wert": len(spec.elements)},
                {"Kennwert": "Oeffnungen", "Wert": len(spec.openings)},
                {"Kennwert": "Reifegrad", "Wert": spec.model_version.current_maturity_level.value},
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    _render_messages(validation_result.messages)


def _render_local_sources_section() -> None:
    st.subheader("Lokale Modellquellen")
    st.caption(f"IFC: {BUILDING_IFC_INPUT_DIR} | 3DM: {BUILDING_RHINO_INPUT_DIR} | CAD: {BUILDING_CAD_INPUT_DIR}")

    source_paths = tuple(
        sorted(
            scan_default_building_input_files(),
            key=lambda path: (path.name.lower() != MASTER_THESIS_REFERENCE_IFC_FILENAME.lower(), path.name.lower()),
        )
    )
    if not source_paths:
        st.info("Keine lokalen IFC- oder 3DM-Dateien gefunden.")
        return

    diagnostics = [diagnose_building_source(path) for path in source_paths]
    source_rows = []
    message_rows = []
    entity_rows = []
    for diagnostic in diagnostics:
        source_rows.append(
            {
                "Datei": diagnostic.source.source_path.name if diagnostic.source.source_path else "",
                "Rolle": _source_role(diagnostic.source.source_path),
                "Format": diagnostic.source.data_format,
                "Groesse Byte": diagnostic.source.file_size_bytes,
                "SHA-256": diagnostic.source.sha256,
                "IFC-Schema": diagnostic.ifc_schema,
            }
        )
        for message in diagnostic.messages:
            message_rows.append(
                {
                    "Datei": diagnostic.source.source_path.name if diagnostic.source.source_path else "",
                    "Schwere": message.severity.value,
                    "Code": message.code,
                    "Meldung": message.message,
                    "Fundstelle": message.location,
                }
            )
        for entity_name, count in diagnostic.entity_counts.items():
            entity_rows.append(
                {
                    "Datei": diagnostic.source.source_path.name if diagnostic.source.source_path else "",
                    "IFC-Entity": entity_name,
                    "Anzahl": count,
                }
            )

    st.dataframe(normalize_table_for_streamlit(source_rows), hide_index=True, width="stretch")
    if entity_rows:
        st.dataframe(normalize_table_for_streamlit(entity_rows), hide_index=True, width="stretch")
    _render_message_rows(message_rows)


def _source_role(path) -> str:
    if path is None:
        return ""
    if path.name.lower() == MASTER_THESIS_REFERENCE_IFC_FILENAME.lower():
        return "Masterarbeits-Referenzmodell"
    if path.suffix.lower() == ".ifc":
        return "IDA-ICE-Sample"
    if path.suffix.lower() == ".3dm":
        return "Rhino-Demoquelle"
    if path.suffix.lower() == ".dwg":
        return "CAD-Beispiel ungeprueft"
    return "lokale Quelle"


def _render_messages(messages: Sequence[DiagnosticMessage]) -> None:
    rows = [
        {
            "Schwere": message.severity.value,
            "Code": message.code,
            "Meldung": message.message,
            "Fundstelle": message.location,
        }
        for message in messages
    ]
    _render_message_rows(rows)


def _render_message_rows(rows: list[dict[str, object]]) -> None:
    if not rows:
        st.success("Keine Validierungs- oder Diagnosemeldungen.")
        return
    if any(row["Schwere"] == DiagnosticSeverity.ERROR.value for row in rows):
        st.error("Fehler blockieren die Freigabe.")
    elif any(row["Schwere"] == DiagnosticSeverity.WARNING.value for row in rows):
        st.warning("Warnungen benoetigen eine bewusste Freigabeentscheidung.")
    else:
        st.info("Nur Informationsmeldungen vorhanden.")
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")
