"""Analyse-View fuer ma_analyse."""

from __future__ import annotations

from typing import Any, MutableMapping

import matplotlib.pyplot as plt
import streamlit as st

from ma_analyse.analysis.components.time_windows import MAX_CALENDAR_WEEK, MONTH_DAY_COUNTS, MONTH_NAMES
from ma_analyse.analysis.templates import (
    DEFAULT_OUTDOOR_COLUMN,
    DEFAULT_SETPOINT_MAX,
    DEFAULT_SETPOINT_MIN,
    DEFAULT_SHOW_OPERATIVE_TEMPERATURE,
    DEFAULT_SHOW_OUTDOOR_TEMPERATURE,
    DEFAULT_SHOW_SETPOINT_BAND,
    DEFAULT_TEMPERATURE_YMAX,
    DEFAULT_TEMPERATURE_YMIN,
    HEATING_YEAR_TEMPLATE,
    PLOT_TEMPLATE_CHOICES,
)
from ma_analyse.analysis_ui import (
    build_analysis_config,
    build_catalog_overlay_line,
    build_plot_template_options,
    build_template_time_options,
    first_selected_value,
    normalize_overlay_line,
    parse_overlay_lines_text,
    plot_template_requires_single_room,
    plot_template_supports_overlays,
    plot_template_view,
    split_csv_text,
)
from ma_analyse.analysis_ui import (
    coerce_bool_default as _default_bool,
)
from ma_analyse.analysis_ui import (
    coerce_float_default as _default_float,
)
from ma_analyse.analysis_ui import (
    coerce_text_default as _default_text,
)
from ma_analyse.analysis_ui import (
    default_fixed_overlays as _default_fixed_overlays,
)
from ma_analyse.analysis_wizard import (
    ANALYSIS_SCOPE_OPTIONS,
    ANALYSIS_SECTION_ORDER,
    AXIS_RANGE_MODE_OPTIONS,
    COMFORT_ANALYSIS_LEVEL_OPTIONS,
    COMFORT_SUBCOMMAND_OPTIONS,
    EXPORT_FORMAT_OPTIONS,
    LOAD_SUBCOMMAND_OPTIONS,
    LOAD_VIEW_OPTIONS,
    PLOT_TEMPLATE_MODE_OPTIONS,
    PLOT_TEMPLATE_SCOPE_OPTIONS,
    ROOM_SCOPE_OPTIONS,
    SERIES_LAYOUT_OPTIONS,
    STREAMLIT_COMMAND_OPTIONS,
    VARIANT_MODE_OPTIONS,
    AnalysisWizardState,
    allowed_comfort_outputs,
    analysis_ready,
    analysis_step_complete,
    analysis_step_summary,
    backend_command,
    comfort_subcommand_label,
    command_label,
    first_incomplete_step,
    irrelevant_section_hint,
    normalize_command,
    room_selection_disabled,
    sanitize_comfort_output,
    section_complete,
    section_label,
    section_relevant,
    section_summary,
)
from ma_analyse.core.config import DATENBANK_DIR, INPUT_DIR, OUTPUT_DIR
from ma_analyse.services import (
    get_plot_template_ui_defaults,
    get_plot_template_ui_spec,
    list_analysis_rooms,
    list_analysis_variants,
)
from ma_ui.streamlit_app.components import render_analysis_result
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.tkinter_app.launcher import launch_tkinter_analyse
from ma_workflow import run_analysis_action

PLOT_TEMPLATE_STEP = "plot-template-analyse"
COMMAND_OPTIONS = STREAMLIT_COMMAND_OPTIONS
DEFAULT_COMMAND_INDEX = COMMAND_OPTIONS.index(PLOT_TEMPLATE_STEP)
FREE_OVERLAY_LINES_SESSION_KEY = "ma_ui_plot_template_free_overlay_lines"
LAST_ANALYSIS_RESULT_SESSION_KEY = "ma_ui_last_analysis_result"
ACTIVE_ANALYSIS_STEP_SESSION_KEY = "ma_ui_analysis_active_step"
LAST_ANALYSIS_COMMAND_SESSION_KEY = "ma_ui_analysis_last_command"
LAST_ANALYSIS_LEVEL_SESSION_KEY = "ma_ui_analysis_last_level"
PLOT_TEMPLATE_OPTIONS_SESSION_KEY = "ma_ui_plot_template_options"
COMMAND_WIDGET_KEY = "ma_ui_analysis_command"
LOAD_SUBCOMMAND_WIDGET_KEY = "ma_ui_analysis_load_subcommand"
COMFORT_SUBCOMMAND_WIDGET_KEY = "ma_ui_analysis_comfort_subcommand"
PREPARE_EXPORT_WIDGET_KEY = "ma_ui_analysis_prepare_export_format"
COMFORT_TYPE_WIDGET_KEY = "ma_ui_analysis_comfort_type"
ANALYSIS_LEVEL_WIDGET_KEY = "ma_ui_analysis_level"
VARIANT_MODE_WIDGET_KEY = "ma_ui_analysis_variant_mode"
SERIES_LAYOUT_WIDGET_KEY = "ma_ui_analysis_series_layout"
LOAD_VIEW_WIDGET_KEY = "ma_ui_analysis_view"
MONTH_WIDGET_KEY = "ma_ui_analysis_month"
WEEK_WIDGET_KEY = "ma_ui_analysis_week"
DAY_WIDGET_KEY = "ma_ui_analysis_day"
PLOT_TEMPLATE_WIDGET_KEY = "ma_ui_analysis_plot_template"
PLOT_TEMPLATE_MODE_WIDGET_KEY = "ma_ui_analysis_plot_template_mode"
ANALYSIS_SCOPE_WIDGET_KEY = "ma_ui_analysis_scope"
ROOM_SCOPE_WIDGET_KEY = "ma_ui_analysis_room_scope"
VARIANT_SELECT_WIDGET_KEY = "ma_ui_analysis_selected_variants"
VARIANT_SINGLE_WIDGET_KEY = "ma_ui_analysis_selected_variant"
VARIANT_MULTI_WIDGET_KEY = "ma_ui_analysis_selected_variants"
VARIANT_MANUAL_WIDGET_KEY = "ma_ui_analysis_manual_variants"
ROOM_SELECT_WIDGET_KEY = "ma_ui_analysis_selected_rooms"
ROOM_SINGLE_WIDGET_KEY = "ma_ui_analysis_selected_room"
ROOM_MULTI_WIDGET_KEY = "ma_ui_analysis_selected_rooms"
ROOM_MANUAL_WIDGET_KEY = "ma_ui_analysis_manual_rooms"
DEBUG_WIDGET_KEY = "ma_ui_analysis_debug"
OVERLAY_ENABLED_WIDGET_KEY = "ma_ui_analysis_overlay_enabled"
PRIMARY_AXIS_MODE_WIDGET_KEY = "ma_ui_analysis_primary_axis_mode"
PRIMARY_YMIN_WIDGET_KEY = "ma_ui_analysis_primary_ymin"
PRIMARY_YMAX_WIDGET_KEY = "ma_ui_analysis_primary_ymax"
SECONDARY_AXIS_MODE_WIDGET_KEY = "ma_ui_analysis_secondary_axis_mode"
SECONDARY_YMIN_WIDGET_KEY = "ma_ui_analysis_secondary_ymin"
SECONDARY_YMAX_WIDGET_KEY = "ma_ui_analysis_secondary_ymax"
INPUT_DIR_WIDGET_KEY = "ma_ui_analysis_input_dir"
DATABASE_DIR_WIDGET_KEY = "ma_ui_analysis_database_dir"
OUTPUT_ROOT_WIDGET_KEY = "ma_ui_analysis_output_root"
RUN_ID_WIDGET_KEY = "ma_ui_analysis_run_id"
FIXED_OVERLAY_LABELS = {
    "outdoor_temperature": "Aussenlufttemperatur",
    "operative_temperature": "Operative Temperatur",
}


def get_session_overlay_lines(
    session_state: MutableMapping[str, Any] | None = None,
) -> list[dict[str, str]]:
    """Liest freie Overlay-Linien aus einem Session-State-kompatiblen Mapping."""
    state = st.session_state if session_state is None else session_state
    raw_lines = state.get(FREE_OVERLAY_LINES_SESSION_KEY, [])
    if not isinstance(raw_lines, list):
        return []

    normalized = [normalize_overlay_line(raw_line) for raw_line in raw_lines if isinstance(raw_line, dict)]
    return [line for line in normalized if line is not None]


def add_session_overlay_line(
    line: dict[str, str],
    session_state: MutableMapping[str, Any] | None = None,
) -> bool:
    """Fuegt eine freie Overlay-Linie hinzu und vermeidet Dubletten."""
    state = st.session_state if session_state is None else session_state
    normalized_line = normalize_overlay_line(line)
    if normalized_line is None:
        return False

    lines = get_session_overlay_lines(state)
    if normalized_line in lines:
        return False
    lines.append(normalized_line)
    state[FREE_OVERLAY_LINES_SESSION_KEY] = lines
    return True


