"""Kleine UI-Widgets ohne Fachlogik."""

from __future__ import annotations

import streamlit as st


def render_placeholder(message: str) -> None:
    """Zeigt einen neutralen Platzhalter fuer geplante Funktionen."""
    st.info(message)
