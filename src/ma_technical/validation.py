"""Fachliche Validierung fuer ma_technical."""

from __future__ import annotations

from collections import defaultdict

from ma_validation import DiagnosticMessage, DiagnosticSeverity, ValidationResult, build_validation_result
from ma_zones import ZoneModelSpecification

from .models import VALID_SYSTEM_TYPES, TechnicalInputDetailLevel, TechnicalSystemSpecification


def validate_technical_spec(
    spec: TechnicalSystemSpecification,
    *,
    zone_spec: ZoneModelSpecification | None = None,
) -> ValidationResult:
    """Prueft eine Technikspezifikation und optional ihren Zonenbezug."""
    messages: list[DiagnosticMessage] = []
    messages.extend(_validate_header(spec))
    messages.extend(_validate_object_ids(spec))
    messages.extend(_validate_systems(spec))
    if zone_spec is not None:
        messages.extend(_validate_zone_reference(spec, zone_spec))
    return build_validation_result(tuple(messages))


def _message(
    severity: DiagnosticSeverity,
    code: str,
    message: str,
    location: str,
) -> DiagnosticMessage:
    return DiagnosticMessage(severity=severity, code=code, message=message, location=location)


def _validate_header(spec: TechnicalSystemSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    required_values = {
        "schema_version": spec.schema_version,
        "technical_model_id": spec.technical_model_id,
        "project_id": spec.project_id,
        "building_id": spec.building_id,
        "source_zone_model_id": spec.source_zone_model_id,
        "input_detail_level": spec.input_detail_level,
    }
    for location, value in required_values.items():
        if not str(value).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_REQUIRED_FIELD_MISSING",
                    "Pflichtfeld der TechnicalSystemSpecification fehlt.",
                    location,
                )
            )

    if spec.input_detail_level and not isinstance(spec.input_detail_level, TechnicalInputDetailLevel):
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "TECHNICAL_INPUT_DETAIL_LEVEL_INVALID",
                f"Unbekannter Technik-Eingabeumfang: {spec.input_detail_level}",
                "input_detail_level",
            )
        )
    return messages


def _validate_object_ids(spec: TechnicalSystemSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    locations_by_id: dict[str, list[str]] = defaultdict(list)
    for object_id, location in spec.object_id_locations():
        if not object_id:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_OBJECT_ID_MISSING",
                    "Eine Objekt-ID ist leer.",
                    location,
                )
            )
            continue
        locations_by_id[object_id].append(location)

    for object_id, locations in locations_by_id.items():
        if len(locations) > 1:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_OBJECT_ID_DUPLICATE",
                    f"Objekt-ID ist mehrfach vergeben: {object_id}",
                    ", ".join(locations),
                )
            )
    return messages


def _validate_systems(spec: TechnicalSystemSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not spec.systems:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "TECHNICAL_SYSTEMS_MISSING",
                "Mindestens ein technisches System ist erforderlich.",
                "systems",
            )
        )
        return messages

    system_types = {system.system_type for system in spec.systems}
    if "heating" not in system_types:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "TECHNICAL_HEATING_SYSTEM_MISSING",
                "LoD-1 benoetigt mindestens eine einfache Heizungsannahme.",
                "systems",
            )
        )
    if "ventilation" not in system_types:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "TECHNICAL_VENTILATION_SYSTEM_MISSING",
                "LoD-1 benoetigt mindestens eine einfache Lueftungsannahme.",
                "systems",
            )
        )

    for index, system in enumerate(spec.systems):
        location = f"systems.{index}"
        if system.system_type not in VALID_SYSTEM_TYPES:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_SYSTEM_TYPE_INVALID",
                    f"Unbekannter Systemtyp: {system.system_type}",
                    f"{location}.system_type",
                )
            )
        if not system.name:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_SYSTEM_NAME_MISSING",
                    "Technische Systeme benoetigen einen Namen.",
                    f"{location}.name",
                )
            )
        if not system.served_zone_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_SERVED_ZONES_MISSING",
                    "Technische Systeme benoetigen mindestens eine bediente Zone.",
                    f"{location}.served_zone_ids",
                )
            )
        if system.system_type in {"heating", "cooling"} and (
            system.design_power_w_m2 is None or system.design_power_w_m2 <= 0
        ):
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_DESIGN_POWER_INVALID",
                    "Heiz- und Kuehlsysteme benoetigen eine positive spezifische Leistung.",
                    f"{location}.design_power_w_m2",
                )
            )
        if system.system_type == "ventilation" and (
            system.air_change_rate_1_h is None or system.air_change_rate_1_h <= 0
        ):
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_AIR_CHANGE_RATE_INVALID",
                    "Lueftungssysteme benoetigen einen positiven Luftwechsel.",
                    f"{location}.air_change_rate_1_h",
                )
            )
        if system.performance_factor is not None and system.performance_factor <= 0:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_PERFORMANCE_FACTOR_INVALID",
                    "Leistungszahlen oder Wirkungsgrade muessen groesser als 0 sein.",
                    f"{location}.performance_factor",
                )
            )
        if system.heat_recovery_efficiency_percent is not None and not 0 <= system.heat_recovery_efficiency_percent <= 100:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_HEAT_RECOVERY_INVALID",
                    "Waermerueckgewinnung muss im Bereich 0 bis 100 Prozent liegen.",
                    f"{location}.heat_recovery_efficiency_percent",
                )
            )
        if not system.control_strategy:
            messages.append(
                _message(
                    DiagnosticSeverity.WARNING,
                    "TECHNICAL_CONTROL_STRATEGY_MISSING",
                    "Die Regelstrategie fehlt und muss vor einer belastbaren Simulation bestaetigt werden.",
                    f"{location}.control_strategy",
                )
            )
    return messages


def _validate_zone_reference(
    spec: TechnicalSystemSpecification,
    zone_spec: ZoneModelSpecification,
) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if spec.project_id != zone_spec.project_id:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "TECHNICAL_PROJECT_REFERENCE_MISMATCH",
                "Technik- und Zonenmodell verwenden unterschiedliche Projekt-IDs.",
                "project_id",
            )
        )
    if spec.building_id != zone_spec.building_id:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "TECHNICAL_BUILDING_REFERENCE_MISMATCH",
                "Technikmodell verweist nicht auf das Zonen-Gebaeude.",
                "building_id",
            )
        )
    if spec.source_zone_model_id != zone_spec.zone_model_id:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "TECHNICAL_ZONE_MODEL_REFERENCE_MISMATCH",
                "Technikmodell verweist nicht auf die geladene Zonenmodellversion.",
                "source_zone_model_id",
            )
        )

    known_zone_ids = zone_spec.zone_ids
    for index, system in enumerate(spec.systems):
        unknown_zone_ids = sorted(set(system.served_zone_ids) - known_zone_ids)
        if unknown_zone_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "TECHNICAL_SERVED_ZONE_UNKNOWN",
                    f"Technisches System verweist auf unbekannte Zonen: {', '.join(unknown_zone_ids)}",
                    f"systems.{index}.served_zone_ids",
                )
            )
    return messages
