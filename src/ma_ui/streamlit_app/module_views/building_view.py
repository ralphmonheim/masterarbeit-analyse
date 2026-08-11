"""Pruefansicht fuer das Gebaeudemodul."""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from ma_building import (
    BUILDING_CAD_INPUT_DIR,
    BUILDING_IFC_INPUT_DIR,
    BUILDING_RHINO_INPUT_DIR,
    BUILDING_SPECIFICATION_OPTIONS,
    BUSINESS_INTEGRATION_REFERENCE_RHINO_FILENAME,
    DEFAULT_DELTA_U_WB_W_M2K,
    FACHLICHER_TEIL_REFERENCE_IFC_FILENAME,
    LocalCatalogValidationError,
    ThermalComponentRow,
    ThermalTransmissionResult,
    calculate_thermal_transmission,
    create_user_catalog_draft,
    diagnose_building_source,
    load_building_excel_catalog,
    load_local_building_catalog,
    load_named_building_specification,
    scan_default_building_input_files,
)
from ma_database import DemoCatalog, DemoCatalogRecord
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_ui.streamlit_app.state import (
    clear_workspace_draft,
    get_active_workspace,
    mark_workspace_draft,
)
from ma_validation import DiagnosticMessage, DiagnosticSeverity
from ma_workspace import load_project_module_config, save_project_module_config

BUILDING_WORKSPACE_TAB_LABELS = (
    "Import",
    "Übersicht",
    "Räume",
    "U-Werte",
    "Ergebnisse",
    "Bauteile",
)
BUILDING_AI_PROMPT_PATH = Path("docs/prompts/MA_BUILDING_AI_MODEL_GENERATION_PROMPT.md")


def render() -> None:
    """Zeigt Demo-Spezifikation und lokale Quelldiagnosen."""
    render_page_header("Gebaeude", "Gebaeude- und Modellrandbedingungen")

    section = st.segmented_control(
        "Gebaeudebereich",
        BUILDING_WORKSPACE_TAB_LABELS,
        default=BUILDING_WORKSPACE_TAB_LABELS[0],
        key="ma_building_workspace_section",
        selection_mode="single",
    )
    section = section or BUILDING_WORKSPACE_TAB_LABELS[0]
    if section == "Import":
        spec = _render_building_import()
    else:
        try:
            spec = _load_building_spec_option(_active_building_spec_key())
        except (OSError, ValueError) as exc:
            st.error(f"Gebaeudespezifikation konnte nicht geladen werden: {exc}")
            return
    if spec is None:
        return
    if section == "Übersicht":
        _render_building_overview(spec)
    elif section == "Räume":
        _render_rooms(spec)
    elif section == "U-Werte":
        _render_u_values(spec)
    elif section == "Ergebnisse":
        _render_thermal_results(spec)
    elif section == "Bauteile":
        _render_construction_catalog(spec)


def building_spec_option_rows() -> list[dict[str, str]]:
    """Liefert die in der UI auswaehlbaren Gebaeudespezifikationen."""
    return [{"Schluessel": key, "Name": label} for key, label, _source in BUILDING_SPECIFICATION_OPTIONS]


def building_spec_summary_rows(spec) -> list[dict[str, object]]:
    """Liefert weiterhin alle Kennwerte fuer bestehende Aufrufer."""
    return building_master_data_rows(spec) + building_area_volume_rows(spec)


def building_master_data_rows(spec) -> list[dict[str, object]]:
    """Liefert kompakte Stammdaten einschliesslich LoD und Reifegrad."""
    return [
        {"Kennwert": "Gebaeude", "Wert": spec.building.name},
        {"Kennwert": "Gebaeude-ID", "Wert": spec.building.building_id},
        {"Kennwert": "Eingabe-LoD", "Wert": _display_value(spec.input_detail_level)},
        {"Kennwert": "Reifegrad", "Wert": _display_value(spec.model_version.current_maturity_level)},
    ]


def building_area_volume_rows(spec) -> list[dict[str, object]]:
    """Liefert die zentralen Geometrie-, Flaechen- und Volumenkennwerte."""
    rows: list[dict[str, object]] = [
        {"Kennwert": "Laenge [m]", "Wert": spec.building.length_m},
        {"Kennwert": "Breite [m]", "Wert": spec.building.width_m},
        {"Kennwert": "Hoehe [m]", "Wert": spec.building.height_m},
        {"Kennwert": "Nutzflaeche Raeume [m2]", "Wert": sum(space.floor_area_m2 for space in spec.spaces)},
        {"Kennwert": "Raumvolumen [m3]", "Wert": sum(space.volume_m3 for space in spec.spaces)},
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
            "ID": element.element_id,
            "Typ": element.element_type,
            "Code": element.construction_code,
            "Konstruktion": element.construction_code,
            "Huellbauteil": "ja" if element.construction_code in external_codes else "nein",
            "Flaeche [m2]": element.area_m2,
            "Orientierung [Grad]": element.orientation_deg,
            "Geschoss": element.storey_id,
        }
        for element in spec.elements
    ]


def building_opening_rows(spec) -> list[dict[str, object]]:
    """Prepares openings as building elements, including their host relation."""
    return [
        {
            "ID": opening.opening_id,
            "Typ": opening.opening_type,
            "Code": opening.construction_code,
            "Konstruktion": opening.construction_code,
            "Flaeche [m2]": opening.area_m2,
            "Huellbauteil": "ja",
            "Orientierung [Grad]": None,
            "Geschoss": "",
        }
        for opening in spec.openings
    ]


