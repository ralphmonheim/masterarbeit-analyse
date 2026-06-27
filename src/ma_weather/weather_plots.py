"""Diagrammerzeugung fuer Wetterdaten."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


@dataclass(frozen=True, slots=True)
class WeatherPlotResult:
    """Ergebnis einer einzelnen Wetterdiagramm-Funktion."""

    plot_key: str
    path: Path | None
    status: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class WeatherPlotSpec:
    """Katalogeintrag fuer ein vorhandenes Wetterdiagramm."""

    plot_key: str
    label: str
    description: str


ALL_WEATHER_PLOTS = "all"

WEATHER_PLOT_SPECS: tuple[WeatherPlotSpec, ...] = (
    WeatherPlotSpec(
        "temperature_year",
        "Temperatur Jahresverlauf",
        "Aussentemperatur ueber den kompletten Wetterdatensatz.",
    ),
    WeatherPlotSpec(
        "temperature_heatmap",
        "Temperatur Heatmap",
        "Temperatur nach Tag des Jahres und Stunde.",
    ),
    WeatherPlotSpec(
        "monthly_radiation",
        "Monatliche Globalstrahlung",
        "Monatliche Summe der Globalstrahlung.",
    ),
    WeatherPlotSpec(
        "monthly_degree_hours",
        "Monatliche Gradstunden",
        "Heiz- und Kuehlgradstunden je Monat.",
    ),
    WeatherPlotSpec(
        "wind_rose",
        "Windrose",
        "Windrichtung und Haeufigkeit als einfache Polardarstellung.",
    ),
    WeatherPlotSpec(
        "temperature_humidity_scatter",
        "Temperatur und relative Feuchte",
        "Streudiagramm fuer Temperatur und relative Feuchte.",
    ),
)

WEATHER_PLOT_CHOICES: tuple[str, ...] = tuple(spec.plot_key for spec in WEATHER_PLOT_SPECS)


def build_weather_plot(
    data: pd.DataFrame,
    *,
    weather_key: str,
    output_dir: str | Path = "data/ma_weather/output",
    plot_key: str,
) -> WeatherPlotResult:
    """Erzeugt genau ein Wetterdiagramm aus dem Katalog."""
    builders = _weather_plot_builders()
    if plot_key not in builders:
        raise ValueError(f"Unbekanntes Wetterdiagramm: {plot_key}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return builders[plot_key](data, weather_key=weather_key, output_dir=output_path)


def build_weather_plots(
    data: pd.DataFrame,
    *,
    weather_key: str,
    output_dir: str | Path = "data/ma_weather/output",
    plot_keys: Iterable[str] | None = None,
) -> tuple[WeatherPlotResult, ...]:
    """Erzeugt die Standarddiagramme fuer einen Wetterdatensatz."""
    if plot_keys is None:
        requested_plot_keys = WEATHER_PLOT_CHOICES
    elif isinstance(plot_keys, str):
        requested_plot_keys = WEATHER_PLOT_CHOICES if plot_keys == ALL_WEATHER_PLOTS else (plot_keys,)
    else:
        requested_plot_keys = tuple(plot_keys)
        if requested_plot_keys == (ALL_WEATHER_PLOTS,):
            requested_plot_keys = WEATHER_PLOT_CHOICES
    return tuple(
        build_weather_plot(
            data,
            weather_key=weather_key,
            output_dir=output_dir,
            plot_key=plot_key,
        )
        for plot_key in requested_plot_keys
    )


def plot_temperature_year(
    data: pd.DataFrame,
    *,
    weather_key: str,
    output_dir: Path,
) -> WeatherPlotResult:
    """Speichert den Jahresverlauf der Aussentemperatur."""
    missing = _missing_columns(data, ("temperature_c",))
    if missing:
        return _skipped("temperature_year", missing)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(data.index, data["temperature_c"], color="#c43c39", linewidth=0.8)
    ax.set_title(f"{weather_key} - Temperatur Jahresverlauf")
    ax.set_xlabel("Zeit")
    ax.set_ylabel("Temperatur [Grad C]")
    ax.grid(True, alpha=0.25)
    return _save_plot(fig, output_dir / f"{weather_key}_temperature_year.png", "temperature_year")


def plot_temperature_heatmap(
    data: pd.DataFrame,
    *,
    weather_key: str,
    output_dir: Path,
) -> WeatherPlotResult:
    """Speichert eine Temperatur-Heatmap nach Tag des Jahres und Stunde."""
    missing = _missing_columns(data, ("temperature_c",))
    if missing:
        return _skipped("temperature_heatmap", missing)

    heatmap_data = pd.DataFrame(
        {
            "day_of_year": data.index.dayofyear,
            "hour": data.index.hour,
            "temperature_c": data["temperature_c"].to_numpy(),
        }
    )
    pivot = heatmap_data.pivot_table(index="hour", columns="day_of_year", values="temperature_c", aggfunc="mean")

    fig, ax = plt.subplots(figsize=(12, 4))
    image = ax.imshow(pivot, aspect="auto", origin="lower", cmap="coolwarm")
    ax.set_title(f"{weather_key} - Temperatur Heatmap")
    ax.set_xlabel("Tag des Jahres")
    ax.set_ylabel("Stunde des Tages")
    fig.colorbar(image, ax=ax, label="Temperatur [Grad C]")
    return _save_plot(fig, output_dir / f"{weather_key}_temperature_heatmap.png", "temperature_heatmap")


def plot_monthly_radiation(
    data: pd.DataFrame,
    *,
    weather_key: str,
    output_dir: Path,
) -> WeatherPlotResult:
    """Speichert die monatliche Globalstrahlungssumme."""
    missing = _missing_columns(data, ("global_radiation_w_m2",))
    if missing:
        return _skipped("monthly_radiation", missing)

    monthly = data["global_radiation_w_m2"].resample("ME").sum() / 1000.0
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(monthly.index.strftime("%b"), monthly, color="#4f81bd")
    ax.set_title(f"{weather_key} - Monatliche Globalstrahlung")
    ax.set_xlabel("Monat")
    ax.set_ylabel("Globalstrahlung [kWh/m2]")
    ax.grid(True, axis="y", alpha=0.25)
    return _save_plot(fig, output_dir / f"{weather_key}_monthly_radiation.png", "monthly_radiation")


def plot_monthly_degree_hours(
    data: pd.DataFrame,
    *,
    weather_key: str,
    output_dir: Path,
    heating_base_c: float = 20.0,
    cooling_base_c: float = 26.0,
) -> WeatherPlotResult:
    """Speichert monatliche Heiz- und Kuehlgradstunden."""
    missing = _missing_columns(data, ("temperature_c",))
    if missing:
        return _skipped("monthly_degree_hours", missing)

    degree_data = pd.DataFrame(index=data.index)
    degree_data["heating"] = (heating_base_c - data["temperature_c"]).clip(lower=0)
    degree_data["cooling"] = (data["temperature_c"] - cooling_base_c).clip(lower=0)
    monthly = degree_data.resample("ME").sum()

    fig, ax = plt.subplots(figsize=(9, 4))
    labels = monthly.index.strftime("%b")
    ax.bar(labels, monthly["heating"], color="#c43c39", label="Heizgradstunden")
    ax.bar(labels, monthly["cooling"], color="#4f81bd", bottom=monthly["heating"], label="Kuehlgradstunden")
    ax.set_title(f"{weather_key} - Monatliche Gradstunden")
    ax.set_xlabel("Monat")
    ax.set_ylabel("Gradstunden [Kh]")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.25)
    return _save_plot(fig, output_dir / f"{weather_key}_monthly_degree_hours.png", "monthly_degree_hours")


def plot_wind_rose(
    data: pd.DataFrame,
    *,
    weather_key: str,
    output_dir: Path,
) -> WeatherPlotResult:
    """Speichert eine einfache Windrose ohne zusaetzliche Drittbibliothek."""
    missing = _missing_columns(data, ("wind_direction_deg", "wind_speed_m_s"))
    if missing:
        return _skipped("wind_rose", missing)

    wind = data[["wind_direction_deg", "wind_speed_m_s"]].dropna()
    if wind.empty:
        return WeatherPlotResult("wind_rose", None, "skipped", ("Keine gueltigen Winddaten vorhanden.",))

    directions = wind["wind_direction_deg"] % 360
    bins = pd.cut(directions, bins=range(0, 361, 22), include_lowest=True, labels=False)
    counts = bins.value_counts().sort_index()
    angles = [index * 22 * 3.141592653589793 / 180 for index in counts.index]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"projection": "polar"})
    ax.bar(angles, counts.values, width=22 * 3.141592653589793 / 180, color="#4f81bd", alpha=0.75)
    ax.set_title(f"{weather_key} - Windrose")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    return _save_plot(fig, output_dir / f"{weather_key}_wind_rose.png", "wind_rose")


def plot_temperature_humidity_scatter(
    data: pd.DataFrame,
    *,
    weather_key: str,
    output_dir: Path,
) -> WeatherPlotResult:
    """Speichert ein Temperatur-Feuchte-Streudiagramm."""
    missing = _missing_columns(data, ("temperature_c", "relative_humidity_pct"))
    if missing:
        return _skipped("temperature_humidity_scatter", missing)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(data["temperature_c"], data["relative_humidity_pct"], s=8, color="#4f81bd", alpha=0.35)
    ax.set_title(f"{weather_key} - Temperatur und relative Feuchte")
    ax.set_xlabel("Temperatur [Grad C]")
    ax.set_ylabel("Relative Feuchte [%]")
    ax.grid(True, alpha=0.25)
    return _save_plot(
        fig,
        output_dir / f"{weather_key}_temperature_humidity_scatter.png",
        "temperature_humidity_scatter",
    )


def _missing_columns(data: pd.DataFrame, columns: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(column for column in columns if column not in data.columns)


def _skipped(plot_key: str, missing_columns: tuple[str, ...]) -> WeatherPlotResult:
    return WeatherPlotResult(
        plot_key=plot_key,
        path=None,
        status="skipped",
        warnings=(f"Diagramm uebersprungen, fehlende Spalten: {', '.join(missing_columns)}",),
    )


def _save_plot(fig: plt.Figure, path: Path, plot_key: str) -> WeatherPlotResult:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return WeatherPlotResult(plot_key=plot_key, path=path, status="created")


def _weather_plot_builders():
    return {
        "temperature_year": plot_temperature_year,
        "temperature_heatmap": plot_temperature_heatmap,
        "monthly_radiation": plot_monthly_radiation,
        "monthly_degree_hours": plot_monthly_degree_hours,
        "wind_rose": plot_wind_rose,
        "temperature_humidity_scatter": plot_temperature_humidity_scatter,
    }
