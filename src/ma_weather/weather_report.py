"""Markdown-Bericht fuer Wetteranalysen."""

from __future__ import annotations

from pathlib import Path

from .try_importer import TryImportResult
from .weather_catalog import WeatherDataset
from .weather_metrics import WeatherMetrics
from .weather_plots import WeatherPlotResult
from .weather_validation import WeatherValidationReport


def write_weather_report(
    *,
    dataset: WeatherDataset,
    import_result: TryImportResult,
    validation_report: WeatherValidationReport,
    metrics: WeatherMetrics,
    plot_results: tuple[WeatherPlotResult, ...],
    output_dir: str | Path = "data/ma_weather/reports",
) -> Path:
    """Schreibt einen einfachen Markdown-Bericht fuer einen Wetterdatensatz."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    report_path = output_path / f"{dataset.weather_key}_weather_report.md"
    report_path.write_text(
        _build_report_markdown(
            dataset=dataset,
            import_result=import_result,
            validation_report=validation_report,
            metrics=metrics,
            plot_results=plot_results,
            output_dir=output_path,
        ),
        encoding="utf-8",
    )
    return report_path


def _build_report_markdown(
    *,
    dataset: WeatherDataset,
    import_result: TryImportResult,
    validation_report: WeatherValidationReport,
    metrics: WeatherMetrics,
    plot_results: tuple[WeatherPlotResult, ...],
    output_dir: Path,
) -> str:
    lines = [
        f"# Wetterbericht {dataset.weather_key}",
        "",
        "## Datensatz",
        "",
        f"- Name: {dataset.display_name}",
        f"- weather_key: {dataset.weather_key}",
        f"- Quelle: {dataset.source}",
        f"- Ort: {dataset.location}",
        f"- Jahrtyp: {dataset.year_type}",
        f"- Klimaszenario: {dataset.climate_scenario or '-'}",
        f"- Dateipfad: `{dataset.file_path}`",
        f"- Ausgabeordner: `{output_dir}`",
        "",
        "## Import",
        "",
        f"- Eingelesene Stundenwerte: {import_result.row_count}",
        f"- Zeitraum: {import_result.data.index.min()} bis {import_result.data.index.max()}",
        f"- Spalten: {', '.join(import_result.columns)}",
        "",
        "## Validierung",
        "",
        f"- Status: {validation_report.status}",
        f"- Fehlende Pflichtspalten: {', '.join(validation_report.missing_columns) or '-'}",
        f"- Doppelte Zeitstempel: {validation_report.duplicate_timestamps}",
        f"- Fehlende Werte: {validation_report.missing_values or '-'}",
        "",
        "### Warnungen",
        "",
        *_list_items(validation_report.warnings),
        "",
        "### Fehler",
        "",
        *_list_items(validation_report.errors),
        "",
        "## Kennwerte",
        "",
        "| Kennwert | Wert |",
        "|---|---:|",
    ]
    lines.extend(f"| `{key}` | {_format_metric(value)} |" for key, value in metrics.as_dict().items())
    lines.extend(
        [
            "",
            "## Diagramme",
            "",
        ]
    )
    for plot_result in plot_results:
        path_text = f"`{plot_result.path}`" if plot_result.path else "-"
        lines.append(f"- {plot_result.plot_key}: {plot_result.status}, {path_text}")
        for warning in plot_result.warnings:
            lines.append(f"  - Warnung: {warning}")
    lines.extend(
        [
            "",
            "## Offene Punkte",
            "",
            "- Fachliche Interpretation und Variantenverknuepfung erfolgen in spaeteren Projektschritten.",
        ]
    )
    return "\n".join(lines) + "\n"


def _list_items(values: tuple[str, ...]) -> list[str]:
    if not values:
        return ["- keine"]
    return [f"- {value}" for value in values]


def _format_metric(value: float | int | None) -> str:
    if value is None:
        return "-"
    if isinstance(value, int):
        return str(value)
    return f"{value:.2f}"
