"""Zeitgewichtete Kennwerte fuer vorbereitete Simulationsergebnisse.

Die Funktionen arbeiten bewusst unabhaengig von einem konkreten
Simulationsprogramm. Zeitpunkte werden in Stunden seit Periodenbeginn
angegeben. Ein Wert gilt fuer das Intervall, das an seinem Zeitstempel beginnt.
Fuer das letzte Intervall muss die Periodengrenze explizit uebergeben werden.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Sequence


@dataclass(frozen=True)
class TimeWeightedSeries:
    """Eine validierte Intervallreihe mit expliziter letzter Periodengrenze."""

    time_hours: tuple[float, ...]
    values: tuple[float, ...]
    period_end_hour: float

    def __post_init__(self) -> None:
        if not self.time_hours or len(self.time_hours) != len(self.values):
            raise ValueError("Zeit- und Wertreihe muessen gleich lang und nicht leer sein.")
        if any(not isfinite(value) for value in (*self.time_hours, *self.values, self.period_end_hour)):
            raise ValueError("Zeitreihe enthaelt nicht-endliche Werte.")
        boundaries = (*self.time_hours, self.period_end_hour)
        if any(right <= left for left, right in zip(boundaries, boundaries[1:], strict=False)):
            raise ValueError("Zeitpunkte und Periodenende muessen streng monoton steigen.")

    @property
    def durations_hours(self) -> tuple[float, ...]:
        boundaries = (*self.time_hours, self.period_end_hour)
        return tuple(right - left for left, right in zip(boundaries, boundaries[1:], strict=False))

    @property
    def covered_hours(self) -> float:
        return sum(self.durations_hours)


def time_weighted_mean(series: TimeWeightedSeries) -> float:
    """Berechnet das zeitgewichtete Mittel einer Intervallreihe."""

    return sum(value * dt for value, dt in zip(series.values, series.durations_hours, strict=True)) / series.covered_hours


def integrate_power_kwh(series: TimeWeightedSeries, *, source_unit: str = "W") -> float:
    """Integriert eine Leistungsreihe nach kWh.

    Unterstuetzt werden nur explizit bestaetigte Einheiten. Dadurch wird kein
    unbestaetigter PRN-Wert still als Watt interpretiert.
    """

    factors = {"W": 1.0 / 1000.0, "kW": 1.0}
    if source_unit not in factors:
        raise ValueError("source_unit muss 'W' oder 'kW' sein.")
    return sum(value * dt for value, dt in zip(series.values, series.durations_hours, strict=True)) * factors[source_unit]


def hours_outside_limit(
    series: TimeWeightedSeries,
    *,
    lower_limit: float | None = None,
    upper_limit: float | None = None,
) -> float:
    """Summiert Intervalldauern ausserhalb expliziter Grenzwerte."""

    if lower_limit is None and upper_limit is None:
        raise ValueError("Mindestens ein Grenzwert ist erforderlich.")
    return sum(
        dt
        for value, dt in zip(series.values, series.durations_hours, strict=True)
        if (lower_limit is not None and value < lower_limit) or (upper_limit is not None and value > upper_limit)
    )


def degree_hours(
    series: TimeWeightedSeries,
    *,
    lower_limit: float | None = None,
    upper_limit: float | None = None,
) -> float:
    """Berechnet Unter- oder Uebertemperaturgradstunden in Kh."""

    if (lower_limit is None) == (upper_limit is None):
        raise ValueError("Genau ein unterer oder oberer Grenzwert ist erforderlich.")
    if lower_limit is not None:
        return sum(max(lower_limit - value, 0.0) * dt for value, dt in zip(series.values, series.durations_hours, strict=True))
    return sum(max(value - float(upper_limit), 0.0) * dt for value, dt in zip(series.values, series.durations_hours, strict=True))


def maximum_continuous_violation_hours(
    series: TimeWeightedSeries,
    *,
    lower_limit: float | None = None,
    upper_limit: float | None = None,
) -> float:
    """Liefert die laengste zusammenhaengende Grenzwertverletzung."""

    if lower_limit is None and upper_limit is None:
        raise ValueError("Mindestens ein Grenzwert ist erforderlich.")
    maximum = current = 0.0
    for value, dt in zip(series.values, series.durations_hours, strict=True):
        violated = (lower_limit is not None and value < lower_limit) or (
            upper_limit is not None and value > upper_limit
        )
        current = current + dt if violated else 0.0
        maximum = max(maximum, current)
    return maximum


def coincident_peak(series_by_zone: Sequence[TimeWeightedSeries]) -> float:
    """Berechnet den zeitgleichen Gebaeudepeak aus deckungsgleichen Reihen."""

    if not series_by_zone:
        raise ValueError("Mindestens eine Zonenreihe ist erforderlich.")
    reference = series_by_zone[0]
    for series in series_by_zone[1:]:
        if series.time_hours != reference.time_hours or series.period_end_hour != reference.period_end_hour:
            raise ValueError("Zonenreihen muessen dieselben Intervallgrenzen besitzen.")
    return max(sum(values) for values in zip(*(series.values for series in series_by_zone), strict=True))


def weighted_person_hours(occupancy: TimeWeightedSeries) -> float:
    """Integriert die Personenzahl zu Personenstunden."""

    if any(value < 0 for value in occupancy.values):
        raise ValueError("Personenzahlen duerfen nicht negativ sein.")
    return sum(value * dt for value, dt in zip(occupancy.values, occupancy.durations_hours, strict=True))


def ppd_weighted_person_hours(ppd: TimeWeightedSeries, occupancy: TimeWeightedSeries) -> float:
    """Integriert PPD-Anteil mal anwesende Personen und Zeit."""

    if ppd.time_hours != occupancy.time_hours or ppd.period_end_hour != occupancy.period_end_hour:
        raise ValueError("PPD und Belegung benoetigen dieselben Intervallgrenzen.")
    if any(value < 0 or value > 100 for value in ppd.values):
        raise ValueError("PPD muss zwischen 0 und 100 Prozent liegen.")
    return sum(
        (ppd_value / 100.0) * persons * dt
        for ppd_value, persons, dt in zip(ppd.values, occupancy.values, ppd.durations_hours, strict=True)
    )


def as_time_weighted_series(
    time_hours: Iterable[float], values: Iterable[float], *, period_end_hour: float
) -> TimeWeightedSeries:
    """Komfortkonstruktor fuer Listen, NumPy- oder Pandas-Reihen."""

    return TimeWeightedSeries(tuple(map(float, time_hours)), tuple(map(float, values)), float(period_end_hour))
