"""Lokaler Projektstart vor der fachlichen Bearbeitungsansicht."""

from __future__ import annotations

from datetime import UTC, datetime

import streamlit as st

from ma_project import (
    DEFAULT_SIMULATION_PROGRAM_CONFIG,
    Project,
    ProjectIdentity,
    ProjectInvestigation,
    ProjectLocation,
    load_simulation_program_profiles,
)
from ma_ui.native_dialogs import TkinterFolderDialogAdapter
from ma_ui.streamlit_app.navigation import select_page
from ma_ui.streamlit_app.state import (
    get_active_workspace,
    open_workspace_drafts,
    set_active_workspace,
)
from ma_workspace import (
    ProjectWorkspace,
    RegistryEntry,
    create_project_id,
    create_project_workspace_from_dialog,
    default_project_workspaces_directory,
    default_workspace_registry_file,
    known_v1_project_suggestions,
    load_project_workspace,
    load_workspace_registry,
    registry_entry_from_workspace,
    remove_registry_entry,
    upsert_registry_entry,
)

DEFAULT_PROJECTS_DIRECTORY = default_project_workspaces_directory()
DEFAULT_REGISTRY_FILE = default_workspace_registry_file()


def _known_workspaces() -> tuple[ProjectWorkspace, ...]:
    workspaces: list[ProjectWorkspace] = []
    for suggestion in known_v1_project_suggestions(DEFAULT_PROJECTS_DIRECTORY):
        if not suggestion.available:
            continue
        workspaces.append(load_project_workspace(suggestion.path))
    return tuple(workspaces)


def _registry_entries() -> tuple[RegistryEntry, ...]:
    try:
        entries = load_workspace_registry(DEFAULT_REGISTRY_FILE)
    except (OSError, ValueError) as exc:
        st.error(f"Lokale Projekt-Registry konnte nicht geladen werden: {exc}")
        return ()
    known_ids = {entry.project_id for entry in entries}
    known_entries = tuple(
        registry_entry_from_workspace(workspace)
        for workspace in _known_workspaces()
        if workspace.project.identity.project_id not in known_ids
    )
    return (*entries, *known_entries)


def _activate_workspace(workspace: ProjectWorkspace) -> None:
    active_workspace = get_active_workspace(st.session_state)
    open_drafts = open_workspace_drafts(st.session_state)
    if (
        active_workspace is not None
        and active_workspace.project.identity.project_id != workspace.project.identity.project_id
        and open_drafts
    ):
        raise ValueError(
            "Projektwechsel ist wegen offener Entwuerfe gesperrt: "
            f"{', '.join(open_drafts)}. Bitte im jeweiligen Modul speichern oder den Entwurf zuruecksetzen."
        )
    upsert_registry_entry(DEFAULT_REGISTRY_FILE, registry_entry_from_workspace(workspace))
    set_active_workspace(st.session_state, workspace)
    select_page(st.session_state, "project")
    st.rerun()


def _render_project_selection() -> None:
    entries = _registry_entries()
    available_entries = tuple(entry for entry in entries if entry.available)
    unavailable_entries = tuple(entry for entry in entries if not entry.available)

    st.subheader("Projekt auswählen")
    active_workspace = get_active_workspace(st.session_state)
    open_drafts = open_workspace_drafts(st.session_state)
    if active_workspace is not None and open_drafts:
        st.warning(
            "Offene Sitzungsentwuerfe: "
            f"{', '.join(open_drafts)}. Ein Wechsel in ein anderes Projekt ist bis zur Uebernahme gesperrt."
        )
    if available_entries:
        selected_id = st.selectbox(
            "Bekannte Projekte",
            [entry.project_id for entry in available_entries],
            format_func=lambda project_id: next(
                entry.name for entry in available_entries if entry.project_id == project_id
            ),
            key="project_start_known_project_id",
        )
        selected_entry = next(entry for entry in available_entries if entry.project_id == selected_id)
        st.caption(str(selected_entry.path))
        if st.button("Projekt auswählen", key="project_start_select"):
            try:
                _activate_workspace(load_project_workspace(selected_entry.path))
            except (OSError, ValueError) as exc:
                st.error(f"Projekt konnte nicht geöffnet werden: {exc}")
    else:
        st.info("Noch kein verfügbares lokales Projekt gefunden.")

    if st.button("Projekt importieren", key="project_start_import"):
        try:
            selected_folder = TkinterFolderDialogAdapter().choose_folder(initial_directory=DEFAULT_PROJECTS_DIRECTORY)
            if selected_folder is not None:
                _activate_workspace(load_project_workspace(selected_folder.resolve()))
        except Exception as exc:  # noqa: BLE001 - nativer Dialogfehler wird in der UI dargestellt.
            st.error(f"Projektimport konnte nicht abgeschlossen werden: {exc}")

    if unavailable_entries:
        with st.expander("Nicht verfügbare Projekte", expanded=False):
            for entry in unavailable_entries:
                st.warning(f"{entry.name}: {entry.path}")
                confirmed = st.checkbox(
                    f"Registry-Eintrag {entry.name} entfernen",
                    key=f"project_remove_confirm_{entry.project_id}",
                )
                if st.button(
                    "Eintrag entfernen",
                    key=f"project_remove_{entry.project_id}",
                    disabled=not confirmed,
                ):
                    remove_registry_entry(
                        DEFAULT_REGISTRY_FILE,
                        entry.project_id,
                        confirmed=confirmed,
                    )
                    st.rerun()


