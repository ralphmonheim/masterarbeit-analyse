"""Kompatibilitaetszugriff auf den Streamlit-Sitzungszustand."""

from __future__ import annotations

import importlib
import sys

from ma_ui.streamlit_app.state import *  # noqa: F403

_ALIASES = ("configuration_state", "project_state")

for _name in _ALIASES:
    sys.modules[f"{__name__}.{_name}"] = importlib.import_module(
        f"ma_ui.streamlit_app.state.{_name}"
    )
