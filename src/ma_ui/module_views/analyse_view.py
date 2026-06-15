"""Analyse-View fuer ma_analyse."""

from __future__ import annotations

from pathlib import Path
from typing import Any, MutableMapping

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
from ma_analyse.analysis_wizard import (
    ANALYSIS_SCOPE_OPTIONS,
    COMFORT_ANALYSIS_LEVEL_OPTIONS,
    COMMAND_OPTIONS,
    EXPORT_FORMAT_OPTIONS,
    LOAD_SUBCOMMAND_OPTIONS,
    LOAD_VIEW_OPTIONS,
    PLOT_TEMPLATE_SCOPE_OPTIONS,
    SERIES_LAYOUT_OPTIONS,
    VARIANT_MODE_OPTIONS,
    AnalysisWizardState,
    allowed_comfort_outputs,
    analysis_step_complete,
    analysis_step_summary,
    command_label,
    first_incomplete_step,
    normalize_command,
    visible_analysis_steps,
)
from ma_analyse.core.config import DATENBANK_DIR, INPUT_DIR, OUTPUT_DIR
from ma_analyse.models import AnalysisConfig
from ma_analyse.services import (
    get_plot_template_ui_defaults,
    get_plot_template_ui_spec,
    list_analysis_rooms,
    list_analysis_variants,
)
from ma_ui.components import render_analysis_result
from ma_ui.legacy_launchers import launch_tkinter_analyse
from ma_ui.shared.layout import render_page_header
from ma_workflow import run_analysis_action

PLOT_TEMPLATE_STEP = "plot-template"
DEFAULT_COMMAND_INDEX = COMMAND_OPTIONS.index(PLOT_TEMPLATE_STEP)
FREE_OVERLAY_LINES_SESSION_KEY = "ma_ui_plot_template_free_overlay_lines"
LAST_ANALYSIS_RESULT_SESSION_KEY = "ma_ui_last_analysis_result"
ACTIVE_ANALYSIS_STEP_SESSION_KEY = "ma_ui_analysis_active_step"
LAST_ANALYSIS_COMMAND_SESSION_KEY = "ma_ui_analysis_last_command"
PLOT_TEMPLATE_OPTIONS_SESSION_KEY = "ma_ui_plot_template_options"
COMMAND_WIDGET_KEY = "ma_ui_analysis_command"
LOAD_SUBCOMMAND_WIDGET_KEY = "ma_ui_analysis_load_subcommand"
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
ANALYSIS_SCOPE_WIDGET_KEY = "ma_ui_analysis_scope"
VARIANT_SELECT_WIDGET_KEY = "ma_ui_analysis_selected_variants"
VARIANT_SINGLE_WIDGET_KEY = "ma_ui_analysis_selected_variant"
VARIANT_MULTI_WIDGET_KEY = "ma_ui_analysis_selected_variants"
VARIANT_MANUAL_WIDGET_KEY = "ma_ui_analysis_manual_variants"
ROOM_SELECT_WIDGET_KEY = "ma_ui_analysis_selected_rooms"
ROOM_SINGLE_WIDGET_KEY = "ma_ui_analysis_selected_room"
ROOM_MULTI_WIDGET_KEY = "ma_ui_analysis_selected_rooms"
ROOM_MANUAL_WIDGET_KEY = "ma_ui_analysis_manual_rooms"
DEBUG_WIDGET_KEY = "ma_ui_analysis_debug"
FIXED_OVERLAY_LABELS = {
    "outdoor_temperature": "Aussenlufttemperatur",
    "operative_temperature": "Operative Temperatur",
}


def split_csv_text(value: str) -> list[str]:
    """Wandelt eine kommaseparierte UI-Eingabe in eine Liste um."""
    return [item.strip() for item in value.split(",") if item.strip()]


def optional_text(value: str) -> str | None:
    """Normalisiert leere Textfelder auf None."""
    stripped = value.strip()
    return stripped or None


def variant_selection_from_scope(value: str, analysis_scope: str) -> list[str] | None:
    """Leitet die Variantenauswahl aus Analyseumfang und Texteingabe ab."""
    if analysis_scope == "Alle Varianten":
        return None
    return split_csv_text(value)


