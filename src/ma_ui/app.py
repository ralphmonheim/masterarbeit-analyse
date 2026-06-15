"""Startpunkt der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

import streamlit as st

from ma_ui.module_views import (
    analyse_view,
    assessment_view,
    building_view,
    export_ida_view,
    feedback_view,
    home_view,
    import_ida_view,
    parameters_view,
    simulation_setup_view,
    variants_view,
    weather_view,
)
from ma_ui.navigation import get_navigation_pages

CURRENT_PAGE_SESSION_KEY = "ma_ui_current_page"

_PAGE_RENDERERS = {
    "home": home_view.render,
    "parameters": parameters_view.render,
    "weather": weather_view.render,
    "building": building_view.render,
    "variants": variants_view.render,
    "simulation_setup": simulation_setup_view.render,
    "export_ida": export_ida_view.render,
    "import_ida": import_ida_view.render,
    "analyse": analyse_view.render,
    "assessment": assessment_view.render,
    "feedback": feedback_view.render,
}


def get_renderable_page_keys() -> tuple[str, ...]:
    """Gibt die aktuell aktiv gerenderten Seiten zurueck."""
    return tuple(_PAGE_RENDERERS)


def normalize_page_key(page_key: object, available_page_keys: tuple[str, ...]) -> str:
    """Normalisiert eine Session-State-Seite auf einen bekannten Zielwert."""
    if isinstance(page_key, str) and page_key in available_page_keys:
        return page_key
    return available_page_keys[0]


def main() -> None:
    """Startet die zentrale lokale Streamlit-App."""
    st.set_page_config(page_title="Masterarbeit", layout="wide")

    pages = get_navigation_pages()
    available_pages = [page for page in pages if page.page_key in _PAGE_RENDERERS]
    available_page_keys = tuple(page.page_key for page in available_pages)
    labels_by_key = {page.page_key: page.label for page in available_pages}
    current_page_key = normalize_page_key(st.session_state.get(CURRENT_PAGE_SESSION_KEY), available_page_keys)
    st.session_state[CURRENT_PAGE_SESSION_KEY] = current_page_key
    page_key = st.sidebar.radio(
        "Bereich",
        options=list(available_page_keys),
        index=available_page_keys.index(current_page_key),
        format_func=lambda key: labels_by_key[key],
    )
    if page_key != current_page_key:
        st.session_state[CURRENT_PAGE_SESSION_KEY] = page_key

    _PAGE_RENDERERS[page_key]()


if __name__ == "__main__":
    main()
