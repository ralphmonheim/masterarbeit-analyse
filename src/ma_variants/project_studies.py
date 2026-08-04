"""Projektbezogene Kandidaten fuer die SmallOffice-V1-Studienrichtungen."""

from __future__ import annotations

import hashlib
import json
import random
import re
from collections.abc import Iterable
from dataclasses import asdict
from pathlib import Path

from ma_parameters import variation_specification_source_fingerprint
from ma_zones import zone_specification_to_dict

from .small_office_v1 import SmallOfficeV1Study

OPTIMIZATION_DIRECTION_ID = "SD-OPTIMIZATION"
SENSITIVITY_DIRECTION_ID = "SD-SENSITIVITY"
REFERENCE_VARIANT_ID = "OPT-SB01-F100"
CAPACITY_STRATEGY_IDEAL_UNLIMITED = "ideal_unlimited"
CAPACITY_STRATEGY_REFERENCE_DIMENSIONED = "reference_dimensioned"
CAPACITY_STRATEGY_DIMENSIONED_WITH_FACTOR = "dimensioned_with_factor"
CAPACITY_STRATEGIES = {
    CAPACITY_STRATEGY_IDEAL_UNLIMITED,
    CAPACITY_STRATEGY_REFERENCE_DIMENSIONED,
    CAPACITY_STRATEGY_DIMENSIONED_WITH_FACTOR,
}
# Bestehende Projektentwuerfe behalten ihre bisherige faktorbegrenzte Bedeutung.
LEGACY_CAPACITY_STRATEGY = CAPACITY_STRATEGY_DIMENSIONED_WITH_FACTOR
# Kompatibilitaetsalias fuer bestehende UI- und Payload-Aufrufer.
CAPACITY_STRATEGY = LEGACY_CAPACITY_STRATEGY
REQUIRED_SMALL_OFFICE_V1_DIMENSIONS = {
    "temperature_setpoint_bands",
    "coupled_heating_cooling_capacity_factors",
    "weather_ofat",
    "occupancy_ofat",
}


def small_office_study_case_rows(study: SmallOfficeV1Study) -> list[dict[str, object]]:
    """Legt Optimierung und Sensitivitaet gleichzeitig als getrennte Cases an."""
    return [
        {
            "study_case_id": "SC-OPT-SMALLOFFICE-5Z",
            "study_direction_id": OPTIMIZATION_DIRECTION_ID,
            "study_direction": "optimization",
            "label": "Optimierung – Sollwertbaender und Kapazitaetsfaktoren",
        },
        {
            "study_case_id": "SC-SENS-WEATHER-SMALLOFFICE-5Z",
            "study_direction_id": SENSITIVITY_DIRECTION_ID,
            "study_direction": "sensitivity",
            "label": "Sensitivitaet – Frankfurt-Jahreswetter",
        },
        {
            "study_case_id": "SC-SENS-OCCUPANCY-SMALLOFFICE-5Z",
            "study_direction_id": SENSITIVITY_DIRECTION_ID,
            "study_direction": "sensitivity",
            "label": "Sensitivitaet – Belegungszeiten",
        },
    ]