def _render_project_creation() -> None:
    programs, default_program_key, _source = load_simulation_program_profiles(
        DEFAULT_SIMULATION_PROGRAM_CONFIG,
        is_template=True,
    )
    program_keys = [program.program_key for program in programs]
    with st.form("project_start_create_form"):
        st.subheader("Projekt erstellen")
        project_name = st.text_input("Projektname")
        simulation_program_key = st.selectbox(
            "Simulationsprogramm",
            program_keys,
            index=program_keys.index(default_program_key),
            format_func=lambda key: next(program.display_name for program in programs if program.program_key == key),
        )
        country_code = st.text_input("Land (ISO-2)", value="DE", max_chars=2)
        city = st.text_input("Stadt")
        address = st.text_input("Adresse (optional)")
        submitted = st.form_submit_button("Projekt erstellen")

    if not submitted:
        return
    if open_workspace_drafts(st.session_state):
        st.error(
            "Ein neues Projekt kann erst nach Uebernahme oder Ruecksetzen "
            "der offenen Fachmodulentwuerfe angelegt werden."
        )
        return
    try:
        entries = _registry_entries()
        project_id = create_project_id([entry.project_id for entry in entries])
        timestamp = datetime.now(UTC)
        project = Project(
            identity=ProjectIdentity(
                project_id=project_id,
                title=project_name,
                short_name=project_name,
            ),
            created_at=timestamp,
            updated_at=timestamp,
            location=ProjectLocation(
                country_code=country_code.upper(),
                city=city,
                street=address,
            ),
            investigation=ProjectInvestigation(),
        )
        workspace = create_project_workspace_from_dialog(
            project,
            TkinterFolderDialogAdapter(),
            simulation_program_key=simulation_program_key,
            project_name=project_name,
            initial_directory=DEFAULT_PROJECTS_DIRECTORY,
        )
        if workspace is None:
            st.info("Projektanlage wurde ohne Änderungen abgebrochen.")
            return
        _activate_workspace(workspace)
    except Exception as exc:  # noqa: BLE001 - Validierung und nativer Dialog werden gemeinsam dargestellt.
        st.error(f"Projekt konnte nicht erstellt werden: {exc}")


def render() -> None:
    """Zeigt die Projektwahl als ersten Einstieg in die Bearbeitung."""
    st.title("Projektstart")
    active_workspace = get_active_workspace(st.session_state)
    if active_workspace is not None:
        st.info(
            f"Aktives Projekt: {active_workspace.project.identity.title}. "
            "Ein anderes Projekt wird erst nach ausdrücklicher Auswahl geöffnet."
        )

    sections = ("Projekt auswählen", "Projekt erstellen")
    section = st.segmented_control(
        "Einstieg",
        sections,
        default=sections[0],
        key="ma_project_start_section",
        selection_mode="single",
    )
    section = section or sections[0]
    if section == "Projekt auswählen":
        _render_project_selection()
    else:
        _render_project_creation()
