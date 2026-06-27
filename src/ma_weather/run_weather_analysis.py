"""Runner fuer die lokale Wetteranalyse."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from ma_core import (
    SessionLogEvent,
    append_session_event,
    create_run_id,
    create_session_id,
)
from ma_validation import (
    ReleaseChoice,
    ReleaseDecision,
    ReleaseStatus,
    create_release_decision,
)

from .try_importer import TryImportResult, import_try_weather_file
from .weather_catalog import DEFAULT_WEATHER_DATASETS_CONFIG, WeatherDataset, import_weather_catalog
from .weather_events import WeatherEvent, detect_critical_weather_events
from .weather_metrics import WeatherMetrics, calculate_weather_metrics
from .weather_plots import ALL_WEATHER_PLOTS, WEATHER_PLOT_CHOICES, WeatherPlotResult, build_weather_plots
from .weather_report import write_weather_report
from .weather_status import create_weather_import_id
from .weather_validation import WeatherValidationReport, validate_weather_dataframe


@dataclass(frozen=True, slots=True)
class WeatherAnalysisResult:
    """Ergebnis eines vollstaendigen Wetteranalyse-Laufs."""

    dataset: WeatherDataset
    import_result: TryImportResult
    validation_report: WeatherValidationReport
    metrics: WeatherMetrics
    critical_events: tuple[WeatherEvent, ...]
    plot_results: tuple[WeatherPlotResult, ...]
    processed_data_path: Path
    report_path: Path
    import_id: str
    session_id: str
    run_id: str
    session_log_path: Path
    release_decision: ReleaseDecision | None


def run_weather_analysis(
    weather_key: str = "TRY_FFM_2015_JAHR",
    *,
    catalog_path: str | Path = DEFAULT_WEATHER_DATASETS_CONFIG,
    project_root: str | Path | None = None,
    database_dir: str | Path = "data/ma_weather/database",
    output_dir: str | Path = "data/ma_weather/output",
    reports_dir: str | Path = "data/ma_weather/reports",
    session_log_dir: str | Path = "logs/sessions",
    start_year: int = 2015,
    session_id: str | None = None,
    run_id: str | None = None,
    import_id: str | None = None,
    weather_plot_keys: Sequence[str] | None = None,
    print_summary: bool = True,
) -> WeatherAnalysisResult:
    """Fuehrt Import, Validierung, Kennwerte, Diagramme und Bericht fuer einen Datensatz aus."""
    root = Path.cwd() if project_root is None else Path(project_root)
    resolved_session_id = session_id or create_session_id()
    resolved_run_id = run_id or create_run_id("weather")
    resolved_import_id = import_id or create_weather_import_id()
    resolved_log_dir = root / session_log_dir
    session_log_path = append_session_event(
        SessionLogEvent(
            session_id=resolved_session_id,
            run_id=resolved_run_id,
            event_type="run_started",
            module_key="ma_weather",
            dataset_key=weather_key,
            related_id=resolved_import_id,
            message="Wetteranalyse gestartet.",
            details={"import_id": resolved_import_id},
        ),
        log_dir=resolved_log_dir,
    )

    try:
        catalog = import_weather_catalog(catalog_path)
        dataset = catalog.get(weather_key)
        source_path = dataset.resolved_file_path(root)

        import_result = import_try_weather_file(source_path, weather_key=dataset.weather_key, start_year=start_year)
        append_session_event(
            SessionLogEvent(
                session_id=resolved_session_id,
                run_id=resolved_run_id,
                event_type="input_source_loaded",
                module_key="ma_weather",
                dataset_key=dataset.weather_key,
                source_id=import_result.source.source_id,
                related_id=resolved_import_id,
                message="TRY-Eingabequelle geladen.",
                details={
                    "import_id": resolved_import_id,
                    "source_kind": import_result.source.source_kind.value,
                    "data_format": import_result.source.data_format,
                    "source_path": str(import_result.source.source_path or ""),
                    "adapter_key": import_result.source.adapter_key,
                    "file_size_bytes": import_result.source.file_size_bytes,
                    "sha256": import_result.source.sha256,
                },
            ),
            log_dir=resolved_log_dir,
        )
        validation_report = validate_weather_dataframe(
            import_result.data,
            additional_messages=import_result.import_diagnostic.messages,
        )
        for message in validation_report.validation_result.messages:
            append_session_event(
                SessionLogEvent(
                    session_id=resolved_session_id,
                    run_id=resolved_run_id,
                    event_type="diagnostic_recorded",
                    module_key="ma_weather",
                    dataset_key=dataset.weather_key,
                    severity=message.severity.value,
                    diagnostic_code=message.code,
                    message=message.message,
                    location=message.location,
                    source_id=import_result.source.source_id,
                    related_id=message.diagnostic_id,
                    details={"import_id": resolved_import_id},
                ),
                log_dir=resolved_log_dir,
            )

        metrics = calculate_weather_metrics(import_result.data)
        critical_events = detect_critical_weather_events(import_result.data, weather_key=dataset.weather_key)
        processed_data_path = _write_processed_data(import_result, root / database_dir, dataset.weather_key)
        plot_results = build_weather_plots(
            import_result.data,
            weather_key=dataset.weather_key,
            output_dir=root / output_dir,
            plot_keys=weather_plot_keys,
        )
        report_path = write_weather_report(
            dataset=dataset,
            import_result=import_result,
            validation_report=validation_report,
            metrics=metrics,
            plot_results=plot_results,
            output_dir=root / reports_dir,
        )

        release_decision = _automatic_release_decision(
            validation_report=validation_report,
            session_id=resolved_session_id,
            run_id=resolved_run_id,
            dataset_key=dataset.weather_key,
        )
        if release_decision is not None:
            _append_release_decision_event(release_decision, resolved_log_dir, import_id=resolved_import_id)

        append_session_event(
            SessionLogEvent(
                session_id=resolved_session_id,
                run_id=resolved_run_id,
                event_type="run_completed",
                module_key="ma_weather",
                dataset_key=dataset.weather_key,
                source_id=import_result.source.source_id,
                related_id=resolved_import_id,
                release_status=validation_report.validation_result.release_status.value,
                message="Wetteranalyse abgeschlossen.",
                details={
                    "import_id": resolved_import_id,
                    "record_count": import_result.row_count,
                    "critical_event_count": len(critical_events),
                    "processed_data_path": str(processed_data_path),
                    "report_path": str(report_path),
                    "validation_status": validation_report.status,
                },
            ),
            log_dir=resolved_log_dir,
        )
    except Exception as exc:
        append_session_event(
            SessionLogEvent(
                session_id=resolved_session_id,
                run_id=resolved_run_id,
                event_type="run_failed",
                module_key="ma_weather",
                dataset_key=weather_key,
                severity="error",
                diagnostic_code="WEATHER_RUN_FAILED",
                message=str(exc),
                related_id=resolved_import_id,
                details={"import_id": resolved_import_id},
            ),
            log_dir=resolved_log_dir,
        )
        raise

    result = WeatherAnalysisResult(
        dataset=dataset,
        import_result=import_result,
        validation_report=validation_report,
        metrics=metrics,
        critical_events=critical_events,
        plot_results=plot_results,
        processed_data_path=processed_data_path,
        report_path=report_path,
        import_id=resolved_import_id,
        session_id=resolved_session_id,
        run_id=resolved_run_id,
        session_log_path=session_log_path,
        release_decision=release_decision,
    )
    if print_summary:
        _print_summary(result)
    return result


def plot_template_weather(
    weather_key: str = "TRY_FFM_2015_JAHR",
    *,
    catalog_path: str | Path = DEFAULT_WEATHER_DATASETS_CONFIG,
    project_root: str | Path | None = None,
    database_dir: str | Path = "data/ma_weather/database",
    output_dir: str | Path = "data/ma_weather/output",
    reports_dir: str | Path = "data/ma_weather/reports",
    session_log_dir: str | Path = "logs/sessions",
    start_year: int = 2015,
    session_id: str | None = None,
    run_id: str | None = None,
    import_id: str | None = None,
    plot_key: str = ALL_WEATHER_PLOTS,
    print_summary: bool = True,
) -> WeatherAnalysisResult:
    """Fuehrt den Wetter-Template-Befehl fuer alle oder ein einzelnes Diagramm aus."""
    weather_plot_keys = None if plot_key == ALL_WEATHER_PLOTS else (plot_key,)
    return run_weather_analysis(
        weather_key,
        catalog_path=catalog_path,
        project_root=project_root,
        database_dir=database_dir,
        output_dir=output_dir,
        reports_dir=reports_dir,
        session_log_dir=session_log_dir,
        start_year=start_year,
        session_id=session_id,
        run_id=run_id,
        import_id=import_id,
        weather_plot_keys=weather_plot_keys,
        print_summary=print_summary,
    )


def _automatic_release_decision(
    *,
    validation_report: WeatherValidationReport,
    session_id: str,
    run_id: str,
    dataset_key: str,
) -> ReleaseDecision | None:
    release_status = validation_report.validation_result.release_status
    if release_status is ReleaseStatus.CONFIRMATION_REQUIRED:
        return None
    choice = (
        ReleaseChoice.KEEP_BLOCKED
        if release_status is ReleaseStatus.BLOCKED
        else ReleaseChoice.AUTOMATIC_RELEASE
    )
    return create_release_decision(
        validation_report.validation_result,
        choice=choice,
        session_id=session_id,
        run_id=run_id,
        module_key="ma_weather",
        dataset_key=dataset_key,
        note="Automatisch aus dem Validierungsergebnis abgeleitet.",
    )


def _append_release_decision_event(
    decision: ReleaseDecision,
    log_dir: Path,
    *,
    import_id: str = "",
) -> Path:
    return append_session_event(
        SessionLogEvent(
            session_id=decision.session_id,
            run_id=decision.run_id,
            event_type="release_decided",
            module_key=decision.module_key,
            dataset_key=decision.dataset_key,
            choice=decision.choice.value,
            release_status=decision.resulting_status.value,
            note=decision.note,
            related_id=decision.decision_id,
            message="Freigabeentscheidung gespeichert.",
            details={
                "diagnostic_ids": list(decision.diagnostic_ids),
                "import_id": import_id,
            },
        ),
        log_dir=log_dir,
    )


def record_weather_release_decision(
    result: WeatherAnalysisResult,
    *,
    choice: ReleaseChoice,
    note: str | None = None,
    log_dir: str | Path | None = None,
) -> ReleaseDecision:
    """Speichert eine ausdrueckliche Entscheidung fuer genau einen Wetterlauf."""
    decision = create_release_decision(
        result.validation_report.validation_result,
        choice=choice,
        session_id=result.session_id,
        run_id=result.run_id,
        module_key="ma_weather",
        dataset_key=result.dataset.weather_key,
        note=note,
    )
    target_log_dir = Path(log_dir) if log_dir is not None else result.session_log_path.parent
    _append_release_decision_event(decision, target_log_dir, import_id=result.import_id)
    return decision


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
    print(f"Import-ID: {result.import_id}")
    print(f"Session-Log: {result.session_log_path}")


def main(argv: Sequence[str] | None = None) -> None:
    """Kleiner Modul-Einstieg fuer lokale Wetteranalysen."""
    parser = argparse.ArgumentParser(description="Lokale TRY-Wetteranalyse ausfuehren.")
    parser.add_argument("--weather-key", default="TRY_FFM_2015_JAHR", help="Technischer weather_key aus dem Wetterkatalog.")
    parser.add_argument(
        "--catalog",
        default=str(DEFAULT_WEATHER_DATASETS_CONFIG),
        help="Pfad zur Wetterkatalog-YAML.",
    )
    parser.add_argument("--start-year", type=int, default=2015, help="Jahr fuer den abgeleiteten Zeitindex.")
    parser.add_argument(
        "--plot",
        choices=(ALL_WEATHER_PLOTS, *WEATHER_PLOT_CHOICES),
        default=ALL_WEATHER_PLOTS,
        help="Wetterdiagramm, das erzeugt werden soll. Standard: alle Diagramme.",
    )
    args = parser.parse_args(argv)

    plot_template_weather(
        args.weather_key,
        catalog_path=args.catalog,
        start_year=args.start_year,
        plot_key=args.plot,
    )


def main_plot_template_weather(argv: Sequence[str] | None = None) -> None:
    """CLI-Einstieg fuer ``plot-template-weather <diagramm>``."""
    parser = argparse.ArgumentParser(description="Wetterdiagramm aus einem TRY-Datensatz erzeugen.")
    parser.add_argument(
        "diagram",
        nargs="?",
        choices=(ALL_WEATHER_PLOTS, *WEATHER_PLOT_CHOICES),
        default=ALL_WEATHER_PLOTS,
        help="Diagramm-Schluessel oder 'all'.",
    )
    parser.add_argument("--weather-key", default="TRY_FFM_2015_JAHR", help="Technischer weather_key aus dem Wetterkatalog.")
    parser.add_argument(
        "--catalog",
        default=str(DEFAULT_WEATHER_DATASETS_CONFIG),
        help="Pfad zur Wetterkatalog-YAML.",
    )
    parser.add_argument("--start-year", type=int, default=2015, help="Jahr fuer den abgeleiteten Zeitindex.")
    plot_args = parser.parse_args(argv)

    plot_template_weather(
        plot_args.weather_key,
        catalog_path=plot_args.catalog,
        start_year=plot_args.start_year,
        plot_key=plot_args.diagram,
    )


if __name__ == "__main__":
    main()
