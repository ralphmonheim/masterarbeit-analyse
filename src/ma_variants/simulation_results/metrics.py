"""Einlesen erster Kennwerte aus vorhandenen Raum-CSV-Dateien."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from matplotlib.path import Path as MplPath

from .models import RoomMetricResult, VariantMetricsResult, VariantResultMapping

DEFAULT_METRICS = (
    "heating_energy_kwh",
    "cooling_energy_kwh",
    "max_heating_power_w",
    "max_cooling_power_w",
    "comfort_hours",
    "overtemperature_hours_25",
    "overtemperature_hours_27",
    "max_co2_ppm",
    "mean_co2_ppm",
    "max_ppd_percent",
    "max_pmv",
    "mean_pmv",
)

COLUMN_ALIASES = {
    "heating_power": ["zone_energy_q_heat"],
    "cooling_power": ["zone_energy_q_cool"],
    "top": ["local_de_comf_diag_t_top", "temperatures_top", "top"],
    "relhum": ["iaq_relhum", "relhum"],
    "co2": ["iaq_xco2vol", "xco2vol", "co2"],
    "ppd": ["local_de_comf_diag_t_ppd", "ppd", "comfort_ppd"],
    "pmv": ["local_de_comf_diag_t_pmv", "pmv", "comfort_pmv"],
}

# Eckpunkte wie in `ma_analyse.analysis.comfort.zones`.
COMFORT_HIGH = [[17.8, 72.0], [22.0, 66.5], [23.8, 33.5], [18.4, 40.0]]
COMFORT_NORMAL = [
    [17.0, 85.5],
    [20.3, 80.0],
    [24.7, 60.0],
    [26.8, 29.0],
    [25.9, 20.0],
    [19.9, 20.0],
    [17.0, 34.5],
    [16.0, 74.0],
]

METRIC_REQUIRED_ALIAS_GROUPS = {
    "heating_energy_kwh": ("heating_power",),
    "cooling_energy_kwh": ("cooling_power",),
    "max_heating_power_w": ("heating_power",),
    "max_cooling_power_w": ("cooling_power",),
    "comfort_hours": ("top", "relhum"),
    "overtemperature_hours_25": ("top",),
    "overtemperature_hours_27": ("top",),
    "max_co2_ppm": ("co2",),
    "mean_co2_ppm": ("co2",),
    "max_ppd_percent": ("ppd",),
    "max_pmv": ("pmv",),
    "mean_pmv": ("pmv",),
}


def _find_column(dataframe: pd.DataFrame, alias_group: str) -> str | None:
    for column_name in COLUMN_ALIASES[alias_group]:
        if column_name in dataframe.columns:
            return column_name
    return None


def _numeric_series(dataframe: pd.DataFrame, alias_group: str) -> pd.Series | None:
    column_name = _find_column(dataframe, alias_group)
    if column_name is None:
        return None
    return pd.to_numeric(dataframe[column_name], errors="coerce").dropna()


def _missing_columns(dataframe: pd.DataFrame, metric_names: list[str]) -> dict[str, list[str]]:
    missing: dict[str, list[str]] = {}
    for metric_name in metric_names:
        required_groups = METRIC_REQUIRED_ALIAS_GROUPS.get(metric_name, ())
        missing_groups = [
            alias_group
            for alias_group in required_groups
            if _find_column(dataframe, alias_group) is None
        ]
        if missing_groups:
            missing[metric_name] = [
                "/".join(COLUMN_ALIASES[alias_group])
                for alias_group in missing_groups
            ]
    return missing


def _count_comfort_hours(dataframe: pd.DataFrame) -> int | None:
    top = _numeric_series(dataframe, "top")
    relhum = _numeric_series(dataframe, "relhum")
    if top is None or relhum is None:
        return None
    comfort_frame = pd.DataFrame({"top": top, "relhum": relhum}).dropna()
    if comfort_frame.empty:
        return 0
    points = comfort_frame[["top", "relhum"]].to_numpy()
    high_mask = MplPath(COMFORT_HIGH).contains_points(points)
    normal_mask = MplPath(COMFORT_NORMAL).contains_points(points)
    return int((high_mask | normal_mask).sum())


def _metric_value(dataframe: pd.DataFrame, metric_name: str) -> float | int | None:
    if metric_name == "heating_energy_kwh":
        series = _numeric_series(dataframe, "heating_power")
        return None if series is None else float(series.clip(lower=0).sum() / 1000)
    if metric_name == "cooling_energy_kwh":
        series = _numeric_series(dataframe, "cooling_power")
        return None if series is None else float(series.abs().sum() / 1000)
    if metric_name == "max_heating_power_w":
        series = _numeric_series(dataframe, "heating_power")
        return None if series is None or series.empty else float(series.max())
    if metric_name == "max_cooling_power_w":
        series = _numeric_series(dataframe, "cooling_power")
        return None if series is None or series.empty else float(series.abs().max())
    if metric_name == "comfort_hours":
        return _count_comfort_hours(dataframe)
    if metric_name == "overtemperature_hours_25":
        series = _numeric_series(dataframe, "top")
        return None if series is None else int((series > 25).sum())
    if metric_name == "overtemperature_hours_27":
        series = _numeric_series(dataframe, "top")
        return None if series is None else int((series > 27).sum())
    if metric_name == "max_co2_ppm":
        series = _numeric_series(dataframe, "co2")
        return None if series is None or series.empty else float(series.max())
    if metric_name == "mean_co2_ppm":
        series = _numeric_series(dataframe, "co2")
        return None if series is None or series.empty else float(series.mean())
    if metric_name == "max_ppd_percent":
        series = _numeric_series(dataframe, "ppd")
        return None if series is None or series.empty else float(series.max())
    if metric_name == "max_pmv":
        series = _numeric_series(dataframe, "pmv")
        return None if series is None or series.empty else float(series.max())
    if metric_name == "mean_pmv":
        series = _numeric_series(dataframe, "pmv")
        return None if series is None or series.empty else float(series.mean())
    raise ValueError(f"Unbekannter Kennwert: {metric_name}")


def _room_name_from_csv(csv_path: Path) -> str:
    return csv_path.stem.replace("_", " ")


def read_room_metrics(
    csv_path: str | Path,
    variant_key: str,
    variant_name: str,
    metric_names: list[str] | tuple[str, ...] = DEFAULT_METRICS,
) -> RoomMetricResult:
    """Liest Kennwerte aus einer aufbereiteten Raum-CSV."""
    path = Path(csv_path)
    dataframe = pd.read_csv(path)
    metrics = {
        metric_name: _metric_value(dataframe, metric_name)
        for metric_name in metric_names
    }
    return RoomMetricResult(
        variant_key=variant_key,
        variant_name=variant_name,
        room_name=_room_name_from_csv(path),
        source_file=path,
        metrics=metrics,
        missing_columns=_missing_columns(dataframe, list(metric_names)),
    )


def _aggregate_room_metrics(room_metrics: list[RoomMetricResult], metric_names: list[str]) -> dict[str, float | int | None]:
    summary: dict[str, float | int | None] = {}
    sum_metrics = {
        "heating_energy_kwh",
        "cooling_energy_kwh",
        "comfort_hours",
        "overtemperature_hours_25",
        "overtemperature_hours_27",
    }
    max_metrics = {"max_heating_power_w", "max_cooling_power_w", "max_co2_ppm", "max_ppd_percent", "max_pmv"}
    mean_metrics = {"mean_co2_ppm", "mean_pmv"}

    for metric_name in metric_names:
        values = [
            room_metric.metrics[metric_name]
            for room_metric in room_metrics
            if room_metric.metrics.get(metric_name) is not None
        ]
        if not values:
            summary[metric_name] = None
        elif metric_name in sum_metrics:
            summary[metric_name] = float(sum(values))
        elif metric_name in max_metrics:
            summary[metric_name] = float(max(values))
        elif metric_name in mean_metrics:
            summary[metric_name] = float(sum(values) / len(values))
        else:
            summary[metric_name] = None
    return summary


def read_variant_metrics(
    mapping: VariantResultMapping,
    rooms: list[str] | tuple[str, ...] | None = None,
    metric_names: list[str] | tuple[str, ...] = DEFAULT_METRICS,
) -> VariantMetricsResult | None:
    """Liest Kennwerte fuer alle verfuegbaren Raum-CSV-Dateien einer zugeordneten Variante."""
    if not mapping.is_mapped or mapping.result_dir is None:
        return None

    result_dir = mapping.result_dir
    if rooms is None:
        csv_files = sorted(result_dir.glob("*.csv"), key=lambda path: path.name.casefold())
    else:
        csv_files = [result_dir / f"{room.replace(' ', '_')}.csv" for room in rooms]

    room_metrics = [
        read_room_metrics(
            csv_path=csv_file,
            variant_key=mapping.variant_key,
            variant_name=mapping.variant_name,
            metric_names=metric_names,
        )
        for csv_file in csv_files
        if csv_file.exists()
    ]

    return VariantMetricsResult(
        variant_key=mapping.variant_key,
        variant_name=mapping.variant_name,
        result_dir=result_dir,
        room_metrics=room_metrics,
        summary_metrics=_aggregate_room_metrics(room_metrics, list(metric_names)),
        metadata={
            "result_display_name": mapping.result_display_name,
            "rooms_requested": list(rooms) if rooms is not None else None,
            "rooms_read": [room_metric.room_name for room_metric in room_metrics],
        },
    )


def collect_simulation_metrics(
    mappings: list[VariantResultMapping],
    rooms: list[str] | tuple[str, ...] | None = None,
    metric_names: list[str] | tuple[str, ...] = DEFAULT_METRICS,
) -> list[VariantMetricsResult]:
    """Liest Kennwerte fuer mehrere zugeordnete Varianten."""
    results = [
        read_variant_metrics(mapping, rooms=rooms, metric_names=metric_names)
        for mapping in mappings
    ]
    return [result for result in results if result is not None]
