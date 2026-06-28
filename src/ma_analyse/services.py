"""UI-neutrale Service-Fassade fuer die ma_analyse-Pipeline."""

from __future__ import annotations

import argparse
import contextlib
import io
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .analysis.templates import DEFAULT_OUTDOOR_COLUMN, get_plot_template_spec, list_heating_year_overlay_sources
from .app.commands import check_required_data, execute_steps, get_comfort_output_settings, run_all
from .core.config import ROOMS
from .models import AnalysisConfig, AnalysisResult, AnalysisStepResult
from .settings.plot_templates import get_plot_template_defaults

ALLOWED_STEPS = {
    "prepare",
    "plots",
    "overview",
    "analysis",
    "analyze",
    "analyze-data",
    "analyze_data",
    "heating",
    "cooling",
    "comfort",
    "plot_template",
    "plot-template",
    "all",
}

STEP_ALIASES = {
    "analyze-data": "analyze",
    "analyze_data": "analyze",
    "plot-template": "plot_template",
}


@dataclass(frozen=True)
class AnalysisRuntimeOptions:
    """Interne, UI-neutrale Laufoptionen fuer den aktuellen Legacy-Runner.

    Die Struktur trennt normalisierte Servicewerte vom alten
    ``argparse.Namespace``-Objekt. Solange ``app.commands`` noch den
    Namespace erwartet, baut ein Adapter daraus das Legacy-Argumentobjekt.
    """

    input_dir: Path
    database_dir: Path
    output_root: Path
    run_id: str | None
    debug: bool
    variants: list[str] | None
    rooms: list[str]
    export_format: str
    view: str
    month: str | None
    week: int | None
    day: int | None
    variant_mode: str | None
    series_layout: str | None
    comfort_output_type: str | None
    template: str
    plot_template_mode: str
    plot_template_options: dict[str, Any]
    setpoint_min: float
    setpoint_max: float
    temperature_ymin: float
    temperature_ymax: float
    outdoor_column: str
    show_setpoint_band: bool
    show_outdoor_temperature: bool
    show_operative_temperature: bool
    overlay_lines: object | None
    fixed_overlays: object | None
    primary_axis_mode: str
    primary_ymin: object | None
    primary_ymax: object | None
    secondary_axis_mode: str
    secondary_ymin: object | None
    secondary_ymax: object | None


@dataclass(frozen=True)
class LegacyExecutionResult:
    """Ergebnis des aktuellen Legacy-Orchestrator-Aufrufs."""

    success: bool
    errors: list[str]
    log_text: str


def _strip_variant_suffix(variant_name: str) -> str:
    for suffix in ("_rohdaten", "_nutzdaten"):
        if variant_name.endswith(suffix):
            return variant_name[: -len(suffix)]
    return variant_name


def list_input_variant_names(input_dir: Path | str) -> list[str]:
    """Listet IDA-Importvarianten fuer Prepare-Aufrufe."""
    root = Path(input_dir)
    if not root.is_dir():
        return []

    variants = []
    for child in root.iterdir():
        if not child.is_dir():
            continue
        if any((child / room_name).is_dir() for room_name in ROOMS):
            variants.append(_strip_variant_suffix(child.name))
    return sorted(set(variants))


def list_database_variant_names(database_dir: Path | str) -> list[str]:
    """Listet aufbereitete Datenbankvarianten fuer Analyseaufrufe."""
    root = Path(database_dir)
    if not root.is_dir():
        return []

    return sorted(
        {
            _strip_variant_suffix(child.name)
            for child in root.iterdir()
            if child.is_dir() and child.name.endswith("_nutzdaten")
        }
    )


def list_analysis_variants(step: str, input_dir: Path | str, database_dir: Path | str) -> list[str]:
    """Listet passende Varianten fuer einen Analysebefehl."""
    normalized_step = STEP_ALIASES.get(step, step.replace("-", "_"))
    if normalized_step == "prepare":
        return list_input_variant_names(input_dir)
    return list_database_variant_names(database_dir)


def list_analysis_rooms() -> list[str]:
    """Gibt die bekannten Analyse-Raeume zurueck."""
    return ROOMS.copy()


