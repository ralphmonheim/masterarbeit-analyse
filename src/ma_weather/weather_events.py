"""Kritische Wetterereignisse fuer ausgewaehlte TRY-Datensaetze."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass(frozen=True, slots=True)
class WeatherEvent:
    """Beschreibt ein aus einem Wetterdatensatz erkanntes kritisches Ereignis."""

    event_id: str
    event_type: str
    weather_key: str
    start_time: datetime
    end_time: datetime
    value: float
    unit: str
    reason: str


def detect_critical_weather_events(data: pd.DataFrame, *, weather_key: str) -> tuple[WeatherEvent, ...]:
    """Erkennt robuste Standardereignisse fuer die spaetere P021-Auswahl."""
    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Wetterereignisse benoetigen einen DatetimeIndex.")

    events: list[WeatherEvent] = []
    if "temperature_c" in data.columns:
        daily_temperature = data["temperature_c"].resample("D").mean().dropna()
        if not daily_temperature.empty:
            events.append(
                _single_day_event(
                    weather_key=weather_key,
                    event_type="hottest_day",
                    series=daily_temperature,
                    mode="max",
                    unit="Grad C",
                    reason="Tag mit der hoechsten mittleren Aussentemperatur im ausgewaehlten Datensatz.",
                )
            )
            events.append(
                _single_day_event(
                    weather_key=weather_key,
                    event_type="coldest_day",
                    series=daily_temperature,
                    mode="min",
                    unit="Grad C",
                    reason="Tag mit der niedrigsten mittleren Aussentemperatur im ausgewaehlten Datensatz.",
                )
            )
            events.extend(_temperature_period_events(daily_temperature, weather_key=weather_key))

    if "global_radiation_w_m2" in data.columns:
        daily_radiation = (data["global_radiation_w_m2"].resample("D").sum() / 1000.0).dropna()
        if not daily_radiation.empty:
            events.append(
                _single_day_event(
                    weather_key=weather_key,
                    event_type="highest_radiation_day",
                    series=daily_radiation,
                    mode="max",
                    unit="kWh/m2d",
                    reason="Tag mit der hoechsten Globalstrahlung im ausgewaehlten Datensatz.",
                )
            )

    if "wind_speed_m_s" in data.columns:
        daily_wind = data["wind_speed_m_s"].resample("D").max().dropna()
        if not daily_wind.empty:
            events.append(
                _single_day_event(
                    weather_key=weather_key,
                    event_type="strongest_wind_day",
                    series=daily_wind,
                    mode="max",
                    unit="m/s",
                    reason="Tag mit der hoechsten stuendlichen Windgeschwindigkeit im ausgewaehlten Datensatz.",
                )
            )

    return tuple(events)


def weather_event_rows(events: tuple[WeatherEvent, ...] | list[WeatherEvent]) -> list[dict[str, object]]:
    """Bereitet Wetterereignisse fuer UI-Tabellen und Tests auf."""
    return [
        {
            "Ereignis-ID": event.event_id,
            "Typ": event.event_type,
            "weather_key": event.weather_key,
            "Start": event.start_time.isoformat(),
            "Ende": event.end_time.isoformat(),
            "Kennwert": round(event.value, 2),
            "Einheit": event.unit,
            "Begruendung": event.reason,
        }
        for event in events
    ]


def _temperature_period_events(daily_temperature: pd.Series, *, weather_key: str) -> tuple[WeatherEvent, ...]:
    if len(daily_temperature) < 3:
        return ()
    rolling_mean = daily_temperature.rolling(window=3).mean().dropna()
    return (
        _period_event(
            weather_key=weather_key,
            event_type="hottest_3day_period",
            series=rolling_mean,
            mode="max",
            unit="Grad C",
            reason="Drei-Tage-Periode mit der hoechsten mittleren Aussentemperatur.",
        ),
        _period_event(
            weather_key=weather_key,
            event_type="coldest_3day_period",
            series=rolling_mean,
            mode="min",
            unit="Grad C",
            reason="Drei-Tage-Periode mit der niedrigsten mittleren Aussentemperatur.",
        ),
    )


def _single_day_event(
    *,
    weather_key: str,
    event_type: str,
    series: pd.Series,
    mode: str,
    unit: str,
    reason: str,
) -> WeatherEvent:
    day = _selected_index(series, mode=mode)
    start_time = pd.Timestamp(day).to_pydatetime()
    end_time = (pd.Timestamp(day) + pd.Timedelta(hours=23)).to_pydatetime()
    return WeatherEvent(
        event_id=_event_id(weather_key, event_type, start_time, end_time),
        event_type=event_type,
        weather_key=weather_key,
        start_time=start_time,
        end_time=end_time,
        value=float(series.loc[day]),
        unit=unit,
        reason=reason,
    )


def _period_event(
    *,
    weather_key: str,
    event_type: str,
    series: pd.Series,
    mode: str,
    unit: str,
    reason: str,
) -> WeatherEvent:
    end_day = pd.Timestamp(_selected_index(series, mode=mode))
    start_day = end_day - pd.Timedelta(days=2)
    start_time = start_day.to_pydatetime()
    end_time = (end_day + pd.Timedelta(hours=23)).to_pydatetime()
    return WeatherEvent(
        event_id=_event_id(weather_key, event_type, start_time, end_time),
        event_type=event_type,
        weather_key=weather_key,
        start_time=start_time,
        end_time=end_time,
        value=float(series.loc[end_day]),
        unit=unit,
        reason=reason,
    )


def _selected_index(series: pd.Series, *, mode: str) -> pd.Timestamp:
    if mode == "min":
        return pd.Timestamp(series.idxmin())
    return pd.Timestamp(series.idxmax())


def _event_id(weather_key: str, event_type: str, start_time: datetime, end_time: datetime) -> str:
    return (
        f"{weather_key}_{event_type}_"
        f"{start_time:%Y%m%d%H}_{end_time:%Y%m%d%H}"
    )
