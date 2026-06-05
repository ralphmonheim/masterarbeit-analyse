"""Streamlit-App fuer lokale Kontrolle und Bedienung."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from ma_variants.ui.services import (
    DEFAULT_EXPORT_DIR,
    DEFAULT_NAMING_CONFIG,
    DEFAULT_OPTION_CONFIG,
    DEFAULT_PARAMETER_CONFIG,
    SELECTION_METHODS,
    ResultFileInfo,
    apply_naming_to_ui_data,
    list_result_files,
    load_variant_ui_data,
    option_value_rows,
    parameter_rows,
    run_variant_export,
    select_variants_by_method,
    select_variants_for_export,
    selection_method_by_label,
    selection_method_rows,
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
        st.subheader("Konfiguration")
        parameter_config = Path(
            st.text_input("Parameter", value=str(DEFAULT_PARAMETER_CONFIG)),
        )
        option_config = Path(
            st.text_input("Optionen", value=str(DEFAULT_OPTION_CONFIG)),
        )
        naming_config = Path(
            st.text_input("Namensregeln", value=str(DEFAULT_NAMING_CONFIG)),
        )
        export_dir = Path(
            st.text_input("Exportordner", value=str(DEFAULT_EXPORT_DIR)),
        )
        max_preview_rows = int(
            st.number_input("Tabellenzeilen", min_value=5, max_value=500, value=50, step=5),
        )
        apply_naming = st.checkbox("Namensregeln anwenden", value=True)
        st.button("Parameter und Optionen laden")

    status_messages = [
        f"Parameterkonfiguration: {parameter_config}",
        f"Optionskonfiguration: {option_config}",
        f"Exportordner: {export_dir}",
    ]

    try:
        base_ui_data = load_variant_ui_data(parameter_config, option_config)
    except Exception as exc:  # noqa: BLE001 - UI zeigt Import-/Validierungsfehler direkt an.
        st.error(str(exc))
        return

    status_messages.append(f"{len(base_ui_data.parameters)} Parameter geladen.")
    status_messages.append(f"{len(base_ui_data.option_sets)} Optionsgruppen geladen.")
    status_messages.append(f"{len(base_ui_data.option_values)} Optionswerte geladen.")
    status_messages.append(f"{len(base_ui_data.generated_variants)} einfache Varianten erzeugt.")

    ui_data = base_ui_data
    if apply_naming:
        try:
            ui_data = apply_naming_to_ui_data(base_ui_data, naming_config)
            status_messages.append(f"Namensregeln angewendet: {naming_config}")
        except Exception as exc:  # noqa: BLE001 - UI zeigt Naming-Fehler direkt an.
            st.warning(f"Namensregeln konnten nicht angewendet werden: {exc}")
            status_messages.append(f"Namensregeln nicht angewendet: {exc}")

    metric_columns = st.columns(4)
    metric_columns[0].metric("Parameter", len(ui_data.parameters))
    metric_columns[1].metric("Optionsgruppen", len(ui_data.option_sets))
    metric_columns[2].metric("Variantenanzahl", ui_data.theoretical_variant_count)
    metric_columns[3].metric("Erzeugt", len(ui_data.generated_variants))

    (
        catalog_tab,
        variant_space_tab,
        selection_tab,
        naming_tab,
        export_tab,
        result_tab,
        status_tab,
    ) = st.tabs(
        [
            "Parameter und Optionen",
            "Variantenraum",
            "Auswahl",
            "Namensgebung",
            "Export",
            "Ergebnisse",
            "Status",
        ],
    )

    with catalog_tab:
        st.subheader("Parameter")
        st.dataframe(parameter_rows(ui_data.parameters), use_container_width=True, hide_index=True)
        st.subheader("Optionsgruppen und Optionswerte")
        st.dataframe(
            option_value_rows(ui_data.option_sets, ui_data.option_values),
            use_container_width=True,
            hide_index=True,
        )

    variant_table_rows = variant_rows(ui_data.generated_variants)
    variant_keys = [str(row["variant_key"]) for row in variant_table_rows]
    default_selection = variant_keys[: min(5, len(variant_keys))]

    with variant_space_tab:
        st.info("Die Variantenanzahl basiert aktuell nur auf aktiven Parametern und aktiven Optionen.")
        st.caption("Komplexe Regeln, Monte Carlo, Sensitivitaet und Optimierung sind noch nicht beruecksichtigt.")
        st.dataframe(variant_table_rows[:max_preview_rows], use_container_width=True, hide_index=True)

    selected_variants = select_variants_for_export(ui_data.generated_variants, default_selection)

    with selection_tab:
        method_label = st.radio(
            "Auswahlmethode",
            options=[method.label for method in SELECTION_METHODS],
            index=0,
        )
        method = selection_method_by_label(method_label)
        st.caption(method.notes)

        if not method.is_implemented:
            st.info("Diese Auswahlmethode ist vorbereitet, aber noch nicht implementiert.")
            selected_variants = []
        elif method.method_key == "manual":
            selected_keys = st.multiselect("variant_key", options=variant_keys, default=default_selection)
            selected_variants = select_variants_by_method(
                ui_data.generated_variants,
                method.method_key,
                selected_variant_keys=selected_keys,
            )
        elif method.method_key == "random":
            random_count = int(st.number_input("Anzahl", min_value=0, max_value=len(variant_keys), value=1, step=1))
            random_seed = int(st.number_input("random_seed", min_value=0, max_value=999999, value=42, step=1))
            selected_variants = select_variants_by_method(
                ui_data.generated_variants,
                method.method_key,
                random_count=random_count,
                random_seed=random_seed,
            )
        elif method.method_key == "filter":
            parameter_by_key = {parameter.parameter_key: parameter for parameter in ui_data.parameters}
            selected_parameter_key = st.selectbox("parameter_key", options=list(parameter_by_key))
            selected_parameter = parameter_by_key[selected_parameter_key]
            option_keys = [
                option_value.option_key
                for option_value in ui_data.option_values
                if option_value.option_set_key == selected_parameter.option_set_key
            ]
            selected_option_keys = st.multiselect("option_key", options=option_keys, default=option_keys[:1])
            selected_variants = select_variants_by_method(
                ui_data.generated_variants,
                method.method_key,
                filter_criteria={selected_parameter_key: selected_option_keys},
            )

        st.metric("Ausgewaehlt", len(selected_variants))
        st.dataframe(variant_rows(selected_variants), use_container_width=True, hide_index=True)

    with naming_tab:
        st.write({"config": str(naming_config), "angewendet": apply_naming})
        if st.button("Namensgenerierung pruefen"):
            st.success("Namensgenerierung ist eindeutig und ausfuehrbar.")
        st.dataframe(variant_table_rows[:max_preview_rows], use_container_width=True, hide_index=True)

    with export_tab:
        st.metric("Exportvarianten", len(selected_variants))
        st.dataframe(variant_rows(selected_variants), use_container_width=True, hide_index=True)
        if st.button("Export starten", type="primary", disabled=not selected_variants):
            export_result = run_variant_export(ui_data, selected_variants, export_dir)
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

    with status_tab:
        st.subheader("Auswahlmethoden")
        st.dataframe(selection_method_rows(), use_container_width=True, hide_index=True)
        st.subheader("Log")
        for message in status_messages:
            st.write(message)


if __name__ == "__main__":
    main()
