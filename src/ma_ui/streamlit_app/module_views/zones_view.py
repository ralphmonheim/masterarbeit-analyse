"""Fachansicht fuer thermische Zonen."""

from __future__ import annotations

from collections.abc import Sequence

import streamlit as st

from ma_building import (
    load_business_integration_lod1_building_spec,
    load_small_office_5z_endvariant_02_building_spec,
)
from ma_parameters import DIN_USAGE_PROFILE_METADATA, suggest_usage_profile_id
from ma_ui.streamlit_app.module_views.technical_release_support import (
    StaleActiveTechnicalRevisionError,
    load_active_technical_revision,
    resolve_selected_building_context,
)
from ma_ui.streamlit_app.module_views.zones_assignment_support import (
    bind_zone_specification_to_project,
    stored_technical_assignment_draft,
    technical_assignment_check_token,
    technical_assignment_editor_rows,
    technical_assignment_project_payload,
    technical_assignments_from_rows,
    technical_handover_rows,
    validate_technical_assignment_draft,
    zone_model_draft_project_payload,
    zone_specification_content_hash,
)
from ma_ui.streamlit_app.module_views.zones_release_preview_support import (
    build_zone_release_preview,
)
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_ui.streamlit_app.state import (
    clear_workspace_draft,
    get_active_workspace,
    mark_workspace_draft,
)
from ma_validation import DiagnosticMessage, DiagnosticSeverity, ReleaseStatus
from ma_workflow import get_module_definition
from ma_workspace import load_project_module_config, save_project_module_config
from ma_zones import (
    ZoneModelSpecification,
    build_small_office_29z_draft,
    load_business_integration_lod1_zone_spec,
    load_small_office_5z_endvariant_02_zone_spec,
    validate_zone_spec,
)

ZONE_WORKSPACE_TAB_LABELS = (
    "Übersicht",
    "Zone zuweisen",
    "Nutzung & interne Lasten",
    "Zeitpläne",
    "Konditionierung & Übergabe",
    "Zusammenfassung & Prüfung",
)
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


def usage_profile_assignment_rows(
    spec: ZoneModelSpecification,
    assignments: dict[str, str],
) -> list[dict[str, object]]:
    """Bereitet die schlanke, bearbeitbare Profilzuordnung je Zone vor."""
    profiles = {profile.profile_id: profile for profile in spec.usage_profiles}
    rows: list[dict[str, object]] = []
    for zone in spec.zones:
        profile = profiles.get(zone.usage_profile_id)
        rows.append(
            {
                "Zone": zone.zone_id,
                "Name": zone.name,
                "Raeume": ", ".join(zone.source_space_ids) or "-",
                "Aktuelles Profil": zone.usage_profile_id,
                "Betrieb [h]": _operation_hours(profile),
                "Tage/Woche": profile.operation_days_per_week if profile else "-",
                "Belegung [m2/P]": profile.occupancy_density_m2_per_person if profile else "-",
                "Beleuchtung [W/m2]": profile.lighting_power_w_m2 if profile else "-",
                "Geraete [W/m2]": profile.equipment_power_w_m2 if profile else "-",
                "Neues Profil": assignments.get(zone.zone_id, zone.usage_profile_id),
            }
        )
    return rows


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


def room_assignment_rows(building_spec, zone_spec: ZoneModelSpecification) -> list[dict[str, object]]:
    """Zeigt vollstaendige Raum-Zonen-Zuordnungen des freigegebenen Stands."""
    zone_by_space_id = {
        space_id: zone
        for zone in zone_spec.zones
        for space_id in zone.source_space_ids
    }
    return [
        {
            "Raum": space.space_id,
            "Name": space.name,
            "Flaeche [m2]": space.floor_area_m2,
            "Volumen [m3]": space.volume_m3,
            "Aktuelle Zone": zone_by_space_id[space.space_id].name if space.space_id in zone_by_space_id else "-",
            "Zonen-ID": zone_by_space_id[space.space_id].zone_id if space.space_id in zone_by_space_id else "-",
            "Status": "zugewiesen" if space.space_id in zone_by_space_id else "nicht zugeordnet",
        }
        for space in building_spec.spaces
    ]


