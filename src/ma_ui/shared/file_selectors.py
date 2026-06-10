"""Einfache Dateipfad-Eingaben fuer Streamlit-Views."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


def path_text_input(label: str, default: str) -> Path:
    """Liest einen Pfad als Textfeld und gibt ihn als Path zurueck."""
    return Path(st.text_input(label, value=default))
