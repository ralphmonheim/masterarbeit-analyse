"""LoD-1-Referenzdimensionierung aus einem ParameterSnapshot."""

from __future__ import annotations

import math
from collections.abc import Mapping

from ma_parameters import ParameterSnapshot, build_business_integration_lod1_parameter_snapshot
from ma_validation import DiagnosticMessage, DiagnosticSeverity

from .models import DimensioningStatus, DimensioningStep, ReferenceDimensioningResult

AIR_HEAT_CAPACITY_WH_M3K = 0.34
DEFAULT_HEATING_OUTDOOR_TEMPERATURE_C = -10.0
DEFAULT_PERSON_SENSIBLE_GAIN_W = 75.0


def run_business_integration_lod1_reference_dimensioning() -> ReferenceDimensioningResult:
    """Fuehrt die LoD-1-Referenzdimensionierung fuer den BusinessIntegration-Snapshot aus."""
    return run_lod1_reference_dimensioning(build_business_integration_lod1_parameter_snapshot())


def run_lod1_reference_dimensioning(
    snapshot: ParameterSnapshot,
    *,
    heating_outdoor_temperature_c: float = DEFAULT_HEATING_OUTDOOR_TEMPERATURE_C,
    person_sensible_gain_w: float = DEFAULT_PERSON_SENSIBLE_GAIN_W,
) -> ReferenceDimensioningResult:
    """Berechnet transparente LoD-1-Startwerte aus einem ParameterSnapshot."""
    parameter_values = _parameter_values(snapshot)
    messages: list[DiagnosticMessage] = []

    length_m = _required_positive_number(parameter_values, "building_length_m", messages)
    width_m = _required_positive_number(parameter_values, "building_width_m", messages)
    height_m = _required_positive_number(parameter_values, "building_height_m", messages)
    wall_u_value = _required_positive_number(parameter_values, "external_wall_u_value_w_m2k", messages)
    window_u_value = _required_positive_number(parameter_values, "window_u_value_w_m2k", messages)
    window_ratio_percent = _required_number(parameter_values, "window_area_ratio_percent", messages)
    zone_floor_area_m2 = _required_positive_number(parameter_values, "zone_floor_area_m2", messages)
    zone_volume_m3 = _required_positive_number(parameter_values, "zone_volume_m3", messages)
    heating_setpoint_c = _required_number_by_suffix(parameter_values, ".heating_setpoint_c", messages)
    minimum_air_change_rate_1_h = _required_positive_number_by_suffix(
        parameter_values,
        ".minimum_air_change_rate_1_h",
        messages,
    )
    occupancy_density_m2_per_person = _required_positive_number_by_suffix(
        parameter_values,
        ".occupancy_density_m2_per_person",
        messages,
    )
    lighting_power_w_m2 = _required_number_by_suffix(parameter_values, ".lighting_power_w_m2", messages)
    equipment_power_w_m2 = _required_number_by_suffix(parameter_values, ".equipment_power_w_m2", messages)

    if window_ratio_percent is not None and not 0 <= window_ratio_percent <= 100:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "DIMENSIONING_WINDOW_RATIO_INVALID",
                "Der Fensterflaechenanteil muss im Bereich 0 bis 100 Prozent liegen.",
                "window_area_ratio_percent",
            )
        )
    if lighting_power_w_m2 is not None and lighting_power_w_m2 < 0:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "DIMENSIONING_LIGHTING_LOAD_INVALID",
                "Die Beleuchtungsleistung darf nicht negativ sein.",
                ".lighting_power_w_m2",
            )
        )
    if equipment_power_w_m2 is not None and equipment_power_w_m2 < 0:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "DIMENSIONING_EQUIPMENT_LOAD_INVALID",
                "Die Geraeteleistung darf nicht negativ sein.",
                ".equipment_power_w_m2",
            )
        )

    if _has_error(messages):
        return _not_evaluable_result(snapshot, tuple(messages))

    assert length_m is not None
    assert width_m is not None
    assert height_m is not None
    assert wall_u_value is not None
    assert window_u_value is not None
    assert window_ratio_percent is not None
    assert zone_floor_area_m2 is not None
    assert zone_volume_m3 is not None
    assert heating_setpoint_c is not None
    assert minimum_air_change_rate_1_h is not None
    assert occupancy_density_m2_per_person is not None
    assert lighting_power_w_m2 is not None
    assert equipment_power_w_m2 is not None

    delta_t_k = heating_setpoint_c - heating_outdoor_temperature_c
    if delta_t_k <= 0:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "DIMENSIONING_HEATING_DELTA_T_INVALID",
                "Die Auslegungs-Temperaturdifferenz muss groesser als 0 K sein.",
                "heating_outdoor_temperature_c",
            )
        )
        return _not_evaluable_result(snapshot, tuple(messages))

    gross_wall_area_m2 = 2.0 * (length_m + width_m) * height_m
    window_area_m2 = gross_wall_area_m2 * window_ratio_percent / 100.0
    opaque_wall_area_m2 = gross_wall_area_m2 - window_area_m2
    transmission_load_w = (opaque_wall_area_m2 * wall_u_value + window_area_m2 * window_u_value) * delta_t_k
    ventilation_load_w = AIR_HEAT_CAPACITY_WH_M3K * zone_volume_m3 * minimum_air_change_rate_1_h * delta_t_k
    heating_total_w = transmission_load_w + ventilation_load_w
    ventilation_volume_flow_m3_h = zone_volume_m3 * minimum_air_change_rate_1_h

    occupancy_people = zone_floor_area_m2 / occupancy_density_m2_per_person
    lighting_load_w = zone_floor_area_m2 * lighting_power_w_m2
    equipment_load_w = zone_floor_area_m2 * equipment_power_w_m2
    people_load_w = occupancy_people * person_sensible_gain_w
    cooling_internal_load_w = lighting_load_w + equipment_load_w + people_load_w

    steps = (
        _step(
            "gross_wall_area_m2",
            "Brutto-Aussenwandflaeche",
            gross_wall_area_m2,
            "m2",
            "2 * (Laenge + Breite) * Hoehe",
            ("building_length_m", "building_width_m", "building_height_m"),
        ),
        _step(
            "window_area_m2",
            "Fensterflaeche LoD-1",
            window_area_m2,
            "m2",
            "Brutto-Aussenwandflaeche * Fensteranteil",
            ("window_area_ratio_percent",),
        ),
        _step(
            "opaque_wall_area_m2",
            "Opake Aussenwandflaeche",
            opaque_wall_area_m2,
            "m2",
            "Brutto-Aussenwandflaeche - Fensterflaeche",
            ("window_area_ratio_percent",),
        ),
        _step(
            "heating_delta_t_k",
            "Auslegungs-Temperaturdifferenz",
            delta_t_k,
            "K",
            "Heiz-Sollwert - Aussentemperatur",
            (".heating_setpoint_c",),
            note=f"Aussentemperatur als LoD-1-Annahme: {heating_outdoor_temperature_c:g} Grad C.",
        ),
        _step(
            "heating_transmission_load_w",
            "Transmissions-Heizlast LoD-1",
            transmission_load_w,
            "W",
            "(A_opak * U_Wand + A_Fenster * U_Fenster) * DeltaT",
            ("external_wall_u_value_w_m2k", "window_u_value_w_m2k", "window_area_ratio_percent"),
        ),
        _step(
            "heating_ventilation_load_w",
            "Lueftungs-Heizlast LoD-1",
            ventilation_load_w,
            "W",
            "0.34 * Volumen * Luftwechsel * DeltaT",
            ("zone_volume_m3", ".minimum_air_change_rate_1_h", ".heating_setpoint_c"),
            note="0.34 Wh/(m3K) ist die uebliche Luft-Waermekapazitaetsnaeherung.",
        ),
        _step(
            "heating_total_load_w",
            "Heizlast gesamt LoD-1",
            heating_total_w,
            "W",
            "Transmissions-Heizlast + Lueftungs-Heizlast",
            ("heating_transmission_load_w", "heating_ventilation_load_w"),
        ),
        _step(
            "ventilation_volume_flow_m3_h",
            "Mindest-Luftvolumenstrom",
            ventilation_volume_flow_m3_h,
            "m3/h",
            "Zonenvolumen * Mindestluftwechsel",
            ("zone_volume_m3", ".minimum_air_change_rate_1_h"),
        ),
        _step(
            "cooling_internal_load_w",
            "Interne Kuehllastannahme LoD-1",
            cooling_internal_load_w,
            "W",
            "Flaeche * (Beleuchtung + Geraete) + Personen * sensible Personenlast",
            (
                "zone_floor_area_m2",
                ".lighting_power_w_m2",
                ".equipment_power_w_m2",
                ".occupancy_density_m2_per_person",
            ),
            note=f"Sensible Personenlast als LoD-1-Annahme: {person_sensible_gain_w:g} W/Person.",
        ),
    )
    messages.extend(_quality_messages())
    messages.extend(_technical_capacity_messages(parameter_values, heating_total_w, cooling_internal_load_w))
    return ReferenceDimensioningResult(
        result_id=f"DIM-{snapshot.snapshot_id}",
        source_snapshot_id=snapshot.snapshot_id,
        source_snapshot_version=snapshot.snapshot_version,
        status=DimensioningStatus.EVALUATED,
        heating_transmission_load_w=round(transmission_load_w, 2),
        heating_ventilation_load_w=round(ventilation_load_w, 2),
        heating_total_load_w=round(heating_total_w, 2),
        cooling_internal_load_w=round(cooling_internal_load_w, 2),
        ventilation_volume_flow_m3_h=round(ventilation_volume_flow_m3_h, 2),
        steps=tuple(_round_step(step) for step in steps),
        messages=tuple(messages),
    )


