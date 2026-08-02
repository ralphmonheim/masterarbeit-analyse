"""Schmaler, unveraenderlicher Uebergabevertrag fuer freigegebene Technikrevisionen."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ma_validation import ReleaseStatus

from .metadata import ObjectReference, tuple_of_strings
from .revisions import TechnicalModelRevision, _content_hash
from .specification import TechnicalModelSchemaVersion


@dataclass(frozen=True, slots=True)
class ReleasedTechnicalServiceInterfaceReference:
    """Referenzmetadaten eines freigegebenen technischen Serviceinterfaces."""

    interface_id: str
    service_type: str
    medium: str
    compatible_terminal_types: tuple[str, ...]
    source_object_reference: ObjectReference

    def __post_init__(self) -> None:
        object.__setattr__(self, "compatible_terminal_types", tuple(self.compatible_terminal_types))


@dataclass(frozen=True, slots=True)
class ReleasedTechnicalHandover:
    """Referenz-only-Handover einer hashkonsistenten Technikrevision."""

    technical_model_id: str
    revision_id: str
    content_hash: str
    release_status: ReleaseStatus
    service_interface_references: tuple[ReleasedTechnicalServiceInterfaceReference, ...]
    project_id: str = ""
    building_reference: ObjectReference | None = None
    service_interface_references_hash: str = ""
    release_evidence_hash: str = ""
    handover_content_hash: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "service_interface_references", tuple(self.service_interface_references))

    def has_consistent_service_interface_references(self) -> bool:
        """Prueft die unveraenderte Referenzliste des builder-erzeugten Handovers."""
        return bool(self.service_interface_references_hash) and self.service_interface_references_hash == (
            _service_interface_references_hash(self.service_interface_references)
        )

    def has_consistent_handover_content(self) -> bool:
        """Prueft Techniktriple, Projekt, Building und Interfaceprojektion gemeinsam."""
        if not self.handover_content_hash or self.building_reference is None:
            return False
        return self.handover_content_hash == _handover_content_hash(
            technical_model_id=self.technical_model_id,
            revision_id=self.revision_id,
            content_hash=self.content_hash,
            project_id=self.project_id,
            building_reference=self.building_reference,
            service_interface_references_hash=self.service_interface_references_hash,
            release_evidence_hash=self.release_evidence_hash,
        )


def build_released_technical_handover(revision: TechnicalModelRevision) -> ReleasedTechnicalHandover:
    """Erzeugt einen kleinen Handover nur aus einer unveraenderten Freigaberevision.

    Der technische Payload verbleibt in ``TechnicalModelRevision``. Der Handover
    enthaelt ausschliesslich die Revisionsmetadaten und die fuer nachgelagerte
    Module relevanten Serviceinterface- und Quellobjektreferenzen.
    """
    if not isinstance(revision, TechnicalModelRevision):
        raise TypeError("revision muss eine TechnicalModelRevision sein.")
    if revision.release_status is not ReleaseStatus.RELEASED:
        raise ValueError("Nur eine freigegebene Technikrevision darf uebergeben werden.")

    technical_model_id = _required_text(revision.technical_model_id, "technical_model_id")
    revision_id = _required_text(revision.revision_id, "revision_id")
    content_hash = _required_text(revision.content_hash, "content_hash")
    payload = revision.specification_payload
    if not isinstance(payload, dict):
        raise ValueError("Technikrevision enthaelt keine Spezifikationsnutzlast.")
    if content_hash != _content_hash(payload):
        raise ValueError("Content-Hash der Technikrevision stimmt nicht mit der Nutzlast ueberein.")

    payload_model_id = _required_text(payload.get("technical_model_id"), "specification.technical_model_id")
    if payload_model_id != technical_model_id:
        raise ValueError("technical_model_id der Revision stimmt nicht mit der Nutzlast ueberein.")
    payload_schema_version = _required_text(payload.get("schema_version"), "specification.schema_version")
    if payload_schema_version != TechnicalModelSchemaVersion.V2.value:
        raise ValueError("Der Technik-Handover erwartet eine freigegebene v2-Spezifikation.")

    interface_references = tuple(
        sorted(
            (_service_interface_reference(item) for item in _service_interface_payloads(payload)),
            key=_service_interface_sort_key,
        )
    )
    project_id = _required_text(payload.get("project_id"), "specification.project_id")
    building_reference = _object_reference(payload.get("building_reference"), "specification.building_reference")
    if not building_reference.revision_id:
        raise ValueError("specification.building_reference.revision_id darf nicht leer sein.")
    service_interface_references_hash = _service_interface_references_hash(interface_references)
    release_evidence_hash = revision.release_evidence_hash.strip()
    return ReleasedTechnicalHandover(
        technical_model_id=technical_model_id,
        revision_id=revision_id,
        content_hash=content_hash,
        release_status=revision.release_status,
        service_interface_references=interface_references,
        project_id=project_id,
        building_reference=building_reference,
        service_interface_references_hash=service_interface_references_hash,
        release_evidence_hash=release_evidence_hash,
        handover_content_hash=_handover_content_hash(
            technical_model_id=technical_model_id,
            revision_id=revision_id,
            content_hash=content_hash,
            project_id=project_id,
            building_reference=building_reference,
            service_interface_references_hash=service_interface_references_hash,
            release_evidence_hash=release_evidence_hash,
        ),
    )


def _service_interface_payloads(payload: dict[str, object]) -> tuple[Mapping[str, object], ...]:
    interfaces = payload.get("service_interfaces", ())
    if not isinstance(interfaces, list | tuple):
        raise ValueError("service_interfaces der Technikrevision muss eine Liste sein.")
    if not all(isinstance(item, Mapping) for item in interfaces):
        raise ValueError("service_interfaces der Technikrevision darf nur Mapping-Eintraege enthalten.")
    return tuple(interfaces)


def _service_interface_reference(payload: Mapping[str, object]) -> ReleasedTechnicalServiceInterfaceReference:
    interface_id = _required_text(payload.get("interface_id"), "service_interfaces.interface_id")
    source_payload = payload.get("source_system_reference")
    source_object_reference = _object_reference(
        source_payload,
        f"service_interfaces.{interface_id}.source_system_reference",
    )
    terminal_types = payload.get("compatible_terminal_types", ())
    if not isinstance(terminal_types, list | tuple):
        raise ValueError(f"Serviceinterface {interface_id} enthaelt keine gueltige Terminal-Kompatibilitaet.")
    return ReleasedTechnicalServiceInterfaceReference(
        interface_id=interface_id,
        service_type=_required_text(payload.get("service_type"), f"service_interfaces.{interface_id}.service_type"),
        medium=_required_text(payload.get("medium"), f"service_interfaces.{interface_id}.medium"),
        compatible_terminal_types=tuple_of_strings(terminal_types),
        source_object_reference=source_object_reference,
    )


def _service_interface_sort_key(
    reference: ReleasedTechnicalServiceInterfaceReference,
) -> tuple[str, str, str, str, str, str, str, tuple[str, ...]]:
    source = reference.source_object_reference
    return (
        reference.interface_id,
        source.object_id,
        source.revision_id,
        source.content_hash,
        source.object_type,
        reference.service_type,
        reference.medium,
        reference.compatible_terminal_types,
    )


def _service_interface_references_hash(
    references: tuple[ReleasedTechnicalServiceInterfaceReference, ...],
) -> str:
    sorted_references = sorted(references, key=_service_interface_sort_key)
    return _content_hash(
        {
            "service_interface_references": [
                {
                    "interface_id": reference.interface_id,
                    "service_type": reference.service_type,
                    "medium": reference.medium,
                    "compatible_terminal_types": sorted(reference.compatible_terminal_types),
                    "source_object_reference": {
                        "object_id": reference.source_object_reference.object_id,
                        "revision_id": reference.source_object_reference.revision_id,
                        "content_hash": reference.source_object_reference.content_hash,
                        "object_type": reference.source_object_reference.object_type,
                    },
                }
                for reference in sorted_references
            ]
        }
    )


def _handover_content_hash(
    *,
    technical_model_id: str,
    revision_id: str,
    content_hash: str,
    project_id: str,
    building_reference: ObjectReference,
    service_interface_references_hash: str,
    release_evidence_hash: str,
) -> str:
    return _content_hash(
        {
            "technical_model_id": technical_model_id,
            "revision_id": revision_id,
            "content_hash": content_hash,
            "project_id": project_id,
            "building_reference": {
                "object_id": building_reference.object_id,
                "revision_id": building_reference.revision_id,
                "content_hash": building_reference.content_hash,
                "object_type": building_reference.object_type,
            },
            "service_interface_references_hash": service_interface_references_hash,
            "release_evidence_hash": release_evidence_hash,
        }
    )


def _object_reference(value: object, location: str) -> ObjectReference:
    if not isinstance(value, Mapping):
        raise ValueError(f"{location} enthaelt keine Quellobjektreferenz.")
    return ObjectReference(
        object_id=_required_text(value.get("object_id"), f"{location}.object_id"),
        revision_id=_optional_text(value.get("revision_id")),
        content_hash=_optional_text(value.get("content_hash")),
        object_type=_optional_text(value.get("object_type")),
    )


def _required_text(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location} darf nicht leer sein.")
    return value.strip()


def _optional_text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""
