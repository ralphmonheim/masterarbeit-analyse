"""Payload-Adapter fuer die atomare Ablage von Registry, VCAT und VSEL.

Der Adapter bleibt beim Varianten-Owner. Die Workspace-Schicht speichert den
von ihm gelieferten Payload anschliessend atomar, ohne selbst VAR-IDs zu
vergeben oder Fachvertraege zu interpretieren.
"""

from __future__ import annotations

from typing import Mapping

from .finalization import FinalizationResult, VariantIdRegistry


def finalization_result_to_payload(
    payload: Mapping[str, object], result: FinalizationResult
) -> dict[str, object]:
    """Schreibt append-only Historien und aktive Referenzen in einen Payload."""
    updated = dict(payload)
    updated["variant_id_registry"] = _registry_payload(result.registry)
    updated["final_catalogs"] = _append_by_id(
        updated.get("final_catalogs"), result.catalog.catalog_id, _catalog_payload(result)
    )
    updated["vsel_records"] = _append_by_id(
        updated.get("vsel_records"), result.selection.selection_id, _selection_payload(result)
    )
    updated["active_final_catalog_id"] = result.catalog.catalog_id
    updated["active_vsel_id"] = result.selection.selection_id
    return updated


def variant_id_registry_from_payload(
    payload: Mapping[str, object], *, project_id: str
) -> VariantIdRegistry:
    """Liest die Registry; ein leerer Bestand beginnt bewusst bei VAR-000001."""
    raw = payload.get("variant_id_registry")
    if raw is None:
        return VariantIdRegistry(project_id=project_id, next_variant_number=1)
    if not isinstance(raw, Mapping):
        raise ValueError("variant_id_registry muss ein Objekt sein.")
    mappings = raw.get("content_fingerprint_to_variant_id")
    if not isinstance(mappings, list):
        raise ValueError("Die VAR-ID-Registry braucht eine Zuordnungsliste.")
    entries: list[tuple[str, str]] = []
    for item in mappings:
        if not isinstance(item, Mapping):
            raise ValueError("Ein VAR-ID-Registry-Eintrag muss ein Objekt sein.")
        fingerprint = item.get("content_fingerprint")
        variant_id = item.get("variant_id")
        if not isinstance(fingerprint, str) or not isinstance(variant_id, str):
            raise ValueError("Ein VAR-ID-Registry-Eintrag ist unvollstaendig.")
        entries.append((fingerprint, variant_id))
    return VariantIdRegistry(
        project_id=_text(raw.get("project_id"), "variant_id_registry.project_id"),
        next_variant_number=_positive_int(raw.get("next_variant_number")),
        content_fingerprint_to_variant_id=tuple(entries),
    )


def _registry_payload(registry: VariantIdRegistry) -> dict[str, object]:
    return {
        "project_id": registry.project_id,
        "next_variant_number": registry.next_variant_number,
        "content_fingerprint_to_variant_id": [
            {"content_fingerprint": fingerprint, "variant_id": variant_id}
            for fingerprint, variant_id in registry.content_fingerprint_to_variant_id
        ],
    }


def _catalog_payload(result: FinalizationResult) -> dict[str, object]:
    catalog = result.catalog
    return {
        "catalog_id": catalog.catalog_id,
        "catalog_fingerprint": catalog.catalog_fingerprint,
        "project_id": catalog.project_id,
        "vver_record_id": catalog.vver_record_id,
        "vver_record_fingerprint": catalog.vver_record_fingerprint,
        "entries": [
            {
                "candidate_id": entry.candidate_id,
                "candidate_fingerprint": entry.candidate_fingerprint,
                "variant_id": entry.variant_id,
                "variant_content_fingerprint": entry.variant_content_fingerprint,
                "dimensioning_result_fingerprint": entry.dimensioning_result_fingerprint,
            }
            for entry in catalog.entries
        ],
    }


def _selection_payload(result: FinalizationResult) -> dict[str, object]:
    selection = result.selection
    return {
        "selection_id": selection.selection_id,
        "selection_fingerprint": selection.selection_fingerprint,
        "catalog_id": selection.catalog_id,
        "catalog_fingerprint": selection.catalog_fingerprint,
        "vver_record_id": selection.vver_record_id,
        "vver_record_fingerprint": selection.vver_record_fingerprint,
        "candidate_to_variant_ids": [
            {"candidate_id": candidate_id, "variant_id": variant_id}
            for candidate_id, variant_id in selection.candidate_to_variant_ids
        ],
    }


def _append_by_id(raw: object, item_id: str, item: dict[str, object]) -> list[object]:
    history = list(raw) if isinstance(raw, list) else []
    retained = [entry for entry in history if not isinstance(entry, Mapping) or entry.get("catalog_id", entry.get("selection_id")) != item_id]
    retained.append(item)
    return retained


def _text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} muss ein nichtleerer Text sein.")
    return value


def _positive_int(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError("next_variant_number muss eine positive Ganzzahl sein.")
    return value