def building_room_rows(spec) -> list[dict[str, object]]:
    """Bereitet die erkannten Raeume als erstes, ungefiltertes Raumbuch auf."""
    return [
        {
            "Raum-ID": space.space_id,
            "IFC-Raumname": space.name,
            "Geschoss": space.storey_id,
            "Flaeche [m2]": space.floor_area_m2,
            "Volumen [m3]": space.volume_m3,
            "Quelle": "BuildingModelSpecification",
            "Validierungsstatus": "erkannt",
        }
        for space in spec.spaces
    ]


def building_import_minimum_ready(spec) -> bool:
    """Prueft die V1-Mindestdaten: Bezeichnung und positive Flaeche."""
    explicit_components = [
        (element.element_id, element.area_m2) for element in spec.elements
    ] + [
        (opening.opening_id, opening.area_m2) for opening in spec.openings
    ]
    if explicit_components:
        return all(bool(component_id) and area_m2 > 0 for component_id, area_m2 in explicit_components)
    envelope = spec.simple_envelope
    if envelope is None:
        return False
    aggregate_areas = (
        envelope.external_wall_area_m2,
        envelope.window_area_m2,
        envelope.roof_area_m2,
        envelope.floor_area_m2,
    )
    return bool(spec.building.name) and any(area is not None and area > 0 for area in aggregate_areas)


def building_import_document_status_rows(spec, active_selection_key: str | None) -> list[dict[str, object]]:
    """Beschreibt den gemeinsamen Entwurfs-/Aktivstand aller Importwege."""
    minimum_ready = building_import_minimum_ready(spec)
    return [
        {"Merkmal": "Gebaeudedokument", "Wert": spec.building.name or "leer"},
        {"Merkmal": "Explizite Bauteile", "Wert": len(spec.elements)},
        {"Merkmal": "Explizite Oeffnungen", "Wert": len(spec.openings)},
        {
            "Merkmal": "V1-Mindestdaten",
            "Wert": "vollstaendig" if minimum_ready else "Bezeichnung und Flaeche fehlen",
        },
        {"Merkmal": "Aktiver Stand", "Wert": active_selection_key or "noch keiner"},
    ]


def _select_building_specification():
    """Waehlt die im Import-Reiter als Entwurf angezeigte Spezifikation."""
    option_rows = building_spec_option_rows()
    option_keys = [row["Schluessel"] for row in option_rows]
    selected_key = st.selectbox(
        "Gebaeudespezifikation",
        option_keys,
        index=option_keys.index(_default_building_spec_key()),
        format_func=lambda option_key: next(
            row["Name"] for row in option_rows if row["Schluessel"] == option_key
        ),
        key="building_specification_draft_key",
        on_change=_mark_building_draft,
    )
    try:
        spec = _load_building_spec_option(selected_key)
    except (OSError, ValueError) as exc:
        st.error(f"Gebaeudespezifikation konnte nicht geladen werden: {exc}")
        return None
    workspace = get_active_workspace(st.session_state)
    project_payload = _building_project_payload(workspace) if workspace is not None else {}
    active_specification = project_payload.get("building_specification", {})
    active_selection_key = (
        str(active_specification.get("selection_key"))
        if isinstance(active_specification, dict) and active_specification.get("selection_key")
        else None
    )
    st.dataframe(
        normalize_table_for_streamlit(building_master_data_rows(spec)),
        hide_index=True,
        width="stretch",
    )
    st.markdown("##### Gemeinsames Gebaeudedokument")
    st.dataframe(
        normalize_table_for_streamlit(
            building_import_document_status_rows(spec, active_selection_key)
        ),
        hide_index=True,
        width="stretch",
    )
    minimum_ready = building_import_minimum_ready(spec)
    replaces_active = bool(active_selection_key and active_selection_key != selected_key)
    replacement_confirmed = False
    if replaces_active:
        st.warning(
            f"Der aktive Stand {active_selection_key} wird durch {selected_key} ersetzt. "
            "Die Ueberschreibung erfolgt nur nach deiner Bestaetigung."
        )
        replacement_confirmed = st.checkbox(
            "Aktiven Gebaeudestand wirklich ueberschreiben",
            key="building_confirm_specification_replacement",
        )
    if not minimum_ready:
        st.warning("Der Entwurf braucht mindestens eine Bauteilbezeichnung und eine positive Flaeche.")
    if workspace is None:
        st.info("Bitte zuerst ein Projekt auswaehlen, um den Stand zu aktivieren.")
    already_active = active_selection_key == selected_key
    if already_active:
        st.success("Dieser Gebaeudestand ist im Projekt aktiv.")
    apply_disabled = (
        workspace is None
        or not minimum_ready
        or already_active
        or (replaces_active and not replacement_confirmed)
    )
    if st.button(
        "Gebaeudedokument aktivieren",
        key="building_apply_specification",
        disabled=apply_disabled,
    ):
        payload = project_payload
        payload["building_specification"] = {
            "selection_key": selected_key,
            "building_id": spec.building.building_id,
            "model_version": spec.model_version.version_id,
        }
        save_project_module_config(workspace, "ma_building", payload)
        st.session_state["building_applied_specification_key"] = selected_key
        clear_workspace_draft(st.session_state, "ma_building")
        st.success("Gebaeudedokument wurde aktiviert und an die Gebaeudeansichten uebergeben.")
    elif not already_active:
        st.info("Die Auswahl ist ein Entwurf und noch nicht im Projekt aktiviert.")
    return spec


