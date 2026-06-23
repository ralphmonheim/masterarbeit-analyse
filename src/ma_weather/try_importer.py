"""Importer fuer lokale TRY-Wetterdateien."""

from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from pathlib import Path

import pandas as pd

from ma_core import InputSource, InputSourceKind, build_input_source
from ma_validation import DiagnosticMessage, DiagnosticSeverity, ImportDiagnostic

TRY_DATA_SEPARATOR = "***"
DEFAULT_TRY_YEAR = 2015

DATE_COLUMN_ALIASES = {
    "month": {"mm", "month", "monat", "mo"},
    "day": {"dd", "day", "tag"},
    "hour": {"hh", "hour", "stunde", "h"},
}

WEATHER_COLUMN_ALIASES = {
    "temperature_c": {"t", "ta", "temp", "temperature", "temperature_c", "tl", "t_luft"},
    "relative_humidity_pct": {"rf", "rh", "relhum", "relative_humidity", "relative_humidity_pct"},
    "wind_direction_deg": {"wr", "wind_dir", "wind_direction", "wind_direction_deg"},
    "wind_speed_m_s": {"wg", "wind", "wind_speed", "wind_speed_m_s", "v_wind"},
    "direct_radiation_w_m2": {"b", "direct", "direct_radiation", "direct_radiation_w_m2"},
    "diffuse_radiation_w_m2": {"d", "diffuse", "diffuse_radiation", "diffuse_radiation_w_m2"},
    "global_radiation_w_m2": {"g", "global", "global_radiation", "global_radiation_w_m2"},
}

FALLBACK_COLUMNS = (
    "region_x",
    "region_y",
    "month",
    "day",
    "hour",
    "temperature_c",
    "pressure_hpa",
    "wind_direction_deg",
    "wind_speed_m_s",
    "cloud_cover_octas",
    "water_content_g_kg",
    "relative_humidity_pct",
    "direct_radiation_w_m2",
    "diffuse_radiation_w_m2",
    "atmospheric_radiation_w_m2",
    "terrestrial_radiation_w_m2",
    "illumination_klux",
)


@dataclass(frozen=True, slots=True)
class TryImportResult:
    """Strukturiertes Ergebnis eines TRY-Imports."""

    data: pd.DataFrame
    source_path: Path
    weather_key: str | None
    row_count: int
    columns: tuple[str, ...]
    warnings: tuple[str, ...]
    source: InputSource
    import_diagnostic: ImportDiagnostic


