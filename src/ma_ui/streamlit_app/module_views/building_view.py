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
from ma_database import DemoCatalog, DemoCatalogRecord, load_demo_catalog
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
    spec = _select_building_specification()
    if spec is None:
        return

    overview_tab, elements_tab, openings_tab, constructions_tab, sources_tab = st.tabs(
        ["Uebersicht", "Bauteile", "Oeffnungen", "Konstruktionen", "Modellquellen"]
    )
    with overview_tab:
        _render_building_overview(spec)
    with elements_tab:
        _render_elements(spec)
    with openings_tab:
        _render_openings(spec)
    with constructions_tab:
        _render_construction_catalog(spec)
    with sources_tab:
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


def building_element_rows(spec) -> list[dict[str, object]]:
    """Prepares explicitly present building elements for inspection in the UI."""
    external_codes = {"AW", "DA", "BP", "FA", "TA"}
    return [
        {
            "Bauteil": element.element_id,
            "Typ": element.element_type,
            "Bauartcode": element.construction_code,
            "Huellbauteil": "ja" if element.construction_code in external_codes else "nein",
            "Flaeche [m2]": element.area_m2,
            "Orientierung [Grad]": element.orientation_deg,
            "Geschoss": element.storey_id,
            "Angrenzende Raeume": ", ".join(element.adjacent_space_ids),
            "Datenherkunft": "Spezifikation / manuell gepflegt",
        }
        for element in spec.elements
    ]


def building_opening_rows(spec) -> list[dict[str, object]]:
    """Prepares explicitly present openings for inspection in the UI."""
    return [
        {
            "Oeffnung": opening.opening_id,
            "Typ": opening.opening_type,
            "Bauartcode": opening.construction_code,
            "Flaeche [m2]": opening.area_m2,
            "Host-Bauteil": opening.host_element_id,
            "Datenherkunft": "Spezifikation / manuell gepflegt",
        }
        for opening in spec.openings
    ]


def _select_building_specification():
    """Selects the read-only specification displayed by the building view."""
    option_rows = building_spec_option_rows()
    selected_label = st.selectbox("Gebaeudespezifikation", [row["Name"] for row in option_rows], index=0)
    selected_key = next(row["Schluessel"] for row in option_rows if row["Name"] == selected_label)
    try:
        return _load_building_spec_option(selected_key)
    except (OSError, ValueError) as exc:
        st.error(f"Gebaeudespezifikation konnte nicht geladen werden: {exc}")
        return None


def _render_building_overview(spec) -> None:
    validation_result = validate_building_spec(spec)
    st.metric("Freigabestatus", validation_result.release_status.value)
    st.dataframe(normalize_table_for_streamlit(building_spec_summary_rows(spec)), hide_index=True, width="stretch")
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


def _render_elements(spec) -> None:
    rows = building_element_rows(spec)
    if not rows:
        st.info("Die gewaehlte Spezifikation enthaelt keine einzeln erfassten Bauteile.")
        return
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")


def _render_openings(spec) -> None:
    rows = building_opening_rows(spec)
    if not rows:
        st.info("Die gewaehlte Spezifikation enthaelt keine einzeln erfassten Oeffnungen.")
        return
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")


def _render_construction_catalog(spec) -> None:
    """Selects local constructions without changing the building specification."""
    try:
        catalog = load_demo_catalog()
    except FileNotFoundError:
        st.info("Lokale Katalogdaten sind nicht Bestandteil des Repositorys und wurden hier nicht gefunden.")
        return
    except (OSError, ValueError) as exc:
        st.error(f"Lokaler Demo-Katalog konnte nicht geladen werden: {exc}")
        return

    construction_tab, material_tab = st.tabs(["Konstruktionen", "Materialien"])
    with construction_tab:
        _render_construction_assignment(spec, catalog)
    with material_tab:
        _render_material_browser(catalog)


