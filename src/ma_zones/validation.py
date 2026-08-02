"""Fachliche Validierung fuer ma_zones."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from ma_building import BuildingModelSpecification
from ma_technical import TechnicalSystemSpecification
from ma_validation import (
    DiagnosticMessage,
    DiagnosticSeverity,
    ReleaseStatus,
    ValidationResult,
    build_validation_result,
)

from .models import ZoneInputDetailLevel, ZoneModelSpecification

if TYPE_CHECKING:
    from ma_technical import ReleasedTechnicalHandover, ReleasedTechnicalServiceInterfaceReference


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
    messages.extend(_validate_technical_assignments(spec))
    if building_spec is not None:
        messages.extend(_validate_building_reference(spec, building_spec))
    return build_validation_result(tuple(messages))


def validate_zone_technical_assignments(
    zone_spec: ZoneModelSpecification,
    technical_handover: ReleasedTechnicalHandover,
) -> ValidationResult:
    """Prueft bestaetigte Zonen-Zuordnungen gegen den freigegebenen P014-Handover."""
    from ma_technical import ReleasedTechnicalHandover

    messages = _validate_technical_assignments(zone_spec)
    if not isinstance(technical_handover, ReleasedTechnicalHandover):
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_TECHNICAL_HANDOVER_TYPE_INVALID",
                "Die technische Zuordnung benoetigt einen ReleasedTechnicalHandover.",
                "technical_handover",
            )
        )
        return build_validation_result(tuple(messages))

    if technical_handover.release_status is not ReleaseStatus.RELEASED:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_TECHNICAL_HANDOVER_NOT_RELEASED",
                "Der referenzierte Technikstand ist nicht freigegeben.",
                "technical_handover.release_status",
            )
        )
    if not all(
        (
            technical_handover.technical_model_id,
            technical_handover.revision_id,
            technical_handover.content_hash,
        )
    ):
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_TECHNICAL_HANDOVER_REFERENCE_INCOMPLETE",
                "Die Modell-, Revisions- oder Hashreferenz des Technikstands ist unvollstaendig.",
                "technical_handover",
            )
        )

    requires_complete_context = bool(zone_spec.technical_assignments)
    if technical_handover.project_id:
        if technical_handover.project_id != zone_spec.project_id:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_TECHNICAL_PROJECT_REFERENCE_MISMATCH",
                    "Technik-Handover und Zonenmodell verwenden unterschiedliche Projekt-IDs.",
                    "technical_handover.project_id",
                )
            )
    elif requires_complete_context:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_TECHNICAL_PROJECT_REFERENCE_MISMATCH",
                "Technik-Handover enthaelt keine Projekt-ID fuer die technische Zonenzuordnung.",
                "technical_handover.project_id",
            )
        )

    building_reference = technical_handover.building_reference
    if building_reference is not None:
        if building_reference.object_id != zone_spec.building_id:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_TECHNICAL_BUILDING_REFERENCE_MISMATCH",
                    "Technik-Handover verweist nicht auf das Gebaeude des Zonenmodells.",
                    "technical_handover.building_reference.object_id",
                )
            )
        if building_reference.revision_id != zone_spec.source_building_version_id:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_TECHNICAL_BUILDING_REVISION_MISMATCH",
                    "Technik-Handover und Zonenmodell verwenden unterschiedliche Building-Revisionen.",
                    "technical_handover.building_reference.revision_id",
                )
            )
    elif requires_complete_context:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_TECHNICAL_BUILDING_REFERENCE_MISMATCH",
                "Technik-Handover enthaelt keine Building-Referenz fuer die technische Zonenzuordnung.",
                "technical_handover.building_reference",
            )
        )

    if technical_handover.service_interface_references_hash:
        if not technical_handover.has_consistent_service_interface_references():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_TECHNICAL_INTERFACE_REFERENCES_HASH_MISMATCH",
                    "Die Serviceinterface-Referenzliste stimmt nicht mit ihrem Handover-Hash ueberein.",
                    "technical_handover.service_interface_references_hash",
                )
            )
    elif requires_complete_context:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_TECHNICAL_INTERFACE_REFERENCES_HASH_MISMATCH",
                "Technik-Handover enthaelt keinen Hash der Serviceinterface-Referenzliste.",
                "technical_handover.service_interface_references_hash",
            )
            )

    if technical_handover.handover_content_hash:
        if not technical_handover.has_consistent_handover_content():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_TECHNICAL_HANDOVER_CONTENT_HASH_MISMATCH",
                    "Techniktriple, Projekt, Building und Interfaceprojektion stimmen nicht mit dem Handover-Hash ueberein.",
                    "technical_handover.handover_content_hash",
                )
            )
    elif requires_complete_context:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_TECHNICAL_HANDOVER_CONTENT_HASH_MISMATCH",
                "Technik-Handover enthaelt keinen gebundenen Handover-Content-Hash.",
                "technical_handover.handover_content_hash",
            )
        )

    references_by_id: dict[str, ReleasedTechnicalServiceInterfaceReference] = {}
    duplicate_interface_ids: set[str] = set()
    for reference in technical_handover.service_interface_references:
        if reference.interface_id in references_by_id:
            duplicate_interface_ids.add(reference.interface_id)
        references_by_id[reference.interface_id] = reference
    if duplicate_interface_ids:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "ZONE_TECHNICAL_INTERFACE_REFERENCE_DUPLICATE",
                "Serviceinterface-IDs sind im Technik-Handover mehrfach enthalten: "
                + ", ".join(sorted(duplicate_interface_ids)),
                "technical_handover.service_interface_references",
            )
        )

    for index, assignment in enumerate(zone_spec.technical_assignments):
        reference = references_by_id.get(assignment.service_interface_id)
        if reference is None:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_TECHNICAL_INTERFACE_UNKNOWN",
                    f"Zuordnung verweist auf unbekanntes Serviceinterface: {assignment.service_interface_id}",
                    f"technical_assignments.{index}.service_interface_id",
                )
            )
            continue
        if assignment.terminal_type and assignment.terminal_type not in reference.compatible_terminal_types:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_TECHNICAL_TERMINAL_INCOMPATIBLE",
                    "Der bestaetigte Terminaltyp ist nicht mit dem Serviceinterface kompatibel.",
                    f"technical_assignments.{index}.terminal_type",
                )
            )
    return build_validation_result(tuple(messages))


def validate_technical_zone_integration(
    zone_spec: ZoneModelSpecification,
    technical_spec: TechnicalSystemSpecification,
) -> ValidationResult:
    """Prueft den zonenseitig verantworteten Abgleich zum Technikstand."""
    messages: list[DiagnosticMessage] = []
    if technical_spec.project_id != zone_spec.project_id:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "TECHNICAL_PROJECT_REFERENCE_MISMATCH",
                "Technik- und Zonenmodell verwenden unterschiedliche Projekt-IDs.",
                "project_id",
            )
        )
    if technical_spec.building_id != zone_spec.building_id:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "TECHNICAL_BUILDING_REFERENCE_MISMATCH",
                "Technikmodell verweist nicht auf das Zonen-Gebaeude.",
                "building_id",
            )
        )
    if technical_spec.source_zone_model_id != zone_spec.zone_model_id:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "TECHNICAL_ZONE_MODEL_REFERENCE_MISMATCH",
                "Technikmodell verweist nicht auf die geladene Zonenmodellversion.",
                "source_zone_model_id",
            )
        )

    known_zone_ids = zone_spec.zone_ids
    for index, system in enumerate(technical_spec.systems):
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


def _validate_technical_assignments(spec: ZoneModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    seen_assignments: set[tuple[str, str]] = set()
    for index, assignment in enumerate(spec.technical_assignments):
        location = f"technical_assignments.{index}"
        required_values = {
            "assignment_id": assignment.assignment_id,
            "zone_id": assignment.zone_id,
            "service_interface_id": assignment.service_interface_id,
            "assignment_origin": assignment.assignment_origin,
        }
        for field_name, value in required_values.items():
            if not value:
                messages.append(
                    _message(
                        DiagnosticSeverity.ERROR,
                        "ZONE_TECHNICAL_ASSIGNMENT_FIELD_MISSING",
                        "Pflichtfeld der technischen Zonenzuordnung fehlt.",
                        f"{location}.{field_name}",
                    )
                )
        if assignment.zone_id and assignment.zone_id not in spec.zone_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_TECHNICAL_ZONE_UNKNOWN",
                    f"Technische Zuordnung verweist auf unbekannte Zone: {assignment.zone_id}",
                    f"{location}.zone_id",
                )
            )
        if assignment.assignment_origin and assignment.assignment_origin != "manual_confirmed":
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_TECHNICAL_ASSIGNMENT_NOT_CONFIRMED",
                    "V1 uebergibt nur ausdruecklich manuell bestaetigte technische Zuordnungen.",
                    f"{location}.assignment_origin",
                )
            )

        assignment_key = (
            assignment.zone_id,
            assignment.service_interface_id,
        )
        if assignment_key in seen_assignments:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "ZONE_TECHNICAL_ASSIGNMENT_DUPLICATE",
                    "Dieselbe Zonen- und Serviceinterface-Zuordnung ist mehrfach enthalten.",
                    location,
                )
            )
        seen_assignments.add(assignment_key)
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

    expected_floor_area = (
        sum(space.floor_area_m2 for space in building_spec.spaces)
        if building_spec.spaces
        else building_spec.building.length_m * building_spec.building.width_m
    )
    total_zone_area = sum(zone.floor_area_m2 for zone in spec.zones)
    if expected_floor_area > 0 and abs(total_zone_area - expected_floor_area) > 0.01:
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "ZONE_AREA_BUILDING_FOOTPRINT_MISMATCH",
                "Die Summe der Zonenflaechen weicht von der Gebaeude-Raumflaeche ab.",
                "zones",
            )
        )
    return messages
