"""Pure JSON- and YAML-compatible serialization for P011 project models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .models import Project, ProjectIdentity, ProjectInvestigation, ProjectLocation


def project_to_payload(project: Project) -> dict[str, object]:
    """Return a stable nested payload without reading or writing any files."""
    if not isinstance(project, Project):
        raise TypeError("project muss ein Project-Objekt sein.")
    return {
        "identity": _identity_to_payload(project.identity),
        "created_at": project.created_at.isoformat(),
        "updated_at": project.updated_at.isoformat(),
        "location": _location_to_payload(project.location),
        "investigation": _investigation_to_payload(project.investigation),
    }


def project_from_payload(payload: dict[str, object]) -> Project:
    """Build a validated project from a JSON- or YAML-compatible dictionary."""
    root = _require_dictionary(payload, "payload")
    _reject_unknown_keys(
        root,
        {"identity", "created_at", "updated_at", "location", "investigation"},
        "payload",
    )
    identity = _identity_from_payload(_require_value(root, "identity", "payload"))
    created_at = _datetime_from_payload(_require_value(root, "created_at", "payload"), "created_at")
    updated_at = _datetime_from_payload(_require_value(root, "updated_at", "payload"), "updated_at")
    return Project(
        identity=identity,
        created_at=created_at,
        updated_at=updated_at,
        location=_location_from_payload(root.get("location")),
        investigation=_investigation_from_payload(root.get("investigation")),
    )


def _identity_to_payload(identity: ProjectIdentity) -> dict[str, object]:
    return {
        "project_id": identity.project_id,
        "title": identity.title,
        "short_name": identity.short_name,
        "description": identity.description,
        "project_type": identity.project_type,
        "author": identity.author,
        "organization": identity.organization,
    }


def _location_to_payload(location: ProjectLocation | None) -> dict[str, object] | None:
    if location is None:
        return None
    return {
        "country_code": location.country_code,
        "display_name": location.display_name,
        "postal_code": location.postal_code,
        "city": location.city,
        "street": location.street,
        "house_number": location.house_number,
        "latitude_deg": location.latitude_deg,
        "longitude_deg": location.longitude_deg,
        "elevation_m": location.elevation_m,
        "timezone": location.timezone,
        "notes": location.notes,
    }


def _investigation_to_payload(investigation: ProjectInvestigation | None) -> dict[str, object] | None:
    if investigation is None:
        return None
    return {
        "objective": investigation.objective,
        "research_question": investigation.research_question,
        "reference_case_description": investigation.reference_case_description,
        "scope": investigation.scope,
        "exclusions": list(investigation.exclusions),
        "methodology_note": investigation.methodology_note,
        "notes": investigation.notes,
    }


def _identity_from_payload(value: object) -> ProjectIdentity:
    payload = _require_dictionary(value, "identity")
    _reject_unknown_keys(
        payload,
        {"project_id", "title", "short_name", "description", "project_type", "author", "organization"},
        "identity",
    )
    return ProjectIdentity(
        project_id=_require_value(payload, "project_id", "identity"),
        title=_require_value(payload, "title", "identity"),
        short_name=_require_value(payload, "short_name", "identity"),
        description=payload.get("description", ""),
        project_type=payload.get("project_type", ""),
        author=payload.get("author", ""),
        organization=payload.get("organization", ""),
    )


def _location_from_payload(value: object | None) -> ProjectLocation | None:
    if value is None:
        return None
    payload = _require_dictionary(value, "location")
    _reject_unknown_keys(
        payload,
        {
            "country_code",
            "display_name",
            "postal_code",
            "city",
            "street",
            "house_number",
            "latitude_deg",
            "longitude_deg",
            "elevation_m",
            "timezone",
            "notes",
        },
        "location",
    )
    return ProjectLocation(
        country_code=_require_value(payload, "country_code", "location"),
        display_name=payload.get("display_name", ""),
        postal_code=payload.get("postal_code", ""),
        city=payload.get("city", ""),
        street=payload.get("street", ""),
        house_number=payload.get("house_number", ""),
        latitude_deg=payload.get("latitude_deg"),
        longitude_deg=payload.get("longitude_deg"),
        elevation_m=payload.get("elevation_m"),
        timezone=payload.get("timezone", ""),
        notes=payload.get("notes", ""),
    )


def _investigation_from_payload(value: object | None) -> ProjectInvestigation | None:
    if value is None:
        return None
    payload = _require_dictionary(value, "investigation")
    _reject_unknown_keys(
        payload,
        {
            "objective",
            "research_question",
            "reference_case_description",
            "scope",
            "exclusions",
            "methodology_note",
            "notes",
        },
        "investigation",
    )
    return ProjectInvestigation(
        objective=payload.get("objective", ""),
        research_question=payload.get("research_question", ""),
        reference_case_description=payload.get("reference_case_description", ""),
        scope=payload.get("scope", ""),
        exclusions=payload.get("exclusions", ()),
        methodology_note=payload.get("methodology_note", ""),
        notes=payload.get("notes", ""),
    )


def _datetime_from_payload(value: object, field_name: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} muss ein ISO-8601-Zeitstempel sein.")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} muss ein ISO-8601-Zeitstempel sein.") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field_name} muss einen Zeitzonenoffset enthalten.")
    return parsed


def _require_dictionary(value: object, field_name: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ValueError(f"{field_name} muss ein Dictionary mit Textschluesseln sein.")
    return value


def _require_value(payload: dict[str, object], field_name: str, parent_name: str) -> Any:
    if field_name not in payload:
        raise ValueError(f"{parent_name} muss {field_name} enthalten.")
    return payload[field_name]


def _reject_unknown_keys(payload: dict[str, object], allowed_keys: set[str], field_name: str) -> None:
    unknown_keys = sorted(set(payload) - allowed_keys)
    if unknown_keys:
        raise ValueError(f"{field_name} enthaelt unbekannte Felder: {', '.join(unknown_keys)}.")