def remove_session_overlay_line(
    index: int,
    session_state: MutableMapping[str, Any] | None = None,
) -> list[dict[str, str]]:
    """Entfernt eine freie Overlay-Linie anhand ihres Listenindex."""
    state = st.session_state if session_state is None else session_state
    lines = get_session_overlay_lines(state)
    if 0 <= index < len(lines):
        del lines[index]
    state[FREE_OVERLAY_LINES_SESSION_KEY] = lines
    return lines


def format_overlay_line(line: dict[str, str]) -> str:
    """Baut eine kurze Anzeige fuer freie Overlay-Linien."""
    return f"{line['source']}:{line['column']} -> {line['label']} ({line['axis']})"


def safe_list_plot_overlay_sources(
    *,
    database_dir: str,
    input_dir: str,
    variant_name: str | None,
    room_name: str | None,
    outdoor_column: str,
) -> dict[str, list[str]]:
    """Liest Overlay-Spalten defensiv fuer die Streamlit-Oberflaeche.

    Streamlit kann beim Hot-Reload noch alte Modulstaende halten. Deshalb wird
    die optionale Komfortfunktion erst beim Rendern importiert und darf auf
    einen leeren Katalog zurueckfallen.
    """
    try:
        from ma_analyse.services import list_plot_overlay_sources
    except ImportError:
        return {"csv": [], "aux": []}

    return list_plot_overlay_sources(
        database_dir=database_dir,
        input_dir=input_dir,
        variant_name=variant_name,
        room_name=room_name,
        outdoor_column=outdoor_column,
    )


def _render_time_options(prefix: str, view: str) -> tuple[str | None, int | None, int | None]:
    month: str | None = None
    week: int | None = None
    day: int | None = None

    if view in {"month", "day"}:
        current_month = st.session_state.get(MONTH_WIDGET_KEY, MONTH_NAMES[0])
        month_index = MONTH_NAMES.index(current_month) if current_month in MONTH_NAMES else 0
        month = st.selectbox(f"{prefix} Monat", options=MONTH_NAMES, index=month_index, key=MONTH_WIDGET_KEY)

    if view == "week":
        current_week = _int_session_value(WEEK_WIDGET_KEY) or 1
        week = int(
            st.number_input(
                f"{prefix} Kalenderwoche",
                min_value=1,
                max_value=MAX_CALENDAR_WEEK,
                value=current_week,
                key=WEEK_WIDGET_KEY,
            )
        )

    if view == "day":
        month_index = MONTH_NAMES.index(month or MONTH_NAMES[0])
        current_day = _int_session_value(DAY_WIDGET_KEY) or 1
        max_day = MONTH_DAY_COUNTS[month_index]
        day_value = min(current_day, max_day)
        day = int(
            st.number_input(
                f"{prefix} Tag",
                min_value=1,
                max_value=max_day,
                value=day_value,
                key=DAY_WIDGET_KEY,
            )
        )

    return month, week, day


def _render_load_options() -> dict[str, object]:
    view = st.selectbox("Zeitansicht", options=LOAD_VIEW_OPTIONS, index=0)
    month, week, day = _render_time_options("Last", view)
    variant_mode = st.selectbox("Variantenmodus", options=VARIANT_MODE_OPTIONS, index=0)
    series_layout = st.selectbox("Reihenlayout", options=SERIES_LAYOUT_OPTIONS, index=0)
    return {
        "view": view,
        "month": month,
        "week": week,
        "day": day,
        "variant_mode": variant_mode,
        "series_layout": series_layout,
    }


def _render_tkinter_launcher() -> None:
    st.info(
        "Falls eine Funktion in Streamlit noch fehlt, kann die bestehende "
        "Tkinter-Analyse als separates Fenster gestartet werden."
    )
    if st.button("Tkinter-Analyse oeffnen", type="secondary"):
        result = launch_tkinter_analyse()
        if result.success:
            st.success(f"Tkinter-Analyse gestartet. Prozess-ID: {result.process_id}")
        else:
            st.error(f"Tkinter-Analyse konnte nicht gestartet werden: {result.error}")
            st.code(" ".join(result.command), language="powershell")


def _render_plot_template_options(
    *,
    template: str,
    template_defaults: dict[str, object],
    template_spec: dict[str, object],
    input_dir: str,
    database_dir: str,
    selected_variants: list[str],
    available_variants: list[str],
    selected_rooms: list[str],
    month: str | None = None,
    week: int | None = None,
    day: int | None = None,
    render_time_options: bool = True,
) -> dict[str, Any]:
    view = plot_template_view(template_spec)
    if render_time_options:
        month, week, day = _render_time_options("Template", view)
    time_options = build_template_time_options(template_spec, month=month, week=week, day=day)

    supports_overlays = plot_template_supports_overlays(template_spec)
    setpoint_min = _default_float(template_defaults, "setpoint_min", DEFAULT_SETPOINT_MIN)
    setpoint_max = _default_float(template_defaults, "setpoint_max", DEFAULT_SETPOINT_MAX)
    secondary_axis_mode = str(
        st.session_state.get(SECONDARY_AXIS_MODE_WIDGET_KEY, "automatic") or "automatic"
    )
    secondary_ymin = _float_session_value(SECONDARY_YMIN_WIDGET_KEY)
    secondary_ymax = _float_session_value(SECONDARY_YMAX_WIDGET_KEY)
    temperature_ymin = (
        secondary_ymin
        if secondary_axis_mode == "manual" and secondary_ymin is not None
        else _default_float(template_defaults, "temperature_ymin", DEFAULT_TEMPERATURE_YMIN)
    )
    temperature_ymax = (
        secondary_ymax
        if secondary_axis_mode == "manual" and secondary_ymax is not None
        else _default_float(template_defaults, "temperature_ymax", DEFAULT_TEMPERATURE_YMAX)
    )
    outdoor_column = _default_text(template_defaults, "outdoor_column", DEFAULT_OUTDOOR_COLUMN)
    show_setpoint_band = _default_bool(template_defaults, "show_setpoint_band", DEFAULT_SHOW_SETPOINT_BAND)
    show_outdoor_temperature = _default_bool(
        template_defaults,
        "show_outdoor_temperature",
        DEFAULT_SHOW_OUTDOOR_TEMPERATURE,
    )
    show_operative_temperature = _default_bool(
        template_defaults,
        "show_operative_temperature",
        DEFAULT_SHOW_OPERATIVE_TEMPERATURE,
    )
    overlay_lines: list[dict[str, str]] = []
    fixed_overlays = _default_fixed_overlays(template_defaults) if supports_overlays else []

    if supports_overlays:
        with st.container(border=True):
            show_setpoint_band = st.checkbox("Sollwertband anzeigen", value=show_setpoint_band)
            show_outdoor_temperature = st.checkbox("Aussenlufttemperatur anzeigen", value=show_outdoor_temperature)
            show_operative_temperature = st.checkbox(
                "Operative Temperatur anzeigen",
                value=show_operative_temperature,
            )
            setpoint_min = st.number_input("Sollwert min [C]", value=float(setpoint_min))
            setpoint_max = st.number_input("Sollwert max [C]", value=float(setpoint_max))
            outdoor_column = st.text_input("Aussenluft-Spalte", value=outdoor_column)

            if fixed_overlays:
                labels = [
                    FIXED_OVERLAY_LABELS.get(str(overlay.get("id", "")), str(overlay.get("label", "")) or "Overlay")
                    for overlay in fixed_overlays
                ]
                st.caption("Feste Template-Overlays: " + ", ".join(labels))

            st.markdown("**Freie Overlay-Linien**")
            overlay_variant = first_selected_value(selected_variants, available_variants)
            overlay_room = first_selected_value(selected_rooms, [])
            overlay_catalog = safe_list_plot_overlay_sources(
                database_dir=database_dir,
                input_dir=input_dir,
                variant_name=overlay_variant,
                room_name=overlay_room,
                outdoor_column=outdoor_column,
            )
            catalog_has_values = bool(overlay_catalog["csv"] or overlay_catalog["aux"])
            if catalog_has_values:
                st.caption(
                    "Overlay-Katalog aus erster gewaehlter Variante und erstem Raum: "
                    f"{overlay_variant or '-'} / {overlay_room or '-'}"
                )
            else:
                st.caption("Kein Overlay-Katalog gefunden. Spalte kann manuell eingegeben werden.")

            catalog_source = st.selectbox("Overlay-Quelle", options=("csv", "aux"), key="plot_template_overlay_source")
            catalog_columns = overlay_catalog.get(catalog_source, [])
            if catalog_columns:
                catalog_column = st.selectbox(
                    "Overlay-Spalte",
                    options=catalog_columns,
                    key="plot_template_overlay_column_select",
                )
            else:
                catalog_column = st.text_input("Overlay-Spalte", value="", key="plot_template_overlay_column_text")
            catalog_axis = st.selectbox("Overlay-Achse", options=("heat", "temperature"), index=0)
            catalog_label = st.text_input("Overlay-Label", value=catalog_column)
            if st.button("Freie Overlay-Linie hinzufuegen", type="secondary"):
                catalog_line = build_catalog_overlay_line(
                    source=catalog_source,
                    column=catalog_column,
                    label=catalog_label,
                    axis=catalog_axis,
                )
                if catalog_line and add_session_overlay_line(catalog_line):
                    st.success("Overlay-Linie hinzugefuegt.")
                else:
                    st.warning("Overlay-Linie konnte nicht hinzugefuegt werden.")

            session_overlay_lines = get_session_overlay_lines()
            if session_overlay_lines:
                selected_line_index = st.selectbox(
                    "Freie Overlay-Linie entfernen",
                    options=range(len(session_overlay_lines)),
                    format_func=lambda index: format_overlay_line(session_overlay_lines[index]),
                    key="plot_template_overlay_remove_index",
                )
                if st.button("Ausgewaehlte Overlay-Linie entfernen", type="secondary"):
                    remove_session_overlay_line(int(selected_line_index))
                    st.success("Overlay-Linie entfernt.")
                    session_overlay_lines = get_session_overlay_lines()
                st.table(
                    [
                        {
                            "Quelle": line["source"],
                            "Spalte": line["column"],
                            "Label": line["label"],
                            "Achse": line["axis"],
                        }
                        for line in session_overlay_lines
                    ]
                )

            with st.expander("Expertenmodus: Overlay-Zeilen als Text"):
                overlay_lines_text = st.text_area(
                    "Freie Overlay-Linien",
                    value="",
                    help="Format je Zeile: source,column,label,axis. source: csv/aux, axis: heat/temperature.",
                )
            overlay_lines = session_overlay_lines + parse_overlay_lines_text(overlay_lines_text)
    else:
        show_setpoint_band = False
        show_outdoor_temperature = False
        show_operative_temperature = False

    return build_plot_template_options(
        template=template,
        month=time_options["month"],
        week=time_options["week"],
        day=time_options["day"],
        show_setpoint_band=show_setpoint_band,
        show_outdoor_temperature=show_outdoor_temperature,
        show_operative_temperature=show_operative_temperature,
        setpoint_min=float(setpoint_min),
        setpoint_max=float(setpoint_max),
        temperature_ymin=float(temperature_ymin),
        temperature_ymax=float(temperature_ymax),
        outdoor_column=outdoor_column,
        overlay_lines=overlay_lines,
        fixed_overlays=fixed_overlays,
        primary_axis_mode=str(
            st.session_state.get(PRIMARY_AXIS_MODE_WIDGET_KEY, "automatic") or "automatic"
        ),
        primary_ymin=_float_session_value(PRIMARY_YMIN_WIDGET_KEY),
        primary_ymax=_float_session_value(PRIMARY_YMAX_WIDGET_KEY),
        secondary_axis_mode=secondary_axis_mode,
        secondary_ymin=secondary_ymin,
        secondary_ymax=secondary_ymax,
    )