def build_small_office_candidate_rows(
    study: SmallOfficeV1Study,
    variation_specification: dict[str, object],
) -> list[dict[str, object]]:
    """Erzeugt die 30 Optimierungs- und 8 Sensitivitaetskandidaten."""
    _validate_small_office_variation_contract(study, variation_specification)
    capacity_strategy = capacity_strategy_from_variation_specification(variation_specification)
    factors = (
        study.capacity_factors
        if capacity_strategy == CAPACITY_STRATEGY_DIMENSIONED_WITH_FACTOR
        else tuple(factor for factor in study.capacity_factors if factor.factor_key == study.reference_factor_key)
    )
    rows: list[dict[str, object]] = []
    for band in study.setpoint_bands:
        for factor in factors:
            rows.append(
                {
                    "candidate_id": f"OPT-{band.band_key}-{factor.factor_key}",
                    "study_case_id": "SC-OPT-SMALLOFFICE-5Z",
                    "study_direction_id": OPTIMIZATION_DIRECTION_ID,
                    "study_direction": "optimization",
                    "label": f"{band.label} | Faktor {factor.factor:g}",
                    "values": {
                        "heating_setpoint_c": band.heating_setpoint_c,
                        "cooling_setpoint_c": band.cooling_setpoint_c,
                        "heating_factor": factor.factor,
                        "cooling_factor": factor.factor,
                        "capacity_strategy": capacity_strategy,
                    },
                    "status": "candidate",
                    "exclusion_reason": "",
                }
            )
    for weather in study.weather_cases:
        rows.append(
            {
                "candidate_id": f"SENS-WEATHER-{weather.weather_key}",
                "study_case_id": "SC-SENS-WEATHER-SMALLOFFICE-5Z",
                "study_direction_id": SENSITIVITY_DIRECTION_ID,
                "study_direction": "sensitivity",
                "label": weather.label,
                "values": {
                    "parent_variant_id": REFERENCE_VARIANT_ID,
                    "ofat_family": "weather",
                    "weather_key": weather.weather_key,
                    "analysis_supported": weather.analysis_supported,
                },
                "status": "candidate",
                "exclusion_reason": "",
            }
        )
    for schedule in study.occupancy_schedules:
        rows.append(
            {
                "candidate_id": f"SENS-OCC-{schedule.schedule_key}",
                "study_case_id": "SC-SENS-OCCUPANCY-SMALLOFFICE-5Z",
                "study_direction_id": SENSITIVITY_DIRECTION_ID,
                "study_direction": "sensitivity",
                "label": schedule.label,
                "values": {
                    "parent_variant_id": REFERENCE_VARIANT_ID,
                    "ofat_family": "occupancy",
                    "operation_start_hour": schedule.start_hour,
                    "operation_end_hour": schedule.end_hour,
                    "same_values_for_all_zones": True,
                },
                "status": "candidate",
                "exclusion_reason": "",
            }
        )
    return rows


def verify_candidate_rows(
    candidates: Iterable[dict[str, object]],
    *,
    reference_dimensioning_complete: bool,
) -> list[dict[str, object]]:
    """Haelt ungueltige Kandidaten sichtbar und ergaenzt den Ausschlussgrund."""
    rows: list[dict[str, object]] = []
    for source in candidates:
        row = dict(source)
        values = row.get("values", {})
        reason = ""
        capacity_strategy = values.get("capacity_strategy") if isinstance(values, dict) else None
        if capacity_strategy != CAPACITY_STRATEGY_IDEAL_UNLIMITED and not reference_dimensioning_complete:
            reason = "Referenzdimensionierung ist unvollstaendig."
        elif not isinstance(values, dict):
            reason = "Kandidatenwerte fehlen."
        elif row.get("study_direction") == "optimization":
            heating = values.get("heating_setpoint_c")
            cooling = values.get("cooling_setpoint_c")
            if not isinstance(heating, int | float) or not isinstance(cooling, int | float):
                reason = "Temperatur-Sollwertband ist unvollstaendig."
            elif heating >= cooling:
                reason = "Heizsollwert muss kleiner als der Kuehlsollwert sein."
            elif values.get("heating_factor") != values.get("cooling_factor"):
                reason = "Heiz- und Kuehlfaktor muessen gekoppelt sein."
        row["status"] = "excluded" if reason else "valid"
        row["exclusion_reason"] = reason
        rows.append(row)
    return rows


def select_candidate_ids(
    valid_candidate_ids: tuple[str, ...],
    *,
    mode: str,
    manual_ids: tuple[str, ...] = (),
    count: int = 1,
    seed: int | None = None,
) -> tuple[str, ...]:
    if mode == "alle":
        return valid_candidate_ids
    if mode == "manuell":
        if not manual_ids:
            raise ValueError("Die manuelle Auswahl braucht mindestens einen Kandidaten.")
        unknown = set(manual_ids) - set(valid_candidate_ids)
        if unknown:
            raise ValueError(f"Nicht auswaehlbare Kandidaten: {', '.join(sorted(unknown))}")
        return tuple(candidate_id for candidate_id in valid_candidate_ids if candidate_id in manual_ids)
    if mode != "zufaellig":
        raise ValueError(f"Unbekannter Auswahlmodus: {mode}")
    if not 1 <= count <= len(valid_candidate_ids):
        raise ValueError("Die Zufallsanzahl liegt ausserhalb des gueltigen Katalogs.")
    return tuple(sorted(random.Random(seed).sample(valid_candidate_ids, count)))