def _render_building_import():
    """Zeigt die vereinbarten Eingabewege, ohne Modellquellen zu verarbeiten."""

    st.subheader("Gebaeudemodell vorbereiten")
    st.caption(
        "Die drei Wege erfassen nur die beabsichtigte Eingabe. Eine IFC-, Rhino- oder KI-Verarbeitung wird hier nicht gestartet."
    )
    input_modes = ("3D-Datei", "KI-Modell", "Textliche Eingabe")
    input_mode = st.segmented_control(
        "Importweg",
        input_modes,
        default=input_modes[0],
        key="ma_building_import_mode",
        selection_mode="single",
    )
    input_mode = input_mode or input_modes[0]
    if input_mode == "3D-Datei":
        uploaded_file = st.file_uploader(
            "3D-Datei fuer die spaetere Pruefung vormerken",
            type=["ifc", "3dm", "dwg", "dxf", "skp", "obj", "stl"],
            key="building_import_3d_file",
            on_change=_mark_building_draft,
        )
        if uploaded_file is None:
            st.info("Noch keine Datei vorgemerkt. Bestehende lokale Referenzmodelle lassen sich in der Gebaeudeuebersicht auswaehlen.")
        else:
            st.info(f"{uploaded_file.name} ist nur in dieser Sitzung vorgemerkt und wurde nicht verarbeitet oder gespeichert.")
    elif input_mode == "KI-Modell":
        st.text_area(
            "Gebaeudebeschreibung",
            placeholder="Zum Beispiel: Kleines Buerogebaeude mit zwei Geschossen und zentraler Technik ...",
            key="building_import_ai_description",
            on_change=_mark_building_draft,
        )
        st.button(
            "Beschreibung abschicken",
            key="building_import_ai_submit",
            disabled=True,
            help="Die spaetere KI-Uebergabe ist in V1 noch nicht angebunden.",
        )
        st.caption("Die Eingabe bleibt lokal in der Sitzung. Es wird kein externes KI-Modell aufgerufen.")
        try:
            fixed_prompt = BUILDING_AI_PROMPT_PATH.read_text(encoding="utf-8")
        except OSError as exc:
            st.error(f"Der feste KI-Prompt konnte nicht geladen werden: {exc}")
        else:
            st.text_area(
                "Fester KI-Prompt",
                value=fixed_prompt,
                height=520,
                disabled=True,
                key="building_fixed_ai_prompt",
            )
            _render_prompt_copy_button(fixed_prompt)
    else:
        st.text_area(
            "Gebaeudebeschreibung erfassen",
            placeholder="Zum Beispiel: Grundflaeche, Geschosse, Raeume, Huelle und bekannte Annahmen ...",
            key="building_import_text_description",
            on_change=_mark_building_draft,
        )
        st.caption("Die Beschreibung ist eine Vorbereitung fuer eine spätere strukturierte BuildingModelSpecification.")
    st.divider()
    st.subheader("Gemeinsames Gebaeudedokument")
    st.caption(
        "Alle Importwege muenden in dieselbe BuildingModelSpecification. "
        "Die aktuelle V1 aktiviert vorhandene strukturierte Demo-Staende; die Datei- und KI-Verarbeitung bleibt getrennte Folgearbeit."
    )
    return _select_building_specification()


def _render_prompt_copy_button(prompt: str) -> None:
    """Zeigt einen lokalen Browser-Kopierbutton ohne externen Dienst."""
    prompt_literal = json.dumps(prompt)
    components.html(
        f"""
        <button id="copy-building-prompt" type="button">Prompt kopieren</button>
        <span id="copy-building-prompt-status" style="margin-left:0.75rem"></span>
        <script>
        const button = document.getElementById("copy-building-prompt");
        const status = document.getElementById("copy-building-prompt-status");
        button.addEventListener("click", async () => {{
            try {{
                await navigator.clipboard.writeText({prompt_literal});
                status.textContent = "Prompt kopiert.";
            }} catch (error) {{
                status.textContent = "Kopieren wurde vom Browser blockiert.";
            }}
        }});
        </script>
        """,
        height=42,
    )


def _render_building_overview(spec) -> None:
    st.subheader("Gebaeudestammdaten und Modellstand")
    st.dataframe(normalize_table_for_streamlit(building_master_data_rows(spec)), hide_index=True, width="stretch")
    st.subheader("Flaechen- und Volumenkennwerte")
    st.dataframe(normalize_table_for_streamlit(building_area_volume_rows(spec)), hide_index=True, width="stretch")


def _render_elements(spec) -> None:
    element_rows = building_element_rows(spec)
    opening_rows = building_opening_rows(spec)
    rows = [*element_rows, *opening_rows]
    if not rows:
        st.info("Die gewaehlte Spezifikation enthaelt keine einzeln erfassten Bauteile.")
        return
    kinds = list(dict.fromkeys(row["Typ"] for row in rows))
    element_sections = ("Uebersicht", *kinds)
    element_section = st.segmented_control(
        "Elementgruppe",
        element_sections,
        default=element_sections[0],
        key="ma_building_element_section",
        selection_mode="single",
    )
    element_section = element_section or element_sections[0]
    if element_section == "Uebersicht":
        st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")
    else:
        st.dataframe(
            normalize_table_for_streamlit([row for row in rows if row["Typ"] == element_section]),
            hide_index=True,
            width="stretch",
        )


