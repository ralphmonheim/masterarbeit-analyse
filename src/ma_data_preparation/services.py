"""Validierung, zeitgewichtete Aggregation und dateibasierter Export."""

from __future__ import annotations

import csv
import json
import math
import re
from dataclasses import asdict
from pathlib import Path

from .models import (
    DataSuitability,
    PreparationPackage,
    PreparationResult,
    PreparedRecord,
    PreparedSeries,
    QualityDiagnostic,
    SeriesQualityReport,
    StandardizedSeries,
    TimeAxisDiagnostics,
    TimeSemantics,
)


def validate_time_axis(series: StandardizedSeries) -> TimeAxisDiagnostics:
    """Prüft Reihenfolge, Endlichkeit, Duplikate und auffällige Zeitlücken."""
    times = tuple(record.time_hours for record in series.records)
    finite_times = tuple(value for value in times if math.isfinite(value))
    finite_values = sum(math.isfinite(record.value) for record in series.records)
    is_sorted = all(left <= right for left, right in zip(times, times[1:], strict=False))
    sorted_times = sorted(finite_times)
    steps = tuple(right - left for left, right in zip(sorted_times, sorted_times[1:], strict=False))
    duplicates = tuple(sorted({left for left, right in zip(sorted_times, sorted_times[1:], strict=False) if left == right}))
    non_positive = tuple(step for step in steps if step <= 0)
    reference_step = series.expected_step_hours
    gap_starts: tuple[float, ...] = ()
    if reference_step is not None and reference_step > 0:
        gap_starts = tuple(left for left, step in zip(sorted_times, steps, strict=False) if step > reference_step * 1.5)
    return TimeAxisDiagnostics(
        record_count=len(times),
        is_sorted=is_sorted,
        finite_time_count=len(finite_times),
        finite_value_count=finite_values,
        duplicate_timestamps=duplicates,
        non_positive_steps=non_positive,
        gap_starts=gap_starts,
        reference_step_hours=reference_step,
    )


def assess_series_quality(series: StandardizedSeries) -> SeriesQualityReport:
    """Leitet eine einfache, konservative Eignungsstufe aus Achsenbefunden ab."""
    axis = validate_time_axis(series)
    findings: list[QualityDiagnostic] = []
    if axis.record_count < 2:
        findings.append(QualityDiagnostic("too_few_records", "Mindestens zwei Zeitpunkte sind erforderlich.", "error"))
    if axis.finite_time_count != axis.record_count or axis.finite_value_count != axis.record_count:
        findings.append(QualityDiagnostic("non_finite_values", "Zeitstempel und Werte müssen endlich sein.", "error"))
    if axis.duplicate_timestamps:
        findings.append(QualityDiagnostic("duplicate_timestamps", "Doppelte Zeitstempel verhindern eine eindeutige Aggregation.", "error"))
    if not axis.is_sorted:
        findings.append(QualityDiagnostic("unsorted_timestamps", "Zeitstempel werden für die Vorbereitung sortiert.", "warning"))
    if axis.gap_starts:
        findings.append(QualityDiagnostic("time_gaps", "Zeitlücken bleiben im Stundenraster sichtbar.", "warning"))
    if any(item.severity == "error" for item in findings):
        suitability = DataSuitability.NOT_READY
    elif findings:
        suitability = DataSuitability.PARTIAL
    else:
        suitability = DataSuitability.READY
    return SeriesQualityReport(series.series_id, suitability, axis, tuple(findings))


def integrate_time_weighted(series: StandardizedSeries) -> float:
    """Integriert Werte über die reale Zeitachse (Ergebnis: Einheit mal Stunde)."""
    quality = assess_series_quality(series)
    if quality.suitability is DataSuitability.NOT_READY:
        raise ValueError(f"Reihe {series.series_id} ist nicht eindeutig integrierbar.")
    records = _usable_sorted_records(series)
    if len(records) < 2:
        return 0.0
    total = 0.0
    for left, right in zip(records, records[1:], strict=False):
        duration = right.time_hours - left.time_hours
        if _is_uncovered_gap(series, duration):
            continue
        if series.time_semantics is TimeSemantics.INTERVAL_AVERAGE:
            total += left.value * duration
        else:
            total += (left.value + right.value) * duration / 2.0
    return total


def prepare_series_to_hourly(series: StandardizedSeries) -> PreparedSeries:
    """Aggregiert eine gültige Reihe auf ganze Stunden ohne Jahresbegrenzung."""
    quality = assess_series_quality(series)
    if quality.suitability is DataSuitability.NOT_READY:
        return PreparedSeries(series.series_id, series.metric, series.unit, series.time_semantics, series.provenance, quality, ())
    records = _usable_sorted_records(series)
    first_hour = math.floor(records[0].time_hours)
    last_hour = math.ceil(records[-1].time_hours)
    prepared = _aggregate_all_hours(series, records, first_hour, last_hour)
    return PreparedSeries(series.series_id, series.metric, series.unit, series.time_semantics, series.provenance, quality, prepared)


