"""VVER-gebundene LoD-1-Dimensionierungsauftraege fuer Variantenstudien.

Die Variantenfachlichkeit liefert nur Kandidaten und die fruehe Auswahl. Dieses
Modul bildet daraus gruppierte LoD-1-Auftraege, berechnet Lasten und leitet
erst hieraus die absoluten Kapazitaeten ab. Es erzeugt bewusst weder VAR-IDs
noch Katalog- oder Simulationsobjekte.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, replace
from typing import Mapping, Protocol, Sequence

from ma_parameters import ParameterSnapshot

from .gateway import execute_lod1_reference_dimensioning, prepare_lod1_reference_dimensioning_request


class VverSelectionLike(Protocol):
    """Schmaler Eingangsvertrag ohne Abhaengigkeit vom Varianten-Owner."""

    record_id: str
    record_fingerprint: str
    pre_dimensioning_upstream_fingerprint: str
    selected_candidates: Sequence[object]


@dataclass(frozen=True, slots=True)
class VariantDimensioningRequest:
    """Ein gruppierter Auftrag ohne finale Variantenidentitaet."""

    dimensioning_input_fingerprint: str
    vver_record_id: str
    vver_record_fingerprint: str
    snapshot: ParameterSnapshot
    candidate_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class VariantDimensioningAssignment:
    """Owner-seitig abgeleitete Lasten und Kapazitaeten eines VVER-Kandidaten."""

    candidate_id: str
    vver_record_id: str
    vver_record_fingerprint: str
    dimensioning_input_fingerprint: str
    gateway_method_id: str
    gateway_method_version: str
    gateway_result_fingerprint: str
    heating_load_w: float
    cooling_load_w: float
    heating_capacity_w: float
    cooling_capacity_w: float
    result_fingerprint: str


def build_vver_selected_lod1_requests(
    snapshot: ParameterSnapshot,
    record: VverSelectionLike,
    candidates: Sequence[Mapping[str, object]],
    *,
    current_pre_dimensioning_upstream_fingerprint: str,
) -> tuple[VariantDimensioningRequest, ...]:
    """Erstellt nur fuer die aktuelle VVER-Auswahl kanonische Lastgruppen."""
    _validate_vver_selection(record, candidates, current_pre_dimensioning_upstream_fingerprint)
    rows_by_id = {str(row["candidate_id"]): row for row in candidates}
    selected = tuple(rows_by_id[reference.candidate_id] for reference in record.selected_candidates)
    groups: dict[str, tuple[ParameterSnapshot, list[str]]] = {}
    for row in selected:
        candidate_snapshot = _snapshot_for_candidate(snapshot, row)
        preparation = prepare_lod1_reference_dimensioning_request(candidate_snapshot)
        if preparation.request is None:
            raise ValueError("Ein VVER-Kandidat ergibt keinen gueltigen LoD-1-Dimensionierungsauftrag.")
        fingerprint = preparation.request.input_fingerprint
        if fingerprint not in groups:
            groups[fingerprint] = (candidate_snapshot, [])
        groups[fingerprint][1].append(str(row["candidate_id"]))
    return tuple(
        VariantDimensioningRequest(
            dimensioning_input_fingerprint=fingerprint,
            vver_record_id=record.record_id,
            vver_record_fingerprint=record.record_fingerprint,
            snapshot=group_snapshot,
            candidate_ids=tuple(sorted(candidate_ids)),
        )
        for fingerprint, (group_snapshot, candidate_ids) in sorted(groups.items())
    )


def execute_vver_selected_lod1_requests(
    requests: Sequence[VariantDimensioningRequest],
    candidates: Sequence[Mapping[str, object]],
) -> tuple[VariantDimensioningAssignment, ...]:
    """Berechnet gruppiert und weist Kapazitaeten nur den VVER-Kandidaten zu."""
    rows_by_id = {str(row["candidate_id"]): row for row in candidates}
    assignments: list[VariantDimensioningAssignment] = []
    for request in requests:
        preparation = prepare_lod1_reference_dimensioning_request(request.snapshot)
        if preparation.request is None or preparation.request.input_fingerprint != request.dimensioning_input_fingerprint:
            raise ValueError("Der gruppierte Dimensionierungsauftrag ist nicht mehr aktuell.")
        execution = execute_lod1_reference_dimensioning(preparation.request)
        result = execution.result
        if result.heating_total_load_w is None or result.cooling_internal_load_w is None:
            raise ValueError("Die gruppierte LoD-1-Berechnung lieferte keine vollstaendigen Lasten.")
        for candidate_id in request.candidate_ids:
            factor = _capacity_factor(rows_by_id[candidate_id])
            assignments.append(
                VariantDimensioningAssignment(
                    candidate_id=candidate_id,
                    vver_record_id=request.vver_record_id,
                    vver_record_fingerprint=request.vver_record_fingerprint,
                    dimensioning_input_fingerprint=request.dimensioning_input_fingerprint,
                    gateway_method_id=execution.request.method_id,
                    gateway_method_version=execution.request.method_version,
                    gateway_result_fingerprint=execution.result_fingerprint,
                    heating_load_w=result.heating_total_load_w,
                    cooling_load_w=result.cooling_internal_load_w,
                    heating_capacity_w=round(result.heating_total_load_w * factor, 2),
                    cooling_capacity_w=round(result.cooling_internal_load_w * factor, 2),
                    result_fingerprint=_fingerprint({
                        "gateway_result_fingerprint": execution.result_fingerprint,
                        "candidate_id": candidate_id,
                        "capacity_factor": factor,
                    }),
                )
            )
    return tuple(sorted(assignments, key=lambda item: item.candidate_id))


@dataclass(frozen=True, slots=True)
class _ResolvedValue:
    parameter_key: str
    value: object
    unit: str = ""


@dataclass(frozen=True, slots=True)
class _Candidate:
    candidate_id: str
    selected_options: tuple[tuple[str, str], ...]
    resolved_values: tuple[_ResolvedValue, ...]


def _candidate_model(row: Mapping[str, object]) -> _Candidate:
    values = _values(row)
    return _Candidate(
        candidate_id=str(row["candidate_id"]),
        selected_options=tuple(sorted((str(key), str(value)) for key, value in values.items())),
        resolved_values=tuple(_ResolvedValue(str(key), value) for key, value in sorted(values.items())),
    )


def _validate_vver_selection(
    record: VverSelectionLike,
    candidates: Sequence[Mapping[str, object]],
    current_pre_dimensioning_upstream_fingerprint: str,
) -> None:
    """Prueft die VVER-Referenzen lokal, ohne deren Owner-Modul zu importieren."""
    if record.pre_dimensioning_upstream_fingerprint != current_pre_dimensioning_upstream_fingerprint:
        raise ValueError("Die VVER-Auswahl ist gegenueber dem Pre-Dimensioning-Upstream veraltet.")
    rows_by_id = {str(row["candidate_id"]): row for row in candidates}
    for reference in record.selected_candidates:
        candidate_id = str(getattr(reference, "candidate_id", ""))
        expected = str(getattr(reference, "candidate_fingerprint", ""))
        row = rows_by_id.get(candidate_id)
        if row is None or _candidate_fingerprint(_candidate_model(row)) != expected:
            raise ValueError(f"Die VVER-Auswahl ist fuer Kandidat '{candidate_id}' nicht aktuell.")


def _candidate_fingerprint(candidate: _Candidate) -> str:
    return _fingerprint(
        {
            "candidate_id": candidate.candidate_id,
            "selected_options": [list(option) for option in sorted(candidate.selected_options)],
            "resolved_values": [
                {"parameter_key": value.parameter_key, "value": value.value, "unit": value.unit}
                for value in sorted(candidate.resolved_values, key=lambda value: value.parameter_key)
            ],
        }
    )


def _snapshot_for_candidate(snapshot: ParameterSnapshot, row: Mapping[str, object]) -> ParameterSnapshot:
    values = _values(row)
    heating = _finite_number(values.get("heating_setpoint_c"), "heating_setpoint_c")
    cooling = _finite_number(values.get("cooling_setpoint_c"), "cooling_setpoint_c")
    if heating >= cooling:
        raise ValueError("Ein Dimensionierungskandidat braucht einen Heizsollwert unter dem Kuehlsollwert.")
    changed = tuple(
        replace(value, value=heating if value.parameter_key.endswith(".heating_setpoint_c") else cooling)
        if value.parameter_key.endswith((".heating_setpoint_c", ".cooling_setpoint_c"))
        else value
        for value in snapshot.values
    )
    if sum(value.parameter_key.endswith(".heating_setpoint_c") for value in changed) != 5:
        raise ValueError("Die SmallOffice-V1-Dimensionierung erwartet genau fuenf Heizzonen.")
    return replace(snapshot, values=changed)


def _capacity_factor(row: Mapping[str, object]) -> float:
    values = _values(row)
    heating = _finite_number(values.get("heating_factor"), "heating_factor")
    cooling = _finite_number(values.get("cooling_factor"), "cooling_factor")
    if heating != cooling:
        raise ValueError("Der SmallOffice-V1-Auftrag verlangt gekoppelte Heiz- und Kuehlfaktoren.")
    return heating


def _values(row: Mapping[str, object]) -> Mapping[str, object]:
    values = row.get("values")
    if not isinstance(values, Mapping):
        raise ValueError("Ein VVER-Kandidat braucht ein Werteobjekt.")
    return values


def _finite_number(value: object, name: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise ValueError(f"{name} muss eine Zahl sein.")
    numeric_value = float(value)
    if not math.isfinite(numeric_value):
        raise ValueError(f"{name} muss eine endliche Zahl sein.")
    return numeric_value


def _fingerprint(payload: object) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()
