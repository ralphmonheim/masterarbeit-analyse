"""Kombinierter Import fuer Parameter- und Optionskonfigurationen."""

from __future__ import annotations

from pathlib import Path

from .options import import_options
from .parameters import import_parameters
from .reports import CatalogImportResult, ImportValidationError, write_import_report

DEFAULT_IMPORT_REPORT = Path("data/ma_variants/imports/import_report.json")


def import_catalog(
    parameter_config: str | Path,
    option_config: str | Path,
    report_path: str | Path | None = DEFAULT_IMPORT_REPORT,
) -> CatalogImportResult:
    """Importiert Parameter und Optionen und validiert ihre Verknuepfungen."""
    option_sets, option_values, option_errors = import_options(option_config)
    parameters, parameter_errors = import_parameters(parameter_config)

    errors = [*option_errors, *parameter_errors]
    option_set_keys = {option_set.option_set_key for option_set in option_sets}
    for parameter in parameters:
        if parameter.option_set_key not in option_set_keys:
            errors.append(
                "Parameter "
                f"'{parameter.parameter_key}' referenziert nicht vorhandene Optionsgruppe "
                f"'{parameter.option_set_key}'."
            )

    result = CatalogImportResult(
        parameters=parameters,
        option_sets=option_sets,
        option_values=option_values,
        errors=errors,
        report_path=Path(report_path) if report_path is not None else None,
    )
    if report_path is not None:
        write_import_report(result, parameter_config, option_config, Path(report_path))

    if errors:
        raise ImportValidationError(errors, report_path=Path(report_path) if report_path is not None else None)

    return result
