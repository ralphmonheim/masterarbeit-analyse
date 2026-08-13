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
    simulation_setup_view,
    technical_view,
    variants_view,
    weather_view,
    workflow_help_view,
    zones_view,
)
from ma_ui.streamlit_app.navigation import (
    CURRENT_PAGE_SESSION_KEY,
    MODULE_INFO_PAGE_SESSION_KEY,
    VIEW_MODE_SESSION_KEY,
    WORKFLOW_HELP_PAGE_SESSION_KEY,
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
    set_workflow_help_active,
)
from ma_ui.streamlit_app.pages import home as workspace_overview_view

_PAGE_RENDERERS = {
    "home": home_view.render,
    "workspace": workspace_overview_view.render,
    "project": project_view.render,
    "workflow": workflow_view.render,
    "building": building_view.render,
    "zones": zones_view.render,
    "technical": technical_view.render,
    "parameters": parameters_view.render,
    "parameter_variations": parameters_view.render_variation,
    "dimensioning": dimensioning_view.render,
    "weather": weather_view.render,
    "variants": variants_view.render,
    "simulation_setup": simulation_setup_view.render,
    "analyse": analyse_view.render,
    "assessment": assessment_view.render,
}


def get_renderable_page_keys() -> tuple[str, ...]:
    """Gibt die aktuell aktiv gerenderten Seiten zurueck."""
    return tuple(page.page_key for page in get_navigation_pages())


def has_module_view(page_key: str) -> bool:
    """Prueft, ob fuer eine Seite eine eigene Fachansicht registriert ist."""
    return page_key not in {"home", "workspace"} and page_key in _PAGE_RENDERERS


def is_module_info_active(current_page_key: str, info_page_key: object) -> bool:
    """Prueft den Infokartenmodus fuer die aktuelle Fachansicht."""
    return has_module_view(current_page_key) and info_page_key == current_page_key


def is_workflow_help_active(current_page_key: str, help_page_key: object) -> bool:
    """Prüft den Ablaufhilfemodus für die aktuelle Fachansicht."""
    return has_module_view(current_page_key) and help_page_key == current_page_key


def _render_page(
    page: NavigationPage,
    *,
    show_module_info: bool = False,
    show_workflow_help: bool = False,
    view_mode: str = WORKSPACE_VIEW_MODE,
) -> None:
    if view_mode == WORKFLOW_VIEW_MODE and page.page_key in {"home", "workflow"}:
        _render_workflow_page(page)
        return

    if show_workflow_help:
        workflow_help_view.render(page.module_key)
        return
    renderer = _PAGE_RENDERERS.get(page.page_key)
    if renderer is not None and not show_module_info:
        renderer()
        return
    module_info_view.render(page.module_key)


def _render_workflow_page(page: NavigationPage) -> None:
    """Zeigt eine der beiden getrennten Einstiegsansichten."""
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
    """Schaltet die technische Modulinfo für das aktuelle Modul."""
    set_module_info_active(
        st.session_state,
        current_page_key,
        active=not show_module_info,
    )
    st.rerun()


def _toggle_workflow_help(current_page_key: str, *, show_workflow_help: bool) -> None:
    """Schaltet die fachliche Ablaufhilfe für das aktuelle Modul."""

    set_workflow_help_active(
        st.session_state,
        current_page_key,
        active=not show_workflow_help,
    )
    st.rerun()


