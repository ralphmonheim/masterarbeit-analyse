"""Kleine, explizite Varianten fuer den Preprocess-V1-Durchstich."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from ma_parameters import BaselineParameterSnapshot


@dataclass(frozen=True, slots=True)
class VariationValue:
    """Eine bewusst explizite Aenderung gegenueber der Baseline."""

    parameter_key: str
    value: object
    unit: str


@dataclass(frozen=True, slots=True)
class PreprocessVariant:
    """Vollstaendige, reproduzierbare Variante fuer P018."""

    variant_id: str
    label: str
    baseline_snapshot_id: str
    baseline_content_hash: str
    values: tuple[VariationValue, ...] = ()
    fingerprint: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", tuple(self.values))
        if not self.fingerprint:
            object.__setattr__(self, "fingerprint", _fingerprint(self))


def build_baseline_variant(snapshot: BaselineParameterSnapshot) -> PreprocessVariant:
    """Erzeugt die unveraenderte Referenzvariante."""
    return PreprocessVariant(
        variant_id="VAR-BASELINE",
        label="Baseline",
        baseline_snapshot_id=snapshot.snapshot_id,
        baseline_content_hash=snapshot.content_hash,
    )


def build_explicit_variant(
    snapshot: BaselineParameterSnapshot,
    *,
    variant_id: str,
    label: str,
    values: tuple[VariationValue, ...],
) -> PreprocessVariant:
    """Erzeugt eine kleine, vollstaendig dokumentierte Studienvariante."""
    if not values:
        raise ValueError("Eine Studienvariante benoetigt mindestens eine explizite Aenderung.")
    if len({value.parameter_key for value in values}) != len(values):
        raise ValueError("Eine Variantenstudie darf einen Parameter nur einmal aendern.")
    return PreprocessVariant(
        variant_id=variant_id,
        label=label,
        baseline_snapshot_id=snapshot.snapshot_id,
        baseline_content_hash=snapshot.content_hash,
        values=values,
    )


def _fingerprint(variant: PreprocessVariant) -> str:
    payload = {
        "variant_id": variant.variant_id,
        "baseline_snapshot_id": variant.baseline_snapshot_id,
        "baseline_content_hash": variant.baseline_content_hash,
        "values": [
            {"parameter_key": value.parameter_key, "value": value.value, "unit": value.unit}
            for value in sorted(variant.values, key=lambda item: item.parameter_key)
        ],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()
