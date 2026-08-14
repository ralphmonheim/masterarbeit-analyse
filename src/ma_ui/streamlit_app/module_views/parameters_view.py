"""Reduzierte V1-Bearbeitungsansicht fuer zentrale Parameter."""

from __future__ import annotations

import math
from datetime import UTC, datetime

import streamlit as st

from ma_parameters import (
    build_business_integration_lod1_baseline_parameter_snapshot,
    build_small_office_5z_v1_baseline_parameter_snapshot,
    variation_specification_source_fingerprint,
)
from ma_ui.streamlit_app.shared import normalize_table_for_streamlit
from ma_ui.streamlit_app.state import (
    clear_workspace_draft,
    get_active_workspace,
    mark_workspace_draft,
)
from ma_variants.project_studies import SMALL_OFFICE_CAPACITY_COUPLING_RULE
from ma_workspace import load_project_module_config, save_project_module_config

PARAMETER_MODULE_KEY = "ma_parameters"
PARAMETER_SECTION_LABELS = (
    "Referenzparameter",
    "Regeln/Vorgaben",
    "Variationsspannen",
    "Uebergabe/Pruefung",
)
RULE_SCOPE_OPTIONS = ("project", "study_direction", "study_case")
RULE_TYPE_OPTIONS = ("coupling", "lock", "hard_limit", "dimensioning_relevance")
VALUE_FORM_OPTIONS = (
    "kein Wert",
    "Einzelwert",
    "Min/Max/Schritt",
    "explizite Liste",
    "gekoppelte Werte",
    "Referenzoption",
)
SMALL_OFFICE_V1_STUDY_ID = "STUDY-SMALL-OFFICE-5Z-V1"
SMALL_OFFICE_V1_DIMENSIONS = (
    "temperature_setpoint_bands",
    "coupled_heating_cooling_capacity_factors",
    "weather_ofat",
    "occupancy_ofat",
)
CAPACITY_STRATEGY_OPTIONS = {
    "ideal_unlimited": "Ideal / unbegrenzt",
    "reference_dimensioned": "Nach Referenzdimensionierung (100 %)",
    "dimensioned_with_factor": "Nach Dimensionierung mit Leistungsfaktor",
}


def render() -> None:
    """Zeigt den Parameter-Referenzstand als ersten ma_parameters-Schritt."""
    _render_parameter_workspace(
        default_section="Referenzparameter",
        state_key="ma_parameters_reference_section",
        title="Parameter-Referenzstand",
    )


def render_variation() -> None:
    """Zeigt dieselbe Fachkonfiguration mit Fokus auf die Variationsspezifikation."""
    _render_parameter_workspace(
        default_section="Variationsspannen",
        state_key="ma_parameters_variation_section",
        title="Parameter-Variationsspezifikation",
    )


def parameter_reference_rows(baseline) -> list[dict[str, object]]:
    """Bereitet alle freigegebenen Baseline-Werte fuer die V1-Tabelle auf."""
    return [
        {
            "Parameter-ID": value.parameter_value_id,
            "Parameter": value.label,
            "Referenzwert": value.value,
            "Einheit": value.unit,
            "Scope": f"{value.scope.scope_type.value}: {value.scope.scope_id}",
            "Variabilitaet": value.variability.value,
            "Status": value.status,
        }
        for value in baseline.parameter_values
    ]


def variation_span_table_rows(baseline, spans: object) -> list[dict[str, object]]:
    """Bereitet fuer jeden Baseline-Parameter eine bearbeitbare Spannenzeile vor."""
    stored_spans = {
        str(span["parameter_key"]): span
        for span in spans
        if isinstance(span, dict) and span.get("parameter_key")
    } if isinstance(spans, list) else {}
    rows: list[dict[str, object]] = []
    for value in baseline.parameter_values:
        stored_span = stored_spans.get(value.parameter_key, {})
        reference_value = value.value
        rows.append(
            {
                "parameter_key": value.parameter_key,
                "label": value.label,
                "unit": value.unit,
                "reference_value": reference_value,
                "minimum": stored_span.get("minimum", reference_value),
                "maximum": stored_span.get("maximum", reference_value),
                "step": stored_span.get("step", 1.0),
                "enabled": bool(stored_span.get("enabled", False)),
            }
        )
    return rows