def thermal_component_table_rows(
    spec,
    result: ThermalTransmissionResult | None = None,
) -> list[dict[str, object]]:
    """Bereitet alle thermischen Bauteile fuer die rechte Auswahltabelle auf."""
    result = result or calculate_thermal_transmission(spec)
    openings_by_id = {opening.opening_id: opening for opening in spec.openings}
    rows = []
    for number, component in enumerate(result.rows, start=1):
        opening = openings_by_id.get(component.component_id)
        aggregate_host = (
            "LOD1-AW"
            if component.source_type == "SimpleEnvelope" and component.construction_code == "FA"
            else ""
        )
        rows.append(
            {
                "Nr.": number,
                "Bauteil": component.category,
                "Bezeichnung": component.component_id,
                "Ausrichtung": _orientation_label(component.orientation_deg),
                "Flaeche [m2]": component.gross_area_m2,
                "U-Wert [W/(m2 K)]": component.u_value_w_m2k,
                "Abzug von": opening.host_element_id if opening is not None else aggregate_host,
            }
        )
    return rows


def thermal_category_table_rows(result: ThermalTransmissionResult) -> list[dict[str, object]]:
    """Liefert die verdichtete U-Wert-Uebersicht je Bauteilkategorie."""
    return [
        {
            "Kategorie": category.category,
            "Flaeche [m2]": category.area_m2,
            "Mittlerer U-Wert [W/(m2 K)]": category.weighted_u_value_w_m2k,
            "F x U x A [W/K]": category.transmission_contribution_w_k,
            "Status": "vollstaendig" if category.is_complete else "unvollstaendig",
        }
        for category in result.category_results
    ]


def thermal_transmission_table_rows(result: ThermalTransmissionResult) -> list[dict[str, object]]:
    """Liefert die nachvollziehbaren Einzelbeitraege der Demo-Transmissionsbilanz."""
    return [
        {
            "Bauteil": row.component_id,
            "Kategorie": row.category,
            "F": row.temperature_correction_factor,
            "U-Wert [W/(m2 K)]": row.u_value_w_m2k,
            "Flaeche A [m2]": row.effective_area_m2,
            "F x U x A [W/K]": (
                row.temperature_correction_factor * row.u_value_w_m2k * row.effective_area_m2
                if row.is_complete
                and row.temperature_correction_factor is not None
                and row.u_value_w_m2k is not None
                else None
            ),
            "Status": "Demo-Annahme" if row.assumption_notes else "aus Modellstand",
        }
        for row in result.rows
        if row.effective_area_m2 > 0
    ]


def _render_u_values(spec) -> None:
    """Zeigt links feste Bauteildetails und rechts alle erkannten Huellbauteile."""
    result = calculate_thermal_transmission(spec)
    table_rows = thermal_component_table_rows(spec, result)
    if not table_rows:
        st.info("Die gewaehlte Spezifikation enthaelt keine auswertbaren Huellbauteile.")
        return
    _render_thermal_source_status(spec)

    detail_column, table_column = st.columns((1, 3), gap="large")
    with table_column:
        st.subheader("Erkannte Bauteile")
        selected_id = st.selectbox(
            "Bauteil fuer die Detailansicht",
            [str(row["Bezeichnung"]) for row in table_rows],
            format_func=lambda component_id: _component_selection_label(component_id, table_rows),
            key="ma_building_u_value_selected_component",
        )
        st.dataframe(
            normalize_table_for_streamlit(table_rows),
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "Die Himmelsrichtung ist ein Bauteilwert und keine Gruppierung. "
            "Abzugsflaechen bleiben als positive Einzelwerte sichtbar."
        )

    selected = next(row for row in result.rows if row.component_id == selected_id)
    with detail_column:
        _render_thermal_component_detail(spec, selected, table_rows)


def _render_thermal_component_detail(
    spec,
    component: ThermalComponentRow,
    table_rows: list[dict[str, object]],
) -> None:
    """Rendert die dauerhaft sichtbare linke Detailkarte eines Bauteils."""
    row_number = next(int(row["Nr."]) for row in table_rows if row["Bezeichnung"] == component.component_id)
    opening = next((item for item in spec.openings if item.opening_id == component.component_id), None)
    host_openings = [item for item in spec.openings if item.host_element_id == component.component_id]
    deduction_lines = [f"{item.opening_id}: {item.area_m2:.2f} m2" for item in host_openings]
    is_aggregate_opening = component.source_type == "SimpleEnvelope" and component.construction_code == "FA"
    if component.source_type == "SimpleEnvelope" and component.construction_code == "AW":
        window_area = spec.simple_envelope.window_area_m2 if spec.simple_envelope is not None else None
        if window_area is not None and window_area > 0:
            deduction_lines = [f"LOD1-FA: {window_area:.2f} m2"]
    if opening is not None:
        deduction_lines = [f"Abzug von: {opening.host_element_id}"]
    elif is_aggregate_opening:
        deduction_lines = ["Abzug von: LOD1-AW"]

    st.subheader("Bauteildetails")
    st.markdown("##### Bauteil")
    number_column, type_column = st.columns((1, 3))
    number_column.number_input("Nr.", value=row_number, disabled=True, key=f"detail_number_{component.component_id}")
    type_column.text_input(
        "Bauteilart",
        value=component.category,
        disabled=True,
        key=f"detail_type_{component.component_id}",
    )
    st.text_input(
        "Bezeichnung",
        value=component.component_id,
        disabled=True,
        key=f"detail_name_{component.component_id}",
    )
    st.text_input(
        "Ausrichtung",
        value=_orientation_label(component.orientation_deg),
        disabled=True,
        key=f"detail_orientation_{component.component_id}",
    )

    st.markdown("##### Geometrie")
    geometry_columns = st.columns(3)
    geometry_columns[0].number_input(
        "Anzahl", value=1, disabled=True, key=f"detail_count_{component.component_id}"
    )
    geometry_columns[1].text_input(
        "Laenge [m]", value="nicht verfuegbar", disabled=True, key=f"detail_length_{component.component_id}"
    )
    geometry_columns[2].text_input(
        "Breite [m]", value="nicht verfuegbar", disabled=True, key=f"detail_width_{component.component_id}"
    )
    st.number_input(
        "Flaeche [m2]",
        value=float(component.gross_area_m2),
        disabled=True,
        key=f"detail_area_{component.component_id}",
    )
    st.text_area(
        "Abzugsflaechen",
        value="\n".join(deduction_lines) if deduction_lines else "keine",
        disabled=True,
        height=80,
        key=f"detail_deductions_{component.component_id}",
    )
    control_columns = st.columns(2)
    control_columns[0].checkbox(
        "Abzugsflaeche",
        value=opening is not None or is_aggregate_opening,
        disabled=True,
        key=f"detail_is_deduction_{component.component_id}",
    )
    control_columns[1].checkbox(
        "Teil der Huelle",
        value=True,
        disabled=True,
        key=f"detail_is_envelope_{component.component_id}",
    )

    st.markdown("##### Eigenschaften")
    st.text_input(
        "U-Wert [W/(m2 K)]",
        value=(f"{component.u_value_w_m2k:.3f}" if component.u_value_w_m2k is not None else "nicht zugewiesen"),
        disabled=True,
        key=f"detail_u_value_{component.component_id}",
    )
    st.text_input(
        "Zugewiesenes Bauteil",
        value=f"Demo-Zuordnung {component.construction_code}",
        disabled=True,
        key=f"detail_assignment_{component.component_id}",
    )
    if component.assumption_notes:
        st.caption(" | ".join(component.assumption_notes))
    if st.button("Vorhandenes Bauteil auswaehlen", key=f"detail_select_catalog_{component.component_id}"):
        st.info("Die dauerhafte Katalogzuordnung wird im Reiter Bauteile verwaltet.")
    st.button(
        "Neues Bauteil erstellen",
        disabled=True,
        help="Der Erstellungsdialog ist als spaetere Ausbaustufe vorgesehen.",
        key=f"detail_create_catalog_{component.component_id}",
    )


