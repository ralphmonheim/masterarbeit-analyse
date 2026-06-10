"""Layout-Helfer fuer die zentrale Streamlit-Oberflaeche."""

from __future__ import annotations

import streamlit as st


def render_page_header(title: str, caption: str | None = None) -> None:
    """Zeigt einen konsistenten Seitenkopf an."""
    st.title(title)
    if caption:
        st.caption(caption)