def validate_parameter_project_payload(payload: dict[str, object]) -> tuple[str, ...]:
    """Prueft nur den vereinbarten projektbezogenen V1-Vertrag."""
    errors: list[str] = []
    reference = payload.get("reference")
    if not isinstance(reference, dict) or not reference.get("snapshot_id"):
        errors.append("Der aktuelle Referenzstand fehlt.")
    rules = payload.get("rules", [])
    if not isinstance(rules, list):
        errors.append("Regeln/Vorgaben muessen als Liste gespeichert sein.")
    else:
        for index, rule in enumerate(rules, start=1):
            if not isinstance(rule, dict) or not rule.get("rule_id") or not rule.get("title"):
                errors.append(f"Regel {index} braucht ID und Bezeichnung.")
                continue
            if rule.get("scope_type") not in RULE_SCOPE_OPTIONS:
                errors.append(f"Regel {index} hat keinen gueltigen Geltungsstatus.")
            if rule.get("scope_type") != "project" and not str(rule.get("scope_id", "")).strip():
                errors.append(f"Regel {index} braucht eine StudyDirection- oder StudyCase-ID.")
    spans = payload.get("variation_spans", [])
    if not isinstance(spans, list):
        errors.append("Variationsspannen muessen als Liste gespeichert sein.")
    else:
        seen_parameters: set[str] = set()
        for index, span in enumerate(spans, start=1):
            if not isinstance(span, dict) or not span.get("parameter_key"):
                errors.append(f"Variationsspanne {index} braucht einen Parameter.")
                continue
            parameter_key = str(span["parameter_key"])
            if parameter_key in seen_parameters:
                errors.append(f"Variationsspanne {index} verwendet einen Parameter doppelt.")
            seen_parameters.add(parameter_key)
            if not isinstance(span.get("enabled"), bool):
                errors.append(f"Variationsspanne {index}: enabled muss true oder false sein.")
                continue
            if span.get("enabled") and span.get("value_form") not in VALUE_FORM_OPTIONS:
                errors.append(f"Variationsspanne {index} hat keine gueltige Werteform.")
                continue
            if not span.get("enabled"):
                continue
            value_form = span.get("value_form")
            if value_form == "kein Wert":
                errors.append(f"Variationsspanne {index} ist aktiviert, hat aber keine Werteform.")
            elif value_form == "Einzelwert":
                try:
                    value = float(span["value"])
                except (KeyError, TypeError, ValueError):
                    errors.append(f"Variationsspanne {index} braucht einen numerischen Einzelwert.")
                else:
                    if not math.isfinite(value):
                        errors.append(f"Variationsspanne {index} braucht einen endlichen Einzelwert.")
            elif value_form == "Min/Max/Schritt":
                _validate_numeric_span(span, index, errors)
            elif value_form == "explizite Liste":
                if not isinstance(span.get("values"), list) or not span.get("values"):
                    errors.append(
                        f"Variationsspanne {index} braucht eine nichtleere explizite Werteliste."
                    )
            elif value_form == "gekoppelte Werte":
                if not str(span.get("coupling_key", "")).strip():
                    errors.append(f"Variationsspanne {index} braucht eine Kopplungs-ID.")
                if not str(span.get("values", "")).strip():
                    errors.append(f"Variationsspanne {index} braucht gekoppelte Werte.")
            elif value_form == "Referenzoption" and not str(
                span.get("reference_option", "")
            ).strip():
                errors.append(f"Variationsspanne {index} braucht eine Referenzoptions-ID.")
    return tuple(errors)


