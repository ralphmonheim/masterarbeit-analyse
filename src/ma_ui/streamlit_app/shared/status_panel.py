"""Statusanzeige fuer Streamlit-Views."""

from __future__ import annotations

import streamlit as st


def render_status(message: str, *, status: str = "info") -> None:
    """Zeigt eine kurze Statusmeldung an."""
    if status == "success":
        st.success(message)
    elif status == "warning":
        st.warning(message)
    elif status == "error":
        st.error(message)
    else:
        st.info(message)
