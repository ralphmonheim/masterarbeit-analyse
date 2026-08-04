"""Fokussierte UI-nahe Tests fuer den VVER-Checkpoint vor der Dimensionierung."""

import pytest

from ma_ui.streamlit_app.pages.variants import (
    _active_vver_selection,
    _dimensioning_is_bound_to_vver,
    _pre_dimensioning_candidates_are_current,
    _selected_candidate_rows,
    _store_vver_selection,
    _vver_candidate_from_row,
    _vver_history_error,
    _vver_selection_is_saveable,
    active_current_vver_selection,
)
from ma_variants.vver_selection import create_vver_selection_record

UPSTREAM_FINGERPRINT = "a" * 64


def _candidate_row(candidate_id: str = "OPT-SB01-F100") -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "study_case_id": "SC-OPT-SMALLOFFICE-5Z",
        "study_direction_id": "SD-OPTIMIZATION",
        "values": {
            "heating_setpoint_c": 21.0,
            "cooling_setpoint_c": 24.0,
            "heating_factor": 1.0,
            "cooling_factor": 1.0,
        },
    }


def test_vver_ui_persists_active_record_without_catalog_or_final_variant_ids() -> None:
    record = create_vver_selection_record(
        study_id="STUDY-SMALL-OFFICE-V1",
        study_case_id="SC-OPT-SMALLOFFICE-5Z",
        study_direction_id="SD-OPTIMIZATION",
        selection_mode="manual",
        selection_reason="Referenzgruppe fuer die Dimensionierung.",
        pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
        selected_candidates=(_vver_candidate_from_row(_candidate_row()),),
    )

    updated = _store_vver_selection({"candidates": [_candidate_row()]}, record)

    assert updated["active_vver_selection_id"] == record.record_id
    assert _active_vver_selection(updated) == record
    stored = updated["vver_selections"][0]
    assert "catalog_id" not in stored
    assert "variant_id" not in stored
    assert "variant_packages" not in updated


def test_vver_ui_replaces_same_record_id_instead_of_duplicating_it() -> None:
    candidate = _vver_candidate_from_row(_candidate_row())
    record = create_vver_selection_record(
        study_id="STUDY-SMALL-OFFICE-V1",
        study_case_id="SC-OPT-SMALLOFFICE-5Z",
        study_direction_id="SD-OPTIMIZATION",
        selection_mode="all",
        selection_reason="Alle Kandidaten der Referenzgruppe.",
        pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
        selected_candidates=(candidate,),
    )

    first = _store_vver_selection({}, record)
    second = _store_vver_selection(first, record)

    assert len(second["vver_selections"]) == 1
    assert second["active_vver_selection_id"] == record.record_id


def test_random_vver_selection_requires_a_seed_before_it_can_be_saved() -> None:
    assert not _vver_selection_is_saveable("zufaellig", None)
    assert _vver_selection_is_saveable("zufaellig", 42)
    assert _vver_selection_is_saveable("manuell", None)


def test_active_current_vver_selection_requires_matching_upstream_and_candidates() -> None:
    record = create_vver_selection_record(
        study_id="STUDY-SMALL-OFFICE-V1",
        study_case_id="SC-OPT-SMALLOFFICE-5Z",
        study_direction_id="SD-OPTIMIZATION",
        selection_mode="manual",
        selection_reason="Referenzgruppe fuer die Dimensionierung.",
        pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
        selected_candidates=(_vver_candidate_from_row(_candidate_row()),),
    )
    payload = _store_vver_selection({"candidates": [_candidate_row()]}, record)

    assert active_current_vver_selection(
        payload,
        study_id="STUDY-SMALL-OFFICE-V1",
        current_pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
    ) == record
    assert active_current_vver_selection(
        payload,
        study_id="STUDY-SMALL-OFFICE-V1",
        current_pre_dimensioning_upstream_fingerprint="b" * 64,
    ) is None


def test_dimensioning_binding_requires_the_current_vver_record() -> None:
    record = create_vver_selection_record(
        study_id="STUDY-SMALL-OFFICE-V1",
        study_case_id="SC-OPT-SMALLOFFICE-5Z",
        study_direction_id="SD-OPTIMIZATION",
        selection_mode="manual",
        selection_reason="Referenzgruppe fuer die Dimensionierung.",
        pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
        selected_candidates=(_vver_candidate_from_row(_candidate_row()),),
    )
    payload = {
        "vver_selection_reference": {
            "record_id": record.record_id,
            "record_fingerprint": record.record_fingerprint,
        }
    }

    assert _dimensioning_is_bound_to_vver(payload, record)
    payload["vver_selection_reference"]["record_fingerprint"] = "other"
    assert not _dimensioning_is_bound_to_vver(payload, record)


def test_final_catalog_candidate_source_is_limited_to_vver_candidates() -> None:
    selected = _selected_candidate_rows(
        [_candidate_row("OPT-SB01-F100"), _candidate_row("OPT-SB02-F090")],
        {"OPT-SB02-F090"},
    )

    assert [row["candidate_id"] for row in selected] == ["OPT-SB02-F090"]


def test_malformed_vver_history_is_reported_and_blocks_new_selection() -> None:
    payload = {
        "vver_selections": [{"record_id": "VVER-broken"}],
        "active_vver_selection_id": "VVER-broken",
    }

    assert _vver_history_error(payload) is not None
    assert active_current_vver_selection(
        payload,
        study_id="STUDY-SMALL-OFFICE-V1",
        current_pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
    ) is None
    with pytest.raises(ValueError, match="VVER-Historie ist fehlerhaft"):
        _store_vver_selection(payload, _record_for_current_candidate())


def test_legacy_candidates_without_pre_dimensioning_fingerprint_require_regeneration() -> None:
    payload = {
        "candidates": [_candidate_row()],
        "source_fingerprint": UPSTREAM_FINGERPRINT,
    }

    assert not _pre_dimensioning_candidates_are_current(payload, UPSTREAM_FINGERPRINT)


def _record_for_current_candidate():
    return create_vver_selection_record(
        study_id="STUDY-SMALL-OFFICE-V1",
        study_case_id="SC-OPT-SMALLOFFICE-5Z",
        study_direction_id="SD-OPTIMIZATION",
        selection_mode="manual",
        selection_reason="Referenzgruppe fuer die Dimensionierung.",
        pre_dimensioning_upstream_fingerprint=UPSTREAM_FINGERPRINT,
        selected_candidates=(_vver_candidate_from_row(_candidate_row()),),
    )
