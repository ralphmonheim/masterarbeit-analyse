"""Fachansicht fuer technische Systeme."""

from __future__ import annotations

from collections.abc import Sequence

import streamlit as st

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
    st.metric("Freigabestatus", validation_result.release_status.value)
    st.dataframe(normalize_table_for_streamlit(technical_summary_rows(technical_spec)), hide_index=True, width="stretch")

    system_tab, scope_tab = st.tabs(["Systeme", "Einordnung"])
    with system_tab:
        st.dataframe(normalize_table_for_streamlit(technical_system_rows(technical_spec)), hide_index=True, width="stretch")
    with scope_tab:
        st.dataframe(normalize_table_for_streamlit(technical_scope_rows()), hide_index=True, width="stretch")
        st.info(module.next_step)

    if technical_spec.assumptions:
        st.dataframe(
            normalize_table_for_streamlit(
                [
                    {"ID": assumption.assumption_id, "Fundstelle": assumption.location or "", "Annahme": assumption.text}
                    for assumption in technical_spec.assumptions
                ]
            ),
            hide_index=True,
            width="stretch",
        )
    _render_messages(validation_result.messages)


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