def _selectbox_index(options: tuple[str, ...], value: object) -> int:
    text_value = str(value or "")
    return options.index(text_value) if text_value in options else 0


def _reset_downstream_analysis_state() -> None:
    """Entfernt alte Auswahlen, wenn der Hauptbefehl gewechselt wurde."""
    for key in (
        LOAD_SUBCOMMAND_WIDGET_KEY,
        COMFORT_SUBCOMMAND_WIDGET_KEY,
        PREPARE_EXPORT_WIDGET_KEY,
        COMFORT_TYPE_WIDGET_KEY,
        ANALYSIS_LEVEL_WIDGET_KEY,
        VARIANT_MODE_WIDGET_KEY,
        SERIES_LAYOUT_WIDGET_KEY,
        LOAD_VIEW_WIDGET_KEY,
        MONTH_WIDGET_KEY,
        WEEK_WIDGET_KEY,
        DAY_WIDGET_KEY,
        ANALYSIS_SCOPE_WIDGET_KEY,
        ROOM_SCOPE_WIDGET_KEY,
        PLOT_TEMPLATE_MODE_WIDGET_KEY,
        VARIANT_SINGLE_WIDGET_KEY,
        VARIANT_MULTI_WIDGET_KEY,
        VARIANT_MANUAL_WIDGET_KEY,
        ROOM_SINGLE_WIDGET_KEY,
        ROOM_MULTI_WIDGET_KEY,
        ROOM_MANUAL_WIDGET_KEY,
        LAST_ANALYSIS_LEVEL_SESSION_KEY,
        PLOT_TEMPLATE_OPTIONS_SESSION_KEY,
        OVERLAY_ENABLED_WIDGET_KEY,
        PRIMARY_AXIS_MODE_WIDGET_KEY,
        PRIMARY_YMIN_WIDGET_KEY,
        PRIMARY_YMAX_WIDGET_KEY,
        SECONDARY_AXIS_MODE_WIDGET_KEY,
        SECONDARY_YMIN_WIDGET_KEY,
        SECONDARY_YMAX_WIDGET_KEY,
    ):
        st.session_state.pop(key, None)


def _sync_command_change() -> None:
    command = normalize_command(str(st.session_state.get(COMMAND_WIDGET_KEY, "") or ""), streamlit=True)
    previous_command = st.session_state.get(LAST_ANALYSIS_COMMAND_SESSION_KEY)
    if command == previous_command:
        return
    _reset_downstream_analysis_state()
    st.session_state[ACTIVE_ANALYSIS_STEP_SESSION_KEY] = "command"
    st.session_state[LAST_ANALYSIS_COMMAND_SESSION_KEY] = command


def _int_session_value(key: str) -> int | None:
    value = st.session_state.get(key)
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _selected_variants_from_state(analysis_scope: str, available_variants: list[str]) -> tuple[str, ...]:
    if analysis_scope == "Alle Varianten":
        return tuple(available_variants)
    if available_variants and analysis_scope == "Eine Variante":
        value = str(st.session_state.get(VARIANT_SINGLE_WIDGET_KEY, "") or "")
        return (value,) if value else ()
    if available_variants:
        values = st.session_state.get(VARIANT_MULTI_WIDGET_KEY, [])
        return tuple(str(value) for value in values if str(value).strip()) if isinstance(values, list) else ()
    return tuple(split_csv_text(str(st.session_state.get(VARIANT_MANUAL_WIDGET_KEY, "") or "")))


def _selected_rooms_from_state(
    *,
    command: str,
    room_scope: str,
    available_rooms: list[str],
    template_spec: dict[str, object],
) -> tuple[str, ...]:
    if room_scope == "Alle Räume":
        return tuple(available_rooms)
    if available_rooms and room_scope == "Ein Raum":
        value = str(st.session_state.get(ROOM_SINGLE_WIDGET_KEY, "") or "")
        return (value,) if value else ()
    selected_values = st.session_state.get(ROOM_MULTI_WIDGET_KEY, [])
    if isinstance(selected_values, list) and selected_values:
        return tuple(str(value) for value in selected_values if str(value).strip())
    return tuple(split_csv_text(str(st.session_state.get(ROOM_MANUAL_WIDGET_KEY, "") or "")))


def _current_wizard_state(
    *,
    available_variants: list[str],
    available_rooms: list[str],
    template_spec: dict[str, object],
) -> AnalysisWizardState:
    command = normalize_command(str(st.session_state.get(COMMAND_WIDGET_KEY, "") or ""), streamlit=True)
    analysis_scope = str(st.session_state.get(ANALYSIS_SCOPE_WIDGET_KEY, "") or "")
    analysis_level = str(st.session_state.get(ANALYSIS_LEVEL_WIDGET_KEY, "") or "")
    room_scope = str(st.session_state.get(ROOM_SCOPE_WIDGET_KEY, "") or "")
    selected_variants = _selected_variants_from_state(analysis_scope, available_variants)
    selected_rooms = _selected_rooms_from_state(
        command=command,
        room_scope=room_scope,
        available_rooms=available_rooms,
        template_spec=template_spec,
    )
    overlay_options = st.session_state.get(PLOT_TEMPLATE_OPTIONS_SESSION_KEY, {})
    overlay_lines = overlay_options.get("overlay_lines", []) if isinstance(overlay_options, dict) else []

    return AnalysisWizardState(
        command=command,
        comfort_subcommand=str(st.session_state.get(COMFORT_SUBCOMMAND_WIDGET_KEY, "") or ""),
        load_subcommand=str(st.session_state.get(LOAD_SUBCOMMAND_WIDGET_KEY, "") or ""),
        prepare_export_format=str(st.session_state.get(PREPARE_EXPORT_WIDGET_KEY, "") or ""),
        comfort_type=str(st.session_state.get(COMFORT_TYPE_WIDGET_KEY, "") or ""),
        analysis_level=analysis_level,
        variant_mode=str(st.session_state.get(VARIANT_MODE_WIDGET_KEY, "") or ""),
        plot_template_mode=str(st.session_state.get(PLOT_TEMPLATE_MODE_WIDGET_KEY, "") or ""),
        series_layout=str(st.session_state.get(SERIES_LAYOUT_WIDGET_KEY, "") or ""),
        view=str(st.session_state.get(LOAD_VIEW_WIDGET_KEY, "") or ""),
        month=str(st.session_state.get(MONTH_WIDGET_KEY, "") or "") or None,
        week=_int_session_value(WEEK_WIDGET_KEY),
        day=_int_session_value(DAY_WIDGET_KEY),
        plot_template=str(st.session_state.get(PLOT_TEMPLATE_WIDGET_KEY, HEATING_YEAR_TEMPLATE) or HEATING_YEAR_TEMPLATE),
        analysis_scope=analysis_scope,
        room_scope=room_scope,
        selected_variants=selected_variants,
        selected_rooms=selected_rooms,
        variant_count=len(available_variants),
        room_count=len(available_rooms),
        overlay_count=len(overlay_lines) if isinstance(overlay_lines, list) else 0,
        overlay_enabled=bool(st.session_state.get(OVERLAY_ENABLED_WIDGET_KEY, False)),
        show_setpoint_band=bool(overlay_options.get("show_setpoint_band", False)) if isinstance(overlay_options, dict) else False,
        show_outdoor_temperature=bool(overlay_options.get("show_outdoor_temperature", False))
        if isinstance(overlay_options, dict)
        else False,
        show_operative_temperature=bool(overlay_options.get("show_operative_temperature", False))
        if isinstance(overlay_options, dict)
        else False,
        primary_axis_mode=str(
            st.session_state.get(PRIMARY_AXIS_MODE_WIDGET_KEY, "automatic") or "automatic"
        ),
        primary_ymin=_float_session_value(PRIMARY_YMIN_WIDGET_KEY),
        primary_ymax=_float_session_value(PRIMARY_YMAX_WIDGET_KEY),
        secondary_axis_mode=str(
            st.session_state.get(SECONDARY_AXIS_MODE_WIDGET_KEY, "automatic") or "automatic"
        ),
        secondary_ymin=_float_session_value(SECONDARY_YMIN_WIDGET_KEY),
        secondary_ymax=_float_session_value(SECONDARY_YMAX_WIDGET_KEY),
    )