def render() -> None:
    """Zeigt 5Z als Referenz und 29Z als getrennten, bearbeitbaren Entwurf."""
    module = get_module_definition("ma_zones")
    render_page_header(module.label, module.purpose)
    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.warning("Bitte zuerst ein Projekt auswaehlen.")
        return
    try:
        project_payload = load_project_module_config(workspace, "ma_zones") or {}
        if workspace.project.identity.title == "Masterarbeit-Analyse":
            building_spec = load_small_office_5z_endvariant_02_building_spec()
            model_key = st.selectbox(
                "Thermisches Modell",
                ("5Z", "29Z"),
                index=0,
                key="ma_zones_thermal_model",
                on_change=_mark_zones_draft,
                help="5Z bleibt der aktive Referenz- und Optimierungsstand. 29Z ist ein alternativer Entwurf.",
            )
            zone_spec = (
                load_small_office_5z_endvariant_02_zone_spec()
                if model_key == "5Z"
                else build_small_office_29z_draft()
            )
        else:
            building_spec = load_business_integration_lod1_building_spec()
            model_key = "1Z"
            zone_spec = load_business_integration_lod1_zone_spec()
    except (OSError, ValueError) as exc:
        st.error(f"Zonenspezifikation konnte nicht geladen werden: {exc}")
        return

    section = st.segmented_control(
        "Zonenbereich",
        ZONE_WORKSPACE_TAB_LABELS,
        default=ZONE_WORKSPACE_TAB_LABELS[0],
        key="ma_zones_workspace_section",
        selection_mode="single",
    )
    section = section or ZONE_WORKSPACE_TAB_LABELS[0]
    if model_key == "29Z":
        _render_29z_status(project_payload, zone_spec)
    else:
        if "zone_usage_profile_assignments" not in st.session_state:
            st.session_state["zone_usage_profile_assignments"] = _stored_5z_assignments(
                project_payload
            )
        validation_result = validate_zone_spec(zone_spec, building_spec=building_spec)
        st.metric("Freigabestatus", validation_result.release_status.value)

    if st.button("Thermisches Modell in Projekt uebernehmen", key="ma_zones_apply_model"):
        updated_payload = dict(project_payload)
        updated_payload.update(
            {
                "schema_version": "1.0",
                "project_id": workspace.project.identity.project_id,
                "active_model": model_key,
                "zone_model_id": zone_spec.zone_model_id,
                "downstream_status": "current" if model_key != "29Z" else "blocked_incomplete",
            }
        )
        save_project_module_config(workspace, "ma_zones", updated_payload)
        clear_workspace_draft(st.session_state, "ma_zones")
        st.session_state["ma_ui_variants_update_required"] = True
        st.success("Der thermische Modellstand wurde projektbezogen gespeichert.")

    if section == "Übersicht":
        if model_key == "29Z":
            st.metric("Freigabestatus", "Entwurf / gesperrt")
        else:
            st.metric("Freigabestatus", validation_result.release_status.value)
        st.dataframe(normalize_table_for_streamlit(zone_summary_rows(zone_spec)), hide_index=True, width="stretch")
        st.dataframe(
            normalize_table_for_streamlit(zone_overview_rows(zone_spec, _saved_zone_assignments())),
            hide_index=True,
            width="stretch",
        )
    elif section == "Zone zuweisen":
        st.caption(
            "Die Zonenzuordnung erfolgt ausschliesslich hier. 29Z bildet jeden Raum genau "
            "einmal als thermische Zone ab."
        )
        st.dataframe(
            normalize_table_for_streamlit(room_assignment_rows(building_spec, zone_spec)),
            hide_index=True,
            width="stretch",
        )
    elif section == "Nutzung & interne Lasten":
        if model_key == "29Z":
            _render_29z_profile_assignment(workspace, project_payload, zone_spec)
        else:
            _render_usage_profile_assignment(workspace, project_payload, zone_spec)
    elif section == "Konditionierung & Übergabe":
        st.dataframe(normalize_table_for_streamlit(thermal_zone_rows(zone_spec)), hide_index=True, width="stretch")
        _render_technical_assignment(
            workspace,
            project_payload,
            model_key=model_key,
            zone_spec=zone_spec,
        )
    elif section == "Zeitpläne":
        st.caption("Die Profile sind LoD-1-Annahmen. Wochen-, Jahres- und Feiertagsprofile folgen getrennt.")
        st.dataframe(normalize_table_for_streamlit(usage_profile_rows(zone_spec)), hide_index=True, width="stretch")
    else:
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
        if model_key == "29Z":
            st.warning(
                "Der 29Z-Entwurf bleibt bis zu einer vollstaendigen, rechtlich freigegebenen "
                "Profilwertquelle fuer die Weitergabe gesperrt."
            )
        else:
            _render_messages(validation_result.messages)
        _render_zone_release_preview(
            workspace,
            project_payload,
            model_key=model_key,
            zone_spec=zone_spec,
        )


