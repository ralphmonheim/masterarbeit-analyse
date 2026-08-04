from dataclasses import replace

import pytest

from ma_dimensionierung.gateway import (
    execute_lod1_reference_dimensioning,
    prepare_lod1_reference_dimensioning_request,
)
from ma_dimensionierung.result_contracts import (
    CALCULATED_LOD1_RESULT_KIND,
    MANUAL_EXTERNAL_IDA_RESULT_KIND,
    CalculatedLod1ReferenceResult,
    ManualIdaReferenceLoadSet,
    build_manual_ida_legacy_payload,
    calculated_lod1_result_from_execution,
    manual_ida_reference_load_set_from_payload,
    validate_manual_ida_editor_rows,
    validate_manual_ida_source_metadata,
)
from ma_parameters import build_business_integration_lod1_parameter_snapshot


def _manual_payload() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "source_type": "manual_ida_result",
        "project_id": "PROJECT-001",
        "zone_model_id": "SmallOffice-5Z-v1",
        "zone_model_hash": "a" * 64,
        "reference_parameter_fingerprint": "b" * 64,
        "unit": "W",
        "zone_loads": [
            {"zone_id": "zone-1", "zone_name": "Office", "heating_load_w": 1000, "cooling_load_w": 800.5},
            {"zone_id": "zone-2", "zone_name": "Meeting", "heating_load_w": 0, "cooling_load_w": 200},
        ],
        "ida_source": {
            "ida_version": "5.0",
            "model_id": "MODEL-001",
            "run_id": "RUN-001",
            "source_file_name": "neutral_export.csv",
            "source_file_sha256": "c" * 64,
            "heating_load_definition": "zone_heating_load",
            "cooling_load_definition": "sensible_zone_load",
            "maximum_definition": "individual_zone_maximum",
            "design_conditions": "synthetic design period",
            "responsible": "Test User",
            "review_status": "reviewed",
            "reviewer": "Reviewer",
            "reviewed_at": "2026-08-02T12:00:00+00:00",
            "review_note": "Plausible gegen manuellen Export.",
            "source_classification": "externally_simulated_result",
        },
        "warnings": ["Zone zone-2 enthaelt 0 W."],
    }


def test_calculated_lod1_contract_adapts_gateway_execution_without_changing_legacy_result():
    preparation = prepare_lod1_reference_dimensioning_request(
        build_business_integration_lod1_parameter_snapshot()
    )
    assert preparation.request is not None
    execution = execute_lod1_reference_dimensioning(preparation.request)

    contract = calculated_lod1_result_from_execution(execution)

    assert contract.result_kind == CALCULATED_LOD1_RESULT_KIND
    assert contract.result_id == execution.result.result_id
    assert contract.input_fingerprint == execution.request.input_fingerprint
    assert contract.result_fingerprint != execution.result_fingerprint
    assert contract.heating_total_load_w == execution.result.heating_total_load_w
    assert execution.result.__class__.__name__ == "ReferenceDimensioningResult"


def test_calculated_lod1_contract_fingerprint_is_deterministic_and_binds_method_contract():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    first = prepare_lod1_reference_dimensioning_request(snapshot)
    second = prepare_lod1_reference_dimensioning_request(snapshot)
    assert first.request is not None and second.request is not None

    first_contract = calculated_lod1_result_from_execution(execute_lod1_reference_dimensioning(first.request))
    second_contract = calculated_lod1_result_from_execution(execute_lod1_reference_dimensioning(second.request))

    assert first_contract.result_fingerprint == second_contract.result_fingerprint
    with pytest.raises(ValueError, match="Rundungsregel"):
        replace(first_contract, rounding_rule="other")


def test_manual_external_ida_contract_is_separate_and_deterministic():
    payload = _manual_payload()

    first = manual_ida_reference_load_set_from_payload(payload)
    second = manual_ida_reference_load_set_from_payload(payload)

    assert isinstance(first, ManualIdaReferenceLoadSet)
    assert first.result_kind == MANUAL_EXTERNAL_IDA_RESULT_KIND
    assert first.result_id == second.result_id
    assert first.result_fingerprint == second.result_fingerprint
    assert first.source.run_id == "RUN-001"
    assert first.zone_loads[1].heating_load_w == 0.0


