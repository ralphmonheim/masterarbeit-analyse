"""Fachansicht fuer Parameterdefinitionen und aktive Optionswerte."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from ma_parameters import (
    DEFAULT_OPTION_CONFIG,
    ParameterOptionSelection,
    apply_option_selection,
    list_local_option_files,
    load_parameter_catalog,
    save_option_selection,
    validate_option_selection,
)
from ma_ui.shared import (
    normalize_table_for_streamlit,
    render_configuration_links,
    render_configuration_return,
)
from ma_ui.state import build_current_variant_ui_data, get_configuration_state
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

    definition_tab, option_tab = st.tabs(["Parameterdefinitionen", "Optionsauswahl"])
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
