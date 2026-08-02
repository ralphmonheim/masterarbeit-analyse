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
    FACHLICHER_TEIL_REFERENCE_IFC_FILENAME,
    LocalCatalogValidationError,
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

BUILDING_WORKSPACE_TAB_LABELS = ("Import", "Uebersicht", "Bauteile", "Raeume", "Konstruktionen/Kataloge")
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
            spec = _load_building_spec_option(
                str(
                    st.session_state.get(
                        "building_specification_draft_key",
                        _default_building_spec_key(),
                    )
                )
            )
        except (OSError, ValueError) as exc:
            st.error(f"Gebaeudespezifikation konnte nicht geladen werden: {exc}")
            return
    if spec is None:
        return
    if section == "Uebersicht":
        _render_building_overview(spec)
    elif section == "Bauteile":
        _render_elements(spec)
    elif section == "Raeume":
        _render_rooms(spec)
    elif section == "Konstruktionen/Kataloge":
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
    st.dataframe(
        normalize_table_for_streamlit(building_master_data_rows(spec)),
        hide_index=True,
        width="stretch",
    )
    if st.button("Gebaeudespezifikation uebernehmen", key="building_apply_specification"):
        workspace = get_active_workspace(st.session_state)
        if workspace is None:
            st.error("Bitte zuerst ein Projekt auswaehlen.")
        else:
            payload = _building_project_payload(workspace)
            payload["building_specification"] = {
                "selection_key": selected_key,
                "building_id": spec.building.building_id,
                "model_version": spec.model_version.version_id,
            }
            save_project_module_config(workspace, "ma_building", payload)
            st.session_state["building_applied_specification_key"] = selected_key
            clear_workspace_draft(st.session_state, "ma_building")
            st.success("Gebaeudespezifikation wurde in die Projektkonfiguration uebernommen.")
    elif st.session_state.get("building_applied_specification_key") != selected_key:
        st.info("Die Auswahl ist eine Vorschau und noch nicht in die Projektkonfiguration uebernommen.")
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
    spec = _load_building_spec_option(
        str(
            st.session_state.get(
                "building_specification_draft_key",
                _default_building_spec_key(),
            )
        )
    )
    if input_mode == "3D-Datei":
        spec = _select_building_specification()
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
    return spec


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
