"""Lokale Diagnose fuer Gebaeude-Eingabedateien ohne produktiven Import."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from ma_core import InputSource, InputSourceKind, build_input_source
from ma_validation import DiagnosticMessage, DiagnosticSeverity, ImportDiagnostic

from .paths import (
    BUILDING_CAD_INPUT_DIR,
    BUILDING_IFC_INPUT_DIR,
    BUILDING_RHINO_INPUT_DIR,
    SUPPORTED_BUILDING_SOURCE_SUFFIXES,
)

IFC_ENTITY_PATTERNS = {
    "IFCBUILDING": re.compile(r"\bIFCBUILDING\s*\(", re.IGNORECASE),
    "IFCBUILDINGSTOREY": re.compile(r"\bIFCBUILDINGSTOREY\s*\(", re.IGNORECASE),
    "IFCSPACE": re.compile(r"\bIFCSPACE\s*\(", re.IGNORECASE),
    "IFCWALL": re.compile(r"\bIFCWALL[A-Z]*\s*\(", re.IGNORECASE),
    "IFCSLAB": re.compile(r"\bIFCSLAB\s*\(", re.IGNORECASE),
    "IFCROOF": re.compile(r"\bIFCROOF\s*\(", re.IGNORECASE),
    "IFCWINDOW": re.compile(r"\bIFCWINDOW\s*\(", re.IGNORECASE),
    "IFCDOOR": re.compile(r"\bIFCDOOR\s*\(", re.IGNORECASE),
}
IFC_SCHEMA_PATTERN = re.compile(r"FILE_SCHEMA\s*\(\s*\(\s*'([^']+)'", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class BuildingSourceDiagnostic:
    """Zusammenfassung einer lokalen Quelldiagnose."""

    source: InputSource
    import_diagnostic: ImportDiagnostic
    ifc_schema: str | None = None
    entity_counts: dict[str, int] = field(default_factory=dict)
    line_count: int = 0

    @property
    def messages(self) -> tuple[DiagnosticMessage, ...]:
        return self.import_diagnostic.messages


def _data_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".ifc":
        return "IFC"
    if suffix == ".3dm":
        return "3DM"
    if suffix == ".dwg":
        return "DWG"
    return suffix.removeprefix(".").upper() or "UNKNOWN"


def _source_for_existing_file(path: Path) -> InputSource:
    return build_input_source(
        module_key="ma_building",
        source_kind=InputSourceKind.IMPORT,
        data_format=_data_format(path),
        source_path=path,
        adapter_key="ma_building.diagnostics",
    )


def _source_for_missing_path(path: Path) -> InputSource:
    return InputSource(
        module_key="ma_building",
        source_kind=InputSourceKind.IMPORT,
        data_format=_data_format(path),
        source_path=path,
        adapter_key="ma_building.diagnostics",
    )


def scan_building_input_directory(path: str | Path) -> tuple[Path, ...]:
    """Findet unterstuetzte lokale IFC- und 3DM-Dateien in einem Ordner."""
    directory = Path(path)
    if not directory.is_dir():
        return ()
    return tuple(
        sorted(
            item
            for item in directory.iterdir()
            if item.is_file() and item.suffix.lower() in SUPPORTED_BUILDING_SOURCE_SUFFIXES
        )
    )


def scan_default_building_input_files() -> tuple[Path, ...]:
    """Findet lokale Modellquellen in den Standardordnern."""
    return (
        scan_building_input_directory(BUILDING_IFC_INPUT_DIR)
        + scan_building_input_directory(BUILDING_RHINO_INPUT_DIR)
        + scan_building_input_directory(BUILDING_CAD_INPUT_DIR)
    )


def diagnose_building_source(path: str | Path) -> BuildingSourceDiagnostic:
    """Diagnostiziert eine lokale Modellquelle ohne Geometrieimport."""
    source_path = Path(path)
    if not source_path.exists():
        return _diagnostic_for_missing_path(source_path)
    if not source_path.is_file():
        return _diagnostic_for_invalid_path(source_path)

    source = _source_for_existing_file(source_path)
    suffix = source_path.suffix.lower()
    if suffix == ".ifc":
        return _diagnose_ifc_file(source_path, source)
    if suffix == ".3dm":
        return _diagnose_3dm_file(source)
    if suffix == ".dwg":
        return _diagnose_dwg_file(source)
    return _diagnose_unsupported_file(source)


def _diagnostic_for_missing_path(path: Path) -> BuildingSourceDiagnostic:
    source = _source_for_missing_path(path)
    messages = (
        DiagnosticMessage(
            DiagnosticSeverity.ERROR,
            "BUILDING_SOURCE_NOT_FOUND",
            "Die lokale Gebaeude-Eingabedatei wurde nicht gefunden.",
            location=str(path),
        ),
    )
    return BuildingSourceDiagnostic(
        source=source,
        import_diagnostic=ImportDiagnostic(source, messages=messages, record_count=1, rejected_count=1),
    )


def _diagnostic_for_invalid_path(path: Path) -> BuildingSourceDiagnostic:
    source = _source_for_missing_path(path)
    messages = (
        DiagnosticMessage(
            DiagnosticSeverity.ERROR,
            "BUILDING_SOURCE_NOT_FILE",
            "Der angegebene Gebaeude-Eingabepfad ist keine Datei.",
            location=str(path),
        ),
    )
    return BuildingSourceDiagnostic(
        source=source,
        import_diagnostic=ImportDiagnostic(source, messages=messages, record_count=1, rejected_count=1),
    )


def _diagnose_ifc_file(path: Path, source: InputSource) -> BuildingSourceDiagnostic:
    entity_counts = {entity_name: 0 for entity_name in IFC_ENTITY_PATTERNS}
    messages: list[DiagnosticMessage] = []
    ifc_schema: str | None = None
    line_count = 0

    try:
        with path.open("r", encoding="utf-8", errors="ignore") as source_file:
            for line in source_file:
                line_count += 1
                if ifc_schema is None:
                    match = IFC_SCHEMA_PATTERN.search(line)
                    if match:
                        ifc_schema = match.group(1)
                for entity_name, pattern in IFC_ENTITY_PATTERNS.items():
                    entity_counts[entity_name] += len(pattern.findall(line))
    except OSError as exc:
        messages.append(
            DiagnosticMessage(
                DiagnosticSeverity.ERROR,
                "BUILDING_IFC_READ_FAILED",
                f"Die IFC-Datei konnte nicht gelesen werden: {exc}",
                location=str(path),
            )
        )
        return BuildingSourceDiagnostic(
            source=source,
            import_diagnostic=ImportDiagnostic(source, messages=tuple(messages), record_count=1, rejected_count=1),
        )

    if ifc_schema:
        messages.append(
            DiagnosticMessage(
                DiagnosticSeverity.INFO,
                "BUILDING_IFC_SCHEMA_DETECTED",
                f"IFC-Schema erkannt: {ifc_schema}",
                location=str(path),
            )
        )
    else:
        messages.append(
            DiagnosticMessage(
                DiagnosticSeverity.WARNING,
                "BUILDING_IFC_SCHEMA_MISSING",
                "Keine IFC-Schemazeile erkannt.",
                location=str(path),
            )
        )

    entity_total = sum(entity_counts.values())
    if entity_total:
        messages.append(
            DiagnosticMessage(
                DiagnosticSeverity.INFO,
                "BUILDING_IFC_ENTITIES_DETECTED",
                f"IFC-Kernobjekte erkannt: {entity_total}",
                location=str(path),
            )
        )
    else:
        messages.append(
            DiagnosticMessage(
                DiagnosticSeverity.WARNING,
                "BUILDING_IFC_NO_CORE_ENTITIES",
                "Keine einfachen IFC-Kernobjekte fuer Gebaeude, Raeume, Bauteile oder Oeffnungen erkannt.",
                location=str(path),
            )
        )

    return BuildingSourceDiagnostic(
        source=source,
        import_diagnostic=ImportDiagnostic(
            source,
            messages=tuple(messages),
            record_count=entity_total,
            accepted_count=entity_total,
        ),
        ifc_schema=ifc_schema,
        entity_counts=entity_counts,
        line_count=line_count,
    )


def _diagnose_3dm_file(source: InputSource) -> BuildingSourceDiagnostic:
    messages = (
        DiagnosticMessage(
            DiagnosticSeverity.WARNING,
            "BUILDING_3DM_PARSER_NOT_ENABLED",
            "3DM-Datei als lokale Quelle erkannt; ein Rhino-Parser ist in v1 nicht aktiv.",
            location=str(source.source_path),
        ),
    )
    return BuildingSourceDiagnostic(
        source=source,
        import_diagnostic=ImportDiagnostic(source, messages=messages, record_count=1, rejected_count=1),
    )


def _diagnose_dwg_file(source: InputSource) -> BuildingSourceDiagnostic:
    messages = (
        DiagnosticMessage(
            DiagnosticSeverity.WARNING,
            "BUILDING_DWG_PARSER_NOT_ENABLED",
            "DWG-Datei als lokale CAD-Quelle erkannt; ein DWG-Parser ist in v1 nicht aktiv.",
            location=str(source.source_path),
        ),
    )
    return BuildingSourceDiagnostic(
        source=source,
        import_diagnostic=ImportDiagnostic(source, messages=messages, record_count=1, rejected_count=1),
    )


def _diagnose_unsupported_file(source: InputSource) -> BuildingSourceDiagnostic:
    messages = (
        DiagnosticMessage(
            DiagnosticSeverity.WARNING,
            "BUILDING_SOURCE_FORMAT_UNSUPPORTED",
            "Dieses Dateiformat wird in ma_building v1 nicht diagnostiziert.",
            location=str(source.source_path),
        ),
    )
    return BuildingSourceDiagnostic(
        source=source,
        import_diagnostic=ImportDiagnostic(source, messages=messages, record_count=1, rejected_count=1),
    )
