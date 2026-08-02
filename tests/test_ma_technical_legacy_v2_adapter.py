from __future__ import annotations

import pytest
import yaml

from ma_technical import load_business_integration_lod1_technical_spec, validate_technical_model
from ma_technical.legacy_v2_adapter import LEGACY_V1_TO_V2_MAPPING_VERSION, adapt_legacy_v1_to_v2
from ma_technical.metadata import ObjectReference
from ma_technical.revisions import load_technical_model_revision, release_technical_model
from ma_validation import DiagnosticSeverity


def _adapted_specification():
    return adapt_legacy_v1_to_v2(
        load_business_integration_lod1_technical_spec(),
        technical_model_id="TECH-000001",
        project_id="PRJ-000001",
        building_reference=ObjectReference(
            object_id="BUILDING-000001",
            revision_id="BUILDING-V1",
            object_type="BuildingModelSpecification",
        ),
        legacy_source_reference="config/ma_technical/examples/business_integration_lod1_technical_spec.yaml",
        legacy_source_sha256="a" * 64,
    )


def test_legacy_adapter_is_deterministic_and_keeps_source_provenance():
    first = _adapted_specification()
    second = _adapted_specification()

    assert first == second
    assert first.project_id == "PRJ-000001"
    assert first.building_reference.revision_id == "BUILDING-V1"
    assert first.source_metadata.source_type == "legacy_v1_adapter"
    assert first.source_metadata.input_source.sha256 == "a" * 64
    assert first.source_metadata.input_source.adapter_key == LEGACY_V1_TO_V2_MAPPING_VERSION
    assert first.source_metadata.source_reference.startswith("config/")


def test_legacy_adapter_discards_zone_relations_and_keeps_unmappable_values_as_assumptions():
    specification = _adapted_specification()
    assumption_texts = [assumption.text for assumption in specification.assumptions]

    assert all(not hasattr(interface, "served_zone_ids") for interface in specification.service_interfaces)
    assert all("ZONE-BI-LOD1-0001" not in text for text in assumption_texts)
    assert any("served_zone_ids wurden verworfen" in text for text in assumption_texts)
    assert any("design_power_w_m2=50.0" in text for text in assumption_texts)
    assert any("nur als supply_air-Serviceinterface" in text for text in assumption_texts)
    assert all(interface.capacity_mode.value == "assumed" for interface in specification.service_interfaces)
    assert any("Dimensionierung verwendet" in text for text in assumption_texts)


def test_legacy_adapter_result_is_structurally_releasable_without_capacity_calculation():
    result = validate_technical_model(_adapted_specification())

    assert not [message for message in result.messages if message.severity is DiagnosticSeverity.ERROR]


def test_legacy_adapter_warnings_require_and_record_explicit_confirmation(tmp_path):
    specification = _adapted_specification()

    with pytest.raises(ValueError, match="ausdruecklich bestaetigt"):
        release_technical_model(
            specification,
            revision_id="TECH-000001-REV-000001",
            target_dir=tmp_path,
        )

    revision = release_technical_model(
        specification,
        revision_id="TECH-000001-REV-000001",
        target_dir=tmp_path,
        warnings_confirmed=True,
    )

    assert revision.warnings_confirmed is True
    assert [warning.code for warning in revision.confirmed_warnings] == [
        "TECHNICAL_V2_SERVICE_INTERFACE_TERMINALS_MISSING",
    ] * 3
    assert len({warning.location for warning in revision.confirmed_warnings}) == 3
    assert revision.release_evidence_hash


def test_warning_revision_cannot_be_downgraded_to_an_unverified_legacy_revision(tmp_path):
    specification = _adapted_specification()
    revision = release_technical_model(
        specification,
        revision_id="TECH-000001-REV-000001",
        target_dir=tmp_path,
        warnings_confirmed=True,
    )
    revision_path = tmp_path / f"{revision.revision_id}.yaml"
    payload = yaml.safe_load(revision_path.read_text(encoding="utf-8"))
    payload.pop("release_evidence_hash")
    payload.pop("warnings_confirmed")
    payload.pop("confirmed_warnings")
    revision_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    with pytest.raises(ValueError, match="Freigabenachweis"):
        load_technical_model_revision(revision_path)


def test_legacy_adapter_rejects_non_relative_source_and_invalid_checksum():
    arguments = {
        "legacy_specification": load_business_integration_lod1_technical_spec(),
        "technical_model_id": "TECH-000001",
        "project_id": "PRJ-000001",
        "building_reference": ObjectReference(
            object_id="BUILDING-000001", revision_id="BUILDING-V1", object_type="BuildingModelSpecification"
        ),
        "legacy_source_reference": "C:/outside/legacy.yaml",
        "legacy_source_sha256": "a" * 64,
    }

    with pytest.raises(ValueError, match="repo-relativer"):
        adapt_legacy_v1_to_v2(**arguments)
    arguments["legacy_source_reference"] = "config/legacy.yaml"
    arguments["legacy_source_sha256"] = "not-a-sha"
    with pytest.raises(ValueError, match="SHA-256"):
        adapt_legacy_v1_to_v2(**arguments)