def _float_session_value(key: str) -> float | None:
    value = st.session_state.get(key)
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _advanced_path_values() -> tuple[str, str, str, str]:
    return (
        str(st.session_state.get(INPUT_DIR_WIDGET_KEY, INPUT_DIR)),
        str(st.session_state.get(DATABASE_DIR_WIDGET_KEY, DATENBANK_DIR)),
        str(st.session_state.get(OUTPUT_ROOT_WIDGET_KEY, OUTPUT_DIR)),
        str(st.session_state.get(RUN_ID_WIDGET_KEY, "")),
    )


def _render_advanced_paths() -> tuple[str, str, str, str]:
    with st.expander("Erweiterte Pfade", expanded=False):
        input_dir = st.text_input("IDA-Importordner", value=str(INPUT_DIR), key=INPUT_DIR_WIDGET_KEY)
        database_dir = st.text_input("Datenbankordner", value=str(DATENBANK_DIR), key=DATABASE_DIR_WIDGET_KEY)
        output_root = st.text_input("Ausgabeordner", value=str(OUTPUT_DIR), key=OUTPUT_ROOT_WIDGET_KEY)
        run_id = st.text_input("Run-ID", value="", key=RUN_ID_WIDGET_KEY)
    return input_dir, database_dir, output_root, run_id


def _render_step_summaries(
    *,
    visible_steps: tuple[str, ...],
    active_step: str,
    state: AnalysisWizardState,
    template_view: str,
) -> None:
    summary_rows = []
    for step in visible_steps:
        if step == active_step:
            break
        summary = analysis_step_summary(state, step, template_view=template_view)
        if summary:
            summary_rows.append(summary)
    if not summary_rows:
        return

    st.markdown("**Bisherige Auswahl**")
    for summary in summary_rows:
        st.caption(summary)


def _render_command_step() -> None:
    options = ("", *COMMAND_OPTIONS)
    st.selectbox(
        "Befehl",
        options=options,
        index=_selectbox_index(options, st.session_state.get(COMMAND_WIDGET_KEY)),
        format_func=command_label,
        key=COMMAND_WIDGET_KEY,
    )
    _sync_command_change()


def _render_subcommand_step(state: AnalysisWizardState) -> None:
    command = normalize_command(state.command)
    if command == "comfort":
        options = ("", *allowed_comfort_outputs(state.analysis_level))
        st.selectbox(
            "Comfort-Unterbefehl",
            options=options,
            index=_selectbox_index(options, st.session_state.get(COMFORT_TYPE_WIDGET_KEY)),
            key=COMFORT_TYPE_WIDGET_KEY,
        )
        return

    options = ("", *LOAD_SUBCOMMAND_OPTIONS)
    label = "Kuehlvergleich Unterbefehl" if command == "cooling" else "Heizvergleich Unterbefehl"
    st.selectbox(
        label,
        options=options,
        index=_selectbox_index(options, st.session_state.get(LOAD_SUBCOMMAND_WIDGET_KEY)),
        key=LOAD_SUBCOMMAND_WIDGET_KEY,
    )
    st.caption("bar erzeugt Maximalwertdiagramme. timeline aktiviert die Zeitansichten.")


def _render_prepare_export_step() -> None:
    options = ("", *EXPORT_FORMAT_OPTIONS)
    st.selectbox(
        "Exportformat",
        options=options,
        index=_selectbox_index(options, st.session_state.get(PREPARE_EXPORT_WIDGET_KEY)),
        key=PREPARE_EXPORT_WIDGET_KEY,
    )
    selected_format = st.session_state.get(PREPARE_EXPORT_WIDGET_KEY)
    if selected_format == "csv":
        st.caption("CSV ist das operative Standardformat fuer die Folgeskripte.")
    elif selected_format == "excel":
        st.caption("Excel dient aktuell nur der uebersichtlicheren Darstellung.")
    elif selected_format == "both":
        st.caption("CSV + Excel erzeugt operative CSV-Dateien und zusaetzlich XLSX-Dateien zur Ansicht.")


def _render_plot_template_selection_step(template_spec: dict[str, object]) -> None:
    current_template = str(st.session_state.get(PLOT_TEMPLATE_WIDGET_KEY, HEATING_YEAR_TEMPLATE) or HEATING_YEAR_TEMPLATE)
    index = PLOT_TEMPLATE_CHOICES.index(current_template) if current_template in PLOT_TEMPLATE_CHOICES else 0
    template = st.selectbox(
        "Template",
        options=PLOT_TEMPLATE_CHOICES,
        index=index,
        key=PLOT_TEMPLATE_WIDGET_KEY,
    )
    if template != current_template:
        st.session_state.pop(PLOT_TEMPLATE_OPTIONS_SESSION_KEY, None)
        template_spec = get_plot_template_ui_spec(template)

    room_mode = "Einzelraum" if plot_template_requires_single_room(template_spec) else "Mehrere Raeume"
    st.caption(
        "Template-Spezifikation: "
        f"{template_spec.get('metric', '-')} / {template_spec.get('view', '-')} / {room_mode}"
    )
    _render_time_options("Template", plot_template_view(template_spec))


def _render_options_step(state: AnalysisWizardState, template_spec: dict[str, object]) -> None:
    command = normalize_command(state.command)
    if command == PLOT_TEMPLATE_STEP:
        _render_plot_template_selection_step(template_spec)
        return
    if command == "comfort":
        previous_level = str(st.session_state.get(LAST_ANALYSIS_LEVEL_SESSION_KEY, "") or "")
        options = ("", *COMFORT_ANALYSIS_LEVEL_OPTIONS)
        selected_level = st.selectbox(
            "Analyseebene",
            options=options,
            index=_selectbox_index(options, st.session_state.get(ANALYSIS_LEVEL_WIDGET_KEY)),
            key=ANALYSIS_LEVEL_WIDGET_KEY,
        )
        if selected_level != previous_level:
            st.session_state[COMFORT_TYPE_WIDGET_KEY] = sanitize_comfort_output(
                selected_level,
                str(st.session_state.get(COMFORT_TYPE_WIDGET_KEY, "") or ""),
            )
            st.session_state[LAST_ANALYSIS_LEVEL_SESSION_KEY] = selected_level
        return
    if command == "analyze_data":
        options = ("", *SERIES_LAYOUT_OPTIONS)
        st.selectbox(
            "Excel-Ausgabe",
            options=options,
            index=_selectbox_index(options, st.session_state.get(SERIES_LAYOUT_WIDGET_KEY)),
            key=SERIES_LAYOUT_WIDGET_KEY,
        )
        st.caption("separate erzeugt eine Excel pro Variante. combined erzeugt eine gemeinsame Excel.")
        return
    if command in {"heating", "cooling"}:
        options = ("", *VARIANT_MODE_OPTIONS)
        st.selectbox(
            "Modus",
            options=options,
            index=_selectbox_index(options, st.session_state.get(VARIANT_MODE_WIDGET_KEY)),
            key=VARIANT_MODE_WIDGET_KEY,
        )
        if st.session_state.get(VARIANT_MODE_WIDGET_KEY) == "compare":
            layout_options = ("", *SERIES_LAYOUT_OPTIONS)
            st.selectbox(
                "Diagrammausgabe",
                options=layout_options,
                index=_selectbox_index(layout_options, st.session_state.get(SERIES_LAYOUT_WIDGET_KEY)),
                key=SERIES_LAYOUT_WIDGET_KEY,
            )
        if state.load_subcommand == "timeline":
            view_options = ("", *LOAD_VIEW_OPTIONS)
            view = st.selectbox(
                "Zeitansicht",
                options=view_options,
                index=_selectbox_index(view_options, st.session_state.get(LOAD_VIEW_WIDGET_KEY)),
                key=LOAD_VIEW_WIDGET_KEY,
            )
            _render_time_options("Last", view)


