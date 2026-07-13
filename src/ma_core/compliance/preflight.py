"""Metadaten-Preflight ohne semantische Auswertung geschuetzter Inhalte."""

from __future__ import annotations

from pathlib import Path

from ma_core.input_sources import sha256_file

from .models import OperationRequest, PreflightRecord


def inspect_request_metadata(request: OperationRequest) -> PreflightRecord:
    """Erfasst Dateiname, Groesse und Hash vor der eigentlichen Verarbeitung."""
    path = request.file_path
    if path is None:
        return PreflightRecord(
            request_id=request.request_id,
            source_origin_known=bool((request.source_origin or "").strip()),
            applicable_license_known=bool((request.declared_license or "").strip()),
        )

    resolved_path = Path(path)
    exists = resolved_path.is_file()
    return PreflightRecord(
        request_id=request.request_id,
        file_name=resolved_path.name,
        file_suffix=resolved_path.suffix.lower() or None,
        file_size_bytes=resolved_path.stat().st_size if exists else None,
        sha256=sha256_file(resolved_path) if exists else None,
        file_exists=exists,
        source_origin_known=bool((request.source_origin or "").strip()),
        applicable_license_known=bool((request.declared_license or "").strip()),
    )