def _render_parameter_workspace(
    *,
    default_section: str,
    state_key: str,
    title: str,
) -> None:
    st.title(title)
    st.caption(
        "Referenzwerte, definierende Regeln und freigegebene Variationsformen. "
        "Aenderungen werden erst ueber den jeweiligen Speicherbutton in das Projekt geschrieben."
    )
    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.warning("Bitte zuerst ein Projekt auswaehlen.")
        return
    try:
        baseline = _active_baseline(workspace)
        payload = load_project_module_config(workspace, PARAMETER_MODULE_KEY) or {}
    except (OSError, ValueError, KeyError) as exc:
        st.error(f"Parameterstand konnte nicht vorbereitet werden: {exc}")
        return

    section = st.segmented_control(
        "Parameterbereich",
        PARAMETER_SECTION_LABELS,
        default=default_section,
        key=state_key,
        selection_mode="single",
    )
    section = section or default_section
    if section == "Referenzparameter":
        _render_reference_section(workspace, baseline, payload)
    elif section == "Regeln/Vorgaben":
        _render_rules_section(workspace, baseline, payload)
    elif section == "Variationsspannen":
        _render_variation_section(workspace, baseline, payload)
    else:
        _render_handover_section(workspace, baseline, payload)


def _active_baseline(workspace):
    if workspace.project.identity.title == "Masterarbeit-Analyse":
        return build_small_office_5z_v1_baseline_parameter_snapshot()
    return build_business_integration_lod1_baseline_parameter_snapshot()


def _render_reference_section(workspace, baseline, payload: dict[str, object]) -> None:
    st.caption(
        "Der Referenzoptionswert ist der fuer die Referenzdimensionierung wirksame Wert. "
        "Variationen bleiben zunaechst gesperrt."
    )
    capacity_state = payload.get("capacity_strategy", {})
    selected_strategy = (
        str(capacity_state.get("mode"))
        if isinstance(capacity_state, dict) and capacity_state.get("mode") in CAPACITY_STRATEGY_OPTIONS
        else (
            "dimensioned_with_factor"
            if workspace.project.identity.title == "Masterarbeit-Analyse"
            else "ideal_unlimited"
        )
    )
    selected_strategy = st.selectbox(
        "Leistungsbegrenzung der Studie",
        tuple(CAPACITY_STRATEGY_OPTIONS),
        index=tuple(CAPACITY_STRATEGY_OPTIONS).index(selected_strategy),
        format_func=CAPACITY_STRATEGY_OPTIONS.__getitem__,
        key="ma_parameters_capacity_strategy",
        on_change=_mark_parameters_draft,
    )
    st.dataframe(
        normalize_table_for_streamlit(_capacity_strategy_rows(workspace, selected_strategy)),
        hide_index=True,
        width="stretch",
    )
    st.dataframe(
        normalize_table_for_streamlit(parameter_reference_rows(baseline)),
        hide_index=True,
        width="stretch",
    )
    if st.button("Eingaben neu pruefen", key="ma_parameters_refresh_reference"):
        updated_payload = dict(payload)
        updated_payload["schema_version"] = "1.0"
        updated_payload["project_id"] = workspace.project.identity.project_id
        updated_payload["reference"] = {
            "snapshot_id": baseline.snapshot_id,
            "snapshot_version": baseline.snapshot_version,
            "content_hash": baseline.content_hash,
            "checked_at": datetime.now(UTC).isoformat(),
            "values": parameter_reference_rows(baseline),
        }
        updated_payload["dependent_results_status"] = "update_required"
        updated_payload["capacity_strategy"] = {
            "mode": selected_strategy,
            "dimensioning_status": "pending",
        }
        _synchronize_variation_specification(
            updated_payload,
            baseline,
            status="draft",
            study_contract=_project_study_contract(workspace, updated_payload),
        )
        save_project_module_config(workspace, PARAMETER_MODULE_KEY, updated_payload)
        st.session_state["ma_ui_variants_update_required"] = True
        st.success("Der aktuelle Referenzstand wurde uebernommen; abhaengige Ergebnisse sind zu aktualisieren.")