def list_plot_overlay_sources(
    database_dir: Path | str,
    input_dir: Path | str,
    variant_name: str | None,
    room_name: str | None,
    outdoor_column: str = DEFAULT_OUTDOOR_COLUMN,
) -> dict[str, list[str]]:
    """Listet verfuegbare Overlay-Spalten fuer Plot-Template-Aufrufe.

    Die UI bekommt bewusst nur einen robusten Katalog zurueck. Fehlende lokale
    Daten sind in der Oberflaeche kein Fehler, sondern bedeuten: manuelle
    Overlay-Eingabe bleibt moeglich.
    """
    if not variant_name or not room_name:
        return {"csv": [], "aux": []}

    try:
        return list_heating_year_overlay_sources(
            database_dir,
            input_dir,
            variant_name,
            room_name,
            outdoor_column=outdoor_column,
        )
    except Exception:  # noqa: BLE001 - Katalog ist UI-Komfort, kein harter Analysefehler.
        return {"csv": [], "aux": []}


def get_plot_template_ui_defaults(template: str, config_path: str | Path | None = None) -> dict[str, object]:
    """Gibt Plot-Template-Defaults fuer UI-Adapter zurueck."""
    if config_path is None:
        return get_plot_template_defaults(template)
    return get_plot_template_defaults(template, config_path)


def get_plot_template_ui_spec(template: str) -> dict[str, object]:
    """Gibt die UI-relevante Plot-Template-Spezifikation als Plain-Dict zurueck."""
    spec = get_plot_template_spec(template)
    if spec is None:
        return {
            "name": template,
            "metric": "",
            "view": "",
            "supports_overlays": False,
            "requires_single_room": True,
        }
    return {
        "name": spec.name,
        "metric": spec.metric,
        "view": spec.view,
        "supports_overlays": spec.supports_overlays,
        "requires_single_room": spec.requires_single_room,
    }


