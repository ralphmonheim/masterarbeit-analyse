"""Kompatibilitaetszugriff auf Streamlit-Komponenten."""

from __future__ import annotations

import importlib
import sys

from ma_ui.streamlit_app.components import *  # noqa: F403

_ALIASES = ("analysis_result",)

for _name in _ALIASES:
    sys.modules[f"{__name__}.{_name}"] = importlib.import_module(
        f"ma_ui.streamlit_app.components.{_name}"
    )
