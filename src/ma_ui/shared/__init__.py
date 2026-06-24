"""Kompatibilitaetszugriff auf gemeinsame Streamlit-Bausteine."""

from __future__ import annotations

import importlib
import sys

from ma_ui.streamlit_app.shared import *  # noqa: F403

_ALIASES = (
    "file_selectors",
    "layout",
    "log_panel",
    "module_links",
    "plot_viewer",
    "status_panel",
    "tables",
    "widgets",
    "workflow_context",
)

for _name in _ALIASES:
    sys.modules[f"{__name__}.{_name}"] = importlib.import_module(
        f"ma_ui.streamlit_app.shared.{_name}"
    )
