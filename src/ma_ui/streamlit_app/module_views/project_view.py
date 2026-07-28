"""Fachansicht fuer Simulationsprogramme und neutrale Variantennamen."""

from __future__ import annotations

from dataclasses import replace
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
    render_configuration_return,
)
from ma_ui.streamlit_app.state import (
    build_current_variant_ui_data,
    get_active_workspace,
    get_configuration_state,
    set_active_workspace,
)
from ma_variants.ui import apply_naming_profile_to_ui_data, variant_rows
from ma_workspace import (
    ProjectWorkspace,
    list_gallery_images,
    remove_gallery_image,
    save_gallery_image,
    save_project_workspace,
)

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


def _render_workspace_overview(workspace: ProjectWorkspace) -> None:
    project = workspace.project
    identity = project.identity
    location = project.location or ProjectLocation(country_code="DE", city="Unbekannt")
    investigation = project.investigation or ProjectInvestigation()

    with st.form("project_workspace_overview"):
        st.text_input("Projekt-ID", value=identity.project_id, disabled=True)
        st.text_input(
            "Projektname",
            value=identity.title,
            disabled=True,
            help="Der Projektname entspricht in V1 dem lokalen Projektordner.",
        )
        short_name = st.text_input("Kurzname", value=identity.short_name)
        description = st.text_area("Beschreibung", value=identity.description)
        investigation_scope = st.text_area("Untersuchungsrahmen", value=investigation.scope)
        country_code = st.text_input("Land (ISO-2)", value=location.country_code, max_chars=2)
        city = st.text_input("Stadt", value=location.city)
        address = st.text_input("Adresse (optional)", value=location.street)
        submitted = st.form_submit_button("Projektdaten speichern")

    if not submitted:
        return
    try:
        updated_project = replace(
            project,
            identity=replace(
                identity,
                short_name=short_name,
                description=description,
            ),
            location=replace(
                location,
                country_code=country_code.upper(),
                display_name=city,
                city=city,
                street=address,
            ),
            investigation=replace(investigation, scope=investigation_scope),
            updated_at=datetime.now(UTC),
        )
        updated_workspace = replace(workspace, project=updated_project)
        save_project_workspace(updated_workspace)
    except (OSError, TypeError, ValueError) as exc:
        st.error(f"Projektdaten konnten nicht gespeichert werden: {exc}")
    else:
        set_active_workspace(st.session_state, updated_workspace)
        st.success("Projektdaten wurden gespeichert.")


def _render_workspace_program(workspace: ProjectWorkspace) -> None:
    programs, default_key, _source = load_simulation_program_profiles(
        DEFAULT_SIMULATION_PROGRAM_CONFIG,
        is_template=True,
    )
    program_keys = [program.program_key for program in programs]
    current_key = workspace.settings.simulation_program_key
    selected_key = st.selectbox(
        "Simulationsprogramm",
        program_keys,
        index=program_keys.index(current_key) if current_key in program_keys else program_keys.index(default_key),
        format_func=lambda key: next(program.display_name for program in programs if program.program_key == key),
        key="project_workspace_program_key",
    )
    selected = next(program for program in programs if program.program_key == selected_key)
    st.dataframe(
        normalize_table_for_streamlit(_program_rows([selected])),
        hide_index=True,
        width="stretch",
    )
    if st.button("Simulationsprogramm übernehmen", key="project_workspace_apply_program"):
        updated_workspace = replace(
            workspace,
            settings=replace(workspace.settings, simulation_program_key=selected_key),
        )
        try:
            save_project_workspace(updated_workspace)
        except (OSError, ValueError) as exc:
            st.error(f"Simulationsprogramm konnte nicht gespeichert werden: {exc}")
        else:
            set_active_workspace(st.session_state, updated_workspace)
            st.success("Simulationsprogramm wurde übernommen.")


