"""Analyse-eigener Katalog und Auswahlvertrag fuer Simulationsausgaben."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class OutputRequirementProfile:
    """Programmunabhaengige, durch die Analyse definierte Pflichtausgabe."""

    profile_id: str
    metric: str
    unit: str
    time_resolution: str
    chart_type: str


def default_output_requirements() -> tuple[OutputRequirementProfile, ...]:
    """Liefert den MVP-V1-Katalog; Auswahl trifft ausschliesslich der Aufrufer."""
    return (
        OutputRequirementProfile("OUT-LOAD", "heating_cooling_load", "W", "hour", "load_comparison"),
        OutputRequirementProfile("OUT-COMFORT", "room_temperature_or_comfort", "degC_or_h", "hour", "comfort_time_series"),
        OutputRequirementProfile("OUT-PEAK", "annual_or_peak_comparison", "W_or_kWh", "year", "variant_comparison"),
    )


def select_output_requirements(profile_ids: Iterable[str]) -> tuple[OutputRequirementProfile, ...]:
    """Validiert die UI-neutrale Checkbox-Auswahl gegen den Analysekatalog."""
    selected_ids = tuple(profile_ids)
    if not selected_ids:
        raise ValueError("Mindestens ein OutputRequirementProfile muss ausgewaehlt werden.")
    if len(set(selected_ids)) != len(selected_ids):
        raise ValueError("Ein OutputRequirementProfile darf nur einmal ausgewaehlt werden.")
    catalog = {profile.profile_id: profile for profile in default_output_requirements()}
    unknown = sorted(set(selected_ids) - set(catalog))
    if unknown:
        raise ValueError(f"Unbekannte OutputRequirementProfile: {', '.join(unknown)}")
    return tuple(profile for profile in default_output_requirements() if profile.profile_id in selected_ids)
