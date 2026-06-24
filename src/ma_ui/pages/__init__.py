"""Kompatibilitaetszugriff auf Streamlit-Seiten."""

from __future__ import annotations

import importlib
import sys

_ALIASES = ("analyse", "assessment", "home", "variants", "weather")

for _name in _ALIASES:
    _module = importlib.import_module(f"ma_ui.streamlit_app.pages.{_name}")
    globals()[_name] = _module
    sys.modules[f"{__name__}.{_name}"] = _module

__all__ = list(_ALIASES)
