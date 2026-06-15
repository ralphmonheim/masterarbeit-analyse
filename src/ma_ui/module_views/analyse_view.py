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
COMMAND_OPTIONS = ("prepare", "comfort", "analysis", "analyze-data", "heating", "cooling", PLOT_TEMPLATE_STEP, "all")
ANALYSIS_SCOPE_OPTIONS = ("Eine Variante", "Mehrere Varianten", "Alle Varianten")
PLOT_TEMPLATE_SCOPE_OPTIONS = ("Eine Variante", "Mehrere Varianten")
COMMAND_LABELS = {
    "prepare": "prepare - Rohdaten aufbereiten",
    "comfort": "comfort - Komfortausgaben",
    "analysis": "analysis - Behaglichkeitsanalyse",
    "analyze-data": "analyze-data - Excel-Auswertung",
    "heating": "heating - Heizleistung",
    "cooling": "cooling - Kuehlleistung",
    PLOT_TEMPLATE_STEP: "plot-template - Diagrammvorlagen",
    "all": "all - Standardprofil",
}
EXPORT_FORMAT_OPTIONS = ("csv", "excel", "both")
COMFORT_OUTPUT_OPTIONS = ("plot", "plot_overview", "plot_analysis", "plot_analysis_overview")
LOAD_VIEW_OPTIONS = ("bar", "year", "month", "week", "day")
VARIANT_MODE_OPTIONS = ("compare", "single")
SERIES_LAYOUT_OPTIONS = ("separate", "combined")
DEFAULT_COMMAND_INDEX = COMMAND_OPTIONS.index(PLOT_TEMPLATE_STEP)
FREE_OVERLAY_LINES_SESSION_KEY = "ma_ui_plot_template_free_overlay_lines"
LAST_ANALYSIS_RESULT_SESSION_KEY = "ma_ui_last_analysis_result"
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
        month = st.selectbox(f"{prefix} Monat", options=MONTH_NAMES, index=0)

    if view == "week":
        week = int(st.number_input(f"{prefix} Kalenderwoche", min_value=1, max_value=MAX_CALENDAR_WEEK, value=1))

    if view == "day":
        month_index = MONTH_NAMES.index(month or MONTH_NAMES[0])
        day = int(st.number_input(f"{prefix} Tag", min_value=1, max_value=MONTH_DAY_COUNTS[month_index], value=1))

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
) -> dict[str, Any]:
    view = plot_template_view(template_spec)
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


