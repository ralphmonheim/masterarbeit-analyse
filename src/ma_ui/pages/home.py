"""Startseite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ma_ui.workflow_view import workflow_step_rows


def render() -> None:
    """Zeigt den aktuellen Gesamtworkflow als Einstiegspunkt."""
    st.title("Masterarbeit Workflow")
    st.caption("Varianten, Wetterdaten, Simulationsergebnisse und Bewertung.")

    st.dataframe(pd.DataFrame(workflow_step_rows()), hide_index=True, use_container_width=True)