def _normalize_steps(steps: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(STEP_ALIASES.get(step, step.replace("-", "_")) for step in steps)


def _validate_config(config: AnalysisConfig) -> list[str]:
    errors: list[str] = []
    if not config.steps:
        errors.append("Es wurde kein Analyse-Schritt angegeben.")

    unknown_steps = [step for step in config.steps if step not in ALLOWED_STEPS]
    if unknown_steps:
        errors.append(f"Unbekannte Analyse-Schritte: {', '.join(unknown_steps)}")

    if not config.rooms:
        errors.append("Es wurde kein Raum angegeben.")

    if config.export_format not in {"csv", "excel", "both"}:
        errors.append("export_format muss csv, excel oder both sein.")
    if "plot_template" in _normalize_steps(config.steps) and config.plot_template_mode not in {"single", "compare"}:
        errors.append("plot_template_mode muss single oder compare sein.")

    return errors


def _build_runtime_options(config: AnalysisConfig) -> AnalysisRuntimeOptions:
    """Normalisiert ``AnalysisConfig`` fuer den Servicepfad."""
    plot_options = dict(config.plot_template_options)
    return AnalysisRuntimeOptions(
        input_dir=config.input_dir,
        database_dir=config.database_dir,
        output_root=config.output_root,
        run_id=config.run_id,
        debug=config.debug,
        variants=config.variants.copy() if config.variants is not None else None,
        rooms=config.rooms.copy(),
        export_format=config.export_format,
        view=config.view or "bar",
        month=config.month,
        week=config.week,
        day=config.day,
        variant_mode=config.variant_mode,
        series_layout=config.series_layout,
        comfort_output_type=config.comfort_output_type,
        template=config.plot_template or str(plot_options.get("template", "heating-year")),
        plot_template_mode=config.plot_template_mode,
        plot_template_options=plot_options,
        setpoint_min=float(plot_options.get("setpoint_min", 21.0)),
        setpoint_max=float(plot_options.get("setpoint_max", 26.0)),
        temperature_ymin=float(plot_options.get("temperature_ymin", -20.0)),
        temperature_ymax=float(plot_options.get("temperature_ymax", 40.0)),
        outdoor_column=str(plot_options.get("outdoor_column", "tair")),
        show_setpoint_band=bool(plot_options.get("show_setpoint_band", True)),
        show_outdoor_temperature=bool(plot_options.get("show_outdoor_temperature", True)),
        show_operative_temperature=bool(plot_options.get("show_operative_temperature", True)),
        overlay_lines=plot_options.get("overlay_lines"),
        fixed_overlays=plot_options.get("fixed_overlays"),
        primary_axis_mode=str(plot_options.get("primary_axis_mode", "automatic")),
        primary_ymin=plot_options.get("primary_ymin"),
        primary_ymax=plot_options.get("primary_ymax"),
        secondary_axis_mode=str(plot_options.get("secondary_axis_mode", "automatic")),
        secondary_ymin=plot_options.get("secondary_ymin"),
        secondary_ymax=plot_options.get("secondary_ymax"),
    )


def _build_legacy_args(runtime_options: AnalysisRuntimeOptions) -> argparse.Namespace:
    """Baut das aktuelle ``argparse.Namespace`` fuer ``ma_analyse.app.commands``."""
    return argparse.Namespace(
        input_dir=str(runtime_options.input_dir),
        datenbank_dir=str(runtime_options.database_dir),
        output_root=str(runtime_options.output_root),
        output_root_explicit=True,
        run_id=runtime_options.run_id,
        debug=runtime_options.debug,
        variants=runtime_options.variants,
        rooms=runtime_options.rooms,
        export_format=runtime_options.export_format,
        view=runtime_options.view,
        month=runtime_options.month,
        week=runtime_options.week,
        day=runtime_options.day,
        heating_mode=runtime_options.variant_mode,
        heating_series_layout=runtime_options.series_layout,
        template=runtime_options.template,
        plot_template_mode=runtime_options.plot_template_mode,
        setpoint_min=runtime_options.setpoint_min,
        setpoint_max=runtime_options.setpoint_max,
        temperature_ymin=runtime_options.temperature_ymin,
        temperature_ymax=runtime_options.temperature_ymax,
        outdoor_column=runtime_options.outdoor_column,
        show_setpoint_band=runtime_options.show_setpoint_band,
        show_outdoor_temperature=runtime_options.show_outdoor_temperature,
        show_operative_temperature=runtime_options.show_operative_temperature,
        overlay_lines=runtime_options.overlay_lines,
        fixed_overlays=runtime_options.fixed_overlays,
        primary_axis_mode=runtime_options.primary_axis_mode,
        primary_ymin=runtime_options.primary_ymin,
        primary_ymax=runtime_options.primary_ymax,
        secondary_axis_mode=runtime_options.secondary_axis_mode,
        secondary_ymin=runtime_options.secondary_ymin,
        secondary_ymax=runtime_options.secondary_ymax,
    )


def _build_args(config: AnalysisConfig) -> argparse.Namespace:
    return _build_legacy_args(_build_runtime_options(config))


def _build_comfort_options(runtime_options: AnalysisRuntimeOptions) -> dict[str, object] | None:
    if not runtime_options.comfort_output_type:
        return None
    return get_comfort_output_settings(runtime_options.comfort_output_type)


def _build_heating_options(runtime_options: AnalysisRuntimeOptions) -> dict[str, object]:
    return {
        "view": runtime_options.view,
        "month": runtime_options.month,
        "week": runtime_options.week,
        "day": runtime_options.day,
        "series_layout": runtime_options.series_layout or "separate",
    }


def _snapshot_files(*roots: Path) -> set[Path]:
    files: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        files.update(path.resolve() for path in root.rglob("*") if path.is_file())
    return files


def _collect_created_files(before: set[Path], *roots: Path) -> list[Path]:
    after = _snapshot_files(*roots)
    return sorted(after - before)


def _build_step_results(
    steps: tuple[str, ...],
    *,
    success: bool,
    created_files: list[Path] | None = None,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
    log_text: str = "",
) -> list[AnalysisStepResult]:
    """Baut eine erste strukturierte Schrittuebersicht fuer Legacy-Laeufe.

    Die aktuelle Orchestrierung meldet Dateien und Logtext noch laufweit statt
    schrittgenau. Fuer Einzelschritt-Laeufe koennen diese Informationen bereits
    direkt zugeordnet werden; bei Mehrschritt-Laeufen bleibt die praezise
    Zuordnung ein P029-Folgeschritt.
    """
    if not steps:
        return []

    created = created_files or []
    warning_items = warnings or []
    error_items = errors or []
    if len(steps) == 1:
        return [
            AnalysisStepResult(
                step=steps[0],
                success=success,
                created_files=created.copy(),
                warnings=warning_items.copy(),
                errors=error_items.copy(),
                log_text=log_text,
            )
        ]

    return [
        AnalysisStepResult(
            step=step,
            success=success,
            errors=error_items.copy() if index == len(steps) - 1 else [],
            log_text=log_text if index == len(steps) - 1 else "",
        )
        for index, step in enumerate(steps)
    ]


def _get_required_data_steps(
    runtime_options: AnalysisRuntimeOptions,
    normalized_steps: tuple[str, ...],
) -> tuple[str, ...]:
    """Ermittelt die tatsaechlichen Daten-Schritte fuer die Vorbedingungspruefung."""
    if normalized_steps == ("all",):
        return ("overview", "analysis", "heating", "cooling")
    if normalized_steps == ("comfort",):
        comfort_settings = get_comfort_output_settings(
            runtime_options.comfort_output_type or "plot_analysis_overview"
        )
        return tuple(comfort_settings["steps"])
    return normalized_steps


def _execute_legacy_analysis(
    runtime_options: AnalysisRuntimeOptions,
    normalized_steps: tuple[str, ...],
) -> LegacyExecutionResult:
    """Fuehrt den aktuellen Legacy-Orchestrator gekapselt aus."""
    args = _build_legacy_args(runtime_options)
    required_data_steps = _get_required_data_steps(runtime_options, normalized_steps)
    precondition = check_required_data(args, required_data_steps)
    if not precondition.ok:
        return LegacyExecutionResult(
            success=False,
            errors=precondition.messages.copy(),
            log_text="\n".join(precondition.messages),
        )

    log_buffer = io.StringIO()
    success = True
    errors: list[str] = []

    try:
        with contextlib.redirect_stdout(log_buffer), contextlib.redirect_stderr(log_buffer):
            if normalized_steps == ("all",):
                run_all(args)
            elif normalized_steps == ("comfort",):
                comfort_settings = get_comfort_output_settings(
                    runtime_options.comfort_output_type or "plot_analysis_overview"
                )
                execute_steps(
                    args,
                    steps=tuple(comfort_settings["steps"]),
                    variants=runtime_options.variants,
                    rooms=runtime_options.rooms,
                    comfort_options=comfort_settings,
                )
            else:
                execute_steps(
                    args,
                    steps=normalized_steps,
                    variants=runtime_options.variants,
                    rooms=runtime_options.rooms,
                    heating_mode=runtime_options.variant_mode,
                    prepare_options={"export_format": runtime_options.export_format},
                    comfort_options=_build_comfort_options(runtime_options),
                    heating_options=_build_heating_options(runtime_options),
                    plot_template_options=(
                        runtime_options.plot_template_options if "plot_template" in normalized_steps else None
                    ),
                )
    except SystemExit as exc:
        success = exc.code in (0, None)
        if not success:
            errors.append(f"Analyse wurde mit Exit-Code {exc.code} beendet.")
    except Exception as exc:  # noqa: BLE001 - Service-Fassade muss UI-freundlich fehlschlagen.
        success = False
        errors.append(str(exc))
        log_buffer.write(traceback.format_exc())

    return LegacyExecutionResult(
        success=success,
        errors=errors,
        log_text=log_buffer.getvalue(),
    )


def run_analysis(config: AnalysisConfig) -> AnalysisResult:
    """Fuehrt bestehende ma_analyse-Logik ueber eine UI-neutrale Fassade aus."""
    validation_errors = _validate_config(config)
    normalized_steps = _normalize_steps(config.steps)
    if validation_errors:
        return AnalysisResult(
            success=False,
            steps=normalized_steps,
            run_id=config.run_id,
            errors=validation_errors,
            step_results=_build_step_results(
                normalized_steps,
                success=False,
                errors=validation_errors,
            ),
        )

    runtime_options = _build_runtime_options(config)
    tracked_roots = (runtime_options.database_dir, runtime_options.output_root)
    files_before = _snapshot_files(*tracked_roots)
    execution_result = _execute_legacy_analysis(runtime_options, normalized_steps)

    created_files = _collect_created_files(files_before, *tracked_roots)
    return AnalysisResult(
        success=execution_result.success,
        steps=normalized_steps,
        run_id=config.run_id,
        created_files=created_files,
        errors=execution_result.errors,
        log_text=execution_result.log_text,
        step_results=_build_step_results(
            normalized_steps,
            success=execution_result.success,
            created_files=created_files,
            errors=execution_result.errors,
            log_text=execution_result.log_text,
        ),
    )
