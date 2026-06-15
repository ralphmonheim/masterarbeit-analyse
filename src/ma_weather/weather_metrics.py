"""Berechnung einfacher Wetterkennwerte."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd


@dataclass(frozen=True, slots=True)
class WeatherMetrics:
    """Abgeleitete Kennwerte fuer einen Wetterdatensatz."""

    mean_temperature_c: float | None
    min_temperature_c: float | None
    max_temperature_c: float | None
    mean_relative_humidity_pct: float | None
    mean_wind_speed_m_s: float | None
    max_wind_speed_m_s: float | None
    global_radiation_kwh_m2a: float | None
    hours_above_25c: int | None
    hours_above_30c: int | None
    heating_degree_hours_kh: float | None
    cooling_degree_hours_kh: float | None

    def as_dict(self) -> dict[str, float | int | None]:
        """Gibt die Kennwerte als einfaches Dictionary zurueck."""
        return asdict(self)


def calculate_weather_metrics(
    data: pd.DataFrame,
    *,
    heating_base_c: float = 20.0,
    cooling_base_c: float = 26.0,
) -> WeatherMetrics:
    """Berechnet Wetterkennwerte getrennt von Diagramm- und Reportlogik."""
    temperature = data["temperature_c"] if "temperature_c" in data.columns else None
    humidity = data["relative_humidity_pct"] if "relative_humidity_pct" in data.columns else None
    wind_speed = data["wind_speed_m_s"] if "wind_speed_m_s" in data.columns else None
    global_radiation = data["global_radiation_w_m2"] if "global_radiation_w_m2" in data.columns else None

    return WeatherMetrics(
        mean_temperature_c=_mean(temperature),
        min_temperature_c=_min(temperature),
        max_temperature_c=_max(temperature),
        mean_relative_humidity_pct=_mean(humidity),
        mean_wind_speed_m_s=_mean(wind_speed),
        max_wind_speed_m_s=_max(wind_speed),
        global_radiation_kwh_m2a=_sum_hourly_w_m2_to_kwh_m2(global_radiation),
        hours_above_25c=_count_above(temperature, 25.0),
        hours_above_30c=_count_above(temperature, 30.0),
        heating_degree_hours_kh=_degree_hours(temperature, base_temperature_c=heating_base_c, mode="heating"),
        cooling_degree_hours_kh=_degree_hours(temperature, base_temperature_c=cooling_base_c, mode="cooling"),
    )


def _mean(series: pd.Series | None) -> float | None:
    return None if series is None else float(series.mean())


def _min(series: pd.Series | None) -> float | None:
    return None if series is None else float(series.min())


def _max(series: pd.Series | None) -> float | None:
    return None if series is None else float(series.max())


def _count_above(series: pd.Series | None, threshold: float) -> int | None:
    return None if series is None else int((series > threshold).sum())


def _sum_hourly_w_m2_to_kwh_m2(series: pd.Series | None) -> float | None:
    return None if series is None else float(series.sum() / 1000.0)


def _degree_hours(series: pd.Series | None, *, base_temperature_c: float, mode: str) -> float | None:
    if series is None:
        return None
    if mode == "heating":
        values = (base_temperature_c - series).clip(lower=0)
    else:
        values = (series - base_temperature_c).clip(lower=0)
    return float(values.sum())
