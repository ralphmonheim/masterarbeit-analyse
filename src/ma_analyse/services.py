"""UI-neutrale Service-Fassade fuer die ma_analyse-Pipeline."""

from __future__ import annotations

import argparse
import contextlib
import io
import traceback
from pathlib import Path

from .analysis.templates import DEFAULT_OUTDOOR_COLUMN, get_plot_template_spec, list_heating_year_overlay_sources
from .app.commands import execute_steps, get_comfort_output_settings, run_all
from .core.config import ROOMS
from .models import AnalysisConfig, AnalysisResult
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

    return errors


def _build_args(config: AnalysisConfig) -> argparse.Namespace:
    plot_options = config.plot_template_options
    return argparse.Namespace(
        input_dir=str(config.input_dir),
        datenbank_dir=str(config.database_dir),
        output_root=str(config.output_root),
        output_root_explicit=True,
        run_id=config.run_id,
        debug=config.debug,
        variants=config.variants,
        rooms=config.rooms,
        export_format=config.export_format,
        view=config.view or "bar",
        month=config.month,
        week=config.week,
        day=config.day,
        heating_mode=config.variant_mode,
        heating_series_layout=config.series_layout,
        template=config.plot_template or plot_options.get("template", "heating-year"),
        setpoint_min=plot_options.get("setpoint_min", 21.0),
        setpoint_max=plot_options.get("setpoint_max", 26.0),
        temperature_ymin=plot_options.get("temperature_ymin", -20.0),
        temperature_ymax=plot_options.get("temperature_ymax", 40.0),
        outdoor_column=plot_options.get("outdoor_column", "tair"),
        show_setpoint_band=plot_options.get("show_setpoint_band", True),
        show_outdoor_temperature=plot_options.get("show_outdoor_temperature", True),
        show_operative_temperature=plot_options.get("show_operative_temperature", True),
        overlay_lines=plot_options.get("overlay_lines"),
        fixed_overlays=plot_options.get("fixed_overlays"),
    )


def _build_comfort_options(config: AnalysisConfig) -> dict[str, object] | None:
    if not config.comfort_output_type:
        return None
    return get_comfort_output_settings(config.comfort_output_type)


def _build_heating_options(config: AnalysisConfig) -> dict[str, object]:
    return {
        "view": config.view or "bar",
        "month": config.month,
        "week": config.week,
        "day": config.day,
        "series_layout": config.series_layout or "separate",
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
        )

    args = _build_args(config)
    log_buffer = io.StringIO()
    success = True
    errors: list[str] = []
    tracked_roots = (config.database_dir, config.output_root)
    files_before = _snapshot_files(*tracked_roots)

    try:
        with contextlib.redirect_stdout(log_buffer), contextlib.redirect_stderr(log_buffer):
            if normalized_steps == ("all",):
                run_all(args)
            elif normalized_steps == ("comfort",):
                comfort_settings = get_comfort_output_settings(config.comfort_output_type or "plot_analysis_overview")
                execute_steps(
                    args,
                    steps=tuple(comfort_settings["steps"]),
                    variants=config.variants,
                    rooms=config.rooms,
                    comfort_options=comfort_settings,
                )
            else:
                execute_steps(
                    args,
                    steps=normalized_steps,
                    variants=config.variants,
                    rooms=config.rooms,
                    heating_mode=config.variant_mode,
                    prepare_options={"export_format": config.export_format},
                    comfort_options=_build_comfort_options(config),
                    heating_options=_build_heating_options(config),
                    plot_template_options=config.plot_template_options if "plot_template" in normalized_steps else None,
                )
    except SystemExit as exc:
        success = exc.code in (0, None)
        if not success:
            errors.append(f"Analyse wurde mit Exit-Code {exc.code} beendet.")
    except Exception as exc:  # noqa: BLE001 - Service-Fassade muss UI-freundlich fehlschlagen.
        success = False
        errors.append(str(exc))
        log_buffer.write(traceback.format_exc())

    return AnalysisResult(
        success=success,
        steps=normalized_steps,
        run_id=config.run_id,
        created_files=_collect_created_files(files_before, *tracked_roots),
        errors=errors,
        log_text=log_buffer.getvalue(),
    )
