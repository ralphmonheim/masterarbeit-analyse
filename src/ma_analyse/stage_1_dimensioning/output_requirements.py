"""Neutrale Ausgabeanforderungen fuer den ersten Ergebnispostprocess."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OutputRequirementProfile:
    """Programmunabhaengige Pflichtausgabe eines Simulationsruns."""

    profile_id: str
    metric: str
    unit: str
    time_resolution: str
    chart_type: str


def default_output_requirements() -> tuple[OutputRequirementProfile, ...]:
    """Liefert die drei fuer MVP V1 vereinbarten Ausgabeprofile."""
    return (
        OutputRequirementProfile("OUT-LOAD", "heating_cooling_load", "W", "hour", "load_comparison"),
        OutputRequirementProfile("OUT-COMFORT", "room_temperature_or_comfort", "degC_or_h", "hour", "comfort_time_series"),
        OutputRequirementProfile("OUT-PEAK", "annual_or_peak_comparison", "W_or_kWh", "year", "variant_comparison"),
    )
