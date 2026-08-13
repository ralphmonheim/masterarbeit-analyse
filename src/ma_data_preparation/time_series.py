"""Öffentliche Zeitreihenoperationen für Adapter und Analysemodule."""

from .models import PreparedSeries, StandardizedSeries
from .services import integrate_time_weighted, prepare_series_to_hourly


def prepare_series(series: StandardizedSeries) -> PreparedSeries:
    """Erzeugt Stundenwerte über die vollständige vorhandene Zeitspanne."""
    return prepare_series_to_hourly(series)


def integrate_power_kwh(series: StandardizedSeries) -> float:
    """Integriert eine Leistungsreihe in Watt zu Energie in kWh."""
    return integrate_time_weighted(series) / 1000.0