def _render_top_navigation(
    current_page_key: str,
    available_pages: list[NavigationPage],
    process_pages: list[NavigationPage],
    *,
    show_module_info: bool,
    show_workflow_help: bool,
    view_mode: str,
) -> None:
    """Zeigt die fachliche Navigation als Kopfzeile."""
    process_page_keys = tuple(page.page_key for page in process_pages)
    labels_by_key = {page.page_key: page.label for page in available_pages}
    is_process_page = current_page_key in process_page_keys
    previous_key = previous_page_key(current_page_key, process_page_keys) if is_process_page else current_page_key
    next_key = next_page_key(current_page_key, process_page_keys) if is_process_page else current_page_key

    start_column, previous_column, next_column, label_column, technical_column, help_column = st.columns(
        [1, 1, 1, 4.3, 1.5, 1.5]
    )
    with start_column:
        if view_mode == WORKFLOW_VIEW_MODE and st.button("Start", width="stretch", disabled=current_page_key == "home"):
            _navigate_to("home")
    with previous_column:
        if st.button("Zurueck", width="stretch", disabled=previous_key == current_page_key):
            _navigate_to(previous_key)
    with next_column:
        if st.button("Weiter", width="stretch", disabled=next_key == current_page_key):
            _navigate_to(next_key)
    with label_column:
        mode_text = "Workflowansicht" if view_mode == WORKFLOW_VIEW_MODE else "Bearbeitungsansicht"
        st.caption(f"Aktueller Bereich: {labels_by_key[current_page_key]} | {mode_text}")
    with technical_column:
        if current_page_key == "workspace":
            if st.button("Workflow", width="stretch"):
                _switch_start_view("workflow", WORKFLOW_VIEW_MODE)
        elif current_page_key == "workflow":
            if st.button("Bearbeitung", width="stretch"):
                _switch_start_view("workspace", WORKSPACE_VIEW_MODE)
        else:
            has_view = has_module_view(current_page_key) and view_mode == WORKSPACE_VIEW_MODE
            button_label = "Zur Bearbeitung" if show_module_info else "Technische Modulinfo"
            if st.button(button_label, width="stretch", disabled=not has_view):
                _toggle_module_info(current_page_key, show_module_info=show_module_info)
    with help_column:
        if current_page_key not in {"workspace", "workflow", "home"}:
            has_view = has_module_view(current_page_key) and view_mode == WORKSPACE_VIEW_MODE
            button_label = "Zur Bearbeitung" if show_workflow_help else "Hilfe zum Ablauf"
            if st.button(button_label, width="stretch", disabled=not has_view):
                _toggle_workflow_help(current_page_key, show_workflow_help=show_workflow_help)


def main() -> None:
    """Startet die zentrale lokale Streamlit-App."""
    st.set_page_config(page_title="Masterarbeit", layout="wide")

    pages = get_navigation_pages()
    available_pages = list(pages)
    process_pages = list(get_process_navigation_pages())
    available_page_keys = tuple(page.page_key for page in available_pages)
    requested_page_key = st.session_state.get(CURRENT_PAGE_SESSION_KEY)
    current_page_key = normalize_page_key(requested_page_key, available_page_keys)
    if requested_page_key is None:
        current_page_key = "workspace"
    st.session_state[CURRENT_PAGE_SESSION_KEY] = current_page_key
    _scroll_to_top_if_requested()
    view_mode = normalize_view_mode(st.session_state.get(VIEW_MODE_SESSION_KEY))
    if current_page_key in {"home", "workflow"}:
        view_mode = WORKFLOW_VIEW_MODE
    elif current_page_key != "home":
        view_mode = WORKSPACE_VIEW_MODE
    st.session_state[VIEW_MODE_SESSION_KEY] = view_mode
    info_page_key = st.session_state.get(MODULE_INFO_PAGE_SESSION_KEY)
    help_page_key = st.session_state.get(WORKFLOW_HELP_PAGE_SESSION_KEY)
    if view_mode == WORKFLOW_VIEW_MODE or info_page_key != current_page_key:
        st.session_state.pop(MODULE_INFO_PAGE_SESSION_KEY, None)
        info_page_key = None
    if view_mode == WORKFLOW_VIEW_MODE or help_page_key != current_page_key:
        st.session_state.pop(WORKFLOW_HELP_PAGE_SESSION_KEY, None)
        help_page_key = None
    show_module_info = is_module_info_active(current_page_key, info_page_key)
    show_workflow_help = is_workflow_help_active(current_page_key, help_page_key)
    _render_top_navigation(
        current_page_key,
        available_pages,
        process_pages,
        show_module_info=show_module_info,
        show_workflow_help=show_workflow_help,
        view_mode=view_mode,
    )

    _render_page(
        get_navigation_page(current_page_key),
        show_module_info=show_module_info,
        show_workflow_help=show_workflow_help,
        view_mode=view_mode,
    )


if __name__ == "__main__":
    main()
