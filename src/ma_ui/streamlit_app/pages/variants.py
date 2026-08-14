"""Projektbezogene V1-Variantenbildung in drei klaren Arbeitsschritten."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

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
    SMALL_OFFICE_V1_STUDY_CONFIGS,
    build_small_office_candidate_rows,
    candidate_simulation_setup,
    load_small_office_v1_study,
    materialize_zonal_capacities,
    select_candidate_ids,
    small_office_source_fingerprint,
    small_office_study_case_rows,
    source_fingerprint,
    variation_specification_is_current,
    verify_candidate_rows,
)
from ma_variants.project_studies import SMALL_OFFICE_CAPACITY_COUPLING_RULE
from ma_variants.vver_selection import (
    VverSelectionRecord,
    create_vver_selection_record,
    validate_vver_selection_is_current,
    vver_selection_record_from_payload,
    vver_selection_record_to_payload,
)
from ma_workspace import load_project_module_config, save_project_module_config
from ma_zones import (
    load_small_office_5z_endvariant_02_zone_spec,
    zone_specification_to_dict,
)

VARIANTS_MODULE_KEY = "ma_variants"
VARIANT_STEP_LABELS = (
    "Variationsraum und VVER",
    "Pruefung und Katalog",
    "Auswahl und Variantenpakete",
)


@dataclass(frozen=True)
class _VverResolvedValue:
    """Adapter, der gespeicherte Kandidatenzeilen an den VVER-Vertrag bindet."""

    parameter_key: str
    value: object
    unit: str = ""


@dataclass(frozen=True)
class _VverCandidate:
    candidate_id: str
    selected_options: tuple[tuple[str, str], ...]
    resolved_values: tuple[_VverResolvedValue, ...]


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

    config_options = tuple(SMALL_OFFICE_V1_STUDY_CONFIGS)
    selected_config_key = st.selectbox(
        "Studienkonfiguration",
        config_options,
        index=config_options.index(str(payload.get("study_config_key", "standard")))
        if str(payload.get("study_config_key", "standard")) in config_options
        else 0,
        format_func=lambda key: SMALL_OFFICE_V1_STUDY_CONFIGS[key][0],
        key="ma_variants_study_config",
        help="Der Testraum ist getrennt vom 30er-Referenzbenchmark und erzeugt 156 theoretische Optimierungsvarianten.",
    )
    try:
        study = load_small_office_v1_study(SMALL_OFFICE_V1_STUDY_CONFIGS[selected_config_key][1])
    except (OSError, ValueError, KeyError) as exc:
        st.error(f"Studienkonfiguration konnte nicht geladen werden: {exc}")
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
    pre_dimensioning_fingerprint = pre_dimensioning_source_fingerprint(
        study,
        baseline,
        zone_spec,
        parameter_payload,
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
    if step == "Variationsraum und VVER":
        _render_candidate_generation(
            workspace,
            study,
            study_cases,
            parameter_payload,
            baseline,
            payload,
            pre_dimensioning_fingerprint,
            active_case,
            selected_config_key,
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
            study,
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
    if direction == "optimization":
        effective_rules.append(SMALL_OFFICE_CAPACITY_COUPLING_RULE)
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
    payload: dict[str, object],
    pre_dimensioning_fingerprint: str,
    active_case: str,
    study_config_key: str,
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
        disabled=not variation_ready,
        key="ma_variants_generate_candidates",
    ):
        started = perf_counter()
        generated_candidates = build_small_office_candidate_rows(
            study,
            parameter_payload["variation_specification"],
        )
        updated_payload = dict(payload)
        updated_payload.update(
            {
                "schema_version": "1.0",
                "project_id": workspace.project.identity.project_id,
                "study_id": study.study_id,
                "study_config_key": study_config_key,
                "study_cases": study_cases,
                "candidates": generated_candidates,
                "catalog": [],
                "pre_dimensioning_source_fingerprint": pre_dimensioning_fingerprint,
                "status": "candidates_current",
                "updated_at": datetime.now(UTC).isoformat(),
            }
        )
        updated_payload["technical_timings"] = [
            _timing_row(
                "candidate_generation",
                perf_counter() - started,
                f"{len(generated_candidates)} Kandidaten erzeugt",
            )
        ]
        save_project_module_config(workspace, VARIANTS_MODULE_KEY, updated_payload)
        st.session_state["ma_ui_variants_update_required"] = True
        st.success(
            "Kandidatenkombinationen fuer beide StudyDirections wurden erzeugt. "
            "Bestehende VVER-Auswahlen bleiben als Historie erhalten und werden gegen den neuen Stand geprueft."
        )

    _render_vver_selection(
        workspace,
        study,
        payload,
        active_case,
        pre_dimensioning_fingerprint,
    )


def _render_vver_selection(
    workspace,
    study,
    payload: dict[str, object],
    active_case: str,
    pre_dimensioning_fingerprint: str,
) -> None:
    """Speichert die verbindliche Kandidatenauswahl vor der Dimensionierung."""
    st.divider()
    st.subheader("VVER: verbindliche Auswahl vor der Dimensionierung")
    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list) or not candidates:
        st.info("Nach dem Erzeugen des Variationsraums kann hier die VVER-Auswahl gespeichert werden.")
        return
    if not _pre_dimensioning_candidates_are_current(payload, pre_dimensioning_fingerprint):
        st.error(
            "Der Variationsraum hat keinen aktuellen Pre-Dimensioning-Fingerprint. "
            "Bitte die Kandidatenkombinationen neu erzeugen; Katalog und VVER-Historie bleiben erhalten."
        )
        return
    history_error = _vver_history_error(payload)
    if history_error is not None:
        st.error(f"Die gespeicherte VVER-Historie ist fehlerhaft und blockiert den Ablauf: {history_error}")
        return
    case_candidates = _case_rows(candidates, active_case)
    candidate_ids = tuple(str(row["candidate_id"]) for row in case_candidates)
    if not candidate_ids:
        st.warning("Der aktive StudyCase enthaelt keine Kandidaten.")
        return
    mode, manual_ids, count, seed = _selection_controls(candidate_ids, key_prefix="ma_vver")
    try:
        selected_ids = select_candidate_ids(
            candidate_ids,
            mode=mode,
            manual_ids=manual_ids,
            count=count,
            seed=seed,
        )
    except ValueError as exc:
        st.warning(str(exc))
        selected_ids = ()
    reason = st.text_input(
        "Begruendung der VVER-Auswahl",
        value="Auswahl fuer die nachfolgende Referenzdimensionierung.",
        key="ma_vver_selection_reason",
    )
    random_selection_without_seed = not _vver_selection_is_saveable(mode, seed)
    if random_selection_without_seed:
        st.warning("Eine zufaellige VVER-Auswahl braucht einen reproduzierbaren Startwert.")
    st.caption(f"{len(selected_ids)} Kandidaten werden vor der Dimensionierung verbindlich ausgewaehlt.")
    if st.button(
        "VVER-Auswahl verbindlich speichern",
        disabled=not selected_ids or not reason.strip() or random_selection_without_seed,
        key="ma_vver_save_selection",
    ):
        started = perf_counter()
        selected_rows = [row for row in case_candidates if str(row["candidate_id"]) in selected_ids]
        record = create_vver_selection_record(
            study_id=study.study_id,
            study_case_id=active_case,
            study_direction_id=str(selected_rows[0]["study_direction_id"]),
            selection_mode={"manuell": "manual", "zufaellig": "random", "alle": "all"}[mode],
            selection_reason=reason.strip(),
            random_seed=seed,
            pre_dimensioning_upstream_fingerprint=pre_dimensioning_fingerprint,
            selected_candidates=tuple(_vver_candidate_from_row(row) for row in selected_rows),
        )
        updated_payload = _store_vver_selection(payload, record)
        _append_timing(
            updated_payload,
            "vver_selection",
            perf_counter() - started,
            f"{len(selected_rows)} Kandidaten verbindlich ausgewaehlt",
        )
        updated_payload["updated_at"] = datetime.now(UTC).isoformat()
        updated_payload["status"] = "vver_selection_current"
        save_project_module_config(workspace, VARIANTS_MODULE_KEY, updated_payload)
        st.success("Die VVER-Auswahl wurde ohne finale VAR-ID gespeichert.")
        payload = updated_payload
    active_record = _active_vver_selection(payload)
    if active_record is not None:
        try:
            validate_vver_selection_is_current(
                active_record,
                current_pre_dimensioning_upstream_fingerprint=pre_dimensioning_fingerprint,
                current_candidates=tuple(_vver_candidate_from_row(row) for row in case_candidates),
            )
        except ValueError as exc:
            st.warning(f"Die aktive VVER-Auswahl ist nicht mehr aktuell: {exc}")
        else:
            st.success(
                f"Aktive VVER-Auswahl: {active_record.record_id} "
                f"({len(active_record.selected_candidates)} Kandidaten)."
            )


def _render_catalog_generation(
    workspace,
    zone_spec,
    baseline,
    parameter_payload: dict[str, object],
    dimensioning_payload: dict[str, object],
    payload: dict[str, object],
    current_fingerprint: str,
    active_case: str,
    study,
) -> None:
    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list) or not candidates:
        st.warning("Zuerst im Variationsraum Kandidatenkombinationen erzeugen.")
        return
    pre_dimensioning_fingerprint = pre_dimensioning_source_fingerprint(study, baseline, zone_spec, parameter_payload)
    candidates_stale = not _pre_dimensioning_candidates_are_current(
        payload, pre_dimensioning_fingerprint
    )
    if candidates_stale:
        st.error(
            "Der Kandidatenraum hat keinen aktuellen Pre-Dimensioning-Fingerprint. "
            "Bitte im Variationsraum neu erzeugen; Katalog und VVER-Historie bleiben erhalten."
        )
    history_error = _vver_history_error(payload)
    if history_error is not None:
        st.error(f"Die gespeicherte VVER-Historie ist fehlerhaft und blockiert den Ablauf: {history_error}")
    active_vver_selection = active_current_vver_selection(
        payload,
        study_id=study.study_id,
        current_pre_dimensioning_upstream_fingerprint=pre_dimensioning_fingerprint,
    )
    if active_vver_selection is None:
        st.warning(
            "Der finale Katalog braucht eine aktuelle, aktive VVER-Auswahl. "
            "Bitte diese zuerst im Variationsraum speichern."
        )
    dimensioning_complete = _dimensioning_complete(
        dimensioning_payload, zone_spec, baseline, parameter_payload
    )
    if not dimensioning_complete:
        st.warning("Der finale Katalog bleibt bis zur vollstaendigen Referenzdimensionierung gesperrt.")
    dimensioning_matches_vver = (
        active_vver_selection is not None
        and _dimensioning_is_bound_to_vver(dimensioning_payload, active_vver_selection)
    )
    if dimensioning_complete and not dimensioning_matches_vver:
        st.warning(
            "Die gespeicherte Referenzdimensionierung gehoert nicht zur aktuellen VVER-Auswahl. "
            "Bitte die Referenzdimensionierung erneut speichern."
        )
    selected_candidate_ids = (
        {reference.candidate_id for reference in active_vver_selection.selected_candidates}
        if active_vver_selection is not None
        else set()
    )
    selected_candidates = _selected_candidate_rows(candidates, selected_candidate_ids)
    verified = verify_candidate_rows(
        selected_candidates,
        reference_dimensioning_complete=dimensioning_complete,
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
        disabled=(
            candidates_stale
            or history_error is not None
            or active_vver_selection is None
            or not dimensioning_complete
            or not dimensioning_matches_vver
        ),
        key="ma_variants_build_catalog",
    ):
        started = perf_counter()
        updated_payload = dict(payload)
        updated_payload.update(
            {
                "catalog": verified,
                "source_fingerprint": current_fingerprint,
                "status": "catalog_current",
                "updated_at": datetime.now(UTC).isoformat(),
            }
        )
        _append_timing(
            updated_payload,
            "catalog_generation",
            perf_counter() - started,
            f"{len(verified)} Kandidaten geprueft",
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
        started = perf_counter()
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
        theoretical_variant_count = sum(
            1
            for row in payload.get("candidates", [])
            if isinstance(row, dict) and row.get("study_direction") == "optimization"
        )
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
                theoretical_variant_count=theoretical_variant_count,
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
        _append_timing(
            updated_payload,
            "variant_package_generation",
            perf_counter() - started,
            f"{len(packages)} Variantenpakete erzeugt",
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
    theoretical_variant_count: int,
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
        "theoretical_variant_count": theoretical_variant_count,
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
        "capacity_strategy": str(
            (candidate.get("values") or {}).get("capacity_strategy", "dimensioned_with_factor")
        ),
        "zonal_capacities": materialize_zonal_capacities(candidate, zone_loads),
        "simulation_setup": candidate_simulation_setup(study, candidate),
        "output_requirements": output_requirements,
        "source_fingerprint": current_fingerprint,
        "status": "confirmed",
    }


def _timing_row(stage: str, duration_seconds: float, details: str) -> dict[str, object]:
    return {
        "stage": stage,
        "status": "success",
        "duration_seconds": round(duration_seconds, 6),
        "recorded_at": datetime.now(UTC).isoformat(),
        "details": details,
    }


def _append_timing(payload: dict[str, object], stage: str, duration_seconds: float, details: str) -> None:
    existing = payload.get("technical_timings", [])
    rows = [row for row in existing if isinstance(row, dict)] if isinstance(existing, list) else []
    rows.append(_timing_row(stage, duration_seconds, details))
    payload["technical_timings"] = rows


def _case_rows(rows: object, active_case: str) -> list[dict[str, object]]:
    if not isinstance(rows, list):
        return []
    return [
        row
        for row in rows
        if isinstance(row, dict) and row.get("study_case_id") == active_case
    ]


def pre_dimensioning_source_fingerprint(study, baseline, zone_spec, parameter_payload: dict[str, object]) -> str:
    """Bindet VSP und VVER nur an ihre fachlichen Eingaben, nicht an Referenzlasten."""
    return source_fingerprint(
        asdict(study),
        {
            "snapshot_id": baseline.snapshot_id,
            "snapshot_version": baseline.snapshot_version,
            "content_hash": baseline.content_hash,
        },
        zone_specification_to_dict(zone_spec),
        parameter_payload.get("variation_specification"),
        parameter_payload.get("variation_spans"),
        parameter_payload.get("rules"),
    )


def _pre_dimensioning_source_fingerprint(study, baseline, zone_spec, parameter_payload: dict[str, object]) -> str:
    """Kompatibilitaetsalias fuer bestehende Aufrufer waehrend der VVER-Migration."""
    return pre_dimensioning_source_fingerprint(study, baseline, zone_spec, parameter_payload)


def _pre_dimensioning_candidates_are_current(
    payload: dict[str, object], current_fingerprint: str
) -> bool:
    """Akzeptiert nur Kandidaten mit dem vollstaendigen VVER-Quellenfingerprint."""
    stored_fingerprint = payload.get("pre_dimensioning_source_fingerprint")
    return (
        isinstance(payload.get("candidates"), list)
        and bool(payload["candidates"])
        and isinstance(stored_fingerprint, str)
        and stored_fingerprint == current_fingerprint
    )


def _vver_candidate_from_row(row: dict[str, object]) -> _VverCandidate:
    values = row.get("values")
    if not isinstance(values, dict):
        raise ValueError("VVER-Kandidatenwerte fehlen.")
    return _VverCandidate(
        candidate_id=str(row["candidate_id"]),
        selected_options=tuple(sorted((str(key), str(value)) for key, value in values.items())),
        resolved_values=tuple(
            _VverResolvedValue(parameter_key=str(key), value=value)
            for key, value in sorted(values.items())
        ),
    )


def _store_vver_selection(
    payload: dict[str, object], record: VverSelectionRecord
) -> dict[str, object]:
    """Speichert Records append-only nach ID und setzt genau eine aktive VVER-Auswahl."""
    history_error = _vver_history_error(payload)
    if history_error is not None:
        raise ValueError(f"VVER-Historie ist fehlerhaft: {history_error}")
    existing = payload.get("vver_selections", [])
    selections = list(existing) if isinstance(existing, list) else []
    serialized = vver_selection_record_to_payload(record)
    selections = [entry for entry in selections if entry.get("record_id") != record.record_id]
    selections.append(serialized)
    updated = dict(payload)
    updated["vver_selections"] = selections
    updated["active_vver_selection_id"] = record.record_id
    return updated


def _active_vver_selection(payload: dict[str, object]) -> VverSelectionRecord | None:
    history_error = _vver_history_error(payload)
    if history_error is not None:
        raise ValueError(f"VVER-Historie ist fehlerhaft: {history_error}")
    active_id = payload.get("active_vver_selection_id")
    selections = payload.get("vver_selections", [])
    if active_id is None and selections == []:
        return None
    for entry in selections:
        if entry["record_id"] == active_id:
            return vver_selection_record_from_payload(entry)
    raise ValueError("Die aktive VVER-Auswahl ist in der Historie nicht vorhanden.")


def _vver_history_error(payload: dict[str, object]) -> str | None:
    """Prueft die persistierte Historie vollstaendig, bevor sie weiterverwendet wird."""
    selections = payload.get("vver_selections", [])
    active_id = payload.get("active_vver_selection_id")
    if not isinstance(selections, list):
        return "vver_selections muss eine Liste sein."
    if not selections:
        return None if active_id is None else "Eine aktive VVER-ID existiert ohne Historieneintrag."
    if not isinstance(active_id, str) or not active_id:
        return "Die aktive VVER-ID fehlt oder ist ungueltig."

    record_ids: set[str] = set()
    for index, entry in enumerate(selections, start=1):
        if not isinstance(entry, dict):
            return f"Historieneintrag {index} ist kein Objekt."
        try:
            record = vver_selection_record_from_payload(entry)
        except ValueError as exc:
            return f"Historieneintrag {index} ist ungueltig: {exc}"
        if record.record_id in record_ids:
            return f"Historieneintrag {index} dupliziert die VVER-ID {record.record_id}."
        record_ids.add(record.record_id)
    if active_id not in record_ids:
        return "Die aktive VVER-ID verweist auf keinen Historieneintrag."
    return None


def active_current_vver_selection(
    payload: dict[str, object],
    *,
    study_id: str,
    current_pre_dimensioning_upstream_fingerprint: str,
) -> VverSelectionRecord | None:
    """Gibt nur eine aktive, zum aktuellen Kandidatenraum passende VVER-Auswahl frei."""
    if _vver_history_error(payload) is not None:
        return None
    record = _active_vver_selection(payload)
    candidates = payload.get("candidates", [])
    if record is None or record.study_id != study_id or not isinstance(candidates, list):
        return None
    try:
        validate_vver_selection_is_current(
            record,
            current_pre_dimensioning_upstream_fingerprint=current_pre_dimensioning_upstream_fingerprint,
            current_candidates=tuple(
                _vver_candidate_from_row(row) for row in candidates if isinstance(row, dict)
            ),
        )
    except ValueError:
        return None
    return record


def _dimensioning_is_bound_to_vver(
    dimensioning_payload: dict[str, object], record: VverSelectionRecord
) -> bool:
    reference = dimensioning_payload.get("vver_selection_reference", {})
    return (
        isinstance(reference, dict)
        and reference.get("record_id") == record.record_id
        and reference.get("record_fingerprint") == record.record_fingerprint
    )


def _selected_candidate_rows(
    candidates: object, selected_candidate_ids: set[str]
) -> list[dict[str, object]]:
    """Beschraenkt VCAT auf die vor der Dimensionierung verbindlich gewaehlten Kandidaten."""
    if not isinstance(candidates, list):
        return []
    return [
        row
        for row in candidates
        if isinstance(row, dict) and str(row.get("candidate_id")) in selected_candidate_ids
    ]


def _selection_controls(
    candidate_ids: tuple[str, ...], *, key_prefix: str
) -> tuple[str, tuple[str, ...], int, int | None]:
    """Gemeinsame Eingaben fuer die deutsche UI und den Auswahlvertrag."""
    mode = st.radio(
        "Auswahlmodus", ("manuell", "zufaellig", "alle"), horizontal=True, key=f"{key_prefix}_mode"
    )
    manual_ids: tuple[str, ...] = ()
    count = 1
    seed: int | None = None
    if mode == "manuell":
        manual_ids = tuple(
            st.multiselect("Kandidaten", candidate_ids, default=candidate_ids[:1], key=f"{key_prefix}_manual")
        )
    elif mode == "zufaellig":
        count = int(
            st.number_input("Anzahl", min_value=1, max_value=len(candidate_ids), value=1, step=1, key=f"{key_prefix}_count")
        )
        if st.checkbox("Reproduzierbaren Startwert verwenden", key=f"{key_prefix}_use_seed"):
            seed = int(st.number_input("Startwert", value=42, step=1, key=f"{key_prefix}_seed"))
    return mode, manual_ids, count, seed


def _vver_selection_is_saveable(mode: str, seed: int | None) -> bool:
    """Der VVER-Vertrag verlangt bei Zufallsauswahl immer einen Startwert."""
    return mode != "zufaellig" or seed is not None


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
