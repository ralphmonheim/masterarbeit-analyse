"""Geplante Ruecksprungziele fuer Feedback aus Analyse und Bewertung."""

from __future__ import annotations

FEEDBACK_TARGETS: tuple[str, ...] = (
    "ma_parameters",
    "ma_weather",
    "ma_building",
    "ma_variants",
    "ma_simulation_setup",
)


def list_feedback_targets() -> tuple[str, ...]:
    """Gibt Module zurueck, in die spaeter Feedback zurueckgefuehrt werden kann."""
    return FEEDBACK_TARGETS
