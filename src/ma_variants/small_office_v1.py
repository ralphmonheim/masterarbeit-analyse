"""Versionierter Variantenraum fuer den SmallOffice-V1-PreProcess."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ma_core import load_configuration_file
from ma_dimensionierung import VariantDimensioningAssignment
from ma_parameters import BaselineParameterSnapshot

from .preprocess import PreprocessVariant, VariationValue, build_explicit_variant

DEFAULT_SMALL_OFFICE_V1_STUDY_CONFIG = Path("config/ma_variants/studies/small_office_v1.yaml")
HEATING_CAPACITY_KEY = "TECH-SYS-HEATING-CENTRAL-001.available_capacity_w"
COOLING_CAPACITY_KEY = "TECH-SYS-COOLING-CENTRAL-001.available_capacity_w"


@dataclass(frozen=True, slots=True)
class SetpointBand:
    band_key: str
    heating_setpoint_c: float
    cooling_setpoint_c: float
    label: str


@dataclass(frozen=True, slots=True)
class CapacityFactor:
    factor_key: str
    factor: float
    label: str


@dataclass(frozen=True, slots=True)
class WeatherSensitivityCase:
    weather_key: str
    label: str
    analysis_supported: bool
    source_path: str
    source_revision: str


@dataclass(frozen=True, slots=True)
class OccupancyScheduleCase:
    schedule_key: str
    label: str
    start_hour: float
    end_hour: float


@dataclass(frozen=True, slots=True)
class SmallOfficeV1Study:
    study_id: str
    label: str
    baseline_snapshot_id: str
    reference_band_key: str
    reference_factor_key: str
    reference_weather_key: str
    reference_schedule_key: str
    setpoint_bands: tuple[SetpointBand, ...]
    capacity_factors: tuple[CapacityFactor, ...]
    weather_cases: tuple[WeatherSensitivityCase, ...]
    occupancy_schedules: tuple[OccupancyScheduleCase, ...]


@dataclass(frozen=True, slots=True)
class OptimizationCase:
    case_id: str
    band: SetpointBand
    capacity_factor: CapacityFactor
    variant: PreprocessVariant
    heating_capacity_w: float
    cooling_capacity_w: float


@dataclass(frozen=True, slots=True)
class SensitivityCase:
    case_id: str
    sensitivity_type: str
    label: str
    parent_variant_id: str
    weather_key: str
    schedule_key: str
    variant: PreprocessVariant
    preparation_only: bool = True


def load_small_office_v1_study(
    config_path: str | Path = DEFAULT_SMALL_OFFICE_V1_STUDY_CONFIG,
) -> SmallOfficeV1Study:
    """Laedt und prueft die freigegebene V1-Studienkonfiguration."""
    raw = load_configuration_file(config_path)
    study = SmallOfficeV1Study(
        study_id=str(raw["study_id"]),
        label=str(raw["label"]),
        baseline_snapshot_id=str(raw["baseline_snapshot_id"]),
        reference_band_key=str(raw["reference_band_key"]),
        reference_factor_key=str(raw["reference_factor_key"]),
        reference_weather_key=str(raw["reference_weather_key"]),
        reference_schedule_key=str(raw["reference_schedule_key"]),
        setpoint_bands=tuple(
            SetpointBand(
                band_key=str(item["band_key"]),
                heating_setpoint_c=float(item["heating_setpoint_c"]),
                cooling_setpoint_c=float(item["cooling_setpoint_c"]),
                label=str(item["label"]),
            )
            for item in _mapping_rows(raw, "setpoint_bands")
        ),
        capacity_factors=tuple(
            CapacityFactor(
                factor_key=str(item["factor_key"]),
                factor=float(item["factor"]),
                label=str(item["label"]),
            )
            for item in _mapping_rows(raw, "capacity_factors")
        ),
        weather_cases=tuple(
            WeatherSensitivityCase(
                weather_key=str(item["weather_key"]),
                label=str(item["label"]),
                analysis_supported=bool(item["analysis_supported"]),
                source_path=str(item.get("source_path", "")),
                source_revision=str(item.get("source_revision", "")),
            )
            for item in _mapping_rows(raw, "weather_cases")
        ),
        occupancy_schedules=tuple(
            OccupancyScheduleCase(
                schedule_key=str(item["schedule_key"]),
                label=str(item["label"]),
                start_hour=float(item["start_hour"]),
                end_hour=float(item["end_hour"]),
            )
            for item in _mapping_rows(raw, "occupancy_schedules")
        ),
    )
    _validate_study(study)
    return study


def build_small_office_v1_optimization_cases(
    baseline: BaselineParameterSnapshot,
    study: SmallOfficeV1Study,
    assignments: tuple[VariantDimensioningAssignment, ...],
    capacity_strategy: str = "dimensioned_with_factor",
) -> tuple[OptimizationCase, ...]:
    """Materialisiert nur Owner-berechnete, VVER-ausgewaehlte Auftraege."""
    if baseline.snapshot_id != study.baseline_snapshot_id:
        raise ValueError("Die V1-Studie referenziert nicht die angegebene Baseline.")
    heating_keys = _parameter_keys_with_suffix(baseline, ".heating_setpoint_c")
    cooling_keys = _parameter_keys_with_suffix(baseline, ".cooling_setpoint_c")
    if len(heating_keys) != 5 or len(cooling_keys) != 5:
        raise ValueError("Die SmallOffice-V1-Studie erwartet genau fuenf konditionierte Zonen.")

    assignment_by_id = {assignment.candidate_id: assignment for assignment in assignments}
    cases: list[OptimizationCase] = []
    for band in study.setpoint_bands:
        for factor in study.capacity_factors:
            case_id = f"OPT-{band.band_key}-{factor.factor_key}"
            assignment = assignment_by_id.get(case_id)
            if assignment is None:
                continue
            heating_capacity_w = assignment.heating_capacity_w
            cooling_capacity_w = assignment.cooling_capacity_w
            values = [
                *(VariationValue(key, band.heating_setpoint_c, "Grad C") for key in heating_keys),
                *(VariationValue(key, band.cooling_setpoint_c, "Grad C") for key in cooling_keys),
            ]
            if capacity_strategy != "ideal_unlimited":
                values.extend(
                    (
                        VariationValue(HEATING_CAPACITY_KEY, heating_capacity_w, "W"),
                        VariationValue(COOLING_CAPACITY_KEY, cooling_capacity_w, "W"),
                    )
                )
            variant = build_explicit_variant(
                baseline,
                variant_id=case_id,
                label=f"{band.label} | Heiz/Kuehl-Faktor {factor.factor:g}",
                values=tuple(values),
                capacity_strategy=capacity_strategy,
                dimensioning_status="available",
                reference_heating_capacity_w=assignment.heating_load_w,
                reference_cooling_capacity_w=assignment.cooling_load_w,
            )
            cases.append(
                OptimizationCase(
                    case_id=case_id,
                    band=band,
                    capacity_factor=factor,
                    variant=variant,
                    heating_capacity_w=heating_capacity_w,
                    cooling_capacity_w=cooling_capacity_w,
                )
            )
    return tuple(cases)


def build_small_office_v1_sensitivity_cases(
    baseline: BaselineParameterSnapshot,
    study: SmallOfficeV1Study,
    optimization_cases: tuple[OptimizationCase, ...],
) -> tuple[SensitivityCase, ...]:
    """Bereitet Wetter- und Belegungsfaelle gegen den festen Referenzfall vor."""
    reference = next(
        case
        for case in optimization_cases
        if case.band.band_key == study.reference_band_key
        and case.capacity_factor.factor_key == study.reference_factor_key
    )
    schedule_reference = next(
        schedule for schedule in study.occupancy_schedules if schedule.schedule_key == study.reference_schedule_key
    )
    cases: list[SensitivityCase] = []
    for weather in study.weather_cases:
        cases.append(
            SensitivityCase(
                case_id=f"SENS-WEATHER-{weather.weather_key}",
                sensitivity_type="weather",
                label=weather.label,
                parent_variant_id=reference.variant.variant_id,
                weather_key=weather.weather_key,
                schedule_key=schedule_reference.schedule_key,
                variant=reference.variant,
            )
        )

    start_keys = _parameter_keys_with_suffix(baseline, ".operation_start_hour")
    end_keys = _parameter_keys_with_suffix(baseline, ".operation_end_hour")
    if len(start_keys) != 5 or len(end_keys) != 5:
        raise ValueError("Die Belegungssensitivitaet erwartet Zeitparameter fuer alle fuenf Zonen.")
    reference_values = list(reference.variant.values)
    for schedule in study.occupancy_schedules:
        schedule_values = [
            *(VariationValue(key, schedule.start_hour, "h") for key in start_keys),
            *(VariationValue(key, schedule.end_hour, "h") for key in end_keys),
        ]
        variant = build_explicit_variant(
            baseline,
            variant_id=f"SENS-OCC-{schedule.schedule_key}",
            label=schedule.label,
            values=tuple((*reference_values, *schedule_values)),
        )
        cases.append(
            SensitivityCase(
                case_id=variant.variant_id,
                sensitivity_type="occupancy",
                label=schedule.label,
                parent_variant_id=reference.variant.variant_id,
                weather_key=study.reference_weather_key,
                schedule_key=schedule.schedule_key,
                variant=variant,
            )
        )
    return tuple(cases)


def optimization_case_rows(cases: tuple[OptimizationCase, ...]) -> list[dict[str, object]]:
    """Kompakte UI- und Berichtstabelle fuer die 30 Optimierungsfaelle."""
    return [
        {
            "Fall": case.case_id,
            "Heizen [Grad C]": case.band.heating_setpoint_c,
            "Kuehlen [Grad C]": case.band.cooling_setpoint_c,
            "Faktor Heizen/Kuehlen": case.capacity_factor.factor,
            "Heizleistung [W]": case.heating_capacity_w,
            "Kuehlleistung [W]": case.cooling_capacity_w,
        }
        for case in cases
    ]


def _parameter_keys_with_suffix(
    baseline: BaselineParameterSnapshot,
    suffix: str,
) -> tuple[str, ...]:
    return tuple(sorted(value.parameter_key for value in baseline.parameter_values if value.parameter_key.endswith(suffix)))


def _mapping_rows(raw: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = raw.get(key)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"SmallOffice-V1-Konfiguration benoetigt eine Liste '{key}'.")
    return value


def _validate_study(study: SmallOfficeV1Study) -> None:
    if len(study.setpoint_bands) != 5:
        raise ValueError("SmallOffice V1 benoetigt genau fuenf Sollwertbaender.")
    if len(study.capacity_factors) != 6:
        raise ValueError("SmallOffice V1 benoetigt genau sechs Kapazitaetsfaktoren.")
    if len({item.band_key for item in study.setpoint_bands}) != 5:
        raise ValueError("Sollwertband-Keys muessen eindeutig sein.")
    if len({item.factor_key for item in study.capacity_factors}) != 6:
        raise ValueError("Kapazitaetsfaktor-Keys muessen eindeutig sein.")
    if any(item.heating_setpoint_c >= item.cooling_setpoint_c for item in study.setpoint_bands):
        raise ValueError("Jedes Sollwertband benoetigt Heizen kleiner Kuehlen.")
    expected_bands = (
        ("SB01", 21.0, 24.0),
        ("SB02", 18.0, 24.0),
        ("SB03", 21.0, 27.0),
        ("SB04", 23.0, 26.0),
        ("SB05", 19.0, 26.0),
    )
    actual_bands = tuple(
        (item.band_key, item.heating_setpoint_c, item.cooling_setpoint_c)
        for item in study.setpoint_bands
    )
    if actual_bands != expected_bands:
        raise ValueError(
            "SmallOffice V1 braucht die freigegebenen Sollwertbaender "
            "21/24, 18/24, 21/27, 23/26 und 19/26."
        )
    if [item.factor for item in study.capacity_factors] != [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]:
        raise ValueError("Kapazitaetsfaktoren muessen von 1,0 bis 0,5 in 0,1-Schritten laufen.")
    if study.reference_band_key not in {item.band_key for item in study.setpoint_bands}:
        raise ValueError("Referenz-Sollwertband fehlt.")
    if study.reference_factor_key not in {item.factor_key for item in study.capacity_factors}:
        raise ValueError("Referenz-Kapazitaetsfaktor fehlt.")
    if len(study.weather_cases) != 4:
        raise ValueError("SmallOffice V1 benoetigt vier Frankfurt-Jahreswetterfaelle.")
    if len(study.occupancy_schedules) != 4:
        raise ValueError("SmallOffice V1 benoetigt vier Belegungszeitfaelle.")
    if any(not 0 <= item.start_hour < item.end_hour <= 24 for item in study.occupancy_schedules):
        raise ValueError("Belegungszeiten muessen innerhalb eines Tages liegen.")
