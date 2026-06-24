"""Direkter Startpunkt fuer die Tkinter-Analyseansicht."""

from __future__ import annotations

import sys

from ma_analyse.app.cli import build_parser, has_cli_option, normalize_rooms

from .app import run_gui


def main() -> None:
    """Startet die Tkinter-Analyse mit den bestehenden GUI-CLI-Optionen."""
    parser = build_parser()
    args = parser.parse_args(["gui", *sys.argv[1:]])
    raw_argv = sys.argv[1:]
    args.variant_mode_explicit = has_cli_option(raw_argv, "--heating-mode", "--variant-mode")
    args.series_layout_explicit = has_cli_option(raw_argv, "--heating-series-layout", "--series-layout")
    args.output_root_explicit = has_cli_option(raw_argv, "--output-root")
    args.rooms = normalize_rooms(args.rooms)
    run_gui(args)


if __name__ == "__main__":
    main()