def _build_plot_template_options_from_state(
    state: AnalysisWizardState,
    template_defaults: dict[str, object],
) -> dict[str, Any]:
    return build_plot_template_options(
        template=state.plot_template,
        month=state.month,
        week=state.week,
        day=state.day,
        show_setpoint_band=state.overlay_enabled
        and _default_bool(template_defaults, "show_setpoint_band", False),
        show_outdoor_temperature=state.overlay_enabled
        and _default_bool(template_defaults, "show_outdoor_temperature", False),
        show_operative_temperature=state.overlay_enabled
        and _default_bool(template_defaults, "show_operative_temperature", False),
        setpoint_min=_default_float(template_defaults, "setpoint_min", DEFAULT_SETPOINT_MIN),
        setpoint_max=_default_float(template_defaults, "setpoint_max", DEFAULT_SETPOINT_MAX),
        temperature_ymin=_default_float(template_defaults, "temperature_ymin", DEFAULT_TEMPERATURE_YMIN),
        temperature_ymax=_default_float(template_defaults, "temperature_ymax", DEFAULT_TEMPERATURE_YMAX),
        outdoor_column=_default_text(template_defaults, "outdoor_column", DEFAULT_OUTDOOR_COLUMN),
        fixed_overlays=_default_fixed_overlays(template_defaults) if state.overlay_enabled else [],
        primary_axis_mode=state.primary_axis_mode,
        primary_ymin=state.primary_ymin,
        primary_ymax=state.primary_ymax,
        secondary_axis_mode=state.secondary_axis_mode,
        secondary_ymin=state.secondary_ymin,
        secondary_ymax=state.secondary_ymax,
    )


def _render_overlay_step(
    *,
    state: AnalysisWizardState,
    template_defaults: dict[str, object],
    template_spec: dict[str, object],
    input_dir: str,
    database_dir: str,
    available_variants: list[str],
) -> None:
    options = _render_plot_template_options(
        template=state.plot_template,
        template_defaults=template_defaults,
        template_spec=template_spec,
        input_dir=input_dir,
        database_dir=database_dir,
        selected_variants=list(state.selected_variants),
        available_variants=available_variants,
        selected_rooms=list(state.selected_rooms),
        month=state.month,
        week=state.week,
        day=state.day,
        render_time_options=False,
    )
    st.session_state[PLOT_TEMPLATE_OPTIONS_SESSION_KEY] = options


def _render_analysis_scope_step(command: str) -> None:
    scope_options = PLOT_TEMPLATE_SCOPE_OPTIONS if command == PLOT_TEMPLATE_STEP else ANALYSIS_SCOPE_OPTIONS
    if st.session_state.get(ANALYSIS_SCOPE_WIDGET_KEY) not in scope_options:
        st.session_state[ANALYSIS_SCOPE_WIDGET_KEY] = ""
    options = ("", *scope_options)
    st.selectbox(
        "Analyseumfang",
        options=options,
        index=_selectbox_index(options, st.session_state.get(ANALYSIS_SCOPE_WIDGET_KEY)),
        key=ANALYSIS_SCOPE_WIDGET_KEY,
    )


def _render_variants_step(state: AnalysisWizardState, available_variants: list[str]) -> None:
    if state.analysis_scope == "Alle Varianten" and normalize_command(state.command) != PLOT_TEMPLATE_STEP:
        st.caption(f"Alle gefundenen Varianten werden verwendet: {len(available_variants)}")
        return
    if available_variants and state.analysis_scope == "Eine Variante":
        current = st.session_state.get(VARIANT_SINGLE_WIDGET_KEY)
        index = available_variants.index(current) if current in available_variants else 0
        st.selectbox("Variante", options=available_variants, index=index, key=VARIANT_SINGLE_WIDGET_KEY)
        return
    if available_variants:
        default = st.session_state.get(VARIANT_MULTI_WIDGET_KEY)
        if not isinstance(default, list):
            default = available_variants[:1]
        st.multiselect("Varianten", options=available_variants, default=default, key=VARIANT_MULTI_WIDGET_KEY)
        return
    st.text_input("Varianten", value="", key=VARIANT_MANUAL_WIDGET_KEY)


def _render_rooms_step(state: AnalysisWizardState, available_rooms: list[str], template_spec: dict[str, object]) -> None:
    if room_selection_disabled(state):
        st.info("Bei Analyse Variante werden alle bekannten Raeume verwendet.")
        return
    if normalize_command(state.command) == PLOT_TEMPLATE_STEP and plot_template_requires_single_room(template_spec):
        default_room = "208 office" if "208 office" in available_rooms else (available_rooms[0] if available_rooms else "")
        index = available_rooms.index(default_room) if default_room in available_rooms else 0
        st.selectbox("Raum", options=available_rooms, index=index, key=ROOM_SINGLE_WIDGET_KEY)
        return

    default_rooms = ["208 office"] if "208 office" in available_rooms else available_rooms[:1]
    current_default = st.session_state.get(ROOM_MULTI_WIDGET_KEY)
    if not isinstance(current_default, list):
        current_default = default_rooms
    st.multiselect("Raeume", options=available_rooms, default=current_default, key=ROOM_MULTI_WIDGET_KEY)
    st.text_input("Raeume manuell", value="", key=ROOM_MANUAL_WIDGET_KEY)


def _render_active_step(
    *,
    active_step: str,
    state: AnalysisWizardState,
    template_defaults: dict[str, object],
    template_spec: dict[str, object],
    input_dir: str,
    database_dir: str,
    available_variants: list[str],
    available_rooms: list[str],
) -> None:
    titles = {
        "command": "Befehl festlegen",
        "subcommand": "Unterbefehl passend zum Befehl waehlen",
        "prepare_export": "Exportformat fuer prepare waehlen",
        "options": "Optionen festlegen",
        "overlays": "Datenlinien fuer Plot-Templates auswaehlen",
        "analysis_scope": "Analyseumfang waehlen",
        "variants": "Varianten passend zum Befehl auswaehlen",
        "rooms": "Raeume auswaehlen oder automatisch uebernehmen",
    }
    st.subheader(titles.get(active_step, active_step))
    if active_step == "command":
        _render_command_step()
    elif active_step == "subcommand":
        _render_subcommand_step(state)
    elif active_step == "prepare_export":
        _render_prepare_export_step()
    elif active_step == "options":
        _render_options_step(state, template_spec)
    elif active_step == "overlays":
        _render_overlay_step(
            state=state,
            template_defaults=template_defaults,
            template_spec=template_spec,
            input_dir=input_dir,
            database_dir=database_dir,
            available_variants=available_variants,
        )
    elif active_step == "analysis_scope":
        _render_analysis_scope_step(normalize_command(state.command))
    elif active_step == "variants":
        _render_variants_step(state, available_variants)
    elif active_step == "rooms":
        _render_rooms_step(state, available_rooms, template_spec)


def _next_step(active_step: str, visible_steps: tuple[str, ...]) -> str | None:
    if active_step not in visible_steps:
        return visible_steps[0] if visible_steps else None
    index = visible_steps.index(active_step)
    if index + 1 >= len(visible_steps):
        return None
    return visible_steps[index + 1]


def _previous_step(active_step: str, visible_steps: tuple[str, ...]) -> str | None:
    if active_step not in visible_steps:
        return None
    index = visible_steps.index(active_step)
    if index == 0:
        return None
    return visible_steps[index - 1]


def _render_step_navigation(
    *,
    active_step: str,
    visible_steps: tuple[str, ...],
    state: AnalysisWizardState,
    template_view: str,
    room_selection_disabled: bool,
) -> None:
    previous_step = _previous_step(active_step, visible_steps)
    next_step = _next_step(active_step, visible_steps)
    current_complete = analysis_step_complete(
        state,
        active_step,
        template_view=template_view,
        room_selection_disabled=room_selection_disabled,
    )

    left, right = st.columns(2)
    with left:
        if previous_step and st.button("Zurueck", type="secondary"):
            st.session_state[ACTIVE_ANALYSIS_STEP_SESSION_KEY] = previous_step
    with right:
        if next_step:
            if st.button("Weiter", type="primary", disabled=not current_complete):
                st.session_state[ACTIVE_ANALYSIS_STEP_SESSION_KEY] = next_step
        elif not current_complete:
            st.info("Bitte Schritt vollstaendig ausfuellen.")


def _analysis_ready(
    state: AnalysisWizardState,
    visible_steps: tuple[str, ...],
    *,
    template_view: str,
    room_selection_disabled: bool,
) -> bool:
    return all(
        analysis_step_complete(
            state,
            step,
            template_view=template_view,
            room_selection_disabled=room_selection_disabled,
        )
        for step in visible_steps
    )


def _build_plot_template_options_for_run(
    state: AnalysisWizardState,
    template_defaults: dict[str, object],
    template_supports_overlays: bool,
) -> dict[str, Any]:
    if template_supports_overlays and state.overlay_enabled:
        stored_options = st.session_state.get(PLOT_TEMPLATE_OPTIONS_SESSION_KEY)
        if isinstance(stored_options, dict):
            return stored_options
    return _build_plot_template_options_from_state(state, template_defaults)