def _render_29z_status(payload: dict[str, object], spec: ZoneModelSpecification) -> None:
    model_drafts = payload.get("model_drafts", {})
    draft = model_drafts.get("29Z", {}) if isinstance(model_drafts, dict) else {}
    assignments = draft.get("assignments", []) if isinstance(draft, dict) else []
    assigned_count = sum(
        bool(row.get("profile_id")) and bool(row.get("confirmed"))
        for row in assignments
        if isinstance(row, dict)
    )
    st.metric("Thermische Zonen", len(spec.zones))
    st.metric("Manuell bestaetigte Profile", f"{assigned_count}/{len(spec.zones)}")
    st.warning(
        "29Z ist auswaehlbar und bearbeitbar, aber nicht der V1-Referenzlauf. "
        "Profilwerte werden nicht aus dem 5Z-Modell geerbt."
    )


def _render_29z_profile_assignment(
    workspace,
    payload: dict[str, object],
    spec: ZoneModelSpecification,
) -> None:
    profile_labels = {
        profile.profile_id: f"{profile.table_reference} {profile.name}"
        for profile in DIN_USAGE_PROFILE_METADATA
    }
    model_drafts = payload.get("model_drafts", {})
    draft = model_drafts.get("29Z", {}) if isinstance(model_drafts, dict) else {}
    stored_rows = draft.get("assignments", []) if isinstance(draft, dict) else []
    stored_by_zone = {
        str(row.get("zone_id")): row
        for row in stored_rows
        if isinstance(row, dict)
    }
    rows = []
    for zone in spec.zones:
        suggestion = suggest_usage_profile_id(zone.name)
        stored = stored_by_zone.get(zone.zone_id, {})
        rows.append(
            {
                "Zone-ID": zone.zone_id,
                "Langer IFC-Raumname": zone.name,
                "IFC-Raum-ID": zone.source_space_ids[0],
                "Vorschlag": suggestion or "",
                "Nutzungsprofil": stored.get("profile_id", suggestion or ""),
                "Begruendung": stored.get("reason", ""),
                "Manuell bestaetigt": bool(stored.get("confirmed", False)),
                "Status": (
                    "bestaetigt"
                    if stored.get("confirmed")
                    else ("Vorauswahl" if suggestion else "manuell bestimmen")
                ),
            }
        )
    edited = st.data_editor(
        normalize_table_for_streamlit(rows),
        hide_index=True,
        width="stretch",
        disabled=("Zone-ID", "Langer IFC-Raumname", "IFC-Raum-ID", "Vorschlag", "Status"),
        column_config={
            "Nutzungsprofil": st.column_config.SelectboxColumn(
                "Nutzungsprofil",
                options=("", *profile_labels),
                format_func=lambda profile_id: profile_labels.get(profile_id, "Bitte waehlen"),
            )
        },
        key="ma_zones_29z_profile_editor",
        on_change=_mark_zones_draft,
    )
    st.caption(
        "Die Vorschlaege stammen nur aus IFC-Namensregeln. Ungenaue oder fehlende "
        "Treffer werden manuell bestimmt; die Begruendung kann spaeter als Lernbasis dienen."
    )
    if st.button("29Z-Zuordnungsentwurf speichern", key="ma_zones_save_29z_assignments"):
        assignments = [
            {
                "zone_id": str(row["Zone-ID"]),
                "ifc_room_name": str(row["Langer IFC-Raumname"]),
                "profile_id": str(row["Nutzungsprofil"]),
                "reason": str(row["Begruendung"]),
                "confirmed": bool(row["Manuell bestaetigt"]),
            }
            for row in edited.to_dict("records")
        ]
        complete = all(
            row["profile_id"] and row["confirmed"] for row in assignments
        )
        try:
            updated_payload = zone_model_draft_project_payload(
                payload,
                project_id=workspace.project.identity.project_id,
                model_key="29Z",
                draft_updates={
                    "zone_model_id": spec.zone_model_id,
                    "assignments": assignments,
                    "assignment_status": "complete" if complete else "manual_review_required",
                    "profile_values_status": "rights_clearance_required",
                    "handover_status": "blocked_profile_values",
                },
            )
            save_project_module_config(workspace, "ma_zones", updated_payload)
        except (OSError, TypeError, ValueError) as exc:
            st.error(f"29Z-Zuordnungsentwurf konnte nicht gespeichert werden: {exc}")
            return
        clear_workspace_draft(st.session_state, "ma_zones")
        if complete:
            st.success("Alle 29 Profilzuordnungen sind gespeichert und manuell bestaetigt.")
        else:
            st.warning("Der Entwurf ist gespeichert; unvollstaendige Zuordnungen bleiben gesperrt.")


