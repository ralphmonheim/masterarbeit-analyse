"""Streamlit-App fuer lokale Kontrolle und Bedienung."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from ma_variants.ui.services import (
    DEFAULT_EXPORT_DIR,
    DEFAULT_OPTION_CONFIG,
    DEFAULT_PARAMETER_CONFIG,
    ResultFileInfo,
    list_result_files,
    load_variant_ui_data,
    option_value_rows,
    parameter_rows,
    run_variant_export,
    select_variants_for_export,
    variant_rows,
)

PREVIEW_SUFFIXES = {".csv", ".json", ".md", ".txt"}


def _load_streamlit() -> Any:
    try:
        import streamlit as st
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Streamlit ist nicht installiert. Installiere die Projektabhaengigkeiten "
            "oder fuege Streamlit zur lokalen Umgebung hinzu."
        ) from exc
    return st


def _result_file_rows(result_files: list[ResultFileInfo]) -> list[dict[str, object]]:
    return [
        {
            **asdict(result_file),
            "path": str(result_file.path),
        }
        for result_file in result_files
    ]


def _file_preview(path: Path, max_chars: int = 12000) -> str:
    if path.suffix.lower() not in PREVIEW_SUFFIXES:
        return ""
    text = path.read_text(encoding="utf-8")
    if len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}\n..."


def main() -> None:
    """Startet die lokale Streamlit-Oberflaeche."""
    st = _load_streamlit()
    st.set_page_config(page_title="IDA Varianten", layout="wide")

    st.title("IDA Varianten")

    with st.sidebar:
        parameter_config = Path(
            st.text_input("Parameter", value=str(DEFAULT_PARAMETER_CONFIG)),
        )
        option_config = Path(
            st.text_input("Optionen", value=str(DEFAULT_OPTION_CONFIG)),
        )
        export_dir = Path(
            st.text_input("Exportordner", value=str(DEFAULT_EXPORT_DIR)),
        )
        max_preview_rows = int(
            st.number_input("Tabellenzeilen", min_value=5, max_value=500, value=50, step=5),
        )

    try:
        ui_data = load_variant_ui_data(parameter_config, option_config)
    except Exception as exc:  # noqa: BLE001 - UI zeigt Import-/Validierungsfehler direkt an.
        st.error(str(exc))
        return

    metric_columns = st.columns(4)
    metric_columns[0].metric("Parameter", len(ui_data.parameters))
    metric_columns[1].metric("Optionswerte", len(ui_data.option_values))
    metric_columns[2].metric("Variantenanzahl", ui_data.theoretical_variant_count)
    metric_columns[3].metric("Erzeugt", len(ui_data.generated_variants))

    parameter_tab, option_tab, variant_tab, export_tab, result_tab = st.tabs(
        ["Parameter", "Optionen", "Varianten", "Export", "Ergebnisse"],
    )

    with parameter_tab:
        st.dataframe(parameter_rows(ui_data.parameters), use_container_width=True, hide_index=True)

    with option_tab:
        st.dataframe(
            option_value_rows(ui_data.option_sets, ui_data.option_values),
            use_container_width=True,
            hide_index=True,
        )

    variant_table_rows = variant_rows(ui_data.generated_variants)
    variant_keys = [str(row["variant_key"]) for row in variant_table_rows]
    default_selection = variant_keys[: min(5, len(variant_keys))]

    with variant_tab:
        st.dataframe(variant_table_rows[:max_preview_rows], use_container_width=True, hide_index=True)
        selected_keys = st.multiselect("Variantenauswahl", options=variant_keys, default=default_selection)
        selected_variants = select_variants_for_export(ui_data.generated_variants, selected_keys)
        st.metric("Ausgewaehlt", len(selected_variants))

    with export_tab:
        selected_keys_for_export = st.multiselect(
            "Exportauswahl",
            options=variant_keys,
            default=default_selection,
            key="export_selection",
        )
        selected_variants_for_export = select_variants_for_export(
            ui_data.generated_variants,
            selected_keys_for_export,
        )
        st.metric("Exportvarianten", len(selected_variants_for_export))
        if st.button("Export starten", type="primary", disabled=not selected_variants_for_export):
            export_result = run_variant_export(ui_data, selected_variants_for_export, export_dir)
            st.success("Export abgeschlossen")
            st.write(
                {
                    "json": str(export_result.json_path),
                    "csv": str(export_result.csv_path),
                    "report": str(export_result.report_path),
                }
            )

    with result_tab:
        result_files = list_result_files(export_dir)
        st.dataframe(_result_file_rows(result_files), use_container_width=True, hide_index=True)
        file_by_name = {result_file.file_name: result_file.path for result_file in result_files}
        if file_by_name:
            selected_file_name = st.selectbox("Datei", options=list(file_by_name), index=0)
            preview = _file_preview(file_by_name[selected_file_name])
            if preview:
                st.code(preview)
        else:
            st.info("Keine Ergebnisdateien vorhanden.")


if __name__ == "__main__":
    main()
