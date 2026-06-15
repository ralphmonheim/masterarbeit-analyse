"""Plausibilitaetspruefung fuer Wetterdaten."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

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


def validate_weather_dataframe(
    data: pd.DataFrame,
    *,
    required_columns: tuple[str, ...] = DEFAULT_REQUIRED_COLUMNS,
    expected_hours: int = 8760,
) -> WeatherValidationReport:
    """Prueft Wetterdaten robust und meldet Auffaelligkeiten strukturiert."""
    warnings: list[str] = []
    errors: list[str] = []
    row_count = len(data)

    if row_count != expected_hours:
        warnings.append(f"Stundenanzahl ist {row_count}, erwartet werden {expected_hours}.")

    missing_columns = tuple(column for column in required_columns if column not in data.columns)
    if missing_columns:
        errors.append(f"Pflichtspalten fehlen: {', '.join(missing_columns)}")

    missing_values = {column: int(count) for column, count in data.isna().sum().items() if int(count) > 0}
    if missing_values:
        warnings.append("Fehlende Werte gefunden.")

    duplicate_timestamps = int(data.index.duplicated().sum())
    if duplicate_timestamps:
        errors.append(f"Doppelte Zeitstempel gefunden: {duplicate_timestamps}")

    _check_temperature(data, warnings)
    _check_relative_humidity(data, warnings)
    _check_wind_speed(data, warnings)
    _check_radiation(data, warnings)

    status = "error" if errors else "warning" if warnings else "ok"
    return WeatherValidationReport(
        status=status,
        warnings=tuple(warnings),
        errors=tuple(errors),
        row_count=row_count,
        missing_columns=missing_columns,
        missing_values=missing_values,
        duplicate_timestamps=duplicate_timestamps,
    )


def _check_temperature(data: pd.DataFrame, warnings: list[str]) -> None:
    if "temperature_c" not in data.columns:
        return
    invalid = data["temperature_c"].dropna()
    if ((invalid < -60) | (invalid > 60)).any():
        warnings.append("Unplausible Temperaturwerte ausserhalb von -60 bis 60 Grad C gefunden.")


def _check_relative_humidity(data: pd.DataFrame, warnings: list[str]) -> None:
    if "relative_humidity_pct" not in data.columns:
        return
    values = data["relative_humidity_pct"].dropna()
    if ((values < 0) | (values > 100)).any():
        warnings.append("Relative Feuchte ausserhalb von 0 bis 100 Prozent gefunden.")


def _check_wind_speed(data: pd.DataFrame, warnings: list[str]) -> None:
    if "wind_speed_m_s" not in data.columns:
        return
    if (data["wind_speed_m_s"].dropna() < 0).any():
        warnings.append("Negative Windgeschwindigkeiten gefunden.")


def _check_radiation(data: pd.DataFrame, warnings: list[str]) -> None:
    radiation_columns = [
        column
        for column in ("direct_radiation_w_m2", "diffuse_radiation_w_m2", "global_radiation_w_m2")
        if column in data.columns
    ]
    for column in radiation_columns:
        if (data[column].dropna() < 0).any():
            warnings.append(f"Negative Strahlungswerte in {column} gefunden.")
