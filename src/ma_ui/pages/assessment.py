"""Bewertungs-Seite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import streamlit as st

from ma_ui.shared import normalize_table_for_streamlit
from ma_variants.economic_analysis import EconomicAssumptions, import_economic_assumptions

DEFAULT_ECONOMIC_CONFIG = Path("config/ma_variants/economic/example_economic_assumptions.yaml")


def economic_assumption_rows(assumptions: EconomicAssumptions) -> dict[str, list[dict[str, object]]]:
    """Bereitet generische Bewertungsannahmen fuer UI-Tabellen auf."""
    return {
        "system_costs": [asdict(cost) for cost in assumptions.generic_system_costs],
        "energy_prices": [asdict(price) for price in assumptions.energy_prices],
        "scenarios": [asdict(scenario) for scenario in assumptions.economic_scenarios],
    }


def render() -> None:
    """Zeigt vorbereitete Bewertungsannahmen ohne Variantenberechnung."""
    st.title("Bewertung")
    st.caption("Generische Kostenannahmen und Szenarien")
    st.info(
        "Diese Seite zeigt derzeit nur vorhandene Wirtschaftlichkeitsannahmen aus ma_variants. "
        "ma_economy, ma_sustainability und die zusammenfassende ma_assessment-Logik "
        "sind noch nicht als eigene Fachmodule umgesetzt."
    )

    assumptions, errors = import_economic_assumptions(DEFAULT_ECONOMIC_CONFIG)
    if errors:
        st.error("Bewertungsannahmen enthalten Fehler.")
        st.json(errors)

    rows = economic_assumption_rows(assumptions)
    metric_columns = st.columns(3)
    metric_columns[0].metric("Systemkosten", len(rows["system_costs"]))
    metric_columns[1].metric("Energiepreise", len(rows["energy_prices"]))
    metric_columns[2].metric("Szenarien", len(rows["scenarios"]))

    tabs = st.tabs(["Systemkosten", "Energiepreise", "Szenarien"])
    with tabs[0]:
        st.dataframe(normalize_table_for_streamlit(rows["system_costs"]), hide_index=True, width="stretch")
    with tabs[1]:
        st.dataframe(normalize_table_for_streamlit(rows["energy_prices"]), hide_index=True, width="stretch")
    with tabs[2]:
        st.dataframe(normalize_table_for_streamlit(rows["scenarios"]), hide_index=True, width="stretch")
