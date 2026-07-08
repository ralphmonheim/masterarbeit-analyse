"""Fachliche Validierung fuer ma_zones."""

from __future__ import annotations

from collections import defaultdict

from ma_building import BuildingModelSpecification
from ma_validation import DiagnosticMessage, DiagnosticSeverity, ValidationResult, build_validation_result

from .models import ZoneInputDetailLevel, ZoneModelSpecification


def validate_zone_spec(
    spec: ZoneModelSpecification,
    *,
    building_spec: BuildingModelSpecification | None = None,
) -> ValidationResult:
    """Prueft eine Zonenspezifikation und optional ihren Gebaeudebezug."""
    messages: list[DiagnosticMessage] = []
    messages.extend(_validate_header(spec))
    messages.extend(_validate_object_ids(spec))
    messages.extend(_validate_usage_profiles(spec))
    messages.extend(_validate_zones(spec))
    if building_spec is not None:
        messages.extend(_validate_building_reference(spec, building_spec))
    return build_validation_result(tuple(messages))


def _message(
    severity: DiagnosticSeverity,
    code: str,
    message: str,
    location: str,
) -> DiagnosticMessage:
    return DiagnosticMessage(severity=severity, code=code, message=message, location=location)


def _validate_header(spec: ZoneModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    required_values = {
        "schema_version": spec.schema_version,
        "zone_model_id": spec.zone_model_id,
        "project_id": spec.project_id,
        "building_id": spec.building_id,
        "source_building_version_id": spec.source_building_version_id,
        "input_detail_level": spec.input_detail_level,
    }
    for location, value in required_values.items():
        if not str(value).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_REQUIRED_FIELD_MISSING",
                    "Pflichtfeld der ZoneModelSpecification fehlt.",
                    location,
                )
            )

    if spec.input_detail_level and not isinstance(spec.input_detail_level, ZoneInputDetailLevel):
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_INPUT_DETAIL_LEVEL_INVALID",
                f"Unbekannter Zonen-Eingabeumfang: {spec.input_detail_level}",
                "input_detail_level",
            )
        )
    return messages


def _validate_object_ids(spec: ZoneModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    locations_by_id: dict[str, list[str]] = defaultdict(list)
    for object_id, location in spec.object_id_locations():
        if not object_id:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_OBJECT_ID_MISSING",
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
                    "ZONE_OBJECT_ID_DUPLICATE",
                    f"Objekt-ID ist mehrfach vergeben: {object_id}",
                    ", ".join(locations),
                )
            )
    return messages


def _validate_usage_profiles(spec: ZoneModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not spec.usage_profiles:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_USAGE_PROFILES_MISSING",
                "Mindestens ein Nutzungsprofil ist erforderlich.",
                "usage_profiles",
            )
        )
    for index, profile in enumerate(spec.usage_profiles):
        if not profile.name:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_USAGE_PROFILE_NAME_MISSING",
                    "Nutzungsprofile benoetigen einen Namen.",
                    f"usage_profiles.{index}.name",
                )
            )
        if not 0 <= profile.operation_start_hour < 24:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_OPERATION_START_INVALID",
                    "Der Betriebsbeginn muss im Bereich 0 <= Stunde < 24 liegen.",
                    f"usage_profiles.{index}.operation_start_hour",
                )
            )
        if not 0 < profile.operation_end_hour <= 24 or profile.operation_end_hour <= profile.operation_start_hour:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_OPERATION_END_INVALID",
                    "Das Betriebsende muss nach dem Betriebsbeginn und maximal bei Stunde 24 liegen.",
                    f"usage_profiles.{index}.operation_end_hour",
                )
            )
        if not 1 <= profile.operation_days_per_week <= 7:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_OPERATION_DAYS_INVALID",
                    "Betriebstage muessen im Bereich 1 bis 7 liegen.",
                    f"usage_profiles.{index}.operation_days_per_week",
                )
            )
        if profile.occupancy_density_m2_per_person <= 0:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_OCCUPANCY_DENSITY_INVALID",
                    "Die Belegungsdichte muss groesser als 0 m2/Person sein.",
                    f"usage_profiles.{index}.occupancy_density_m2_per_person",
                )
            )
        if min(profile.lighting_power_w_m2, profile.equipment_power_w_m2) < 0:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_INTERNAL_LOAD_INVALID",
                    "Interne Lasten duerfen nicht negativ sein.",
                    f"usage_profiles.{index}",
                )
            )
    return messages