def _plot_template_specs_by_name() -> dict[str, dict[str, object]]:
    return {template: get_plot_template_ui_spec(template) for template in PLOT_TEMPLATE_CHOICES}


def _filtered_plot_template_choices(group: str, mode: str, view: str) -> list[str]:
    specs = _plot_template_specs_by_name()
    return [
        template
        for template in PLOT_TEMPLATE_CHOICES
        if str(specs.get(template, {}).get("view") or "") == view
    ]


def _render_expander_summary(state: AnalysisWizardState, section: str) -> None:
    summary = section_summary(state, section)
    if summary and summary != "-":
        st.caption(f"Auswahl: {summary}")


def _render_section(
    *,
    section: str,
    state: AnalysisWizardState,
    expanded: bool,
    template_defaults: dict[str, object],
    template_spec: dict[str, object],
    input_dir: str,
    database_dir: str,
    output_root: str,
    run_id: str,
    available_variants: list[str],
    available_rooms: list[str],
) -> None:
    label = section_label(section)
    with st.container(border=True):
        st.markdown(f"**{label}**")
        if not section_relevant(state, section):
            st.info(irrelevant_section_hint(state.command, section))
            return
        if section != "command":
            _render_expander_summary(state, section)

        if section == "command":
            _render_command_step()
        elif section == "subcommand":
            _render_subcommand_section(state)
        elif section == "export":
            _render_export_section(state)
        elif section == "template_diagram":
            _render_template_diagram_section(
                state=state,
                template_defaults=template_defaults,
                template_spec=template_spec,
                input_dir=input_dir,
                database_dir=database_dir,
                available_variants=available_variants,
            )
        elif section == "variants":
            _render_variant_scope_section(available_variants)
        elif section == "rooms":
            _render_room_scope_section(
                state=state,
                available_rooms=available_rooms,
                template_spec=template_spec,
            )
        elif section == "overlays":
            _render_overlay_section(
                state=state,
                template_defaults=template_defaults,
                template_spec=template_spec,
                input_dir=input_dir,
                database_dir=database_dir,
                available_variants=available_variants,
            )


def _render_subcommand_section(state: AnalysisWizardState) -> None:
    command = normalize_command(state.command, streamlit=True)
    if command == "comfort":
        options = ("", *COMFORT_SUBCOMMAND_OPTIONS)
        st.selectbox(
            "Comfort-Unterbefehl",
            options=options,
            index=_selectbox_index(options, st.session_state.get(COMFORT_SUBCOMMAND_WIDGET_KEY)),
            format_func=comfort_subcommand_label,
            key=COMFORT_SUBCOMMAND_WIDGET_KEY,
        )
        st.caption("Die konkrete Comfort-Ausgabe wird im Bereich Template / Diagramm gewaehlt.")
        return

    if command in {"heating", "cooling"}:
        options = ("", *LOAD_SUBCOMMAND_OPTIONS)
        label = "Cooling-Unterbefehl" if command == "cooling" else "Heating-Unterbefehl"
        st.selectbox(
            label,
            options=options,
            index=_selectbox_index(options, st.session_state.get(LOAD_SUBCOMMAND_WIDGET_KEY)),
            key=LOAD_SUBCOMMAND_WIDGET_KEY,
        )
        st.caption("bar erzeugt Balkendiagramme. timeline aktiviert Zeitansichten.")
        return

    if command == PLOT_TEMPLATE_STEP:
        current_template = str(
            st.session_state.get(PLOT_TEMPLATE_WIDGET_KEY, HEATING_YEAR_TEMPLATE)
            or HEATING_YEAR_TEMPLATE
        )
        if current_template not in PLOT_TEMPLATE_CHOICES:
            current_template = HEATING_YEAR_TEMPLATE
        template = st.selectbox(
            "Diagramm",
            options=PLOT_TEMPLATE_CHOICES,
            index=PLOT_TEMPLATE_CHOICES.index(current_template),
            key=PLOT_TEMPLATE_WIDGET_KEY,
        )
        if template != current_template:
            st.session_state.pop(PLOT_TEMPLATE_OPTIONS_SESSION_KEY, None)
            st.session_state[LOAD_VIEW_WIDGET_KEY] = plot_template_view(get_plot_template_ui_spec(template))
        spec = get_plot_template_ui_spec(template)
        st.session_state[LOAD_VIEW_WIDGET_KEY] = plot_template_view(spec)
        room_mode = "Einzelplot" if plot_template_requires_single_room(spec) else "Sammeldiagramm"
        st.caption(
            f"{spec.get('metric', '-')} · {spec.get('view', '-')} · {room_mode}. "
            "Die fachliche Gruppierung erfolgt erst bei der Übernahme in einen Hauptbefehl."
        )


def _render_export_section(state: AnalysisWizardState) -> None:
    command = normalize_command(state.command, streamlit=True)
    if command == "prepare":
        _render_prepare_export_step()
        _render_advanced_paths()
        return
    if command == "analyze_data":
        options = ("", *SERIES_LAYOUT_OPTIONS)
        st.selectbox(
            "Excel-Ausgabe",
            options=options,
            index=_selectbox_index(options, st.session_state.get(SERIES_LAYOUT_WIDGET_KEY)),
            key=SERIES_LAYOUT_WIDGET_KEY,
        )
        st.caption("separate erzeugt eine Excel pro Variante. combined erzeugt eine gemeinsame Excel.")
        _render_advanced_paths()
        return

    if command in {"heating", "cooling"}:
        options = ("", *VARIANT_MODE_OPTIONS)
        st.selectbox(
            "Ausgabemodus",
            options=options,
            index=_selectbox_index(options, st.session_state.get(VARIANT_MODE_WIDGET_KEY)),
            key=VARIANT_MODE_WIDGET_KEY,
        )
        if st.session_state.get(VARIANT_MODE_WIDGET_KEY) == "compare":
            layout_options = ("", *SERIES_LAYOUT_OPTIONS)
            st.selectbox(
                "Diagrammausgabe",
                options=layout_options,
                index=_selectbox_index(layout_options, st.session_state.get(SERIES_LAYOUT_WIDGET_KEY)),
                key=SERIES_LAYOUT_WIDGET_KEY,
            )
        st.caption("single nutzt eine Auswahl, compare erzeugt Vergleichsdarstellungen.")
        _render_advanced_paths()
        return

    if command == PLOT_TEMPLATE_STEP:
        options = ("", *PLOT_TEMPLATE_MODE_OPTIONS)
        st.selectbox(
            "Ausgabemodus",
            options=options,
            index=_selectbox_index(options, st.session_state.get(PLOT_TEMPLATE_MODE_WIDGET_KEY)),
            key=PLOT_TEMPLATE_MODE_WIDGET_KEY,
        )
        st.caption(
            "single erzeugt je Variante-Raum-Kombination ein eigenes Diagramm. "
            "compare führt alle ausgewählten Kombinationen in einer gemeinsamen Ausgabe zusammen."
        )
        _render_advanced_paths()
        return

    _render_advanced_paths()


def _render_template_diagram_section(
    *,
    state: AnalysisWizardState,
    template_defaults: dict[str, object],
    template_spec: dict[str, object],
    input_dir: str,
    database_dir: str,
    available_variants: list[str],
) -> None:
    command = normalize_command(state.command, streamlit=True)
    if command == "comfort":
        _render_comfort_template_diagram_options()
        return
    if command in {"heating", "cooling"}:
        _render_load_template_diagram_options(state)
        return
    if command == PLOT_TEMPLATE_STEP:
        _render_plot_template_diagram_options(
            state=state,
            template_defaults=template_defaults,
            template_spec=template_spec,
            input_dir=input_dir,
            database_dir=database_dir,
            available_variants=available_variants,
        )


def _render_comfort_template_diagram_options() -> None:
    options = ("", *allowed_comfort_outputs())
    st.selectbox(
        "Comfort-Diagramm",
        options=options,
        index=_selectbox_index(options, st.session_state.get(COMFORT_TYPE_WIDGET_KEY)),
        key=COMFORT_TYPE_WIDGET_KEY,
    )
    st.caption("Diese vier Ausgaben gehoeren aktuell zur Comfort-Gruppe t_op / rel_hum.")


def _render_load_template_diagram_options(state: AnalysisWizardState) -> None:
    if state.load_subcommand == "timeline":
        view_options = ("", *LOAD_VIEW_OPTIONS)
        view = st.selectbox(
            "Zeitansicht",
            options=view_options,
            index=_selectbox_index(view_options, st.session_state.get(LOAD_VIEW_WIDGET_KEY)),
            key=LOAD_VIEW_WIDGET_KEY,
        )
        if view:
            _render_time_options("Diagramm", view)
        with st.expander("Overlay", expanded=False):
            st.caption("Overlay-Optionen fuer Heating/Cooling werden hier vorbereitet. Die bestehende Backend-Ausfuehrung nutzt aktuell die Hauptdiagrammwerte.")
        with st.expander("Diagrammanpassung", expanded=False):
            st.caption("Achsen, Beschriftungen und Darstellungsoptionen werden hier gebuendelt. Konkrete Werte werden in einem Folgeslice an die Analysefunktionen angebunden.")
    elif state.load_subcommand == "bar":
        st.caption("Balkendiagramme verwenden keine Zeitansicht.")
        with st.expander("Overlay", expanded=False):
            st.caption("Overlay ist fuer Balkendiagramme aktuell nicht aktiv.")
        with st.expander("Diagrammanpassung", expanded=False):
            st.caption("Diagrammanpassungen fuer Balkenplots werden in einem Folgeslice angebunden.")
    else:
        st.info("Waehle zuerst den Unterbefehl bar oder timeline.")


