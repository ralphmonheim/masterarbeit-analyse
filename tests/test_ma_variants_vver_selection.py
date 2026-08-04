"""Vertragstests fuer die fruehe Auswahl im VVER-Checkpoint."""

from dataclasses import replace

import pytest

from ma_parameters import (
    build_business_integration_lod1_baseline_parameter_snapshot,
    load_reference_variation_specification,
)
from ma_variants.vver_selection import (
    create_vver_selection_record,
    validate_vver_selection_is_current,
    vver_selection_record_from_payload,
    vver_selection_record_to_payload,
)
from ma_variants.workflow import build_variant_space

UPSTREAM_FINGERPRINT = "a" * 64


def _candidates():
    baseline = build_business_integration_lod1_baseline_parameter_snapshot()
    specification = load_reference_variation_specification(baseline)
    return build_variant_space(baseline, specification)


def _record():
    candidates = _candidates()
    return create_vver_selection_record(
        study_id="STUDY-SMALL-OFFICE-V1",
        study_case_id="CASE-OPT-001",
        study_direction_id="optimization",
        selection_mode="manual",
        selection_reason="Referenzgruppe fuer die nachfolgende Dimensionierung.",
        pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
        selected_candidates=(candidates[1], candidates[0]),
    )


def test_vver_record_is_canonical_and_roundtrips_without_final_variant_objects():
    record = _record()

    assert [reference.candidate_id for reference in record.selected_candidates] == sorted(
        reference.candidate_id for reference in record.selected_candidates
    )
    assert record.record_id == f"VVER-{record.record_fingerprint[:16]}"
    payload = vver_selection_record_to_payload(record)
    assert "catalog_id" not in payload
    assert "variant_ids" not in payload
    assert vver_selection_record_from_payload(payload) == record


def test_vver_record_rejects_tampered_payload_and_stale_upstream():
    record = _record()
    payload = vver_selection_record_to_payload(record)
    payload["selection_reason"] = "Nachtraeglich veraendert"

    with pytest.raises(ValueError, match="veraendert|inkonsistent"):
        vver_selection_record_from_payload(payload)
    with pytest.raises(ValueError, match="Upstream veraltet"):
        validate_vver_selection_is_current(
            record,
            current_pre_dimensioning_upstream_fingerprint="b" * 64,
            current_candidates=_candidates(),
        )


def test_vver_payload_rejects_unknown_or_missing_contract_fields():
    payload = vver_selection_record_to_payload(_record())
    payload["future_extension"] = "not silently accepted"

    with pytest.raises(ValueError, match="exakte Vertragsform"):
        vver_selection_record_from_payload(payload)


def test_vver_record_rejects_stale_candidate_and_non_random_seed():
    record = _record()
    candidates = list(_candidates())
    candidates[0] = replace(candidates[0], selected_options=(("changed", "option"),))

    with pytest.raises(ValueError, match="Kandidat.*veraltet"):
        validate_vver_selection_is_current(
            record,
            current_pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
            current_candidates=candidates,
        )
    with pytest.raises(ValueError, match="random_seed"):
        create_vver_selection_record(
            study_id="study",
            study_case_id="case",
            study_direction_id="direction",
            selection_mode="manual",
            selection_reason="Begruendung",
            pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
            selected_candidates=(_candidates()[0],),
            random_seed=4,
        )
