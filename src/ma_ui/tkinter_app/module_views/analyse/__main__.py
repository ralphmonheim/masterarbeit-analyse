"""Direkter Startpunkt fuer die Tkinter-Analyseansicht."""

from __future__ import annotations

import sys

from .app import run_gui
from .cli import parse_tkinter_analyse_args


def main() -> None:
    """Startet die Tkinter-Analyse mit den bestehenden GUI-CLI-Optionen."""
    run_gui(parse_tkinter_analyse_args(sys.argv[1:]))


if __name__ == "__main__":
    main()