def dimensioning_summary_rows(result: ReferenceDimensioningResult) -> list[dict[str, object]]:
    """Bereitet zentrale Ergebniswerte fuer die UI auf."""
    return [
        {"Kennwert": "Status", "Wert": result.status.value, "Einheit": ""},
        {"Kennwert": "Quell-Snapshot", "Wert": result.source_snapshot_id, "Einheit": ""},
        {"Kennwert": "Snapshot-Version", "Wert": result.source_snapshot_version, "Einheit": ""},
        {"Kennwert": "Transmissions-Heizlast", "Wert": result.heating_transmission_load_w, "Einheit": "W"},
        {"Kennwert": "Lueftungs-Heizlast", "Wert": result.heating_ventilation_load_w, "Einheit": "W"},
        {"Kennwert": "Heizlast gesamt", "Wert": result.heating_total_load_w, "Einheit": "W"},
        {"Kennwert": "Interne Kuehllastannahme", "Wert": result.cooling_internal_load_w, "Einheit": "W"},
        {"Kennwert": "Mindest-Luftvolumenstrom", "Wert": result.ventilation_volume_flow_m3_h, "Einheit": "m3/h"},
    ]


def dimensioning_step_rows(result: ReferenceDimensioningResult) -> list[dict[str, object]]:
    """Bereitet Rechenschritte fuer UI-Tabellen und Tests auf."""
    return [
        {
            "Schritt": step.step_key,
            "Bezeichnung": step.label,
            "Wert": step.value,
            "Einheit": step.unit,
            "Formel": step.formula,
            "Quellen": ", ".join(step.source_parameter_keys),
            "Hinweis": step.note,
        }
        for step in result.steps
    ]