def _saved_zone_assignments() -> dict[str, str]:
    value = st.session_state.get("zone_usage_profile_assignments")
    return value if isinstance(value, dict) else {}


def _stored_5z_assignments(payload: dict[str, object]) -> dict[str, str]:
    drafts = payload.get("model_drafts", {})
    draft = drafts.get("5Z", {}) if isinstance(drafts, dict) else {}
    assignments = draft.get("profile_assignments", {}) if isinstance(draft, dict) else {}
    return (
        {str(zone_id): str(profile_id) for zone_id, profile_id in assignments.items()}
        if isinstance(assignments, dict)
        else {}
    )


def _mark_zones_draft() -> None:
    st.session_state.pop("ma_zones_checked_technical_assignment", None)
    mark_workspace_draft(st.session_state, "ma_zones")


def _render_zone_release_preview(
    workspace,
    payload: dict[str, object],
    *,
    model_key: str,
    zone_spec: ZoneModelSpecification,
) -> None:
    """Zeigt die vollstaendige P013-Pruefkette, ohne einen Stand zu speichern."""
    st.markdown("### Freigabebereitschaft und Handover-Vorschau")
    st.caption(
        "Die Vorschau verbindet den uebernommenen Building-Stand, die versionierte Zonenquelle, "
        "den gespeicherten P013-Projektentwurf und den aktiven P014-Handover. Sie schreibt weder "
        "eine Zonenrevision noch einen aktiven Handover."
    )
    if not st.button(
        "Freigabebereitschaft und Handover-Vorschau prüfen",
        key=f"ma_zones_release_preview_{model_key}",
    ):
        return
    try:
        building_context = resolve_selected_building_context(workspace)
        active_technical = load_active_technical_revision(
            workspace,
            building_context.reference,
        )
        if active_technical is None:
            st.warning(
                "Fuer den uebernommenen Building-Stand ist kein aktiver P014-Handover vorhanden."
            )
            return
        revision, handover, _revision_path = active_technical
        preview = build_zone_release_preview(
            payload,
            project_id=workspace.project.identity.project_id,
            model_key=model_key,
            building_specification=building_context.specification,
            building_reference=building_context.reference,
            source_zone_specification=zone_spec,
            technical_revision=revision,
            technical_handover=handover,
        )
    except StaleActiveTechnicalRevisionError:
        st.error(
            "Die aktive Technikrevision gehoert zu einer frueheren Building-Version. "
            "Bitte den Technikstand in Technische Systeme neu freigeben."
        )
        return
    except (OSError, TypeError, ValueError) as exc:
        st.error(f"Handover-Vorschau ist gesperrt: {exc}")
        return

    _render_messages(preview.validation_result.messages)
    if preview.zone_handover is None:
        st.warning(
            "Der materialisierte Projektstand ist noch nicht freigabebereit. "
            "Es wurde kein Handover-Vorschauobjekt erzeugt."
        )
        return
    handover = preview.zone_handover
    st.success("Der aktuelle Projektentwurf ist strukturell freigabebereit.")
    st.markdown(
        f"**Status:** nur im Speicher, nicht persistiert und nicht aktiv  "
        f"\n**ThermalBuildingModel:** `{preview.thermal_building_model.thermal_building_model_id}`  "
        f"\n**Handover-ID:** `{handover.zone_handover_id}`  "
        f"\n**Handover-Revision:** `{handover.revision_id}`  "
        f"\n**Handover-Content-Hash:** `{handover.content_hash}`  "
        f"\n**Projekt / Building / Zone:** `{handover.project_id}` / `{handover.building_id}` / "
        f"`{handover.zone_model_id}`  "
        f"\n**Building-Revision:** `{handover.building_revision_id}`  "
        f"\n**P014-Referenz:** `{handover.technical_model_id}` / `{handover.technical_revision_id}` / "
        f"`{handover.technical_content_hash}`  "
        f"\n**P014-Handover-Hash:** `{handover.technical_handover_content_hash or 'ohne Zuordnungsbindung'}`"
    )
    st.info(
        "Die Vorschau bestaetigt nur die fachliche Integritaet der aktuellen Ableitung. "
        "Sie weist weder vollstaendige Versorgung noch technische Eignung, Lastdeckung, "
        "Dimensionierung, Simulation oder eine persistierte P018-Freigabe nach."
    )


