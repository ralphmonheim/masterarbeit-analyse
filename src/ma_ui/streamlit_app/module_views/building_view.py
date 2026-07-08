"""Pruefansicht fuer das Gebaeudemodul."""

from __future__ import annotations

from collections.abc import Sequence

import streamlit as st

from ma_building import (
    BUILDING_CAD_INPUT_DIR,
    BUILDING_IFC_INPUT_DIR,
    BUILDING_RHINO_INPUT_DIR,
    BUSINESS_INTEGRATION_REFERENCE_RHINO_FILENAME,
    FACHLICHER_TEIL_REFERENCE_IFC_FILENAME,
    diagnose_building_source,
    load_business_integration_lod1_building_spec,
    load_demo_building_spec,
    scan_default_building_input_files,
    validate_building_spec,
)
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_validation import DiagnosticMessage, DiagnosticSeverity

_BUILDING_SPEC_OPTIONS = (
    ("demo", "Demo-Gebaeudespezifikation", load_demo_building_spec),
    ("business_integration_lod1", "BusinessIntegration LoD-1", load_business_integration_lod1_building_spec),
)


def render() -> None:
    """Zeigt Demo-Spezifikation und lokale Quelldiagnosen."""
    render_page_header("Gebaeude", "Gebaeude- und Modellrandbedingungen")
    _render_demo_spec_section()
    _render_local_sources_section()


def building_spec_option_rows() -> list[dict[str, str]]:
    """Liefert die in der UI auswaehlbaren Gebaeudespezifikationen."""
    return [{"Schluessel": key, "Name": label} for key, label, _loader in _BUILDING_SPEC_OPTIONS]


def building_spec_summary_rows(spec) -> list[dict[str, object]]:
    """Liefert kompakte Kennwerte einer BuildingModelSpecification."""
    rows: list[dict[str, object]] = [
        {"Kennwert": "Gebaeude", "Wert": spec.building.name},
        {"Kennwert": "Eingabe-LoD", "Wert": _display_value(spec.input_detail_level)},
        {"Kennwert": "Reifegrad", "Wert": _display_value(spec.model_version.current_maturity_level)},
        {"Kennwert": "Laenge [m]", "Wert": spec.building.length_m},
        {"Kennwert": "Breite [m]", "Wert": spec.building.width_m},
        {"Kennwert": "Hoehe [m]", "Wert": spec.building.height_m},
        {"Kennwert": "Geschosse", "Wert": len(spec.storeys)},
        {"Kennwert": "Raeume", "Wert": len(spec.spaces)},
        {"Kennwert": "Bauteile", "Wert": len(spec.elements)},
        {"Kennwert": "Oeffnungen", "Wert": len(spec.openings)},
    ]
    if spec.simple_envelope is not None:
        envelope = spec.simple_envelope
        rows.extend(
            [
                {"Kennwert": "U-Wert Aussenwand [W/m2K]", "Wert": envelope.external_wall_u_value_w_m2k},
                {"Kennwert": "U-Wert Fenster [W/m2K]", "Wert": envelope.window_u_value_w_m2k},
                {"Kennwert": "Fensteranteil [%]", "Wert": envelope.window_area_ratio_percent},
                {"Kennwert": "U-Wert Dach [W/m2K]", "Wert": envelope.roof_u_value_w_m2k},
                {"Kennwert": "U-Wert Boden [W/m2K]", "Wert": envelope.floor_u_value_w_m2k},
                {"Kennwert": "Aussenwandflaeche [m2]", "Wert": envelope.external_wall_area_m2},
                {"Kennwert": "Fensterflaeche [m2]", "Wert": envelope.window_area_m2},
            ]
        )
    return rows


def _render_demo_spec_section() -> None:
    st.subheader("Gebaeudespezifikation")
    option_rows = building_spec_option_rows()
    option_labels = [row["Name"] for row in option_rows]
    selected_label = st.selectbox("Spezifikation", option_labels, index=0)
    selected_key = next(row["Schluessel"] for row in option_rows if row["Name"] == selected_label)
    try:
        spec = _load_building_spec_option(selected_key)
    except (OSError, ValueError) as exc:
        st.error(f"Gebaeudespezifikation konnte nicht geladen werden: {exc}")
        return

    validation_result = validate_building_spec(spec)
    st.metric("Freigabestatus", validation_result.release_status.value)
    st.dataframe(
        normalize_table_for_streamlit(building_spec_summary_rows(spec)),
        hide_index=True,
        width="stretch",
    )
    if spec.assumptions:
        st.dataframe(
            normalize_table_for_streamlit(
                [
                    {"ID": assumption.assumption_id, "Fundstelle": assumption.location or "", "Annahme": assumption.text}
                    for assumption in spec.assumptions
                ]
            ),
            hide_index=True,
            width="stretch",
        )
    _render_messages(validation_result.messages)


def _load_building_spec_option(option_key: str):
    for key, _label, loader in _BUILDING_SPEC_OPTIONS:
        if key == option_key:
            return loader()
    raise ValueError(f"Unbekannte Gebaeudespezifikation: {option_key}")


def _display_value(value) -> str:
    return str(value.value if hasattr(value, "value") else value)


def _render_local_sources_section() -> None:
    st.subheader("Lokale Modellquellen")
    st.caption(f"IFC: {BUILDING_IFC_INPUT_DIR} | 3DM: {BUILDING_RHINO_INPUT_DIR} | CAD: {BUILDING_CAD_INPUT_DIR}")

    source_paths = tuple(
        sorted(
            scan_default_building_input_files(),
            key=lambda path: (
                path.name.lower() != BUSINESS_INTEGRATION_REFERENCE_RHINO_FILENAME.lower(),
                path.name.lower() != FACHLICHER_TEIL_REFERENCE_IFC_FILENAME.lower(),
                path.name.lower(),
            ),
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
    if path.name.lower() == BUSINESS_INTEGRATION_REFERENCE_RHINO_FILENAME.lower():
        return "BusinessIntegration-Testgebaeude"
    if path.name.lower() == FACHLICHER_TEIL_REFERENCE_IFC_FILENAME.lower():
        return "Fachteil-Referenzmodell"
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
