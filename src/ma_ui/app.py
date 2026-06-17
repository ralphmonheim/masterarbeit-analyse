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
from ma_ui.navigation import (
    CURRENT_PAGE_SESSION_KEY,
    NavigationPage,
    get_navigation_pages,
    next_page_key,
    normalize_page_key,
    previous_page_key,
)

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


def _navigate_to(page_key: str) -> None:
    """Setzt die aktive Seite und startet Streamlit neu."""
    st.session_state[CURRENT_PAGE_SESSION_KEY] = page_key
    st.rerun()


def _render_top_navigation(current_page_key: str, available_pages: list[NavigationPage]) -> None:
    """Zeigt die fachliche Navigation als Kopfzeile."""
    available_page_keys = tuple(page.page_key for page in available_pages)
    labels_by_key = {page.page_key: page.label for page in available_pages}
    previous_key = previous_page_key(current_page_key, available_page_keys)
    next_key = next_page_key(current_page_key, available_page_keys)

    start_column, previous_column, next_column, label_column = st.columns([1, 1, 1, 5])
    with start_column:
        if st.button("Start", width="stretch", disabled=current_page_key == "home"):
            _navigate_to("home")
    with previous_column:
        if st.button("Zurueck", width="stretch", disabled=previous_key == current_page_key):
            _navigate_to(previous_key)
    with next_column:
        if st.button("Weiter", width="stretch", disabled=next_key == current_page_key):
            _navigate_to(next_key)
    with label_column:
        st.caption(f"Aktueller Bereich: {labels_by_key[current_page_key]}")


def main() -> None:
    """Startet die zentrale lokale Streamlit-App."""
    st.set_page_config(page_title="Masterarbeit", layout="wide")

    pages = get_navigation_pages()
    available_pages = [page for page in pages if page.page_key in _PAGE_RENDERERS]
    available_page_keys = tuple(page.page_key for page in available_pages)
    current_page_key = normalize_page_key(st.session_state.get(CURRENT_PAGE_SESSION_KEY), available_page_keys)
    st.session_state[CURRENT_PAGE_SESSION_KEY] = current_page_key
    _render_top_navigation(current_page_key, available_pages)

    _PAGE_RENDERERS[current_page_key]()


if __name__ == "__main__":
    main()
