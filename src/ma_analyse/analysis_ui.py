"""UI-neutrale Helfer fuer Analyseoberflaechen.

Dieses Modul enthaelt keine Streamlit- oder Tkinter-Imports. Es sammelt die
kleinen Transformationsregeln, die mehrere Oberflaechen nutzen koennen.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .analysis.templates import (
    DEFAULT_OUTDOOR_COLUMN,
    DEFAULT_SETPOINT_MAX,
    DEFAULT_SETPOINT_MIN,
    DEFAULT_SHOW_OPERATIVE_TEMPERATURE,
    DEFAULT_SHOW_OUTDOOR_TEMPERATURE,
    DEFAULT_SHOW_SETPOINT_BAND,
    DEFAULT_TEMPERATURE_YMAX,
    DEFAULT_TEMPERATURE_YMIN,
)
from .models import AnalysisConfig


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


def normalize_overlay_line(raw_line: dict[str, object]) -> dict[str, str] | None:
    """Normalisiert eine freie Overlay-Zeile fuer Session-State und Config."""
    source = str(raw_line.get("source") or "").strip()
    column = str(raw_line.get("column") or "").strip()
    label = str(raw_line.get("label") or "").strip() or column
    axis = str(raw_line.get("axis") or "").strip()
    return build_catalog_overlay_line(source, column, label, axis)


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
        line = build_catalog_overlay_line(source, column, label, axis)
        if line is not None:
            overlay_lines.append(line)
    return overlay_lines


def coerce_float_default(defaults: dict[str, object], key: str, fallback: float) -> float:
    """Liest einen numerischen Default robust aus Template-Defaults."""
    try:
        return float(defaults.get(key, fallback))
    except (TypeError, ValueError):
        return fallback


def coerce_bool_default(defaults: dict[str, object], key: str, fallback: bool) -> bool:
    """Liest einen booleschen Default robust aus Template-Defaults."""
    value = defaults.get(key, fallback)
    return value if isinstance(value, bool) else fallback


def coerce_text_default(defaults: dict[str, object], key: str, fallback: str) -> str:
    """Liest einen Text-Default robust aus Template-Defaults."""
    value = defaults.get(key, fallback)
    return value.strip() if isinstance(value, str) and value.strip() else fallback


def default_fixed_overlays(defaults: dict[str, object]) -> list[dict[str, object]]:
    """Liest feste Overlay-Definitionen robust aus Template-Defaults."""
    raw_overlays = defaults.get("default_overlays", [])
    if not isinstance(raw_overlays, list):
        return []
    return [overlay for overlay in raw_overlays if isinstance(overlay, dict)]


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
    primary_axis_mode: str = "automatic",
    primary_ymin: float | None = None,
    primary_ymax: float | None = None,
    secondary_axis_mode: str = "automatic",
    secondary_ymin: float | None = None,
    secondary_ymax: float | None = None,
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
        "primary_axis_mode": primary_axis_mode,
        "primary_ymin": primary_ymin,
        "primary_ymax": primary_ymax,
        "secondary_axis_mode": secondary_axis_mode,
        "secondary_ymin": secondary_ymin,
        "secondary_ymax": secondary_ymax,
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
    plot_template_mode: str = "single",
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
        plot_template_mode=plot_template_mode,
        plot_template_options=plot_template_options or {},
    )