def _render_rules_section(workspace, baseline, payload: dict[str, object]) -> None:
    rules = payload.get("rules", [])
    if not isinstance(rules, list):
        rules = []
    st.caption(
        "Regeln werden vor den konkreten Spannen definiert. Ein definierender Status macht "
        "die Regel fuer den angegebenen Geltungsbereich verbindlich."
    )
    if workspace.project.identity.title == "Masterarbeit-Analyse":
        st.markdown("##### Systemregel der SmallOffice-V1-Studie")
        st.dataframe(
            normalize_table_for_streamlit([SMALL_OFFICE_CAPACITY_COUPLING_RULE]),
            hide_index=True,
            width="stretch",
        )
        st.caption("Diese Regel wird vom Varianten- und Dimensionierungsmodul technisch erzwungen.")
    if rules:
        st.dataframe(normalize_table_for_streamlit(rules), hide_index=True, width="stretch")
    else:
        st.info("Noch keine projektbezogenen Regeln/Vorgaben gespeichert.")

    rule_id = st.text_input(
        "Regel-ID",
        key="ma_parameters_rule_id",
        on_change=_mark_parameters_draft,
    )
    title = st.text_input(
        "Bezeichnung",
        key="ma_parameters_rule_title",
        on_change=_mark_parameters_draft,
    )
    rule_type = st.selectbox(
        "Regeltyp",
        RULE_TYPE_OPTIONS,
        key="ma_parameters_rule_type",
        on_change=_mark_parameters_draft,
    )
    defining = st.checkbox(
        "Definierender Status",
        value=True,
        key="ma_parameters_rule_defining",
        on_change=_mark_parameters_draft,
    )
    scope_type = st.selectbox(
        "Geltungsstatus",
        RULE_SCOPE_OPTIONS,
        key="ma_parameters_rule_scope",
        on_change=_mark_parameters_draft,
    )
    scope_id = ""
    if scope_type == "study_direction":
        scope_id = st.selectbox(
            "StudyDirection",
            ("optimization", "sensitivity"),
            key="ma_parameters_rule_direction",
        )
    elif scope_type == "study_case":
        scope_id = st.text_input("StudyCase-ID", key="ma_parameters_rule_case")
    parent_rule = st.selectbox(
        "Ueberschreibt Regel",
        ("", *[str(rule.get("rule_id", "")) for rule in rules]),
        key="ma_parameters_parent_rule",
        help="Spezifischere Regeln ueberschreiben allgemeinere nur mit dieser Referenz.",
    )
    details = st.text_area("Regelinhalt/Begruendung", key="ma_parameters_rule_details")
    if st.button("Regel in Projekt speichern", key="ma_parameters_save_rule"):
        candidate = {
            "rule_id": rule_id.strip(),
            "title": title.strip(),
            "rule_type": rule_type,
            "defining": defining,
            "scope_type": scope_type,
            "scope_id": scope_id.strip(),
            "overrides_rule_id": parent_rule,
            "details": details.strip(),
        }
        test_payload = dict(payload)
        test_payload["reference"] = test_payload.get("reference") or {
            "snapshot_id": baseline.snapshot_id
        }
        test_payload["rules"] = [
            *[rule for rule in rules if rule.get("rule_id") != candidate["rule_id"]],
            candidate,
        ]
        errors = validate_parameter_project_payload(test_payload)
        if errors:
            for error in errors:
                st.error(error)
        else:
            test_payload["dependent_results_status"] = "update_required"
            _synchronize_variation_specification(
                test_payload,
                baseline,
                status="draft",
            )
            _save_parameter_payload(workspace, test_payload)
            st.session_state["ma_ui_variants_update_required"] = True
            clear_workspace_draft(st.session_state, PARAMETER_MODULE_KEY)
            st.success("Regel/Vorgabe wurde projektbezogen gespeichert.")