def _render_thermal_results(spec) -> None:
    """Zeigt U-Wert-Uebersicht und vereinfachten Transmissionskennwert."""
    result = calculate_thermal_transmission(spec)
    _render_thermal_source_status(spec)
    u_value_tab, transmission_tab = st.tabs(("U-Wert-Übersicht", "Transmissionswärmeverlust"))
    with u_value_tab:
        _render_u_value_results(result)
    with transmission_tab:
        _render_transmission_results(result)


def _render_u_value_results(result: ThermalTransmissionResult) -> None:
    st.subheader("Flaechengewichtete U-Werte nach Bauteilkategorie")
    table_column, chart_column = st.columns((1, 2), gap="large")
    category_rows = thermal_category_table_rows(result)
    with table_column:
        for category in result.category_results:
            st.markdown(f"##### {category.category}")
            component_rows = [
                {
                    "Bauteil": row.component_id,
                    "U-Wert [W/(m2 K)]": row.u_value_w_m2k,
                    "Flaeche [m2]": row.effective_area_m2,
                }
                for row in result.rows
                if row.category == category.category and row.effective_area_m2 > 0
            ]
            st.dataframe(normalize_table_for_streamlit(component_rows), hide_index=True, width="stretch")
            mean_value = category.weighted_u_value_w_m2k
            st.metric(
                f"Mittlerer U-Wert {category.category}",
                f"{mean_value:.3f} W/(m2 K)" if mean_value is not None else "nicht berechenbar",
            )
    with chart_column:
        chart_rows = [
            {
                "Kategorie": row["Kategorie"],
                "Mittlerer U-Wert [W/(m2 K)]": row["Mittlerer U-Wert [W/(m2 K)]"],
            }
            for row in category_rows
            if row["Mittlerer U-Wert [W/(m2 K)]"] is not None
        ]
        if chart_rows:
            st.bar_chart(chart_rows, x="Kategorie", y="Mittlerer U-Wert [W/(m2 K)]")
        st.caption("Informative Demo-Auswertung; kein GEG-Nachweis.")


def _render_transmission_results(result: ThermalTransmissionResult) -> None:
    st.subheader("Transmissionswärmetransferkoeffizient H_T")
    st.caption(
        "Vereinfachte Demo-Bilanz mit manuell gesetzten Randbedingungen. "
        "H'_T wird beim Nichtwohngebaeude nur als informativer Huellkennwert gezeigt."
    )
    transmission_rows = thermal_transmission_table_rows(result)
    table_column, chart_column = st.columns((1, 2), gap="large")
    with table_column:
        st.dataframe(normalize_table_for_streamlit(transmission_rows), hide_index=True, width="stretch")
        base_heat_loss = (
            sum(
                float(row["F x U x A [W/K]"])
                for row in transmission_rows
                if row["F x U x A [W/K]"] is not None
            )
            if result.is_complete
            else None
        )
        thermal_bridge = (
            result.thermal_bridge_delta_u_w_m2k * result.envelope_area_m2
            if result.is_complete
            else None
        )
        summary_rows = [
            {"Kennwert": "Summe F x U x A", "Wert": base_heat_loss, "Einheit": "W/K"},
            {
                "Kennwert": "Waermebrueckenzuschlag",
                "Wert": thermal_bridge,
                "Einheit": "W/K",
            },
            {
                "Kennwert": "H_T",
                "Wert": result.heat_loss_coefficient_w_k,
                "Einheit": "W/K",
            },
            {
                "Kennwert": "H'_T",
                "Wert": result.heat_loss_coefficient_per_area_w_m2k,
                "Einheit": "W/(m2 K)",
            },
        ]
        st.dataframe(normalize_table_for_streamlit(summary_rows), hide_index=True, width="stretch")
    with chart_column:
        chart_rows = [
            {"Bauteil": row["Bauteil"], "F x U x A [W/K]": row["F x U x A [W/K]"]}
            for row in transmission_rows
            if row["F x U x A [W/K]"] is not None
        ]
        if chart_rows:
            st.bar_chart(chart_rows, x="Bauteil", y="F x U x A [W/K]")
        st.metric(
            "H'_T",
            (
                f"{result.heat_loss_coefficient_per_area_w_m2k:.3f} W/(m2 K)"
                if result.heat_loss_coefficient_per_area_w_m2k is not None
                else "nicht berechenbar"
            ),
        )
        st.caption(
            f"Manuelle Demo-Annahme: Delta U_WB = {DEFAULT_DELTA_U_WB_W_M2K:.2f} W/(m2 K)."
        )
    for warning in result.warnings:
        st.warning(warning)