def _render_workspace_naming(workspace: ProjectWorkspace) -> None:
    choices = [DEFAULT_NAMING_CONFIG, *list_local_naming_files()]
    current_reference = workspace.settings.naming_profile_reference
    current_index = next(
        (
            index
            for index, path in enumerate(choices)
            if current_reference in {str(path), path.as_posix()}
        ),
        0,
    )
    selected_path = st.selectbox(
        "Naming-Regel",
        choices,
        index=current_index,
        format_func=lambda path: path.name,
        key="project_workspace_naming_path",
    )
    try:
        profile, _source = load_variant_naming_profile(
            selected_path,
            is_template=Path(selected_path) == DEFAULT_NAMING_CONFIG,
        )
        state = get_configuration_state(st.session_state)
        preview = apply_naming_profile_to_ui_data(build_current_variant_ui_data(state), profile)
    except (OSError, TypeError, ValueError) as exc:
        st.error(f"Naming-Vorschau konnte nicht erzeugt werden: {exc}")
        return
    st.caption("Vorschau; die Naming-Regel wird erst in ma_variants auf Varianten angewendet.")
    st.dataframe(
        normalize_table_for_streamlit(variant_rows(preview.generated_variants[:8])),
        hide_index=True,
        width="stretch",
    )
    if st.button("Naming-Regel übernehmen", key="project_workspace_apply_naming"):
        updated_workspace = replace(
            workspace,
            settings=replace(
                workspace.settings,
                naming_profile_reference=Path(selected_path).as_posix(),
            ),
        )
        try:
            save_project_workspace(updated_workspace)
        except (OSError, ValueError) as exc:
            st.error(f"Naming-Regel konnte nicht gespeichert werden: {exc}")
        else:
            set_active_workspace(st.session_state, updated_workspace)
            st.success("Naming-Regel wurde übernommen.")


def _render_workspace_gallery(workspace: ProjectWorkspace) -> None:
    list_column, preview_column = st.columns([1, 2])
    images = list_gallery_images(workspace)
    with list_column:
        uploaded_file = st.file_uploader(
            "Eigene Bilder",
            type=["png", "jpg", "jpeg", "webp"],
            key="project_gallery_upload",
        )
        if st.button(
            "Bilder hochladen",
            key="project_gallery_upload_button",
            disabled=uploaded_file is None,
        ):
            try:
                save_gallery_image(workspace, uploaded_file.name, uploaded_file.getvalue())
            except (OSError, ValueError) as exc:
                st.error(f"Bild konnte nicht gespeichert werden: {exc}")
            else:
                st.rerun()
        if images:
            selected_name = st.radio(
                "Projektbilder",
                [path.name for path in images],
                key="project_gallery_selected_image",
            )
            confirmed = st.checkbox(
                "Ausgewähltes Bild wirklich entfernen",
                key="project_gallery_remove_confirmed",
            )
            if st.button(
                "Bild entfernen",
                key="project_gallery_remove",
                disabled=not confirmed,
            ):
                try:
                    remove_gallery_image(workspace, selected_name, confirmed=confirmed)
                except (OSError, ValueError) as exc:
                    st.error(f"Bild konnte nicht entfernt werden: {exc}")
                else:
                    st.rerun()
        else:
            selected_name = None
            st.info("Noch keine eigenen Projektbilder vorhanden.")

    with preview_column:
        if selected_name is not None:
            selected_path = next(path for path in images if path.name == selected_name)
            st.image(str(selected_path), caption=selected_path.name, width="stretch")


def render() -> None:
    """Zeigt die reduzierte Projektbearbeitung des aktiven Workspaces."""
    st.title("Projekt")
    st.caption("Projektübersicht, Galerie und projektweite Auswahlprofile")
    render_configuration_return()

    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.warning("Bitte zuerst auf der Startseite ein Projekt auswählen oder erstellen.")
        return

    sections = ("Projektübersicht", "Galerie", "Simulationsprogramm", "Naming-Regeln")
    section = st.segmented_control(
        "Projektbereich",
        sections,
        default=sections[0],
        key="ma_project_workspace_section",
        selection_mode="single",
    )
    section = section or sections[0]
    if section == "Projektübersicht":
        _render_workspace_overview(workspace)
    elif section == "Galerie":
        _render_workspace_gallery(workspace)
    elif section == "Simulationsprogramm":
        _render_workspace_program(workspace)
    else:
        _render_workspace_naming(workspace)
