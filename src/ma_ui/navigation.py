"""Navigation fuer die zentrale Streamlit-Oberflaeche."""

from __future__ import annotations

from dataclasses import dataclass

CURRENT_PAGE_SESSION_KEY = "ma_ui_current_page"


@dataclass(frozen=True, slots=True)
class NavigationPage:
    """Beschreibt eine Seite der zentralen lokalen UI."""

    page_key: str
    label: str
    module_key: str
    status: str


_NAVIGATION_PAGES: tuple[NavigationPage, ...] = (
    NavigationPage("home", "Start", "project", "available"),
    NavigationPage("parameters", "Parameter", "ma_parameters", "planned"),
    NavigationPage("weather", "Wetterdaten", "ma_weather", "planned"),
    NavigationPage("building", "Gebaeude", "ma_building", "planned"),
    NavigationPage("variants", "Varianten", "ma_variants", "partial"),
    NavigationPage("simulation_setup", "Simulation Setup", "ma_simulation_setup", "planned"),
    NavigationPage("export_ida", "IDA Export", "ma_export_ida", "planned"),
    NavigationPage("import_ida", "IDA Import", "ma_import_ida", "planned"),
    NavigationPage("analyse", "Analyse", "ma_analyse", "partial"),
    NavigationPage("assessment", "Bewertung", "ma_assessment", "planned"),
    NavigationPage("feedback", "Feedback", "ma_feedback", "planned"),
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
