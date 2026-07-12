from dataclasses import replace

from ma_parameters import (
    BASELINE_SNAPSHOT_SCHEMA_VERSION,
    BUSINESS_INTEGRATION_LOD1_BASELINE_SNAPSHOT_ID,
    BUSINESS_INTEGRATION_LOD1_BASELINE_SNAPSHOT_VERSION,
    BuildingDetailMode,
    FreshnessStatus,
    baseline_parameter_snapshot_reference_rows,
    baseline_parameter_snapshot_source_rows,
    baseline_parameter_snapshot_summary_rows,
    baseline_parameter_snapshot_value_rows,
    build_baseline_parameter_snapshot_from_parameter_snapshot,
    build_business_integration_lod1_baseline_parameter_snapshot,
    build_business_integration_lod1_parameter_snapshot,
    validate_baseline_parameter_snapshot,
)
from ma_validation import ReleaseStatus


def _codes(result):
    return {message.code for message in result.messages}


def test_business_integration_lod1_baseline_snapshot_is_released():
    snapshot = build_business_integration_lod1_baseline_parameter_snapshot()

    result = validate_baseline_parameter_snapshot(snapshot)
    value_rows = baseline_parameter_snapshot_value_rows(snapshot)
    source_rows = baseline_parameter_snapshot_source_rows(snapshot)
    reference_rows = baseline_parameter_snapshot_reference_rows(snapshot)
    summary_rows = baseline_parameter_snapshot_summary_rows(snapshot)
    parameters = {row["Parameter"] for row in value_rows}
    scopes = {row["Scope"] for row in value_rows}

    assert snapshot.snapshot_id == BUSINESS_INTEGRATION_LOD1_BASELINE_SNAPSHOT_ID
    assert snapshot.snapshot_version == BUSINESS_INTEGRATION_LOD1_BASELINE_SNAPSHOT_VERSION
    assert snapshot.schema_version == BASELINE_SNAPSHOT_SCHEMA_VERSION
    assert snapshot.building_detail_mode is BuildingDetailMode.SIMPLIFIED
    assert snapshot.freshness_status is FreshnessStatus.CURRENT
    assert result.release_status is ReleaseStatus.RELEASED
    assert result.messages == ()
    assert "window_area_ratio_percent" in parameters
    assert {"building", "zone_group", "zone", "technical_system"} <= scopes
    assert len(source_rows) == 3
    assert len(reference_rows) == 3
    assert {row["Kennwert"] for row in summary_rows} >= {"Baseline", "Detailmodus", "Content-Hash"}


def test_baseline_snapshot_keeps_v1_snapshot_reference():
    source_snapshot = build_business_integration_lod1_parameter_snapshot()
    baseline = build_baseline_parameter_snapshot_from_parameter_snapshot(
        source_snapshot,
        snapshot_id="PARAM-BI-LOD1-BASELINE-TEST",
        snapshot_version="PARAM-BI-LOD1-BASELINE-TEST-V2",
    )

    assert baseline.source_snapshot_id == source_snapshot.snapshot_id
    assert baseline.source_snapshot_version == source_snapshot.snapshot_version
    assert len(baseline.parameter_values) == len(source_snapshot.values)


def test_baseline_duplicate_parameter_value_ids_block_release():
    snapshot = build_business_integration_lod1_baseline_parameter_snapshot()
    duplicate_value = replace(
        snapshot.parameter_values[1],
        parameter_value_id=snapshot.parameter_values[0].parameter_value_id,
    )
    invalid_snapshot = replace(
        snapshot,
        parameter_values=(snapshot.parameter_values[0], duplicate_value, *snapshot.parameter_values[2:]),
    )

    result = validate_baseline_parameter_snapshot(invalid_snapshot)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BASELINE_OBJECT_ID_DUPLICATE" in _codes(result)


def test_baseline_duplicate_parameter_key_in_same_scope_blocks_release():
    snapshot = build_business_integration_lod1_baseline_parameter_snapshot()
    duplicate_value = replace(
        snapshot.parameter_values[1],
        parameter_value_id="PV-DUPLICATE-SCOPE-TEST",
        parameter_key=snapshot.parameter_values[0].parameter_key,
        scope=snapshot.parameter_values[0].scope,
    )
    invalid_snapshot = replace(
        snapshot,
        parameter_values=(snapshot.parameter_values[0], duplicate_value, *snapshot.parameter_values[2:]),
    )

    result = validate_baseline_parameter_snapshot(invalid_snapshot)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BASELINE_SCOPED_PARAMETER_DUPLICATE" in _codes(result)


def test_baseline_unknown_source_reference_blocks_release():
    snapshot = build_business_integration_lod1_baseline_parameter_snapshot()
    invalid_value = replace(snapshot.parameter_values[0], source_reference_id="ma_unknown:missing")
    invalid_snapshot = replace(snapshot, parameter_values=(invalid_value, *snapshot.parameter_values[1:]))

    result = validate_baseline_parameter_snapshot(invalid_snapshot)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BASELINE_VALUE_SOURCE_UNKNOWN" in _codes(result)


def test_baseline_unreleased_source_blocks_release():
    snapshot = build_business_integration_lod1_baseline_parameter_snapshot()
    blocked_source = replace(snapshot.source_references[0], validation_status=ReleaseStatus.BLOCKED.value)
    invalid_snapshot = replace(snapshot, source_references=(blocked_source, *snapshot.source_references[1:]))

    result = validate_baseline_parameter_snapshot(invalid_snapshot)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "BASELINE_SOURCE_NOT_RELEASED" in _codes(result)