def dimensioning_message_rows(result: ReferenceDimensioningResult) -> list[dict[str, object]]:
    """Bereitet Diagnosemeldungen fuer UI-Tabellen und Tests auf."""
    return [
        {
            "Schwere": message.severity.value,
            "Code": message.code,
            "Meldung": message.message,
            "Fundstelle": message.location,
        }
        for message in result.messages
    ]


def _parameter_values(snapshot: ParameterSnapshot) -> dict[str, object]:
    return {value.parameter_key: value.value for value in snapshot.values}


def _required_number(
    values: Mapping[str, object],
    parameter_key: str,
    messages: list[DiagnosticMessage],
) -> float | None:
    if parameter_key not in values:
        messages.append(_missing_parameter_message(parameter_key))
        return None
    return _as_finite_number(values[parameter_key], parameter_key, messages)


def _required_positive_number(
    values: Mapping[str, object],
    parameter_key: str,
    messages: list[DiagnosticMessage],
) -> float | None:
    value = _required_number(values, parameter_key, messages)
    if value is not None and value <= 0:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "DIMENSIONING_PARAMETER_NOT_POSITIVE",
                "Dieser Dimensionierungsparameter muss groesser als 0 sein.",
                parameter_key,
            )
        )
    return value


def _required_number_by_suffix(
    values: Mapping[str, object],
    suffix: str,
    messages: list[DiagnosticMessage],
) -> float | None:
    key = _unique_key_by_suffix(values, suffix, messages)
    if key is None:
        return None
    return _as_finite_number(values[key], key, messages)


def _required_positive_number_by_suffix(
    values: Mapping[str, object],
    suffix: str,
    messages: list[DiagnosticMessage],
) -> float | None:
    key = _unique_key_by_suffix(values, suffix, messages)
    if key is None:
        return None
    value = _as_finite_number(values[key], key, messages)
    if value is not None and value <= 0:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "DIMENSIONING_PARAMETER_NOT_POSITIVE",
                "Dieser Dimensionierungsparameter muss groesser als 0 sein.",
                key,
            )
        )
    return value


def _unique_key_by_suffix(
    values: Mapping[str, object],
    suffix: str,
    messages: list[DiagnosticMessage],
) -> str | None:
    matches = [key for key in values if key.endswith(suffix)]
    if not matches:
        messages.append(_missing_parameter_message(suffix))
        return None
    if len(matches) > 1:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "DIMENSIONING_PARAMETER_AMBIGUOUS",
                f"Parameter-Suffix ist nicht eindeutig: {suffix}",
                suffix,
            )
        )
        return None
    return matches[0]


