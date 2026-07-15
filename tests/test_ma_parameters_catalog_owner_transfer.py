"""Contract tests for the P032-W2a catalog ownership transfer."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

import ma_variants
from ma_parameters.catalogs import (
    CatalogImportResult,
    ImportValidationError,
    OptionSet,
    OptionValue,
    Parameter,
    import_catalog,
    import_options,
    import_parameters,
)
from ma_parameters.catalogs.io import load_config_file
from ma_parameters.catalogs.reports import write_import_report
from ma_variants import option_catalog as legacy_option_catalog
from ma_variants import parameter_catalog as legacy_parameter_catalog
from ma_variants.importing import catalog as legacy_catalog_module
from ma_variants.importing import reports as legacy_reports_module
from ma_variants.option_catalog import importer as legacy_option_importer
from ma_variants.option_catalog import models as legacy_option_models
from ma_variants.parameter_catalog import importer as legacy_parameter_importer
from ma_variants.parameter_catalog import models as legacy_parameter_models


def _write_synthetic_catalog_files(tmp_path: Path, *, parameter_option_set_key: str) -> tuple[Path, Path]:
    parameter_path = tmp_path / "parameters.yaml"
    option_path = tmp_path / "options.yaml"
    parameter_path.write_text(
        "\n".join(
            [
                "parameters:",
                "  - parameter_key: synthetic_parameter",
                "    display_name: Synthetischer Parameter",
                "    category: test",
                "    parameter_class: sizing",
                f"    option_set_key: {parameter_option_set_key}",
                '    unit: "-"',
                "    is_variant_relevant: true",
                "    is_naming_relevant: false",
                "    is_export_relevant: true",
            ]
        ),
        encoding="utf-8",
    )
    option_path.write_text(
        "\n".join(
            [
                "option_sets:",
                "  - option_set_key: synthetic_options",
                "    display_name: Synthetische Optionen",
                "    description: Nur fuer den Contract-Test.",
                "    values:",
                "      - option_key: synthetic_option",
                "        label: Synthetische Option",
                "        value: 42",
                '        unit: "-"',
                "        is_active: true",
            ]
        ),
        encoding="utf-8",
    )
    return parameter_path, option_path


def test_legacy_catalog_paths_reexport_canonical_objects() -> None:
    """The legacy package must not create duplicate catalog types or importers."""
    assert legacy_parameter_catalog.Parameter is Parameter
    assert legacy_parameter_models.Parameter is Parameter
    assert ma_variants.Parameter is Parameter
    assert legacy_option_catalog.OptionSet is OptionSet
    assert legacy_option_models.OptionSet is OptionSet
    assert ma_variants.OptionSet is OptionSet
    assert legacy_option_catalog.OptionValue is OptionValue
    assert legacy_option_models.OptionValue is OptionValue
    assert ma_variants.OptionValue is OptionValue
    assert legacy_parameter_catalog.import_parameters is import_parameters
    assert legacy_parameter_importer.import_parameters is import_parameters
    assert legacy_parameter_importer.Parameter is Parameter
    assert legacy_parameter_importer.load_config_file is load_config_file
    assert legacy_option_catalog.import_options is import_options
    assert legacy_option_importer.import_options is import_options
    assert legacy_option_importer.OptionSet is OptionSet
    assert legacy_option_importer.OptionValue is OptionValue
    assert legacy_option_importer.load_config_file is load_config_file
    assert legacy_reports_module.CatalogImportResult is CatalogImportResult
    assert legacy_reports_module.ImportValidationError is ImportValidationError
    assert legacy_reports_module.Parameter is Parameter
    assert legacy_reports_module.OptionSet is OptionSet
    assert legacy_reports_module.OptionValue is OptionValue
    assert legacy_reports_module.write_import_report is write_import_report
    assert legacy_catalog_module.import_catalog is import_catalog
    assert legacy_catalog_module.import_parameters is import_parameters
    assert legacy_catalog_module.import_options is import_options
    assert legacy_catalog_module.CatalogImportResult is CatalogImportResult
    assert legacy_catalog_module.ImportValidationError is ImportValidationError
    assert legacy_catalog_module.write_import_report is write_import_report
    assert ma_variants.import_catalog is import_catalog


def test_owner_and_legacy_catalog_imports_return_compatible_synthetic_results(tmp_path: Path) -> None:
    parameter_path, option_path = _write_synthetic_catalog_files(
        tmp_path,
        parameter_option_set_key="synthetic_options",
    )

    owner_result = import_catalog(parameter_path, option_path, report_path=None)
    legacy_result = legacy_catalog_module.import_catalog(parameter_path, option_path, report_path=None)

    assert isinstance(owner_result, CatalogImportResult)
    assert owner_result == legacy_result
    assert owner_result.errors == []
    assert isinstance(owner_result.parameters[0], Parameter)
    assert isinstance(owner_result.option_sets[0], OptionSet)
    assert isinstance(owner_result.option_values[0], OptionValue)
    assert owner_result.report_path is None


def test_owner_and_legacy_catalog_imports_report_the_same_synthetic_error(tmp_path: Path) -> None:
    parameter_path, option_path = _write_synthetic_catalog_files(
        tmp_path,
        parameter_option_set_key="missing_options",
    )

    with pytest.raises(ImportValidationError) as owner_error:
        import_catalog(parameter_path, option_path, report_path=None)
    with pytest.raises(legacy_reports_module.ImportValidationError) as legacy_error:
        legacy_catalog_module.import_catalog(parameter_path, option_path, report_path=None)

    assert owner_error.value.errors == legacy_error.value.errors
    assert owner_error.value.report_path is None
    assert legacy_error.value.report_path is None
    assert "nicht vorhandene Optionsgruppe" in owner_error.value.errors[0]


def test_ma_parameters_and_ma_variants_import_in_a_fresh_interpreter() -> None:
    """Package imports must not depend on an earlier legacy import side effect."""
    repository_root = Path(__file__).resolve().parents[1]
    environment = dict(os.environ)
    existing_python_path = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = os.pathsep.join(
        path for path in (str(repository_root / "src"), existing_python_path) if path
    )

    completed = subprocess.run(
        [sys.executable, "-c", "import ma_parameters; import ma_variants"],
        check=False,
        capture_output=True,
        cwd=repository_root,
        env=environment,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
