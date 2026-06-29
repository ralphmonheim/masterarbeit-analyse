"""Restart-Argumente fuer die Tkinter-Analyseansicht."""

from __future__ import annotations

import sys

from ma_analyse.analysis.templates import (
    DEFAULT_OUTDOOR_COLUMN,
    DEFAULT_SETPOINT_MAX,
    DEFAULT_SETPOINT_MIN,
    DEFAULT_TEMPERATURE_YMAX,
    DEFAULT_TEMPERATURE_YMIN,
    HEATING_YEAR_TEMPLATE,
)
from ma_analyse.core.config import DATENBANK_DIR, INPUT_DIR, OUTPUT_DIR
from ma_analyse.settings.plot_templates import get_heating_year_template_defaults

from .selection import format_cli_list


def build_gui_restart_argv(args, refresh_port):
    """Baut den CLI-Aufruf, mit dem sich die GUI selbst neu startet."""
    argv = [sys.executable, "-m", "ma_ui.tkinter_app.module_views.analyse"]
    template_defaults = get_heating_year_template_defaults()

    option_values = [
        ("--input-dir", getattr(args, "input_dir", None), INPUT_DIR),
        ("--datenbank-dir", getattr(args, "datenbank_dir", None), DATENBANK_DIR),
        ("--output-root", getattr(args, "output_root", None), OUTPUT_DIR),
        ("--run-id", getattr(args, "run_id", None), None),
        ("--variants", format_cli_list(getattr(args, "variants", None)), None),
        ("--rooms", format_cli_list(getattr(args, "rooms", None)), None),
        ("--view", getattr(args, "view", None), "bar"),
        ("--month", getattr(args, "month", None), None),
        ("--week", getattr(args, "week", None), None),
        ("--day", getattr(args, "day", None), None),
        ("--heating-mode", getattr(args, "heating_mode", None), "compare"),
        ("--heating-series-layout", getattr(args, "heating_series_layout", None), "separate"),
        ("--export-format", getattr(args, "export_format", None), "csv"),
        ("--template", getattr(args, "template", None), HEATING_YEAR_TEMPLATE),
        (
            "--setpoint-min",
            getattr(args, "setpoint_min", None),
            template_defaults.get("setpoint_min", DEFAULT_SETPOINT_MIN),
        ),
        (
            "--setpoint-max",
            getattr(args, "setpoint_max", None),
            template_defaults.get("setpoint_max", DEFAULT_SETPOINT_MAX),
        ),
        (
            "--temperature-ymin",
            getattr(args, "temperature_ymin", None),
            template_defaults.get("temperature_ymin", DEFAULT_TEMPERATURE_YMIN),
        ),
        (
            "--temperature-ymax",
            getattr(args, "temperature_ymax", None),
            template_defaults.get("temperature_ymax", DEFAULT_TEMPERATURE_YMAX),
        ),
        (
            "--outdoor-column",
            getattr(args, "outdoor_column", None),
            template_defaults.get("outdoor_column", DEFAULT_OUTDOOR_COLUMN),
        ),
    ]

    for option_name, value, default_value in option_values:
        if value is None:
            continue
        if default_value is not None and value == default_value:
            continue
        argv.extend([option_name, str(value)])

    if getattr(args, "debug", True):
        argv.append("--debug")
    else:
        argv.append("--no-debug")

    if getattr(args, "show_setpoint_band", template_defaults.get("show_setpoint_band", True)) is False:
        argv.append("--no-setpoint-band")
    if getattr(args, "show_outdoor_temperature", template_defaults.get("show_outdoor_temperature", True)) is False:
        argv.append("--no-outdoor-temperature")
    if getattr(args, "show_operative_temperature", template_defaults.get("show_operative_temperature", True)) is False:
        argv.append("--no-operative-temperature")

    window_geometry = getattr(args, "gui_window_geometry", None)
    if isinstance(window_geometry, dict):
        for option_name, key in (
            ("--gui-window-x", "x"),
            ("--gui-window-y", "y"),
            ("--gui-window-width", "width"),
            ("--gui-window-height", "height"),
        ):
            value = window_geometry.get(key)
            if value is not None:
                argv.extend([option_name, str(value)])

    argv.extend(
        [
            "--gui-window-maximized",
            "1" if getattr(args, "gui_window_maximized", False) else "0",
        ]
    )
    argv.extend(["--gui-refresh-port", str(refresh_port)])
    return argv
