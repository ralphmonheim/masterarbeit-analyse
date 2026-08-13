"""Sichere, rein lesende Adapter fuer explizit freigegebene IDA-ICE-Ergebnisse."""

from .report_tables import extract_zone_report_rows
from .results import (
    ADAPTER_KEY,
    SCHEMA_VERSION,
    IdaArtifact,
    IdaDiagnostic,
    IdaPackage,
    RawIdaResult,
    StandardizedIdaResult,
    detect_ida_artifact,
    inspect_ida_package,
    parse_html_report,
    parse_prn_file,
    read_excel_metadata,
    sha256_file,
)

__all__ = [
    "ADAPTER_KEY",
    "SCHEMA_VERSION",
    "IdaArtifact",
    "IdaDiagnostic",
    "IdaPackage",
    "RawIdaResult",
    "StandardizedIdaResult",
    "detect_ida_artifact",
    "inspect_ida_package",
    "parse_html_report",
    "parse_prn_file",
    "read_excel_metadata",
    "sha256_file",
    "extract_zone_report_rows",
]