def _render_variation_section(workspace, baseline, payload: dict[str, object]) -> None:
    spans = payload.get("variation_spans", [])
    if not isinstance(spans, list):
        spans = []
    table_rows = variation_span_table_rows(baseline, spans)
    header_columns = st.columns((3, 1, 1, 1, 1))
    for column, label in zip(
        header_columns,
        ("Parameter", "Minimum", "Maximum", "Schritt", "Freigabe"),
        strict=True,
    ):
        column.markdown(f"**{label}**")

    candidates: list[dict[str, object]] = []
    for row in table_rows:
        parameter_key = str(row["parameter_key"])
        columns = st.columns((3, 1, 1, 1, 1))
        unit_suffix = f" [{row['unit']}]" if row["unit"] else ""
        columns[0].write(f"{row['label']} ({parameter_key}){unit_suffix}")
        minimum = columns[1].text_input(
            "Minimum",
            value=str(row["minimum"]),
            key=f"ma_parameters_span_{parameter_key}_minimum",
            label_visibility="collapsed",
            on_change=_mark_parameters_draft,
        )
        maximum = columns[2].text_input(
            "Maximum",
            value=str(row["maximum"]),
            key=f"ma_parameters_span_{parameter_key}_maximum",
            label_visibility="collapsed",
            on_change=_mark_parameters_draft,
        )
        step = columns[3].text_input(
            "Schritt",
            value=str(row["step"]),
            key=f"ma_parameters_span_{parameter_key}_step",
            label_visibility="collapsed",
            on_change=_mark_parameters_draft,
        )
        enabled = columns[4].checkbox(
            "Freigabe",
            value=bool(row["enabled"]),
            key=f"ma_parameters_span_{parameter_key}_enabled",
            label_visibility="collapsed",
            on_change=_mark_parameters_draft,
        )
        candidates.append(
            {
                "parameter_key": parameter_key,
                "label": row["label"],
                "unit": row["unit"],
                "reference_value": row["reference_value"],
                "enabled": enabled,
                "value_form": "Min/Max/Schritt" if enabled else "kein Wert",
                "minimum": minimum,
                "maximum": maximum,
                "step": step,
            }
        )

    if st.button("Variationsspanne in Projekt speichern", key="ma_parameters_save_span"):
        updated_payload = dict(payload)
        updated_payload["reference"] = updated_payload.get("reference") or {
            "snapshot_id": baseline.snapshot_id
        }
        candidate_keys = {candidate["parameter_key"] for candidate in candidates}
        updated_payload["variation_spans"] = [
            *candidates,
            *[
                span
                for span in spans
                if isinstance(span, dict) and span.get("parameter_key") not in candidate_keys
            ],
        ]
        updated_payload["dependent_results_status"] = "update_required"
        errors = validate_parameter_project_payload(updated_payload)
        if errors:
            for error in errors:
                st.error(error)
        else:
            _synchronize_variation_specification(
                updated_payload,
                baseline,
                status="draft",
            )
            _save_parameter_payload(workspace, updated_payload)
            st.session_state["ma_ui_variants_update_required"] = True
            clear_workspace_draft(st.session_state, PARAMETER_MODULE_KEY)
            st.success("Variationsspanne wurde gespeichert; Varianten muessen aktualisiert werden.")


def _variation_form_values(value_form: str, *, enabled: bool) -> dict[str, object]:
    if not enabled or value_form == "kein Wert":
        return {"values": []}
    if value_form == "Einzelwert":
        return {"value": st.number_input("Einzelwert", key="ma_parameters_single_value")}
    if value_form == "Min/Max/Schritt":
        columns = st.columns(3)
        return {
            "minimum": columns[0].number_input("Minimum", key="ma_parameters_minimum"),
            "maximum": columns[1].number_input("Maximum", key="ma_parameters_maximum"),
            "step": columns[2].number_input(
                "Schritt",
                min_value=0.0,
                key="ma_parameters_step",
            ),
        }
    if value_form == "explizite Liste":
        raw_values = st.text_input(
            "Werte, durch Komma getrennt",
            key="ma_parameters_explicit_values",
        )
        return {"values": [value.strip() for value in raw_values.split(",") if value.strip()]}
    if value_form == "gekoppelte Werte":
        return {
            "coupling_key": st.text_input("Kopplungs-ID", key="ma_parameters_coupling_key"),
            "values": st.text_input("Gekoppelte Werte", key="ma_parameters_coupled_values"),
        }
    return {
        "reference_option": st.text_input(
            "Referenzoptions-ID",
            key="ma_parameters_reference_option",
        )
    }


