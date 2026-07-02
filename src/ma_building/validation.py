"""Fachliche Validierung fuer die v1-Gebaeudespezifikation."""

from __future__ import annotations

from collections import defaultdict

from ma_validation import DiagnosticMessage, DiagnosticSeverity, ValidationResult, build_validation_result

from .models import VALID_CONSTRUCTION_CODES, BuildingMaturityLevel, BuildingModelSpecification


def validate_building_spec(spec: BuildingModelSpecification) -> ValidationResult:
    """Prueft die v1-Spezifikation und erzeugt ein gemeinsames ValidationResult."""
    messages: list[DiagnosticMessage] = []
    messages.extend(_validate_header(spec))
    messages.extend(_validate_object_ids(spec))
    messages.extend(_validate_storey_references(spec))
    messages.extend(_validate_spaces(spec))
    messages.extend(_validate_elements(spec))
    messages.extend(_validate_openings(spec))
    messages.extend(_validate_shading_devices(spec))
    return build_validation_result(tuple(messages))


def _message(
    severity: DiagnosticSeverity,
    code: str,
    message: str,
    location: str,
) -> DiagnosticMessage:
    return DiagnosticMessage(severity=severity, code=code, message=message, location=location)


def _validate_header(spec: BuildingModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    required_values = {
        "schema_version": spec.schema_version,
        "project.project_id": spec.project.project_id,
        "project.name": spec.project.name,
        "building.building_id": spec.building.building_id,
        "building.name": spec.building.name,
        "building.unit": spec.building.unit,
        "model_version.version_id": spec.model_version.version_id,
        "model_version.source_input_level": spec.model_version.source_input_level,
        "model_version.detected_input_level": spec.model_version.detected_input_level,
        "model_version.confirmed_input_level": spec.model_version.confirmed_input_level,
        "model_version.current_maturity_level": spec.model_version.current_maturity_level,
        "model_version.target_maturity_level": spec.model_version.target_maturity_level,
    }
    for location, value in required_values.items():
        if not str(value).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_REQUIRED_FIELD_MISSING",
                    "Pflichtfeld der BuildingModelSpecification fehlt.",
                    location,
                )
            )

    for location in (
        "model_version.source_input_level",
        "model_version.detected_input_level",
        "model_version.confirmed_input_level",
        "model_version.current_maturity_level",
        "model_version.target_maturity_level",
    ):
        value = getattr(spec.model_version, location.rsplit(".", maxsplit=1)[1])
        if value and not isinstance(value, BuildingMaturityLevel):
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_MATURITY_LEVEL_INVALID",
                    f"Unbekannter Gebaeude-Reifegrad: {value}",
                    location,
                )
            )

    if spec.building.unit != "m":
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BUILDING_UNIT_UNSUPPORTED",
                "ma_building v1 unterstuetzt als Laengeneinheit nur Meter.",
                "building.unit",
            )
        )
    if not 0 <= spec.building.north_angle_deg < 360:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BUILDING_NORTH_ANGLE_INVALID",
                "Die Nordrichtung muss im Bereich 0 <= Winkel < 360 Grad liegen.",
                "building.north_angle_deg",
            )
        )
    if min(spec.building.length_m, spec.building.width_m, spec.building.height_m) <= 0:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BUILDING_DIMENSIONS_INVALID",
                "Gebaeudeabmessungen muessen groesser als 0 sein.",
                "building",
            )
        )
    return messages


def _validate_object_ids(spec: BuildingModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    locations_by_id: dict[str, list[str]] = defaultdict(list)
    for object_id, location in spec.object_id_locations():
        if not object_id:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_OBJECT_ID_MISSING",
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
                    "BUILDING_OBJECT_ID_DUPLICATE",
                    f"Objekt-ID ist mehrfach vergeben: {object_id}",
                    ", ".join(locations),
                )
            )
    return messages


