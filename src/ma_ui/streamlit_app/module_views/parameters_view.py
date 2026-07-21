"""Fachansicht fuer Parameterdefinitionen und aktive Optionswerte."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from ma_parameters import (
    DEFAULT_OPTION_CONFIG,
    ParameterOptionSelection,
    apply_option_selection,
    baseline_parameter_snapshot_reference_rows,
    baseline_parameter_snapshot_source_rows,
    baseline_parameter_snapshot_summary_rows,
    baseline_parameter_snapshot_value_rows,
    build_business_integration_lod1_baseline_parameter_snapshot,
    build_business_integration_lod1_parameter_input_package,
    build_business_integration_lod1_parameter_snapshot,
    list_local_option_files,
    load_parameter_catalog,
    load_reference_variation_specification,
    parameter_input_package_source_rows,
    parameter_input_package_summary_rows,
    parameter_input_package_value_rows,
    parameter_snapshot_source_rows,
    parameter_snapshot_summary_rows,
    parameter_snapshot_value_rows,
    save_option_selection,
    validate_baseline_parameter_snapshot,
    validate_option_selection,
    validate_parameter_input_package,
    validate_parameter_snapshot,
    variation_area_rows,
    variation_dimension_rows,
)
from ma_ui.streamlit_app.shared import (
    normalize_table_for_streamlit,
    render_configuration_links,
    render_configuration_return,
)
from ma_ui.streamlit_app.state import build_current_variant_ui_data, get_configuration_state
from ma_variants.ui import option_value_rows, parameter_rows


def _clear_option_widgets(option_set_keys: list[str]) -> None:
    for option_set_key in option_set_keys:
        st.session_state.pop(f"p028_options_{option_set_key}", None)


def _render_option_file_controls(state: object) -> None:
    local_files = list_local_option_files()
    choices = [DEFAULT_OPTION_CONFIG, *local_files]
    selected_path = st.selectbox(
        "Optionsauswahl laden",
        choices,
        format_func=lambda path: path.name,
        key="p028_option_load_path",
    )
    if st.button("Ausgewaehlte Optionsauswahl laden", key="p028_option_load"):
        is_template = Path(selected_path) == DEFAULT_OPTION_CONFIG
        parameters, option_sets, option_values, selection = load_parameter_catalog(
            option_config=selected_path,
            option_is_template=is_template,
        )
        state.parameters = parameters
        state.option_sets = option_sets
        state.option_values = option_values
        state.option_selection = selection
        _clear_option_widgets([option_set.option_set_key for option_set in option_sets])
        st.rerun()


def _render_save_controls(state: object, *, selection_is_valid: bool) -> None:
    st.markdown("##### Optionsauswahl speichern")
    new_name = st.text_input("Neuer Dateiname", key="p028_option_new_name")
    if st.button(
        "Als neue Datei speichern",
        key="p028_option_save_new",
        disabled=not selection_is_valid,
    ):
        try:
            result = save_option_selection(
                state.parameters,
                state.option_sets,
                state.option_values,
                state.option_selection,
                file_name=new_name,
            )
        except (ValueError, FileExistsError, PermissionError) as exc:
            st.error(str(exc))
        else:
            state.option_selection = ParameterOptionSelection(
                active_option_keys_by_set=state.option_selection.active_option_keys_by_set,
                source=type(state.option_selection.source)(path=result.path, is_template=False),
            )
            st.success(f"Gespeichert: {result.path}")

    if not state.option_selection.source.is_template:
        confirmed = st.checkbox(
            "Bestehende eigene Optionsauswahl wirklich ueberschreiben",
            key="p028_option_overwrite_confirmed",
        )
        if st.button(
            "Geladene eigene Datei ueberschreiben",
            key="p028_option_overwrite",
            disabled=not confirmed or not selection_is_valid,
        ):
            try:
                save_option_selection(
                    state.parameters,
                    state.option_sets,
                    state.option_values,
                    state.option_selection,
                    file_name=state.option_selection.source.path.name,
                    overwrite_existing=True,
                    overwrite_confirmed=confirmed,
                )
            except (ValueError, FileNotFoundError, PermissionError) as exc:
                st.error(str(exc))
            else:
                st.success("Eigene Optionsauswahl wurde ueberschrieben.")


def render() -> None:
    """Zeigt Definitionen schreibgeschuetzt und erlaubt die aktive Auswahl."""
    st.title("Parameter")
    st.caption("Schreibgeschuetzte Definitionen und aktive Optionswerte")
    render_configuration_return()
    render_configuration_links(
        "parameters",
        (
            ("Projekt und Benennung", "project"),
            ("Varianten pruefen", "variants"),
        ),
    )

    try:
        state = get_configuration_state(st.session_state)
    except Exception as exc:  # noqa: BLE001 - UI stellt Initialisierungsfehler dar.
        st.error(f"Demokonfiguration konnte nicht initialisiert werden: {exc}")
        return

    st.caption(
        f"Parameter-Vorlage: {state.parameter_source.path.as_posix()} | "
        f"Optionsquelle: {state.option_selection.source.path.as_posix()}"
    )
    _render_option_file_controls(state)

    (
        reference_dimensioning_tab,
        variations_tab,
        definition_tab,
        option_tab,
        snapshot_tab,
        input_package_tab,
        baseline_tab,
    ) = st.tabs(
        [
            "Referenzdimensionierung",
            "Variationen",
            "Parameterdefinitionen",
            "Optionsauswahl (Altbestand)",
            "LoD-1-Snapshot",
            "Eingangspaket",
            "Baseline v2",
        ]
    )
    try:
        reference_baseline = build_business_integration_lod1_baseline_parameter_snapshot()
        reference_specification = load_reference_variation_specification(reference_baseline)
    except (OSError, ValueError, KeyError) as exc:
        reference_baseline = None
        reference_specification = None
        st.error(f"Referenzkonfiguration konnte nicht geladen werden: {exc}")

    with reference_dimensioning_tab:
        st.caption("Freigegebene Referenzwerte je Eingabemodul. Der Sperrstatus steuert den Variantenraum.")
        if reference_specification is not None and reference_baseline is not None:
            st.dataframe(
                normalize_table_for_streamlit(variation_area_rows(reference_specification)),
                hide_index=True,
                width="stretch",
            )
            source_rows = baseline_parameter_snapshot_value_rows(reference_baseline)
            area_tabs = st.tabs([area.label for area in reference_specification.areas])
            module_by_area = {
                "weather": "ma_weather",
                "building": "ma_building",
                "technical": "ma_technical",
                "zones": "ma_zones",
            }
            for area, area_tab in zip(reference_specification.areas, area_tabs, strict=True):
                with area_tab:
                    st.dataframe(
                        normalize_table_for_streamlit(
                            [row for row in source_rows if row["Modul"] == module_by_area[area.module_key]]
                        ),
                        hide_index=True,
                        width="stretch",
                    )

    with variations_tab:
        st.caption("Nur nicht gesperrte Bereiche erzeugen Varianten. Gekoppelte Werte werden gemeinsam gefuehrt.")
        if reference_specification is not None:
            st.dataframe(
                normalize_table_for_streamlit(variation_dimension_rows(reference_specification)),
                hide_index=True,
                width="stretch",
            )
    with definition_tab:
        st.info("Parameterdefinitionen sind in diesem Umsetzungsschritt nicht bearbeitbar.")
        st.dataframe(
            normalize_table_for_streamlit(parameter_rows(state.parameters)),
            hide_index=True,
            width="stretch",
        )

    selection_is_valid = False
    with option_tab:
        selected_by_set: dict[str, tuple[str, ...]] = {}
        for option_set in state.option_sets:
            available_options = [
                option
                for option in state.option_values
                if option.option_set_key == option_set.option_set_key
            ]
            option_labels = {option.option_key: option.label for option in available_options}
            current_selection = [
                option_key
                for option_key in state.option_selection.active_option_keys_by_set.get(
                    option_set.option_set_key,
                    (),
                )
                if option_key in option_labels
            ]
            selected_keys = st.multiselect(
                option_set.display_name,
                list(option_labels),
                default=current_selection,
                format_func=lambda key, labels=option_labels: labels[key],
                key=f"p028_options_{option_set.option_set_key}",
                help=option_set.description,
            )
            selected_by_set[option_set.option_set_key] = tuple(selected_keys)

        edited_selection = ParameterOptionSelection(
            active_option_keys_by_set=selected_by_set,
            source=state.option_selection.source,
        )
        try:
            validate_option_selection(
                state.parameters,
                state.option_sets,
                state.option_values,
                edited_selection,
            )
        except ValueError as exc:
            st.error(str(exc))
        else:
            state.option_selection = edited_selection
            ui_data = build_current_variant_ui_data(state)
            selection_is_valid = True
            st.success(f"Die aktuelle Auswahl erzeugt {ui_data.theoretical_variant_count} Varianten.")

        st.dataframe(
            normalize_table_for_streamlit(
                option_value_rows(
                    state.option_sets,
                    apply_option_selection(
                        state.parameters,
                        state.option_sets,
                        state.option_values,
                        edited_selection,
                    )
                    if selection_is_valid
                    else state.option_values,
                )
            ),
            hide_index=True,
            width="stretch",
        )
        _render_save_controls(state, selection_is_valid=selection_is_valid)

    with snapshot_tab:
        st.info("Dieser Snapshot v1 buendelt die validierte BusinessIntegration-LoD-1-Eingabekette.")
        try:
            snapshot = build_business_integration_lod1_parameter_snapshot()
            validation_result = validate_parameter_snapshot(snapshot)
        except (OSError, ValueError) as exc:
            st.error(f"ParameterSnapshot konnte nicht erzeugt werden: {exc}")
        else:
            st.metric("Freigabestatus", validation_result.release_status.value)
            st.dataframe(
                normalize_table_for_streamlit(parameter_snapshot_summary_rows(snapshot)),
                hide_index=True,
                width="stretch",
            )
            value_tab, source_tab, message_tab = st.tabs(["Parameterwerte", "Quellen", "Validierung"])
            with value_tab:
                st.dataframe(
                    normalize_table_for_streamlit(parameter_snapshot_value_rows(snapshot)),
                    hide_index=True,
                    width="stretch",
                )
            with source_tab:
                st.dataframe(
                    normalize_table_for_streamlit(parameter_snapshot_source_rows(snapshot)),
                    hide_index=True,
                    width="stretch",
                )
            with message_tab:
                message_rows = [
                    {
                        "Schwere": message.severity.value,
                        "Code": message.code,
                        "Meldung": message.message,
                        "Fundstelle": message.location,
                    }
                    for message in validation_result.messages
                ]
                if message_rows:
                    st.dataframe(normalize_table_for_streamlit(message_rows), hide_index=True, width="stretch")
                else:
                    st.success("Keine Validierungsmeldungen.")

    with input_package_tab:
        st.info("P015-S3a prueft die LoD-1-Eingabekette mit aktiviertem Wetter-Default.")
        try:
            input_package = build_business_integration_lod1_parameter_input_package()
            input_package_validation = validate_parameter_input_package(input_package)
        except (OSError, ValueError, KeyError) as exc:
            st.error(f"Parameter-Eingangspaket konnte nicht erzeugt werden: {exc}")
        else:
            st.metric("Freigabestatus", input_package_validation.release_status.value)
            st.dataframe(
                normalize_table_for_streamlit(parameter_input_package_summary_rows(input_package)),
                hide_index=True,
                width="stretch",
            )
            value_tab, source_tab, message_tab = st.tabs(["Parameterwerte", "Quellen", "Validierung"])
            with value_tab:
                st.dataframe(
                    normalize_table_for_streamlit(parameter_input_package_value_rows(input_package)),
                    hide_index=True,
                    width="stretch",
                )
            with source_tab:
                st.dataframe(
                    normalize_table_for_streamlit(parameter_input_package_source_rows(input_package)),
                    hide_index=True,
                    width="stretch",
                )
            with message_tab:
                message_rows = [
                    {
                        "Schwere": message.severity.value,
                        "Code": message.code,
                        "Meldung": message.message,
                        "Fundstelle": message.location,
                    }
                    for message in input_package_validation.messages
                ]
                if message_rows:
                    st.dataframe(normalize_table_for_streamlit(message_rows), hide_index=True, width="stretch")
                else:
                    st.success("Keine Validierungsmeldungen.")

    with baseline_tab:
        st.info("P015-S2 leitet aus dem Snapshot v1 einen BaselineParameterSnapshot mit Scopes ab.")
        try:
            baseline_snapshot = build_business_integration_lod1_baseline_parameter_snapshot()
            baseline_validation = validate_baseline_parameter_snapshot(baseline_snapshot)
        except (OSError, ValueError) as exc:
            st.error(f"BaselineParameterSnapshot konnte nicht erzeugt werden: {exc}")
        else:
            st.metric("Freigabestatus", baseline_validation.release_status.value)
            st.dataframe(
                normalize_table_for_streamlit(baseline_parameter_snapshot_summary_rows(baseline_snapshot)),
                hide_index=True,
                width="stretch",
            )
            value_tab, source_tab, reference_tab, message_tab = st.tabs(
                ["Parameterwerte", "Quellen", "Referenzen", "Validierung"]
            )
            with value_tab:
                st.dataframe(
                    normalize_table_for_streamlit(baseline_parameter_snapshot_value_rows(baseline_snapshot)),
                    hide_index=True,
                    width="stretch",
                )
            with source_tab:
                st.dataframe(
                    normalize_table_for_streamlit(baseline_parameter_snapshot_source_rows(baseline_snapshot)),
                    hide_index=True,
                    width="stretch",
                )
            with reference_tab:
                st.dataframe(
                    normalize_table_for_streamlit(baseline_parameter_snapshot_reference_rows(baseline_snapshot)),
                    hide_index=True,
                    width="stretch",
                )
            with message_tab:
                message_rows = [
                    {
                        "Schwere": message.severity.value,
                        "Code": message.code,
                        "Meldung": message.message,
                        "Fundstelle": message.location,
                    }
                    for message in baseline_validation.messages
                ]
                if message_rows:
                    st.dataframe(normalize_table_for_streamlit(message_rows), hide_index=True, width="stretch")
                else:
                    st.success("Keine Validierungsmeldungen.")
