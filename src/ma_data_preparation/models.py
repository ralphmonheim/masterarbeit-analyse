"""Kleine, programmunabhaengige Datenvertraege fuer die Datenvorbereitung."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DataSuitability(StrEnum):
    """Eignung einer Reihe fuer nachfolgende Analysen."""

    READY = "ready"
    PARTIAL = "partial"
    NOT_READY = "not_ready"


class TimeSemantics(StrEnum):
    """Bedeutung eines Messwertes auf der Zeitachse."""

    INTERVAL_AVERAGE = "interval_average"
    INSTANTANEOUS = "instantaneous"


@dataclass(frozen=True, slots=True)
class SourceProvenance:
    """Nachvollziehbare Herkunft einer standardisierten Reihe."""

    source_system: str
    source_id: str
    source_file: str | None = None


# Der fachlich bevorzugte Name. SourceProvenance bleibt als lesbarer Alias
# erhalten, damit Adapter beide Bezeichnungen verwenden können.
SeriesProvenance = SourceProvenance


@dataclass(frozen=True, slots=True)
class StandardizedRecord:
    """Ein numerischer Wert mit Zeitstempel in Stunden seit dem Serienbeginn."""

    time_hours: float
    value: float


@dataclass(frozen=True, slots=True)
class StandardizedSeries:
    """Programmunabhaengige Eingabe für die Datenvorbereitung.

    ``INTERVAL_AVERAGE`` beschreibt einen konstanten Mittelwert bis zum
    nächsten Zeitstempel. ``INSTANTANEOUS`` wird zwischen Stützstellen linear
    interpoliert. Ein erwarteter Schritt macht Lücken explizit prüfbar.
    """

    series_id: str
    metric: str
    unit: str
    time_semantics: TimeSemantics
    provenance: SourceProvenance
    records: tuple[StandardizedRecord, ...]
    expected_step_hours: float | None = None


@dataclass(frozen=True, slots=True)
class TimeAxisDiagnostics:
    """Prüfergebnis einer Zeitachse; Befunde werden nicht verborgen."""

    record_count: int
    is_sorted: bool
    finite_time_count: int
    finite_value_count: int
    duplicate_timestamps: tuple[float, ...]
    non_positive_steps: tuple[float, ...]
    gap_starts: tuple[float, ...]
    reference_step_hours: float | None


@dataclass(frozen=True, slots=True)
class QualityDiagnostic:
    code: str
    message: str
    severity: str


@dataclass(frozen=True, slots=True)
class SeriesQualityReport:
    series_id: str
    suitability: DataSuitability
    time_axis: TimeAxisDiagnostics
    diagnostics: tuple[QualityDiagnostic, ...]


@dataclass(frozen=True, slots=True)
class PreparedRecord:
    """Ein Stundenwert; ``None`` kennzeichnet bewusst fehlende Abdeckung."""

    hour_start: int
    value: float | None
    coverage_hours: float


@dataclass(frozen=True, slots=True)
class PreparedSeries:
    series_id: str
    metric: str
    unit: str
    time_semantics: TimeSemantics
    provenance: SourceProvenance
    quality: SeriesQualityReport
    records: tuple[PreparedRecord, ...]


@dataclass(frozen=True, slots=True)
class PreparationPackage:
    package_id: str
    series: tuple[PreparedSeries, ...]


@dataclass(frozen=True, slots=True)
class PreparationResult:
    package: PreparationPackage
    output_directory: str
    manifest_path: str
    csv_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PreparationReference:
    """Speicherschlanke Referenz auf ein bereits geschriebenes Datenpaket."""

    package_id: str
    manifest_path: str
    series_count: int