def _render_thermal_source_status(spec) -> None:
    """Macht die Herkunft und Vorlaeufigkeit der U-Werte sichtbar."""
    relevant_assumptions = [
        assumption.text
        for assumption in spec.assumptions
        if assumption.location and assumption.location.startswith("simple_envelope")
    ]
    st.caption("Berechnet mit Demo-Annahmen; nicht gemessen und nicht als GEG-Nachweis freigegeben.")
    if relevant_assumptions:
        with st.expander("Herkunft und Grenzen der Huellkennwerte"):
            for assumption in relevant_assumptions:
                st.markdown(f"- {assumption}")


def _component_selection_label(component_id: str, rows: list[dict[str, object]]) -> str:
    row = next(item for item in rows if item["Bezeichnung"] == component_id)
    return f"{row['Nr.']} · {row['Bauteil']} · {component_id}"


def _orientation_label(orientation_deg: float | None) -> str:
    if orientation_deg is None:
        return "nicht verfuegbar"
    directions = ("N", "NO", "O", "SO", "S", "SW", "W", "NW")
    direction = directions[round((orientation_deg % 360.0) / 45.0) % len(directions)]
    return f"{direction} ({orientation_deg:g} Grad)"


def _render_rooms(spec) -> None:
    rows = building_room_rows(spec)
    if not rows:
        st.info("Die gewaehlte Spezifikation enthaelt keine erkannten Raeume.")
        return
    st.subheader("Raumbuch")
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")
    st.caption("Die Zonenzuordnung erfolgt ausschliesslich im Modul Zonen.")


def _render_construction_catalog(spec) -> None:
    """Zeigt Excel als alleinige Inhaltsquelle und schreibt nur Projektkopien."""
    catalog_types = {
        "Bauteile": "components",
        "Materialien": "materials",
        "Produkte": "products",
    }
    catalog_section = st.segmented_control(
        "Katalog",
        tuple(catalog_types),
        default="Bauteile",
        key="ma_building_catalog_section",
        selection_mode="single",
    )
    _render_excel_catalog_selection(spec, catalog_types[catalog_section or "Bauteile"])
    _render_user_catalog_drafts(catalog_types[catalog_section or "Bauteile"])


