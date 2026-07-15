"""Importberichte fuer Parameter- und Optionskataloge."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .models import OptionSet, OptionValue, Parameter


class ImportValidationError(ValueError):
    """Fehler fuer ungueltige Importdaten."""

    def __init__(self, errors: list[str], report_path: Path | None = None) -> None:
        self.errors = errors
        self.report_path = report_path
        report_hint = f" Importbericht: {report_path}" if report_path is not None else ""
        super().__init__(f"Importdaten sind ungueltig: {len(errors)} Fehler.{report_hint}")


@dataclass(frozen=True, slots=True)
class CatalogImportResult:
    """Ergebnis eines kombinierten Parameter- und Optionsimports."""

    parameters: list[Parameter]
    option_sets: list[OptionSet]
    option_values: list[OptionValue]
    errors: list[str]
    report_path: Path | None = None


def write_import_report(
    result: CatalogImportResult,
    parameter_config: str | Path,
    option_config: str | Path,
    report_path: Path,
) -> None:
    """Schreibt einen kompakten JSON-Bericht zum Importlauf."""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_data = {
        "status": "failed" if result.errors else "success",
        "source_files": {
            "parameters": str(parameter_config),
            "options": str(option_config),
        },
        "counts": {
            "parameters": len(result.parameters),
            "option_sets": len(result.option_sets),
            "option_values": len(result.option_values),
            "errors": len(result.errors),
        },
        "errors": result.errors,
    }
    report_path.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")
