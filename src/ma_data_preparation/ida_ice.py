"""Kontrollierte Vorbereitung der im Projekt belegten IDA-PRN-Strukturen."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from ma_import_simulation.adapters.ida_ice import parse_prn_file, sha256_file

from .models import PreparationReference, SourceProvenance, StandardizedRecord, StandardizedSeries, TimeSemantics
from .services import prepare_dataset

PRN_COLUMN_UNITS = {
    "air_age": "h",
    "relhum": "%",
    "xco2vol": "ppm",
    "tair": "°C",
    "tairmean": "°C",
    "top": "°C",
    "mean_t": "°C",
}

KNOWN_MODEL_DIRECTORIES = {
    "5Z": "Masterthesis_Dimensionierung_5Z",
    "29Z": "Masterthesis_Dimensionierung_29Z",
}
RESULT_FOLDERS = ("heating", "cooling", "energy", "summer-peak")


@dataclass(frozen=True, slots=True)
class IdaSeriesSelection:
    cohort: str
    model_id: str
    run_id: str
    variant_id: str
    zone_id: str | None
    result_kind: str
    path: Path


def prn_column_unit(column: str) -> str:
    """Ordnet belegte IDA-Spalten einer expliziten Einheit zu."""

    normalized = column.lower()
    if normalized in PRN_COLUMN_UNITS:
        return PRN_COLUMN_UNITS[normalized]
    if normalized.startswith(("q", "boil_", "chil_", "loccool", "locheat")):
        return "W"
    return "unverified"


def read_prn_as_standardized_series(selection: IdaSeriesSelection) -> tuple[StandardizedSeries, ...]:
    """Bildet jede numerische PRN-Wertspalte auf eine Standardreihe ab."""

    header, rows = parse_prn_file(selection.path)
    normalized_header = tuple(column.lower() for column in header)
    if "time" not in normalized_header:
        raise ValueError(f"PRN-Datei ohne time-Spalte: {selection.path}")
    time_index = normalized_header.index("time")
    source_hash = sha256_file(selection.path)
    provenance = SourceProvenance(
        source_system="ida_ice",
        source_id=f"{selection.run_id}:{selection.variant_id}:{source_hash}",
        source_file=str(selection.path),
    )
    result: list[StandardizedSeries] = []
    for column_index, column in enumerate(normalized_header):
        if column in {"time", "order"}:
            continue
        values = [row[column_index] for row in rows]
        unit = prn_column_unit(column)
        if column == "relhum" and values and max(abs(value) for value in values) <= 1.5:
            values = [value * 100.0 for value in values]
        records = _collapse_repeated_records(tuple(
            StandardizedRecord(float(row[time_index]), float(value)) for row, value in zip(rows, values, strict=True)
        ))
        result.append(
            StandardizedSeries(
                series_id=_series_id(selection, column),
                metric=f"{selection.path.stem.split('.')[-1].lower().replace('-', '_')}.{column}",
                unit=unit,
                time_semantics=TimeSemantics.INSTANTANEOUS,
                provenance=provenance,
                records=records,
            )
        )
    return tuple(result)


def discover_known_ida_prn(input_root: str | Path) -> tuple[IdaSeriesSelection, ...]:
    """Findet nur die explizit belegten 5Z-, 29Z- und ALT-PRN-Strukturen."""

    root = Path(input_root)
    selections: list[IdaSeriesSelection] = []
    for cohort, directory_name in KNOWN_MODEL_DIRECTORIES.items():
        model_root = root / directory_name
        if not model_root.is_dir():
            continue
        for result_kind in RESULT_FOLDERS:
            result_root = model_root / result_kind
            if not result_root.is_dir():
                continue
            for path in sorted(result_root.glob("*.prn")):
                selections.append(
                    IdaSeriesSelection(
                        cohort=cohort,
                        model_id=directory_name,
                        run_id=f"{directory_name}:{result_kind}",
                        variant_id="Dimensionierung",
                        zone_id=_zone_from_prn_name(path),
                        result_kind=result_kind,
                        path=path,
                    )
                )
    alt_root = root / "ALT"
    if alt_root.is_dir():
        for variant_root in sorted(path for path in alt_root.iterdir() if path.is_dir()):
            for path in sorted(variant_root.glob("*.prn")):
                selections.append(_alt_selection(variant_root, path, None))
            for room_root in sorted(path for path in variant_root.iterdir() if path.is_dir()):
                for path in sorted(room_root.glob("*.prn")):
                    selections.append(_alt_selection(variant_root, path, room_root.name))
    return tuple(selections)


def prepare_known_ida_results(
    input_root: str | Path,
    output_root: str | Path,
    *,
    cohorts: tuple[str, ...] = ("5Z", "29Z", "ALT"),
    resume_existing: bool = False,
) -> dict[str, PreparationReference]:
    """Bereitet die bekannten Kohorten getrennt auf und schreibt Manifeste."""

    results: dict[str, PreparationReference] = {}
    for selection in discover_known_ida_prn(input_root):
        if selection.cohort not in cohorts:
            continue
        package_id = _package_id(selection)
        if resume_existing and _prepared_manifest_matches_source(output_root, package_id, selection.path):
            continue
        series = read_prn_as_standardized_series(selection)
        prepared = prepare_dataset(package_id, series, output_root)
        results[package_id] = PreparationReference(package_id, prepared.manifest_path, len(prepared.package.series))
    return results


def _alt_selection(variant_root: Path, path: Path, zone_id: str | None) -> IdaSeriesSelection:
    return IdaSeriesSelection(
        cohort="ALT",
        model_id="historical_5_room_optimization",
        run_id=f"ALT:{variant_root.name}",
        variant_id=variant_root.name,
        zone_id=zone_id or _zone_from_prn_name(path),
        result_kind="optimization",
        path=path,
    )


def _zone_from_prn_name(path: Path) -> str | None:
    stem = path.stem
    if "." in stem:
        prefix = stem.rsplit(".", 1)[0]
        return prefix if prefix not in {"AHU", "BUILD", "PLANT"} else None
    return None


def _series_id(selection: IdaSeriesSelection, column: str) -> str:
    parts = (
        selection.cohort,
        selection.variant_id,
        selection.result_kind,
        selection.zone_id or "building",
        selection.path.stem,
        column,
    )
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", "__".join(parts)).strip("_")


def _package_id(selection: IdaSeriesSelection) -> str:
    parts = (
        "ida",
        selection.cohort,
        selection.variant_id,
        selection.result_kind,
        selection.zone_id or "building",
        selection.path.stem,
    )
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", "__".join(parts)).strip("_")


def _prepared_manifest_matches_source(output_root: str | Path, package_id: str, source_path: Path) -> bool:
    """Verwendet nur ein vollstaendiges Paket derselben Quelldateiversion."""

    safe_package_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", package_id).strip("._")
    manifest_path = Path(output_root) / safe_package_id / "preparation_manifest.json"
    if not manifest_path.is_file():
        return False
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_series = payload.get("series", [])
        if not manifest_series:
            return False
        source_ids = {
            item.get("provenance", {}).get("source_id")
            for item in manifest_series
            if isinstance(item, dict)
        }
        expected_suffix = f":{sha256_file(source_path)}"
        return len(source_ids) == 1 and next(iter(source_ids), "").endswith(expected_suffix)
    except (OSError, ValueError, TypeError, AttributeError):
        return False


def _collapse_repeated_records(
    records: tuple[StandardizedRecord, ...], *, time_tolerance: float = 1e-8, value_tolerance: float = 1e-9
) -> tuple[StandardizedRecord, ...]:
    """Entfernt nur numerisch gleiche IDA-Stuetzstellen mit gleichem Wert.

    Widerspruechliche Werte am selben Zeitpunkt bleiben erhalten und werden
    anschliessend von der Qualitaetspruefung als nicht eindeutig gemeldet.
    """

    collapsed: list[StandardizedRecord] = []
    for record in records:
        if collapsed and abs(record.time_hours - collapsed[-1].time_hours) <= time_tolerance:
            if abs(record.value - collapsed[-1].value) <= value_tolerance:
                continue
        collapsed.append(record)
    return tuple(collapsed)
