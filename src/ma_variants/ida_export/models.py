"""Datenmodelle fuer den vorbereiteten IDA-ICE-Export."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class IdaExportResult:
    """Zusammenfassung eines vorbereiteten IDA-ICE-Exports."""

    output_root: Path
    variant_exports: list["IdaVariantExportResult"]


@dataclass(frozen=True, slots=True)
class IdaVariantExportResult:
    """Dateipfade fuer eine exportierte Varianten-Uebergabestruktur."""

    variant_key: str
    export_dir: Path
    metadata_path: Path
    resolved_parameters_path: Path
    export_log_path: Path
