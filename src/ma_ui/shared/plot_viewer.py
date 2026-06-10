"""Anzeigehelfer fuer vorhandene Plotdateien."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


def render_existing_image(path: Path, *, caption: str | None = None) -> None:
    """Zeigt ein Bild nur an, wenn die Datei lokal existiert."""
    if path.exists():
        st.image(str(path), caption=caption)
    else:
        st.warning(f"Bilddatei nicht gefunden: {path}")
