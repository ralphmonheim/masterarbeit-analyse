from dataclasses import replace

from ma_parameters import (
    ParameterSourceReference,
    build_business_integration_lod1_parameter_snapshot,
    parameter_snapshot_source_rows,
    parameter_snapshot_summary_rows,
    parameter_snapshot_value_rows,
    validate_parameter_snapshot,
)
from ma_validation import ReleaseStatus


def _codes(result):
    return {message.code for message in result.messages}


def test_business_integration_lod1_parameter_snapshot_is_released():
    snapshot = build_business_integration_lod1_parameter_snapshot()

    result = validate_parameter_snapshot(snapshot)
    value_rows = parameter_snapshot_value_rows(snapshot)
    source_rows = parameter_snapshot_source_rows(snapshot)
    summary_rows = parameter_snapshot_summary_rows(snapshot)
    parameters = {row["Parameter"] for row in value_rows}

    assert snapshot.snapshot_id == "PARAM-BI-LOD1-SNAPSHOT-0001"
    assert result.release_status is ReleaseStatus.RELEASED
    assert result.messages == ()
    assert "window_area_ratio_percent" in parameters
    assert "technical_system_count" in parameters
    assert len(source_rows) == 3
    assert {row["Kennwert"] for row in summary_rows} >= {"Snapshot", "Version", "Parameterwerte"}


def test_parameter_snapshot_duplicate_parameter_keys_block_release():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    duplicate_value = replace(snapshot.values[1], parameter_key=snapshot.values[0].parameter_key)
    invalid_snapshot = replace(snapshot, values=(snapshot.values[0], duplicate_value, *snapshot.values[2:]))

    result = validate_parameter_snapshot(invalid_snapshot)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "PARAMETER_OBJECT_ID_DUPLICATE" in _codes(result)


def test_parameter_snapshot_missing_required_lod1_key_blocks_release():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    values = tuple(value for value in snapshot.values if value.parameter_key != "window_area_ratio_percent")
    invalid_snapshot = replace(snapshot, values=values)

    result = validate_parameter_snapshot(invalid_snapshot)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "PARAMETER_REQUIRED_KEY_MISSING" in _codes(result)


def test_parameter_snapshot_unreleased_source_blocks_release():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    blocked_source = replace(snapshot.source_references[0], validation_status=ReleaseStatus.BLOCKED.value)
    invalid_snapshot = replace(snapshot, source_references=(blocked_source, *snapshot.source_references[1:]))

    result = validate_parameter_snapshot(invalid_snapshot)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "PARAMETER_SOURCE_NOT_RELEASED" in _codes(result)


def test_parameter_snapshot_unknown_source_reference_blocks_release():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    invalid_value = replace(snapshot.values[0], source_reference_id="ma_unknown:missing")
    invalid_snapshot = replace(snapshot, values=(invalid_value, *snapshot.values[1:]))

    result = validate_parameter_snapshot(invalid_snapshot)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "PARAMETER_SOURCE_UNKNOWN" in _codes(result)


def test_parameter_snapshot_missing_source_module_blocks_release():
    snapshot = build_business_integration_lod1_parameter_snapshot()
    extra_source = ParameterSourceReference(
        source_reference_id="ma_unknown:demo",
        module_key="ma_unknown",
        dataset_key="demo",
        version_id="demo",
        validation_status=ReleaseStatus.RELEASED.value,
    )
    invalid_snapshot = replace(snapshot, source_references=(extra_source,))

    result = validate_parameter_snapshot(invalid_snapshot)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "PARAMETER_REQUIRED_SOURCE_MISSING" in _codes(result)