def variant_text_from_selection(analysis_scope: str, selected_variants: list[str], manual_value: str) -> str:
    """Baut die Varianteneingabe aus Auswahlfeld oder manueller Eingabe."""
    if analysis_scope == "Alle Varianten":
        return ""
    if selected_variants:
        if analysis_scope == "Eine Variante":
            return selected_variants[0]
        return ",".join(selected_variants)
    return manual_value


def room_text_from_selection(selected_rooms: list[str], manual_value: str) -> str:
    """Baut die Raumeingabe aus Auswahlfeld oder manueller Eingabe."""
    if selected_rooms:
        return ",".join(selected_rooms)
    return manual_value


def first_selected_value(selected_values: list[str], fallback_values: list[str]) -> str | None:
    """Waehlt einen stabilen Referenzwert fuer optionale Katalogabfragen."""
    if selected_values:
        return selected_values[0]
    if fallback_values:
        return fallback_values[0]
    return None


def plot_template_view(template_spec: dict[str, object]) -> str:
    """Liest die Zeitlogik aus der Template-Spezifikation."""
    return str(template_spec.get("view") or "")


def plot_template_supports_overlays(template_spec: dict[str, object]) -> bool:
    """Prueft, ob feste und freie Overlays fuer ein Template sichtbar sein sollen."""
    return bool(template_spec.get("supports_overlays", False))


def plot_template_requires_single_room(template_spec: dict[str, object]) -> bool:
    """Prueft, ob die Streamlit-Auswahl auf genau einen Raum begrenzt wird."""
    return bool(template_spec.get("requires_single_room", True))


def build_template_time_options(
    template_spec: dict[str, object],
    *,
    month: str | None = None,
    week: int | None = None,
    day: int | None = None,
) -> dict[str, str | int | None]:
    """Gibt nur die Zeitfelder weiter, die das Template wirklich erwartet."""
    view = plot_template_view(template_spec)
    return {
        "month": month if view in {"month", "day"} else None,
        "week": week if view == "week" else None,
        "day": day if view == "day" else None,
    }


def room_values_from_template_selection(
    *,
    selected_rooms: list[str],
    manual_value: str,
    template_spec: dict[str, object],
) -> list[str]:
    """Normalisiert die Raumauswahl passend zur Template-Spezifikation."""
    rooms = split_csv_text(room_text_from_selection(selected_rooms, manual_value))
    if plot_template_requires_single_room(template_spec):
        return rooms[:1]
    return rooms


def _normalize_overlay_line(raw_line: dict[str, object]) -> dict[str, str] | None:
    source = str(raw_line.get("source") or "").strip()
    column = str(raw_line.get("column") or "").strip()
    label = str(raw_line.get("label") or "").strip() or column
    axis = str(raw_line.get("axis") or "").strip()
    return build_catalog_overlay_line(source, column, label, axis)


def get_session_overlay_lines(
    session_state: MutableMapping[str, Any] | None = None,
) -> list[dict[str, str]]:
    """Liest freie Overlay-Linien aus einem Session-State-kompatiblen Mapping."""
    state = st.session_state if session_state is None else session_state
    raw_lines = state.get(FREE_OVERLAY_LINES_SESSION_KEY, [])
    if not isinstance(raw_lines, list):
        return []

    normalized = [_normalize_overlay_line(raw_line) for raw_line in raw_lines if isinstance(raw_line, dict)]
    return [line for line in normalized if line is not None]


def add_session_overlay_line(
    line: dict[str, str],
    session_state: MutableMapping[str, Any] | None = None,
) -> bool:
    """Fuegt eine freie Overlay-Linie hinzu und vermeidet Dubletten."""
    state = st.session_state if session_state is None else session_state
    normalized_line = _normalize_overlay_line(line)
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


def _default_float(defaults: dict[str, object], key: str, fallback: float) -> float:
    try:
        return float(defaults.get(key, fallback))
    except (TypeError, ValueError):
        return fallback


def _default_bool(defaults: dict[str, object], key: str, fallback: bool) -> bool:
    value = defaults.get(key, fallback)
    return value if isinstance(value, bool) else fallback


def _default_text(defaults: dict[str, object], key: str, fallback: str) -> str:
    value = defaults.get(key, fallback)
    return value.strip() if isinstance(value, str) and value.strip() else fallback