def _validate_storey_references(spec: BuildingModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not spec.storeys:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BUILDING_STOREYS_MISSING",
                "Mindestens ein Geschoss ist erforderlich.",
                "storeys",
            )
        )
    for index, storey in enumerate(spec.storeys):
        if storey.height_m <= 0:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_STOREY_HEIGHT_INVALID",
                    "Geschosshoehen muessen groesser als 0 sein.",
                    f"storeys.{index}.height_m",
                )
            )
    return messages


def _validate_spaces(spec: BuildingModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not spec.spaces:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BUILDING_SPACES_MISSING",
                "Mindestens ein Raum ist erforderlich.",
                "spaces",
            )
        )
    for index, space in enumerate(spec.spaces):
        if space.storey_id not in spec.storey_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_SPACE_STOREY_UNKNOWN",
                    f"Raum verweist auf unbekanntes Geschoss: {space.storey_id}",
                    f"spaces.{index}.storey_id",
                )
            )
        if min(space.floor_area_m2, space.volume_m3) <= 0:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_SPACE_GEOMETRY_INVALID",
                    "Raumflaeche und Raumvolumen muessen groesser als 0 sein.",
                    f"spaces.{index}",
                )
            )
    return messages


def _validate_elements(spec: BuildingModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not spec.elements:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BUILDING_ELEMENTS_MISSING",
                "Mindestens ein Bauteil ist erforderlich.",
                "elements",
            )
        )
    for index, element in enumerate(spec.elements):
        if element.construction_code not in VALID_CONSTRUCTION_CODES:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_CONSTRUCTION_CODE_INVALID",
                    f"Unbekannter Bauteilcode: {element.construction_code}",
                    f"elements.{index}.construction_code",
                )
            )
        if element.storey_id not in spec.storey_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_ELEMENT_STOREY_UNKNOWN",
                    f"Bauteil verweist auf unbekanntes Geschoss: {element.storey_id}",
                    f"elements.{index}.storey_id",
                )
            )
        if element.area_m2 <= 0:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_ELEMENT_AREA_INVALID",
                    "Bauteilflaechen muessen groesser als 0 sein.",
                    f"elements.{index}.area_m2",
                )
            )
        if element.orientation_deg is not None and not 0 <= element.orientation_deg < 360:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_ELEMENT_ORIENTATION_INVALID",
                    "Bauteilorientierungen muessen im Bereich 0 <= Winkel < 360 Grad liegen.",
                    f"elements.{index}.orientation_deg",
                )
            )
        for space_id in element.adjacent_space_ids:
            if space_id not in spec.space_ids:
                messages.append(
                    _message(
                        DiagnosticSeverity.ERROR,
                        "BUILDING_ELEMENT_SPACE_UNKNOWN",
                        f"Bauteil verweist auf unbekannten Raum: {space_id}",
                        f"elements.{index}.adjacent_space_ids",
                    )
                )
    return messages


def _validate_openings(spec: BuildingModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    for index, opening in enumerate(spec.openings):
        if opening.construction_code not in VALID_CONSTRUCTION_CODES:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_OPENING_CODE_INVALID",
                    f"Unbekannter Oeffnungscode: {opening.construction_code}",
                    f"openings.{index}.construction_code",
                )
            )
        if opening.host_element_id not in spec.element_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_OPENING_HOST_UNKNOWN",
                    f"Oeffnung verweist auf unbekanntes Host-Bauteil: {opening.host_element_id}",
                    f"openings.{index}.host_element_id",
                )
            )
        if opening.area_m2 <= 0:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_OPENING_AREA_INVALID",
                    "Oeffnungsflaechen muessen groesser als 0 sein.",
                    f"openings.{index}.area_m2",
                )
            )
    return messages


def _validate_shading_devices(spec: BuildingModelSpecification) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    opening_ids = {opening.opening_id for opening in spec.openings}
    for index, shading in enumerate(spec.shading_devices):
        if shading.opening_id not in opening_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BUILDING_SHADING_OPENING_UNKNOWN",
                    f"Sonnenschutz verweist auf unbekannte Oeffnung: {shading.opening_id}",
                    f"shading_devices.{index}.opening_id",
                )
            )
    return messages
