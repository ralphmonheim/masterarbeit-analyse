"""Schreibfreie P013-Freigabebereitschaft fuer die direkte Modulansicht."""

from __future__ import annotations

from dataclasses import dataclass, replace

from ma_building import (
    BuildingModelSpecification,
    ProjectInfo,
    validate_building_spec,
)
from ma_technical import ObjectReference, ReleasedTechnicalHandover, TechnicalModelRevision
from ma_validation import ReleaseStatus, ValidationResult, build_validation_result
from ma_zones import (
    ReleasedZoneHandover,
    ThermalBuildingModel,
    ZoneModelSpecification,
    build_released_zone_handover,
    build_thermal_building_model,
    validate_thermal_building_model,
    validate_zone_spec,
    validate_zone_technical_assignments,
)

from .zones_assignment_support import (
    bind_zone_specification_to_project,
    stored_technical_assignment_draft,
)


@dataclass(frozen=True, slots=True)
class ZoneReleasePreview:
    """Nur im Speicher erzeugte P013-Pruefkette ohne Freigabepersistenz."""

    building_specification: BuildingModelSpecification
    zone_specification: ZoneModelSpecification
    thermal_building_model: ThermalBuildingModel
    validation_result: ValidationResult
    zone_handover: ReleasedZoneHandover | None


def materialize_project_zone_specification(
    payload: dict[str, object],
    *,
    project_id: str,
    model_key: str,
    source_zone_specification: ZoneModelSpecification,
    building_reference: ObjectReference,
    technical_handover: ReleasedTechnicalHandover,
) -> ZoneModelSpecification:
    """Fuehrt den versionierten Zonenstand und gespeicherte Projektdrafts zusammen."""
    _require_active_model(payload, project_id=project_id, model_key=model_key, zone_spec=source_zone_specification)
    project_zone_spec = bind_zone_specification_to_project(
        source_zone_specification,
        project_id=project_id,
        building_reference=building_reference,
    )
    model_draft = _model_draft(payload, model_key)
    if model_draft.get("technical_assignment_status") not in {
        "validated_draft",
        "empty_validated_draft",
    }:
        raise ValueError(
            "Die technische Zonenzuordnung wurde noch nicht als gepruefter Projektentwurf gespeichert."
        )
    stored_assignments = stored_technical_assignment_draft(
        payload,
        model_key=model_key,
        zone_spec=project_zone_spec,
        handover=technical_handover,
    )
    if not stored_assignments.has_stored_draft:
        raise ValueError(
            "Die technische Zonenzuordnung wurde noch nicht als gepruefter Projektentwurf gespeichert."
        )
    if not stored_assignments.matches_active_handover:
        raise ValueError(
            "Die gespeicherte technische Zonenzuordnung gehoert nicht zum aktiven Zonen- und P014-Stand."
        )

    profile_assignments = _profile_assignments(
        model_draft,
        model_key=model_key,
        zone_spec=project_zone_spec,
    )
    zones = tuple(
        replace(zone, usage_profile_id=profile_assignments.get(zone.zone_id, zone.usage_profile_id))
        for zone in project_zone_spec.zones
    )
    return replace(
        project_zone_spec,
        zones=zones,
        technical_assignments=stored_assignments.assignments,
    )


def build_zone_release_preview(
    payload: dict[str, object],
    *,
    project_id: str,
    model_key: str,
    building_specification: BuildingModelSpecification,
    building_reference: ObjectReference,
    source_zone_specification: ZoneModelSpecification,
    technical_revision: TechnicalModelRevision,
    technical_handover: ReleasedTechnicalHandover,
) -> ZoneReleasePreview:
    """Baut und prueft den aktuellen P013-Stand ausschliesslich im Speicher."""
    building_spec = _bind_building_specification_to_project(
        building_specification,
        project_id=project_id,
        building_reference=building_reference,
    )
    zone_spec = materialize_project_zone_specification(
        payload,
        project_id=project_id,
        model_key=model_key,
        source_zone_specification=source_zone_specification,
        building_reference=building_reference,
        technical_handover=technical_handover,
    )
    thermal_model = build_thermal_building_model(
        building_spec,
        zone_spec,
        technical_revision,
        thermal_building_model_id="P013-READINESS-PREVIEW",
    )
    messages = (
        *validate_building_spec(building_spec).messages,
        *validate_zone_spec(zone_spec, building_spec=building_spec).messages,
        *validate_zone_technical_assignments(zone_spec, technical_handover).messages,
        *validate_thermal_building_model(
            thermal_model,
            building_spec=building_spec,
            zone_spec=zone_spec,
        ).messages,
    )
    validation = build_validation_result(tuple(messages))
    zone_handover = None
    if validation.release_status is ReleaseStatus.RELEASED:
        zone_handover = build_released_zone_handover(
            building_spec,
            zone_spec,
            thermal_model,
            technical_handover,
        )
    return ZoneReleasePreview(
        building_specification=building_spec,
        zone_specification=zone_spec,
        thermal_building_model=thermal_model,
        validation_result=validation,
        zone_handover=zone_handover,
    )