def _render_handover_section(workspace, baseline, payload: dict[str, object]) -> None:
    errors = validate_parameter_project_payload(payload)
    rules = payload.get("rules", [])
    spans = payload.get("variation_spans", [])
    st.dataframe(
        normalize_table_for_streamlit(
            [
                {"Pruefpunkt": "Baseline", "Wert": baseline.snapshot_id},
                {"Pruefpunkt": "Regeln/Vorgaben", "Wert": len(rules) if isinstance(rules, list) else 0},
                {
                    "Pruefpunkt": "Freigegebene Variationsspannen",
                    "Wert": (
                        sum(bool(span.get("enabled")) for span in spans)
                        if isinstance(spans, list)
                        else 0
                    ),
                },
                {
                    "Pruefpunkt": "Abhaengige Ergebnisse",
                    "Wert": payload.get("dependent_results_status", "noch nicht erzeugt"),
                },
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    if errors:
        for error in errors:
            st.error(error)
    else:
        st.success("Der aktuelle Parameterentwurf ist formal uebergabefaehig.")
    if st.button(
        "Vorschau erzeugen",
        disabled=bool(errors),
        key="ma_parameters_create_preview",
    ):
        st.session_state["ma_parameters_handover_preview"] = {
            "baseline_snapshot_id": baseline.snapshot_id,
            "rules": rules,
            "variation_spans": spans,
            "study_contract": _project_study_contract(workspace, payload),
        }
    preview = st.session_state.get("ma_parameters_handover_preview")
    if isinstance(preview, dict):
        st.json(preview)
    if st.button(
        "Variationsspezifikation speichern",
        disabled=bool(errors) or not isinstance(preview, dict),
        key="ma_parameters_save_specification",
    ):
        updated_payload = dict(payload)
        updated_payload["variation_specification"] = {
            "status": "current",
            "saved_at": datetime.now(UTC).isoformat(),
            **preview,
        }
        _synchronize_variation_specification(
            updated_payload,
            baseline,
            status="current",
            study_contract=preview.get("study_contract"),
        )
        updated_payload["dependent_results_status"] = "update_required"
        _save_parameter_payload(workspace, updated_payload)
        st.session_state["ma_ui_variants_update_required"] = True
        clear_workspace_draft(st.session_state, PARAMETER_MODULE_KEY)
        st.success("Die aktuelle Variationsspezifikation wurde projektbezogen gespeichert.")


def _save_parameter_payload(workspace, payload: dict[str, object]) -> None:
    payload["schema_version"] = "1.0"
    payload["project_id"] = workspace.project.identity.project_id
    save_project_module_config(workspace, PARAMETER_MODULE_KEY, payload)


def _mark_parameters_draft() -> None:
    mark_workspace_draft(st.session_state, PARAMETER_MODULE_KEY)


def _validate_numeric_span(
    span: dict[str, object],
    index: int,
    errors: list[str],
) -> None:
    try:
        minimum = float(span["minimum"])
        maximum = float(span["maximum"])
        step = float(span["step"])
    except (KeyError, TypeError, ValueError):
        errors.append(f"Variationsspanne {index} braucht numerische Min/Max/Schritt-Werte.")
        return
    if not all(math.isfinite(value) for value in (minimum, maximum, step)):
        errors.append(f"Variationsspanne {index} braucht endliche Min/Max/Schritt-Werte.")
    if minimum > maximum:
        errors.append(f"Variationsspanne {index}: Minimum darf Maximum nicht ueberschreiten.")
    if step <= 0:
        errors.append(f"Variationsspanne {index}: Schritt muss groesser als 0 sein.")


def _synchronize_variation_specification(
    payload: dict[str, object],
    baseline,
    *,
    status: str,
    study_contract: object | None = None,
) -> None:
    """Synchronisiert den Entwurf; nur der eigene Uebergabeschritt setzt ihn aktuell."""
    if status not in {"draft", "current"}:
        raise ValueError(f"Unbekannter Variationsspezifikationsstatus: {status}")
    if study_contract is None:
        stored = payload.get("variation_specification")
        study_contract = (
            stored.get("study_contract")
            if isinstance(stored, dict)
            else None
        )
    contract = {
        "baseline_snapshot_id": baseline.snapshot_id,
        "baseline_snapshot_version": baseline.snapshot_version,
        "baseline_content_hash": baseline.content_hash,
        "rules": payload.get("rules", []),
        "variation_spans": payload.get("variation_spans", []),
        "study_contract": study_contract,
    }
    payload["variation_specification"] = {
        "status": status,
        "source_fingerprint": variation_specification_source_fingerprint(
            baseline,
            rules=contract["rules"],
            variation_spans=contract["variation_spans"],
            study_contract=contract["study_contract"],
        ),
        "updated_at": datetime.now(UTC).isoformat(),
        **contract,
    }


def _project_study_contract(workspace, payload: dict[str, object] | None = None) -> dict[str, object] | None:
    if workspace.project.identity.title != "Masterarbeit-Analyse":
        return None
    capacity_state = payload.get("capacity_strategy", {}) if isinstance(payload, dict) else {}
    strategy = (
        str(capacity_state.get("mode"))
        if isinstance(capacity_state, dict) and capacity_state.get("mode") in CAPACITY_STRATEGY_OPTIONS
        else "dimensioned_with_factor"
    )
    return {
        "study_id": SMALL_OFFICE_V1_STUDY_ID,
        "enabled_dimensions": list(SMALL_OFFICE_V1_DIMENSIONS),
        "capacity_strategy": strategy,
        "approval_action": "Variationsspezifikation speichern",
    }


def _capacity_strategy_rows(workspace, strategy: str) -> list[dict[str, object]]:
    """Zeigt Referenzlasten erst nach ihrem getrennten Dimensionierungsschritt."""
    dimensioning = load_project_module_config(workspace, "ma_analyse_stage_1_dimensioning") or {}
    zone_loads = dimensioning.get("zone_loads", []) if isinstance(dimensioning, dict) else []
    valid_loads = [item for item in zone_loads if isinstance(item, dict)] if isinstance(zone_loads, list) else []
    if not valid_loads:
        reference = "Referenzdimensionierung ausstehend"
        heating = cooling = reference
    else:
        heating_total = sum(float(item.get("heating_load_w", 0.0)) for item in valid_loads)
        cooling_total = sum(float(item.get("cooling_load_w", 0.0)) for item in valid_loads)
        heating = f"{heating_total:,.2f} W".replace(",", "X").replace(".", ",").replace("X", ".")
        cooling = f"{cooling_total:,.2f} W".replace(",", "X").replace(".", ",").replace("X", ".")
    if strategy == "ideal_unlimited":
        return [
            {"Parameter": "Verfuegbare Heizleistung", "Wert": f"unbegrenzt ({heating})"},
            {"Parameter": "Verfuegbare Kuehlleistung", "Wert": f"unbegrenzt ({cooling})"},
        ]
    if strategy == "reference_dimensioned":
        return [
            {"Parameter": "Verfuegbare Heizleistung", "Wert": heating},
            {"Parameter": "Verfuegbare Kuehlleistung", "Wert": cooling},
        ]
    return [
        {"Parameter": "Leistungsbezug", "Wert": f"Referenzdimensionierung mit Leistungsfaktor ({heating}; {cooling})"}
    ]
