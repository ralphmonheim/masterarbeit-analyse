"""Focused contracts for the technical Excel catalog presentation helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from ma_technical import TechnicalExcelCatalog
from ma_ui.streamlit_app.module_views.technical_view import (
    technical_excel_catalog_rows,
    technical_excel_selection_payload,
)


def _catalog() -> TechnicalExcelCatalog:
    return TechnicalExcelCatalog(
        source_path=Path("C:/synthetic/technical.xlsx"),
        source_sha256="a" * 64,
        id_column="System-ID",
        rows=(),
    )


def test_excel_rows_show_activity_and_validation_status_without_replacing_source_values():
    rows = technical_excel_catalog_rows(
        ({"System-ID": "TECH-001", "Aktiv": "ja", "Prüfstatus": "freigegeben", "Hersteller": "Quelle"},),
        "System-ID",
    )

    assert rows == [
        {
            "System-ID": "TECH-001",
            "Aktiv": "ja",
            "Validiert": "ja",
            "Validierungsstatus": "freigegeben",
            "Prüfstatus": "freigegeben",
            "Hersteller": "Quelle",
        }
    ]


def test_project_selection_preserves_source_path_version_hash_and_exact_record():
    record = {"System-ID": "TECH-001", "Aktiv": True, "Status": "validated", "Leistung": 1200}

    payload = technical_excel_selection_payload(_catalog(), record)

    assert payload["catalog_record_id"] == "TECH-001"
    assert payload["source_path"] == "C:/synthetic/technical.xlsx"
    assert payload["source_version"] == f"sha256:{'a' * 12}"
    assert payload["source_sha256"] == "a" * 64
    assert payload["record"] == record


def test_project_selection_blocks_inactive_or_unvalidated_records():
    with pytest.raises(ValueError, match="aktive und validierte"):
        technical_excel_selection_payload(
            _catalog(), {"System-ID": "TECH-002", "Aktiv": "nein", "Status": "validiert"}
        )