def _bind_building_specification_to_project(
    building_spec: BuildingModelSpecification,
    *,
    project_id: str,
    building_reference: ObjectReference,
) -> BuildingModelSpecification:
    if building_spec.building.building_id != building_reference.object_id:
        raise ValueError("Building-Spezifikation und uebernommene Building-ID stimmen nicht ueberein.")
    if building_spec.model_version.version_id != building_reference.revision_id:
        raise ValueError("Building-Spezifikation und uebernommene Building-Revision stimmen nicht ueberein.")
    normalized_project_id = project_id.strip()
    if not normalized_project_id:
        raise ValueError("Die Projekt-ID fuer die Vorschau darf nicht leer sein.")
    return replace(
        building_spec,
        project=ProjectInfo(project_id=normalized_project_id, name=building_spec.project.name),
    )


def _require_active_model(
    payload: dict[str, object],
    *,
    project_id: str,
    model_key: str,
    zone_spec: ZoneModelSpecification,
) -> None:
    if payload.get("project_id") != project_id:
        raise ValueError("Die Zonenkonfiguration gehoert nicht zum aktiven Projekt.")
    if payload.get("active_model") != model_key:
        raise ValueError("Das sichtbare Zonenmodell ist noch nicht als aktives Projektmodell uebernommen.")
    if payload.get("zone_model_id") != zone_spec.zone_model_id:
        raise ValueError("Die aktive Zonenmodell-ID stimmt nicht mit der geladenen Quelle ueberein.")


def _model_draft(payload: dict[str, object], model_key: str) -> dict[str, object]:
    model_drafts = payload.get("model_drafts")
    if not isinstance(model_drafts, dict):
        raise ValueError("Die Zonenkonfiguration enthaelt keine gueltigen Modelldrafts.")
    model_draft = model_drafts.get(model_key)
    if not isinstance(model_draft, dict):
        raise ValueError("Fuer das aktive Zonenmodell fehlt ein gueltiger Projektentwurf.")
    if model_draft.get("zone_model_id") != payload.get("zone_model_id"):
        raise ValueError("Der Projektentwurf gehoert nicht zur aktiven Zonenmodell-ID.")
    return model_draft


def _profile_assignments(
    model_draft: dict[str, object],
    *,
    model_key: str,
    zone_spec: ZoneModelSpecification,
) -> dict[str, str]:
    if model_key == "29Z":
        raise ValueError(
            "Der 29Z-Entwurf besitzt noch keinen autoritativen, hashgebundenen Quellen- und "
            "Rechtenachweis fuer vollstaendige Profilwerte."
        )
    raw_assignments = model_draft.get("profile_assignments")
    if raw_assignments is None:
        return {}
    if not isinstance(raw_assignments, dict):
        raise ValueError("Gespeicherte Nutzungsprofil-Zuordnungen haben ein ungueltiges Format.")
    assignments = {
        str(zone_id).strip(): str(profile_id).strip()
        for zone_id, profile_id in raw_assignments.items()
    }
    if set(assignments) != zone_spec.zone_ids:
        raise ValueError("Die Nutzungsprofil-Zuordnungen decken nicht exakt alle Zonen ab.")
    unknown_profile_ids = sorted(set(assignments.values()) - zone_spec.usage_profile_ids)
    if unknown_profile_ids:
        raise ValueError(
            "Fuer die gewaehlten Nutzungsprofile fehlen vollstaendige Profilwerte: "
            + ", ".join(unknown_profile_ids)
        )
    return assignments
