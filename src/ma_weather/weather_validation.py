"""Plausibilitaetspruefung fuer Wetterdaten."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ma_validation import (
    DiagnosticMessage,
    DiagnosticSeverity,
    ValidationResult,
    build_validation_result,
)

DEFAULT_REQUIRED_COLUMNS = ("temperature_c",)


@dataclass(frozen=True, slots=True)
class WeatherValidationReport:
    """Strukturierter Bericht zur Wetterdatenvalidierung."""

    status: str
    warnings: tuple[str, ...]
    errors: tuple[str, ...]
    row_count: int
    missing_columns: tuple[str, ...]
    missing_values: dict[str, int]
    duplicate_timestamps: int
    validation_result: ValidationResult


def validate_weather_dataframe(
    data: pd.DataFrame,
    *,
    required_columns: tuple[str, ...] = DEFAULT_REQUIRED_COLUMNS,
    expected_hours: int = 8760,
    additional_messages: tuple[DiagnosticMessage, ...] = (),
) -> WeatherValidationReport:
    """Prueft Wetterdaten robust und meldet Auffaelligkeiten strukturiert."""
    messages: list[DiagnosticMessage] = list(additional_messages)
    row_count = len(data)

    if row_count != expected_hours:
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "WEATHER_HOUR_COUNT_MISMATCH",
                f"Stundenanzahl ist {row_count}, erwartet werden {expected_hours}.",
                "time.row_count",
            )
        )

    missing_columns = tuple(column for column in required_columns if column not in data.columns)
    if missing_columns:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "WEATHER_REQUIRED_COLUMNS_MISSING",
                f"Pflichtspalten fehlen: {', '.join(missing_columns)}",
                "columns",
            )
        )

    missing_values = {column: int(count) for column, count in data.isna().sum().items() if int(count) > 0}
    if missing_values:
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "WEATHER_MISSING_VALUES",
                "Fehlende Werte gefunden.",
                f"columns.{','.join(sorted(missing_values))}",
            )
        )

    duplicate_timestamps = int(data.index.duplicated().sum())
    if duplicate_timestamps:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "WEATHER_DUPLICATE_TIMESTAMPS",
                f"Doppelte Zeitstempel gefunden: {duplicate_timestamps}",
                "time.index",
            )
        )

    _check_temperature(data, messages)
    _check_relative_humidity(data, messages)
    _check_wind_speed(data, messages)
    _check_radiation(data, messages)

    validation_result = build_validation_result(tuple(messages))
    warnings = tuple(message.message for message in messages if message.severity is DiagnosticSeverity.WARNING)
    errors = tuple(message.message for message in messages if message.severity is DiagnosticSeverity.ERROR)
    status = "error" if errors else "warning" if warnings else "ok"
    return WeatherValidationReport(
        status=status,
        warnings=warnings,
        errors=errors,
        row_count=row_count,
        missing_columns=missing_columns,
        missing_values=missing_values,
        duplicate_timestamps=duplicate_timestamps,
        validation_result=validation_result,
    )


def _message(
    severity: DiagnosticSeverity,
    code: str,
    message: str,
    location: str,
) -> DiagnosticMessage:
    return DiagnosticMessage(
        severity=severity,
        code=code,
        message=message,
        location=location,
    )


def _check_temperature(data: pd.DataFrame, messages: list[DiagnosticMessage]) -> None:
    if "temperature_c" not in data.columns:
        return
    invalid = data["temperature_c"].dropna()
    if ((invalid < -60) | (invalid > 60)).any():
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "WEATHER_TEMPERATURE_OUT_OF_RANGE",
                "Unplausible Temperaturwerte ausserhalb von -60 bis 60 Grad C gefunden.",
                "columns.temperature_c",
            )
        )


def _check_relative_humidity(data: pd.DataFrame, messages: list[DiagnosticMessage]) -> None:
    if "relative_humidity_pct" not in data.columns:
        return
    values = data["relative_humidity_pct"].dropna()
    if ((values < 0) | (values > 100)).any():
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "WEATHER_RELATIVE_HUMIDITY_OUT_OF_RANGE",
                "Relative Feuchte ausserhalb von 0 bis 100 Prozent gefunden.",
                "columns.relative_humidity_pct",
            )
        )


def _check_wind_speed(data: pd.DataFrame, messages: list[DiagnosticMessage]) -> None:
    if "wind_speed_m_s" not in data.columns:
        return
    if (data["wind_speed_m_s"].dropna() < 0).any():
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "WEATHER_NEGATIVE_WIND_SPEED",
                "Negative Windgeschwindigkeiten gefunden.",
                "columns.wind_speed_m_s",
            )
        )


def _check_radiation(data: pd.DataFrame, messages: list[DiagnosticMessage]) -> None:
    radiation_columns = [
        column
        for column in ("direct_radiation_w_m2", "diffuse_radiation_w_m2", "global_radiation_w_m2")
        if column in data.columns
    ]
    for column in radiation_columns:
        if (data[column].dropna() < 0).any():
            messages.append(
                _message(
                    DiagnosticSeverity.WARNING,
                    "WEATHER_NEGATIVE_RADIATION",
                    f"Negative Strahlungswerte in {column} gefunden.",
                    f"columns.{column}",
                )
            )
