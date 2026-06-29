"""CLI-Startargumente fuer die getrennte Tkinter-Analyseansicht."""

from __future__ import annotations

import argparse

from ma_analyse.analysis.components.time_windows import MONTH_NAMES
from ma_analyse.app.cli import (
    add_plot_template_arguments,
    has_cli_option,
    normalize_rooms,
    parse_comma_separated_list,
)
from ma_analyse.core.config import DATENBANK_DIR, EXPORT_FORMATS, INPUT_DIR, OUTPUT_DIR


def build_tkinter_analyse_parser(plot_template_config_path=None) -> argparse.ArgumentParser:
    """Baut den Parser fuer ``python -m ma_ui.tkinter_app.module_views.analyse``."""
    parser = argparse.ArgumentParser(
        description="Startet die getrennte Tkinter-Analyseansicht."
    )
    parser.set_defaults(command="gui", debug=True)

    parser.add_argument(
        "--input-dir",
        default=INPUT_DIR,
        help="Wurzelverzeichnis mit IDA-Importvarianten",
    )
    parser.add_argument(
        "--datenbank-dir",
        default=DATENBANK_DIR,
        help="Verzeichnis mit aufbereiteten Nutzdaten",
    )
    parser.add_argument(
        "--output-root",
        default=OUTPUT_DIR,
        help="Wurzelverzeichnis fuer erzeugte Ausgaben",
    )
    parser.add_argument("--run-id", default=None, help="Optionale Lauf-ID")
    parser.add_argument(
        "--variants",
        type=parse_comma_separated_list,
        default=None,
        help="Komma-getrennte Varianten",
    )
    parser.add_argument(
        "--rooms",
        type=parse_comma_separated_list,
        default=None,
        help="Komma-getrennte Raeume",
    )
    parser.add_argument(
        "--view",
        choices=["bar", "year", "month", "week", "day"],
        default="bar",
        help="Startwert fuer die Zeitansicht",
    )
    parser.add_argument(
        "--month",
        choices=MONTH_NAMES,
        default=None,
        help="Startwert fuer Monatsfilter",
    )
    parser.add_argument("--week", type=int, default=None, help="Startwert fuer Kalenderwoche")
    parser.add_argument("--day", type=int, default=None, help="Startwert fuer Tag im Monat")
    parser.add_argument(
        "--heating-mode",
        "--variant-mode",
        choices=["single", "compare"],
        default=None,
        dest="heating_mode",
        help="Startwert fuer Variantenmodus",
    )
    parser.add_argument(
        "--heating-series-layout",
        "--series-layout",
        choices=["separate", "combined"],
        default=None,
        dest="heating_series_layout",
        help="Startwert fuer Diagramm-/Excel-Ausgabe",
    )
    parser.add_argument(
        "--export-format",
        choices=EXPORT_FORMATS,
        default="csv",
        help="Startwert fuer das Prepare-Exportformat",
    )
    parser.add_argument("--debug", dest="debug", action="store_true", help="Aktiviert Debug-Ausgaben")
    parser.add_argument("--no-debug", dest="debug", action="store_false", help="Deaktiviert Debug-Ausgaben")
    parser.add_argument("--gui-refresh-port", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--gui-window-x", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--gui-window-y", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--gui-window-width", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--gui-window-height", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument(
        "--gui-window-maximized",
        type=int,
        choices=[0, 1],
        default=0,
        help=argparse.SUPPRESS,
    )
    add_plot_template_arguments(parser, hide_help=True, config_path=plot_template_config_path)
    return parser


def parse_tkinter_analyse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parst und normalisiert Startargumente fuer die Tkinter-Analyse."""
    parser = build_tkinter_analyse_parser()
    args = parser.parse_args(argv)
    raw_argv = argv or []
    args.variant_mode_explicit = has_cli_option(raw_argv, "--heating-mode", "--variant-mode")
    args.series_layout_explicit = has_cli_option(raw_argv, "--heating-series-layout", "--series-layout")
    args.output_root_explicit = has_cli_option(raw_argv, "--output-root")
    args.rooms = normalize_rooms(args.rooms)
    return args


__all__ = ["build_tkinter_analyse_parser", "parse_tkinter_analyse_args"]
