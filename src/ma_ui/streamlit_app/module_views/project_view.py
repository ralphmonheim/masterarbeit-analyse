"""Fachansicht fuer Simulationsprogramme und neutrale Variantennamen."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from ma_project import (
    DEFAULT_NAMING_CONFIG,
    DEFAULT_SIMULATION_PROGRAM_CONFIG,
    Project,
    ProjectIdentity,
    ProjectInvestigation,
    ProjectLocation,
    SimulationProgramProfile,
    VariantNamingPart,
    VariantNamingProfile,
    list_local_naming_files,
    list_local_simulation_program_files,
    load_simulation_program_profiles,
    load_variant_naming_profile,
    save_simulation_program_profiles,
    save_variant_naming_profile,
)
from ma_ui.streamlit_app.shared import (
    normalize_table_for_streamlit,
    render_configuration_links,
    render_configuration_return,
)
from ma_ui.streamlit_app.state import build_current_variant_ui_data, get_configuration_state
from ma_variants.ui import apply_naming_profile_to_ui_data, variant_rows

_PROJECT_OVERVIEW_DEMO = Project(
    identity=ProjectIdentity(
        project_id="PRJ-000001",
        title="V1-Demoprojekt",
        short_name="V1-Demo",
        project_type="Synthetischer Referenzfall",
    ),
    created_at=datetime(2026, 7, 18, tzinfo=UTC),
    updated_at=datetime(2026, 7, 18, tzinfo=UTC),
    location=ProjectLocation(country_code="DE", display_name="Synthetischer Referenzstandort"),
    investigation=ProjectInvestigation(
        objective="Nachvollziehbare V1-Konfiguration des Referenzfalls",
        scope="Lesende Projektübersicht, Simulationsprogramme und Varianten-Benennung",
    ),
)


def _source_label(path: Path, *, is_template: bool) -> str:
    source_type = "Vorlage" if is_template else "Eigene Datei"
    return f"{source_type}: {path.as_posix()}"


def _program_rows(programs: list[SimulationProgramProfile]) -> list[dict[str, str]]:
    return [
        {
            "program_key": program.program_key,
            "display_name": program.display_name,
            "version": program.version,
            "note": program.note,
        }
        for program in programs
    ]


def _programs_from_editor(editor_value: object) -> list[SimulationProgramProfile]:
    if not isinstance(editor_value, pd.DataFrame):
        raise ValueError("Programmtabelle konnte nicht ausgewertet werden.")
    programs: list[SimulationProgramProfile] = []
    for row in editor_value.to_dict("records"):
        if not any(str(value).strip() for value in row.values()):
            continue
        programs.append(
            SimulationProgramProfile(
                program_key=str(row.get("program_key", "")).strip(),
                display_name=str(row.get("display_name", "")).strip(),
                version=str(row.get("version", "")).strip(),
                note=str(row.get("note", "")).strip(),
            )
        )
    keys = [program.program_key for program in programs]
    if len(keys) != len(set(keys)):
        raise ValueError("Programmschluessel muessen eindeutig sein.")
    if not programs:
        raise ValueError("Mindestens ein Simulationsprogramm ist erforderlich.")
    return programs


def naming_token_rows(profile: VariantNamingProfile) -> list[dict[str, object]]:
    """Bereitet die geordnete Tokenstruktur fuer den Editor auf."""
    rows: list[dict[str, object]] = []
    for order, part in enumerate(profile.parts, start=1):
        for option_key, token in part.option_tokens.items():
            rows.append(
                {
                    "order": order,
                    "parameter_key": part.parameter_key,
                    "option_key": option_key,
                    "token": token,
                }
            )
    return rows


def naming_profile_from_rows(
    *,
    prefix: str,
    index_width: int,
    separator: str,
    include_index: bool,
    editor_value: object,
) -> VariantNamingProfile:
    """Erzeugt ein valides Benennungsprofil aus den sichtbaren Tabellenzeilen."""
    if not isinstance(editor_value, pd.DataFrame):
        raise ValueError("Token-Tabelle konnte nicht ausgewertet werden.")

    grouped: dict[tuple[int, str], dict[str, str]] = {}
    for raw_row in editor_value.to_dict("records"):
        parameter_key = str(raw_row.get("parameter_key", "")).strip()
        option_key = str(raw_row.get("option_key", "")).strip()
        token = str(raw_row.get("token", "")).strip()
        if not parameter_key and not option_key and not token:
            continue
        order = int(raw_row.get("order", 0))
        group_key = (order, parameter_key)
        option_tokens = grouped.setdefault(group_key, {})
        if option_key in option_tokens:
            raise ValueError(f"Optionswert '{option_key}' ist fuer '{parameter_key}' doppelt eingetragen.")
        option_tokens[option_key] = token

    parts = tuple(
        VariantNamingPart(parameter_key=parameter_key, option_tokens=option_tokens)
        for (_order, parameter_key), option_tokens in sorted(grouped.items())
    )
    return VariantNamingProfile(
        prefix=prefix.strip(),
        index_width=index_width,
        separator=separator,
        include_index=include_index,
        parts=parts,
    )


def project_overview_rows(project: Project, state: object) -> list[dict[str, str]]:
    """Provides a compact, read-only V1 project overview for the session."""
    identity = project.identity
    location = project.location
    investigation = project.investigation
    active_program = next(
        (program for program in state.simulation_programs if program.program_key == state.active_program_key),
        None,
    )
    return [
        {"Bereich": "Projekt", "Merkmal": "Projekt-ID", "Wert": identity.project_id},
        {"Bereich": "Projekt", "Merkmal": "Name", "Wert": identity.title},
        {"Bereich": "Projekt", "Merkmal": "Kurzname", "Wert": identity.short_name},
        {"Bereich": "Projekt", "Merkmal": "Projektart", "Wert": identity.project_type},
        {"Bereich": "Standort", "Merkmal": "Standort", "Wert": location.display_name if location else ""},
        {"Bereich": "Untersuchung", "Merkmal": "Ziel", "Wert": investigation.objective if investigation else ""},
        {
            "Bereich": "Sitzung",
            "Merkmal": "Aktives Simulationsprogramm",
            "Wert": active_program.display_name if active_program else "",
        },
        {"Bereich": "Sitzung", "Merkmal": "Benennungsprofil", "Wert": state.naming_profile.prefix},
    ]


def _render_project_overview(state: object) -> None:
    st.subheader("Projektstammdaten")
    st.dataframe(
        normalize_table_for_streamlit(project_overview_rows(_PROJECT_OVERVIEW_DEMO, state)),
        hide_index=True,
        width="stretch",
    )
    st.caption(
        "Die Übersicht zeigt einen synthetischen Referenzfall und den aktuellen Sitzungsstand. Änderungen werden hier nicht gespeichert."
    )


def _render_program_file_controls(state: object) -> None:
    local_files = list_local_simulation_program_files()
    choices = [DEFAULT_SIMULATION_PROGRAM_CONFIG, *local_files]
    selected_path = st.selectbox(
        "Programmliste laden",
        choices,
        format_func=lambda path: path.name,
        key="p028_program_load_path",
    )
    if st.button("Ausgewaehlte Programmliste laden", key="p028_program_load"):
        is_template = Path(selected_path) == DEFAULT_SIMULATION_PROGRAM_CONFIG
        programs, active_key, source = load_simulation_program_profiles(
            selected_path,
            is_template=is_template,
        )
        state.simulation_programs = programs
        state.active_program_key = active_key
        state.simulation_program_source = source
        st.session_state.pop("p028_program_editor", None)
        st.session_state.pop("p028_active_program_key", None)
        st.rerun()


def _render_program_save_controls(state: object) -> None:
    st.markdown("##### Programmliste speichern")
    new_name = st.text_input("Neuer Dateiname", key="p028_program_new_name")
    if st.button("Als neue Datei speichern", key="p028_program_save_new"):
        try:
            result = save_simulation_program_profiles(
                state.simulation_programs,
                state.active_program_key,
                file_name=new_name,
            )
        except (ValueError, FileExistsError, PermissionError) as exc:
            st.error(str(exc))
        else:
            state.simulation_program_source = type(state.simulation_program_source)(
                path=result.path,
                is_template=False,
            )
            st.success(f"Gespeichert: {result.path}")

    if not state.simulation_program_source.is_template:
        confirmed = st.checkbox(
            "Bestehende eigene Programmliste wirklich ueberschreiben",
            key="p028_program_overwrite_confirmed",
        )
        if st.button(
            "Geladene eigene Datei ueberschreiben",
            key="p028_program_overwrite",
            disabled=not confirmed,
        ):
            try:
                save_simulation_program_profiles(
                    state.simulation_programs,
                    state.active_program_key,
                    file_name=state.simulation_program_source.path.name,
                    source=state.simulation_program_source,
                    overwrite_existing=True,
                    overwrite_confirmed=confirmed,
                )
            except (ValueError, FileNotFoundError, PermissionError) as exc:
                st.error(str(exc))
            else:
                st.success("Eigene Programmliste wurde ueberschrieben.")


def _render_naming_file_controls(state: object) -> None:
    local_files = list_local_naming_files()
    choices = [DEFAULT_NAMING_CONFIG, *local_files]
    selected_path = st.selectbox(
        "Benennungsprofil laden",
        choices,
        format_func=lambda path: path.name,
        key="p028_naming_load_path",
    )
    if st.button("Ausgewaehltes Benennungsprofil laden", key="p028_naming_load"):
        is_template = Path(selected_path) == DEFAULT_NAMING_CONFIG
        profile, source = load_variant_naming_profile(selected_path, is_template=is_template)
        state.naming_profile = profile
        state.naming_source = source
        for widget_key in (
            "p028_naming_prefix",
            "p028_naming_include_index",
            "p028_naming_index_width",
            "p028_naming_separator",
            "p028_naming_token_editor",
        ):
            st.session_state.pop(widget_key, None)
        st.rerun()


def _render_naming_save_controls(state: object, *, profile_is_valid: bool) -> None:
    st.markdown("##### Benennungsprofil speichern")
    new_name = st.text_input("Neuer Dateiname", key="p028_naming_new_name")
    if st.button(
        "Als neue Datei speichern",
        key="p028_naming_save_new",
        disabled=not profile_is_valid,
    ):
        try:
            result = save_variant_naming_profile(
                state.naming_profile,
                file_name=new_name,
            )
        except (ValueError, FileExistsError, PermissionError) as exc:
            st.error(str(exc))
        else:
            state.naming_source = type(state.naming_source)(path=result.path, is_template=False)
            st.success(f"Gespeichert: {result.path}")

    if not state.naming_source.is_template:
        confirmed = st.checkbox(
            "Bestehendes eigenes Benennungsprofil wirklich ueberschreiben",
            key="p028_naming_overwrite_confirmed",
        )
        if st.button(
            "Geladene eigene Datei ueberschreiben",
            key="p028_naming_overwrite",
            disabled=not confirmed or not profile_is_valid,
        ):
            try:
                save_variant_naming_profile(
                    state.naming_profile,
                    file_name=state.naming_source.path.name,
                    source=state.naming_source,
                    overwrite_existing=True,
                    overwrite_confirmed=confirmed,
                )
            except (ValueError, FileNotFoundError, PermissionError) as exc:
                st.error(str(exc))
            else:
                st.success("Eigenes Benennungsprofil wurde ueberschrieben.")


def render() -> None:
    """Zeigt die erste Fachansicht des Projektmoduls."""
    st.title("Projekt")
    st.caption("Simulationsprogramme und neutrale Varianten-Benennungsprofile")
    render_configuration_return()
    render_configuration_links(
        "project",
        (
            ("Parameter konfigurieren", "parameters"),
            ("Varianten pruefen", "variants"),
        ),
    )

    try:
        state = get_configuration_state(st.session_state)
    except Exception as exc:  # noqa: BLE001 - UI stellt Initialisierungsfehler dar.
        st.error(f"Demokonfiguration konnte nicht initialisiert werden: {exc}")
        return

    overview_tab, program_tab, naming_tab = st.tabs(["Projektübersicht", "Simulationsprogramme", "Varianten-Benennung"])

    with overview_tab:
        _render_project_overview(state)

    with program_tab:
        st.caption(
            _source_label(
                state.simulation_program_source.path,
                is_template=state.simulation_program_source.is_template,
            )
        )
        _render_program_file_controls(state)
        edited_programs = st.data_editor(
            pd.DataFrame(_program_rows(state.simulation_programs)),
            num_rows="dynamic",
            hide_index=True,
            width="stretch",
            key="p028_program_editor",
        )
        try:
            programs = _programs_from_editor(edited_programs)
            program_keys = [program.program_key for program in programs]
            active_index = (
                program_keys.index(state.active_program_key) if state.active_program_key in program_keys else 0
            )
            active_program_key = st.selectbox(
                "Aktives Simulationsprogramm",
                program_keys,
                index=active_index,
                format_func=lambda key: next(
                    program.display_name for program in programs if program.program_key == key
                ),
                key="p028_active_program_key",
            )
        except (TypeError, ValueError) as exc:
            st.error(str(exc))
        else:
            state.simulation_programs = programs
            state.active_program_key = active_program_key
        st.info("Die Programmauswahl veraendert das neutrale Benennungsprofil nicht automatisch.")
        _render_program_save_controls(state)

    with naming_tab:
        st.caption(_source_label(state.naming_source.path, is_template=state.naming_source.is_template))
        _render_naming_file_controls(state)
        profile = state.naming_profile
        field_columns = st.columns(4)
        prefix = field_columns[0].text_input("Praefix", value=profile.prefix, key="p028_naming_prefix")
        include_index = field_columns[1].checkbox(
            "Index verwenden",
            value=profile.include_index,
            key="p028_naming_include_index",
        )
        index_width = field_columns[2].number_input(
            "Indexbreite",
            min_value=1,
            value=profile.index_width,
            step=1,
            key="p028_naming_index_width",
        )
        separator = field_columns[3].text_input(
            "Trennzeichen",
            value=profile.separator,
            key="p028_naming_separator",
        )
        token_editor = st.data_editor(
            pd.DataFrame(naming_token_rows(profile)),
            num_rows="dynamic",
            hide_index=True,
            width="stretch",
            key="p028_naming_token_editor",
        )

        profile_is_valid = False
        try:
            edited_profile = naming_profile_from_rows(
                prefix=prefix,
                index_width=int(index_width),
                separator=separator,
                include_index=include_index,
                editor_value=token_editor,
            )
            ui_data = build_current_variant_ui_data(state)
            named_ui_data = apply_naming_profile_to_ui_data(ui_data, edited_profile)
        except (TypeError, ValueError) as exc:
            st.error(f"Benennungsprofil ist nicht anwendbar: {exc}")
        else:
            state.naming_profile = edited_profile
            profile_is_valid = True
            st.success("Benennungsprofil ist vollstaendig und erzeugt eindeutige Namen.")
            st.dataframe(
                normalize_table_for_streamlit(variant_rows(named_ui_data.generated_variants[:8])),
                hide_index=True,
                width="stretch",
            )
        _render_naming_save_controls(state, profile_is_valid=profile_is_valid)
