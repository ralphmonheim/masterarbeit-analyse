"""UI-neutraler SmallOffice-V1-PreProcess bis ma_simulation_setup."""

from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from time import perf_counter
from typing import Any, Callable

import yaml

from ma_analyse.stage_1_dimensioning import ReferenceDimensioningResult, run_lod1_reference_dimensioning
from ma_building import load_small_office_5z_endvariant_02_building_spec, validate_building_spec
from ma_parameters import (
    BaselineParameterSnapshot,
    ParameterSnapshot,
    build_small_office_5z_v1_baseline_parameter_snapshot,
    build_small_office_5z_v1_parameter_snapshot,
    validate_baseline_parameter_snapshot,
    validate_parameter_snapshot,
)
from ma_simulation_setup import SimulationSetupSpecification, build_run_manifest, materialize_run_package
from ma_technical import load_small_office_5z_endvariant_02_technical_spec, validate_technical_spec
from ma_validation import DiagnosticMessage, DiagnosticSeverity
from ma_variants import (
    OptimizationCase,
    SensitivityCase,
    SmallOfficeV1Study,
    build_small_office_v1_optimization_cases,
    build_small_office_v1_sensitivity_cases,
    load_small_office_v1_study,
)
from ma_weather import import_weather_catalog
from ma_zones import (
    load_small_office_5z_endvariant_02_zone_spec,
    validate_technical_zone_integration,
    validate_zone_spec,
)

DEFAULT_SMALL_OFFICE_V1_OUTPUT_ROOT = Path("data/test_output/small_office/preprocess")
STEP_ORDER = (
    ("project", "Projekt"),
    ("weather", "Wetter"),
    ("building", "Gebaeude"),
    ("zones", "Zonen"),
    ("technical", "Technik"),
    ("parameters", "Parameter"),
    ("dimensioning", "Referenzdimensionierung"),
    ("parameter_variations", "Parameter-Variationsspezifikation"),
    ("variants", "Varianten"),
    ("simulation_setup", "Simulation-Setup"),
)