def render() -> None:
    """Zeigt eine Analysemaske ohne eigene Fachlogik."""
    render_page_header("Analyse", "Simulationsergebnisanalyse")
    _render_tkinter_legacy_launcher()

    step = st.selectbox(
        "Analyseschritt",
        options=COMMAND_OPTIONS,
        index=DEFAULT_COMMAND_INDEX,
        format_func=lambda value: COMMAND_LABELS[value],
    )

    st.subheader("Pfade und Auswahl")
    input_dir = st.text_input("IDA-Importordner", value="data/ma_analyse/ida_imports")
    database_dir = st.text_input("Datenbankordner", value="data/ma_analyse/database")
    output_root = st.text_input("Ausgabeordner", value="data/ma_analyse/output")
    run_id = st.text_input("Run-ID", value="")

    plot_template = None
    plot_template_defaults: dict[str, object] = {}
    plot_template_spec: dict[str, object] = {}
    if step == PLOT_TEMPLATE_STEP:
        plot_template = st.selectbox(
            "Template",
            options=PLOT_TEMPLATE_CHOICES,
            index=PLOT_TEMPLATE_CHOICES.index(HEATING_YEAR_TEMPLATE),
        )
        plot_template_defaults = get_plot_template_ui_defaults(plot_template)
        plot_template_spec = get_plot_template_ui_spec(plot_template)
        room_mode = "Einzelraum" if plot_template_requires_single_room(plot_template_spec) else "Mehrere Raeume"
        st.caption(
            "Template-Spezifikation: "
            f"{plot_template_spec.get('metric', '-')} / {plot_template_spec.get('view', '-')} / {room_mode}"
        )

    scope_options = PLOT_TEMPLATE_SCOPE_OPTIONS if step == PLOT_TEMPLATE_STEP else ANALYSIS_SCOPE_OPTIONS
    scope_index = 0 if step == PLOT_TEMPLATE_STEP else 1
    analysis_scope = st.selectbox("Analyseumfang", options=scope_options, index=scope_index)

    available_variants = list_analysis_variants(step, input_dir, database_dir)
    selected_variants: list[str] = []
    manual_variants = ""
    if analysis_scope == "Alle Varianten":
        st.caption(f"Alle gefundenen Varianten werden verwendet: {len(available_variants)}")
    elif available_variants:
        if analysis_scope == "Eine Variante":
            selected_variant = st.selectbox("Variante", options=available_variants, index=0)
            selected_variants = [selected_variant]
        else:
            selected_variants = st.multiselect("Varianten", options=available_variants, default=available_variants[:1])
    else:
        manual_variants = st.text_input("Varianten", value="")
    variants = variant_text_from_selection(analysis_scope, selected_variants, manual_variants)

    available_rooms = list_analysis_rooms()
    default_rooms = ["208 office"] if "208 office" in available_rooms else available_rooms[:1]
    manual_rooms = ""
    if step == PLOT_TEMPLATE_STEP and plot_template_requires_single_room(plot_template_spec):
        default_room_index = available_rooms.index(default_rooms[0]) if default_rooms else 0
        selected_room = st.selectbox("Raum", options=available_rooms, index=default_room_index)
        selected_rooms = [selected_room]
        rooms = ",".join(
            room_values_from_template_selection(
                selected_rooms=selected_rooms,
                manual_value=manual_rooms,
                template_spec=plot_template_spec,
            )
        )
    else:
        selected_rooms = st.multiselect("Raeume", options=available_rooms, default=default_rooms)
        manual_rooms = st.text_input("Raeume manuell", value="")
        if step == PLOT_TEMPLATE_STEP:
            rooms = ",".join(
                room_values_from_template_selection(
                    selected_rooms=selected_rooms,
                    manual_value=manual_rooms,
                    template_spec=plot_template_spec,
                )
            )
        else:
            rooms = room_text_from_selection(selected_rooms, manual_rooms)
    debug = st.checkbox("Debug-Ausgabe", value=False)

    export_format = "csv"
    comfort_output_type = None
    analysis_series_layout = None
    load_options: dict[str, object] = {}
    plot_template_options: dict[str, Any] = {}

    st.subheader("Befehlsspezifische Optionen")
    if step == "prepare":
        export_format = st.selectbox("Prepare-Exportformat", options=EXPORT_FORMAT_OPTIONS, index=0)
    elif step == "comfort":
        comfort_output_type = st.selectbox("Comfort-Ausgabeprofil", options=COMFORT_OUTPUT_OPTIONS, index=3)
    elif step == "analyze-data":
        analysis_series_layout = st.selectbox("Excel-Ausgabe", options=SERIES_LAYOUT_OPTIONS, index=0)
    elif step in {"heating", "cooling"}:
        load_options = _render_load_options()
    elif step == PLOT_TEMPLATE_STEP and plot_template is not None:
        plot_template_options = _render_plot_template_options(
            template=plot_template,
            template_defaults=plot_template_defaults,
            template_spec=plot_template_spec,
            input_dir=input_dir,
            database_dir=database_dir,
            selected_variants=selected_variants,
            available_variants=available_variants,
            selected_rooms=selected_rooms,
        )
    else:
        st.caption("Fuer diesen Schritt werden aktuell keine weiteren Optionen abgefragt.")

    submitted = st.button("Analyse starten", type="primary")
    if submitted:
        config = build_analysis_config(
            step=step,
            input_dir=input_dir,
            database_dir=database_dir,
            output_root=output_root,
            run_id=run_id,
            variants=variants,
            analysis_scope=analysis_scope,
            rooms=rooms,
            debug=debug,
            export_format=export_format,
            comfort_output_type=comfort_output_type,
            view=load_options.get("view"),
            month=load_options.get("month"),
            week=load_options.get("week"),
            day=load_options.get("day"),
            variant_mode=load_options.get("variant_mode"),
            series_layout=analysis_series_layout or load_options.get("series_layout"),
            plot_template=plot_template,
            plot_template_options=plot_template_options,
        )
        st.session_state[LAST_ANALYSIS_RESULT_SESSION_KEY] = run_analysis_action(config)

    result = st.session_state.get(LAST_ANALYSIS_RESULT_SESSION_KEY)
    if result is not None:
        render_analysis_result(result)
