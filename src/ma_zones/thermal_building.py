"""Abschlussvertrag von Building-, Zonen- und Technikstand fuer P018."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ma_building import BuildingModelSpecification
from ma_validation import (
    DiagnosticMessage,
    DiagnosticSeverity,
    ReleaseStatus,
    ValidationResult,
    build_validation_result,
)

from .models import ZoneModelSpecification

if TYPE_CHECKING:
    from ma_technical import TechnicalModelRevision


@dataclass(frozen=True, slots=True)
class ThermalBuildingModel:
    """Freigegebener, referenzbasierter Gebaeude-/Zonenabschluss."""

    thermal_building_model_id: str
    project_id: str
    building_id: str
    building_revision_id: str
    zone_model_id: str
    technical_model_id: str
    technical_revision_id: str
    technical_content_hash: str
    room_zone_assignments: tuple[tuple[str, str], ...]
    release_status: ReleaseStatus = ReleaseStatus.RELEASED

    def __post_init__(self) -> None:
        object.__setattr__(self, "room_zone_assignments", tuple(self.room_zone_assignments))
        if not isinstance(self.release_status, ReleaseStatus):
            object.__setattr__(self, "release_status", ReleaseStatus(self.release_status))


def build_thermal_building_model(
    building_spec: BuildingModelSpecification,
    zone_spec: ZoneModelSpecification,
    technical_revision: TechnicalModelRevision,
    *,
    thermal_building_model_id: str,
) -> ThermalBuildingModel:
    """Baut den Abschlussvertrag aus bereits freigegebenen Quellobjekten."""
    assignments = tuple(
        (space_id, zone.zone_id)
        for zone in zone_spec.zones
        for space_id in zone.source_space_ids
    )
    return ThermalBuildingModel(
        thermal_building_model_id=thermal_building_model_id,
        project_id=building_spec.project.project_id,
        building_id=building_spec.building.building_id,
        building_revision_id=building_spec.model_version.version_id,
        zone_model_id=zone_spec.zone_model_id,
        technical_model_id=technical_revision.technical_model_id,
        technical_revision_id=technical_revision.revision_id,
        technical_content_hash=technical_revision.content_hash,
        room_zone_assignments=assignments,
        release_status=technical_revision.release_status,
    )


def validate_thermal_building_model(
    model: ThermalBuildingModel,
    *,
    building_spec: BuildingModelSpecification,
    zone_spec: ZoneModelSpecification,
) -> ValidationResult:
    """Prueft den Abschlussvertrag gegen die geladenen Building- und Zonenstaende."""
    messages: list[DiagnosticMessage] = []
    if model.project_id != building_spec.project.project_id or model.project_id != zone_spec.project_id:
        messages.append(_message("THERMAL_BUILDING_PROJECT_MISMATCH", "Projekt-IDs der Eingabestaende stimmen nicht ueberein.", "project_id"))
    if model.building_id != building_spec.building.building_id or model.building_id != zone_spec.building_id:
        messages.append(_message("THERMAL_BUILDING_BUILDING_MISMATCH", "Gebaeude-IDs der Eingabestaende stimmen nicht ueberein.", "building_id"))
    if model.building_revision_id != building_spec.model_version.version_id:
        messages.append(_message("THERMAL_BUILDING_REVISION_MISMATCH", "Building-Revision stimmt nicht mit dem Abschlussvertrag ueberein.", "building_revision_id"))
    if model.zone_model_id != zone_spec.zone_model_id:
        messages.append(_message("THERMAL_BUILDING_ZONE_MODEL_MISMATCH", "Zonenmodell stimmt nicht mit dem Abschlussvertrag ueberein.", "zone_model_id"))
    if model.release_status is not ReleaseStatus.RELEASED:
        messages.append(_message("THERMAL_BUILDING_TECHNICAL_NOT_RELEASED", "Der referenzierte Technikstand ist nicht freigegeben.", "technical_revision_id"))
    if not model.technical_model_id or not model.technical_revision_id or not model.technical_content_hash:
        messages.append(_message("THERMAL_BUILDING_TECHNICAL_REFERENCE_INCOMPLETE", "Die technische Referenz ist unvollstaendig.", "technical_revision_id"))

    assignments = dict(model.room_zone_assignments)
    if len(assignments) != len(model.room_zone_assignments):
        messages.append(_message("THERMAL_BUILDING_ROOM_DUPLICATE", "Ein Raum ist mehreren Zonen zugeordnet.", "room_zone_assignments"))
    for space_id in building_spec.space_ids:
        if space_id not in assignments:
            messages.append(_message("THERMAL_BUILDING_ROOM_UNASSIGNED", "Ein Building-Raum ist keiner Zone zugeordnet.", "room_zone_assignments"))
    if set(assignments) - building_spec.space_ids:
        messages.append(_message("THERMAL_BUILDING_ROOM_REFERENCE_UNKNOWN", "Die Raumzuordnung enthaelt unbekannte Raeume.", "room_zone_assignments"))
    if not set(assignments.values()) <= zone_spec.zone_ids:
        messages.append(_message("THERMAL_BUILDING_ZONE_REFERENCE_UNKNOWN", "Die Raumzuordnung enthaelt unbekannte Zonen.", "room_zone_assignments"))
    return build_validation_result(tuple(messages))


def _message(code: str, message: str, location: str) -> DiagnosticMessage:
    return DiagnosticMessage(DiagnosticSeverity.ERROR, code, message, location)
