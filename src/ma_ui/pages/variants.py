"""Varianten-Seite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

import streamlit as st

from ma_ui.shared import (
    normalize_table_for_streamlit,
    render_configuration_links,
    render_configuration_return,
)
from ma_ui.state import build_current_variant_ui_data, get_configuration_state
from ma_variants.ui.services import (
    apply_naming_profile_to_ui_data,
    list_result_files,
    option_value_rows,
    parameter_rows,
    selection_method_rows,
    variant_rows,
)


def render() -> None:
    """Zeigt eine kompakte Uebersicht aus den vorhandenen ma_variants-Services."""
    st.title("Varianten")
    st.caption("Gemeinsamer Projekt-, Parameter- und Benennungsstand")
    render_configuration_return()
    render_configuration_links(
        "variants",
        (
            ("Projekt und Benennung", "project"),
            ("Parameter konfigurieren", "parameters"),
        ),
    )

    try:
        state = get_configuration_state(st.session_state)
        ui_data = build_current_variant_ui_data(state)
        ui_data = apply_naming_profile_to_ui_data(ui_data, state.naming_profile)
    except Exception as exc:  # noqa: BLE001 - UI zeigt Servicefehler als Status an.
        st.error(f"Variantendaten konnten nicht geladen werden: {exc}")
        return

    active_program = next(
        program
        for program in state.simulation_programs
        if program.program_key == state.active_program_key
    )
    st.info(
        f"Aktives Simulationsprogramm: {active_program.display_name} | "
        f"Optionsquelle: {state.option_selection.source.path.name} | "
        f"Benennungsquelle: {state.naming_source.path.name}"
    )

    metric_columns = st.columns(4)
    metric_columns[0].metric("Parameter", len(ui_data.parameters))
    metric_columns[1].metric("Optionsgruppen", len(ui_data.option_sets))
    metric_columns[2].metric("Optionswerte", len(ui_data.option_values))
    metric_columns[3].metric("Theoretische Varianten", ui_data.theoretical_variant_count)

    tabs = st.tabs(
        [
            "Parameter",
            "Optionen",
            "Varianten",
            "Benennung",
            "Auswahlmethoden",
            "Exportdateien",
        ]
    )

    with tabs[0]:
        st.dataframe(normalize_table_for_streamlit(parameter_rows(ui_data.parameters)), hide_index=True, width="stretch")

    with tabs[1]:
        st.dataframe(
            normalize_table_for_streamlit(option_value_rows(ui_data.option_sets, ui_data.option_values)),
            hide_index=True,
            width="stretch",
        )

    with tabs[2]:
        st.dataframe(
            normalize_table_for_streamlit(variant_rows(ui_data.generated_variants)),
            hide_index=True,
            width="stretch",
        )

    with tabs[3]:
        st.write(
            {
                "prefix": state.naming_profile.prefix,
                "include_index": state.naming_profile.include_index,
                "index_width": state.naming_profile.index_width,
                "separator": state.naming_profile.separator,
                "parameter_order": [
                    part.parameter_key for part in state.naming_profile.parts
                ],
            }
        )
        st.dataframe(
            normalize_table_for_streamlit(variant_rows(ui_data.generated_variants[:8])),
            hide_index=True,
            width="stretch",
        )

    with tabs[4]:
        st.dataframe(normalize_table_for_streamlit(selection_method_rows()), hide_index=True, width="stretch")

    with tabs[5]:
        rows = [
            {
                "Datei": result_file.file_name,
                "Pfad": str(result_file.path),
                "Groesse Byte": result_file.size_bytes,
                "Geaendert": result_file.modified_at,
            }
            for result_file in list_result_files()
        ]
        st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")
