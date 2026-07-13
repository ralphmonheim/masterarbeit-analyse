import json

import pytest

from ma_core.compliance import (
    ComplianceAuditLogger,
    ComplianceBlockedError,
    ComplianceLevel,
    ComplianceOperation,
    ComplianceService,
    OperationRequest,
    ProcessingEnvironment,
    SourceType,
    find_sensitive_markers,
    safe_parse,
    sanitize_text,
)


def _request(
    source_type: SourceType,
    operation: ComplianceOperation,
    **overrides,
) -> OperationRequest:
    values = {
        "source_type": source_type,
        "operation": operation,
        "purpose": "Automatisierter Compliance-Test",
        "source_origin": "Dokumentierte Testquelle",
        "declared_license": "Dokumentierte Testlizenz",
    }
    values.update(overrides)
    return OperationRequest(**values)


@pytest.mark.parametrize(
    ("operation_request", "expected_level"),
    [
        (
            _request(SourceType.IDA_RESULT, ComplianceOperation.ANALYZE, user_owned=True),
            ComplianceLevel.GREEN,
        ),
        (
            _request(SourceType.IDA_IDM, ComplianceOperation.PARSE),
            ComplianceLevel.YELLOW,
        ),
        (
            _request(
                SourceType.IDA_IDM,
                ComplianceOperation.UPLOAD_EXTERNAL,
                environment=ProcessingEnvironment.EXTERNAL_AI,
            ),
            ComplianceLevel.YELLOW,
        ),
        (
            _request(SourceType.EQUA_LIBRARY, ComplianceOperation.EXTRACT),
            ComplianceLevel.RED,
        ),
        (
            _request(SourceType.IDA_IDM, ComplianceOperation.BATCH_SIMULATION),
            ComplianceLevel.RED,
        ),
        (
            _request(SourceType.EQUA_PARAMETER, ComplianceOperation.COMPARE),
            ComplianceLevel.YELLOW,
        ),
        (
            _request(SourceType.DIN_METADATA, ComplianceOperation.STORE),
            ComplianceLevel.GREEN,
        ),
        (
            _request(SourceType.DIN_PARAPHRASE, ComplianceOperation.ANALYZE),
            ComplianceLevel.GREEN,
        ),
        (
            _request(SourceType.DIN_CONTENT, ComplianceOperation.OCR),
            ComplianceLevel.RED,
        ),
        (
            _request(SourceType.DIN_CONTENT, ComplianceOperation.RAG),
            ComplianceLevel.RED,
        ),
        (
            _request(SourceType.DIN_SHORT_QUOTE, ComplianceOperation.PUBLISH),
            ComplianceLevel.YELLOW,
        ),
        (
            _request(
                SourceType.DWD_OPEN_DATA,
                ComplianceOperation.CONVERT,
                declared_license="CC-BY-4.0",
                official_source=True,
                attribution_present=True,
                third_party_rights_cleared=True,
            ),
            ComplianceLevel.GREEN,
        ),
        (
            _request(
                SourceType.DWD_OPEN_DATA,
                ComplianceOperation.CONVERT,
                declared_license="CC-BY-4.0",
                official_source=True,
                attribution_present=False,
                third_party_rights_cleared=True,
            ),
            ComplianceLevel.RED,
        ),
        (
            _request(SourceType.DWD_THIRD_PARTY, ComplianceOperation.ANALYZE),
            ComplianceLevel.YELLOW,
        ),
        (
            _request(
                SourceType.USER_OWNED,
                ComplianceOperation.READ,
                user_owned=True,
                contains_license_or_access_data=True,
            ),
            ComplianceLevel.RED,
        ),
        (
            _request(
                SourceType.UNKNOWN,
                ComplianceOperation.READ,
                source_origin=None,
                declared_license=None,
            ),
            ComplianceLevel.UNKNOWN,
        ),
    ],
)
def test_compliance_matrix(operation_request, expected_level):
    decision = ComplianceService().evaluate(operation_request)

    assert decision.classification is expected_level
    assert decision.processing_allowed is (expected_level is ComplianceLevel.GREEN)
    if expected_level is not ComplianceLevel.GREEN:
        with pytest.raises(ComplianceBlockedError):
            decision.require_allowed()


def test_yellow_requires_confirmation_and_permission_when_configured():
    request = _request(
        SourceType.IDA_IDM,
        ComplianceOperation.UPLOAD_EXTERNAL,
        environment=ProcessingEnvironment.EXTERNAL_AI,
    )
    service = ComplianceService()
    decision = service.evaluate(request)

    with pytest.raises(ComplianceBlockedError, match="Rechtefreigabe"):
        decision.with_approval(confirmation_reference="USER-001")

    approved = service.approve_yellow(
        request,
        decision,
        confirmation_reference="USER-001",
        permission_reference="EQUA-WRITTEN-PERMISSION-001",
    )

    assert approved.processing_allowed
    approved.require_allowed()


def test_safe_parse_never_calls_parser_for_blocked_decision():
    called = False

    def parser():
        nonlocal called
        called = True
        return "parsed"

    decision = ComplianceService().evaluate(_request(SourceType.DIN_CONTENT, ComplianceOperation.OCR))

    with pytest.raises(ComplianceBlockedError):
        safe_parse(parser, decision=decision)

    assert not called


def test_audit_contains_metadata_but_no_file_content_or_full_path(tmp_path):
    source = tmp_path / "protected.idm"
    source.write_text("TOP-SECRET-FULLTEXT", encoding="utf-8")
    log_path = tmp_path / "audit" / "decisions.jsonl"
    service = ComplianceService(audit_logger=ComplianceAuditLogger(log_path))

    service.evaluate(
        _request(
            SourceType.IDA_IDM,
            ComplianceOperation.PARSE,
            file_path=source,
        )
    )

    payload = json.loads(log_path.read_text(encoding="utf-8").splitlines()[0])
    serialized = json.dumps(payload)
    assert payload["request"]["file_path"] == "protected.idm"
    assert payload["preflight"]["sha256"]
    assert "TOP-SECRET-FULLTEXT" not in serialized
    assert str(tmp_path) not in serialized


def test_sanitization_masks_email_user_path_and_license_key():
    text = r"Kontakt a@example.org, Datei C:\Users\ralph\secret, license=ABCDEF1234567890"

    findings = find_sensitive_markers(text)
    sanitized = sanitize_text(text)

    assert {finding.category for finding in findings} == {
        "email",
        "license_or_api_key",
        "windows_user_path",
    }
    assert "a@example.org" not in sanitized
    assert "ABCDEF1234567890" not in sanitized
    assert "C:\\Users\\ralph" not in sanitized
