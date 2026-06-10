"""Analyse-View fuer ma_analyse."""

from __future__ import annotations

from pathlib import Path
from typing import Any

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
from ma_analyse.services import list_analysis_rooms, list_analysis_variants
from ma_ui.components import render_analysis_result
from ma_ui.shared.layout import render_page_header
from ma_workflow import run_analysis_action

COMMAND_OPTIONS = ("prepare", "comfort", "analysis", "analyze-data", "heating", "cooling", "plot-template", "all")
ANALYSIS_SCOPE_OPTIONS = ("Eine Variante", "Mehrere Varianten", "Alle Varianten")
COMMAND_LABELS = {
    "prepare": "prepare - Rohdaten aufbereiten",
    "comfort": "comfort - Komfortausgaben",
    "analysis": "analysis - Behaglichkeitsanalyse",
    "analyze-data": "analyze-data - Excel-Auswertung",
    "heating": "heating - Heizleistung",
    "cooling": "cooling - Kuehlleistung",
    "plot-template": "plot-template - Diagrammvorlagen",
    "all": "all - Standardprofil",
}
EXPORT_FORMAT_OPTIONS = ("csv", "excel", "both")
COMFORT_OUTPUT_OPTIONS = ("plot", "plot_overview", "plot_analysis", "plot_analysis_overview")
LOAD_VIEW_OPTIONS = ("bar", "year", "month", "week", "day")
VARIANT_MODE_OPTIONS = ("compare", "single")
SERIES_LAYOUT_OPTIONS = ("separate", "combined")


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


def _render_plot_template_options(
    *,
    input_dir: str,
    database_dir: str,
    selected_variants: list[str],
    available_variants: list[str],
    selected_rooms: list[str],
) -> tuple[str, dict[str, Any]]:
    template = st.selectbox("Template", options=PLOT_TEMPLATE_CHOICES, index=PLOT_TEMPLATE_CHOICES.index(HEATING_YEAR_TEMPLATE))
    time_view = st.selectbox("Zeitfilter", options=("none", "month", "week", "day"), index=0)
    month, week, day = _render_time_options("Template", time_view) if time_view != "none" else (None, None, None)
    overlay_lines: list[dict[str, str]] = []

    with st.expander("Overlay- und Achsoptionen"):
        show_setpoint_band = st.checkbox("Sollwertband anzeigen", value=DEFAULT_SHOW_SETPOINT_BAND)
        show_outdoor_temperature = st.checkbox("Aussenlufttemperatur anzeigen", value=DEFAULT_SHOW_OUTDOOR_TEMPERATURE)
        show_operative_temperature = st.checkbox("Operative Temperatur anzeigen", value=DEFAULT_SHOW_OPERATIVE_TEMPERATURE)
        setpoint_min = st.number_input("Sollwert min [C]", value=float(DEFAULT_SETPOINT_MIN))
        setpoint_max = st.number_input("Sollwert max [C]", value=float(DEFAULT_SETPOINT_MAX))
        temperature_ymin = st.number_input("Temperaturachse min [C]", value=float(DEFAULT_TEMPERATURE_YMIN))
        temperature_ymax = st.number_input("Temperaturachse max [C]", value=float(DEFAULT_TEMPERATURE_YMAX))
        outdoor_column = st.text_input("Aussenluft-Spalte", value=DEFAULT_OUTDOOR_COLUMN)
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
            catalog_source = st.selectbox("Overlay-Quelle aus Katalog", options=("csv", "aux"))
            catalog_columns = overlay_catalog.get(catalog_source, [])
            if catalog_columns:
                catalog_column = st.selectbox("Overlay-Spalte aus Katalog", options=catalog_columns)
                catalog_axis = st.selectbox("Overlay-Achse", options=("heat", "temperature"), index=0)
                catalog_label = st.text_input("Overlay-Label", value=catalog_column)
                if st.checkbox("Katalog-Overlay uebernehmen", value=False):
                    catalog_line = build_catalog_overlay_line(
                        source=catalog_source,
                        column=catalog_column,
                        label=catalog_label,
                        axis=catalog_axis,
                    )
                    if catalog_line:
                        overlay_lines.append(catalog_line)
            else:
                st.caption("Fuer diese Quelle wurden keine nutzbaren Spalten gefunden.")
        else:
            st.caption("Kein Overlay-Katalog gefunden. Freie Overlay-Linien koennen weiter manuell eingegeben werden.")

        overlay_lines_text = st.text_area(
            "Freie Overlay-Linien",
            value="",
            help="Format je Zeile: source,column,label,axis. source: csv/aux, axis: heat/temperature.",
        )
        overlay_lines.extend(parse_overlay_lines_text(overlay_lines_text))

    return template, build_plot_template_options(
        template=template,
        month=month,
        week=week,
        day=day,
        show_setpoint_band=show_setpoint_band,
        show_outdoor_temperature=show_outdoor_temperature,
        show_operative_temperature=show_operative_temperature,
        setpoint_min=float(setpoint_min),
        setpoint_max=float(setpoint_max),
        temperature_ymin=float(temperature_ymin),
        temperature_ymax=float(temperature_ymax),
        outdoor_column=outdoor_column,
        overlay_lines=overlay_lines,
    )


def render() -> None:
    """Zeigt eine Analysemaske ohne eigene Fachlogik."""
    render_page_header("Analyse", "Simulationsergebnisanalyse")

    with st.form("analysis_form"):
        step = st.selectbox(
            "Analyseschritt",
            options=COMMAND_OPTIONS,
            index=0,
            format_func=lambda value: COMMAND_LABELS[value],
        )

        st.subheader("Pfade und Auswahl")
        input_dir = st.text_input("IDA-Importordner", value="data/ma_analyse/ida_imports")
        database_dir = st.text_input("Datenbankordner", value="data/ma_analyse/database")
        output_root = st.text_input("Ausgabeordner", value="data/ma_analyse/output")
        run_id = st.text_input("Run-ID", value="")
        analysis_scope = st.selectbox("Analyseumfang", options=ANALYSIS_SCOPE_OPTIONS, index=1)

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
                selected_variants = st.multiselect("Varianten", options=available_variants)
        else:
            manual_variants = st.text_input("Varianten", value="")
        variants = variant_text_from_selection(analysis_scope, selected_variants, manual_variants)

        available_rooms = list_analysis_rooms()
        default_rooms = ["208 office"] if "208 office" in available_rooms else available_rooms[:1]
        selected_rooms = st.multiselect("Raeume", options=available_rooms, default=default_rooms)
        manual_rooms = st.text_input("Raeume manuell", value="")
        rooms = room_text_from_selection(selected_rooms, manual_rooms)
        debug = st.checkbox("Debug-Ausgabe", value=False)

        export_format = "csv"
        comfort_output_type = None
        analysis_series_layout = None
        load_options: dict[str, object] = {}
        plot_template = None
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
        elif step == "plot-template":
            plot_template, plot_template_options = _render_plot_template_options(
                input_dir=input_dir,
                database_dir=database_dir,
                selected_variants=selected_variants,
                available_variants=available_variants,
                selected_rooms=selected_rooms,
            )
        else:
            st.caption("Fuer diesen Schritt werden aktuell keine weiteren Optionen abgefragt.")

        submitted = st.form_submit_button("Analyse starten")

    if not submitted:
        return

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
    result = run_analysis_action(config)

    render_analysis_result(result)
