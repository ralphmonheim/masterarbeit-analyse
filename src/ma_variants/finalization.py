"""Finale VCAT-/VSEL-Vertraege nach VVER und Dimensionierung.

Dieses Modul beginnt erst nach der owner-seitigen Dimensionierung. Es vergibt
VAR-IDs deshalb ausschliesslich beim finalen Variantenkatalog und bildet die
fruehe VVER-Auswahl ohne erneute Auswahlentscheidung darauf ab.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, replace
from typing import Mapping, Sequence

from ma_dimensionierung import VariantDimensioningAssignment

from .preprocess import PreprocessVariant
from .vver_selection import VverSelectionRecord

FINAL_VARIANT_CATALOG_CONTRACT_VERSION = "1.0"
FINAL_VARIANT_CATALOG_KIND = "vcat_final"
FINAL_VARIANT_SELECTION_KIND = "vsel_vver_mapping"
_VARIANT_ID_PATTERN = re.compile(r"VAR-(\d{6})\Z")


@dataclass(frozen=True, slots=True)
class VariantIdRegistry:
    """Projektweite, append-only fortgeschriebene VAR-ID-Zuordnung."""

    project_id: str
    next_variant_number: int
    content_fingerprint_to_variant_id: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.project_id.strip() or self.next_variant_number < 1:
            raise ValueError("Die VAR-ID-Registry ist unvollstaendig.")
        mapping = tuple(sorted(self.content_fingerprint_to_variant_id))
        if len({item[0] for item in mapping}) != len(mapping):
            raise ValueError("Ein Varianteninhalt darf nur einer VAR-ID zugeordnet sein.")
        if len({item[1] for item in mapping}) != len(mapping):
            raise ValueError("Eine VAR-ID darf nicht mehreren Varianteninhalten zugeordnet sein.")
        for fingerprint, variant_id in mapping:
            if not _is_fingerprint(fingerprint) or not _VARIANT_ID_PATTERN.fullmatch(variant_id):
                raise ValueError("Die VAR-ID-Registry enthaelt einen ungueltigen Eintrag.")
        object.__setattr__(self, "content_fingerprint_to_variant_id", mapping)


@dataclass(frozen=True, slots=True)
class FinalVariantCatalogEntry:
    """Nachgerechnete Variante mit finaler, projektweiter Identitaet."""

    candidate_id: str
    candidate_fingerprint: str
    variant_id: str
    variant_content_fingerprint: str
    dimensioning_result_fingerprint: str


@dataclass(frozen=True, slots=True)
class FinalVariantCatalog:
    """Finaler Katalog: erst hier existieren VAR-IDs."""

    catalog_id: str
    catalog_fingerprint: str
    project_id: str
    vver_record_id: str
    vver_record_fingerprint: str
    entries: tuple[FinalVariantCatalogEntry, ...]


@dataclass(frozen=True, slots=True)
class VselVverMapping:
    """Deterministische Abbildung der VVER-Auswahl auf finale VAR-IDs."""

    selection_id: str
    selection_fingerprint: str
    catalog_id: str
    catalog_fingerprint: str
    vver_record_id: str
    vver_record_fingerprint: str
    candidate_to_variant_ids: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class FinalizationResult:
    """Atomar zu persistierende Registry sowie finaler VCAT und VSEL."""

    registry: VariantIdRegistry
    catalog: FinalVariantCatalog
    selection: VselVverMapping


def generate_final_variants(
    catalog: FinalVariantCatalog,
    pre_dimensioning_variants: Mapping[str, PreprocessVariant],
) -> dict[str, PreprocessVariant]:
    """VGEN: bindet erst nach VCAT die finalen VAR-IDs an Fachvarianten."""
    expected = {entry.candidate_id for entry in catalog.entries}
    if set(pre_dimensioning_variants) != expected:
        raise ValueError("VGEN braucht genau die im finalen VCAT enthaltenen Kandidaten.")
    return {
        entry.candidate_id: replace(
            pre_dimensioning_variants[entry.candidate_id],
            variant_id=entry.variant_id,
            fingerprint="",
            content_fingerprint=entry.variant_content_fingerprint,
        )
        for entry in catalog.entries
    }


def finalize_vver_dimensioning(
    *,
    project_id: str,
    vver_selection: VverSelectionRecord,
    candidates: Sequence[Mapping[str, object]],
    assignments: Sequence[VariantDimensioningAssignment],
    registry: VariantIdRegistry | None = None,
) -> FinalizationResult:
    """Prueft VVER-Auftraege nach und erzeugt finalen VCAT, VSEL und VAR-IDs."""
    if not project_id.strip():
        raise ValueError("project_id darf nicht leer sein.")
    active_registry = registry or VariantIdRegistry(project_id=project_id, next_variant_number=1)
    if active_registry.project_id != project_id:
        raise ValueError("Die VAR-ID-Registry gehoert zu einem anderen Projekt.")

    rows_by_id = {str(row.get("candidate_id", "")): row for row in candidates}
    assignment_by_id = {assignment.candidate_id: assignment for assignment in assignments}
    if len(assignment_by_id) != len(assignments):
        raise ValueError("Ein VVER-Kandidat besitzt mehrere Dimensionierungsergebnisse.")

    entries: list[FinalVariantCatalogEntry] = []
    mapping = dict(active_registry.content_fingerprint_to_variant_id)
    next_number = active_registry.next_variant_number
    for reference in vver_selection.selected_candidates:
        row = rows_by_id.get(reference.candidate_id)
        assignment = assignment_by_id.pop(reference.candidate_id, None)
        if row is None or assignment is None:
            raise ValueError("Jeder VVER-Kandidat braucht genau ein aktuelles Dimensionierungsergebnis.")
        if _candidate_fingerprint(row) != reference.candidate_fingerprint:
            raise ValueError("Ein Kandidat weicht von seiner verbindlichen VVER-Referenz ab.")
        _validate_assignment(assignment, vver_selection)
        content_fingerprint = _variant_content_fingerprint(row, assignment)
        variant_id = mapping.get(content_fingerprint)
        if variant_id is None:
            variant_id = f"VAR-{next_number:06d}"
            mapping[content_fingerprint] = variant_id
            next_number += 1
        entries.append(
            FinalVariantCatalogEntry(
                candidate_id=reference.candidate_id,
                candidate_fingerprint=reference.candidate_fingerprint,
                variant_id=variant_id,
                variant_content_fingerprint=content_fingerprint,
                dimensioning_result_fingerprint=assignment.result_fingerprint,
            )
        )
    if assignment_by_id:
        raise ValueError("Dimensionierungsergebnisse ausserhalb der verbindlichen VVER-Auswahl sind unzulaessig.")

    ordered_entries = tuple(sorted(entries, key=lambda entry: entry.candidate_id))
    catalog_fingerprint = _fingerprint(
        {
            "contract_version": FINAL_VARIANT_CATALOG_CONTRACT_VERSION,
            "project_id": project_id,
            "vver_record_fingerprint": vver_selection.record_fingerprint,
            "entries": [_entry_payload(entry) for entry in ordered_entries],
        }
    )
    catalog = FinalVariantCatalog(
        catalog_id=f"VCAT-{catalog_fingerprint[:16]}",
        catalog_fingerprint=catalog_fingerprint,
        project_id=project_id,
        vver_record_id=vver_selection.record_id,
        vver_record_fingerprint=vver_selection.record_fingerprint,
        entries=ordered_entries,
    )
    candidate_to_variant_ids = tuple((entry.candidate_id, entry.variant_id) for entry in ordered_entries)
    selection_fingerprint = _fingerprint(
        {
            "contract_version": FINAL_VARIANT_CATALOG_CONTRACT_VERSION,
            "catalog_fingerprint": catalog.catalog_fingerprint,
            "vver_record_fingerprint": vver_selection.record_fingerprint,
            "candidate_to_variant_ids": [list(item) for item in candidate_to_variant_ids],
        }
    )
    selection = VselVverMapping(
        selection_id=f"VSEL-{selection_fingerprint[:16]}",
        selection_fingerprint=selection_fingerprint,
        catalog_id=catalog.catalog_id,
        catalog_fingerprint=catalog.catalog_fingerprint,
        vver_record_id=vver_selection.record_id,
        vver_record_fingerprint=vver_selection.record_fingerprint,
        candidate_to_variant_ids=candidate_to_variant_ids,
    )
    return FinalizationResult(
        registry=VariantIdRegistry(
            project_id=project_id,
            next_variant_number=next_number,
            content_fingerprint_to_variant_id=tuple(mapping.items()),
        ),
        catalog=catalog,
        selection=selection,
    )


def _validate_assignment(assignment: VariantDimensioningAssignment, record: VverSelectionRecord) -> None:
    if assignment.vver_record_id != record.record_id or assignment.vver_record_fingerprint != record.record_fingerprint:
        raise ValueError("Das Dimensionierungsergebnis gehoert nicht zur aktuellen VVER-Auswahl.")
    if not assignment.gateway_method_id or not assignment.gateway_method_version:
        raise ValueError("Dem Dimensionierungsergebnis fehlt die Gateway-Methodenprovenienz.")
    if not _is_fingerprint(assignment.gateway_result_fingerprint) or not _is_fingerprint(assignment.result_fingerprint):
        raise ValueError("Dem Dimensionierungsergebnis fehlt ein gueltiger Ergebnisfingerprint.")
    for value in (
        assignment.heating_load_w,
        assignment.cooling_load_w,
        assignment.heating_capacity_w,
        assignment.cooling_capacity_w,
    ):
        if not math.isfinite(value) or value < 0:
            raise ValueError("Dimensionierungsergebnisse muessen endliche, nichtnegative Werte sein.")


def _candidate_fingerprint(row: Mapping[str, object]) -> str:
    values = row.get("values")
    if not isinstance(values, Mapping):
        raise ValueError("Ein finalisierter Kandidat braucht ein Werteobjekt.")
    return _fingerprint(
        {
            "candidate_id": str(row.get("candidate_id", "")),
            "selected_options": [list(item) for item in sorted((str(key), str(value)) for key, value in values.items())],
            "resolved_values": [
                {"parameter_key": str(key), "value": value, "unit": ""}
                for key, value in sorted(values.items())
            ],
        }
    )


def _variant_content_fingerprint(
    row: Mapping[str, object], assignment: VariantDimensioningAssignment
) -> str:
    """Hash ohne Kandidaten-, Katalog- oder VAR-ID fuer projektweite Wiederverwendung."""
    values = row.get("values")
    assert isinstance(values, Mapping)
    return _fingerprint(
        {
            "candidate_values": {str(key): value for key, value in sorted(values.items())},
            "dimensioning": {
                "method_id": assignment.gateway_method_id,
                "method_version": assignment.gateway_method_version,
                "input_fingerprint": assignment.dimensioning_input_fingerprint,
                "gateway_result_fingerprint": assignment.gateway_result_fingerprint,
                "heating_capacity_w": assignment.heating_capacity_w,
                "cooling_capacity_w": assignment.cooling_capacity_w,
            },
        }
    )


def _entry_payload(entry: FinalVariantCatalogEntry) -> dict[str, str]:
    return {
        "candidate_id": entry.candidate_id,
        "candidate_fingerprint": entry.candidate_fingerprint,
        "variant_id": entry.variant_id,
        "variant_content_fingerprint": entry.variant_content_fingerprint,
        "dimensioning_result_fingerprint": entry.dimensioning_result_fingerprint,
    }


def _is_fingerprint(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value))


def _fingerprint(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()
