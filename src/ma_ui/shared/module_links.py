"""Kleine Navigationsbausteine fuer zusammenhaengende Fachansichten."""

from __future__ import annotations

import streamlit as st

from ma_ui.navigation import (
    CONFIGURATION_RETURN_PAGE_SESSION_KEY,
    return_to_configuration_origin,
    select_related_configuration_page,
)


def render_configuration_links(
    current_page_key: str,
    links: tuple[tuple[str, str], ...],
) -> None:
    """Zeigt fachliche Querverweise mit gezieltem Ruecksprung."""
    if not links:
        return
    columns = st.columns(len(links))
    for column, (label, target_page_key) in zip(columns, links, strict=True):
        with column:
            if st.button(label, key=f"p028_link_{current_page_key}_{target_page_key}", width="stretch"):
                select_related_configuration_page(
                    st.session_state,
                    target_page_key,
                    return_page_key=current_page_key,
                )
                st.rerun()


def render_configuration_return() -> None:
    """Zeigt den Ruecksprung nur innerhalb eines aktiven Konfigurationskontexts."""
    return_page_key = st.session_state.get(CONFIGURATION_RETURN_PAGE_SESSION_KEY)
    if not isinstance(return_page_key, str):
        return
    if st.button("Zur Ausgangsansicht zurueck", key="p028_return_to_origin"):
        return_to_configuration_origin(st.session_state)
        st.rerun()
