"""Projektbezogener Abschluss des V1-PreProcesses."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from time import perf_counter

import streamlit as st
import yaml

from ma_parameters import build_small_office_5z_v1_baseline_parameter_snapshot
from ma_simulation_setup import materialize_project_setup_packages
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_ui.streamlit_app.state import (
    get_active_workspace,
    small_office_v1_uses_reference_zone_model,
)
from ma_variants import load_selected_small_office_v1_study, small_office_source_fingerprint
from ma_workspace import load_project_module_config, save_project_module_config
from ma_zones import load_small_office_5z_endvariant_02_zone_spec

PROJECT_ROOT = Path(__file__).resolve().parents[4]


def simulation_setup_output_root(project_id: str, *, test_only: bool) -> Path:
    """Trennt isolierte Testlaeufe von regulaeren Projektartefakten."""
    root_name = "test_output" if test_only else "project_output"
    return PROJECT_ROOT / "data" / root_name / project_id / "simulation_setup"


def render() -> None:
    """Materialisiert nur bestaetigte, aktuelle Varianten bis Simulation-Setup."""
    render_page_header(
        "Simulation vorbereiten",
        "Bestaetigte Varianten als lokale Pakete fuer die manuelle Simulation vorbereiten",
    )
    st.info(
        "Der V1-PreProcess endet hier. Es wird keine Simulation gestartet und "
        "es werden keine Ergebnisse importiert oder ausgewertet."
    )
    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.warning("Bitte zuerst ein Projekt auswaehlen.")
        return
    if workspace.project.identity.title != "Masterarbeit-Analyse":
        st.info("Fuer dieses Demo-Projekt ist noch kein V1-Simulation-Setup definiert.")
        return
    try:
        variants_payload = load_project_module_config(workspace, "ma_variants") or {}
        parameter_payload = load_project_module_config(workspace, "ma_parameters") or {}
        dimensioning_payload = (
            load_project_module_config(workspace, "ma_analyse_stage_1_dimensioning") or {}
        )
        zone_payload = load_project_module_config(workspace, "ma_zones") or {}
        study = load_selected_small_office_v1_study(variants_payload)
        baseline = build_small_office_5z_v1_baseline_parameter_snapshot()
        zone_spec = load_small_office_5z_endvariant_02_zone_spec()
    except (OSError, ValueError, KeyError) as exc:
        st.error(f"Simulation-Setup konnte nicht vorbereitet werden: {exc}")
        return
    if (
        workspace.project.identity.title == "Masterarbeit-Analyse"
        and not small_office_v1_uses_reference_zone_model(zone_payload)
    ):
        st.error("Das aktive 29Z-Modell ist noch nicht weitergabefaehig.")
        return
    packages = variants_payload.get("variant_packages", [])
    source_fingerprint = str(variants_payload.get("source_fingerprint", ""))
    current_fingerprint = small_office_source_fingerprint(
        study,
        baseline,
        zone_spec,
        parameter_payload,
        dimensioning_payload,
    )
    if source_fingerprint != current_fingerprint:
        st.warning(
            "Parameter, Zonenmodell, Studienvertrag oder Referenzdimensionierung "
            "haben sich geaendert. Die Variantenpakete muessen neu erzeugt werden."
        )
        return
    status = variants_payload.get("status")
    if status != "packages_current" or not isinstance(packages, list) or not packages:
        st.warning(
            "Es liegen keine bestaetigten, aktuellen Variantenpakete vor. "
            "Bitte zuerst den Variantenablauf abschliessen."
        )
        return
    st.dataframe(
        normalize_table_for_streamlit(
            [
                {
                    "Varianten-ID": package.get("variant_id"),
                    "Name": package.get("variant_name"),
                    "StudyCase": package.get("study_case_id"),
                    "Status": package.get("status"),
                }
                for package in packages
                if isinstance(package, dict)
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    default_group = f"PREPROCESS-{datetime.now().astimezone():%Y%m%d-%H%M%S}"
    run_group_id = st.text_input(
        "Run-Gruppen-ID",
        value=default_group,
        key="ma_simulation_setup_run_group",
    )
    output_root = simulation_setup_output_root(
        workspace.project.identity.project_id,
        test_only=study.test_only,
    )
    st.caption(f"Ausgabe: {output_root / run_group_id}")
    if st.button(
        "Simulation-Setup-Pakete erzeugen",
        type="primary",
        key="ma_simulation_setup_materialize",
    ):
        started = perf_counter()
        technical_timings = [
            row for row in variants_payload.get("technical_timings", []) if isinstance(row, dict)
        ] if isinstance(variants_payload.get("technical_timings"), list) else []
        dimensioning_timing = dimensioning_payload.get("technical_timing")
        if isinstance(dimensioning_timing, dict):
            technical_timings.append(dimensioning_timing)
        try:
            paths = materialize_project_setup_packages(
                output_root=output_root,
                run_group_id=run_group_id,
                project_id=workspace.project.identity.project_id,
                simulation_program_key=workspace.settings.simulation_program_key,
                variant_packages=packages,
                source_fingerprint=current_fingerprint,
                study_label=study.label,
                test_only=study.test_only,
                technical_timings=technical_timings,
            )
            materialization_duration = round(perf_counter() - started, 6)
            timing_path = paths[0].parent / "timings.yaml"
            timing_payload = yaml.safe_load(timing_path.read_text(encoding="utf-8"))
            save_project_module_config(
                workspace,
                "ma_simulation_setup",
                {
                    "schema_version": "1.0",
                    "project_id": workspace.project.identity.project_id,
                    "run_group_id": run_group_id,
                    "source_fingerprint": current_fingerprint,
                    "status": "prepared",
                    "run_directories": [path.as_posix() for path in paths],
                    "automatic_simulation": False,
                    "technical_duration_seconds": materialization_duration,
                    "timing_log": timing_path.as_posix(),
                },
            )
        except (OSError, ValueError) as exc:
            st.error(f"Simulation-Setup konnte nicht erzeugt werden: {exc}")
        else:
            st.success(f"{len(paths)} Simulation-Setup-Pakete wurden vorbereitet.")
            if isinstance(timing_payload, dict) and isinstance(timing_payload.get("timings"), list):
                st.dataframe(
                    normalize_table_for_streamlit(timing_payload["timings"]),
                    hide_index=True,
                    width="stretch",
                )