def _default_fixed_overlays(defaults: dict[str, object]) -> list[dict[str, object]]:
    raw_overlays = defaults.get("default_overlays", [])
    if not isinstance(raw_overlays, list):
        return []
    return [overlay for overlay in raw_overlays if isinstance(overlay, dict)]


def build_catalog_overlay_line(source: str, column: str, label: str, axis: str) -> dict[str, str] | None:
    """Baut eine Overlay-Zeile aus Katalogauswahlwerten."""
    if source not in {"csv", "aux"} or axis not in {"heat", "temperature"} or not column:
        return None
    return {
        "source": source,
        "column": column,
        "label": label.strip() or column,
        "axis": axis,
    }


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


def parse_overlay_lines_text(value: str) -> list[dict[str, str]]:
    """Liest freie Overlay-Linien aus einfachen CSV-Textzeilen.

    Format je Zeile: source,column,label,axis
    source: csv oder aux
    axis: heat oder temperature
    """
    overlay_lines: list[dict[str, str]] = []
    for raw_line in value.splitlines():
        parts = [part.strip() for part in raw_line.split(",")]
        if len(parts) != 4:
            continue
        source, column, label, axis = parts
        if source not in {"csv", "aux"} or axis not in {"heat", "temperature"} or not column:
            continue
        overlay_lines.append(
            {
                "source": source,
                "column": column,
                "label": label or column,
                "axis": axis,
            }
        )
    return overlay_lines


def build_plot_template_options(
    *,
    template: str,
    month: str | None = None,
    week: int | None = None,
    day: int | None = None,
    show_setpoint_band: bool = DEFAULT_SHOW_SETPOINT_BAND,
    show_outdoor_temperature: bool = DEFAULT_SHOW_OUTDOOR_TEMPERATURE,
    show_operative_temperature: bool = DEFAULT_SHOW_OPERATIVE_TEMPERATURE,
    setpoint_min: float = DEFAULT_SETPOINT_MIN,
    setpoint_max: float = DEFAULT_SETPOINT_MAX,
    temperature_ymin: float = DEFAULT_TEMPERATURE_YMIN,
    temperature_ymax: float = DEFAULT_TEMPERATURE_YMAX,
    outdoor_column: str = DEFAULT_OUTDOOR_COLUMN,
    overlay_lines: list[dict[str, str]] | None = None,
    fixed_overlays: list[dict[str, object]] | None = None,
) -> dict[str, Any]:
    """Baut die UI-neutralen Plot-Template-Optionen fuer AnalysisConfig."""
    return {
        "template": template,
        "month": month,
        "week": week,
        "day": day,
        "show_setpoint_band": show_setpoint_band,
        "show_outdoor_temperature": show_outdoor_temperature,
        "show_operative_temperature": show_operative_temperature,
        "setpoint_min": setpoint_min,
        "setpoint_max": setpoint_max,
        "temperature_ymin": temperature_ymin,
        "temperature_ymax": temperature_ymax,
        "outdoor_column": outdoor_column,
        "overlay_lines": overlay_lines or [],
        "fixed_overlays": fixed_overlays or [],
    }


