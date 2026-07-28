"""Fachansicht fuer technische Systeme."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import streamlit as st

from ma_database import CatalogSelection, DemoCatalogRecord, load_demo_catalog, select_demo_record
from ma_technical import (
    TechnicalSystemSpecification,
    load_business_integration_lod1_technical_spec,
    load_small_office_5z_endvariant_02_technical_spec,
    load_technical_excel_catalog,
    technical_catalog_record_status,
    validate_technical_spec,
)
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_ui.streamlit_app.state import (
    clear_workspace_draft,
    get_active_workspace,
    mark_workspace_draft,
    small_office_v1_uses_reference_zone_model,
)
from ma_validation import DiagnosticMessage, DiagnosticSeverity
from ma_workflow import get_module_definition
from ma_workspace import load_project_module_config, save_project_module_config

TECHNICAL_WORKSPACE_TAB_LABELS = ("Technikmodell", "Übersicht", "Auswahl")
TECHNICAL_SELECTION_TAB_LABELS = (
    "Heizung",
    "Kuehlung",
    "Lueftung",
    "Speicher",
    "Trinkwarmwasser",
    "Elektrik",
)
TECHNICAL_CATALOG_DIRECTORY = Path("data/catalogs/technical_systems")


def technical_scope_rows() -> list[dict[str, object]]:
    """Liefert den aktuellen geplanten Umfang von ma_technical."""
    module = get_module_definition("ma_technical")
    return [
        {"Bereich": "Status", "Stand": module.status, "Einordnung": "P014-S1 Lite"},
        {"Bereich": "Eingabe", "Stand": "Zonenanforderungen", "Einordnung": "kommt validiert aus ma_zones"},
        {"Bereich": "Eingabe", "Stand": "System- und Produktdaten", "Einordnung": "LoD-1-Demo vorhanden"},
        {"Bereich": "Ausgabe", "Stand": "validierte Technikdaten", "Einordnung": "Zielrichtung ma_parameters"},
        {"Bereich": "Abgrenzung", "Stand": "keine Variantenbildung", "Einordnung": "bleibt in ma_variants"},
        {"Bereich": "Naechster Fokus", "Stand": "ParameterSnapshot", "Einordnung": "folgt in P015"},
    ]


def technical_summary_rows(spec: TechnicalSystemSpecification) -> list[dict[str, object]]:
    """Liefert kompakte Kennwerte einer TechnicalSystemSpecification."""
    return [
        {"Kennwert": "Technikmodell", "Wert": spec.technical_model_id},
        {"Kennwert": "Gebaeude", "Wert": spec.building_id},
        {"Kennwert": "Zonenmodell", "Wert": spec.source_zone_model_id},
        {"Kennwert": "Eingabe-LoD", "Wert": _display_value(spec.input_detail_level)},
        {"Kennwert": "Systeme", "Wert": len(spec.systems)},
    ]


def technical_system_rows(spec: TechnicalSystemSpecification) -> list[dict[str, object]]:
    """Bereitet technische Systeme fuer die UI auf."""
    return [
        {
            "System": system.system_id,
            "Name": system.name,
            "Typ": system.system_type,
            "Zonen": ", ".join(system.served_zone_ids),
            "Leistung [W/m2]": system.design_power_w_m2,
            "Zuluft/Versorgung [Grad C]": system.supply_temperature_c,
            "Ruecklauf [Grad C]": system.return_temperature_c,
            "Leistungszahl": system.performance_factor,
            "Luftwechsel [1/h]": system.air_change_rate_1_h,
            "WRG [%]": system.heat_recovery_efficiency_percent,
            "Regelung": system.control_strategy,
        }
        for system in spec.systems
    ]


def render() -> None:
    """Zeigt die LoD-1-Technikspezifikation und ihre Validierung."""
    module = get_module_definition("ma_technical")
    render_page_header(module.label, module.purpose)
    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.warning("Bitte zuerst ein Projekt auswaehlen.")
        return
    try:
        zone_payload = load_project_module_config(workspace, "ma_zones") or {}
        if not small_office_v1_uses_reference_zone_model(zone_payload):
            st.error(
                "Das 29Z-Modell ist noch nicht weitergabefaehig. "
                "Bitte in Zonen den validierten 5Z-Referenzstand aktivieren."
            )
            return
        technical_spec = (
            load_small_office_5z_endvariant_02_technical_spec()
            if workspace.project.identity.title == "Masterarbeit-Analyse"
            else load_business_integration_lod1_technical_spec()
        )
    except (OSError, ValueError) as exc:
        st.error(f"Technikspezifikation konnte nicht geladen werden: {exc}")
        return

    validation_result = validate_technical_spec(technical_spec)
    section = st.segmented_control(
        "Technikbereich",
        TECHNICAL_WORKSPACE_TAB_LABELS,
        default=TECHNICAL_WORKSPACE_TAB_LABELS[0],
        key="ma_technical_workspace_section",
        selection_mode="single",
    )
    section = section or TECHNICAL_WORKSPACE_TAB_LABELS[0]
    if section == "Technikmodell":
        st.metric("Freigabestatus", validation_result.release_status.value)
        st.dataframe(
            normalize_table_for_streamlit(technical_summary_rows(technical_spec)), hide_index=True, width="stretch"
        )
        st.dataframe(
            normalize_table_for_streamlit(technical_system_rows(technical_spec)), hide_index=True, width="stretch"
        )
        if technical_spec.assumptions:
            st.dataframe(
                normalize_table_for_streamlit(
                    [
                        {
                            "ID": assumption.assumption_id,
                            "Fundstelle": assumption.location or "",
                            "Annahme": assumption.text,
                        }
                        for assumption in technical_spec.assumptions
                    ]
                ),
                hide_index=True,
                width="stretch",
            )
        _render_messages(validation_result.messages)

    elif section == "Übersicht":
        _render_fixed_technical_reference(technical_spec)
    else:
        _render_fixed_technical_selection(technical_spec)


def _render_fixed_technical_reference(spec: TechnicalSystemSpecification) -> None:
    """Zeigt die für die Arbeit verbindliche Referenz ohne Auswahlentwurf."""

    st.subheader("Referenz-Techniksatz")
    st.caption("Der Techniksatz ist für die Masterarbeit fest. Varianten ändern nur freigegebene Zonenparameter.")
    st.dataframe(normalize_table_for_streamlit(technical_system_rows(spec)), hide_index=True, width="stretch")


def _render_fixed_technical_selection(spec: TechnicalSystemSpecification) -> None:
    """Zeigt Excel-Datensaetze und uebernimmt nur bewusst ausgewaehlte Quellen."""

    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.error("Bitte zuerst ein Projekt auswaehlen.")
        return
    selected_area = st.segmented_control(
        "Systembereich",
        TECHNICAL_SELECTION_TAB_LABELS,
        default=TECHNICAL_SELECTION_TAB_LABELS[0],
        key="ma_technical_excel_system_area",
        selection_mode="single",
    )
    selected_area = selected_area or TECHNICAL_SELECTION_TAB_LABELS[0]
    st.caption(
        f"Bearbeitungsbereich: {selected_area}. Die Excel-Zeile bleibt die einzige Inhaltsquelle."
    )
    catalog_files = tuple(sorted(TECHNICAL_CATALOG_DIRECTORY.glob("*.xlsx")))
    if not catalog_files:
        st.warning(
            "Quelle fehlt: Für technische Systempakete ist noch kein Excel-Katalog unter "
            f"`{TECHNICAL_CATALOG_DIRECTORY.as_posix()}` vorhanden. Es werden keine Produktdaten erfunden."
        )
        st.caption("Die vorhandene Config bleibt nur als Referenzvorlage sichtbar.")
        st.dataframe(
            normalize_table_for_streamlit(technical_system_rows(spec)),
            hide_index=True,
            width="stretch",
        )
        return

    selected_catalog = st.selectbox(
        "Techniksystem-Katalog",
        catalog_files,
        format_func=lambda path: path.name,
        key="technical_catalog_file",
    )
    try:
        catalog = load_technical_excel_catalog(selected_catalog)
    except (OSError, ValueError) as exc:
        st.error(f"Techniksystem-Katalog konnte nicht gelesen werden: {exc}")
        return

    st.caption(f"Excel-Quelle: {catalog.source_path.as_posix()} · SHA-256: {catalog.source_sha256}")
    st.dataframe(
        normalize_table_for_streamlit(technical_excel_catalog_rows(catalog.rows, catalog.id_column)),
        hide_index=True,
        width="stretch",
    )
    selected_id = st.selectbox(
        "Techniksystem-Entwurf",
        [str(row[catalog.id_column]) for row in catalog.rows],
        format_func=lambda record_id: _technical_excel_option_label(catalog.rows, catalog.id_column, record_id),
        key="technical_excel_catalog_selection",
        on_change=_mark_technical_draft,
    )
    selected_record = next(row for row in catalog.rows if str(row[catalog.id_column]) == selected_id)
    active, validated, validation_status = technical_catalog_record_status(selected_record)
    st.dataframe(
        normalize_table_for_streamlit(
            [
                {"Merkmal": "Auswahl", "Wert": selected_id},
                {"Merkmal": "Aktiv", "Wert": "ja" if active else "nein"},
                {"Merkmal": "Validiert", "Wert": "ja" if validated else "nein"},
                {"Merkmal": "Validierungsstatus", "Wert": validation_status},
                *[{"Merkmal": key, "Wert": value} for key, value in selected_record.items()],
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    if not active or not validated:
        st.warning("Nur aktive und validierte Excel-Datensaetze duerfen projektbezogen uebernommen werden.")
    if st.button(
        "Ausgewählten Techniksystem-Entwurf projektbezogen übernehmen",
        key="technical_apply_excel_catalog_selection",
        disabled=not active or not validated,
    ):
        payload = _technical_project_payload(workspace)
        payload["excel_catalog_selection"] = {
            **technical_excel_selection_payload(catalog, selected_record),
            "system_area": selected_area,
        }
        try:
            save_project_module_config(workspace, "ma_technical", payload)
        except (OSError, ValueError) as exc:
            st.error(f"Projektkonfiguration konnte nicht gespeichert werden: {exc}")
        else:
            clear_workspace_draft(st.session_state, "ma_technical")
            st.success("Der validierte Techniksystem-Entwurf wurde projektbezogen gespeichert.")


def technical_excel_catalog_rows(rows: tuple[dict[str, object], ...], id_column: str) -> list[dict[str, object]]:
    """Add transparent source statuses without changing the Excel record content."""
    result: list[dict[str, object]] = []
    for row in rows:
        active, validated, status = technical_catalog_record_status(row)
        result.append(
            {
                id_column: row[id_column],
                "Aktiv": "ja" if active else "nein",
                "Validiert": "ja" if validated else "nein",
                "Validierungsstatus": status,
                **{key: value for key, value in row.items() if key != id_column},
            }
        )
    return result


def technical_excel_selection_payload(catalog, record: dict[str, object]) -> dict[str, object]:
    """Create the small project-owned reference to a selected, unchanged Excel record."""
    active, validated, validation_status = technical_catalog_record_status(record)
    if not active or not validated:
        raise ValueError("Nur aktive und validierte Techniksystem-Datensaetze duerfen uebernommen werden.")
    return {
        "catalog_record_id": str(record[catalog.id_column]),
        "source_path": catalog.source_path.as_posix(),
        "source_version": f"sha256:{catalog.source_sha256[:12]}",
        "source_sha256": catalog.source_sha256,
        "source_sheet": "Übersicht",
        "active": active,
        "validated": validated,
        "validation_status": validation_status,
        "record": dict(record),
    }


def _technical_excel_option_label(rows: tuple[dict[str, object], ...], id_column: str, record_id: str) -> str:
    row = next(row for row in rows if str(row[id_column]) == record_id)
    active, validated, status = technical_catalog_record_status(row)
    return f"{record_id} · {'aktiv' if active else 'inaktiv'} · {status} · {'validiert' if validated else 'nicht validiert'}"


def _technical_project_payload(workspace) -> dict[str, object]:
    payload = load_project_module_config(workspace, "ma_technical")
    if not isinstance(payload, dict):
        payload = {}
    payload.setdefault("schema_version", "1.0")
    payload.setdefault("project_id", workspace.project.identity.project_id)
    return payload


def _mark_technical_draft() -> None:
    mark_workspace_draft(st.session_state, "ma_technical")


def _render_technical_topic(topic_key: str, label: str, catalog_category: str | None = None) -> None:
    """Shows one technical topic with an explicit not-installed option."""
    catalog = None
    records = ()
    if catalog_category is not None:
        try:
            catalog = load_demo_catalog()
        except FileNotFoundError:
            st.info("Lokale Katalogdaten sind nicht Bestandteil des Repositorys und wurden hier nicht gefunden.")
        except (OSError, ValueError) as exc:
            st.error(f"Lokaler Demo-Katalog konnte nicht geladen werden: {exc}")
        else:
            records = catalog.records_for(catalog_category)
    options = ["not_installed", *[record.record_id for record in records]]
    if not records:
        options.append("present_without_demo_record")
    selected_id = st.selectbox(
        label,
        options,
        format_func=lambda option_id, available_records=records: _technical_option_label(available_records, option_id),
        key=f"technical_topic_{topic_key}",
    )
    selection_key = f"technical_topic_draft_selection_{topic_key}"
    if selected_id == "not_installed":
        st.session_state[selection_key] = {"availability": "not_installed", "topic": topic_key}
        st.dataframe(
            normalize_table_for_streamlit(
                [
                    {"Merkmal": "Status", "Wert": "Nicht vorhanden"},
                    {"Merkmal": "Verfuegbarkeit", "Wert": "not_installed"},
                ]
            ),
            hide_index=True,
            width="stretch",
        )
        return
    if selected_id == "present_without_demo_record":
        st.session_state[selection_key] = {"availability": "planned", "topic": topic_key}
        st.dataframe(
            normalize_table_for_streamlit(
                [
                    {"Merkmal": "Status", "Wert": "Vorhanden, noch ohne Demo-Datensatz"},
                    {"Merkmal": "Verfuegbarkeit", "Wert": "planned"},
                ]
            ),
            hide_index=True,
            width="stretch",
        )
        return

    if catalog is None or catalog_category is None:
        raise RuntimeError("Eine lokale Katalogauswahl braucht einen geladenen Katalog und eine Kategorie.")
    selection = select_demo_record(catalog, category=catalog_category, record_id=selected_id)
    st.session_state[selection_key] = selection
    selected_record = next(record for record in records if record.record_id == selected_id)
    st.warning("Demo-Wert: fachlich nicht verifiziert und nicht simulationsbereit.")
    st.dataframe(
        normalize_table_for_streamlit(_demo_record_rows(selected_record, selection)),
        hide_index=True,
        width="stretch",
    )


def _render_technical_selection_overview() -> None:
    """Displays the session-only choices from the individual technical tabs."""
    topic_labels = {
        "heating": "Heizung",
        "cooling": "Kuehlung",
        "ventilation": "Lueftung",
        "storage": "Speicher",
        "domestic_hot_water": "Trinkwarmwasser",
        "electrical": "Elektrik",
    }
    rows = []
    for topic_key, label in topic_labels.items():
        selection = st.session_state.get(f"technical_topic_selection_{topic_key}")
        if isinstance(selection, CatalogSelection):
            value = selection.label
            status = selection.selection_status
        elif isinstance(selection, dict):
            value = (
                "Nicht vorhanden"
                if selection.get("availability") == "not_installed"
                else "Vorhanden ohne Demo-Datensatz"
            )
            status = str(selection.get("availability"))
        else:
            value = "Noch nicht ausgewaehlt"
            status = "unknown"
        rows.append({"Thema": label, "Auswahl": value, "Status": status})
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")


def _save_technical_selection() -> None:
    """Uebernimmt nur den sichtbaren Sitzungsentwurf, ohne die Ansicht zu verlassen."""
    for topic_key in (
        "heating",
        "cooling",
        "ventilation",
        "storage",
        "domestic_hot_water",
        "electrical",
    ):
        draft_key = f"technical_topic_draft_selection_{topic_key}"
        if draft_key in st.session_state:
            st.session_state[f"technical_topic_selection_{topic_key}"] = st.session_state[draft_key]


def _technical_option_label(records: tuple[DemoCatalogRecord, ...], option_id: str) -> str:
    if option_id == "not_installed":
        return "Nicht vorhanden"
    if option_id == "present_without_demo_record":
        return "Vorhanden, noch ohne Demo-Datensatz"
    return _demo_label(records, option_id)


def _demo_label(records: tuple[DemoCatalogRecord, ...], record_id: str) -> str:
    record = next(record for record in records if record.record_id == record_id)
    return f"{record.label} ({record.record_id})"


def _demo_record_rows(record: DemoCatalogRecord, selection: CatalogSelection) -> list[dict[str, object]]:
    """Keeps the selected record inspectable without exposing it as an editable model."""
    fields = [
        ("ID", record.record_id),
        ("Name", record.label),
        ("Kategorie", record.category),
        ("Auswahlstatus", selection.selection_status),
        ("Pruefstatus", record.data["verification_status"]),
        ("Bestaetigung", record.data["confirmation_status"]),
    ]
    return [{"Merkmal": name, "Wert": value} for name, value in fields]


def _display_value(value) -> str:
    return str(value.value if hasattr(value, "value") else value)


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
    if not rows:
        st.success("Keine Validierungsmeldungen.")
        return
    if any(row["Schwere"] == DiagnosticSeverity.ERROR.value for row in rows):
        st.error("Fehler blockieren die Freigabe.")
    elif any(row["Schwere"] == DiagnosticSeverity.WARNING.value for row in rows):
        st.warning("Warnungen benoetigen eine bewusste Freigabeentscheidung.")
    else:
        st.info("Nur Informationsmeldungen vorhanden.")
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")
