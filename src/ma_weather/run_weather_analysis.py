"""Runner fuer die lokale Wetteranalyse."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .try_importer import TryImportResult, import_try_weather_file
from .weather_catalog import DEFAULT_WEATHER_DATASETS_CONFIG, WeatherDataset, import_weather_catalog
from .weather_metrics import WeatherMetrics, calculate_weather_metrics
from .weather_plots import WeatherPlotResult, build_weather_plots
from .weather_report import write_weather_report
from .weather_validation import WeatherValidationReport, validate_weather_dataframe


@dataclass(frozen=True, slots=True)
class WeatherAnalysisResult:
    """Ergebnis eines vollstaendigen Wetteranalyse-Laufs."""

    dataset: WeatherDataset
    import_result: TryImportResult
    validation_report: WeatherValidationReport
    metrics: WeatherMetrics
    plot_results: tuple[WeatherPlotResult, ...]
    processed_data_path: Path
    report_path: Path


def run_weather_analysis(
    weather_key: str = "TRY_FFM_2015",
    *,
    catalog_path: str | Path = DEFAULT_WEATHER_DATASETS_CONFIG,
    project_root: str | Path | None = None,
    database_dir: str | Path = "data/ma_weather/database",
    output_dir: str | Path = "data/ma_weather/output",
    reports_dir: str | Path = "data/ma_weather/reports",
    start_year: int = 2015,
    print_summary: bool = True,
) -> WeatherAnalysisResult:
    """Fuehrt Import, Validierung, Kennwerte, Diagramme und Bericht fuer einen Datensatz aus."""
    root = Path.cwd() if project_root is None else Path(project_root)
    catalog = import_weather_catalog(catalog_path)
    dataset = catalog.get(weather_key)
    source_path = dataset.resolved_file_path(root)

    import_result = import_try_weather_file(source_path, weather_key=dataset.weather_key, start_year=start_year)
    validation_report = validate_weather_dataframe(import_result.data)
    metrics = calculate_weather_metrics(import_result.data)

    processed_data_path = _write_processed_data(import_result, root / database_dir, dataset.weather_key)
    plot_results = build_weather_plots(import_result.data, weather_key=dataset.weather_key, output_dir=root / output_dir)
    report_path = write_weather_report(
        dataset=dataset,
        import_result=import_result,
        validation_report=validation_report,
        metrics=metrics,
        plot_results=plot_results,
        output_dir=root / reports_dir,
    )

    result = WeatherAnalysisResult(
        dataset=dataset,
        import_result=import_result,
        validation_report=validation_report,
        metrics=metrics,
        plot_results=plot_results,
        processed_data_path=processed_data_path,
        report_path=report_path,
    )
    if print_summary:
        _print_summary(result)
    return result


def _write_processed_data(import_result: TryImportResult, output_dir: Path, weather_key: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{weather_key}_weather_data.csv"
    import_result.data.to_csv(output_path, index=True)
    return output_path


def _print_summary(result: WeatherAnalysisResult) -> None:
    created_plots = [plot for plot in result.plot_results if plot.status == "created"]
    print(f"Wetteranalyse: {result.dataset.weather_key}")
    print(f"Status Validierung: {result.validation_report.status}")
    print(f"Stundenwerte: {result.import_result.row_count}")
    print(f"Diagramme erzeugt: {len(created_plots)}")
    print(f"Bericht: {result.report_path}")


def main(argv: Sequence[str] | None = None) -> None:
    """Kleiner Modul-Einstieg fuer lokale Wetteranalysen."""
    parser = argparse.ArgumentParser(description="Lokale TRY-Wetteranalyse ausfuehren.")
    parser.add_argument("--weather-key", default="TRY_FFM_2015", help="Technischer weather_key aus dem Wetterkatalog.")
    parser.add_argument(
        "--catalog",
        default=str(DEFAULT_WEATHER_DATASETS_CONFIG),
        help="Pfad zur Wetterkatalog-YAML.",
    )
    parser.add_argument("--start-year", type=int, default=2015, help="Jahr fuer den abgeleiteten Zeitindex.")
    args = parser.parse_args(argv)

    run_weather_analysis(
        args.weather_key,
        catalog_path=args.catalog,
        start_year=args.start_year,
    )


if __name__ == "__main__":
    main()
