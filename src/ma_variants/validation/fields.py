"""Kleine Pflichtfeldvalidierung fuer dataclass-Modelle."""

from __future__ import annotations

from typing import Any


def _field_label(model_name: str, field_name: str) -> str:
    return f"{model_name}.{field_name}"


def require_non_empty(value: str, field_name: str, model_name: str) -> None:
    """Stellt sicher, dass ein Textfeld gesetzt und nicht leer ist."""
    if not isinstance(value, str):
        raise ValueError(f"{_field_label(model_name, field_name)} muss ein Textwert sein.")
    if not value.strip():
        raise ValueError(f"{_field_label(model_name, field_name)} darf nicht leer sein.")


def require_present(value: Any, field_name: str, model_name: str) -> None:
    """Stellt sicher, dass ein Wert gesetzt ist; 0 und False bleiben gueltig."""
    if value is None:
        raise ValueError(f"{_field_label(model_name, field_name)} muss gesetzt sein.")
    if isinstance(value, str) and not value.strip():
        raise ValueError(f"{_field_label(model_name, field_name)} darf nicht leer sein.")


def require_bool(value: bool, field_name: str, model_name: str) -> None:
    """Stellt sicher, dass ein Flag als echter bool-Wert uebergeben wird."""
    if not isinstance(value, bool):
        raise ValueError(f"{_field_label(model_name, field_name)} muss ein boolescher Wert sein.")
