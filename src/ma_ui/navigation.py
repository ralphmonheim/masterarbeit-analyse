"""Navigation fuer die zentrale Streamlit-Oberflaeche."""

from __future__ import annotations

from dataclasses import dataclass

from ma_workflow import get_module_definition, list_module_definitions

CURRENT_PAGE_SESSION_KEY = "ma_ui_current_page"


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
