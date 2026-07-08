"""Fachansicht fuer die Referenzdimensionierung."""

from __future__ import annotations

import streamlit as st

from ma_analyse.stage_1_dimensioning import (
    dimensioning_message_rows,
    dimensioning_step_rows,
    dimensioning_summary_rows,
    run_business_integration_lod1_reference_dimensioning,
)
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_workflow import get_module_definition


def render() -> None:
    """Zeigt die LoD-1-Referenzdimensionierung mit Rechenweg."""
    module = get_module_definition("ma_analyse.stage_1_dimensioning")
    render_page_header(module.label, module.purpose)

    try:
        result = run_business_integration_lod1_reference_dimensioning()
    except (OSError, ValueError) as exc:
        st.error(f"Referenzdimensionierung konnte nicht ausgefuehrt werden: {exc}")
        return

    st.metric("Status", result.status.value)
    st.dataframe(normalize_table_for_streamlit(dimensioning_summary_rows(result)), hide_index=True, width="stretch")

    steps_tab, messages_tab, scope_tab = st.tabs(["Rechenweg", "Hinweise", "Einordnung"])
    with steps_tab:
        st.dataframe(normalize_table_for_streamlit(dimensioning_step_rows(result)), hide_index=True, width="stretch")
    with messages_tab:
        message_rows = dimensioning_message_rows(result)
        if message_rows:
            st.dataframe(normalize_table_for_streamlit(message_rows), hide_index=True, width="stretch")
        else:
            st.success("Keine Dimensionierungshinweise.")
    with scope_tab:
        st.markdown("- LoD-1-Naeherung aus validiertem ParameterSnapshot v1")
        st.markdown("- Keine normative Heizlast und keine dynamische Kuehllast")
        st.markdown("- Ergebnisse sind Startwerte fuer Folgeplanung und Variantenanbindung")
        st.info(module.next_step)