def build_analysis_config(
    *,
    step: str,
    input_dir: str,
    database_dir: str,
    output_root: str,
    run_id: str,
    variants: str,
    rooms: str,
    debug: bool,
    analysis_scope: str = "Mehrere Varianten",
    export_format: str = "csv",
    comfort_output_type: str | None = None,
    view: str | None = None,
    month: str | None = None,
    week: int | None = None,
    day: int | None = None,
    variant_mode: str | None = None,
    series_layout: str | None = None,
    plot_template: str | None = None,
    plot_template_options: dict[str, Any] | None = None,
) -> AnalysisConfig:
    """Baut den UI-neutralen Analyseauftrag aus Formularwerten."""
    return AnalysisConfig(
        steps=(step,),
        input_dir=Path(input_dir),
        database_dir=Path(database_dir),
        output_root=Path(output_root),
        run_id=optional_text(run_id),
        variants=variant_selection_from_scope(variants, analysis_scope),
        rooms=split_csv_text(rooms),
        debug=debug,
        export_format=export_format,
        comfort_output_type=comfort_output_type,
        view=view,
        month=month,
        week=week,
        day=day,
        variant_mode=variant_mode,
        series_layout=series_layout,
        plot_template=plot_template,
        plot_template_options=plot_template_options or {},
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


def _render_tkinter_legacy_launcher() -> None:
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
    temperature_ymin = _default_float(template_defaults, "temperature_ymin", DEFAULT_TEMPERATURE_YMIN)
    temperature_ymax = _default_float(template_defaults, "temperature_ymax", DEFAULT_TEMPERATURE_YMAX)
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
        with st.expander("Overlay- und Achsoptionen", expanded=True):
            show_setpoint_band = st.checkbox("Sollwertband anzeigen", value=show_setpoint_band)
            show_outdoor_temperature = st.checkbox("Aussenlufttemperatur anzeigen", value=show_outdoor_temperature)
            show_operative_temperature = st.checkbox(
                "Operative Temperatur anzeigen",
                value=show_operative_temperature,
            )
            setpoint_min = st.number_input("Sollwert min [C]", value=float(setpoint_min))
            setpoint_max = st.number_input("Sollwert max [C]", value=float(setpoint_max))
            temperature_ymin = st.number_input("Temperaturachse min [C]", value=float(temperature_ymin))
            temperature_ymax = st.number_input("Temperaturachse max [C]", value=float(temperature_ymax))
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
    )


def _selectbox_index(options: tuple[str, ...], value: object) -> int:
    text_value = str(value or "")
    return options.index(text_value) if text_value in options else 0


def _reset_downstream_analysis_state() -> None:
    """Entfernt alte Auswahlen, wenn der Hauptbefehl gewechselt wurde."""
    for key in (
        LOAD_SUBCOMMAND_WIDGET_KEY,
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
        VARIANT_SINGLE_WIDGET_KEY,
        VARIANT_MULTI_WIDGET_KEY,
        VARIANT_MANUAL_WIDGET_KEY,
        ROOM_SINGLE_WIDGET_KEY,
        ROOM_MULTI_WIDGET_KEY,
        ROOM_MANUAL_WIDGET_KEY,
        PLOT_TEMPLATE_OPTIONS_SESSION_KEY,
    ):
        st.session_state.pop(key, None)


def _sync_command_change() -> None:
    command = normalize_command(str(st.session_state.get(COMMAND_WIDGET_KEY, "") or ""))
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
    analysis_level: str,
    available_rooms: list[str],
    template_spec: dict[str, object],
) -> tuple[str, ...]:
    if command == "comfort" and analysis_level == "Analyse Variante":
        return tuple(available_rooms)
    if command == PLOT_TEMPLATE_STEP and plot_template_requires_single_room(template_spec):
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
    command = normalize_command(str(st.session_state.get(COMMAND_WIDGET_KEY, "") or ""))
    analysis_scope = str(st.session_state.get(ANALYSIS_SCOPE_WIDGET_KEY, "") or "")
    analysis_level = str(st.session_state.get(ANALYSIS_LEVEL_WIDGET_KEY, "") or "")
    selected_variants = _selected_variants_from_state(analysis_scope, available_variants)
    selected_rooms = _selected_rooms_from_state(
        command=command,
        analysis_level=analysis_level,
        available_rooms=available_rooms,
        template_spec=template_spec,
    )
    overlay_options = st.session_state.get(PLOT_TEMPLATE_OPTIONS_SESSION_KEY, {})
    overlay_lines = overlay_options.get("overlay_lines", []) if isinstance(overlay_options, dict) else []

    return AnalysisWizardState(
        command=command,
        load_subcommand=str(st.session_state.get(LOAD_SUBCOMMAND_WIDGET_KEY, "") or ""),
        prepare_export_format=str(st.session_state.get(PREPARE_EXPORT_WIDGET_KEY, "") or ""),
        comfort_type=str(st.session_state.get(COMFORT_TYPE_WIDGET_KEY, "") or ""),
        analysis_level=analysis_level,
        variant_mode=str(st.session_state.get(VARIANT_MODE_WIDGET_KEY, "") or ""),
        series_layout=str(st.session_state.get(SERIES_LAYOUT_WIDGET_KEY, "") or ""),
        view=str(st.session_state.get(LOAD_VIEW_WIDGET_KEY, "") or ""),
        month=str(st.session_state.get(MONTH_WIDGET_KEY, "") or "") or None,
        week=_int_session_value(WEEK_WIDGET_KEY),
        day=_int_session_value(DAY_WIDGET_KEY),
        plot_template=str(st.session_state.get(PLOT_TEMPLATE_WIDGET_KEY, HEATING_YEAR_TEMPLATE) or HEATING_YEAR_TEMPLATE),
        analysis_scope=analysis_scope,
        selected_variants=selected_variants,
        selected_rooms=selected_rooms,
        variant_count=len(available_variants),
        overlay_count=len(overlay_lines) if isinstance(overlay_lines, list) else 0,
        show_setpoint_band=bool(overlay_options.get("show_setpoint_band", False)) if isinstance(overlay_options, dict) else False,
        show_outdoor_temperature=bool(overlay_options.get("show_outdoor_temperature", False))
        if isinstance(overlay_options, dict)
        else False,
        show_operative_temperature=bool(overlay_options.get("show_operative_temperature", False))
        if isinstance(overlay_options, dict)
        else False,
    )


