"""Navigation fuer die zentrale Streamlit-Oberflaeche."""

from __future__ import annotations

from dataclasses import dataclass

from ma_workflow import get_workflow_step

CURRENT_PAGE_SESSION_KEY = "ma_ui_current_page"


@dataclass(frozen=True, slots=True)
class NavigationPage:
    """Beschreibt eine Seite der zentralen lokalen UI."""

    page_key: str
    label: str
    module_key: str
    status: str


_PAGE_TO_WORKFLOW_STEP = {
    "parameters": "parameters",
    "weather": "weather",
    "building": "building",
    "variants": "variants",
    "simulation_setup": "simulation_setup",
    "export_ida": "ida_export",
    "import_ida": "ida_import",
    "analyse": "analyse",
    "assessment": "assessment",
    "feedback": "feedback",
}


def _workflow_status(page_key: str) -> str:
    """Leitet den Seitenstatus aus dem zentralen Workflow-Katalog ab."""
    step_key = _PAGE_TO_WORKFLOW_STEP.get(page_key)
    if step_key is None:
        return "available"
    return get_workflow_step(step_key).status


_NAVIGATION_PAGE_DEFINITIONS: tuple[tuple[str, str, str], ...] = (
    ("home", "Start", "project"),
    ("parameters", "Parameter", "ma_parameters"),
    ("weather", "Wetterdaten", "ma_weather"),
    ("building", "Gebaeude", "ma_building"),
    ("variants", "Varianten", "ma_variants"),
    ("simulation_setup", "Simulation Setup", "ma_simulation_setup"),
    ("export_ida", "IDA Export", "ma_export_ida"),
    ("import_ida", "IDA Import", "ma_import_ida"),
    ("analyse", "Analyse", "ma_analyse"),
    ("assessment", "Bewertung", "ma_assessment"),
    ("feedback", "Feedback", "ma_feedback"),
)

_NAVIGATION_PAGES: tuple[NavigationPage, ...] = tuple(
    NavigationPage(page_key, label, module_key, _workflow_status(page_key))
    for page_key, label, module_key in _NAVIGATION_PAGE_DEFINITIONS
)


def get_navigation_pages() -> tuple[NavigationPage, ...]:
    """Gibt die aktuell vorbereiteten UI-Seiten zurueck."""
    return _NAVIGATION_PAGES


def get_navigation_page(page_key: str) -> NavigationPage:
    """Findet eine UI-Seite ueber ihren technischen Key."""
    for page in _NAVIGATION_PAGES:
        if page.page_key == page_key:
            return page
    raise KeyError(f"Unbekannte UI-Seite: {page_key}")


def normalize_page_key(page_key: object, available_page_keys: tuple[str, ...]) -> str:
    """Normalisiert eine Session-State-Seite auf einen bekannten Zielwert."""
    if isinstance(page_key, str) and page_key in available_page_keys:
        return page_key
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
