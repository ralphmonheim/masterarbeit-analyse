"""Projektbezogene V1-Variantenbildung in drei klaren Arbeitsschritten."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

import streamlit as st

from ma_analyse.stage_1_dimensioning import default_output_requirements
from ma_parameters import (
    build_small_office_5z_v1_baseline_parameter_snapshot,
    reference_dimensioning_parameter_fingerprint,
)
from ma_project import load_variant_naming_profile
from ma_ui.streamlit_app.shared import normalize_table_for_streamlit
from ma_ui.streamlit_app.state import (
    get_active_workspace,
    small_office_v1_uses_reference_zone_model,
)
from ma_variants import (
    build_small_office_candidate_rows,
    candidate_simulation_setup,
    candidate_source_is_current,
    load_small_office_v1_study,
    materialize_zonal_capacities,
    select_candidate_ids,
    small_office_source_fingerprint,
    small_office_study_case_rows,
    source_fingerprint,
    variation_specification_is_current,
    verify_candidate_rows,
)
from ma_workspace import load_project_module_config, save_project_module_config
from ma_zones import (
    load_small_office_5z_endvariant_02_zone_spec,
    zone_specification_to_dict,
)

VARIANTS_MODULE_KEY = "ma_variants"
VARIANT_STEP_LABELS = (
    "Variationsraum",
    "Pruefung und Katalog",
    "Auswahl und Variantenpakete",
)


def render() -> None:
    st.title("Varianten")
    st.caption(
        "Optimierung und Sensitivitaet werden gleichzeitig als getrennte StudyDirections "
        "angelegt. Kandidaten, Katalog und Pakete entstehen erst ueber die drei Aktionen."
    )
    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.warning("Bitte zuerst ein Projekt auswaehlen.")
        return
    if workspace.project.identity.title != "Masterarbeit-Analyse":
        st.info("Fuer dieses Demo-Projekt ist noch keine V1-Studienkonfiguration hinterlegt.")
        return
    try:
        study = load_small_office_v1_study()
        baseline = build_small_office_5z_v1_baseline_parameter_snapshot()
        zone_spec = load_small_office_5z_endvariant_02_zone_spec()
        parameter_payload = load_project_module_config(workspace, "ma_parameters") or {}
        dimensioning_payload = (
            load_project_module_config(workspace, "ma_analyse_stage_1_dimensioning") or {}
        )
        payload = load_project_module_config(workspace, VARIANTS_MODULE_KEY) or {}
    except (OSError, ValueError, KeyError) as exc:
        st.error(f"Variantenstand konnte nicht vorbereitet werden: {exc}")
        return

    zone_payload = load_project_module_config(workspace, "ma_zones") or {}
    if not small_office_v1_uses_reference_zone_model(zone_payload):
        st.error(
            "Varianten V1 sind an das freigegebene 5Z-Referenzmodell gebunden. "
            "Das gewaehlte 29Z-Modell ist noch nicht weitergabefaehig."
        )
        return
    current_fingerprint = small_office_source_fingerprint(
        study,
        baseline,
        zone_spec,
        parameter_payload,
        dimensioning_payload,
    )
    stored_fingerprint = payload.get("source_fingerprint")
    if stored_fingerprint and stored_fingerprint != current_fingerprint:
        st.warning(
            "Regeln, Spannen oder Referenzdimensionierung wurden geaendert. "
            "Kataloge und Pakete bleiben erhalten, muessen aber aktualisiert werden."
        )
        st.session_state["ma_ui_variants_update_required"] = True

    study_cases = small_office_study_case_rows(study)
    active_case = st.selectbox(
        "Aktiver StudyCase",
        [row["study_case_id"] for row in study_cases],
        format_func=lambda case_id: next(
            str(row["label"]) for row in study_cases if row["study_case_id"] == case_id
        ),
        key="ma_variants_active_study_case",
    )
    active_direction = next(
        str(row["study_direction"])
        for row in study_cases
        if row["study_case_id"] == active_case
    )
    _render_effective_rules(parameter_payload, active_direction, active_case)

    step = st.segmented_control(
        "Arbeitsschritt",
        VARIANT_STEP_LABELS,
        default=VARIANT_STEP_LABELS[0],
        key="ma_variants_step",
        selection_mode="single",
    )
    step = step or VARIANT_STEP_LABELS[0]
    if step == "Variationsraum":
        _render_candidate_generation(
            workspace,
            study,
            study_cases,
            parameter_payload,
            baseline,
            dimensioning_payload,
            zone_spec,
            payload,
            current_fingerprint,
            active_case,
        )
    elif step == "Pruefung und Katalog":
        _render_catalog_generation(
            workspace,
            zone_spec,
            baseline,
            parameter_payload,
            dimensioning_payload,
            payload,
            current_fingerprint,
            active_case,
        )
    else:
        _render_selection_and_packages(
            workspace,
            study,
            baseline,
            zone_spec,
            parameter_payload,
            dimensioning_payload,
            payload,
            active_case,
            current_fingerprint,
        )


def _render_effective_rules(
    parameter_payload: dict[str, object],
    direction: str,
    case_id: str,
) -> None:
    rules = parameter_payload.get("rules", [])
    effective_rules = []
    if isinstance(rules, list):
        for rule in rules:
            if not isinstance(rule, dict) or not rule.get("defining"):
                continue
            scope_type = rule.get("scope_type")
            scope_id = rule.get("scope_id")
            if (
                scope_type == "project"
                or (scope_type == "study_direction" and scope_id == direction)
                or (scope_type == "study_case" and scope_id == case_id)
            ):
                effective_rules.append(rule)
    with st.expander("Wirksame Regeln/Vorgaben", expanded=False):
        if effective_rules:
            st.dataframe(
                normalize_table_for_streamlit(effective_rules),
                hide_index=True,
                width="stretch",
            )
        else:
            st.info("Fuer diesen StudyCase sind noch keine definierenden Projektregeln gespeichert.")


def _render_candidate_generation(
    workspace,
    study,
    study_cases: list[dict[str, object]],
    parameter_payload: dict[str, object],
    baseline,
    dimensioning_payload: dict[str, object],
    zone_spec,
    payload: dict[str, object],
    current_fingerprint: str,
    active_case: str,
) -> None:
    st.subheader("Variationsraum festlegen")
    st.dataframe(
        normalize_table_for_streamlit(study_cases),
        hide_index=True,
        width="stretch",
    )
    spans = parameter_payload.get("variation_spans", [])
    if isinstance(spans, list) and spans:
        st.dataframe(normalize_table_for_streamlit(spans), hide_index=True, width="stretch")
    else:
        st.warning(
            "Noch keine projektbezogenen Variationsspannen gespeichert. "
            "Die freigegebene SmallOffice-V1-Studienkonfiguration dient als Kandidatenquelle."
        )
    dimensioning_complete = _dimensioning_complete(
        dimensioning_payload,
        zone_spec,
        baseline,
        parameter_payload,
    )
    if not dimensioning_complete:
        st.warning("Die manuelle Referenzdimensionierung ist noch nicht vollstaendig.")
    variation_ready = variation_specification_is_current(
        parameter_payload,
        baseline,
        study,
    )
    if not variation_ready:
        st.warning(
            "Zuerst in Parameter-Variationsspezifikation den aktuellen Regel- und "
            "Spannenstand speichern."
        )

    candidates = payload.get("candidates", [])
    case_rows = _case_rows(candidates, active_case)
    if case_rows:
        st.dataframe(normalize_table_for_streamlit(case_rows), hide_index=True, width="stretch")
    if st.button(
        "Kandidatenkombinationen erzeugen",
        disabled=not dimensioning_complete or not variation_ready,
        key="ma_variants_generate_candidates",
    ):
        updated_payload = dict(payload)
        updated_payload.update(
            {
                "schema_version": "1.0",
                "project_id": workspace.project.identity.project_id,
                "study_id": study.study_id,
                "study_cases": study_cases,
                "candidates": build_small_office_candidate_rows(
                    study,
                    parameter_payload["variation_specification"],
                ),
                "catalog": [],
                "source_fingerprint": current_fingerprint,
                "status": "candidates_current",
                "updated_at": datetime.now(UTC).isoformat(),
            }
        )
        save_project_module_config(workspace, VARIANTS_MODULE_KEY, updated_payload)
        st.session_state["ma_ui_variants_update_required"] = True
        st.success("Kandidatenkombinationen fuer beide StudyDirections wurden erzeugt.")


def _render_catalog_generation(
    workspace,
    zone_spec,
    baseline,
    parameter_payload: dict[str, object],
    dimensioning_payload: dict[str, object],
    payload: dict[str, object],
    current_fingerprint: str,
    active_case: str,
) -> None:
    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list) or not candidates:
        st.warning("Zuerst im Variationsraum Kandidatenkombinationen erzeugen.")
        return
    candidates_stale = not candidate_source_is_current(payload, current_fingerprint)
    if candidates_stale:
        st.error(
            "Der Kandidatenraum gehoert zu einem aelteren Fachstand. "
            "Bitte im Variationsraum neu erzeugen."
        )
    verified = verify_candidate_rows(
        candidates,
        reference_dimensioning_complete=_dimensioning_complete(
            dimensioning_payload,
            zone_spec,
            baseline,
            parameter_payload,
        ),
    )
    st.dataframe(
        normalize_table_for_streamlit(_case_rows(verified, active_case)),
        hide_index=True,
        width="stretch",
    )
    excluded = sum(row["status"] == "excluded" for row in verified)
    st.caption(
        f"{len(verified) - excluded} gueltig, {excluded} ausgeschlossen. "
        "Ausgeschlossene Kandidaten bleiben mit Grund sichtbar."
    )
    if st.button(
        "Gueltigen Katalog bilden",
        disabled=candidates_stale,
        key="ma_variants_build_catalog",
    ):
        updated_payload = dict(payload)
        updated_payload.update(
            {
                "catalog": verified,
                "source_fingerprint": current_fingerprint,
                "status": "catalog_current",
                "updated_at": datetime.now(UTC).isoformat(),
            }
        )
        save_project_module_config(workspace, VARIANTS_MODULE_KEY, updated_payload)
        st.session_state["ma_ui_variants_update_required"] = True
        st.success("Der gueltige Katalog wurde projektbezogen gespeichert.")


def _render_selection_and_packages(
    workspace,
    study,
    baseline,
    zone_spec,
    parameter_payload: dict[str, object],
    dimensioning_payload: dict[str, object],
    payload: dict[str, object],
    active_case: str,
    current_fingerprint: str,
) -> None:
    catalog = payload.get("catalog", [])
    if not isinstance(catalog, list) or not catalog:
        st.warning("Zuerst unter Pruefung und Katalog den gueltigen Katalog bilden.")
        return
    valid_rows = [
        row
        for row in catalog
        if isinstance(row, dict)
        and row.get("status") == "valid"
        and row.get("study_case_id") == active_case
    ]
    valid_ids = tuple(str(row["candidate_id"]) for row in valid_rows)
    if not valid_ids:
        st.warning("Der aktive StudyCase enthaelt keine gueltigen Kandidaten.")
        return
    mode = st.radio(
        "Auswahlmodus",
        ("manuell", "zufaellig", "alle"),
        horizontal=True,
        key="ma_variants_selection_mode",
    )
    manual_ids: tuple[str, ...] = ()
    count = 1
    seed: int | None = None
    if mode == "manuell":
        manual_ids = tuple(
            st.multiselect(
                "Kandidaten",
                valid_ids,
                default=valid_ids[:1],
                key="ma_variants_manual_selection",
            )
        )
    elif mode == "zufaellig":
        count = st.number_input(
            "Anzahl",
            min_value=1,
            max_value=len(valid_ids),
            value=1,
            step=1,
            key="ma_variants_random_count",
        )
        use_seed = st.checkbox("Reproduzierbaren Startwert verwenden", key="ma_variants_use_seed")
        if use_seed:
            seed = int(
                st.number_input(
                    "Startwert",
                    value=42,
                    step=1,
                    key="ma_variants_random_seed",
                )
            )
    try:
        selected_ids = select_candidate_ids(
            valid_ids,
            mode=mode,
            manual_ids=manual_ids,
            count=int(count),
            seed=seed,
        )
    except ValueError as exc:
        st.warning(str(exc))
        selected_ids = ()
    st.caption(f"{len(selected_ids)} Kandidaten ausgewaehlt.")

    naming_reference = workspace.settings.naming_profile_reference
    if not naming_reference:
        st.error("Vor der Paketerzeugung muss in Projekt ein Naming-Profil ausgewaehlt werden.")
        return
    try:
        naming_profile, _source = load_variant_naming_profile(Path(naming_reference))
    except (OSError, ValueError) as exc:
        st.error(f"Naming-Profil konnte nicht geladen werden: {exc}")
        return
    if st.button(
        "Namensvorschau erzeugen",
        disabled=not selected_ids,
        key="ma_variants_create_naming_preview",
    ):
        st.session_state["ma_variants_naming_preview"] = {
            "context": {
                "project_id": workspace.project.identity.project_id,
                "study_case_id": active_case,
                "candidate_ids": list(selected_ids),
                "source_fingerprint": current_fingerprint,
                "naming_profile_reference": str(naming_reference),
            },
            "rows": _naming_preview(
                naming_profile,
                valid_rows,
                selected_ids,
            ),
        }
    preview = st.session_state.get("ma_variants_naming_preview")
    expected_preview_context = {
        "project_id": workspace.project.identity.project_id,
        "study_case_id": active_case,
        "candidate_ids": list(selected_ids),
        "source_fingerprint": current_fingerprint,
        "naming_profile_reference": str(naming_reference),
    }
    preview_rows = naming_preview_rows_for_context(
        preview,
        expected_preview_context,
    )
    if isinstance(preview_rows, list):
        st.dataframe(
            normalize_table_for_streamlit(preview_rows),
            hide_index=True,
            width="stretch",
        )
    elif preview is not None:
        st.info("Die Namensvorschau gehoert zu einem anderen Kontext und muss neu erzeugt werden.")
    stale = payload.get("source_fingerprint") != current_fingerprint
    if stale:
        st.warning("Die Variantenquelle ist aktualisierungsbeduerftig; Paketerzeugung ist gesperrt.")
    if st.button(
        "Ausgewaehlte Variantenpakete erzeugen",
        disabled=stale or not selected_ids or not isinstance(preview_rows, list),
        key="ma_variants_generate_packages",
    ):
        selected_by_id = {str(row["candidate_id"]): row for row in valid_rows}
        names_by_id = {
            str(row["candidate_id"]): str(row["variant_name"])
            for row in preview_rows
        }
        selection_fingerprint = source_fingerprint(
            {
                "study_case_id": active_case,
                "mode": mode,
                "candidate_ids": sorted(selected_ids),
                "random_seed": seed,
                "source_fingerprint": current_fingerprint,
            }
        )
        selection_id = f"SEL-{active_case}-{selection_fingerprint[:12]}"
        selection_reference = {
            "selection_id": selection_id,
            "selection_fingerprint": selection_fingerprint,
            "study_case_id": active_case,
            "study_direction_id": str(valid_rows[0]["study_direction_id"]),
            "mode": mode,
            "candidate_ids": list(selected_ids),
            "random_seed": seed,
            "source_fingerprint": current_fingerprint,
        }
        packages = [
            _variant_package(
                study=study,
                baseline=baseline,
                zone_spec=zone_spec,
                parameter_payload=parameter_payload,
                dimensioning_payload=dimensioning_payload,
                candidate=selected_by_id[candidate_id],
                variant_name=names_by_id[candidate_id],
                selection_reference=selection_reference,
                current_fingerprint=current_fingerprint,
            )
            for candidate_id in selected_ids
        ]
        updated_payload = dict(payload)
        updated_payload.update(
            {
                "selection": {
                    **selection_reference,
                },
                "variant_packages": packages,
                "status": "packages_current",
                "updated_at": datetime.now(UTC).isoformat(),
            }
        )
        save_project_module_config(workspace, VARIANTS_MODULE_KEY, updated_payload)
        st.session_state["ma_ui_variants_update_required"] = False
        st.success("Die ausgewaehlten Variantenpakete wurden projektbezogen erzeugt.")


def _dimensioning_complete(
    payload: dict[str, object],
    zone_spec,
    baseline,
    parameter_payload: dict[str, object],
) -> bool:
    zone_loads = payload.get("zone_loads", [])
    expected_zone_ids = {zone.zone_id for zone in zone_spec.zones}
    actual_zone_ids = [
        str(row.get("zone_id"))
        for row in zone_loads
        if isinstance(row, dict)
    ] if isinstance(zone_loads, list) else []
    ida_source = payload.get("ida_source", {})
    ida_required = {
        "ida_version",
        "model_id",
        "run_id",
        "source_file_name",
        "source_file_sha256",
        "heating_load_definition",
        "cooling_load_definition",
        "maximum_definition",
        "design_conditions",
        "responsible",
        "reviewer",
        "reviewed_at",
        "review_note",
        "source_classification",
    }
    return (
        payload.get("zone_model_id") == zone_spec.zone_model_id
        and payload.get("zone_model_hash")
        == _content_hash(zone_specification_to_dict(zone_spec))
        and
        isinstance(zone_loads, list)
        and len(zone_loads) == len(expected_zone_ids)
        and len(actual_zone_ids) == len(set(actual_zone_ids))
        and set(actual_zone_ids) == expected_zone_ids
        and isinstance(ida_source, dict)
        and ida_source.get("review_status") == "reviewed"
        and ida_required <= set(ida_source)
        and all(str(ida_source.get(key, "")).strip() for key in ida_required)
        and re.fullmatch(
            r"[0-9a-f]{64}",
            str(ida_source.get("source_file_sha256", "")),
        )
        is not None
        and payload.get("reference_parameter_fingerprint")
        == reference_dimensioning_parameter_fingerprint(
            baseline,
            parameter_payload,
        )
        and all(
            isinstance(row, dict)
            and isinstance(row.get("heating_load_w"), int | float)
            and isinstance(row.get("cooling_load_w"), int | float)
            and math.isfinite(float(row["heating_load_w"]))
            and math.isfinite(float(row["cooling_load_w"]))
            and row["heating_load_w"] >= 0
            and row["cooling_load_w"] >= 0
            for row in zone_loads
        )
    )


def _variant_package(
    *,
    study,
    baseline,
    zone_spec,
    parameter_payload: dict[str, object],
    dimensioning_payload: dict[str, object],
    candidate: dict[str, object],
    variant_name: str,
    selection_reference: dict[str, object],
    current_fingerprint: str,
) -> dict[str, object]:
    zone_loads = dimensioning_payload.get("zone_loads", [])
    if not isinstance(zone_loads, list):
        raise ValueError("Zonale Referenzlasten fehlen.")
    output_requirements = [asdict(item) for item in default_output_requirements()]
    return {
        "schema_version": "1.0",
        "variant_id": str(candidate["candidate_id"]),
        "variant_name": variant_name,
        "study_id": study.study_id,
        "study_case_id": str(candidate["study_case_id"]),
        "study_direction_id": str(candidate["study_direction_id"]),
        "selection_id": selection_reference["selection_id"],
        "selection_reference": selection_reference,
        "candidate": candidate,
        "baseline_reference": {
            "snapshot_id": baseline.snapshot_id,
            "snapshot_version": baseline.snapshot_version,
            "content_hash": baseline.content_hash,
        },
        "parameter_reference": {
            "project_configuration_fingerprint": source_fingerprint(parameter_payload),
        },
        "zone_model_reference": {
            "zone_model_id": zone_spec.zone_model_id,
            "content_hash": _content_hash(zone_specification_to_dict(zone_spec)),
            "zone_ids": [zone.zone_id for zone in zone_spec.zones],
        },
        "dimensioning_reference": {
            "content_hash": source_fingerprint(dimensioning_payload),
            "source_type": dimensioning_payload.get("source_type"),
            "ida_source": dimensioning_payload.get("ida_source"),
        },
        "capacity_strategy": "fixed_reference_21_24_zonal_capacity",
        "zonal_capacities": materialize_zonal_capacities(candidate, zone_loads),
        "simulation_setup": candidate_simulation_setup(study, candidate),
        "output_requirements": output_requirements,
        "source_fingerprint": current_fingerprint,
        "status": "confirmed",
    }


def _case_rows(rows: object, active_case: str) -> list[dict[str, object]]:
    if not isinstance(rows, list):
        return []
    return [
        row
        for row in rows
        if isinstance(row, dict) and row.get("study_case_id") == active_case
    ]


def _naming_preview(profile, rows: list[dict[str, object]], selected_ids: tuple[str, ...]) -> list[dict[str, object]]:
    selected_by_id = {str(row["candidate_id"]): row for row in rows}
    preview = []
    for index, candidate_id in enumerate(selected_ids, start=1):
        parts = [profile.prefix]
        if profile.include_index:
            parts.append(f"{index:0{profile.index_width}d}")
        parts.append(candidate_id)
        preview.append(
            {
                "candidate_id": candidate_id,
                "variant_name": profile.separator.join(parts),
                "label": selected_by_id[candidate_id]["label"],
            }
        )
    return preview


def naming_preview_rows_for_context(
    preview: object,
    expected_context: dict[str, object],
) -> list[dict[str, object]] | None:
    """Gibt eine Vorschau nur in ihrem exakten Projekt-/Auswahlkontext frei."""
    if not isinstance(preview, dict) or preview.get("context") != expected_context:
        return None
    rows = preview.get("rows")
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        return None
    return rows


def _content_hash(payload: object) -> str:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
