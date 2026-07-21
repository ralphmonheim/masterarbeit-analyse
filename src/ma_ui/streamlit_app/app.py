"""Startpunkt der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from ma_ui.streamlit_app import workflow_view
from ma_ui.streamlit_app.module_views import (
    analyse_view,
    assessment_view,
    building_view,
    dimensioning_view,
    home_view,
    module_info_view,
    parameters_view,
    project_view,
    technical_view,
    variants_view,
    weather_view,
    zones_view,
)
from ma_ui.streamlit_app.navigation import (
    CURRENT_PAGE_SESSION_KEY,
    MODULE_INFO_PAGE_SESSION_KEY,
    VIEW_MODE_SESSION_KEY,
    WORKFLOW_VIEW_MODE,
    WORKSPACE_VIEW_MODE,
    NavigationPage,
    consume_scroll_to_top,
    get_navigation_page,
    get_navigation_pages,
    get_process_navigation_pages,
    next_page_key,
    normalize_page_key,
    normalize_view_mode,
    previous_page_key,
    select_page,
    select_view_mode,
    set_module_info_active,
)

_PAGE_RENDERERS = {
    "home": home_view.render,
    "project": project_view.render,
    "workflow": workflow_view.render,
    "building": building_view.render,
    "zones": zones_view.render,
    "technical": technical_view.render,
    "parameters": parameters_view.render,
    "dimensioning": dimensioning_view.render,
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


def _render_page(
    page: NavigationPage,
    *,
    show_module_info: bool = False,
    view_mode: str = WORKSPACE_VIEW_MODE,
) -> None:
    if view_mode == WORKFLOW_VIEW_MODE and page.page_key in {"home", "workflow"}:
        _render_workflow_page(page)
        return

    renderer = _PAGE_RENDERERS.get(page.page_key)
    if renderer is not None and not show_module_info:
        renderer()
        return
    module_info_view.render(page.module_key)


def _render_workflow_page(page: NavigationPage) -> None:
    """Zeigt eine praesentationsorientierte Modulansicht."""
    if page.page_key == "home":
        home_view.render()
        return
    if page.page_key == "workflow":
        workflow_view.render()
        return


def _navigate_to(page_key: str) -> None:
    """Setzt die aktive Seite und startet Streamlit neu."""
    select_page(st.session_state, page_key)
    st.rerun()


def _switch_start_view(page_key: str, view_mode: str) -> None:
    """Wechselt zwischen Bearbeitungsstart und Workflowstart."""
    select_view_mode(st.session_state, view_mode)
    select_page(st.session_state, page_key)
    st.rerun()


def _scroll_to_top_if_requested() -> None:
    """Springt nach einem Seitenwechsel einmalig an den Seitenanfang."""
    if not consume_scroll_to_top(st.session_state):
        return
    components.html(
        """
        <script>
        window.parent.scrollTo({ top: 0, left: 0, behavior: "auto" });
        </script>
        """,
        height=1,
    )


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
    process_pages: list[NavigationPage],
    *,
    show_module_info: bool,
    view_mode: str,
) -> None:
    """Zeigt die fachliche Navigation als Kopfzeile."""
    process_page_keys = tuple(page.page_key for page in process_pages)
    labels_by_key = {page.page_key: page.label for page in available_pages}
    is_process_page = current_page_key in process_page_keys
    previous_key = previous_page_key(current_page_key, process_page_keys) if is_process_page else current_page_key
    next_key = next_page_key(current_page_key, process_page_keys) if is_process_page else current_page_key

    start_column, previous_column, next_column, label_column, info_column = st.columns([1, 1, 1, 5, 1.35])
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
        mode_text = "Praesentationsansicht" if view_mode == WORKFLOW_VIEW_MODE else "Bearbeitungsansicht"
        st.caption(f"Aktueller Bereich: {labels_by_key[current_page_key]} | {mode_text}")
    with info_column:
        if current_page_key == "home":
            if st.button("Workflow", width="stretch"):
                _switch_start_view("workflow", WORKFLOW_VIEW_MODE)
        elif current_page_key == "workflow":
            if st.button("Bearbeitung", width="stretch"):
                _switch_start_view("home", WORKSPACE_VIEW_MODE)
        else:
            has_view = has_module_view(current_page_key) and view_mode == WORKSPACE_VIEW_MODE
            button_label = "Modulansicht" if show_module_info else "Infokarte"
            if st.button(button_label, width="stretch", disabled=not has_view):
                _toggle_module_info(current_page_key, show_module_info=show_module_info)


def main() -> None:
    """Startet die zentrale lokale Streamlit-App."""
    st.set_page_config(page_title="Masterarbeit", layout="wide")

    pages = get_navigation_pages()
    available_pages = list(pages)
    process_pages = list(get_process_navigation_pages())
    available_page_keys = tuple(page.page_key for page in available_pages)
    current_page_key = normalize_page_key(st.session_state.get(CURRENT_PAGE_SESSION_KEY), available_page_keys)
    st.session_state[CURRENT_PAGE_SESSION_KEY] = current_page_key
    _scroll_to_top_if_requested()
    view_mode = normalize_view_mode(st.session_state.get(VIEW_MODE_SESSION_KEY))
    if current_page_key == "workflow":
        view_mode = WORKFLOW_VIEW_MODE
    elif current_page_key != "home":
        view_mode = WORKSPACE_VIEW_MODE
    st.session_state[VIEW_MODE_SESSION_KEY] = view_mode
    info_page_key = st.session_state.get(MODULE_INFO_PAGE_SESSION_KEY)
    if view_mode == WORKFLOW_VIEW_MODE or info_page_key != current_page_key:
        st.session_state.pop(MODULE_INFO_PAGE_SESSION_KEY, None)
        info_page_key = None
    show_module_info = is_module_info_active(current_page_key, info_page_key)
    _render_top_navigation(
        current_page_key,
        available_pages,
        process_pages,
        show_module_info=show_module_info,
        view_mode=view_mode,
    )

    _render_page(
        get_navigation_page(current_page_key),
        show_module_info=show_module_info,
        view_mode=view_mode,
    )


if __name__ == "__main__":
    main()
