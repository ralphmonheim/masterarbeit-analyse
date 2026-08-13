"""Öffentliche Qualitätsprüfung für standardisierte Zeitreihen."""

from .models import SeriesQualityReport, StandardizedSeries
from .services import assess_series_quality


def assess_series(series: StandardizedSeries) -> SeriesQualityReport:
    """Bewertet die Eignung einer Reihe, ohne die Eingabe zu verändern."""
    return assess_series_quality(series)
