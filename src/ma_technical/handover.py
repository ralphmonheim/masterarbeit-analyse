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

    def __post_init__(self) -> None:
        object.__setattr__(self, "service_interface_references", tuple(self.service_interface_references))


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
    return ReleasedTechnicalHandover(
        technical_model_id=technical_model_id,
        revision_id=revision_id,
        content_hash=content_hash,
        release_status=revision.release_status,
        service_interface_references=interface_references,
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
    if not isinstance(source_payload, Mapping):
        raise ValueError(f"Serviceinterface {interface_id} enthaelt keine Quellobjektreferenz.")
    source_object_reference = ObjectReference(
        object_id=_required_text(
            source_payload.get("object_id"),
            f"service_interfaces.{interface_id}.source_system_reference.object_id",
        ),
        revision_id=_optional_text(source_payload.get("revision_id")),
        content_hash=_optional_text(source_payload.get("content_hash")),
        object_type=_optional_text(source_payload.get("object_type")),
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


def _required_text(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location} darf nicht leer sein.")
    return value.strip()


def _optional_text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""
