"""Sitzungszustand fuer den aktiven lokalen Projekt-Workspace."""

from __future__ import annotations

from collections.abc import MutableMapping

from ma_workspace import ProjectWorkspace

ACTIVE_WORKSPACE_SESSION_KEY = "ma_ui_active_project_workspace"
OPEN_WORKSPACE_DRAFTS_SESSION_KEY = "ma_ui_open_workspace_drafts"


def get_active_workspace(session_state: MutableMapping[str, object]) -> ProjectWorkspace | None:
    workspace = session_state.get(ACTIVE_WORKSPACE_SESSION_KEY)
    return workspace if isinstance(workspace, ProjectWorkspace) else None


def set_active_workspace(
    session_state: MutableMapping[str, object],
    workspace: ProjectWorkspace,
) -> None:
    if not isinstance(workspace, ProjectWorkspace):
        raise TypeError("workspace muss ein ProjectWorkspace-Objekt sein.")
    session_state[ACTIVE_WORKSPACE_SESSION_KEY] = workspace


def mark_workspace_draft(
    session_state: MutableMapping[str, object],
    module_key: str,
) -> None:
    """Merkt einen ungespeicherten Fachmodulentwurf fuer den Projektwechsel."""
    drafts = session_state.get(OPEN_WORKSPACE_DRAFTS_SESSION_KEY)
    draft_keys = set(drafts) if isinstance(drafts, tuple | list | set) else set()
    draft_keys.add(module_key)
    session_state[OPEN_WORKSPACE_DRAFTS_SESSION_KEY] = tuple(sorted(draft_keys))


def clear_workspace_draft(
    session_state: MutableMapping[str, object],
    module_key: str,
) -> None:
    drafts = set(open_workspace_drafts(session_state))
    drafts.discard(module_key)
    session_state[OPEN_WORKSPACE_DRAFTS_SESSION_KEY] = tuple(sorted(drafts))


def open_workspace_drafts(
    session_state: MutableMapping[str, object],
) -> tuple[str, ...]:
    drafts = session_state.get(OPEN_WORKSPACE_DRAFTS_SESSION_KEY)
    if not isinstance(drafts, tuple | list | set):
        return ()
    return tuple(sorted(str(module_key) for module_key in drafts if str(module_key).strip()))


def small_office_v1_uses_reference_zone_model(
    zone_payload: dict[str, object],
) -> bool:
    """V1 ist bis zur spaeteren 29Z-Freigabe ausschliesslich an 5Z gebunden."""
    return zone_payload.get("active_model", "5Z") == "5Z"