class PreProcessStepStatus(StrEnum):
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class PreProcessStepTrace:
    step_key: str
    label: str
    status: PreProcessStepStatus
    duration_seconds: float
    inputs: tuple[str, ...]
    process: tuple[str, ...]
    outputs: tuple[str, ...]
    handover: tuple[str, ...]
    technical_result: str
    domain_result: str
    diagnostics: tuple[dict[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class SmallOfficeV1PreProcessResult:
    run_id: str
    output_directory: Path
    steps: tuple[PreProcessStepTrace, ...]
    optimization_cases: tuple[OptimizationCase, ...]
    sensitivity_cases: tuple[SensitivityCase, ...]

    @property
    def has_critical_error(self) -> bool:
        return any(step.status in {PreProcessStepStatus.ERROR, PreProcessStepStatus.BLOCKED} for step in self.steps)


StepAction = Callable[[], tuple[Any, tuple[DiagnosticMessage, ...], tuple[str, ...], tuple[str, ...]]]


def run_small_office_v1_preprocess(
    *,
    run_id: str,
    output_root: str | Path = DEFAULT_SMALL_OFFICE_V1_OUTPUT_ROOT,
) -> SmallOfficeV1PreProcessResult:
    """Fuehrt die freigegebene V1-Kette aus und materialisiert nur Draft-Pakete."""
    run_directory = Path(output_root) / run_id
    if run_directory.exists():
        raise FileExistsError(f"PreProcess-Ausgabe existiert bereits: {run_directory}")
    run_directory.mkdir(parents=True)

    artifacts: dict[str, Any] = {}
    traces: list[PreProcessStepTrace] = []

    def execute(
        step_key: str,
        label: str,
        *,
        dependencies: tuple[str, ...],
        inputs: tuple[str, ...],
        process: tuple[str, ...],
        action: StepAction,
    ) -> None:
        blocking = [
            trace.step_key
            for trace in traces
            if trace.step_key in dependencies and trace.status in {PreProcessStepStatus.ERROR, PreProcessStepStatus.BLOCKED}
        ]
        if blocking:
            traces.append(
                PreProcessStepTrace(
                    step_key=step_key,
                    label=label,
                    status=PreProcessStepStatus.BLOCKED,
                    duration_seconds=0.0,
                    inputs=inputs,
                    process=process,
                    outputs=(),
                    handover=(),
                    technical_result=f"Blockiert durch: {', '.join(blocking)}",
                    domain_result="Keine fachliche Verarbeitung.",
                )
            )
            return

        started = perf_counter()
        try:
            artifact, diagnostics, outputs, handover = action()
            artifacts[step_key] = artifact
            status = _status_from_diagnostics(diagnostics)
            traces.append(
                PreProcessStepTrace(
                    step_key=step_key,
                    label=label,
                    status=status,
                    duration_seconds=round(perf_counter() - started, 6),
                    inputs=inputs,
                    process=process,
                    outputs=outputs,
                    handover=handover,
                    technical_result=_technical_result(status, diagnostics),
                    domain_result=_domain_result(status, outputs),
                    diagnostics=tuple(_diagnostic_payload(message) for message in diagnostics),
                )
            )
        except Exception as exc:  # noqa: BLE001 - Runner protokolliert Modulfehler strukturiert.
            traces.append(
                PreProcessStepTrace(
                    step_key=step_key,
                    label=label,
                    status=PreProcessStepStatus.ERROR,
                    duration_seconds=round(perf_counter() - started, 6),
                    inputs=inputs,
                    process=process,
                    outputs=(),
                    handover=(),
                    technical_result=f"Kritischer Fehler: {exc}",
                    domain_result="Kein freigabefaehiges Fachartefakt.",
                    diagnostics=(
                        {
                            "severity": "error",
                            "code": f"PREPROCESS_{step_key.upper()}_EXCEPTION",
                            "message": str(exc),
                            "location": step_key,
                        },
                    ),
                )
            )

    execute(
        "project",
        "Projekt",
        dependencies=(),
        inputs=("Versionierte SmallOffice-V1-Studienkonfiguration",),
        process=("Projekt- und Studien-ID laden", "V1-Referenzen pruefen"),
        action=_project_action,
    )
    execute(
        "weather",
        "Wetter",
        dependencies=("project",),
        inputs=("Vier benannte Frankfurt-Jahresfaelle", "Versionierter Wetterkatalog"),
        process=("2015/2045 im Katalog pruefen", "2010/2035 als vorbereitende Metadaten markieren"),
        action=lambda: _weather_action(artifacts["project"]),
    )
    execute(
        "building",
        "Gebaeude",
        dependencies=("project",),
        inputs=("Endvariante 02: 29 Raeume und aggregierte Huellgeometrie",),
        process=("Building-Spezifikation laden", "Geometrie und Referenzen validieren"),
        action=_building_action,
    )
    execute(
        "zones",
        "Zonen",
        dependencies=("building",),
        inputs=("Fuenf feste Zonen", "29 Raum-Zonen-Zuordnungen"),
        process=("Zonen gegen Gebaeude validieren", "Aktives thermisches Modell freigeben"),
        action=lambda: _zones_action(artifacts["building"]),
    )
    execute(
        "technical",
        "Technik",
        dependencies=("zones",),
        inputs=("Endvariante 02: technische Ausgangswerte", "Aktives Zonenmodell und Zonen-IDs"),
        process=("Technik eigenstaendig validieren", "Technik gegen aktive Zonen-IDs pruefen"),
        action=lambda: _technical_action(artifacts["zones"]),
    )
    execute(
        "parameters",
        "Parameter",
        dependencies=("weather", "building", "technical", "zones"),
        inputs=("Gebaeude-, Zonen- und Technikstand", "Referenzwetter-Metadatum"),
        process=("ParameterSnapshot bilden", "BaselineParameterSnapshot bilden und validieren"),
        action=_parameters_action,
    )
    execute(
        "dimensioning",
        "Referenzdimensionierung",
        dependencies=("parameters",),
        inputs=("SmallOffice-V1 ParameterSnapshot mit 21/24 Grad C",),
        process=("Mehrzonen-Heizlast und interne Kuehllast transparent berechnen",),
        action=lambda: _dimensioning_action(artifacts["parameters"][0]),
    )
    execute(
        "parameter_variations",
        "Parameter-Variationsspezifikation",
        dependencies=("dimensioning",),
        inputs=("Parameter-Referenzstand", "Referenzdimensionierung", "SmallOffice-V1-Studienregeln"),
        process=("Regeln und Wertespannen pruefen", "Variationsspezifikation fuer Kandidaten freigeben"),
        action=lambda: _parameter_variations_action(
            artifacts["project"],
            artifacts["parameters"][1],
            artifacts["dimensioning"],
        ),
    )
    execute(
        "variants",
        "Varianten",
        dependencies=("parameter_variations",),
        inputs=("Fuenf globale Sollwertbaender", "Sechs gemeinsame Heiz-/Kuehlleistungsfaktoren"),
        process=("30 kartesische Optimierungsfaelle erzeugen", "Acht Sensitivitaetsfaelle vorbereiten"),
        action=lambda: _variants_action(
            artifacts["project"],
            artifacts["parameters"][1],
            artifacts["dimensioning"],
        ),
    )
    execute(
        "simulation_setup",
        "Simulation-Setup",
        dependencies=("variants",),
        inputs=("30 Optimierungsfaelle", "Acht Sensitivitaetsfaelle", "OutputRequirementProfiles"),
        process=("Draft-Run-Manifeste bauen", "Simulatorneutrale Pakete materialisieren"),
        action=lambda: _simulation_setup_action(
            run_directory,
            artifacts["project"],
            artifacts["parameters"][1],
            artifacts["variants"][0],
            artifacts["variants"][1],
        ),
    )

    optimization_cases, sensitivity_cases = artifacts.get("variants", ((), ()))
    result = SmallOfficeV1PreProcessResult(
        run_id=run_id,
        output_directory=run_directory,
        steps=tuple(traces),
        optimization_cases=optimization_cases,
        sensitivity_cases=sensitivity_cases,
    )
    _write_run_reports(result)
    return result


def small_office_v1_summary_rows() -> list[dict[str, object]]:
    """Liefert die festgelegte Studie ohne einen Lauf zu starten."""
    study = load_small_office_v1_study()
    return [
        {"Merkmal": "Studie", "Wert": study.label},
        {"Merkmal": "Zonen", "Wert": 5},
        {"Merkmal": "Sollwertbaender", "Wert": len(study.setpoint_bands)},
        {"Merkmal": "Kapazitaetsfaktoren", "Wert": len(study.capacity_factors)},
        {"Merkmal": "Optimierungsfaelle", "Wert": len(study.setpoint_bands) * len(study.capacity_factors)},
        {"Merkmal": "Wetter-Sensitivitaet", "Wert": len(study.weather_cases)},
        {"Merkmal": "Belegungs-Sensitivitaet", "Wert": len(study.occupancy_schedules)},
    ]


def _project_action() -> tuple[SmallOfficeV1Study, tuple[DiagnosticMessage, ...], tuple[str, ...], tuple[str, ...]]:
    study = load_small_office_v1_study()
    return (
        study,
        (),
        (f"Studie {study.study_id}", "Endvariante 02 als feste V1-Geometrie"),
        ("Studienvertrag an Wetter, Gebaeude und Varianten",),
    )


def _weather_action(
    study: SmallOfficeV1Study,
) -> tuple[SmallOfficeV1Study, tuple[DiagnosticMessage, ...], tuple[str, ...], tuple[str, ...]]:
    catalog = import_weather_catalog(include_local=False)
    known_keys = {dataset.weather_key for dataset in catalog.datasets}
    required_active = {"TRY_FFM_2015_JAHR", "TRY_FFM_2045_JAHR"}
    missing = sorted(required_active - known_keys)
    if missing:
        raise ValueError(f"Erforderliche Frankfurt-Wetterkatalogeintraege fehlen: {', '.join(missing)}")
    diagnostics = tuple(
        DiagnosticMessage(
            DiagnosticSeverity.WARNING,
            "PREPROCESS_WEATHER_METADATA_ONLY",
            f"{case.label} ist nur als Simulation-Setup-Metadatum vorbereitet; PRN-Adapter und Analyse fehlen.",
            case.weather_key,
        )
        for case in study.weather_cases
        if not case.analysis_supported
    )
    return (
        study,
        diagnostics,
        tuple(case.label for case in study.weather_cases),
        ("Vier Wetterfall-Referenzen an Simulation-Setup",),
    )


def _building_action() -> tuple[Any, tuple[DiagnosticMessage, ...], tuple[str, ...], tuple[str, ...]]:
    spec = load_small_office_5z_endvariant_02_building_spec()
    validation = validate_building_spec(spec)
    return (
        spec,
        validation.messages,
        (
            f"{len(spec.spaces)} Raeume",
            f"{sum(space.floor_area_m2 for space in spec.spaces):.3f} m2",
            f"{sum(space.volume_m3 for space in spec.spaces):.5f} m3",
            "Zweigeschossige Lobbygeometrie als Quellenstand dokumentiert",
        ),
        ("BuildingModelSpecification an Technik-Zonen-Kette und Parameter",),
    )


def _technical_action(
    zone_spec: Any,
) -> tuple[Any, tuple[DiagnosticMessage, ...], tuple[str, ...], tuple[str, ...]]:
    spec = load_small_office_5z_endvariant_02_technical_spec()
    local_validation = validate_technical_spec(spec)
    integration_validation = validate_technical_zone_integration(zone_spec, spec)
    diagnostics = (*local_validation.messages, *integration_validation.messages)
    return (
        spec,
        tuple(diagnostics),
        (f"{len(spec.systems)} technische Systeme", "Technik-Zonen-Integritaet freigegeben"),
        ("TechnicalSystemSpecification an Parameter",),
    )


def _zones_action(
    building_spec: Any,
) -> tuple[Any, tuple[DiagnosticMessage, ...], tuple[str, ...], tuple[str, ...]]:
    spec = load_small_office_5z_endvariant_02_zone_spec()
    local_validation = validate_zone_spec(spec, building_spec=building_spec)
    return (
        spec,
        local_validation.messages,
        (f"{len(spec.zones)} thermische Zonen", "29 von 29 Raeumen zugeordnet", "Kein neuer V1-Zonenzuschnitt"),
        ("ZoneModelSpecification und aktive Zonen-IDs an Technik",),
    )


def _parameters_action(
) -> tuple[
    tuple[ParameterSnapshot, BaselineParameterSnapshot],
    tuple[DiagnosticMessage, ...],
    tuple[str, ...],
    tuple[str, ...],
]:
    snapshot = build_small_office_5z_v1_parameter_snapshot()
    baseline = build_small_office_5z_v1_baseline_parameter_snapshot()
    snapshot_validation = validate_parameter_snapshot(snapshot)
    baseline_validation = validate_baseline_parameter_snapshot(baseline)
    diagnostics = (*snapshot_validation.messages, *baseline_validation.messages)
    return (
        (snapshot, baseline),
        tuple(diagnostics),
        (f"{len(snapshot.values)} Parameterwerte", f"Baseline-Hash {baseline.content_hash}"),
        ("ParameterSnapshot an Dimensionierung", "BaselineParameterSnapshot an Varianten und Simulation-Setup"),
    )


def _dimensioning_action(
    snapshot: ParameterSnapshot,
) -> tuple[ReferenceDimensioningResult, tuple[DiagnosticMessage, ...], tuple[str, ...], tuple[str, ...]]:
    result = run_lod1_reference_dimensioning(snapshot)
    return (
        result,
        result.messages,
        (
            f"Heizlast {result.heating_total_load_w} W",
            f"Interne Kuehllast {result.cooling_internal_load_w} W",
            f"Luftvolumenstrom {result.ventilation_volume_flow_m3_h} m3/h",
        ),
        ("ReferenceDimensioningResult an Varianten",),
    )


def _parameter_variations_action(
    study: SmallOfficeV1Study,
    baseline: BaselineParameterSnapshot,
    dimensioning: ReferenceDimensioningResult,
) -> tuple[SmallOfficeV1Study, tuple[DiagnosticMessage, ...], tuple[str, ...], tuple[str, ...]]:
    if baseline.snapshot_id != study.baseline_snapshot_id:
        raise ValueError("Variationsspezifikation referenziert nicht den aktuellen Baseline-Stand.")
    if dimensioning.heating_total_load_w is None or dimensioning.cooling_internal_load_w is None:
        raise ValueError("Variationsspezifikation braucht eine vollstaendige Referenzdimensionierung.")
    return (
        study,
        (),
        (
            f"{len(study.setpoint_bands)} Temperatur-Sollwertbaender",
            f"{len(study.capacity_factors)} gekoppelte Heiz-/Kuehlfaktoren",
        ),
        ("ParameterVariationSpecification an Varianten",),
    )


def _variants_action(
    study: SmallOfficeV1Study,
    baseline: BaselineParameterSnapshot,
    dimensioning: ReferenceDimensioningResult,
) -> tuple[
    tuple[tuple[OptimizationCase, ...], tuple[SensitivityCase, ...]],
    tuple[DiagnosticMessage, ...],
    tuple[str, ...],
    tuple[str, ...],
]:
    optimization_cases = build_small_office_v1_optimization_cases(baseline, dimensioning, study)
    sensitivity_cases = build_small_office_v1_sensitivity_cases(baseline, study, optimization_cases)
    return (
        (optimization_cases, sensitivity_cases),
        (),
        (f"{len(optimization_cases)} Optimierungsfaelle", f"{len(sensitivity_cases)} Sensitivitaetsfaelle"),
        ("Verifizierte PreprocessVariant-Objekte an Simulation-Setup",),
    )


def _simulation_setup_action(
    run_directory: Path,
    study: SmallOfficeV1Study,
    baseline: BaselineParameterSnapshot,
    optimization_cases: tuple[OptimizationCase, ...],
    sensitivity_cases: tuple[SensitivityCase, ...],
) -> tuple[tuple[int, int], tuple[DiagnosticMessage, ...], tuple[str, ...], tuple[str, ...]]:
    schedule_by_key = {item.schedule_key: item for item in study.occupancy_schedules}
    weather_by_key = {item.weather_key: item for item in study.weather_cases}
    reference_schedule = schedule_by_key[study.reference_schedule_key]
    reference_weather = weather_by_key[study.reference_weather_key]

    optimization_root = run_directory / "optimization"
    for case in optimization_cases:
        setup = SimulationSetupSpecification(
            study_id=study.study_id,
            study_case_type="optimization",
            weather_key=reference_weather.weather_key,
            weather_label=reference_weather.label,
            occupancy_schedule_key=reference_schedule.schedule_key,
            occupancy_start_hour=reference_schedule.start_hour,
            occupancy_end_hour=reference_schedule.end_hour,
        )
        manifest = build_run_manifest(
            baseline,
            case.variant,
            run_id=f"RUN-{case.case_id}",
            release=False,
            simulation_setup=setup,
        )
        materialize_run_package(manifest, case.variant, optimization_root)

    sensitivity_root = run_directory / "sensitivity"
    for case in sensitivity_cases:
        schedule = schedule_by_key[case.schedule_key]
        weather = weather_by_key[case.weather_key]
        setup = SimulationSetupSpecification(
            study_id=study.study_id,
            study_case_type=f"sensitivity_{case.sensitivity_type}",
            weather_key=weather.weather_key,
            weather_label=weather.label,
            occupancy_schedule_key=schedule.schedule_key,
            occupancy_start_hour=schedule.start_hour,
            occupancy_end_hour=schedule.end_hour,
            parent_variant_id=case.parent_variant_id,
            preparation_only=case.preparation_only,
        )
        manifest = build_run_manifest(
            baseline,
            case.variant,
            run_id=f"RUN-{case.case_id}",
            release=False,
            simulation_setup=setup,
        )
        materialize_run_package(manifest, case.variant, sensitivity_root)

    return (
        (len(optimization_cases), len(sensitivity_cases)),
        (),
        (
            f"{len(optimization_cases)} Draft-Run-Pakete Optimierung",
            f"{len(sensitivity_cases)} Draft-Run-Pakete Sensitivitaet",
        ),
        ("Manuelle V1-Pruefung; kein Simulationsstart und keine Ergebnisbewertung",),
    )


def _status_from_diagnostics(diagnostics: tuple[DiagnosticMessage, ...]) -> PreProcessStepStatus:
    if any(message.severity is DiagnosticSeverity.ERROR for message in diagnostics):
        return PreProcessStepStatus.ERROR
    if any(message.severity is DiagnosticSeverity.WARNING for message in diagnostics):
        return PreProcessStepStatus.WARNING
    return PreProcessStepStatus.SUCCESS


def _technical_result(status: PreProcessStepStatus, diagnostics: tuple[DiagnosticMessage, ...]) -> str:
    return f"{status.value}; {len(diagnostics)} strukturierte Meldungen"


def _domain_result(status: PreProcessStepStatus, outputs: tuple[str, ...]) -> str:
    if status is PreProcessStepStatus.ERROR:
        return "Fachartefakt blockiert."
    return "; ".join(outputs)


def _diagnostic_payload(message: DiagnosticMessage) -> dict[str, str]:
    return {
        "severity": message.severity.value,
        "code": message.code,
        "message": message.message,
        "location": message.location or "",
    }


def _write_run_reports(result: SmallOfficeV1PreProcessResult) -> None:
    modules_directory = result.output_directory / "modules"
    modules_directory.mkdir()
    for index, trace in enumerate(result.steps, start=1):
        payload = _trace_payload(trace)
        (modules_directory / f"{index:02d}_{trace.step_key}.yaml").write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    summary = {
        "run_id": result.run_id,
        "created_at": datetime.now().astimezone().isoformat(),
        "status": "blocked" if result.has_critical_error else "prepared_for_manual_v1_review",
        "simulation_started": False,
        "optimization_case_count": len(result.optimization_cases),
        "sensitivity_case_count": len(result.sensitivity_cases),
        "source_metadata": {
            "endvariant": "ENDVAR-02-5Z-OHNE",
            "zone_model_id": "ZONEVAR-REDUCED-5-BOUNDARIES-REMOVED-001",
            "room_count": 29,
            "zone_count": 5,
            "floor_area_m2": 516.842,
            "volume_m3": 1677.64455,
            "source_archive": "data/catalogs/sources/demo_masterarbeit_endvarianten_optionen_v2.zip",
            "source_archive_sha256": _file_hash(
                Path("data/catalogs/sources/demo_masterarbeit_endvarianten_optionen_v2.zip")
            ),
        },
        "steps": [_trace_payload(trace) for trace in result.steps],
    }
    (result.output_directory / "preprocess_run.yaml").write_text(
        yaml.safe_dump(summary, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    all_diagnostics = [
        {"step": trace.step_key, **diagnostic}
        for trace in result.steps
        for diagnostic in trace.diagnostics
    ]
    (result.output_directory / "diagnostics.yaml").write_text(
        yaml.safe_dump({"diagnostics": all_diagnostics}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    with (result.output_directory / "timings.csv").open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=("step", "label", "status", "duration_seconds"))
        writer.writeheader()
        writer.writerows(
            {
                "step": trace.step_key,
                "label": trace.label,
                "status": trace.status.value,
                "duration_seconds": f"{trace.duration_seconds:.6f}",
            }
            for trace in result.steps
        )
    (result.output_directory / "manual_v1_acceptance.md").write_text(
        "# Manueller V1-Abnahmelauf\n\n"
        "Dieser Ordner enthaelt die Vorbereitung bis einschliesslich "
        "`ma_simulation_setup`. Alle Run-Pakete sind `draft`; es wurde keine "
        "Simulation gestartet und kein Ergebnis bewertet.\n\n"
        "V1 wird erst nach der manuellen Pruefung der Moduluebergaben, "
        "Diagnosen, 30 Optimierungsfaelle und Sensitivitaetspakete bestaetigt.\n",
        encoding="utf-8",
    )


def _trace_payload(trace: PreProcessStepTrace) -> dict[str, object]:
    return {
        "step_key": trace.step_key,
        "label": trace.label,
        "status": trace.status.value,
        "duration_seconds": trace.duration_seconds,
        "inputs": list(trace.inputs),
        "process": list(trace.process),
        "outputs": list(trace.outputs),
        "handover": list(trace.handover),
        "technical_result": trace.technical_result,
        "domain_result": trace.domain_result,
        "diagnostics": list(trace.diagnostics),
    }


def _file_hash(path: Path) -> str:
    if not path.is_file():
        return "source_file_missing"
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SmallOffice-V1-PreProcess bis Simulation-Setup")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_SMALL_OFFICE_V1_OUTPUT_ROOT))
    args = parser.parse_args(argv)
    result = run_small_office_v1_preprocess(run_id=args.run_id, output_root=args.output_root)
    print(result.output_directory)
    return 1 if result.has_critical_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
