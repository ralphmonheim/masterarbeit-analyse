"""Vertragstests fuer den finalen VCAT-/VSEL-Abschluss nach VVER."""

from dataclasses import replace

import pytest

from ma_dimensionierung import build_vver_selected_lod1_requests, execute_vver_selected_lod1_requests
from ma_parameters import (
    build_small_office_5z_v1_baseline_parameter_snapshot,
    build_small_office_5z_v1_parameter_snapshot,
)
from ma_variants import (
    VariantIdRegistry,
    build_small_office_v1_optimization_cases,
    finalization_result_to_payload,
    finalize_vver_dimensioning,
    generate_final_variants,
    load_small_office_v1_study,
    variant_id_registry_from_payload,
)
from ma_variants.project_studies import build_small_office_candidate_rows
from ma_variants.vver_selection import create_vver_selection_record


class _Candidate:
    def __init__(self, row: dict[str, object]) -> None:
        values = row["values"]
        assert isinstance(values, dict)
        self.candidate_id = str(row["candidate_id"])
        self.selected_options = tuple(sorted((str(key), str(value)) for key, value in values.items()))
        self.resolved_values = tuple(
            type("Resolved", (), {"parameter_key": str(key), "value": value, "unit": ""})()
            for key, value in sorted(values.items())
        )


def _finalization_input():
    study = load_small_office_v1_study()
    candidates = build_small_office_candidate_rows(study, _variation_specification(study))
    optimization = [row for row in candidates if row["study_direction"] == "optimization"]
    selection = create_vver_selection_record(
        study_id=study.study_id,
        study_case_id="SC-OPT-SMALLOFFICE-5Z",
        study_direction_id="SD-OPTIMIZATION",
        selection_mode="all",
        selection_reason="Alle Optimierungskandidaten werden verbindlich nachgerechnet.",
        pre_dimensioning_upstream_fingerprint="a" * 64,
        selected_candidates=tuple(_Candidate(row) for row in optimization),
    )
    requests = build_vver_selected_lod1_requests(
        build_small_office_5z_v1_parameter_snapshot(),
        selection,
        candidates,
        current_pre_dimensioning_upstream_fingerprint="a" * 64,
    )
    return study, candidates, selection, execute_vver_selected_lod1_requests(requests, candidates)


def _variation_specification(study):
    return {
        "status": "current",
        "study_contract": {
            "study_id": study.study_id,
            "enabled_dimensions": [
                "temperature_setpoint_bands",
                "coupled_heating_cooling_capacity_factors",
                "weather_ofat",
                "occupancy_ofat",
            ],
        },
    }


def test_final_vcat_allocates_ids_only_after_vver_dimensioning_and_vsel_maps_without_selection():
    _study, candidates, selection, assignments = _finalization_input()

    result = finalize_vver_dimensioning(
        project_id="PROJECT-SMALLOFFICE-V1",
        vver_selection=selection,
        candidates=candidates,
        assignments=assignments,
    )

    assert result.catalog.catalog_id.startswith("VCAT-")
    assert [entry.variant_id for entry in result.catalog.entries] == [f"VAR-{index:06d}" for index in range(1, 31)]
    assert result.selection.catalog_id == result.catalog.catalog_id
    assert result.selection.candidate_to_variant_ids == tuple(
        (entry.candidate_id, entry.variant_id) for entry in result.catalog.entries
    )
    assert result.registry.next_variant_number == 31


def test_final_vcat_reuses_an_existing_var_id_for_identical_final_content():
    _study, candidates, selection, assignments = _finalization_input()
    first = finalize_vver_dimensioning(
        project_id="PROJECT-SMALLOFFICE-V1",
        vver_selection=selection,
        candidates=candidates,
        assignments=assignments,
    )
    second = finalize_vver_dimensioning(
        project_id="PROJECT-SMALLOFFICE-V1",
        vver_selection=selection,
        candidates=candidates,
        assignments=assignments,
        registry=first.registry,
    )

    assert [entry.variant_id for entry in second.catalog.entries] == [entry.variant_id for entry in first.catalog.entries]
    assert second.registry.next_variant_number == first.registry.next_variant_number


def test_vgen_binds_final_ids_only_to_the_final_vcat_entries():
    study, candidates, selection, assignments = _finalization_input()
    result = finalize_vver_dimensioning(
        project_id="PROJECT-SMALLOFFICE-V1",
        vver_selection=selection,
        candidates=candidates,
        assignments=assignments,
    )
    cases = build_small_office_v1_optimization_cases(
        build_small_office_5z_v1_baseline_parameter_snapshot(), study, assignments
    )

    variants = generate_final_variants(result.catalog, {case.case_id: case.variant for case in cases})

    reference_entry = next(entry for entry in result.catalog.entries if entry.candidate_id == "OPT-SB01-F100")
    assert variants["OPT-SB01-F100"].variant_id == reference_entry.variant_id
    assert variants["OPT-SB01-F100"].content_fingerprint == reference_entry.variant_content_fingerprint

    with pytest.raises(ValueError, match="genau die im finalen VCAT"):
        generate_final_variants(result.catalog, {"OPT-SB01-F100": cases[0].variant})


def test_final_vcat_rejects_assignment_outside_vver_or_wrong_provenance():
    _study, candidates, selection, assignments = _finalization_input()

    with pytest.raises(ValueError, match="ausserhalb"):
        finalize_vver_dimensioning(
            project_id="PROJECT-SMALLOFFICE-V1",
            vver_selection=selection,
            candidates=candidates,
            assignments=(*assignments, replace(assignments[0], candidate_id="OPT-outside")),
        )
    with pytest.raises(ValueError, match="gehoert nicht"):
        finalize_vver_dimensioning(
            project_id="PROJECT-SMALLOFFICE-V1",
            vver_selection=selection,
            candidates=candidates,
            assignments=(replace(assignments[0], vver_record_id="VVER-other"), *assignments[1:]),
        )


def test_registry_rejects_non_projectwide_or_duplicate_id_mappings():
    with pytest.raises(ValueError, match="mehreren"):
        VariantIdRegistry(
            project_id="PROJECT-SMALLOFFICE-V1",
            next_variant_number=3,
            content_fingerprint_to_variant_id=(("a" * 64, "VAR-000001"), ("b" * 64, "VAR-000001")),
        )


def test_finalization_payload_keeps_history_and_reloads_the_projectwide_registry():
    _study, candidates, selection, assignments = _finalization_input()
    result = finalize_vver_dimensioning(
        project_id="PROJECT-SMALLOFFICE-V1",
        vver_selection=selection,
        candidates=candidates,
        assignments=assignments,
    )

    payload = finalization_result_to_payload({"existing": "preserved"}, result)

    assert payload["existing"] == "preserved"
    assert payload["active_final_catalog_id"] == result.catalog.catalog_id
    assert payload["active_vsel_id"] == result.selection.selection_id
    assert len(payload["final_catalogs"]) == len(payload["vsel_records"]) == 1
    assert variant_id_registry_from_payload(payload, project_id="PROJECT-SMALLOFFICE-V1") == result.registry
