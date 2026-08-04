"""Versionierter Vertrag fuer die fruehe verbindliche VVER-Auswahl.

VVER waehlt nach der Vorpruefung Kandidaten aus, aber noch keine finalen
Varianten. Deshalb enthält dieser Vertrag bewusst weder VAR-IDs noch VCAT-,
VSEL- oder VGEN-Daten. Die spaetere Abbildung auf finale Varianten bleibt ein
eigener Migrationsschritt.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Final, Mapping, Protocol, Sequence

VVER_SELECTION_CONTRACT_VERSION: Final = "1.0"
VVER_SELECTION_RECORD_KIND: Final = "vver_early_selection"
_SHA256_PATTERN: Final = re.compile(r"[0-9a-f]{64}\Z")
_SELECTION_MODES: Final = frozenset({"all", "manual", "random"})


class _CandidateLike(Protocol):
    """Minimaler Kandidatenvertrag; vermeidet eine Kopplung an VCAT."""

    candidate_id: str
    selected_options: Sequence[tuple[str, str]]
    resolved_values: Sequence[object]


@dataclass(frozen=True, slots=True)
class VverCandidateReference:
    """Unveraenderliche VVER-Referenz auf einen vorgeprueften Kandidaten."""

    candidate_id: str
    candidate_fingerprint: str

    def __post_init__(self) -> None:
        _require_text("candidate_id", self.candidate_id)
        _require_sha256("candidate_fingerprint", self.candidate_fingerprint)


@dataclass(frozen=True, slots=True)
class VverSelectionRecord:
    """Fruehe Auswahl vor der Dimensionierung mit vollstaendiger Herkunft."""

    record_kind: str
    contract_version: str
    record_id: str
    study_id: str
    study_case_id: str
    study_direction_id: str
    selection_mode: str
    selection_reason: str
    random_seed: int | None
    pre_dimensioning_upstream_fingerprint: str
    selected_candidates: tuple[VverCandidateReference, ...]
    record_fingerprint: str

    def __post_init__(self) -> None:
        if self.record_kind != VVER_SELECTION_RECORD_KIND:
            raise ValueError("Der Auswahlvertrag ist nur fuer fruehe VVER-Auswahlen gueltig.")
        if self.contract_version != VVER_SELECTION_CONTRACT_VERSION:
            raise ValueError("Die VVER-Auswahlvertragsversion ist nicht unterstuetzt.")
        for field_name, value in (
            ("record_id", self.record_id),
            ("study_id", self.study_id),
            ("study_case_id", self.study_case_id),
            ("study_direction_id", self.study_direction_id),
            ("selection_reason", self.selection_reason),
        ):
            _require_text(field_name, value)
        if self.selection_mode not in _SELECTION_MODES:
            raise ValueError("selection_mode muss 'all', 'manual' oder 'random' sein.")
        if self.selection_mode == "random" and (
            not isinstance(self.random_seed, int) or isinstance(self.random_seed, bool)
        ):
            raise ValueError("Eine zufaellige VVER-Auswahl braucht einen ganzzahligen random_seed.")
        if self.selection_mode != "random" and self.random_seed is not None:
            raise ValueError("random_seed ist nur fuer eine zufaellige VVER-Auswahl erlaubt.")
        _require_sha256("pre_dimensioning_upstream_fingerprint", self.pre_dimensioning_upstream_fingerprint)
        _require_sha256("record_fingerprint", self.record_fingerprint)
        references = tuple(self.selected_candidates)
        if not references:
            raise ValueError("Eine VVER-Auswahl braucht mindestens einen Kandidaten.")
        if len({reference.candidate_id for reference in references}) != len(references):
            raise ValueError("Eine VVER-Auswahl darf keinen Kandidaten mehrfach referenzieren.")
        if tuple(sorted(references, key=lambda reference: reference.candidate_id)) != references:
            raise ValueError("VVER-Kandidatenreferenzen muessen kanonisch nach candidate_id sortiert sein.")
        object.__setattr__(self, "selected_candidates", references)


def candidate_fingerprint(candidate: _CandidateLike) -> str:
    """Bildet einen stabilen Inhaltshash ohne eine finale Varianten-ID zu erzeugen."""
    candidate_id = _require_text("candidate_id", candidate.candidate_id)
    return _fingerprint(
        {
            "candidate_id": candidate_id,
            "selected_options": [list(option) for option in sorted(candidate.selected_options)],
            "resolved_values": sorted(
                (_resolved_value_payload(value) for value in candidate.resolved_values),
                key=lambda value: str(value["parameter_key"]),
            ),
        }
    )


def create_vver_selection_record(
    *,
    study_id: str,
    study_case_id: str,
    study_direction_id: str,
    selection_mode: str,
    selection_reason: str,
    pre_dimensioning_upstream_fingerprint: str,
    selected_candidates: Sequence[_CandidateLike],
    random_seed: int | None = None,
) -> VverSelectionRecord:
    """Erstellt eine kanonische, vor Dimensionierung bindende VVER-Auswahl."""
    references = tuple(
        sorted(
            (
                VverCandidateReference(candidate.candidate_id, candidate_fingerprint(candidate))
                for candidate in selected_candidates
            ),
            key=lambda reference: reference.candidate_id,
        )
    )
    payload = _record_payload(
        study_id=study_id,
        study_case_id=study_case_id,
        study_direction_id=study_direction_id,
        selection_mode=selection_mode,
        selection_reason=selection_reason,
        random_seed=random_seed,
        pre_dimensioning_upstream_fingerprint=pre_dimensioning_upstream_fingerprint,
        selected_candidates=references,
    )
    record_fingerprint = _fingerprint(payload)
    return VverSelectionRecord(
        record_kind=VVER_SELECTION_RECORD_KIND,
        contract_version=VVER_SELECTION_CONTRACT_VERSION,
        record_id=f"VVER-{record_fingerprint[:16]}",
        study_id=study_id,
        study_case_id=study_case_id,
        study_direction_id=study_direction_id,
        selection_mode=selection_mode,
        selection_reason=selection_reason,
        random_seed=random_seed,
        pre_dimensioning_upstream_fingerprint=pre_dimensioning_upstream_fingerprint,
        selected_candidates=references,
        record_fingerprint=record_fingerprint,
    )


def vver_selection_record_to_payload(record: VverSelectionRecord) -> dict[str, object]:
    """Serialisiert den Vertrag vollstaendig und ohne abgeleitete Variantenobjekte."""
    return {
        "record_kind": record.record_kind,
        "contract_version": record.contract_version,
        "record_id": record.record_id,
        "study_id": record.study_id,
        "study_case_id": record.study_case_id,
        "study_direction_id": record.study_direction_id,
        "selection_mode": record.selection_mode,
        "selection_reason": record.selection_reason,
        "random_seed": record.random_seed,
        "pre_dimensioning_upstream_fingerprint": record.pre_dimensioning_upstream_fingerprint,
        "selected_candidates": [
            {"candidate_id": reference.candidate_id, "candidate_fingerprint": reference.candidate_fingerprint}
            for reference in record.selected_candidates
        ],
        "record_fingerprint": record.record_fingerprint,
    }


def vver_selection_record_from_payload(payload: Mapping[str, object]) -> VverSelectionRecord:
    """Parst nur vollstaendige, kanonische und hash-konsistente VVER-Payloads."""
    _require_exact_keys(
        payload,
        {
            "record_kind",
            "contract_version",
            "record_id",
            "study_id",
            "study_case_id",
            "study_direction_id",
            "selection_mode",
            "selection_reason",
            "random_seed",
            "pre_dimensioning_upstream_fingerprint",
            "selected_candidates",
            "record_fingerprint",
        },
        "VVER-Auswahlpayload",
    )
    references_raw = _require_list(payload, "selected_candidates")
    references = tuple(
        VverCandidateReference(
            candidate_id=_require_text(
                "selected_candidates[].candidate_id",
                _candidate_reference_mapping(value).get("candidate_id"),
            ),
            candidate_fingerprint=_require_text(
                "selected_candidates[].candidate_fingerprint",
                _candidate_reference_mapping(value).get("candidate_fingerprint"),
            ),
        )
        for value in references_raw
    )
    record = VverSelectionRecord(
        record_kind=_require_text("record_kind", payload.get("record_kind")),
        contract_version=_require_text("contract_version", payload.get("contract_version")),
        record_id=_require_text("record_id", payload.get("record_id")),
        study_id=_require_text("study_id", payload.get("study_id")),
        study_case_id=_require_text("study_case_id", payload.get("study_case_id")),
        study_direction_id=_require_text("study_direction_id", payload.get("study_direction_id")),
        selection_mode=_require_text("selection_mode", payload.get("selection_mode")),
        selection_reason=_require_text("selection_reason", payload.get("selection_reason")),
        random_seed=_optional_int(payload.get("random_seed"), "random_seed"),
        pre_dimensioning_upstream_fingerprint=_require_text(
            "pre_dimensioning_upstream_fingerprint", payload.get("pre_dimensioning_upstream_fingerprint")
        ),
        selected_candidates=references,
        record_fingerprint=_require_text("record_fingerprint", payload.get("record_fingerprint")),
    )
    expected_fingerprint = _fingerprint(_record_payload_from_record(record))
    if record.record_fingerprint != expected_fingerprint:
        raise ValueError("Der VVER-Auswahlrecord wurde veraendert oder ist inkonsistent.")
    if record.record_id != f"VVER-{record.record_fingerprint[:16]}":
        raise ValueError("Die VVER-Record-ID passt nicht zum Record-Fingerprint.")
    return record


def validate_vver_selection_is_current(
    record: VverSelectionRecord,
    *,
    current_pre_dimensioning_upstream_fingerprint: str,
    current_candidates: Sequence[_CandidateLike],
) -> None:
    """Blockiert eine Auswahl, sobald ihr Upstream- oder Kandidatenstand abweicht."""
    _require_sha256("current_pre_dimensioning_upstream_fingerprint", current_pre_dimensioning_upstream_fingerprint)
    if record.pre_dimensioning_upstream_fingerprint != current_pre_dimensioning_upstream_fingerprint:
        raise ValueError("Die VVER-Auswahl ist gegenueber dem Pre-Dimensioning-Upstream veraltet.")
    current = {candidate.candidate_id: candidate_fingerprint(candidate) for candidate in current_candidates}
    for reference in record.selected_candidates:
        if current.get(reference.candidate_id) != reference.candidate_fingerprint:
            raise ValueError(f"Die VVER-Auswahl ist fuer Kandidat '{reference.candidate_id}' veraltet.")


def _record_payload_from_record(record: VverSelectionRecord) -> dict[str, object]:
    return _record_payload(
        study_id=record.study_id,
        study_case_id=record.study_case_id,
        study_direction_id=record.study_direction_id,
        selection_mode=record.selection_mode,
        selection_reason=record.selection_reason,
        random_seed=record.random_seed,
        pre_dimensioning_upstream_fingerprint=record.pre_dimensioning_upstream_fingerprint,
        selected_candidates=record.selected_candidates,
    )


def _record_payload(**values: object) -> dict[str, object]:
    references = values["selected_candidates"]
    assert isinstance(references, tuple)
    return {
        "record_kind": VVER_SELECTION_RECORD_KIND,
        "contract_version": VVER_SELECTION_CONTRACT_VERSION,
        **values,
        "selected_candidates": [
            {"candidate_id": reference.candidate_id, "candidate_fingerprint": reference.candidate_fingerprint}
            for reference in references
        ],
    }


def _resolved_value_payload(value: object) -> dict[str, object]:
    try:
        return {"parameter_key": value.parameter_key, "value": value.value, "unit": value.unit}
    except AttributeError as error:
        raise ValueError("Ein VVER-Kandidat braucht aufgeloeste Werte mit parameter_key, value und unit.") from error


def _require_text(field_name: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} muss ein nichtleerer Text sein.")
    return value


def _require_sha256(field_name: str, value: str) -> None:
    if not _SHA256_PATTERN.fullmatch(value):
        raise ValueError(f"{field_name} muss ein SHA-256-Hash in Kleinbuchstaben sein.")


def _require_mapping(value: object, field_name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} muss ein Objekt sein.")
    return value


def _candidate_reference_mapping(value: object) -> Mapping[str, object]:
    mapping = _require_mapping(value, "selected_candidates[]")
    _require_exact_keys(mapping, {"candidate_id", "candidate_fingerprint"}, "selected_candidates[]")
    return mapping


def _require_exact_keys(payload: Mapping[str, object], expected_keys: set[str], field_name: str) -> None:
    actual_keys = set(payload)
    if actual_keys != expected_keys:
        unknown = sorted(actual_keys - expected_keys)
        missing = sorted(expected_keys - actual_keys)
        details = []
        if unknown:
            details.append(f"unbekannte Felder: {', '.join(unknown)}")
        if missing:
            details.append(f"fehlende Felder: {', '.join(missing)}")
        raise ValueError(f"{field_name} hat keine exakte Vertragsform ({'; '.join(details)}).")


def _require_list(payload: Mapping[str, object], field_name: str) -> list[object]:
    value = payload.get(field_name)
    if not isinstance(value, list):
        raise ValueError(f"{field_name} muss eine Liste sein.")
    return value


def _optional_int(value: object, field_name: str) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{field_name} muss eine Ganzzahl oder null sein.")
    return value


def _fingerprint(payload: object) -> str:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
