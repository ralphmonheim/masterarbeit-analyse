"""Schmale UI-Unterstuetzung fuer manuelle P013-Technikzuordnungen."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from typing import Any

from ma_technical import ObjectReference, ReleasedTechnicalHandover
from ma_validation import ReleaseStatus, ValidationResult
from ma_zones import (
    ZoneModelSpecification,
    ZoneTechnicalServiceAssignment,
    validate_zone_technical_assignments,
    zone_specification_to_dict,
)


@dataclass(frozen=True, slots=True)
class StoredTechnicalAssignmentDraft:
    """Bereits gespeicherter Entwurf und sein Bezug zum aktiven Handover."""

    assignments: tuple[ZoneTechnicalServiceAssignment, ...]
    has_stored_draft: bool
    matches_active_handover: bool


def bind_zone_specification_to_project(
    zone_spec: ZoneModelSpecification,
    *,
    project_id: str,
    building_reference: ObjectReference,
) -> ZoneModelSpecification:
    """Bindet eine versionierte Zonenquelle an das Projekt, ohne sie zu aendern."""
    if zone_spec.building_id != building_reference.object_id:
        raise ValueError("Zonenmodell und uebernommener Building-Stand haben unterschiedliche Building-IDs.")
    if zone_spec.source_building_version_id != building_reference.revision_id:
        raise ValueError("Zonenmodell und uebernommener Building-Stand haben unterschiedliche Revisionen.")
    normalized_project_id = project_id.strip()
    if not normalized_project_id:
        raise ValueError("Die Projekt-ID fuer den Zonenentwurf darf nicht leer sein.")
    return replace(zone_spec, project_id=normalized_project_id)


def technical_handover_rows(handover: ReleasedTechnicalHandover) -> list[dict[str, object]]:
    """Bereitet den aktiven P014-Handover kompakt fuer die direkte UI auf."""
    return [
        {
            "Serviceinterface": reference.interface_id,
            "Dienst": reference.service_type,
            "Medium": reference.medium,
            "Technikobjekt": reference.source_object_reference.object_id,
            "Kompatible Terminaltypen": ", ".join(reference.compatible_terminal_types) or "nicht deklariert",
        }
        for reference in handover.service_interface_references
    ]


def technical_assignment_editor_rows(
    zone_spec: ZoneModelSpecification,
    handover: ReleasedTechnicalHandover,
    stored_assignments: tuple[ZoneTechnicalServiceAssignment, ...] = (),
) -> list[dict[str, object]]:
    """Zeigt jede moegliche Zone-Interface-Kombination ohne Vorauswahl."""
    stored_by_key = {
        (assignment.zone_id, assignment.service_interface_id): assignment
        for assignment in stored_assignments
    }
    rows: list[dict[str, object]] = []
    for zone in zone_spec.zones:
        for reference in handover.service_interface_references:
            stored = stored_by_key.get((zone.zone_id, reference.interface_id))
            rows.append(
                {
                    "Zone-ID": zone.zone_id,
                    "Zone": zone.name,
                    "Serviceinterface": reference.interface_id,
                    "Dienst": reference.service_type,
                    "Medium": reference.medium,
                    "Zuordnen": stored is not None,
                    "Terminaltyp": stored.terminal_type if stored else "",
                    "Manuell bestaetigt": bool(
                        stored is not None and stored.assignment_origin == "manual_confirmed"
                    ),
                }
            )
    return rows


def technical_assignments_from_rows(
    zone_spec: ZoneModelSpecification,
    handover: ReleasedTechnicalHandover,
    edited_rows: Any,
) -> tuple[ZoneTechnicalServiceAssignment, ...]:
    """Erzeugt nur aus explizit ausgewaehlten Tabellenzeilen Fachobjekte."""
    known_zone_ids = zone_spec.zone_ids
    known_interface_ids = {
        reference.interface_id for reference in handover.service_interface_references
    }
    assignments: list[ZoneTechnicalServiceAssignment] = []
    for row in _records(edited_rows):
        selected = _checkbox_value(row.get("Zuordnen", False), "Zuordnen")
        if not selected:
            continue
        zone_id = str(row.get("Zone-ID", "")).strip()
        interface_id = str(row.get("Serviceinterface", "")).strip()
        if zone_id not in known_zone_ids:
            raise ValueError(f"Unbekannte Zone im Zuordnungsentwurf: {zone_id}")
        if interface_id not in known_interface_ids:
            raise ValueError(f"Unbekanntes Serviceinterface im Zuordnungsentwurf: {interface_id}")
        assignments.append(
            ZoneTechnicalServiceAssignment(
                assignment_id=f"ZTA-{zone_id}--{interface_id}",
                zone_id=zone_id,
                service_interface_id=interface_id,
                terminal_type=str(row.get("Terminaltyp", "")).strip(),
                assignment_origin=(
                    "manual_confirmed"
                    if _checkbox_value(
                        row.get("Manuell bestaetigt", False),
                        "Manuell bestaetigt",
                    )
                    else ""
                ),
            )
        )
    return tuple(
        sorted(
            assignments,
            key=lambda assignment: (assignment.zone_id, assignment.service_interface_id),
        )
    )


def validate_technical_assignment_draft(
    zone_spec: ZoneModelSpecification,
    handover: ReleasedTechnicalHandover,
    assignments: tuple[ZoneTechnicalServiceAssignment, ...],
) -> tuple[ZoneModelSpecification, ValidationResult]:
    """Validiert den Entwurf gegen genau den sichtbaren P014-Handover."""
    draft_spec = replace(zone_spec, technical_assignments=assignments)
    return draft_spec, validate_zone_technical_assignments(draft_spec, handover)


def technical_assignment_check_token(
    zone_spec: ZoneModelSpecification,
    handover: ReleasedTechnicalHandover,
    assignments: tuple[ZoneTechnicalServiceAssignment, ...],
) -> tuple[object, ...]:
    """Bindet eine UI-Pruefung an Entwurf, Zonenmodell und Technikstand."""
    return (
        zone_spec.zone_model_id,
        zone_spec.project_id,
        zone_spec.building_id,
        zone_spec.source_building_version_id,
        zone_specification_content_hash(zone_spec),
        handover.technical_model_id,
        handover.revision_id,
        handover.content_hash,
        handover.handover_content_hash,
        tuple(
            (
                assignment.assignment_id,
                assignment.zone_id,
                assignment.service_interface_id,
                assignment.terminal_type,
                assignment.assignment_origin,
            )
            for assignment in assignments
        ),
    )


def stored_technical_assignment_draft(
    payload: dict[str, object],
    *,
    model_key: str,
    zone_spec: ZoneModelSpecification,
    handover: ReleasedTechnicalHandover,
) -> StoredTechnicalAssignmentDraft:
    """Laedt nur Zuordnungen fuer exakt denselben Zonen- und Technikstand."""
    _require_payload_project_id(payload, zone_spec.project_id)
    model_drafts = payload.get("model_drafts", {})
    if not isinstance(model_drafts, dict):
        raise ValueError("Gespeicherte model_drafts haben ein ungueltiges Format.")
    if model_key not in model_drafts:
        return StoredTechnicalAssignmentDraft((), False, False)
    model_draft = model_drafts[model_key]
    if not isinstance(model_draft, dict):
        raise ValueError("Der gespeicherte Zonenmodelldraft hat ein ungueltiges Format.")
    rows = model_draft.get("technical_assignments")
    has_stored_draft = "technical_assignment_status" in model_draft
    if rows is None and has_stored_draft:
        rows = []
    elif rows is None:
        return StoredTechnicalAssignmentDraft((), False, False)
    if not isinstance(rows, list):
        raise ValueError("Gespeicherte technische Zuordnungen haben ein ungueltiges Format.")
    reference = model_draft.get("technical_handover_reference")
    zone_reference = model_draft.get("zone_specification_reference")
    matches = (
        reference == technical_handover_reference(handover)
        and zone_reference == zone_specification_reference(zone_spec)
    )
    if not matches:
        return StoredTechnicalAssignmentDraft((), True, False)
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("Gespeicherte technische Zuordnungen haben ein ungueltiges Format.")
    assignments = tuple(
        ZoneTechnicalServiceAssignment(
            assignment_id=str(row.get("assignment_id", "")),
            zone_id=str(row.get("zone_id", "")),
            service_interface_id=str(row.get("service_interface_id", "")),
            terminal_type=str(row.get("terminal_type", "")),
            assignment_origin=str(row.get("assignment_origin", "")),
        )
        for row in rows
    )
    return StoredTechnicalAssignmentDraft(assignments, True, True)


def technical_assignment_project_payload(
    payload: dict[str, object],
    *,
    project_id: str,
    model_key: str,
    zone_spec: ZoneModelSpecification,
    handover: ReleasedTechnicalHandover,
    assignments: tuple[ZoneTechnicalServiceAssignment, ...],
) -> dict[str, object]:
    """Ergaenzt den validierten Entwurf additiv in der ma_zones-Konfiguration."""
    if zone_spec.project_id != project_id:
        raise ValueError("Zonenentwurf und Projektkonfiguration verwenden unterschiedliche Projekt-IDs.")
    _require_payload_project_id(payload, project_id)
    _draft_spec, validation = validate_technical_assignment_draft(
        zone_spec,
        handover,
        assignments,
    )
    if validation.release_status is not ReleaseStatus.RELEASED:
        raise ValueError("Nur ein fehlerfreier technischer Zuordnungsentwurf darf gespeichert werden.")
    updated_payload = dict(payload)
    model_drafts = updated_payload.get("model_drafts", {})
    if not isinstance(model_drafts, dict):
        raise ValueError("Gespeicherte model_drafts haben ein ungueltiges Format.")
    model_drafts = dict(model_drafts)
    model_draft = model_drafts.get(model_key, {})
    if not isinstance(model_draft, dict):
        raise ValueError("Der gespeicherte Zonenmodelldraft hat ein ungueltiges Format.")
    model_draft = dict(model_draft)
    model_draft.update(
        {
            "zone_model_id": zone_spec.zone_model_id,
            "technical_assignment_status": (
                "validated_draft" if assignments else "empty_validated_draft"
            ),
            "technical_handover_reference": technical_handover_reference(handover),
            "zone_specification_reference": zone_specification_reference(zone_spec),
            "zone_handover_status": "not_created",
        }
    )
    if assignments:
        model_draft["technical_assignments"] = [asdict(assignment) for assignment in assignments]
    else:
        model_draft.pop("technical_assignments", None)
    model_drafts[model_key] = model_draft
    updated_payload.update(
        {
            "schema_version": "1.0",
            "project_id": project_id,
            "model_drafts": model_drafts,
        }
    )
    return updated_payload


def technical_handover_reference(handover: ReleasedTechnicalHandover) -> dict[str, str]:
    """Liefert das vollstaendige gespeicherte Referenztriple samt Bindungshashes."""
    building_reference = handover.building_reference
    return {
        "technical_model_id": handover.technical_model_id,
        "technical_revision_id": handover.revision_id,
        "technical_content_hash": handover.content_hash,
        "technical_handover_content_hash": handover.handover_content_hash,
        "service_interface_references_hash": handover.service_interface_references_hash,
        "release_evidence_hash": handover.release_evidence_hash,
        "building_id": building_reference.object_id if building_reference else "",
        "building_revision_id": building_reference.revision_id if building_reference else "",
    }


def zone_specification_reference(zone_spec: ZoneModelSpecification) -> dict[str, str]:
    """Bindet einen Entwurf an die konkrete Zonen- und Raumzusammensetzung."""
    return {
        "zone_model_id": zone_spec.zone_model_id,
        "zone_specification_content_hash": zone_specification_content_hash(zone_spec),
        "building_id": zone_spec.building_id,
        "building_revision_id": zone_spec.source_building_version_id,
    }


def zone_specification_content_hash(zone_spec: ZoneModelSpecification) -> str:
    """Hasht den kanonischen Zoneninhalt ohne den bearbeiteten Assignment-Entwurf."""
    payload = zone_specification_to_dict(replace(zone_spec, technical_assignments=()))
    canonical_json = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def _records(edited_rows: Any) -> list[dict[str, object]]:
    if hasattr(edited_rows, "to_dict"):
        records = edited_rows.to_dict("records")
    elif isinstance(edited_rows, list | tuple):
        records = edited_rows
    else:
        raise ValueError("Der technische Zuordnungsentwurf ist keine Tabelle.")
    if not all(isinstance(row, dict) for row in records):
        raise ValueError("Der technische Zuordnungsentwurf enthaelt ungueltige Zeilen.")
    return list(records)


def _checkbox_value(value: object, field_name: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{field_name} muss ein expliziter Checkboxwert sein.")
    return value


def _require_payload_project_id(payload: dict[str, object], expected_project_id: str) -> None:
    if "project_id" not in payload:
        return
    stored_project_id = payload["project_id"]
    if not isinstance(stored_project_id, str) or not stored_project_id.strip():
        raise ValueError("Die vorhandene Zonenkonfiguration hat keine gueltige Projekt-ID.")
    if stored_project_id.strip() != expected_project_id:
        raise ValueError("Die vorhandene Zonenkonfiguration gehoert nicht zum aktiven Projekt.")
