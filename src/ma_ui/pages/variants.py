"""Varianten-Seite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

import streamlit as st

from ma_variants.ui.services import (
    list_result_files,
    load_variant_ui_data,
    option_value_rows,
    parameter_rows,
    selection_method_rows,
    variant_rows,
)


def render() -> None:
    """Zeigt eine kompakte Uebersicht aus den vorhandenen ma_variants-Services."""
    st.title("Varianten")
    st.caption("Parameter, Optionen, Variantenraum und vorhandene Exportdateien")

    try:
        ui_data = load_variant_ui_data()
    except Exception as exc:  # noqa: BLE001 - UI zeigt Servicefehler als Status an.
        st.error(f"Variantendaten konnten nicht geladen werden: {exc}")
        return

    metric_columns = st.columns(4)
    metric_columns[0].metric("Parameter", len(ui_data.parameters))
    metric_columns[1].metric("Optionsgruppen", len(ui_data.option_sets))
    metric_columns[2].metric("Optionswerte", len(ui_data.option_values))
    metric_columns[3].metric("Theoretische Varianten", ui_data.theoretical_variant_count)

    tabs = st.tabs(["Parameter", "Optionen", "Varianten", "Auswahlmethoden", "Exportdateien"])

    with tabs[0]:
        st.dataframe(parameter_rows(ui_data.parameters), hide_index=True, use_container_width=True)

    with tabs[1]:
        st.dataframe(option_value_rows(ui_data.option_sets, ui_data.option_values), hide_index=True, use_container_width=True)

    with tabs[2]:
        st.dataframe(variant_rows(ui_data.generated_variants), hide_index=True, use_container_width=True)

    with tabs[3]:
        st.dataframe(selection_method_rows(), hide_index=True, use_container_width=True)

    with tabs[4]:
        rows = [
            {
                "Datei": result_file.file_name,
                "Pfad": str(result_file.path),
                "Groesse Byte": result_file.size_bytes,
                "Geaendert": result_file.modified_at,
            }
            for result_file in list_result_files()
        ]
        st.dataframe(rows, hide_index=True, use_container_width=True)
