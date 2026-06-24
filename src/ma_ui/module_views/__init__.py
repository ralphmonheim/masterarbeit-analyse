"""Kompatibilitaetszugriff auf Streamlit-Modulansichten."""

from __future__ import annotations

import importlib
import sys

_ALIASES = (
    "analyse_view",
    "assessment_view",
    "building_view",
    "export_ida_view",
    "feedback_view",
    "home_view",
    "import_ida_view",
    "module_info_view",
    "parameters_view",
    "project_view",
    "simulation_setup_view",
    "variants_view",
    "weather_view",
)

for _name in _ALIASES:
    _module = importlib.import_module(f"ma_ui.streamlit_app.module_views.{_name}")
    globals()[_name] = _module
    sys.modules[f"{__name__}.{_name}"] = _module

__all__ = list(_ALIASES)
