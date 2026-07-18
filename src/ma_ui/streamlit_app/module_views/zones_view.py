"""Fachansicht fuer thermische Zonen."""

from __future__ import annotations

from collections.abc import Sequence

import streamlit as st

from ma_building import load_business_integration_lod1_building_spec
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_validation import DiagnosticMessage, DiagnosticSeverity
from ma_workflow import get_module_definition
from ma_zones import (
    ZoneModelSpecification,
    load_business_integration_lod1_zone_spec,
    validate_zone_spec,
)

ZONE_WORKSPACE_TAB_LABELS = ("Übersicht", "Nutzungsprofile zuweisen")
SYNTHETIC_USAGE_PROFILE_OPTIONS = (
    ("synthetic_office", "Demo-Buero (synthetisch)"),
    ("synthetic_education", "Demo-Lernen (synthetisch)"),
)


def zones_scope_rows() -> list[dict[str, object]]:
    """Liefert den aktuellen geplanten Umfang von ma_zones."""
    module = get_module_definition("ma_zones")
    return [
        {"Bereich": "Status", "Stand": module.status, "Einordnung": "P013-S1 LoD-1"},
        {"Bereich": "Eingabe", "Stand": "Raumdaten", "Einordnung": "kommt validiert aus ma_building"},
        {"Bereich": "Eingabe", "Stand": "Nutzungsanforderungen", "Einordnung": "LoD-1-Demo vorhanden"},
        {"Bereich": "Ausgabe", "Stand": "validierte Zonendaten", "Einordnung": "Zielrichtung ma_parameters"},
        {"Bereich": "Abgrenzung", "Stand": "keine Gebaeudegeometrie", "Einordnung": "bleibt in ma_building"},
        {"Bereich": "Abgrenzung", "Stand": "keine Anlagenberechnung", "Einordnung": "bleibt in ma_technical"},
    ]


def zone_summary_rows(spec: ZoneModelSpecification) -> list[dict[str, object]]:
    """Liefert kompakte Kennwerte einer ZoneModelSpecification."""
    total_floor_area = sum(zone.floor_area_m2 for zone in spec.zones)
    total_volume = sum(zone.volume_m3 for zone in spec.zones)
    return [
        {"Kennwert": "Zonenmodell", "Wert": spec.zone_model_id},
        {"Kennwert": "Gebaeude", "Wert": spec.building_id},
        {"Kennwert": "Eingabe-LoD", "Wert": _display_value(spec.input_detail_level)},
        {"Kennwert": "Zonen", "Wert": len(spec.zones)},
        {"Kennwert": "Nutzungsprofile", "Wert": len(spec.usage_profiles)},
        {"Kennwert": "Zonenflaeche [m2]", "Wert": total_floor_area},
        {"Kennwert": "Zonenvolumen [m3]", "Wert": total_volume},
    ]


def thermal_zone_rows(spec: ZoneModelSpecification) -> list[dict[str, object]]:
    """Bereitet thermische Zonen fuer die UI auf."""
    return [
        {
            "Zone": zone.zone_id,
            "Name": zone.name,
            "Nutzungsprofil": zone.usage_profile_id,
            "Flaeche [m2]": zone.floor_area_m2,
            "Volumen [m3]": zone.volume_m3,
            "Heizen [Grad C]": zone.heating_setpoint_c,
            "Kuehlen [Grad C]": zone.cooling_setpoint_c,
            "Mindestluftwechsel [1/h]": zone.minimum_air_change_rate_1_h,
        }
        for zone in spec.zones
    ]


def usage_profile_rows(spec: ZoneModelSpecification) -> list[dict[str, object]]:
    """Bereitet Nutzungsprofile fuer die UI auf."""
    return [
        {
            "Profil": profile.profile_id,
            "Name": profile.name,
            "Betrieb Start": profile.operation_start_hour,
            "Betrieb Ende": profile.operation_end_hour,
            "Tage/Woche": profile.operation_days_per_week,
            "Belegung [m2/P]": profile.occupancy_density_m2_per_person,
            "Beleuchtung [W/m2]": profile.lighting_power_w_m2,
            "Geraete [W/m2]": profile.equipment_power_w_m2,
        }
        for profile in spec.usage_profiles
    ]