def _validate_zones(spec: ZoneModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not spec.zones:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_ZONES_MISSING",
                "Mindestens eine thermische Zone ist erforderlich.",
                "zones",
            )
        )
        return messages
    if spec.input_detail_level is ZoneInputDetailLevel.LOD_1 and len(spec.zones) > 1:
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "ZONE_LOD1_MULTIPLE_ZONES",
                "LoD-1 ist als einfache Gesamtgebaeudezone vorgesehen; mehrere Zonen benoetigen eine bewusste Freigabe.",
                "zones",
            )
        )

    for index, zone in enumerate(spec.zones):
        if zone.usage_profile_id not in spec.usage_profile_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_USAGE_PROFILE_UNKNOWN",
                    f"Zone verweist auf unbekanntes Nutzungsprofil: {zone.usage_profile_id}",
                    f"zones.{index}.usage_profile_id",
                )
            )
        if min(zone.floor_area_m2, zone.volume_m3) <= 0:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_GEOMETRY_INVALID",
                    "Zonenflaeche und Zonenvolumen muessen groesser als 0 sein.",
                    f"zones.{index}",
                )
            )
        if not 5 <= zone.heating_setpoint_c <= 30:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_HEATING_SETPOINT_INVALID",
                    "Heiz-Sollwerte muessen im Bereich 5 bis 30 Grad C liegen.",
                    f"zones.{index}.heating_setpoint_c",
                )
            )
        if not 15 <= zone.cooling_setpoint_c <= 40:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_COOLING_SETPOINT_INVALID",
                    "Kuehl-Sollwerte muessen im Bereich 15 bis 40 Grad C liegen.",
                    f"zones.{index}.cooling_setpoint_c",
                )
            )
        if zone.heating_setpoint_c >= zone.cooling_setpoint_c:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_SETPOINT_ORDER_INVALID",
                    "Der Heiz-Sollwert muss unter dem Kuehl-Sollwert liegen.",
                    f"zones.{index}",
                )
            )
        if zone.minimum_air_change_rate_1_h < 0:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_AIR_CHANGE_RATE_INVALID",
                    "Der Mindestluftwechsel darf nicht negativ sein.",
                    f"zones.{index}.minimum_air_change_rate_1_h",
                )
            )
    return messages


def _validate_building_reference(
    spec: ZoneModelSpecification,
    building_spec: BuildingModelSpecification,
) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if spec.project_id != building_spec.project.project_id:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_PROJECT_REFERENCE_MISMATCH",
                "Zonenmodell und Gebaeudemodell verwenden unterschiedliche Projekt-IDs.",
                "project_id",
            )
        )
    if spec.building_id != building_spec.building.building_id:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_BUILDING_REFERENCE_MISMATCH",
                "Zonenmodell verweist nicht auf das geladene Gebaeude.",
                "building_id",
            )
        )
    if spec.source_building_version_id != building_spec.model_version.version_id:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_BUILDING_VERSION_REFERENCE_MISMATCH",
                "Zonenmodell verweist nicht auf die geladene Gebaeudemodellversion.",
                "source_building_version_id",
            )
        )

    known_space_ids = building_spec.space_ids
    for index, zone in enumerate(spec.zones):
        unknown_space_ids = sorted(set(zone.source_space_ids) - known_space_ids)
        if unknown_space_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_SOURCE_SPACE_UNKNOWN",
                    f"Zone verweist auf unbekannte Raeume: {', '.join(unknown_space_ids)}",
                    f"zones.{index}.source_space_ids",
                )
            )

    expected_floor_area = building_spec.building.length_m * building_spec.building.width_m
    total_zone_area = sum(zone.floor_area_m2 for zone in spec.zones)
    if expected_floor_area > 0 and abs(total_zone_area - expected_floor_area) > 0.01:
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "ZONE_AREA_BUILDING_FOOTPRINT_MISMATCH",
                "Die Summe der Zonenflaechen weicht von der einfachen Gebaeudegrundflaeche ab.",
                "zones",
            )
        )
    return messages
