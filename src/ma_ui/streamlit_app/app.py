"""Startpunkt der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

import streamlit as st

from ma_ui.streamlit_app.module_views import (
    analyse_view,
    assessment_view,
    home_view,
    module_info_view,
    parameters_view,
    project_view,
    variants_view,
    weather_view,
)
from ma_ui.streamlit_app.navigation import (
    CURRENT_PAGE_SESSION_KEY,
    MODULE_INFO_PAGE_SESSION_KEY,
    NavigationPage,
    get_navigation_page,
    get_navigation_pages,
    next_page_key,
    normalize_page_key,
    previous_page_key,
    select_page,
    set_module_info_active,
)

_PAGE_RENDERERS = {
    "home": home_view.render,
    "project": project_view.render,
    "parameters": parameters_view.render,
    "weather": weather_view.render,
    "variants": variants_view.render,
    "analyse": analyse_view.render,
    "assessment": assessment_view.render,
}


def get_renderable_page_keys() -> tuple[str, ...]:
    """Gibt die aktuell aktiv gerenderten Seiten zurueck."""
    return tuple(page.page_key for page in get_navigation_pages())


def has_module_view(page_key: str) -> bool:
    """Prueft, ob fuer eine Seite eine eigene Fachansicht registriert ist."""
    return page_key != "home" and page_key in _PAGE_RENDERERS


def is_module_info_active(current_page_key: str, info_page_key: object) -> bool:
    """Prueft den Infokartenmodus fuer die aktuelle Fachansicht."""
    return has_module_view(current_page_key) and info_page_key == current_page_key


def _render_page(page: NavigationPage, *, show_module_info: bool = False) -> None:
    renderer = _PAGE_RENDERERS.get(page.page_key)
    if renderer is not None and not show_module_info:
        renderer()
        return
    module_info_view.render(page.module_key)


def _navigate_to(page_key: str) -> None:
    """Setzt die aktive Seite und startet Streamlit neu."""
    select_page(st.session_state, page_key)
    st.rerun()


def _toggle_module_info(current_page_key: str, *, show_module_info: bool) -> None:
    """Schaltet fuer das aktuelle Modul zwischen Fachansicht und Infokarte."""
    set_module_info_active(
        st.session_state,
        current_page_key,
        active=not show_module_info,
    )
    st.rerun()


def _render_top_navigation(
    current_page_key: str,
    available_pages: list[NavigationPage],
    *,
    show_module_info: bool,
) -> None:
    """Zeigt die fachliche Navigation als Kopfzeile."""
    available_page_keys = tuple(page.page_key for page in available_pages)
    labels_by_key = {page.page_key: page.label for page in available_pages}
    previous_key = previous_page_key(current_page_key, available_page_keys)
    next_key = next_page_key(current_page_key, available_page_keys)

    start_column, previous_column, next_column, label_column, info_column = st.columns([1, 1, 1, 5, 1.25])
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
    with info_column:
        if current_page_key != "home":
            has_view = has_module_view(current_page_key)
            button_label = "Modulansicht" if show_module_info else "Infokarte"
            if st.button(button_label, width="stretch", disabled=not has_view):
                _toggle_module_info(current_page_key, show_module_info=show_module_info)


def main() -> None:
    """Startet die zentrale lokale Streamlit-App."""
    st.set_page_config(page_title="Masterarbeit", layout="wide")

    pages = get_navigation_pages()
    available_pages = list(pages)
    available_page_keys = tuple(page.page_key for page in available_pages)
    current_page_key = normalize_page_key(st.session_state.get(CURRENT_PAGE_SESSION_KEY), available_page_keys)
    st.session_state[CURRENT_PAGE_SESSION_KEY] = current_page_key
    info_page_key = st.session_state.get(MODULE_INFO_PAGE_SESSION_KEY)
    if info_page_key != current_page_key:
        st.session_state.pop(MODULE_INFO_PAGE_SESSION_KEY, None)
        info_page_key = None
    show_module_info = is_module_info_active(current_page_key, info_page_key)
    _render_top_navigation(
        current_page_key,
        available_pages,
        show_module_info=show_module_info,
    )

    _render_page(
        get_navigation_page(current_page_key),
        show_module_info=show_module_info,
    )


if __name__ == "__main__":
    main()
