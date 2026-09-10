"""Reproduzierbarer Softwarebenchmark fuer Kapitel 5.4.

Misst ausschliesslich den bestehenden SmallOffice-V1-PreProcess bis zum
Simulation-Setup. Weder IDA ICE noch eine fachliche Nachweisfuehrung werden
gestartet oder bewertet. Die feste V1-Studie umfasst genau 30 Optimierungs-
und 8 Sensitivitaetspakete; andere Paketanzahlen werden bewusst nicht durch
Duplizieren von Varianten simuliert.
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any
from uuid import uuid4

import pandas as pd

# Der Runner muss auch ohne editable Installation aus dem Repository laufen.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from ma_variants import load_small_office_v1_study
from ma_variants.project_studies import build_small_office_candidate_rows
from ma_variants.vver_selection import create_vver_selection_record
from ma_workflow import run_small_office_v1_preprocess
from ma_analyse.analysis.templates import build_heating_year_template


REPETITIONS = 10
UPSTREAM_FINGERPRINT = "a" * 64
V1_PACKAGE_COUNT = 38
PLOT_REPETITIONS = 10
PLOT_TIMEPOINTS = 1200


def _benchmark_output_root() -> Path:
    """Legt nachvollziehbare, ignorierte Testartefakte im Repository-Testpfad ab."""
    root = REPOSITORY_ROOT / "data" / "test_output"
    root.mkdir(parents=True, exist_ok=True)
    output_root = root / "chapter_5_4_benchmark"
    output_root.mkdir(exist_ok=True)
    return output_root


def _create_plot_test_data() -> tuple[Path, Path, tuple[str, str], str]:
    """Materialisiert die bereits in ``tests/test_plot_templates.py`` genutzte Testbasis.

    Die Dateien entstehen vor der Messung. Sie sind unmittelbare, aufbereitete
    CSV-Eingaben der Plotfunktion; weder PRN-Parsing noch Datenaufbereitung
    gehören damit zur gemessenen Prozessgrenze.
    """
    root = _benchmark_output_root() / "plot_input"
    database_dir = root / "database"
    input_dir = root / "input"
    room_name = "101 lobby"
    room_stub = "101_lobby"
    variants = ("Dimensionierung", "Variante_A")
    hours = list(range(PLOT_TIMEPOINTS))
    for variant_index, variant_name in enumerate(variants):
        variant_dir = database_dir / f"{variant_name}_nutzdaten"
        variant_dir.mkdir(parents=True, exist_ok=True)
        # Der vorhandene Renderer löst die Rohdatenvariante auch ohne aktive
        # Overlays auf und verlangt dafür eine REPORT-AUX-Datei. Sie wird in
        # diesem Fall nicht geparst und liegt deshalb vor Beginn der Messung
        # nur als minimale vorhandene Eingabereferenz bereit.
        raw_variant_dir = input_dir / variant_name
        raw_variant_dir.mkdir(parents=True, exist_ok=True)
        (raw_variant_dir / "REPORT-AUX.prn").write_text("# time order tair\n", encoding="utf-8")
        pd.DataFrame(
            {
                "time": hours,
                "zone_energy_q_heat": [
                    500 + 200 * variant_index if hour % 24 < 12 else 0 for hour in hours
                ],
            }
        ).to_csv(variant_dir / f"{room_stub}.csv", index=False)
    return database_dir, input_dir, variants, room_name


def _one_plot_measurement(
    *,
    database_dir: Path,
    input_dir: Path,
    selected_variants: list[str],
    output_mode: str,
    run_id: str,
) -> dict[str, Any]:
    """Misst den vorhandenen Plot-Aufruf einschliesslich PNG-Speichern."""
    started = perf_counter()
    output = build_heating_year_template(
        datenbank_dir=database_dir,
        input_dir=input_dir,
        output_root=_benchmark_output_root() / "plot_outputs",
        selected_variants=selected_variants,
        rooms=["101 lobby"],
        output_mode=output_mode,
        show_setpoint_band=False,
        show_outdoor_temperature=False,
        show_operative_temperature=False,
        run_id=run_id,
    )
    elapsed = perf_counter() - started
    output_paths = [output] if isinstance(output, str) else output
    if not output_paths or not all(Path(path).is_file() and Path(path).stat().st_size > 1000 for path in output_paths):
        raise RuntimeError("Der Plot-Benchmark hat keine vollständige PNG-Ausgabe erzeugt.")
    return {
        "elapsed_seconds": elapsed,
        "output_files": [str(path) for path in output_paths],
        "output_format": "png",
        "variant_count": len(selected_variants),
        "room_count": 1,
        "series_count": len(selected_variants),
        "timepoint_count_per_series": PLOT_TIMEPOINTS,
    }


def _plot_case_definition(case_key: str) -> tuple[list[str], str]:
    if case_key == "year_single":
        return ["Dimensionierung"], "single"
    if case_key == "year_compare":
        return ["Dimensionierung", "Variante_A"], "compare"
    raise ValueError(f"Unbekannter Plot-Benchmarkfall: {case_key}")


def _run_plot_cold_start(case_key: str) -> dict[str, Any]:
    command = [sys.executable, str(Path(__file__).resolve()), "--plot-worker", case_key]
    started = perf_counter()
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return {
        "process_wall_seconds": perf_counter() - started,
        "worker_measurement": json.loads(completed.stdout),
    }


def _run_plot_case(case_key: str) -> dict[str, Any]:
    database_dir, input_dir, _variants, _room = _create_plot_test_data()
    selected_variants, output_mode = _plot_case_definition(case_key)
    cold_start = _run_plot_cold_start(case_key)
    run_prefix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    warm_repetitions = [
        _one_plot_measurement(
            database_dir=database_dir,
            input_dir=input_dir,
            selected_variants=selected_variants,
            output_mode=output_mode,
            run_id=f"{run_prefix}-{case_key}-WARM-{index:02d}",
        )
        for index in range(1, PLOT_REPETITIONS + 1)
    ]
    return {
        "plot_function": "ma_analyse.analysis.templates.build_heating_year_template",
        "template": "heating-year",
        "output_mode": output_mode,
        "measurement_boundary": (
            "Aufruf der vorhandenen Plotfunktion ab bereitliegender aufbereiteter CSV bis vollständig "
            "gespeicherter PNG-Datei; internes CSV-Lesen und unmittelbar plotbezogene Transformationen enthalten."
        ),
        "input_data": {
            "basis": "Reproduzierbare bestehende Testdatenstruktur aus tests/test_plot_templates.py",
            "data_kind": "synthetische Testdaten, keine Kapitel-4-Realwerte",
            "variant_count": len(selected_variants),
            "room_count": 1,
            "zone_count": 1,
            "series_count": len(selected_variants),
            "timepoint_count_per_series": PLOT_TIMEPOINTS,
            "prepared_csv_files": len(selected_variants),
        },
        "cold_start": cold_start,
        "warm_repetitions": warm_repetitions,
        "summary": _summary([item["elapsed_seconds"] for item in warm_repetitions]),
    }


def run_plot_benchmark() -> dict[str, Any]:
    """Misst vorhandenes Jahresdiagramm und vorhandenen Variantenvergleich."""
    return {
        "schema_version": "1.0",
        "benchmark_id": "BENCH-CH5-4-PLOTS-V0425",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "commit": _git_commit(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "cases": {
            "year_single": _run_plot_case("year_single"),
            "year_compare": _run_plot_case("year_compare"),
        },
    }


@dataclass(frozen=True)
class _ResolvedValue:
    parameter_key: str
    value: object
    unit: str = ""


@dataclass(frozen=True)
class _VverCandidate:
    candidate_id: str
    selected_options: tuple[tuple[str, str], ...]
    resolved_values: tuple[_ResolvedValue, ...]


def _selection_for_current_v1_workflow():
    """Erzeugt die im Test belegte VVER-Auswahl ohne Fachwerte zu veraendern."""
    study = load_small_office_v1_study()
    candidates = build_small_office_candidate_rows(
        study,
        {
            "status": "current",
            "study_contract": {
                "study_id": study.study_id,
                "enabled_dimensions": [
                    "temperature_setpoint_bands",
                    "coupled_heating_cooling_capacity_factors",
                    "weather_ofat",
                    "occupancy_ofat",
                ],
                "capacity_strategy": "dimensioned_with_factor",
            },
        },
    )
    optimization_candidates = tuple(
        _VverCandidate(
            candidate_id=str(row["candidate_id"]),
            selected_options=tuple(sorted((str(key), str(value)) for key, value in row["values"].items())),
            resolved_values=tuple(
                _ResolvedValue(str(key), value) for key, value in sorted(row["values"].items())
            ),
        )
        for row in candidates
        if row["study_direction"] == "optimization"
    )
    return create_vver_selection_record(
        study_id=study.study_id,
        study_case_id="SC-OPT-SMALLOFFICE-5Z",
        study_direction_id="SD-OPTIMIZATION",
        selection_mode="all",
        selection_reason="Kapitel-5.4-Benchmark des vorhandenen V1-Workflows.",
        pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
        selected_candidates=optimization_candidates,
    )


def _one_measurement(output_root: Path, run_id: str) -> dict[str, Any]:
    selection = _selection_for_current_v1_workflow()
    started = perf_counter()
    result = run_small_office_v1_preprocess(
        run_id=run_id,
        output_root=output_root,
        vver_selection=selection,
        vver_pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
    )
    elapsed = perf_counter() - started
    if result.has_critical_error:
        raise RuntimeError("Der PreProcess-Benchmarklauf wurde blockiert.")
    if len(result.optimization_cases) + len(result.sensitivity_cases) != V1_PACKAGE_COUNT:
        raise RuntimeError("Der aktuelle V1-Workflow erzeugte nicht die erwarteten 38 Pakete.")
    return {
        "elapsed_seconds": elapsed,
        "optimization_case_count": len(result.optimization_cases),
        "sensitivity_case_count": len(result.sensitivity_cases),
        "package_count": V1_PACKAGE_COUNT,
        "step_seconds": {step.step_key: step.duration_seconds for step in result.steps},
    }


def _summary(values: list[float]) -> dict[str, float]:
    return {
        "mean_seconds": statistics.fmean(values),
        "median_seconds": statistics.median(values),
        "min_seconds": min(values),
        "max_seconds": max(values),
        "stdev_seconds": statistics.stdev(values) if len(values) > 1 else 0.0,
    }


def _run_cold_start() -> dict[str, Any]:
    command = [sys.executable, str(Path(__file__).resolve()), "--worker"]
    started = perf_counter()
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    wall_seconds = perf_counter() - started
    payload = json.loads(completed.stdout)
    return {"process_wall_seconds": wall_seconds, "worker_measurement": payload}


def run_benchmark() -> dict[str, Any]:
    """Fuehrt einen Cold Start und zehn Warm-Wiederholungen mit frischem Output aus."""
    cold_start = _run_cold_start()
    output_root = _benchmark_output_root()
    run_prefix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    repetitions = [
        _one_measurement(output_root, f"{run_prefix}-WARM-{index:02d}")
        for index in range(1, REPETITIONS + 1)
    ]

    total_values = [item["elapsed_seconds"] for item in repetitions]
    variant_values = [item["step_seconds"]["variants"] for item in repetitions]
    setup_values = [item["step_seconds"]["simulation_setup"] for item in repetitions]
    return {
        "schema_version": "1.0",
        "benchmark_id": "BENCH-CH5-4-V0425",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "commit": _git_commit(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "measurement_boundary": (
            "run_small_office_v1_preprocess: Aufruf bis materialisierte Draft-"
            "Simulation-Setup-Pakete; kein IDA-Export, keine IDA-Simulation, kein Ergebnisimport."
        ),
        "input_case": {
            "workflow": "SmallOffice V1",
            "zone_count": 5,
            "optimization_case_count": 30,
            "sensitivity_case_count": 8,
            "package_count": V1_PACKAGE_COUNT,
        },
        "cold_start": cold_start,
        "warm_repetitions": repetitions,
        "summaries": {
            "preprocess_total": _summary(total_values),
            "variant_generation_step": _summary(variant_values),
            "simulation_setup_materialization_step": _summary(setup_values),
        },
        "unsupported_scale_points": {
            str(count): "Nicht gemessen: Der aktuelle V1-Workflow besitzt nur den fachlich definierten 38-Paket-Fall; keine Duplikation erstellt."
            for count in (1, 5, 10, 25, 50, 100)
        },
        "not_measured": [
            "IDA-ICE-Modellerzeugung, -Aenderung und -Simulation",
            "fachliche Nachweisfuehrung (Stage 3 ist NOT_EVALUABLE)",
            "Import, Datenaufbereitung, Kennwertberechnung, Excel und Diagramme: keine versionierte vollstaendige IDA-Ergebnisbasis vorhanden",
        ],
    }


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def main() -> int:
    parser = argparse.ArgumentParser(description="Kapitel-5.4-Softwarebenchmark")
    parser.add_argument("--worker", action="store_true", help="Interner Einzellauf fuer Cold-Start-Messung.")
    parser.add_argument(
        "--plot-worker",
        choices=("year_single", "year_compare"),
        help="Interner Einzellauf eines Plotfalls fuer die Cold-Start-Messung.",
    )
    parser.add_argument("--output", type=Path, help="JSON-Zieldatei fuer den Gesamtlauf.")
    parser.add_argument("--plot-output", type=Path, help="JSON-Zieldatei fuer den Plot-Benchmark.")
    args = parser.parse_args()
    if args.worker:
        run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-COLD-{uuid4().hex[:8]}"
        print(json.dumps(_one_measurement(_benchmark_output_root(), run_id), ensure_ascii=False))
        return 0
    if args.plot_worker:
        database_dir, input_dir, _variants, _room = _create_plot_test_data()
        selected_variants, output_mode = _plot_case_definition(args.plot_worker)
        run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{args.plot_worker}-COLD-{uuid4().hex[:8]}"
        print(
            json.dumps(
                _one_plot_measurement(
                    database_dir=database_dir,
                    input_dir=input_dir,
                    selected_variants=selected_variants,
                    output_mode=output_mode,
                    run_id=run_id,
                ),
                ensure_ascii=False,
            )
        )
        return 0
    if args.plot_output is not None:
        result = run_plot_benchmark()
        args.plot_output.parent.mkdir(parents=True, exist_ok=True)
        args.plot_output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(args.plot_output)
        return 0

    result = run_benchmark()
    if args.output is None:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
