"""Loganzeige fuer Streamlit-Views."""

from __future__ import annotations

import streamlit as st


def render_log(log_text: str, *, height: int = 280) -> None:
    """Zeigt Laufprotokolle kontrolliert an."""
    if log_text:
        st.text_area("Log", value=log_text, height=height)
