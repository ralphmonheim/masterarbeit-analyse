"""Navigation fuer die zentrale Streamlit-Oberflaeche."""

from __future__ import annotations

from dataclasses import dataclass
from typing import MutableMapping

from ma_workflow import get_module_definition, list_module_definitions

CURRENT_PAGE_SESSION_KEY = "ma_ui_current_page"
MODULE_INFO_PAGE_SESSION_KEY = "ma_ui_module_info_page"
CONFIGURATION_RETURN_PAGE_SESSION_KEY = "ma_ui_configuration_return_page"
VIEW_MODE_SESSION_KEY = "ma_ui_view_mode"
SCROLL_TO_TOP_SESSION_KEY = "ma_ui_scroll_to_top"
WORKSPACE_VIEW_MODE = "workspace"
WORKFLOW_VIEW_MODE = "workflow"
VIEW_MODE_OPTIONS = (WORKSPACE_VIEW_MODE, WORKFLOW_VIEW_MODE)


def normalize_view_mode(view_mode: object) -> str:
    """Normalisiert den UI-Modus auf Workspace oder Workflow."""
    return str(view_mode) if view_mode in VIEW_MODE_OPTIONS else WORKSPACE_VIEW_MODE


def select_view_mode(session_state: MutableMapping[str, object], view_mode: str) -> None:
    """Wechselt zwischen Bearbeitungs- und Praesentationsansicht."""
    session_state[VIEW_MODE_SESSION_KEY] = normalize_view_mode(view_mode)
    session_state.pop(MODULE_INFO_PAGE_SESSION_KEY, None)


def toggle_view_mode(session_state: MutableMapping[str, object]) -> str:
    """Schaltet den aktuellen View-Modus um und gibt den neuen Modus zurueck."""
    current_view_mode = normalize_view_mode(session_state.get(VIEW_MODE_SESSION_KEY))
    next_view_mode = WORKFLOW_VIEW_MODE if current_view_mode == WORKSPACE_VIEW_MODE else WORKSPACE_VIEW_MODE
    select_view_mode(session_state, next_view_mode)
    return next_view_mode


def request_scroll_to_top(session_state: MutableMapping[str, object]) -> None:
    """Merkt vor, dass die naechste gerenderte Seite oben starten soll."""
    session_state[SCROLL_TO_TOP_SESSION_KEY] = True


def consume_scroll_to_top(session_state: MutableMapping[str, object]) -> bool:
    """Verbraucht eine vorgemerkte Scroll-Anforderung genau einmal."""
    return bool(session_state.pop(SCROLL_TO_TOP_SESSION_KEY, False))


def select_page(session_state: MutableMapping[str, object], page_key: str) -> None:
    """Waehlt eine Seite und beendet einen eventuell aktiven Infokartenmodus."""
    session_state.pop(MODULE_INFO_PAGE_SESSION_KEY, None)
    session_state.pop(CONFIGURATION_RETURN_PAGE_SESSION_KEY, None)
    session_state[CURRENT_PAGE_SESSION_KEY] = page_key
    request_scroll_to_top(session_state)


def select_related_configuration_page(
    session_state: MutableMapping[str, object],
    target_page_key: str,
    *,
    return_page_key: str,
) -> None:
    """Oeffnet eine Konfigurationsseite und merkt die fachliche Ausgangsseite."""
    session_state.pop(MODULE_INFO_PAGE_SESSION_KEY, None)
    session_state[CONFIGURATION_RETURN_PAGE_SESSION_KEY] = return_page_key
    session_state[CURRENT_PAGE_SESSION_KEY] = target_page_key
    request_scroll_to_top(session_state)


