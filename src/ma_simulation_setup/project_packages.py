"""Materialisierung bestaetigter Projektvarianten bis Simulation-Setup."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import shutil
from pathlib import Path
from time import perf_counter
from uuid import uuid4

import yaml

_RUN_GROUP_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}\Z")
_STAGING_DIRECTORY_ATTEMPTS = 32


def materialize_project_setup_packages(
    *,
    output_root: str | Path,
    run_group_id: str,
    project_id: str,
    simulation_program_key: str,
    variant_packages: list[dict[str, object]],
    source_fingerprint: str,
    study_label: str = "",
    test_only: bool = False,
    technical_timings: list[dict[str, object]] | None = None,
) -> tuple[Path, ...]:
    """Schreibt nur bestaetigte, aktuelle Pakete und startet keine Simulation."""
    materialization_started = perf_counter()
    if not _RUN_GROUP_PATTERN.fullmatch(run_group_id):
        raise ValueError("Run-Gruppen-ID enthaelt unzulaessige Zeichen oder ist zu lang.")
    if not variant_packages:
        raise ValueError("Mindestens ein bestaetigtes Variantenpaket ist erforderlich.")
    for package in variant_packages:
        if package.get("status") != "confirmed":
            raise ValueError("Simulation-Setup akzeptiert nur bestaetigte Variantenpakete.")
        if package.get("source_fingerprint") != source_fingerprint:
            raise ValueError("Ein Variantenpaket ist aktualisierungsbeduerftig.")
        _validate_complete_package(package)

    selection_ids = {package["selection_id"] for package in variant_packages}
    if len(selection_ids) != 1:
        raise ValueError("Eine Run-Gruppe muss genau eine Variantenauswahl referenzieren.")
    selection_id = next(iter(selection_ids))
    selection_references = [package["selection_reference"] for package in variant_packages]
    if any(reference != selection_references[0] for reference in selection_references):
        raise ValueError("Variantenpakete muessen dieselbe Selection referenzieren.")
    selection_reference = selection_references[0]
    _validate_selection_integrity(
        selection_reference,
        variant_packages,
        source_fingerprint,
    )
    unresolved_weather = any(
        package["simulation_setup"]["weather_source_reference"]["source_status"] != "resolved_local_file"
        for package in variant_packages
    )
    group_status = "preparation_incomplete_weather_source" if unresolved_weather else "prepared_for_manual_simulation"

    group_directory = Path(output_root) / run_group_id
    if group_directory.exists():
        raise FileExistsError(f"Run-Gruppenordner existiert bereits: {group_directory}")
    prepared_runs = []
    for index, package in enumerate(variant_packages, start=1):
        variant_id = package["variant_id"]
        run_id = f"{run_group_id}-{index:03d}"
        weather_resolved = (
            package["simulation_setup"]["weather_source_reference"]["source_status"] == "resolved_local_file"
        )
        run_status = "prepared_for_manual_simulation" if weather_resolved else "preparation_incomplete_weather_source"
        prepared_runs.append(
            (
                run_id,
                package,
                {
                    "schema_version": "1.0",
                    "run_id": run_id,
                    "run_group_id": run_group_id,
                    "selection_id": selection_id,
                    "project_id": project_id,
                    "variant_id": variant_id,
                    "variant_name": package["variant_name"],
                    "study_case_id": package["study_case_id"],
                    "study_direction_id": package["study_direction_id"],
                    "simulation_program_key": simulation_program_key,
                    "source_fingerprint": source_fingerprint,
                    "status": run_status,
                    "automatic_simulation": False,
                    "baseline_reference": package["baseline_reference"],
                    "parameter_reference": package["parameter_reference"],
                    "zone_model_reference": package["zone_model_reference"],
                    "dimensioning_reference": package["dimensioning_reference"],
                    "output_requirements": package["output_requirements"],
                },
                {
                    "schema_version": "1.0",
                    "run_id": run_id,
                    "run_group_id": run_group_id,
                    "selection_id": selection_id,
                    "selection_fingerprint": selection_reference["selection_fingerprint"],
                    "variant_id": variant_id,
                    "study_id": package["study_id"],
                    "study_case_id": package["study_case_id"],
                    "study_direction_id": package["study_direction_id"],
                    "baseline_reference": package["baseline_reference"],
                    "parameter_reference": package["parameter_reference"],
                    "zone_model_reference": package["zone_model_reference"],
                    "dimensioning_reference": package["dimensioning_reference"],
                    "capacity_strategy": package["capacity_strategy"],
                    "zonal_capacities": package["zonal_capacities"],
                    "weather": {
                        "weather_key": package["simulation_setup"]["weather_key"],
                        "weather_label": package["simulation_setup"]["weather_label"],
                        "analysis_supported": package["simulation_setup"]["weather_analysis_supported"],
                    },
                    "occupancy": {
                        "schedule_key": package["simulation_setup"]["occupancy_schedule_key"],
                        "start_hour": package["simulation_setup"]["occupancy_start_hour"],
                        "end_hour": package["simulation_setup"]["occupancy_end_hour"],
                        "same_values_for_all_zones": package["simulation_setup"]["same_values_for_all_zones"],
                    },
                    "time_zone": package["simulation_setup"]["time_zone"],
                    "simulation_period": package["simulation_setup"]["simulation_period"],
                    "simulation_start": package["simulation_setup"]["simulation_start"],
                    "simulation_end": package["simulation_setup"]["simulation_end"],
                    "calendar_definition": package["simulation_setup"]["calendar_definition"],
                    "daylight_saving_time": package["simulation_setup"]["daylight_saving_time"],
                    "simulation_timestep_seconds": package["simulation_setup"]["simulation_timestep_seconds"],
                    "weather_source_reference": package["simulation_setup"]["weather_source_reference"],
                    "output_requirements": package["output_requirements"],
                    "preparation_only": True,
                    "next_action": (
                        "manual_simulation" if weather_resolved else "resolve_weather_source_before_manual_simulation"
                    ),
                },
            )
        )

    output_directory = Path(output_root)
    output_directory.mkdir(parents=True, exist_ok=True)
    temporary_directory = _create_staging_directory(output_directory, run_group_id)
    try:
        _write_yaml_new(
            temporary_directory / "selection_manifest.yaml",
            {
                "schema_version": "1.0",
                "run_group_id": run_group_id,
                "selection_id": selection_id,
                "project_id": project_id,
                "simulation_program_key": simulation_program_key,
                "source_fingerprint": source_fingerprint,
                "variant_ids": [package["variant_id"] for package in variant_packages],
                "study_case_id": selection_reference["study_case_id"],
                "study_direction_id": selection_reference["study_direction_id"],
                "selection_fingerprint": selection_reference["selection_fingerprint"],
                "selection_mode": selection_reference["mode"],
                "random_seed": selection_reference["random_seed"],
                "status": group_status,
                "automatic_simulation": False,
            },
        )
        package_timing_rows: list[dict[str, object]] = []
        for run_id, package, manifest, setup in prepared_runs:
            package_started = perf_counter()
            run_directory = temporary_directory / run_id
            run_directory.mkdir()
            _write_yaml_new(run_directory / "run_manifest.yaml", manifest)
            _write_yaml_new(run_directory / "variant_package.yaml", package)
            _write_yaml_new(run_directory / "simulation_setup.yaml", setup)
            package_timing_rows.append(
                {
                    "stage": "simulation_setup_package",
                    "status": "success",
                    "duration_seconds": round(perf_counter() - package_started, 6),
                    "recorded_at": "",
                    "details": f"{run_id} / {package['variant_id']}",
                }
            )
        timing_rows = [*_normalized_timing_rows(technical_timings), *package_timing_rows]
        timing_rows.append(
            {
                "stage": "simulation_setup_materialization",
                "status": "success",
                "duration_seconds": round(perf_counter() - materialization_started, 6),
                "recorded_at": "",
                "details": f"{len(prepared_runs)} Run-Pakete materialisiert",
            }
        )
        _write_yaml_new(
            temporary_directory / "timings.yaml",
            {"schema_version": "1.0", "timings": timing_rows},
        )
        _write_timings_csv(temporary_directory / "timings.csv", timing_rows)
        _write_yaml_new(
            temporary_directory / "run_summary.yaml",
            {
                "schema_version": "1.0",
                "run_group_id": run_group_id,
                "project_id": project_id,
                "study_id": variant_packages[0]["study_id"],
                "study_label": study_label,
                "test_only": test_only,
                "selection_id": selection_id,
                "selection_mode": selection_reference["mode"],
                "random_seed": selection_reference["random_seed"],
                "theoretical_variant_count": _theoretical_variant_count(variant_packages),
                "selected_variant_count": len(variant_packages),
                "variant_ids": [package["variant_id"] for package in variant_packages],
                "run_ids": [run_id for run_id, *_rest in prepared_runs],
                "status": group_status,
                "automatic_simulation": False,
                "artifacts": {
                    "selection_manifest": "selection_manifest.yaml",
                    "timing_log_yaml": "timings.yaml",
                    "timing_log_csv": "timings.csv",
                    "run_manifests": [f"{run_id}/run_manifest.yaml" for run_id, *_rest in prepared_runs],
                    "variant_packages": [f"{run_id}/variant_package.yaml" for run_id, *_rest in prepared_runs],
                    "simulation_setups": [f"{run_id}/simulation_setup.yaml" for run_id, *_rest in prepared_runs],
                },
            },
        )
        temporary_directory.replace(group_directory)
    except Exception:
        shutil.rmtree(temporary_directory, ignore_errors=True)
        raise
    return tuple(group_directory / run_id for run_id, *_rest in prepared_runs)


def _normalized_timing_rows(records: list[dict[str, object]] | None) -> list[dict[str, object]]:
    if records is None:
        return []
    rows: list[dict[str, object]] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        duration = record.get("duration_seconds")
        if not isinstance(duration, int | float) or duration < 0:
            continue
        rows.append(
            {
                "stage": str(record.get("stage", "unknown")),
                "status": str(record.get("status", "success")),
                "duration_seconds": round(float(duration), 6),
                "recorded_at": str(record.get("recorded_at", "")),
                "details": str(record.get("details", "")),
            }
        )
    return rows


def _write_timings_csv(path: Path, timing_rows: list[dict[str, object]]) -> None:
    with path.open("x", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(
            target,
            fieldnames=("stage", "status", "duration_seconds", "recorded_at", "details"),
        )
        writer.writeheader()
        writer.writerows(timing_rows)


def _theoretical_variant_count(variant_packages: list[dict[str, object]]) -> int | None:
    """Leitet den Wert nur ab, wenn der UI-Test ihn als Paketmetadatum mitgibt."""
    counts = {package.get("theoretical_variant_count") for package in variant_packages}
    if len(counts) != 1:
        return None
    count = next(iter(counts))
    return count if isinstance(count, int) and count > 0 else None


def _validate_complete_package(package: dict[str, object]) -> None:
    required = (
        "variant_id",
        "variant_name",
        "study_id",
        "study_case_id",
        "study_direction_id",
        "selection_id",
        "selection_reference",
        "baseline_reference",
        "parameter_reference",
        "zone_model_reference",
        "dimensioning_reference",
        "capacity_strategy",
        "zonal_capacities",
        "simulation_setup",
        "output_requirements",
    )
    missing = [key for key in required if not package.get(key)]
    if missing:
        raise ValueError("Variantenpaket ist fachlich unvollstaendig: " + ", ".join(missing))
    selection_reference = package["selection_reference"]
    if not isinstance(selection_reference, dict):
        raise ValueError("Selection-Referenz ist ungueltig.")
    required_selection_keys = {
        "selection_id",
        "selection_fingerprint",
        "study_case_id",
        "study_direction_id",
        "mode",
        "candidate_ids",
        "random_seed",
        "source_fingerprint",
    }
    if not required_selection_keys <= set(selection_reference):
        raise ValueError("Selection-Referenz ist unvollstaendig.")
    _validate_nonempty_string_ids(
        package,
        ("variant_id", "study_case_id", "study_direction_id", "selection_id"),
        context="Variantenpaket",
    )
    _validate_nonempty_string_ids(
        selection_reference,
        ("selection_id", "study_case_id", "study_direction_id"),
        context="Selection",
    )
    candidate_ids = selection_reference["candidate_ids"]
    if (
        not isinstance(candidate_ids, list)
        or not candidate_ids
        or any(not isinstance(value, str) or not value.strip() for value in candidate_ids)
    ):
        raise ValueError("Selection-Kandidaten-IDs muessen nichtleere Strings sein.")
    capacities = package["zonal_capacities"]
    zone_reference = package["zone_model_reference"]
    if not isinstance(capacities, list) or not isinstance(zone_reference, dict):
        raise ValueError("Zonale Kapazitaeten oder Zonenreferenz sind ungueltig.")
    expected_zone_ids = zone_reference.get("zone_ids", [])
    actual_zone_ids = [row.get("zone_id") for row in capacities if isinstance(row, dict)]
    if (
        not isinstance(expected_zone_ids, list)
        or len(actual_zone_ids) != len(expected_zone_ids)
        or set(actual_zone_ids) != set(expected_zone_ids)
    ):
        raise ValueError("Zonale Kapazitaeten passen nicht zum referenzierten Zonenmodell.")
    required_capacity_keys = {
        "zone_id",
        "reference_heating_load_w",
        "reference_cooling_load_w",
        "heating_factor",
        "cooling_factor",
        "available_heating_capacity_w",
        "available_cooling_capacity_w",
    }
    if any(not isinstance(row, dict) or not required_capacity_keys <= set(row) for row in capacities):
        raise ValueError("Eine zonale Kapazitaetszeile ist unvollstaendig.")
    for row in capacities:
        try:
            reference_heating = float(row["reference_heating_load_w"])
            reference_cooling = float(row["reference_cooling_load_w"])
            heating_factor = float(row["heating_factor"])
            cooling_factor = float(row["cooling_factor"])
            available_heating = float(row["available_heating_capacity_w"])
            available_cooling = float(row["available_cooling_capacity_w"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Zonale Kapazitaetswerte muessen numerisch sein.") from exc
        numeric_values = (
            reference_heating,
            reference_cooling,
            heating_factor,
            cooling_factor,
            available_heating,
            available_cooling,
        )
        if not all(math.isfinite(value) and value >= 0 for value in numeric_values):
            raise ValueError("Zonale Kapazitaeten muessen endlich und nichtnegativ sein.")
        if heating_factor != cooling_factor:
            raise ValueError("Heiz- und Kuehlfaktor muessen gekoppelt sein.")
        if not math.isclose(
            available_heating,
            reference_heating * heating_factor,
            rel_tol=1e-9,
            abs_tol=1e-6,
        ) or not math.isclose(
            available_cooling,
            reference_cooling * cooling_factor,
            rel_tol=1e-9,
            abs_tol=1e-6,
        ):
            raise ValueError("Verfuegbare Zonenleistung muss Referenzlast mal Faktor entsprechen.")
    setup = package["simulation_setup"]
    required_setup_keys = {
        "weather_key",
        "weather_label",
        "weather_analysis_supported",
        "occupancy_schedule_key",
        "occupancy_start_hour",
        "occupancy_end_hour",
        "same_values_for_all_zones",
        "time_zone",
        "simulation_period",
        "simulation_start",
        "simulation_end",
        "calendar_definition",
        "daylight_saving_time",
        "simulation_timestep_seconds",
        "weather_source_reference",
    }
    if not isinstance(setup, dict) or not required_setup_keys <= set(setup):
        raise ValueError("Simulation-Setup-Randbedingungen sind unvollstaendig.")
    _validate_simulation_setup(setup)


def _validate_selection_integrity(
    selection: dict[str, object],
    packages: list[dict[str, object]],
    current_source_fingerprint: str,
) -> None:
    candidate_ids = selection.get("candidate_ids")
    if not isinstance(candidate_ids, list) or not candidate_ids:
        raise ValueError("Selection braucht mindestens eine Kandidaten-ID.")
    package_ids = [package["variant_id"] for package in packages]
    if (
        len(candidate_ids) != len(set(candidate_ids))
        or len(package_ids) != len(set(package_ids))
        or set(candidate_ids) != set(package_ids)
    ):
        raise ValueError("Selection und materialisierte Varianten stimmen nicht ueberein.")
    if selection.get("source_fingerprint") != current_source_fingerprint:
        raise ValueError("Selection referenziert nicht den aktuellen Upstream-Stand.")
    if any(package["selection_id"] != selection["selection_id"] for package in packages):
        raise ValueError("Variantenpaket und Selection-ID stimmen nicht ueberein.")
    if any(package["study_case_id"] != selection["study_case_id"] for package in packages):
        raise ValueError("Variantenpaket und Selection-StudyCase stimmen nicht ueberein.")
    if any(package["study_direction_id"] != selection["study_direction_id"] for package in packages):
        raise ValueError("Variantenpaket und Selection-StudyDirection stimmen nicht ueberein.")
    fingerprint_payload = {
        "study_case_id": selection["study_case_id"],
        "mode": selection["mode"],
        "candidate_ids": sorted(candidate_ids),
        "random_seed": selection["random_seed"],
        "source_fingerprint": current_source_fingerprint,
    }
    expected_fingerprint = _source_fingerprint(fingerprint_payload)
    if selection.get("selection_fingerprint") != expected_fingerprint:
        raise ValueError("Selection-Fingerprint ist inkonsistent.")
    expected_id = f"SEL-{selection['study_case_id']}-{expected_fingerprint[:12]}"
    if selection.get("selection_id") != expected_id:
        raise ValueError("Selection-ID ist inkonsistent.")


def _validate_simulation_setup(setup: dict[str, object]) -> None:
    weather_key = str(setup["weather_key"])
    year_match = re.search(r"(20\d{2})", weather_key)
    if year_match is None:
        raise ValueError("Wetter-Key enthaelt kein Simulationsjahr.")
    year = int(year_match.group(1))
    if setup["simulation_start"] != f"{year:04d}-01-01T00:00:00":
        raise ValueError("Startgrenze des Jahreslaufs ist inkonsistent.")
    if setup["simulation_end"] != f"{year:04d}-12-31T23:00:00":
        raise ValueError("Endgrenze des Jahreslaufs ist inkonsistent.")
    if setup["calendar_definition"] != "TRY_non_leap_standard_year_8760":
        raise ValueError("Der V1-Jahreslauf braucht den 8760-Stunden-TRY-Kalender.")
    if setup["daylight_saving_time"] is not False:
        raise ValueError("Der TRY-Jahreslauf darf keine Sommerzeitverschiebung anwenden.")
    if setup["simulation_timestep_seconds"] != 3600:
        raise ValueError("Der V1-Simulationszeitschritt muss 3600 Sekunden betragen.")
    if setup["time_zone"] != "Europe/Berlin":
        raise ValueError("Der V1-Jahreslauf braucht die Zeitzone Europe/Berlin.")
    if setup["simulation_period"] != "annual":
        raise ValueError("Der V1-Simulationszeitraum muss ein Jahreslauf sein.")
    weather_reference = setup["weather_source_reference"]
    if not isinstance(weather_reference, dict):
        raise ValueError("Wetterquellenreferenz ist ungueltig.")
    required_weather_keys = {
        "source_path",
        "source_revision",
        "source_file_sha256",
        "study_record_fingerprint",
        "source_status",
    }
    if not required_weather_keys <= set(weather_reference):
        raise ValueError("Wetterquellenreferenz ist unvollstaendig.")
    status = weather_reference["source_status"]
    if status not in {
        "resolved_local_file",
        "source_resolution_required_before_simulation",
    }:
        raise ValueError("Wetterquellenstatus ist ungueltig.")
    if not str(weather_reference["source_revision"]).strip():
        raise ValueError("Wetterquellenrevision fehlt.")
    if not re.fullmatch(
        r"[0-9a-f]{64}",
        str(weather_reference["study_record_fingerprint"]),
    ):
        raise ValueError("Wetter-Studienrecord-Fingerprint ist ungueltig.")
    source_hash = str(weather_reference["source_file_sha256"])
    if status == "resolved_local_file":
        source_path_value = str(weather_reference["source_path"]).strip()
        if not source_path_value:
            raise ValueError("Aufgeloeste Wetterquelle braucht einen Pfad.")
        if not re.fullmatch(r"[0-9a-f]{64}", source_hash):
            raise ValueError("Aufgeloeste Wetterquelle braucht einen SHA-256.")
        source_path = Path(source_path_value)
        if not source_path.is_file():
            raise ValueError("Aufgeloeste Wetterquelle ist am referenzierten Pfad nicht vorhanden.")
        if _file_sha256(source_path) != source_hash:
            raise ValueError("Wetterquelle stimmt nicht mit dem gespeicherten SHA-256 ueberein.")
    elif source_hash:
        raise ValueError("Nicht aufgeloeste Wetterquelle darf keinen Datei-Hash behaupten.")


def _validate_nonempty_string_ids(
    payload: dict[str, object],
    keys: tuple[str, ...],
    *,
    context: str,
) -> None:
    invalid = [key for key in keys if not isinstance(payload.get(key), str) or not str(payload[key]).strip()]
    if invalid:
        raise ValueError(f"{context}-IDs muessen nichtleere Strings sein: {', '.join(invalid)}.")


def _source_fingerprint(payload: object) -> str:
    serialized = json.dumps((payload,), sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _create_staging_directory(output_directory: Path, run_group_id: str) -> Path:
    """Erzeugt ein lokales Staging-Verzeichnis mit geerbten Windows-ACLs."""
    for _ in range(_STAGING_DIRECTORY_ATTEMPTS):
        staging_directory = output_directory / f"{run_group_id}-staging-{uuid4().hex}"
        try:
            staging_directory.mkdir()
        except FileExistsError:
            continue
        return staging_directory
    raise RuntimeError("Staging-Verzeichnis konnte nicht eindeutig erzeugt werden.")


def _write_yaml_new(path: Path, payload: dict[str, object]) -> None:
    with path.open("x", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)