def _room_selection_disabled(state: AnalysisWizardState) -> bool:
    return normalize_command(state.command) == "comfort" and state.analysis_level == "Analyse Variante"


def _render_advanced_paths() -> tuple[str, str, str, str]:
    with st.expander("Erweiterte Pfade", expanded=False):
        input_dir = st.text_input("IDA-Importordner", value=str(INPUT_DIR))
        database_dir = st.text_input("Datenbankordner", value=str(DATENBANK_DIR))
        output_root = st.text_input("Ausgabeordner", value=str(OUTPUT_DIR))
        run_id = st.text_input("Run-ID", value="")
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
        options = ("", *COMFORT_ANALYSIS_LEVEL_OPTIONS)
        st.selectbox(
            "Analyseebene",
            options=options,
            index=_selectbox_index(options, st.session_state.get(ANALYSIS_LEVEL_WIDGET_KEY)),
            key=ANALYSIS_LEVEL_WIDGET_KEY,
        )
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
        show_setpoint_band=_default_bool(template_defaults, "show_setpoint_band", False),
        show_outdoor_temperature=_default_bool(template_defaults, "show_outdoor_temperature", False),
        show_operative_temperature=_default_bool(template_defaults, "show_operative_temperature", False),
        setpoint_min=_default_float(template_defaults, "setpoint_min", DEFAULT_SETPOINT_MIN),
        setpoint_max=_default_float(template_defaults, "setpoint_max", DEFAULT_SETPOINT_MAX),
        temperature_ymin=_default_float(template_defaults, "temperature_ymin", DEFAULT_TEMPERATURE_YMIN),
        temperature_ymax=_default_float(template_defaults, "temperature_ymax", DEFAULT_TEMPERATURE_YMAX),
        outdoor_column=_default_text(template_defaults, "outdoor_column", DEFAULT_OUTDOOR_COLUMN),
        fixed_overlays=_default_fixed_overlays(template_defaults),
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
    if _room_selection_disabled(state):
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
    if template_supports_overlays:
        stored_options = st.session_state.get(PLOT_TEMPLATE_OPTIONS_SESSION_KEY)
        if isinstance(stored_options, dict):
            return stored_options
    return _build_plot_template_options_from_state(state, template_defaults)