def import_try_weather_file(
    file_path: str | Path,
    *,
    weather_key: str | None = None,
    start_year: int = DEFAULT_TRY_YEAR,
) -> TryImportResult:
    """Liest eine TRY-Datei ein und normalisiert die wichtigsten Wetterspalten."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"TRY-Datei nicht gefunden: {path}")

    text = _read_try_text(path)
    data_lines = _extract_data_block(text)
    raw_data = _read_data_table(data_lines)
    data, diagnostic_messages = _normalize_try_dataframe(raw_data, start_year=start_year)
    source = build_input_source(
        module_key="ma_weather",
        source_kind=InputSourceKind.IMPORT,
        data_format="TRY",
        source_path=path,
        adapter_key="ma_weather.try_importer",
    )
    import_diagnostic = ImportDiagnostic(
        source=source,
        messages=tuple(diagnostic_messages),
        record_count=len(data),
        accepted_count=len(data),
    )

    return TryImportResult(
        data=data,
        source_path=path,
        weather_key=weather_key,
        row_count=len(data),
        columns=tuple(data.columns),
        warnings=tuple(message.message for message in diagnostic_messages),
        source=source,
        import_diagnostic=import_diagnostic,
    )


def _read_try_text(path: Path) -> str:
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_data_block(text: str) -> list[str]:
    lines = text.splitlines()
    separator_index = next((index for index, line in enumerate(lines) if TRY_DATA_SEPARATOR in line), None)
    if separator_index is None:
        raise ValueError("TRY-Datenblock nicht gefunden: Zeile mit drei Sternen fehlt.")

    data_lines = [line.strip() for line in lines[separator_index + 1 :] if line.strip()]
    if not data_lines:
        raise ValueError("TRY-Datenblock ist leer.")
    return data_lines


def _read_data_table(data_lines: list[str]) -> pd.DataFrame:
    first_line = data_lines[0]
    has_header = _line_looks_like_header(first_line)
    buffer = StringIO("\n".join(data_lines))
    if has_header:
        return pd.read_csv(buffer, sep=r"\s+", engine="python")

    data = pd.read_csv(buffer, sep=r"\s+", engine="python", header=None)
    data.columns = _fallback_columns_for_width(len(data.columns))
    return data


def _line_looks_like_header(line: str) -> bool:
    tokens = line.split()
    return bool(tokens) and any(any(character.isalpha() for character in token) for token in tokens)


def _fallback_columns_for_width(width: int) -> list[str]:
    if width <= len(FALLBACK_COLUMNS):
        return list(FALLBACK_COLUMNS[:width])
    columns = list(FALLBACK_COLUMNS)
    columns.extend(f"extra_{index}" for index in range(1, width - len(FALLBACK_COLUMNS) + 1))
    return columns


def _normalize_try_dataframe(
    raw_data: pd.DataFrame,
    *,
    start_year: int,
) -> tuple[pd.DataFrame, list[DiagnosticMessage]]:
    diagnostics: list[DiagnosticMessage] = []
    data = raw_data.copy()
    data.columns = [_normalize_column_name(column) for column in data.columns]
    data = _rename_known_columns(data)

    for column in data.columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    if {"direct_radiation_w_m2", "diffuse_radiation_w_m2"}.issubset(data.columns):
        data["global_radiation_w_m2"] = data["direct_radiation_w_m2"] + data["diffuse_radiation_w_m2"]
    elif "global_radiation_w_m2" not in data.columns:
        diagnostics.append(
            DiagnosticMessage(
                severity=DiagnosticSeverity.WARNING,
                code="WEATHER_IMPORT_GLOBAL_RADIATION_MISSING",
                message="Globalstrahlung konnte nicht berechnet werden: direkte oder diffuse Strahlung fehlt.",
                location="columns.direct_radiation_w_m2|diffuse_radiation_w_m2",
            )
        )

    if "temperature_c" not in data.columns:
        diagnostics.append(
            DiagnosticMessage(
                severity=DiagnosticSeverity.WARNING,
                code="WEATHER_IMPORT_TEMPERATURE_COLUMN_UNRECOGNIZED",
                message="Temperaturspalte wurde nicht eindeutig erkannt.",
                location="columns.temperature_c",
            )
        )

    data.index = _build_time_index(data, start_year=start_year)
    data.index.name = "time"
    return data, diagnostics


def _normalize_column_name(column: object) -> str:
    return str(column).strip().lower().replace("[", "").replace("]", "").replace("/", "_").replace("-", "_")


def _rename_known_columns(data: pd.DataFrame) -> pd.DataFrame:
    rename_map: dict[str, str] = {}
    for target_column, aliases in DATE_COLUMN_ALIASES.items():
        _add_first_matching_column(rename_map, data.columns, target_column, aliases)
    for target_column, aliases in WEATHER_COLUMN_ALIASES.items():
        _add_first_matching_column(rename_map, data.columns, target_column, aliases)
    return data.rename(columns=rename_map)


def _add_first_matching_column(
    rename_map: dict[str, str],
    columns: pd.Index,
    target_column: str,
    aliases: set[str],
) -> None:
    if target_column in columns:
        return
    for column in columns:
        if column in aliases and column not in rename_map:
            rename_map[column] = target_column
            return


def _build_time_index(data: pd.DataFrame, *, start_year: int) -> pd.DatetimeIndex:
    if {"month", "day", "hour"}.issubset(data.columns):
        month = data["month"].astype("Int64")
        day = data["day"].astype("Int64")
        try_hour = data["hour"].astype("Int64")
        pandas_hour = try_hour.clip(lower=1, upper=24) - 1
        timestamps = pd.to_datetime(
            {
                "year": start_year,
                "month": month,
                "day": day,
                "hour": pandas_hour,
            },
            errors="coerce",
        )
        if timestamps.isna().any():
            raise ValueError("TRY-Zeitindex konnte nicht aus month/day/hour erzeugt werden.")
        return pd.DatetimeIndex(timestamps)

    return pd.date_range(start=f"{start_year}-01-01 00:00:00", periods=len(data), freq="h")
