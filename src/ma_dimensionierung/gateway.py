"""Pruefbarer Eingangskontrakt fuer die LoD-1-Referenzdimensionierung.

Der Gateway ist bewusst additiv: Er sichert den fachlichen Eingang ab und
delegiert danach an die noch historische Berechnung. Die Ergebnisarten werden
erst in einem folgenden P016-Slice in eigene Owner-Modelle ueberfuehrt.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Final

from ma_analyse.stage_1_dimensioning import (
    DEFAULT_HEATING_OUTDOOR_TEMPERATURE_C,
    DEFAULT_PERSON_SENSIBLE_GAIN_W,
    ReferenceDimensioningResult,
    run_lod1_reference_dimensioning,
)
from ma_parameters import ParameterSnapshot, validate_parameter_snapshot
from ma_validation import DiagnosticMessage, DiagnosticSeverity, ValidationResult, build_validation_result

LOD1_REFERENCE_METHOD_ID: Final = "lod1_reference_dimensioning"
LOD1_REFERENCE_METHOD_VERSION: Final = "1.0"
LOD1_GATEWAY_CONTRACT_VERSION: Final = "1.0"
LOD1_RESULT_ROUNDING_RULE: Final = "python_round_float_to_2_decimals_after_calculation"

_GLOBAL_EXPECTED_UNITS: Final = {
    "building_length_m": "m",
    "building_width_m": "m",
    "building_height_m": "m",
    "external_wall_u_value_w_m2k": "W/m2K",
    "window_u_value_w_m2k": "W/m2K",
    "window_area_ratio_percent": "%",
    "zone_floor_area_m2": "m2",
    "zone_volume_m3": "m3",
    "external_wall_area_m2": "m2",
    "window_area_m2": "m2",
}
_ZONE_SUFFIX_EXPECTED_UNITS: Final = {
    ".floor_area_m2": "m2",
    ".volume_m3": "m3",
    ".heating_setpoint_c": "Grad C",
    ".minimum_air_change_rate_1_h": "1/h",
    ".occupancy_density_m2_per_person": "m2/Person",
    ".lighting_power_w_m2": "W/m2",
    ".equipment_power_w_m2": "W/m2",
}


@dataclass(frozen=True, slots=True)
class DimensioningAssumption:
    """Eine stabile, fachlich erklaerte Annahme der LoD-1-Methode."""

    assumption_id: str
    value: float
    unit: str
    source: str
    meaning: str


@dataclass(frozen=True, slots=True)
class Lod1DimensioningRequest:
    """Validierter und reproduzierbar beschriebener Berechnungsauftrag."""

    snapshot: ParameterSnapshot
    method_id: str
    method_version: str
    contract_version: str
    assumptions: tuple[DimensioningAssumption, ...]
    rounding_rule: str
    input_fingerprint: str

    def __post_init__(self) -> None:
        if self.method_id != LOD1_REFERENCE_METHOD_ID or self.method_version != LOD1_REFERENCE_METHOD_VERSION:
            raise ValueError("Der Gateway akzeptiert nur die aktuelle LoD-1-Referenzmethode.")
        if self.contract_version != LOD1_GATEWAY_CONTRACT_VERSION:
            raise ValueError("Der Gateway-Vertrag besitzt eine unpassende Version.")
        if self.rounding_rule != LOD1_RESULT_ROUNDING_RULE:
            raise ValueError("Der Gateway-Vertrag besitzt eine unpassende Rundungsregel.")
        if {assumption.assumption_id for assumption in self.assumptions} != {
            "air_heat_capacity_wh_m3k",
            "heating_outdoor_temperature_c",
            "person_sensible_gain_w",
        }:
            raise ValueError("Der LoD-1-Auftrag benoetigt genau die dokumentierten Annahmen.")


@dataclass(frozen=True, slots=True)
class Lod1GatewayPreparation:
    """Ergebnis der Eingangspruefung vor einer LoD-1-Berechnung."""

    validation: ValidationResult
    request: Lod1DimensioningRequest | None


@dataclass(frozen=True, slots=True)
class Lod1GatewayExecution:
    """Unveraendertes Legacy-Ergebnis mit nachvollziehbarer Gateway-Provenienz."""

    request: Lod1DimensioningRequest
    result: ReferenceDimensioningResult
    result_fingerprint: str


def prepare_lod1_reference_dimensioning_request(
    snapshot: ParameterSnapshot,
    *,
    heating_outdoor_temperature_c: float = DEFAULT_HEATING_OUTDOOR_TEMPERATURE_C,
    person_sensible_gain_w: float = DEFAULT_PERSON_SENSIBLE_GAIN_W,
) -> Lod1GatewayPreparation:
    """Prueft Snapshot und Einheiten und baut nur dann einen Rechenauftrag."""
    messages = list(validate_parameter_snapshot(snapshot).messages)
    messages.extend(_unit_messages(snapshot))
    messages.extend(_assumption_messages(heating_outdoor_temperature_c, person_sensible_gain_w))
    validation = build_validation_result(tuple(messages))
    if validation.errors:
        return Lod1GatewayPreparation(validation=validation, request=None)

    assumptions = _assumptions(
        heating_outdoor_temperature_c=heating_outdoor_temperature_c,
        person_sensible_gain_w=person_sensible_gain_w,
    )
    request = Lod1DimensioningRequest(
        snapshot=snapshot,
        method_id=LOD1_REFERENCE_METHOD_ID,
        method_version=LOD1_REFERENCE_METHOD_VERSION,
        contract_version=LOD1_GATEWAY_CONTRACT_VERSION,
        assumptions=assumptions,
        rounding_rule=LOD1_RESULT_ROUNDING_RULE,
        input_fingerprint=_input_fingerprint(snapshot, assumptions),
    )
    return Lod1GatewayPreparation(validation=validation, request=request)


def execute_lod1_reference_dimensioning(request: Lod1DimensioningRequest) -> Lod1GatewayExecution:
    """Delegiert einen bereits validierten Auftrag an die historische Methode."""
    assumptions = {assumption.assumption_id: assumption.value for assumption in request.assumptions}
    preparation = prepare_lod1_reference_dimensioning_request(
        request.snapshot,
        heating_outdoor_temperature_c=assumptions["heating_outdoor_temperature_c"],
        person_sensible_gain_w=assumptions["person_sensible_gain_w"],
    )
    if preparation.request != request:
        raise ValueError("Der LoD-1-Auftrag ist nicht mehr gueltig oder unveraendert.")
    result = run_lod1_reference_dimensioning(
        request.snapshot,
        heating_outdoor_temperature_c=assumptions["heating_outdoor_temperature_c"],
        person_sensible_gain_w=assumptions["person_sensible_gain_w"],
    )
    return Lod1GatewayExecution(
        request=request,
        result=result,
        result_fingerprint=_result_fingerprint(request, result),
    )


def _assumptions(*, heating_outdoor_temperature_c: float, person_sensible_gain_w: float) -> tuple[DimensioningAssumption, ...]:
    return (
        DimensioningAssumption("air_heat_capacity_wh_m3k", 0.34, "Wh/(m3K)", "method_constant", "Luft-Waermekapazitaetsnaeherung"),
        DimensioningAssumption("heating_outdoor_temperature_c", heating_outdoor_temperature_c, "Grad C", "method_default" if heating_outdoor_temperature_c == DEFAULT_HEATING_OUTDOOR_TEMPERATURE_C else "caller_value", "Heiz-Auslegungs-Aussentemperatur"),
        DimensioningAssumption("person_sensible_gain_w", person_sensible_gain_w, "W/Person", "method_default" if person_sensible_gain_w == DEFAULT_PERSON_SENSIBLE_GAIN_W else "caller_value", "Sensible Personenlast"),
    )


def _unit_messages(snapshot: ParameterSnapshot) -> tuple[DiagnosticMessage, ...]:
    messages: list[DiagnosticMessage] = []
    for value in snapshot.values:
        expected_unit = _expected_unit(value.parameter_key)
        if expected_unit is not None and value.unit != expected_unit:
            messages.append(
                DiagnosticMessage(
                    severity=DiagnosticSeverity.ERROR,
                    code="DIMENSIONING_INPUT_UNIT_INVALID",
                    message=f"Fuer diesen LoD-1-Parameter wird die Einheit '{expected_unit}' erwartet.",
                    location=value.parameter_key,
                )
            )
    return tuple(messages)


def _assumption_messages(
    heating_outdoor_temperature_c: float,
    person_sensible_gain_w: float,
) -> tuple[DiagnosticMessage, ...]:
    messages: list[DiagnosticMessage] = []
    for assumption_key, value in (
        ("heating_outdoor_temperature_c", heating_outdoor_temperature_c),
        ("person_sensible_gain_w", person_sensible_gain_w),
    ):
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            messages.append(
                DiagnosticMessage(
                    severity=DiagnosticSeverity.ERROR,
                    code="DIMENSIONING_ASSUMPTION_NOT_FINITE",
                    message="LoD-1-Annahmen muessen endliche Zahlen sein.",
                    location=assumption_key,
                )
            )
    return tuple(messages)


def _expected_unit(parameter_key: str) -> str | None:
    if parameter_key in _GLOBAL_EXPECTED_UNITS:
        return _GLOBAL_EXPECTED_UNITS[parameter_key]
    return next((unit for suffix, unit in _ZONE_SUFFIX_EXPECTED_UNITS.items() if parameter_key.endswith(suffix)), None)


def _input_fingerprint(snapshot: ParameterSnapshot, assumptions: tuple[DimensioningAssumption, ...]) -> str:
    values = sorted(
        (
            {"parameter_key": value.parameter_key, "value": value.value, "unit": value.unit}
            for value in snapshot.values
            if _expected_unit(value.parameter_key) is not None
        ),
        key=lambda row: str(row["parameter_key"]),
    )
    return _fingerprint(
        {
            "contract_version": LOD1_GATEWAY_CONTRACT_VERSION,
            "method_id": LOD1_REFERENCE_METHOD_ID,
            "method_version": LOD1_REFERENCE_METHOD_VERSION,
            "rounding_rule": LOD1_RESULT_ROUNDING_RULE,
            "values": values,
            "assumptions": [asdict(assumption) for assumption in assumptions],
        }
    )


def _result_fingerprint(request: Lod1DimensioningRequest, result: ReferenceDimensioningResult) -> str:
    return _fingerprint(
        {
            "result_kind": "calculated_lod1_reference",
            "method_id": request.method_id,
            "method_version": request.method_version,
            "input_fingerprint": request.input_fingerprint,
            "status": result.status.value,
            "heating_transmission_load_w": result.heating_transmission_load_w,
            "heating_ventilation_load_w": result.heating_ventilation_load_w,
            "heating_total_load_w": result.heating_total_load_w,
            "cooling_internal_load_w": result.cooling_internal_load_w,
            "ventilation_volume_flow_m3_h": result.ventilation_volume_flow_m3_h,
        }
    )


def _fingerprint(payload: object) -> str:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