def _render_plot_template_diagram_options(
    *,
    state: AnalysisWizardState,
    template_defaults: dict[str, object],
    template_spec: dict[str, object],
    input_dir: str,
    database_dir: str,
    available_variants: list[str],
) -> None:
    template = str(st.session_state.get(PLOT_TEMPLATE_WIDGET_KEY, HEATING_YEAR_TEMPLATE) or HEATING_YEAR_TEMPLATE)
    template_defaults = get_plot_template_ui_defaults(template)
    template_spec = get_plot_template_ui_spec(template)
    view = plot_template_view(template_spec)
    st.session_state[LOAD_VIEW_WIDGET_KEY] = view
    st.markdown(f"**Zeitansicht:** {view or '-'}")
    if view in LOAD_VIEW_OPTIONS:
        _render_time_options("Template", view)
    else:
        st.caption("Dieses Diagramm benötigt keine zusätzliche Monats-, Wochen- oder Tagesauswahl.")

    room_mode = "Einzelraum" if plot_template_requires_single_room(template_spec) else "Mehrere Raeume"
    st.caption(
        "Template-Spezifikation: "
        f"{template_spec.get('metric', '-')} / {template_spec.get('view', '-')} / {room_mode}"
    )

    supports_overlays = plot_template_supports_overlays(template_spec)
    if supports_overlays:
        st.checkbox(
            "Overlay aktivieren",
            value=bool(st.session_state.get(OVERLAY_ENABLED_WIDGET_KEY, False)),
            key=OVERLAY_ENABLED_WIDGET_KEY,
        )
        st.caption("Nach Varianten und Räumen erscheint dafür ein eigener Overlay-Bereich.")
    else:
        st.session_state[OVERLAY_ENABLED_WIDGET_KEY] = False
        st.caption("Dieses Template unterstuetzt keine Overlay-Auswahl.")

    _render_diagram_adjustment_mockup(template_spec, template_defaults)


def _template_has_secondary_axis(template_spec: dict[str, object]) -> bool:
    metric = str(template_spec.get("metric") or "")
    return plot_template_supports_overlays(template_spec) or metric in {
        "energy_balance",
        "thermal_room_climate",
    }


def _render_diagram_adjustment_mockup(
    template_spec: dict[str, object],
    template_defaults: dict[str, object],
) -> None:
    with st.expander("Diagrammanpassung", expanded=False):
        st.caption(
            "Das Mock-up verwendet Beispieldaten. Die echte Vorschau wird erst mit den gewählten "
            "Varianten und Räumen erzeugt."
        )
        mode_labels = {"automatic": "Automatisch", "manual": "Manuell"}
        primary_mode = st.selectbox(
            "Primäre Y-Achse",
            options=AXIS_RANGE_MODE_OPTIONS,
            index=_selectbox_index(
                AXIS_RANGE_MODE_OPTIONS,
                st.session_state.get(PRIMARY_AXIS_MODE_WIDGET_KEY, "automatic"),
            ),
            format_func=lambda value: mode_labels[value],
            key=PRIMARY_AXIS_MODE_WIDGET_KEY,
        )
        primary_ymin = _float_session_value(PRIMARY_YMIN_WIDGET_KEY)
        primary_ymax = _float_session_value(PRIMARY_YMAX_WIDGET_KEY)
        if primary_mode == "manual":
            primary_columns = st.columns(2)
            primary_ymin = primary_columns[0].number_input(
                "Primär Minimum",
                value=float(primary_ymin if primary_ymin is not None else 0.0),
                key=PRIMARY_YMIN_WIDGET_KEY,
            )
            primary_ymax = primary_columns[1].number_input(
                "Primär Maximum",
                value=float(primary_ymax if primary_ymax is not None else 1000.0),
                key=PRIMARY_YMAX_WIDGET_KEY,
            )

        has_secondary_axis = _template_has_secondary_axis(template_spec)
        secondary_mode = "automatic"
        secondary_ymin = None
        secondary_ymax = None
        if has_secondary_axis:
            secondary_mode = st.selectbox(
                "Sekundäre Y-Achse",
                options=AXIS_RANGE_MODE_OPTIONS,
                index=_selectbox_index(
                    AXIS_RANGE_MODE_OPTIONS,
                    st.session_state.get(SECONDARY_AXIS_MODE_WIDGET_KEY, "automatic"),
                ),
                format_func=lambda value: mode_labels[value],
                key=SECONDARY_AXIS_MODE_WIDGET_KEY,
            )
            secondary_ymin = _float_session_value(SECONDARY_YMIN_WIDGET_KEY)
            secondary_ymax = _float_session_value(SECONDARY_YMAX_WIDGET_KEY)
            if secondary_mode == "manual":
                secondary_columns = st.columns(2)
                secondary_ymin = secondary_columns[0].number_input(
                    "Sekundär Minimum",
                    value=float(
                        secondary_ymin
                        if secondary_ymin is not None
                        else _default_float(template_defaults, "temperature_ymin", DEFAULT_TEMPERATURE_YMIN)
                    ),
                    key=SECONDARY_YMIN_WIDGET_KEY,
                )
                secondary_ymax = secondary_columns[1].number_input(
                    "Sekundär Maximum",
                    value=float(
                        secondary_ymax
                        if secondary_ymax is not None
                        else _default_float(template_defaults, "temperature_ymax", DEFAULT_TEMPERATURE_YMAX)
                    ),
                    key=SECONDARY_YMAX_WIDGET_KEY,
                )
        else:
            st.session_state[SECONDARY_AXIS_MODE_WIDGET_KEY] = "automatic"

        figure, primary_axis = plt.subplots(figsize=(7.2, 3.2))
        hours = list(range(25))
        primary_values = [180 + ((hour % 8) * 85) for hour in hours]
        primary_axis.plot(hours, primary_values, color="#d62828", label="Primäre Datenreihe")
        primary_axis.set_xlabel("Zeit")
        primary_axis.set_ylabel("Primäre Achse")
        primary_axis.grid(True, alpha=0.25)
        if primary_mode == "manual" and primary_ymin is not None and primary_ymax is not None:
            if primary_ymin < primary_ymax:
                primary_axis.set_ylim(primary_ymin, primary_ymax)
            else:
                st.warning("Das Minimum der primären Achse muss kleiner als das Maximum sein.")

        handles, labels = primary_axis.get_legend_handles_labels()
        if has_secondary_axis:
            secondary_axis = primary_axis.twinx()
            secondary_values = [8 + ((hour % 12) * 1.4) for hour in hours]
            secondary_axis.plot(hours, secondary_values, color="#2563eb", label="Sekundäre Datenreihe")
            secondary_axis.set_ylabel("Sekundäre Achse")
            if secondary_mode == "manual" and secondary_ymin is not None and secondary_ymax is not None:
                if secondary_ymin < secondary_ymax:
                    secondary_axis.set_ylim(secondary_ymin, secondary_ymax)
                else:
                    st.warning("Das Minimum der sekundären Achse muss kleiner als das Maximum sein.")
            secondary_handles, secondary_labels = secondary_axis.get_legend_handles_labels()
            handles.extend(secondary_handles)
            labels.extend(secondary_labels)
        primary_axis.legend(handles, labels, loc="upper left", fontsize=8)
        figure.tight_layout()
        st.pyplot(figure, clear_figure=True)


def _render_overlay_section(
    *,
    state: AnalysisWizardState,
    template_defaults: dict[str, object],
    template_spec: dict[str, object],
    input_dir: str,
    database_dir: str,
    available_variants: list[str],
) -> None:
    if not plot_template_supports_overlays(template_spec):
        st.info("Das ausgewählte Diagramm unterstützt keine zusätzlichen Overlay-Datenreihen.")
        return
    if not section_complete(state, "variants") or not section_complete(state, "rooms"):
        st.info("Wähle zuerst Varianten und Räume, damit der Overlay-Katalog geladen werden kann.")
        return

    reference_variant = first_selected_value(list(state.selected_variants), available_variants)
    reference_room = first_selected_value(list(state.selected_rooms), [])
    st.info(
        "Referenz für den Overlay-Katalog: "
        f"{reference_variant or '-'} / {reference_room or '-'}. "
        "Weitere ausgewählte Kombinationen werden beim Analysestart auf die benötigten Spalten geprüft."
    )
    options = _render_plot_template_options(
        template=state.plot_template,
        template_defaults=template_defaults,
        template_spec=template_spec,
        input_dir=input_dir,
        database_dir=database_dir,
        selected_variants=list(state.selected_variants),
        available_variants=available_variants,
        selected_rooms=list(state.selected_rooms),
        month=state.month,
        week=state.week,
        day=state.day,
        render_time_options=False,
    )
    st.session_state[PLOT_TEMPLATE_OPTIONS_SESSION_KEY] = options