def _render_construction_assignment(spec, catalog: DemoCatalog) -> None:
    targets = [
        (element.element_id, element.construction_code, element.element_type)
        for element in spec.elements
    ] + [
        (opening.opening_id, opening.construction_code, opening.opening_type)
        for opening in spec.openings
    ]
    if not targets:
        st.info("Fuer diese Spezifikation sind keine Bauteile oder Oeffnungen fuer eine Konstruktion vorhanden.")
        return

    target_id = st.selectbox("Bauteil oder Oeffnung", [target[0] for target in targets], key="building_construction_target")
    _target_id, construction_code, target_type = next(target for target in targets if target[0] == target_id)
    candidates = tuple(
        record for record in catalog.records_for("constructions") if record.data["construction_code"] == construction_code
    )
    option_ids = ["not_assigned", *[record.record_id for record in candidates]]
    selected_id = st.selectbox(
        "Demo-Konstruktion",
        option_ids,
        format_func=lambda option_id: _construction_option_label(candidates, option_id),
        key=f"building_construction_{target_id}",
    )
    st.session_state[f"building_construction_selection_{target_id}"] = selected_id
    if selected_id == "not_assigned":
        st.dataframe(
            normalize_table_for_streamlit(
                [{"Merkmal": "Zuordnung", "Wert": "Keine Konstruktion zugeordnet"}, {"Merkmal": "Bauartcode", "Wert": construction_code}]
            ),
            hide_index=True,
            width="stretch",
        )
        return
    record = next(record for record in candidates if record.record_id == selected_id)
    st.dataframe(
        normalize_table_for_streamlit(_construction_rows(target_type, construction_code, record)),
        hide_index=True,
        width="stretch",
    )
    layer_rows = _construction_layer_rows(catalog, record.record_id)
    if layer_rows:
        st.dataframe(normalize_table_for_streamlit(layer_rows), hide_index=True, width="stretch")


def _render_material_browser(catalog: DemoCatalog) -> None:
    materials = catalog.records_for("materials")
    material_id = st.selectbox(
        "Demo-Material",
        [record.record_id for record in materials],
        format_func=lambda record_id: _catalog_label(materials, record_id),
        key="building_material_browser",
    )
    record = next(record for record in materials if record.record_id == material_id)
    st.dataframe(
        normalize_table_for_streamlit(_catalog_record_rows(record)),
        hide_index=True,
        width="stretch",
    )


def _construction_option_label(records: tuple[DemoCatalogRecord, ...], option_id: str) -> str:
    return "Keine Konstruktion zugeordnet" if option_id == "not_assigned" else _catalog_label(records, option_id)


def _catalog_label(records: tuple[DemoCatalogRecord, ...], record_id: str) -> str:
    record = next(record for record in records if record.record_id == record_id)
    return f"{record.label} ({record.record_id})"


def _construction_rows(target_type: str, construction_code: str, record: DemoCatalogRecord) -> list[dict[str, object]]:
    return [
        {"Merkmal": "Bauteiltyp", "Wert": target_type},
        {"Merkmal": "Bauartcode", "Wert": construction_code},
        {"Merkmal": "Konstruktion", "Wert": record.label},
        {"Merkmal": "U-Wert [W/m2K]", "Wert": record.data.get("calculated_u_value_w_m2k")},
        {"Merkmal": "Pruefstatus", "Wert": record.data["verification_status"]},
    ]


def _construction_layer_rows(catalog: DemoCatalog, construction_id: str) -> list[dict[str, object]]:
    material_labels = {record.record_id: record.label for record in catalog.records_for("materials")}
    return [
        {
            "Schicht": layer["layer_no"],
            "Material": material_labels.get(layer["material_ref"], layer["material_ref"]),
            "Dicke [m]": layer["thickness_m"],
            "Funktion": layer["layer_function"],
        }
        for layer in catalog.layers_for(construction_id)
    ]


def _catalog_record_rows(record: DemoCatalogRecord) -> list[dict[str, object]]:
    fields = [
        ("ID", record.record_id),
        ("Name", record.label),
        ("Kategorie", record.category),
        ("Pruefstatus", record.data["verification_status"]),
        ("Bestaetigung", record.data["confirmation_status"]),
    ]
    return [{"Merkmal": name, "Wert": value} for name, value in fields]


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