def _render_excel_catalog_selection(spec, catalog_type: str) -> None:
    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.error("Bitte zuerst ein Projekt auswaehlen.")
        return
    try:
        catalog = load_building_excel_catalog(catalog_type)
    except FileNotFoundError as exc:
        st.warning(f"Excel-Katalog fehlt: {exc}")
        return
    except (OSError, ValueError) as exc:
        st.error(f"Excel-Katalog ist nicht auswertbar: {exc}")
        return

    st.caption(
        f"Quelle: {catalog.source_path.as_posix()} | SHA-256: {catalog.source_sha256[:12]}…"
    )
    project_payload = _building_project_payload(workspace)
    stored_selections = project_payload.get("catalog_selections", {})
    stored_selection = (
        stored_selections.get(catalog_type, {})
        if isinstance(stored_selections, dict)
        else {}
    )
    if (
        isinstance(stored_selection, dict)
        and stored_selection.get("source_sha256")
        and stored_selection.get("source_sha256") != catalog.source_sha256
    ):
        st.warning(
            "Der zentrale Excel-Katalog wurde seit der Projektuebernahme geaendert. "
            "Die im Projekt gespeicherte Datensatzkopie bleibt unveraendert, bis du "
            "eine neue Auswahl ausdruecklich uebernimmst."
        )
    if not catalog.rows:
        st.info(
            "Die Arbeitsmappe ist vorhanden, enthaelt aber noch keine freigegebenen "
            f"{_catalog_type_label(catalog_type)}-Datensaetze."
        )
        return
    st.dataframe(
        normalize_table_for_streamlit(list(catalog.rows)),
        hide_index=True,
        width="stretch",
    )

    record_ids = [str(next(iter(row.values()))) for row in catalog.rows]
    selected_id = st.selectbox(
        f"{_catalog_type_label(catalog_type)} auswaehlen",
        record_ids,
        key=f"building_excel_catalog_{catalog_type}_record",
        on_change=_mark_building_draft,
    )
    selected_record = next(
        row for row in catalog.rows if str(next(iter(row.values()))) == selected_id
    )
    targets = [
        (element.element_id, element.element_type, element.construction_code)
        for element in spec.elements
    ] + [
        (opening.opening_id, opening.opening_type, opening.construction_code)
        for opening in spec.openings
    ]
    if not targets:
        st.warning("Das aktive Gebaeudemodell enthaelt keine zuweisbaren Elemente.")
        return
    target_id = st.selectbox(
        "Zielelement",
        [target[0] for target in targets],
        key=f"building_excel_catalog_{catalog_type}_target",
        on_change=_mark_building_draft,
    )
    target = next(item for item in targets if item[0] == target_id)
    scope = st.radio(
        "Geltungsbereich",
        ("Dieses Element", "Alle Elemente derselben Gruppe"),
        horizontal=True,
        key=f"building_excel_catalog_{catalog_type}_scope",
        on_change=_mark_building_draft,
    )
    st.markdown("##### Vorschau")
    st.dataframe(
        normalize_table_for_streamlit(
            [
                {"Merkmal": "Katalogtyp", "Wert": _catalog_type_label(catalog_type)},
                {"Merkmal": "Katalogeintrag", "Wert": selected_id},
                {"Merkmal": "Zielelement", "Wert": target_id},
                {"Merkmal": "Elementgruppe", "Wert": f"{target[1]} / {target[2]}"},
                {"Merkmal": "Geltungsbereich", "Wert": scope},
                *[
                    {"Merkmal": key, "Wert": value}
                    for key, value in selected_record.items()
                ],
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    if st.button(
        "Aenderungen in Projektkonfiguration uebernehmen",
        key=f"building_excel_catalog_{catalog_type}_apply",
    ):
        payload = project_payload
        selections = payload.setdefault("catalog_selections", {})
        if not isinstance(selections, dict):
            selections = {}
            payload["catalog_selections"] = selections
        selections[catalog_type] = building_excel_selection_payload(
            catalog,
            selected_record,
            target_id=target_id,
            target_group={
                "element_type": target[1],
                "construction_code": target[2],
            },
            scope="element" if scope == "Dieses Element" else "element_group",
        )
        try:
            save_project_module_config(workspace, "ma_building", payload)
        except (OSError, ValueError) as exc:
            st.error(f"Projektkonfiguration konnte nicht gespeichert werden: {exc}")
        else:
            clear_workspace_draft(st.session_state, "ma_building")
            st.success("Katalogauswahl wurde als projektbezogene Kopie gespeichert.")


def building_excel_selection_payload(
    catalog,
    selected_record: dict[str, object],
    *,
    target_id: str,
    target_group: dict[str, object],
    scope: str,
) -> dict[str, object]:
    """Erzeugt die unveraenderliche Projektkopie einer Excel-Auswahl."""
    return {
        "catalog_record_id": str(next(iter(selected_record.values()))),
        "target_element_id": target_id,
        "target_group": target_group,
        "scope": scope,
        "source_path": catalog.source_path.as_posix(),
        "source_version": f"sha256:{catalog.source_sha256[:12]}",
        "source_sha256": catalog.source_sha256,
        "source_sheet": "Übersicht",
        "catalog_record": dict(selected_record),
        "overrides": {},
    }


def _building_project_payload(workspace) -> dict[str, object]:
    payload = load_project_module_config(workspace, "ma_building")
    if not isinstance(payload, dict):
        payload = {}
    payload.setdefault("schema_version", "1.0")
    payload.setdefault("project_id", workspace.project.identity.project_id)
    return payload


def _catalog_type_label(catalog_type: str) -> str:
    return {
        "components": "Bauteile",
        "materials": "Materialien",
        "products": "Produkte",
    }[catalog_type]


def _mark_building_draft() -> None:
    mark_workspace_draft(st.session_state, "ma_building")


def _render_user_catalog_drafts(catalog_type: str) -> None:
    """Erfasst eigene Werte als lokale Entwuerfe, nie als Quellwert-Aenderung."""
    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        return
    with st.expander("Eigenen Katalogentwurf erfassen"):
        st.caption(
            "Eigene Eingaben bleiben als ungepruefter lokaler Entwurf gespeichert. "
            "Sie aendern keine Excel- oder Herstellerwerte."
        )
        label = st.text_input("Bezeichnung", key=f"building_user_draft_{catalog_type}_label")
        source_reference = st.text_input(
            "Herkunft / Begründung",
            key=f"building_user_draft_{catalog_type}_source_reference",
        )
        source_url = st.text_input("Quellen-URL (optional)", key=f"building_user_draft_{catalog_type}_source_url")
        details = st.text_area("Zusätzliche Angaben (optional)", key=f"building_user_draft_{catalog_type}_details")
        if st.button("Lokalen Entwurf speichern", key=f"building_user_draft_{catalog_type}_save"):
            try:
                draft = create_user_catalog_draft(
                    catalog_type=catalog_type,
                    label=label,
                    source_reference=source_reference,
                    source_url=source_url,
                    details=details,
                )
                payload = _building_project_payload(workspace)
                drafts_by_type = payload.setdefault("user_catalog_drafts", {})
                if not isinstance(drafts_by_type, dict):
                    raise ValueError("Lokale Katalogentwuerfe haben ein ungueltiges Format.")
                drafts = drafts_by_type.setdefault(catalog_type, [])
                if not isinstance(drafts, list):
                    raise ValueError("Lokale Katalogentwuerfe haben ein ungueltiges Format.")
                drafts.append(draft)
                save_project_module_config(workspace, "ma_building", payload)
            except (OSError, ValueError) as exc:
                st.error(f"Lokaler Katalogentwurf konnte nicht gespeichert werden: {exc}")
            else:
                clear_workspace_draft(st.session_state, "ma_building")
                st.success("Lokaler Katalogentwurf wurde als user_unverified gespeichert.")

    payload = _building_project_payload(workspace)
    drafts_by_type = payload.get("user_catalog_drafts", {})
    drafts = drafts_by_type.get(catalog_type, []) if isinstance(drafts_by_type, dict) else []
    if isinstance(drafts, list) and drafts:
        st.caption(f"Lokale Entwuerfe ({len(drafts)}): " + ", ".join(str(draft.get("label", "ohne Name")) for draft in drafts if isinstance(draft, dict)))


def _render_wall_construction_catalog() -> None:
    st.subheader("Konstruktionen")
    catalog = _load_catalog_for_ui("wall_constructions")
    if catalog is None:
        return
    max_layers = max((len(record.get("layers", [])) for record in catalog.records), default=0)
    rows = []
    for record in catalog.records:
        row = {
            "Name": record["name"],
            "ID": record["wall_construction_id"],
            "U-Wert [W/(m2 K)]": record.get("u_value_w_m2k"),
            "Dicke [m]": record.get("thickness_m"),
        }
        for layer_number in range(1, max_layers + 1):
            layers = record.get("layers", [])
            layer = layers[layer_number - 1] if layer_number <= len(layers) else {}
            row[f"Schicht {layer_number}"] = layer.get("material_name", "")
        rows.append(row)
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")


def _render_surface_catalog() -> None:
    st.subheader("Surfaces")
    _render_local_catalog_table(
        "surfaces",
        [
            "name",
            "surface_id",
            "group",
            "surface_type",
            "wetted_area_m2",
            "connected_to",
            "construction_name",
            "u_value_w_m2k",
            "thickness_m",
        ],
        {
            "name": "Name",
            "surface_id": "ID",
            "group": "Gruppe",
            "surface_type": "Typ",
            "wetted_area_m2": "Flaeche [m2]",
            "connected_to": "Angrenzend",
            "construction_name": "Konstruktion",
            "u_value_w_m2k": "U-Wert [W/(m2 K)]",
            "thickness_m": "Dicke [m]",
        },
    )


def _render_products(spec) -> None:
    rows = [
        {
            "Name": opening.opening_type,
            "ID": opening.opening_id,
            "Code": opening.construction_code,
            "Flaeche [m2]": opening.area_m2,
            "Host-Bauteil": opening.host_element_id,
        }
        for opening in spec.openings
    ]
    if rows:
        st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")
    else:
        st.info("Keine Fenster oder Tueren in der gewaehlten Spezifikation vorhanden.")


def _render_local_catalog_table(catalog_key: str, fields: list[str], labels: dict[str, str]) -> None:
    catalog = _load_catalog_for_ui(catalog_key)
    if catalog is None:
        return
    rows = [{labels[field]: record.get(field, "") for field in fields} for record in catalog.records]
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")


def _load_catalog_for_ui(catalog_key: str):
    try:
        return load_local_building_catalog(catalog_key)
    except FileNotFoundError:
        st.info("Dieser lokale Referenzkatalog ist auf diesem Rechner nicht vorhanden.")
    except (OSError, LocalCatalogValidationError, ValueError) as exc:
        st.error(f"Lokaler Referenzkatalog ist vorhanden, aber fehlerhaft: {exc}")
    return None


def _render_construction_assignment(spec, catalog: DemoCatalog) -> None:
    targets = [(element.element_id, element.construction_code, element.element_type) for element in spec.elements] + [
        (opening.opening_id, opening.construction_code, opening.opening_type) for opening in spec.openings
    ]
    if not targets:
        st.info("Fuer diese Spezifikation sind keine Bauteile oder Oeffnungen fuer eine Konstruktion vorhanden.")
        return

    target_id = st.selectbox(
        "Bauteil oder Oeffnung", [target[0] for target in targets], key="building_construction_target"
    )
    _target_id, construction_code, target_type = next(target for target in targets if target[0] == target_id)
    candidates = tuple(
        record
        for record in catalog.records_for("constructions")
        if record.data["construction_code"] == construction_code
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
                [
                    {"Merkmal": "Zuordnung", "Wert": "Keine Konstruktion zugeordnet"},
                    {"Merkmal": "Bauartcode", "Wert": construction_code},
                ]
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
    return load_named_building_specification(option_key)


def _active_building_spec_key() -> str:
    """Liefert fuer Folgereiter den aktivierten statt des blossen Entwurfsstands."""
    workspace = get_active_workspace(st.session_state)
    payload = _building_project_payload(workspace) if workspace is not None else {}
    return resolve_active_building_spec_key(
        workspace_present=workspace is not None,
        project_payload=payload,
        session_key=str(st.session_state.get("building_applied_specification_key", "")),
        default_key=_default_building_spec_key(),
    )


def resolve_active_building_spec_key(
    *,
    workspace_present: bool,
    project_payload: dict[str, object],
    session_key: str,
    default_key: str,
) -> str:
    """Loest den Aktivstand auf, ohne ihn zwischen Projekten zu vererben."""
    option_keys = {key for key, _label, _source in BUILDING_SPECIFICATION_OPTIONS}
    if workspace_present:
        selection = project_payload.get("building_specification", {})
        if isinstance(selection, dict):
            selected_key = str(selection.get("selection_key", ""))
            if selected_key in option_keys:
                return selected_key
        return default_key
    return session_key if session_key in option_keys else default_key


def _default_building_spec_key() -> str:
    workspace = get_active_workspace(st.session_state)
    if workspace is not None and workspace.project.identity.title == "Masterarbeit-Analyse":
        return "small_office_5z_endvariant_02"
    if workspace is not None and workspace.project.identity.title == "Demo-Project1":
        return "business_integration_lod1"
    return "demo"


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