def _render_technical_assignment(
    workspace,
    payload: dict[str, object],
    *,
    model_key: str,
    zone_spec: ZoneModelSpecification,
) -> None:
    """Bearbeitet die P013-eigene Zuordnung zum aktiven P014-Handover."""
    st.caption(
        "Hier werden Zonen manuell freigegebenen technischen Serviceinterfaces zugeordnet. "
        "Es werden weder Lasten berechnet noch Systeme oder Dimensionen veraendert."
    )
    try:
        building_context = resolve_selected_building_context(workspace)
        project_zone_spec = bind_zone_specification_to_project(
            zone_spec,
            project_id=workspace.project.identity.project_id,
            building_reference=building_context.reference,
        )
        active_technical = load_active_technical_revision(
            workspace,
            building_context.reference,
        )
    except StaleActiveTechnicalRevisionError:
        st.error(
            "Die aktive Technikrevision gehoert zu einer frueheren Building-Version. "
            "Bitte den Technikstand in Technische Systeme neu freigeben."
        )
        return
    except (OSError, TypeError, ValueError) as exc:
        st.error(f"Technische Zuordnung ist gesperrt: {exc}")
        return
    if active_technical is None:
        st.warning(
            "Fuer den uebernommenen Building-Stand ist noch kein aktiver P014-Handover vorhanden. "
            "Bitte zuerst Technische Systeme freigeben."
        )
        return
    _revision, handover, _revision_path = active_technical
    st.markdown(
        f"**Aktiver Technikstand:** `{handover.technical_model_id}` / `{handover.revision_id}`  "
        f"\n**Building-Revision:** `{building_context.reference.revision_id}`  "
        f"\n**Technik-Content-Hash:** `{handover.content_hash}`  "
        f"\n**Handover-Hash:** `{handover.handover_content_hash}`  "
        f"\n**Freigabenachweis-Hash:** `{handover.release_evidence_hash or 'nicht vorhanden'}`  "
        f"\n**Zoneninhalt-Hash:** `{zone_specification_content_hash(project_zone_spec)}`"
    )
    interface_rows = technical_handover_rows(handover)
    if not interface_rows:
        st.warning("Der aktive Technikstand enthaelt keine zuordenbaren Serviceinterfaces.")
        return
    st.dataframe(
        normalize_table_for_streamlit(interface_rows),
        hide_index=True,
        width="stretch",
    )

    try:
        stored = stored_technical_assignment_draft(
            payload,
            model_key=model_key,
            zone_spec=project_zone_spec,
            handover=handover,
        )
    except ValueError as exc:
        st.error(f"Gespeicherter Zuordnungsentwurf ist ungueltig: {exc}")
        return
    if stored.has_stored_draft and not stored.matches_active_handover:
        st.warning(
            "Der gespeicherte Zuordnungsentwurf referenziert einen anderen Zonen- oder "
            "Technikstand und wird nicht vorausgewaehlt."
        )
    edited_rows = st.data_editor(
        normalize_table_for_streamlit(
            technical_assignment_editor_rows(
                project_zone_spec,
                handover,
                stored.assignments,
            )
        ),
        hide_index=True,
        width="stretch",
        disabled=("Zone-ID", "Zone", "Serviceinterface", "Dienst", "Medium"),
        key=(
            f"ma_zones_technical_assignment_editor_{model_key}_"
            f"{handover.revision_id}_{handover.content_hash[:8]}"
        ),
        on_change=_mark_zones_draft,
    )
    st.caption(
        "Nicht markierte Zeilen bleiben unzugeordnet. Ein Terminaltyp ist optional; wenn er "
        "angegeben wird, muss er im aktiven Serviceinterface als kompatibel freigegeben sein."
    )
    st.info(
        "Die Prüfung bestätigt nur die Integrität der gewählten Beziehungen. Sie ist kein "
        "Nachweis vollständiger Versorgung, technischer Eignung, Lastdeckung oder Dimensionierung."
    )
    try:
        assignments = technical_assignments_from_rows(
            project_zone_spec,
            handover,
            edited_rows,
        )
        _draft_spec, validation = validate_technical_assignment_draft(
            project_zone_spec,
            handover,
            assignments,
        )
        check_token = technical_assignment_check_token(
            project_zone_spec,
            handover,
            assignments,
        )
    except (TypeError, ValueError) as exc:
        st.error(f"Zuordnungsentwurf ist ungueltig: {exc}")
        return

    if st.button("Technische Zuordnungen prüfen", key=f"ma_zones_check_technical_{model_key}"):
        _render_messages(validation.messages)
        if validation.release_status is ReleaseStatus.RELEASED:
            st.session_state["ma_zones_checked_technical_assignment"] = check_token
            st.success(
                "Der Entwurf ist gegen den aktiven Zonen- und P014-Handover-Stand geprueft. "
                "Vollstaendigkeit oder Versorgung sind damit nicht nachgewiesen."
            )
        else:
            st.session_state.pop("ma_zones_checked_technical_assignment", None)

    if st.button(
        "Geprüfte technische Zuordnungen übernehmen",
        type="primary",
        key=f"ma_zones_save_technical_{model_key}",
    ):
        if st.session_state.get("ma_zones_checked_technical_assignment") != check_token:
            st.warning("Bitte den unveraenderten Zuordnungsentwurf zuerst erfolgreich pruefen.")
            return
        try:
            updated_payload = technical_assignment_project_payload(
                payload,
                project_id=workspace.project.identity.project_id,
                model_key=model_key,
                zone_spec=project_zone_spec,
                handover=handover,
                assignments=assignments,
            )
            save_project_module_config(workspace, "ma_zones", updated_payload)
        except (OSError, TypeError, ValueError) as exc:
            st.error(f"Technische Zuordnungen konnten nicht gespeichert werden: {exc}")
            return
        clear_workspace_draft(st.session_state, "ma_zones")
        st.session_state.pop("ma_zones_checked_technical_assignment", None)
        st.session_state["ma_ui_variants_update_required"] = True
        st.success(
            "Die geprueften technischen Zuordnungen wurden als projektbezogener P013-Entwurf gespeichert. "
            "Ein ReleasedZoneHandover und ein Versorgungs- oder Dimensionierungsnachweis wurden nicht erzeugt."
        )