def render() -> None:
    """Zeigt die ma_analyse-Bedienung als schrittweisen Wizard."""
    render_page_header("Analyse", "Simulationsergebnisanalyse")
    _render_tkinter_legacy_launcher()

    input_dir, database_dir, output_root, run_id = _render_advanced_paths()
    available_rooms = list_analysis_rooms()

    current_template = str(st.session_state.get(PLOT_TEMPLATE_WIDGET_KEY, HEATING_YEAR_TEMPLATE) or HEATING_YEAR_TEMPLATE)
    template_defaults = get_plot_template_ui_defaults(current_template)
    template_spec = get_plot_template_ui_spec(current_template)
    template_view = plot_template_view(template_spec)
    template_supports_overlays = plot_template_supports_overlays(template_spec)

    current_command = normalize_command(str(st.session_state.get(COMMAND_WIDGET_KEY, "") or ""))
    available_variants = list_analysis_variants(current_command, input_dir, database_dir) if current_command else []
    state = _current_wizard_state(
        available_variants=available_variants,
        available_rooms=available_rooms,
        template_spec=template_spec,
    )
    visible_steps = visible_analysis_steps(state, template_supports_overlays=template_supports_overlays)
    active_step = str(st.session_state.get(ACTIVE_ANALYSIS_STEP_SESSION_KEY, "command") or "command")
    if active_step not in visible_steps:
        active_step = first_incomplete_step(
            state,
            visible_steps,
            template_view=template_view,
            room_selection_disabled=_room_selection_disabled(state),
        )
        st.session_state[ACTIVE_ANALYSIS_STEP_SESSION_KEY] = active_step
    else:
        first_open_step = first_incomplete_step(
            state,
            visible_steps,
            template_view=template_view,
            room_selection_disabled=_room_selection_disabled(state),
        )
        if visible_steps.index(first_open_step) < visible_steps.index(active_step):
            active_step = first_open_step
            st.session_state[ACTIVE_ANALYSIS_STEP_SESSION_KEY] = active_step

    _render_step_summaries(
        visible_steps=visible_steps,
        active_step=active_step,
        state=state,
        template_view=template_view,
    )
    _render_active_step(
        active_step=active_step,
        state=state,
        template_defaults=template_defaults,
        template_spec=template_spec,
        input_dir=input_dir,
        database_dir=database_dir,
        available_variants=available_variants,
        available_rooms=available_rooms,
    )

    current_template = str(st.session_state.get(PLOT_TEMPLATE_WIDGET_KEY, current_template) or current_template)
    template_defaults = get_plot_template_ui_defaults(current_template)
    template_spec = get_plot_template_ui_spec(current_template)
    template_view = plot_template_view(template_spec)
    template_supports_overlays = plot_template_supports_overlays(template_spec)
    state = _current_wizard_state(
        available_variants=available_variants,
        available_rooms=available_rooms,
        template_spec=template_spec,
    )
    visible_steps = visible_analysis_steps(state, template_supports_overlays=template_supports_overlays)
    room_selection_disabled = _room_selection_disabled(state)
    _render_step_navigation(
        active_step=active_step,
        visible_steps=visible_steps,
        state=state,
        template_view=template_view,
        room_selection_disabled=room_selection_disabled,
    )

    ready = _analysis_ready(
        state,
        visible_steps,
        template_view=template_view,
        room_selection_disabled=room_selection_disabled,
    )
    if ready and active_step == visible_steps[-1]:
        st.divider()
        debug = st.checkbox("Debug-Ausgabe", value=False, key=DEBUG_WIDGET_KEY)
        if st.button("Analyse starten", type="primary"):
            view = "bar" if state.load_subcommand == "bar" else state.view or None
            plot_template_options = {}
            if normalize_command(state.command) == PLOT_TEMPLATE_STEP:
                plot_template_options = _build_plot_template_options_for_run(
                    state,
                    template_defaults,
                    template_supports_overlays,
                )
            config = build_analysis_config(
                step=normalize_command(state.command),
                input_dir=input_dir,
                database_dir=database_dir,
                output_root=output_root,
                run_id=run_id,
                variants="" if state.analysis_scope == "Alle Varianten" else ",".join(state.selected_variants),
                analysis_scope=state.analysis_scope,
                rooms=",".join(state.selected_rooms),
                debug=debug,
                export_format=state.prepare_export_format or "csv",
                comfort_output_type=state.comfort_type or None,
                view=view,
                month=state.month,
                week=state.week,
                day=state.day,
                variant_mode=state.variant_mode or None,
                series_layout=state.series_layout or None,
                plot_template=state.plot_template if normalize_command(state.command) == PLOT_TEMPLATE_STEP else None,
                plot_template_options=plot_template_options,
            )
            st.session_state[LAST_ANALYSIS_RESULT_SESSION_KEY] = run_analysis_action(config)

    result = st.session_state.get(LAST_ANALYSIS_RESULT_SESSION_KEY)
    if result is not None:
        render_analysis_result(result)
