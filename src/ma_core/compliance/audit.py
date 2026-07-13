"""Datensparsames append-only Auditprotokoll fuer Compliance-Entscheidungen."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from .models import ComplianceDecision, OperationRequest, PreflightRecord

DEFAULT_COMPLIANCE_AUDIT_PATH = Path("logs/compliance/decisions.jsonl")


def _json_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return value.name
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


class ComplianceAuditLogger:
    """Schreibt nur Entscheidungs- und Dateimetadaten, niemals Quelldateiinhalte."""

    def __init__(self, log_path: str | Path = DEFAULT_COMPLIANCE_AUDIT_PATH) -> None:
        self.log_path = Path(log_path)

    def append(
        self,
        request: OperationRequest,
        preflight: PreflightRecord,
        decision: ComplianceDecision,
    ) -> Path:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        request_payload = asdict(request)
        request_payload["file_path"] = request.file_path.name if request.file_path else None
        payload = {
            "request": _json_value(request_payload),
            "preflight": _json_value(asdict(preflight)),
            "decision": _json_value(asdict(decision)),
        }
        with self.log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        return self.log_path
