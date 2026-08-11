"""Fachansicht fuer die Referenzdimensionierung."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from time import perf_counter

import pandas as pd
import streamlit as st

from ma_dimensionierung import (
    dimensioning_message_rows,
    dimensioning_step_rows,
    dimensioning_summary_rows,
    run_business_integration_lod1_reference_dimensioning,
)
from ma_dimensionierung.result_contracts import (
    build_manual_ida_legacy_payload,
    validate_manual_ida_editor_rows,
    validate_manual_ida_source_metadata,
)
from ma_parameters import (
    build_business_integration_lod1_baseline_parameter_snapshot,
    build_small_office_5z_v1_baseline_parameter_snapshot,
    reference_dimensioning_parameter_fingerprint,
)
from ma_ui.streamlit_app.pages.variants import (
    VARIANTS_MODULE_KEY,
    active_current_vver_selection,
    pre_dimensioning_source_fingerprint,
)
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.state import (
    clear_workspace_draft,
    get_active_workspace,
    mark_workspace_draft,
    small_office_v1_uses_reference_zone_model,
)
from ma_variants import load_selected_small_office_v1_study
from ma_workflow import get_module_definition
from ma_workspace import load_project_module_config, save_project_module_config
from ma_zones import (
    load_business_integration_lod1_zone_spec,
    load_small_office_5z_endvariant_02_zone_spec,
    zone_specification_to_dict,
)

REFERENCE_DIMENSIONING_MODULE_KEY = "ma_analyse_stage_1_dimensioning"
__all__ = [
    "dimensioning_message_rows",
    "dimensioning_step_rows",
    "dimensioning_summary_rows",
    "manual_reference_load_rows",
    "render",
    "run_business_integration_lod1_reference_dimensioning",
    "validate_manual_reference_load_rows",
]


def manual_reference_load_rows(zone_spec, payload: dict[str, object] | None) -> list[dict[str, object]]:
    """Baut genau die drei vereinbarten Spalten aus dem aktiven Zonenmodell."""
    values_by_zone: dict[str, dict[str, object]] = {}
    if isinstance(payload, dict):
        raw_values = payload.get("zone_loads", [])
        if isinstance(raw_values, list):
            values_by_zone = {
                str(value.get("zone_id")): value
                for value in raw_values
                if isinstance(value, dict)
            }
    return [
        {
            "Zone": zone.name,
            "Heizlast [W]": values_by_zone.get(zone.zone_id, {}).get("heating_load_w"),
            "Kuehllast [W]": values_by_zone.get(zone.zone_id, {}).get("cooling_load_w"),
        }
        for zone in zone_spec.zones
    ]


def validate_manual_reference_load_rows(
    zone_spec,
    editor_value: object,
) -> tuple[list[dict[str, object]], tuple[str, ...]]:
    if not isinstance(editor_value, pd.DataFrame):
        raise ValueError("Lasttabelle konnte nicht ausgewertet werden.")
    return validate_manual_ida_editor_rows(
        tuple((zone.zone_id, zone.name) for zone in zone_spec.zones),
        editor_value.to_dict("records"),
    )


def _active_zone_spec(workspace):
    if workspace.project.identity.title == "Masterarbeit-Analyse":
        return load_small_office_5z_endvariant_02_zone_spec()
    return load_business_integration_lod1_zone_spec()


def render() -> None:
    """Erfasst zonale IDA-Referenzlasten manuell in Watt."""
    module = get_module_definition("ma_analyse.stage_1_dimensioning")
    render_page_header(module.label, module.purpose)

    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.warning("Bitte zuerst ein Projekt auswählen.")
        return
    try:
        zone_spec = _active_zone_spec(workspace)
        zone_payload = load_project_module_config(workspace, "ma_zones") or {}
        parameter_payload = load_project_module_config(workspace, "ma_parameters") or {}
        baseline = _active_baseline(workspace)
        stored_payload = load_project_module_config(workspace, REFERENCE_DIMENSIONING_MODULE_KEY)
        variants_payload = load_project_module_config(workspace, VARIANTS_MODULE_KEY) or {}
    except (OSError, ValueError) as exc:
        st.error(f"Referenzdimensionierung konnte nicht vorbereitet werden: {exc}")
        return

    active_vver_selection = None
    if workspace.project.identity.title == "Masterarbeit-Analyse":
        study = load_selected_small_office_v1_study(variants_payload)
        active_vver_selection = active_current_vver_selection(
            variants_payload,
            study_id=study.study_id,
            current_pre_dimensioning_upstream_fingerprint=pre_dimensioning_source_fingerprint(
                study,
                baseline,
                zone_spec,
                parameter_payload,
            ),
        )
        if active_vver_selection is None:
            st.warning(
                "Die Referenzdimensionierung ist erst nach einer aktuellen, aktiven VVER-Auswahl moeglich."
            )
        else:
            st.caption(
                f"Aktive VVER-Auswahl: {active_vver_selection.record_id} "
                f"({len(active_vver_selection.selected_candidates)} Kandidaten)."
            )
    if (
        workspace.project.identity.title == "Masterarbeit-Analyse"
        and not small_office_v1_uses_reference_zone_model(zone_payload)
    ):
        st.error(
            "Die V1-Referenzdimensionierung ist an das freigegebene 5Z-Modell gebunden. "
            "Das aktuell gewaehlte 29Z-Modell ist noch nicht weitergabefaehig."
        )
        return

    st.caption(
        f"V1-Referenzmodell: {zone_spec.zone_model_id}. "
        "Die Werte werden manuell aus IDA übernommen."
    )
    edited_rows = st.data_editor(
        pd.DataFrame(manual_reference_load_rows(zone_spec, stored_payload)),
        hide_index=True,
        disabled=("Zone",),
        width="stretch",
        key=f"manual_reference_dimensioning_{zone_spec.zone_model_id}",
        on_change=_mark_dimensioning_draft,
    )
    source_metadata = _render_ida_source_metadata(stored_payload)
    try:
        zone_loads, warnings = validate_manual_reference_load_rows(zone_spec, edited_rows)
        validate_manual_ida_source_metadata(source_metadata)
    except ValueError as exc:
        st.error(str(exc))
        can_save = False
    else:
        can_save = True
        for warning in warnings:
            st.warning(warning)
        if not warnings:
            st.success("Alle Zonen enthalten vollständige, nichtnegative Lastwerte.")

    if st.button(
        "Referenzdimensionierung speichern",
        disabled=not can_save or (
            workspace.project.identity.title == "Masterarbeit-Analyse" and active_vver_selection is None
        ),
        key="save_manual_reference_dimensioning",
    ):
        started = perf_counter()
        payload = build_manual_ida_legacy_payload(
            project_id=workspace.project.identity.project_id,
            zone_model_id=zone_spec.zone_model_id,
            zone_model_hash=_content_hash(zone_specification_to_dict(zone_spec)),
            parameter_fingerprint=_content_hash(parameter_payload),
            reference_parameter_fingerprint=reference_dimensioning_parameter_fingerprint(
                baseline,
                parameter_payload,
            ),
            zone_loads=zone_loads,
            source_metadata=source_metadata,
            warnings=warnings,
        )
        if active_vver_selection is not None:
            payload["vver_selection_reference"] = {
                "record_id": active_vver_selection.record_id,
                "record_fingerprint": active_vver_selection.record_fingerprint,
            }
        payload["technical_timing"] = {
            "stage": "reference_dimensioning_save",
            "status": "success",
            "duration_seconds": round(perf_counter() - started, 6),
            "recorded_at": datetime.now(UTC).isoformat(),
            "details": f"{len(zone_loads)} Zonenlasten gespeichert",
        }
        try:
            save_project_module_config(workspace, REFERENCE_DIMENSIONING_MODULE_KEY, payload)
        except (OSError, ValueError) as exc:
            st.error(f"Referenzdimensionierung konnte nicht gespeichert werden: {exc}")
        else:
            st.session_state["ma_ui_variants_update_required"] = True
            clear_workspace_draft(
                st.session_state,
                REFERENCE_DIMENSIONING_MODULE_KEY,
            )
            st.success("Referenzdimensionierung wurde projektbezogen gespeichert.")


def _mark_dimensioning_draft() -> None:
    mark_workspace_draft(st.session_state, REFERENCE_DIMENSIONING_MODULE_KEY)


def _active_baseline(workspace):
    if workspace.project.identity.title == "Masterarbeit-Analyse":
        return build_small_office_5z_v1_baseline_parameter_snapshot()
    return build_business_integration_lod1_baseline_parameter_snapshot()


def _render_ida_source_metadata(payload: dict[str, object] | None) -> dict[str, str]:
    stored = payload.get("ida_source", {}) if isinstance(payload, dict) else {}
    stored = stored if isinstance(stored, dict) else {}
    with st.expander("IDA-Quellmetadaten", expanded=True):
        st.caption(
            "Die Lasttabelle bleibt bei den drei vereinbarten Spalten. "
            "Diese Metadaten sichern die wissenschaftliche Reproduzierbarkeit."
        )
        ida_version = st.text_input(
            "IDA-ICE-Version",
            value=str(stored.get("ida_version", "")),
            key="dimensioning_ida_version",
            on_change=_mark_dimensioning_draft,
        )
        model_id = st.text_input(
            "IDA-Modell-ID/Revision",
            value=str(stored.get("model_id", "")),
            key="dimensioning_ida_model_id",
            on_change=_mark_dimensioning_draft,
        )
        run_id = st.text_input(
            "IDA-Run-ID",
            value=str(stored.get("run_id", "")),
            key="dimensioning_ida_run_id",
            on_change=_mark_dimensioning_draft,
        )
        source_file_name = st.text_input(
            "IDA-Quelldateiname",
            value=str(stored.get("source_file_name", "")),
            key="dimensioning_ida_source_file",
            on_change=_mark_dimensioning_draft,
        )
        source_file_sha256 = st.text_input(
            "SHA-256 der IDA-Quelldatei",
            value=str(stored.get("source_file_sha256", "")),
            key="dimensioning_ida_source_sha256",
            on_change=_mark_dimensioning_draft,
        )
        cooling_load_definition = st.selectbox(
            "Kuehllastdefinition",
            ("", "sensible_zone_load", "latent_zone_load", "total_zone_load"),
            index=(
                ("", "sensible_zone_load", "latent_zone_load", "total_zone_load").index(
                    str(stored.get("cooling_load_definition", ""))
                )
                if str(stored.get("cooling_load_definition", ""))
                in {"", "sensible_zone_load", "latent_zone_load", "total_zone_load"}
                else 0
            ),
            key="dimensioning_cooling_definition",
            on_change=_mark_dimensioning_draft,
        )
        maximum_definition = st.selectbox(
            "Maximums-/Aggregationsdefinition",
            (
                "",
                "individual_zone_maximum",
                "zone_values_at_simultaneous_system_maximum",
            ),
            index=(
                (
                    "",
                    "individual_zone_maximum",
                    "zone_values_at_simultaneous_system_maximum",
                ).index(
                    str(stored.get("maximum_definition", ""))
                )
                if str(stored.get("maximum_definition", ""))
                in {
                    "",
                    "individual_zone_maximum",
                    "zone_values_at_simultaneous_system_maximum",
                }
                else 0
            ),
            key="dimensioning_maximum_definition",
            on_change=_mark_dimensioning_draft,
        )
        design_conditions = st.text_input(
            "Auslegungsbedingungen/ausgewerteter Zeitraum",
            value=str(stored.get("design_conditions", "")),
            key="dimensioning_design_conditions",
            on_change=_mark_dimensioning_draft,
        )
        responsible = st.text_input(
            "Eingabeverantwortlich",
            value=str(stored.get("responsible", "")),
            key="dimensioning_responsible",
            on_change=_mark_dimensioning_draft,
        )
        review_status = st.selectbox(
            "Pruefstatus",
            ("unreviewed", "reviewed"),
            index=1 if stored.get("review_status") == "reviewed" else 0,
            key="dimensioning_review_status",
            on_change=_mark_dimensioning_draft,
        )
        reviewer = st.text_input(
            "Geprueft durch",
            value=str(stored.get("reviewer", "")),
            key="dimensioning_reviewer",
            on_change=_mark_dimensioning_draft,
        )
        reviewed_at = st.text_input(
            "Pruefdatum (ISO 8601)",
            value=str(stored.get("reviewed_at", "")),
            key="dimensioning_reviewed_at",
            on_change=_mark_dimensioning_draft,
        )
        review_note = st.text_input(
            "Pruefhinweis",
            value=str(stored.get("review_note", "")),
            key="dimensioning_review_note",
            on_change=_mark_dimensioning_draft,
        )
    return {
        "ida_version": ida_version.strip(),
        "model_id": model_id.strip(),
        "run_id": run_id.strip(),
        "source_file_name": source_file_name.strip(),
        "source_file_sha256": source_file_sha256.strip().lower(),
        "heating_load_definition": "zone_heating_load",
        "cooling_load_definition": cooling_load_definition,
        "maximum_definition": maximum_definition,
        "design_conditions": design_conditions.strip(),
        "responsible": responsible.strip(),
        "review_status": review_status,
        "reviewer": reviewer.strip(),
        "reviewed_at": reviewed_at.strip(),
        "review_note": review_note.strip(),
        "source_classification": "externally_simulated_result",
    }


def _content_hash(payload: object) -> str:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