def return_to_configuration_origin(session_state: MutableMapping[str, object]) -> str | None:
    """Kehrt zur gemerkten Ausgangsseite zurueck und beendet den Kontext."""
    return_page_key = session_state.pop(CONFIGURATION_RETURN_PAGE_SESSION_KEY, None)
    if not isinstance(return_page_key, str):
        return None
    session_state.pop(MODULE_INFO_PAGE_SESSION_KEY, None)
    session_state[CURRENT_PAGE_SESSION_KEY] = return_page_key
    request_scroll_to_top(session_state)
    return return_page_key


def set_module_info_active(
    session_state: MutableMapping[str, object],
    page_key: str,
    *,
    active: bool,
) -> None:
    """Speichert oder beendet den Infokartenmodus fuer ein Modul."""
    if active:
        session_state[MODULE_INFO_PAGE_SESSION_KEY] = page_key
    else:
        session_state.pop(MODULE_INFO_PAGE_SESSION_KEY, None)


@dataclass(frozen=True, slots=True)
class NavigationPage:
    """Beschreibt eine Seite der zentralen lokalen UI."""

    page_key: str
    label: str
    module_key: str
    status: str


_PAGE_TO_WORKFLOW_STEP = {
    module.page_key: module.module_key for module in list_module_definitions()
}

PAGE_KEY_ALIASES = {
    "export_ida": "export_simulation",
    "import_ida": "import_simulation",
    "ida_export": "export_simulation",
    "ida_import": "import_simulation",
    "stage_2_optimization": "analyse",
    "stage_3_verification": "standards_compliance",
}


def _workflow_status(page_key: str) -> str:
    """Leitet den Seitenstatus aus dem zentralen Modulkatalog ab."""
    module_key = _PAGE_TO_WORKFLOW_STEP.get(page_key)
    if module_key is None:
        return "available"
    return get_module_definition(module_key).status


_NAVIGATION_PAGE_DEFINITIONS: tuple[tuple[str, str, str], ...] = (
    ("home", "Start", "project"),
    *tuple((module.page_key, module.label, module.module_key) for module in list_module_definitions()),
)

_NAVIGATION_PAGES: tuple[NavigationPage, ...] = tuple(
    NavigationPage(page_key, label, module_key, _workflow_status(page_key))
    for page_key, label, module_key in _NAVIGATION_PAGE_DEFINITIONS
)


def get_navigation_pages() -> tuple[NavigationPage, ...]:
    """Gibt die aktuell vorbereiteten UI-Seiten zurueck."""
    return _NAVIGATION_PAGES


def get_navigation_page(page_key: str) -> NavigationPage:
    """Findet eine UI-Seite einschliesslich historischer Seitenaliase."""
    canonical_key = PAGE_KEY_ALIASES.get(page_key, page_key)
    for page in _NAVIGATION_PAGES:
        if page.page_key == canonical_key:
            return page
    raise KeyError(f"Unbekannte UI-Seite: {page_key}")


def normalize_page_key(page_key: object, available_page_keys: tuple[str, ...]) -> str:
    """Normalisiert eine Session-State-Seite auf einen bekannten Zielwert."""
    if isinstance(page_key, str):
        canonical_key = PAGE_KEY_ALIASES.get(page_key, page_key)
        if canonical_key in available_page_keys:
            return canonical_key
    return available_page_keys[0]


def previous_page_key(page_key: str, available_page_keys: tuple[str, ...]) -> str:
    """Gibt die vorherige Seite in der fachlichen Workflow-Reihenfolge zurueck."""
    normalized_page_key = normalize_page_key(page_key, available_page_keys)
    current_index = available_page_keys.index(normalized_page_key)
    return available_page_keys[max(0, current_index - 1)]


def next_page_key(page_key: str, available_page_keys: tuple[str, ...]) -> str:
    """Gibt die naechste Seite in der fachlichen Workflow-Reihenfolge zurueck."""
    normalized_page_key = normalize_page_key(page_key, available_page_keys)
    current_index = available_page_keys.index(normalized_page_key)
    return available_page_keys[min(len(available_page_keys) - 1, current_index + 1)]