def zone_overview_rows(spec: ZoneModelSpecification, assignments: dict[str, str]) -> list[dict[str, object]]:
    """Zeigt Zonen mit der in dieser Sitzung gespeicherten Profilzuordnung."""
    profiles = {profile.profile_id: profile for profile in spec.usage_profiles}
    profile_labels = {profile_id: profile.name for profile_id, profile in profiles.items()}
    profile_labels.update(dict(SYNTHETIC_USAGE_PROFILE_OPTIONS))
    rows: list[dict[str, object]] = []
    for zone in spec.zones:
        profile_id = assignments.get(zone.zone_id, zone.usage_profile_id)
        row = {
            "Zone": zone.zone_id,
            "Name": zone.name,
            "Nutzungsprofil": profile_labels.get(profile_id, profile_id),
            "Profil-ID": profile_id,
            "Flaeche [m2]": zone.floor_area_m2,
            "Volumen [m3]": zone.volume_m3,
        }
        if profile_id in profiles:
            profile = profiles[profile_id]
            row.update(
                {
                    "Betrieb [h]": f"{profile.operation_start_hour:g}-{profile.operation_end_hour:g}",
                    "Heizen [Grad C]": zone.heating_setpoint_c,
                    "Kuehlen [Grad C]": zone.cooling_setpoint_c,
                }
            )
        else:
            row.update({"Betrieb [h]": "Demo-Annahme", "Heizen [Grad C]": "", "Kuehlen [Grad C]": ""})
        rows.append(row)
    return rows


def render() -> None:
    """Zeigt die LoD-1-Zonenspezifikation und ihre Validierung."""
    module = get_module_definition("ma_zones")
    render_page_header(module.label, module.purpose)
    try:
        building_spec = load_business_integration_lod1_building_spec()
        zone_spec = load_business_integration_lod1_zone_spec()
    except (OSError, ValueError) as exc:
        st.error(f"Zonenspezifikation konnte nicht geladen werden: {exc}")
        return

    validation_result = validate_zone_spec(zone_spec, building_spec=building_spec)
    st.metric("Freigabestatus", validation_result.release_status.value)
    st.dataframe(normalize_table_for_streamlit(zone_summary_rows(zone_spec)), hide_index=True, width="stretch")

    overview_tab, assignment_tab = st.tabs(ZONE_WORKSPACE_TAB_LABELS)
    with overview_tab:
        st.dataframe(
            normalize_table_for_streamlit(zone_overview_rows(zone_spec, _saved_zone_assignments())),
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "Zentrale Profilwerte werden fuer vorhandene Referenzprofile angezeigt. Demo-Profile bleiben Annahmen."
        )
        st.dataframe(normalize_table_for_streamlit(usage_profile_rows(zone_spec)), hide_index=True, width="stretch")
    with assignment_tab:
        _render_usage_profile_assignment(zone_spec)

    if zone_spec.assumptions:
        st.dataframe(
            normalize_table_for_streamlit(
                [
                    {
                        "ID": assumption.assumption_id,
                        "Fundstelle": assumption.location or "",
                        "Annahme": assumption.text,
                    }
                    for assumption in zone_spec.assumptions
                ]
            ),
            hide_index=True,
            width="stretch",
        )
    _render_messages(validation_result.messages)


def _saved_zone_assignments() -> dict[str, str]:
    value = st.session_state.get("zone_usage_profile_assignments")
    return value if isinstance(value, dict) else {}


def _render_usage_profile_assignment(spec: ZoneModelSpecification) -> None:
    """Bearbeitet Zuordnungen als Entwurf und uebernimmt sie nur explizit."""
    profile_labels = {profile.profile_id: profile.name for profile in spec.usage_profiles}
    profile_labels.update(dict(SYNTHETIC_USAGE_PROFILE_OPTIONS))
    options = tuple(profile_labels)
    saved_assignments = _saved_zone_assignments()
    for zone in spec.zones:
        draft_key = f"zone_usage_profile_draft_{zone.zone_id}"
        if draft_key not in st.session_state:
            st.session_state[draft_key] = saved_assignments.get(zone.zone_id, zone.usage_profile_id)
        st.selectbox(
            f"{zone.name} ({zone.zone_id})",
            options,
            format_func=lambda profile_id: profile_labels[profile_id],
            key=draft_key,
        )
    st.caption("Demo-Profile sind synthetische Darstellungsoptionen, keine normativen Nutzungsprofile.")
    if st.button("Nutzungsprofile speichern", type="primary", key="zone_usage_profile_save"):
        st.session_state["zone_usage_profile_assignments"] = {
            zone.zone_id: str(st.session_state[f"zone_usage_profile_draft_{zone.zone_id}"]) for zone in spec.zones
        }
        st.success("Nutzungsprofil-Zuordnungen wurden fuer diese Sitzung uebernommen.")


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