def prepare_package(package_id: str, series: tuple[StandardizedSeries, ...]) -> PreparationPackage:
    """Bereitet mehrere unabhängige Reihen in einem unveränderlichen Paket vor."""
    if not package_id.strip():
        raise ValueError("package_id darf nicht leer sein.")
    if len({item.series_id for item in series}) != len(series):
        raise ValueError("series_id muss innerhalb eines Pakets eindeutig sein.")
    return PreparationPackage(package_id, tuple(prepare_series_to_hourly(item) for item in series))


class DataPreparationService:
    """Schreibt vorbereitete CSV-Reihen und ein JSON-Manifest in einen Zielordner."""

    def __init__(self, output_root: str | Path) -> None:
        self.output_root = Path(output_root)

    def prepare_and_write(self, package_id: str, series: tuple[StandardizedSeries, ...]) -> PreparationResult:
        package = prepare_package(package_id, series)
        output_directory = self.output_root / _safe_name(package_id)
        output_directory.mkdir(parents=True, exist_ok=True)
        csv_paths = tuple(_write_series_csv(output_directory, item) for item in package.series)
        manifest_path = output_directory / "preparation_manifest.json"
        manifest_path.write_text(json.dumps(_manifest_payload(package, csv_paths), indent=2, ensure_ascii=False), encoding="utf-8")
        return PreparationResult(package, str(output_directory), str(manifest_path), tuple(str(path) for path in csv_paths))


def prepare_dataset(
    dataset_id: str, series: tuple[StandardizedSeries, ...], output_root: str | Path
) -> PreparationResult:
    """Bereitet ein Dataset vor und speichert CSV-Reihen sowie JSON-Manifest."""
    return DataPreparationService(output_root).prepare_and_write(dataset_id, series)


def _aggregate_all_hours(
    series: StandardizedSeries, records: tuple, first_hour: int, last_hour: int
) -> tuple[PreparedRecord, ...]:
    """Aggregiert in einem linearen Durchlauf statt Stunde mal Stuetzstelle."""

    integrals = {hour: 0.0 for hour in range(first_hour, last_hour)}
    coverages = {hour: 0.0 for hour in range(first_hour, last_hour)}
    for left, right in zip(records, records[1:], strict=False):
        if _is_uncovered_gap(series, right.time_hours - left.time_hours):
            continue
        cursor = left.time_hours
        while cursor < right.time_hours:
            hour = math.floor(cursor)
            overlap_end = min(right.time_hours, float(hour + 1))
            duration = overlap_end - cursor
            if duration <= 0:
                break
            if series.time_semantics is TimeSemantics.INTERVAL_AVERAGE:
                integrals[hour] += left.value * duration
            else:
                integrals[hour] += _linear_integral(
                    left.time_hours,
                    left.value,
                    right.time_hours,
                    right.value,
                    cursor,
                    overlap_end,
                )
            coverages[hour] += duration
            cursor = overlap_end
    return tuple(
        PreparedRecord(hour, integrals[hour] / coverages[hour] if coverages[hour] else None, coverages[hour])
        for hour in range(first_hour, last_hour)
    )


def _linear_integral(x0: float, y0: float, x1: float, y1: float, start: float, end: float) -> float:
    slope = (y1 - y0) / (x1 - x0)
    return y0 * (end - start) + slope * ((end - x0) ** 2 - (start - x0) ** 2) / 2.0


def _usable_sorted_records(series: StandardizedSeries) -> tuple:
    return tuple(sorted((record for record in series.records if math.isfinite(record.time_hours) and math.isfinite(record.value)), key=lambda record: record.time_hours))


def _is_uncovered_gap(series: StandardizedSeries, duration: float) -> bool:
    expected = series.expected_step_hours
    return expected is not None and expected > 0 and duration > expected * 1.5


def _write_series_csv(directory: Path, series: PreparedSeries) -> Path:
    target = directory / f"{_safe_name(series.series_id)}.csv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("hour_start", "value", "coverage_hours"))
        writer.writeheader()
        writer.writerows(asdict(record) for record in series.records)
    return target


def _manifest_payload(package: PreparationPackage, csv_paths: tuple[Path, ...]) -> dict[str, object]:
    return {
        "package_id": package.package_id,
        "series": [
            {
                "series_id": item.series_id,
                "metric": item.metric,
                "unit": item.unit,
                "time_semantics": item.time_semantics.value,
                "provenance": asdict(item.provenance),
                "suitability": item.quality.suitability.value,
                "quality_diagnostics": [asdict(finding) for finding in item.quality.diagnostics],
                "time_axis": asdict(item.quality.time_axis),
                "record_count": len(item.records),
                "csv_file": path.name,
            }
            for item, path in zip(package.series, csv_paths, strict=True)
        ],
    }


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._") or "prepared_series"
