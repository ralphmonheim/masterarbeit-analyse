import hashlib
import json
from datetime import datetime, timezone

import pytest

from ma_parameters import parameter_source_reference_from_released_technical_handover
from ma_technical import (
    ReleasedTechnicalHandover,
    TechnicalModelRevision,
    build_released_technical_handover,
)
from ma_validation import ReleaseStatus


def _handover(*, release_status: ReleaseStatus = ReleaseStatus.RELEASED) -> ReleasedTechnicalHandover:
    return ReleasedTechnicalHandover(
        technical_model_id="TECH-V2-0001",
        revision_id="TECH-V2-REV-0001",
        content_hash="a" * 64,
        release_status=release_status,
        service_interface_references=(),
    )


def test_released_technical_handover_becomes_revision_aware_parameter_source_reference():
    source = parameter_source_reference_from_released_technical_handover(_handover())

    assert source.source_reference_id == "ma_technical:TECH-V2-0001"
    assert source.dataset_key == "TECH-V2-0001"
    assert source.version_id == "TECH-V2-REV-0001"
    assert source.validation_status == "released"
    assert source.reference_id == "TECH-V2-0001"
    assert source.reference_version == "TECH-V2-REV-0001"
    assert source.content_hash == "a" * 64
    assert source.freshness_status == "current"


def test_released_technical_handover_converter_preserves_given_legacy_source_id():
    source = parameter_source_reference_from_released_technical_handover(
        _handover(),
        source_reference_id="ma_technical:TECH-LEGACY-COMPATIBLE",
    )

    assert source.source_reference_id == "ma_technical:TECH-LEGACY-COMPATIBLE"
    assert source.reference_version == "TECH-V2-REV-0001"


def test_released_revision_handover_converts_to_a_compatible_parameter_source_reference():
    payload = {
        "schema_version": "2.0",
        "technical_model_id": "TECH-V2-0001",
        "service_interfaces": [],
    }
    content_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    revision = TechnicalModelRevision(
        technical_model_id="TECH-V2-0001",
        revision_id="TECH-V2-REV-0001",
        content_hash=content_hash,
        release_status=ReleaseStatus.RELEASED,
        specification_payload=payload,
        released_at=datetime.now(timezone.utc),
    )

    source = parameter_source_reference_from_released_technical_handover(
        build_released_technical_handover(revision),
        source_reference_id="ma_technical:TECH-LEGACY-COMPATIBLE",
    )

    assert source.source_reference_id == "ma_technical:TECH-LEGACY-COMPATIBLE"
    assert source.reference_id == revision.technical_model_id
    assert source.reference_version == revision.revision_id
    assert source.content_hash == revision.content_hash


def test_released_technical_handover_converter_rejects_unreleased_metadata():
    with pytest.raises(ValueError, match="freigegebene"):
        parameter_source_reference_from_released_technical_handover(_handover(release_status=ReleaseStatus.BLOCKED))