def _render_variant_scope_section(available_variants: list[str]) -> None:
    options = ("", *ANALYSIS_SCOPE_OPTIONS)
    st.selectbox(
        "Variantenauswahl",
        options=options,
        index=_selectbox_index(options, st.session_state.get(ANALYSIS_SCOPE_WIDGET_KEY)),
        key=ANALYSIS_SCOPE_WIDGET_KEY,
    )
    scope = str(st.session_state.get(ANALYSIS_SCOPE_WIDGET_KEY, "") or "")
    if scope == "Alle Varianten":
        st.caption(f"Alle gefundenen Varianten werden verwendet: {len(available_variants)}")
        return
    if available_variants and scope == "Eine Variante":
        current = st.session_state.get(VARIANT_SINGLE_WIDGET_KEY)
        index = available_variants.index(current) if current in available_variants else 0
        st.selectbox("Variante", options=available_variants, index=index, key=VARIANT_SINGLE_WIDGET_KEY)
        return
    if available_variants and scope == "Mehrere Varianten":
        default = st.session_state.get(VARIANT_MULTI_WIDGET_KEY)
        if not isinstance(default, list):
            default = available_variants[:1]
        st.multiselect("Varianten", options=available_variants, default=default, key=VARIANT_MULTI_WIDGET_KEY)
        return
    if scope:
        st.text_input("Varianten manuell", value="", key=VARIANT_MANUAL_WIDGET_KEY)


def _render_room_scope_section(
    *,
    state: AnalysisWizardState,
    available_rooms: list[str],
    template_spec: dict[str, object],
) -> None:
    options = ("", *ROOM_SCOPE_OPTIONS)
    st.selectbox(
        "Raumauswahl",
        options=options,
        index=_selectbox_index(options, st.session_state.get(ROOM_SCOPE_WIDGET_KEY)),
        key=ROOM_SCOPE_WIDGET_KEY,
    )
    scope = str(st.session_state.get(ROOM_SCOPE_WIDGET_KEY, "") or "")
    if scope == "Alle Räume":
        st.caption(f"Gefundene Raeume: {len(available_rooms)}")
        st.caption("Alle Räume werden als eigene Auswahlkombinationen verarbeitet.")
        return
    if available_rooms and scope == "Ein Raum":
        default_room = "208 office" if "208 office" in available_rooms else available_rooms[0]
        current = st.session_state.get(ROOM_SINGLE_WIDGET_KEY, default_room)
        index = available_rooms.index(current) if current in available_rooms else available_rooms.index(default_room)
        st.selectbox("Raum", options=available_rooms, index=index, key=ROOM_SINGLE_WIDGET_KEY)
        return
    if available_rooms and scope == "Mehrere Räume":
        default_rooms = ["208 office"] if "208 office" in available_rooms else available_rooms[:1]
        current_default = st.session_state.get(ROOM_MULTI_WIDGET_KEY)
        if not isinstance(current_default, list):
            current_default = default_rooms
        st.multiselect("Raeume", options=available_rooms, default=current_default, key=ROOM_MULTI_WIDGET_KEY)
        return
    if scope:
        st.text_input("Raeume manuell", value="", key=ROOM_MANUAL_WIDGET_KEY)


def _resolved_rooms_for_run(state: AnalysisWizardState, available_rooms: list[str], template_spec: dict[str, object]) -> tuple[str, ...]:
    return state.selected_rooms


def _render_run_section(
    *,
    state: AnalysisWizardState,
    template_defaults: dict[str, object],
    template_spec: dict[str, object],
    input_dir: str,
    database_dir: str,
    output_root: str,
    run_id: str,
    available_rooms: list[str],
) -> None:
    st.markdown("**Aktionsbereich**")
    ready = analysis_ready(state)
    debug = st.checkbox("Debug-Ausgabe", value=False, key=DEBUG_WIDGET_KEY)
    if not ready:
        missing_step = first_incomplete_step(state)
        st.info(f"Analyse noch nicht startbereit. Naechster fehlender Bereich: {section_label(missing_step or 'run')}")

    preview_col, run_col = st.columns(2)
    with preview_col:
        if st.button("Vorschau aktualisieren", type="secondary", disabled=not ready):
            config = _build_run_config(
                state=state,
                template_defaults=template_defaults,
                template_spec=template_spec,
                input_dir=input_dir,
                database_dir=database_dir,
                output_root=output_root,
                run_id=run_id,
                available_rooms=available_rooms,
                debug=debug,
            )
            st.session_state[LAST_ANALYSIS_RESULT_SESSION_KEY] = run_analysis_action(config)
    with run_col:
        if st.button("Analyse starten", type="primary", disabled=not ready):
            config = _build_run_config(
                state=state,
                template_defaults=template_defaults,
                template_spec=template_spec,
                input_dir=input_dir,
                database_dir=database_dir,
                output_root=output_root,
                run_id=run_id,
                available_rooms=available_rooms,
                debug=debug,
            )
            st.session_state[LAST_ANALYSIS_RESULT_SESSION_KEY] = run_analysis_action(config)


def _build_run_config(
    *,
    state: AnalysisWizardState,
    template_defaults: dict[str, object],
    template_spec: dict[str, object],
    input_dir: str,
    database_dir: str,
    output_root: str,
    run_id: str,
    available_rooms: list[str],
    debug: bool,
):
    view = "bar" if state.load_subcommand == "bar" else state.view or None
    plot_template_options = {}
    command = normalize_command(state.command, streamlit=True)
    if command == PLOT_TEMPLATE_STEP:
        plot_template_options = _build_plot_template_options_for_run(
            state,
            template_defaults,
            plot_template_supports_overlays(template_spec),
        )
    rooms = _resolved_rooms_for_run(state, available_rooms, template_spec)
    return build_analysis_config(
        step=backend_command(command),
        input_dir=input_dir,
        database_dir=database_dir,
        output_root=output_root,
        run_id=run_id,
        variants="" if state.analysis_scope == "Alle Varianten" else ",".join(state.selected_variants),
        analysis_scope=state.analysis_scope,
        rooms=",".join(rooms),
        debug=debug,
        export_format=state.prepare_export_format or "csv",
        comfort_output_type=state.comfort_type or None,
        view=view,
        month=state.month,
        week=state.week,
        day=state.day,
        variant_mode=state.variant_mode or None,
        series_layout=state.series_layout or None,
        plot_template=state.plot_template if command == PLOT_TEMPLATE_STEP else None,
        plot_template_mode=state.plot_template_mode or "single",
        plot_template_options=plot_template_options,
    )


def render() -> None:
    """Zeigt die ma_analyse-Bedienung als eingeklappte Schrittstruktur."""
    render_page_header("Analyse", "Simulationsergebnisanalyse")
    _render_tkinter_launcher()

    input_dir, database_dir, output_root, run_id = _advanced_path_values()
    available_rooms = list_analysis_rooms()

    current_template = str(st.session_state.get(PLOT_TEMPLATE_WIDGET_KEY, HEATING_YEAR_TEMPLATE) or HEATING_YEAR_TEMPLATE)
    template_defaults = get_plot_template_ui_defaults(current_template)
    template_spec = get_plot_template_ui_spec(current_template)

    current_command = normalize_command(str(st.session_state.get(COMMAND_WIDGET_KEY, "") or ""), streamlit=True)
    available_variants = list_analysis_variants(current_command, input_dir, database_dir) if current_command else []
    state = _current_wizard_state(
        available_variants=available_variants,
        available_rooms=available_rooms,
        template_spec=template_spec,
    )

    first_open_step = first_incomplete_step(state) or "run"
    for section in ANALYSIS_SECTION_ORDER:
        if section == "run":
            continue
        if section == "overlays" and not section_relevant(state, section):
            continue
        _render_section(
            section=section,
            state=state,
            expanded=section == first_open_step,
            template_defaults=template_defaults,
            template_spec=template_spec,
            input_dir=input_dir,
            database_dir=database_dir,
            output_root=output_root,
            run_id=run_id,
            available_variants=available_variants,
            available_rooms=available_rooms,
        )

        current_template = str(st.session_state.get(PLOT_TEMPLATE_WIDGET_KEY, current_template) or current_template)
        template_defaults = get_plot_template_ui_defaults(current_template)
        template_spec = get_plot_template_ui_spec(current_template)
        current_command = normalize_command(str(st.session_state.get(COMMAND_WIDGET_KEY, "") or ""), streamlit=True)
        available_variants = list_analysis_variants(current_command, input_dir, database_dir) if current_command else []
        state = _current_wizard_state(
            available_variants=available_variants,
            available_rooms=available_rooms,
            template_spec=template_spec,
        )

    input_dir, database_dir, output_root, run_id = _advanced_path_values()
    _render_run_section(
        state=state,
        template_defaults=template_defaults,
        template_spec=template_spec,
        input_dir=input_dir,
        database_dir=database_dir,
        output_root=output_root,
        run_id=run_id,
        available_rooms=available_rooms,
    )

    result = st.session_state.get(LAST_ANALYSIS_RESULT_SESSION_KEY)
    if result is not None:
        render_analysis_result(result)