def _as_finite_number(
    value: object,
    parameter_key: str,
    messages: list[DiagnosticMessage],
) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "DIMENSIONING_PARAMETER_NOT_NUMERIC",
                "Dieser Dimensionierungsparameter muss numerisch sein.",
                parameter_key,
            )
        )
        return None
    if not math.isfinite(number):
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "DIMENSIONING_PARAMETER_NOT_FINITE",
                "Dieser Dimensionierungsparameter muss endlich sein.",
                parameter_key,
            )
        )
        return None
    return number


def _technical_capacity_messages(
    values: Mapping[str, object],
    heating_total_w: float,
    cooling_internal_load_w: float,
) -> tuple[DiagnosticMessage, ...]:
    messages: list[DiagnosticMessage] = []
    heating_capacity = _optional_number_by_marker(values, "TECH-HEATING", ".estimated_design_power_w")
    cooling_capacity = _optional_number_by_marker(values, "TECH-COOLING", ".estimated_design_power_w")
    if heating_capacity is not None and heating_capacity < heating_total_w:
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "DIMENSIONING_HEATING_TECH_POWER_LOW",
                "Die einfache Heizsystemannahme liegt unter der berechneten LoD-1-Heizlast.",
                "TECH-HEATING.estimated_design_power_w",
            )
        )
    if cooling_capacity is not None and cooling_capacity < cooling_internal_load_w:
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "DIMENSIONING_COOLING_TECH_POWER_LOW",
                "Die einfache Kuehlsystemannahme liegt unter der internen LoD-1-Kuehllastannahme.",
                "TECH-COOLING.estimated_design_power_w",
            )
        )
    return tuple(messages)


def _optional_number_by_marker(
    values: Mapping[str, object],
    marker: str,
    suffix: str,
) -> float | None:
    matches = [value for key, value in values.items() if marker in key and key.endswith(suffix)]
    if len(matches) != 1:
        return None
    try:
        number = float(matches[0])
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _quality_messages() -> tuple[DiagnosticMessage, ...]:
    return (
        _message(
            DiagnosticSeverity.WARNING,
            "DIMENSIONING_LOD1_METHOD_LIMITED",
            "Die Dimensionierung ist eine LoD-1-Naeherung und ersetzt kein normatives Heiz-/Kuehllastverfahren.",
            "ma_analyse.stage_1_dimensioning",
        ),
        _message(
            DiagnosticSeverity.WARNING,
            "DIMENSIONING_COOLING_SOLAR_NOT_INCLUDED",
            "Die Kuehllastannahme enthaelt interne Lasten, aber noch keine solaren Gewinne oder dynamische Bilanz.",
            "cooling_internal_load_w",
        ),
    )


def _not_evaluable_result(
    snapshot: ParameterSnapshot,
    messages: tuple[DiagnosticMessage, ...],
) -> ReferenceDimensioningResult:
    return ReferenceDimensioningResult(
        result_id=f"DIM-{snapshot.snapshot_id}",
        source_snapshot_id=snapshot.snapshot_id,
        source_snapshot_version=snapshot.snapshot_version,
        status=DimensioningStatus.NOT_EVALUABLE,
        heating_transmission_load_w=None,
        heating_ventilation_load_w=None,
        heating_total_load_w=None,
        cooling_internal_load_w=None,
        ventilation_volume_flow_m3_h=None,
        steps=(),
        messages=messages,
    )


def _has_error(messages: list[DiagnosticMessage]) -> bool:
    return any(message.severity is DiagnosticSeverity.ERROR for message in messages)


def _missing_parameter_message(parameter_key: str) -> DiagnosticMessage:
    return _message(
        DiagnosticSeverity.ERROR,
        "DIMENSIONING_PARAMETER_MISSING",
        "Erforderlicher Parameter fehlt im ParameterSnapshot.",
        parameter_key,
    )


def _message(
    severity: DiagnosticSeverity,
    code: str,
    message: str,
    location: str,
) -> DiagnosticMessage:
    return DiagnosticMessage(severity=severity, code=code, message=message, location=location)


def _step(
    step_key: str,
    label: str,
    value: float,
    unit: str,
    formula: str,
    source_parameter_keys: tuple[str, ...],
    *,
    note: str = "",
) -> DimensioningStep:
    return DimensioningStep(
        step_key=step_key,
        label=label,
        value=value,
        unit=unit,
        formula=formula,
        source_parameter_keys=source_parameter_keys,
        note=note,
    )


def _round_step(step: DimensioningStep) -> DimensioningStep:
    return DimensioningStep(
        step_key=step.step_key,
        label=step.label,
        value=round(step.value, 2),
        unit=step.unit,
        formula=step.formula,
        source_parameter_keys=step.source_parameter_keys,
        note=step.note,
    )
