"""Ausgabepfade und Manifest fuer ma_weather-Laeufe."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .weather_catalog import WeatherDataset
from .weather_events import WeatherEvent
from .weather_plots import WeatherPlotResult

DEFAULT_WEATHER_OUTPUT_ROOT = Path("data/ma_weather/output")


@dataclass(frozen=True, slots=True)
class WeatherOutputPaths:
    """Gebuendelte Pfade fuer genau einen Wetteranalyse-Lauf."""

    run_output_dir: Path
    data_dir: Path
    plots_dir: Path
    reports_dir: Path
    processed_data_path: Path
    report_path: Path
    manifest_path: Path


def build_weather_output_paths(
    weather_key: str,
    run_id: str,
    *,
    output_root: str | Path = DEFAULT_WEATHER_OUTPUT_ROOT,
) -> WeatherOutputPaths:
    """Baut die Run-Ordnerstruktur fuer einen Wetterdatensatz."""
    safe_weather_key = sanitize_weather_output_name(weather_key)
    safe_run_id = sanitize_weather_output_name(run_id)
    run_output_dir = Path(output_root) / safe_weather_key / safe_run_id
    data_dir = run_output_dir / "data"
    plots_dir = run_output_dir / "plots"
    reports_dir = run_output_dir / "reports"
    return WeatherOutputPaths(
        run_output_dir=run_output_dir,
        data_dir=data_dir,
        plots_dir=plots_dir,
        reports_dir=reports_dir,
        processed_data_path=data_dir / f"{safe_weather_key}_weather_data.csv",
        report_path=reports_dir / f"{safe_weather_key}_weather_report.md",
        manifest_path=run_output_dir / "weather_run_manifest.json",
    )


def sanitize_weather_output_name(value: str) -> str:
    """Macht technische IDs fuer Ordner und Dateinamen robust."""
    normalized = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return normalized.strip("._") or "weather_output"


def write_weather_run_manifest(
    *,
    manifest_path: str | Path,
    dataset: WeatherDataset,
    import_result: Any,
    validation_report: Any,
    plot_results: tuple[WeatherPlotResult, ...],
    critical_events: tuple[WeatherEvent, ...],
    processed_data_path: Path,
    report_path: Path,
    session_log_path: Path,
    session_id: str,
    run_id: str,
    import_id: str,
    run_output_dir: Path,
    project_root: str | Path | None = None,
) -> Path:
    """Schreibt ein JSON-Manifest fuer die erzeugten Wetterartefakte."""
    target_path = Path(manifest_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    relative_base = Path.cwd() if project_root is None else Path(project_root)
    payload = {
        "module": "ma_weather",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "dataset": {
            "weather_key": dataset.weather_key,
            "display_name": dataset.display_name,
            "year_type": dataset.year_type,
            "climate_scenario": dataset.climate_scenario,
            "dataset_role": dataset.dataset_role,
            "location": dataset.location,
            "location_id": dataset.location_id,
            "reference_location_id": dataset.reference_location_id,
        },
        "ids": {
            "session_id": session_id,
            "run_id": run_id,
            "import_id": import_id,
        },
        "source": {
            "source_id": import_result.source.source_id,
            "source_kind": import_result.source.source_kind.value,
            "data_format": import_result.source.data_format,
            "source_path": str(import_result.source.source_path or ""),
            "adapter_key": import_result.source.adapter_key,
            "file_size_bytes": import_result.source.file_size_bytes,
            "sha256": import_result.source.sha256,
        },
        "validation": {
            "status": validation_report.status,
            "release_status": validation_report.validation_result.release_status.value,
            "warning_count": len(validation_report.warnings),
            "error_count": len(validation_report.errors),
            "diagnostic_ids": [
                message.diagnostic_id for message in validation_report.validation_result.messages
            ],
        },
        "artifacts": {
            "run_output_dir": _relative_path(run_output_dir, relative_base),
            "processed_data": _relative_path(processed_data_path, relative_base),
            "report": _relative_path(report_path, relative_base),
            "session_log": _relative_path(session_log_path, relative_base),
            "plots": [
                {
                    "plot_key": plot_result.plot_key,
                    "status": plot_result.status,
                    "path": _relative_path(plot_result.path, relative_base) if plot_result.path else "",
                    "warnings": list(plot_result.warnings),
                }
                for plot_result in plot_results
            ],
        },
        "critical_events": [
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "weather_key": event.weather_key,
            }
            for event in critical_events
        ],
    }
    target_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target_path


def _relative_path(path: Path | str, base_path: Path) -> str:
    candidate = Path(path)
    try:
        return candidate.relative_to(base_path).as_posix()
    except ValueError:
        return candidate.as_posix()