def test_manual_external_ida_contract_rejects_incomplete_or_corrupt_legacy_payloads():
    missing_review = _manual_payload()
    missing_review["ida_source"] = {**missing_review["ida_source"], "reviewer": ""}  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="reviewer"):
        manual_ida_reference_load_set_from_payload(missing_review)

    duplicate_zone = _manual_payload()
    duplicate_zone["zone_loads"] = [*duplicate_zone["zone_loads"], duplicate_zone["zone_loads"][0]]  # type: ignore[index]
    with pytest.raises(ValueError, match="doppelte Zonen-ID"):
        manual_ida_reference_load_set_from_payload(duplicate_zone)

    negative_load = _manual_payload()
    negative_load["zone_loads"] = [{**negative_load["zone_loads"][0], "heating_load_w": -1}]  # type: ignore[index]
    with pytest.raises(ValueError, match="nichtnegative"):
        manual_ida_reference_load_set_from_payload(negative_load)


def test_owner_validates_editor_rows_before_building_legacy_payload():
    rows, warnings = validate_manual_ida_editor_rows(
        (("zone-1", "Office"), ("zone-2", "Meeting")),
        (
            {"Zone": "Office", "Heizlast [W]": 1000, "Kuehllast [W]": 800.5},
            {"Zone": "Meeting", "Heizlast [W]": 0, "Kuehllast [W]": 200},
        ),
    )

    assert rows == _manual_payload()["zone_loads"]
    assert warnings == ("Zone 'Meeting' enthält 0 W und muss fachlich geprüft werden.",)
    with pytest.raises(ValueError, match="sortiert oder veraendert"):
        validate_manual_ida_editor_rows(
            (("zone-1", "Office"),),
            ({"Zone": "Other", "Heizlast [W]": 1, "Kuehllast [W]": 1},),
        )


def test_owner_builds_exact_legacy_payload_after_metadata_validation():
    source = _manual_payload()["ida_source"]
    assert isinstance(source, dict)
    provenance = validate_manual_ida_source_metadata(source)
    payload = _manual_payload()
    built = build_manual_ida_legacy_payload(
        project_id=str(payload["project_id"]),
        zone_model_id=str(payload["zone_model_id"]),
        zone_model_hash=str(payload["zone_model_hash"]),
        parameter_fingerprint="parameter-fingerprint-kept-for-legacy-compatibility",
        reference_parameter_fingerprint=str(payload["reference_parameter_fingerprint"]),
        zone_loads=payload["zone_loads"],  # type: ignore[arg-type]
        source_metadata=source,
        warnings=payload["warnings"],  # type: ignore[arg-type]
        updated_at="2026-08-02T12:00:00+00:00",
    )

    assert provenance.run_id == "RUN-001"
    assert list(built) == [
        "schema_version", "source_type", "project_id", "zone_model_id", "zone_model_hash",
        "updated_at", "unit", "zone_loads", "parameter_fingerprint",
        "reference_parameter_fingerprint", "ida_source", "warnings",
    ]
    assert built["schema_version"] == "1.0"
    assert built["source_type"] == "manual_ida_result"
    assert built["parameter_fingerprint"] == "parameter-fingerprint-kept-for-legacy-compatibility"
    assert manual_ida_reference_load_set_from_payload(built).source == provenance

    incomplete = {**source, "model_id": ""}
    with pytest.raises(ValueError, match="model_id"):
        validate_manual_ida_source_metadata(incomplete)


def test_calculated_and_manual_result_contracts_cannot_be_mistaken_for_each_other():
    manual = manual_ida_reference_load_set_from_payload(_manual_payload())

    with pytest.raises(ValueError, match="manuelle externe IDA"):
        replace(manual, result_kind=CALCULATED_LOD1_RESULT_KIND)

    with pytest.raises(ValueError, match="berechnete LoD-1"):
        CalculatedLod1ReferenceResult(
            result_kind=MANUAL_EXTERNAL_IDA_RESULT_KIND,
            contract_version=manual.contract_version,
            result_id="calculated-1",
            source_snapshot_id="snapshot-1",
            source_snapshot_version="1",
            status="evaluated",
            method_id="lod1",
            method_version="1",
            assumptions=(),
            rounding_rule="python_round_float_to_2_decimals_after_calculation",
            input_fingerprint="d" * 64,
            result_fingerprint="e" * 64,
            heating_transmission_load_w=1,
            heating_ventilation_load_w=1,
            heating_total_load_w=2,
            cooling_internal_load_w=1,
            ventilation_volume_flow_m3_h=1,
        )
