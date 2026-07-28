"""Inhaltsfingerprints fuer fachlich relevante Parameterstaende."""

from __future__ import annotations

import hashlib
import json


def reference_dimensioning_parameter_fingerprint(
    baseline,
    parameter_payload: dict[str, object],
) -> str:
    """Bindet IDA-Lasten nur an den dimensionierungsrelevanten Referenzstand."""
    contract = {
        "baseline_snapshot_id": baseline.snapshot_id,
        "baseline_snapshot_version": baseline.snapshot_version,
        "baseline_content_hash": baseline.content_hash,
        "project_reference": parameter_payload.get("reference"),
    }
    serialized = json.dumps(contract, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def variation_specification_source_fingerprint(
    baseline,
    *,
    rules: object,
    variation_spans: object,
    study_contract: object,
) -> str:
    """Bindet den bestaetigten Variationsvertrag an Baseline und Projektregeln."""
    contract = {
        "baseline_snapshot_id": baseline.snapshot_id,
        "baseline_snapshot_version": baseline.snapshot_version,
        "baseline_content_hash": baseline.content_hash,
        "rules": rules,
        "variation_spans": variation_spans,
        "study_contract": study_contract,
    }
    serialized = json.dumps(contract, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