def source_fingerprint(*payloads: object) -> str:
    serialized = json.dumps(payloads, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def candidate_source_is_current(
    variants_payload: dict[str, object],
    current_fingerprint: str,
) -> bool:
    """Verhindert, dass alte Kandidaten mit einem neuen Fingerprint etikettiert werden."""
    candidates = variants_payload.get("candidates")
    return (
        isinstance(candidates, list)
        and bool(candidates)
        and variants_payload.get("source_fingerprint") == current_fingerprint
    )


def variation_specification_is_current(
    parameter_payload: dict[str, object],
    baseline,
    study: SmallOfficeV1Study,
) -> bool:
    specification = parameter_payload.get("variation_specification")
    if not isinstance(specification, dict) or specification.get("status") != "current":
        return False
    contract = {
        "baseline_snapshot_id": baseline.snapshot_id,
        "baseline_snapshot_version": baseline.snapshot_version,
        "baseline_content_hash": baseline.content_hash,
        "rules": parameter_payload.get("rules", []),
        "variation_spans": parameter_payload.get("variation_spans", []),
        "study_contract": specification.get("study_contract"),
    }
    expected = variation_specification_source_fingerprint(
        baseline,
        rules=contract["rules"],
        variation_spans=contract["variation_spans"],
        study_contract=contract["study_contract"],
    )
    if specification.get("source_fingerprint") != expected:
        return False
    try:
        _validate_small_office_variation_contract(study, specification)
    except ValueError:
        return False
    return True


def small_office_source_fingerprint(
    study: SmallOfficeV1Study,
    baseline,
    zone_spec,
    parameter_payload: dict[str, object],
    dimensioning_payload: dict[str, object],
) -> str:
    """Bindet alle fachlichen Upstream-Staende an Katalog und Variantenpakete."""
    return source_fingerprint(
        asdict(study),
        {
            "snapshot_id": baseline.snapshot_id,
            "snapshot_version": baseline.snapshot_version,
            "content_hash": baseline.content_hash,
        },
        zone_specification_to_dict(zone_spec),
        parameter_payload.get("variation_specification"),
        parameter_payload.get("variation_spans"),
        parameter_payload.get("rules"),
        dimensioning_payload,
    )


def materialize_zonal_capacities(
    candidate: dict[str, object],
    zone_loads: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Bindet den gekoppelten Faktor an jede zonale 21/24-Referenzlast."""
    values = candidate.get("values", {})
    if not isinstance(values, dict):
        raise ValueError("Kandidatenwerte fehlen.")
    capacity_strategy = str(values.get("capacity_strategy", LEGACY_CAPACITY_STRATEGY))
    if capacity_strategy not in CAPACITY_STRATEGIES:
        raise ValueError("Unbekannte Kapazitaetsstrategie.")
    factor_value = values.get("heating_factor") if candidate.get("study_direction") == "optimization" else 1.0
    if not isinstance(factor_value, int | float):
        raise ValueError("Kapazitaetsfaktor fehlt.")
    factor = float(factor_value)
    rows: list[dict[str, object]] = []
    for source in zone_loads:
        if not isinstance(source, dict):
            raise ValueError("Zonale Referenzlast ist ungueltig.")
        heating = float(source["heating_load_w"])
        cooling = float(source["cooling_load_w"])
        rows.append(
            {
                "zone_id": str(source["zone_id"]),
                "zone_name": str(source.get("zone_name", "")),
                "reference_heating_load_w": heating,
                "reference_cooling_load_w": cooling,
                "heating_factor": factor,
                "cooling_factor": factor,
                "capacity_strategy": capacity_strategy,
                "available_heating_capacity_w": (
                    None if capacity_strategy == CAPACITY_STRATEGY_IDEAL_UNLIMITED else round(heating * factor, 6)
                ),
                "available_cooling_capacity_w": (
                    None if capacity_strategy == CAPACITY_STRATEGY_IDEAL_UNLIMITED else round(cooling * factor, 6)
                ),
            }
        )
    return rows


def candidate_simulation_setup(
    study: SmallOfficeV1Study,
    candidate: dict[str, object],
) -> dict[str, object]:
    """Materialisiert Wetter, Belegung und Jahresrandbedingungen je Kandidat."""
    values = candidate.get("values", {})
    if not isinstance(values, dict):
        raise ValueError("Kandidatenwerte fehlen.")
    direction = str(candidate.get("study_direction", ""))
    weather_key = (
        str(values.get("weather_key"))
        if direction == "sensitivity" and values.get("ofat_family") == "weather"
        else study.reference_weather_key
    )
    schedule_key = (
        next(
            schedule.schedule_key
            for schedule in study.occupancy_schedules
            if schedule.start_hour == values.get("operation_start_hour")
            and schedule.end_hour == values.get("operation_end_hour")
        )
        if direction == "sensitivity" and values.get("ofat_family") == "occupancy"
        else study.reference_schedule_key
    )
    weather = next(item for item in study.weather_cases if item.weather_key == weather_key)
    schedule = next(item for item in study.occupancy_schedules if item.schedule_key == schedule_key)
    year_match = re.search(r"(20\d{2})", weather.weather_key)
    simulation_year = int(year_match.group(1)) if year_match else 2015
    weather_path = Path(weather.source_path) if weather.source_path else None
    weather_file_sha256 = _file_sha256(weather_path) if weather_path is not None and weather_path.is_file() else ""
    return {
        "weather_key": weather.weather_key,
        "weather_label": weather.label,
        "weather_analysis_supported": weather.analysis_supported,
        "occupancy_schedule_key": schedule.schedule_key,
        "occupancy_start_hour": schedule.start_hour,
        "occupancy_end_hour": schedule.end_hour,
        "same_values_for_all_zones": True,
        "time_zone": "Europe/Berlin",
        "simulation_period": "annual",
        "simulation_start": f"{simulation_year:04d}-01-01T00:00:00",
        "simulation_end": f"{simulation_year:04d}-12-31T23:00:00",
        "calendar_definition": "TRY_non_leap_standard_year_8760",
        "daylight_saving_time": False,
        "simulation_timestep_seconds": 3600,
        "weather_source_reference": {
            "source_path": weather.source_path,
            "source_revision": weather.source_revision,
            "source_file_sha256": weather_file_sha256,
            "study_record_fingerprint": source_fingerprint(asdict(weather)),
            "source_status": (
                "resolved_local_file" if weather_file_sha256 else "source_resolution_required_before_simulation"
            ),
        },
        "preparation_only": True,
    }


def _validate_small_office_variation_contract(
    study: SmallOfficeV1Study,
    specification: dict[str, object],
) -> None:
    if specification.get("status") != "current":
        raise ValueError("Die Parameter-Variationsspezifikation ist nicht aktuell.")
    contract = specification.get("study_contract")
    if not isinstance(contract, dict) or contract.get("study_id") != study.study_id:
        raise ValueError("Die Variationsspezifikation bestaetigt nicht den V1-Studienvertrag.")
    enabled = contract.get("enabled_dimensions")
    if (
        not isinstance(enabled, list)
        or any(not isinstance(value, str) for value in enabled)
        or len(enabled) != len(set(enabled))
        or set(enabled) != REQUIRED_SMALL_OFFICE_V1_DIMENSIONS
    ):
        raise ValueError(
            "Die V1-Variationsdimensionen muessen den vier freigegebenen Dimensionen exakt und eindeutig entsprechen."
        )
    capacity_strategy_from_variation_specification(specification)


def capacity_strategy_from_variation_specification(specification: dict[str, object]) -> str:
    """Liest die vor der Dimensionierung festgelegte Kapazitaetsstrategie."""
    contract = specification.get("study_contract")
    if not isinstance(contract, dict):
        raise ValueError("Die Variationsspezifikation besitzt keinen Studienvertrag.")
    strategy = str(contract.get("capacity_strategy", LEGACY_CAPACITY_STRATEGY))
    if strategy not in CAPACITY_STRATEGIES:
        raise ValueError("Der Studienvertrag besitzt eine ungueltige Kapazitaetsstrategie.")
    return strategy


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