def _render_usage_profile_assignment(
    workspace,
    payload: dict[str, object],
    spec: ZoneModelSpecification,
) -> None:
    """Bearbeitet Zuordnungen als Entwurf und uebernimmt sie nur explizit."""
    profile_labels = {profile.profile_id: profile.name for profile in spec.usage_profiles}
    profile_labels.update(dict(SYNTHETIC_USAGE_PROFILE_OPTIONS))
    profile_ids = tuple(profile_labels)
    st.caption("Die Zuordnung bleibt ein Sitzungsentwurf und aendert keinen freigegebenen Zonenstand.")
    edited_rows = st.data_editor(
        normalize_table_for_streamlit(usage_profile_assignment_rows(spec, _saved_zone_assignments())),
        hide_index=True,
        width="stretch",
        disabled=(
            "Zone",
            "Name",
            "Raeume",
            "Aktuelles Profil",
            "Betrieb [h]",
            "Tage/Woche",
            "Belegung [m2/P]",
            "Beleuchtung [W/m2]",
            "Geraete [W/m2]",
        ),
        column_config={
            "Neues Profil": st.column_config.SelectboxColumn(
                "Neues Profil",
                options=profile_ids,
                format_func=lambda profile_id: profile_labels[profile_id],
                required=True,
            )
        },
        key="zone_usage_profile_assignment_editor",
        on_change=_mark_zones_draft,
    )
    st.caption("Demo-Profile sind synthetische Darstellungsoptionen, keine normativen Nutzungsprofile.")
    if st.button("Entwurf in dieser Sitzung uebernehmen", type="primary", key="zone_usage_profile_save"):
        assignments = _profile_assignments_from_rows(
            spec, edited_rows, profile_ids
        )
        st.session_state["zone_usage_profile_assignments"] = assignments
        try:
            updated_payload = zone_model_draft_project_payload(
                payload,
                project_id=workspace.project.identity.project_id,
                model_key="5Z",
                draft_updates={
                    "zone_model_id": spec.zone_model_id,
                    "profile_assignments": assignments,
                    "assignment_status": "complete",
                },
            )
            save_project_module_config(workspace, "ma_zones", updated_payload)
        except (OSError, TypeError, ValueError) as exc:
            st.error(f"Nutzungsprofil-Zuordnungen konnten nicht gespeichert werden: {exc}")
            return
        clear_workspace_draft(st.session_state, "ma_zones")
        st.success("Nutzungsprofil-Zuordnungen wurden projektbezogen uebernommen.")


def _profile_assignments_from_rows(
    spec: ZoneModelSpecification,
    edited_rows,
    allowed_profile_ids: tuple[str, ...],
) -> dict[str, str]:
    """Liest nur gueltige Profilzuordnungen aus der UI-Tabelle."""
    rows_by_zone = {
        str(row["Zone"]): str(row["Neues Profil"])
        for row in edited_rows.to_dict("records")
        if "Zone" in row and "Neues Profil" in row
    }
    assignments: dict[str, str] = {}
    for zone in spec.zones:
        profile_id = rows_by_zone.get(zone.zone_id, zone.usage_profile_id)
        if profile_id not in allowed_profile_ids:
            raise ValueError(f"Unbekanntes Nutzungsprofil fuer {zone.zone_id}: {profile_id}")
        assignments[zone.zone_id] = profile_id
    return assignments


def _operation_hours(profile) -> str:
    """Formatiert Betriebsstunden fuer die Zuweisungstabelle."""
    if profile is None:
        return "-"
    return f"{profile.operation_start_hour:g}-{profile.operation_end_hour:g}"


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
