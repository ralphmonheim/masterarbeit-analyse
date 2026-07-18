"""Fachansicht fuer technische Systeme."""

from __future__ import annotations

from collections.abc import Sequence

import streamlit as st

from ma_database import CatalogSelection, DemoCatalogRecord, load_demo_catalog, select_demo_record
from ma_technical import (
    TechnicalSystemSpecification,
    load_business_integration_lod1_technical_spec,
    validate_technical_spec,
)
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_validation import DiagnosticMessage, DiagnosticSeverity
from ma_workflow import get_module_definition
from ma_zones import load_business_integration_lod1_zone_spec

TECHNICAL_WORKSPACE_TAB_LABELS = ("Technikmodell", "Übersicht", "Auswahl")
TECHNICAL_SELECTION_TAB_LABELS = (
    "Heizung",
    "Kuehlung",
    "Lueftung",
    "Speicher",
    "Trinkwarmwasser",
    "Elektrik",
)


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
    try:
        zone_spec = load_business_integration_lod1_zone_spec()
        technical_spec = load_business_integration_lod1_technical_spec()
    except (OSError, ValueError) as exc:
        st.error(f"Technikspezifikation konnte nicht geladen werden: {exc}")
        return

    validation_result = validate_technical_spec(technical_spec, zone_spec=zone_spec)
    model_tab, overview_tab, selection_tab = st.tabs(TECHNICAL_WORKSPACE_TAB_LABELS)
    with model_tab:
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

    with overview_tab:
        _render_technical_selection_overview()
    with selection_tab:
        st.caption("Die Auswahl bleibt ein synthetischer Sitzungsentwurf und wird erst mit Speichern uebernommen.")
        heating_tab, cooling_tab, ventilation_tab, storage_tab, dhw_tab, electrical_tab = st.tabs(
            TECHNICAL_SELECTION_TAB_LABELS
        )
        with heating_tab:
            _render_technical_topic("heating", "Heizung", "heating_generators")
        with cooling_tab:
            _render_technical_topic("cooling", "Kuehlung", "cooling_generators")
        with ventilation_tab:
            _render_technical_topic("ventilation", "Lueftung")
        with storage_tab:
            _render_technical_topic("storage", "Speicher", "thermal_storages")
        with dhw_tab:
            _render_technical_topic("domestic_hot_water", "Trinkwarmwasser")
        with electrical_tab:
            _render_technical_topic("electrical", "Elektrik")
        if st.button("Technikauswahl speichern", type="primary", key="technical_selection_save"):
            _save_technical_selection()
            st.success("Technikauswahl wurde fuer diese Sitzung uebernommen.")


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
