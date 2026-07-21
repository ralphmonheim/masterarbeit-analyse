from ma_parameters import (
    build_business_integration_lod1_baseline_parameter_snapshot,
    load_reference_variation_specification,
)
from ma_variants import (
    build_variant_workflow,
    generate_selected_variants,
    select_catalog_candidates,
)


def _workflow():
    baseline = build_business_integration_lod1_baseline_parameter_snapshot()
    specification = load_reference_variation_specification(baseline)
    return baseline, build_variant_workflow(baseline, specification)


def test_zone_only_reference_creates_three_verified_candidates():
    _, workflow = _workflow()

    assert len(workflow.candidates) == 3
    assert len(workflow.catalog.candidates) == 3
    assert workflow.catalog.rejected_count == 0
    assert len(workflow.rules) == 1


def test_selected_variant_materializes_only_selected_candidate_with_linked_values():
    baseline, workflow = _workflow()
    candidate = workflow.catalog.candidates[0]
    selection = select_catalog_candidates(workflow.catalog, (candidate.candidate_id,))

    generated = generate_selected_variants(baseline, workflow.catalog, selection)

    assert [variant.variant_id for variant in generated] == [candidate.candidate_id]
    assert len(generated[0].values) == 2
    values = {item.parameter_key: item.value for item in generated[0].values}
    assert values["ZONE-BI-LOD1-0001.heating_setpoint_c"] == 19.0
    assert values["ZONE-BI-LOD1-0001.cooling_setpoint_c"] == 24.7


def test_selection_rejects_unknown_catalog_id():
    _, workflow = _workflow()

    try:
        select_catalog_candidates(workflow.catalog, ("VAR-UNKNOWN",))
    except ValueError as error:
        assert "unbekannte Varianten" in str(error)
    else:
        raise AssertionError("Eine unbekannte VAR-ID muss blockiert werden.")
