import json

import pytest

from ma_variants.importing.catalog import import_catalog
from ma_variants.importing.reports import ImportValidationError
from ma_variants.option_catalog import import_options
from ma_variants.parameter_catalog import import_parameters


def test_import_catalog_loads_example_configs_and_writes_report(tmp_path):
    report_path = tmp_path / "import_report.json"

    result = import_catalog(
        "config/parameters/example_parameters.yaml",
        "config/options/example_options.yaml",
        report_path=report_path,
    )

    report_data = json.loads(report_path.read_text(encoding="utf-8"))
    assert len(result.parameters) == 3
    assert len(result.option_sets) == 3
    assert len(result.option_values) == 6
    assert report_data["status"] == "success"
    assert report_data["counts"]["errors"] == 0


def test_parameter_import_reports_missing_required_field(tmp_path):
    config_file = tmp_path / "parameters.yaml"
    config_file.write_text(
        "\n".join(
            [
                "parameters:",
                "  - display_name: Heizleistungsfaktor",
                "    category: hvac",
                "    parameter_class: sizing",
                "    option_set_key: heating_capacity_factors",
                "    unit: '%'",
                "    is_variant_relevant: true",
                "    is_naming_relevant: true",
                "    is_export_relevant: true",
            ]
        ),
        encoding="utf-8",
    )

    parameters, errors = import_parameters(config_file)

    assert parameters == []
    assert any("parameter_key" in error for error in errors)


def test_parameter_import_reports_duplicate_parameter_key(tmp_path):
    config_file = tmp_path / "parameters.yaml"
    config_file.write_text(
        "\n".join(
            [
                "parameters:",
                "  - parameter_key: heating_capacity_factor",
                "    display_name: Heizleistungsfaktor",
                "    category: hvac",
                "    parameter_class: sizing",
                "    option_set_key: heating_capacity_factors",
                "    unit: '%'",
                "    is_variant_relevant: true",
                "    is_naming_relevant: true",
                "    is_export_relevant: true",
                "  - parameter_key: heating_capacity_factor",
                "    display_name: Heizleistungsfaktor Kopie",
                "    category: hvac",
                "    parameter_class: sizing",
                "    option_set_key: heating_capacity_factors",
                "    unit: '%'",
                "    is_variant_relevant: true",
                "    is_naming_relevant: true",
                "    is_export_relevant: true",
            ]
        ),
        encoding="utf-8",
    )

    parameters, errors = import_parameters(config_file)

    assert len(parameters) == 1
    assert any("Doppelter parameter_key" in error for error in errors)


def test_option_import_reports_duplicate_option_key_and_empty_value(tmp_path):
    config_file = tmp_path / "options.yaml"
    config_file.write_text(
        "\n".join(
            [
                "option_sets:",
                "  - option_set_key: heating_capacity_factors",
                "    display_name: Heizleistungsfaktoren",
                "    description: Beispielstufen.",
                "    values:",
                "      - option_key: heating_capacity_80",
                "        label: 80 Prozent",
                "        value: 80",
                "        unit: '%'",
                "        is_active: true",
                "      - option_key: heating_capacity_80",
                "        label: 80 Prozent Kopie",
                "        value: 80",
                "        unit: '%'",
                "        is_active: true",
                "      - option_key: heating_capacity_empty",
                "        label: Leer",
                "        value: ''",
                "        unit: '%'",
                "        is_active: true",
            ]
        ),
        encoding="utf-8",
    )

    option_sets, option_values, errors = import_options(config_file)

    assert len(option_sets) == 1
    assert len(option_values) == 1
    assert any("Doppelter option_key" in error for error in errors)
    assert any("darf nicht leer sein" in error for error in errors)


def test_import_catalog_reports_missing_referenced_option_set(tmp_path):
    parameter_file = tmp_path / "parameters.yaml"
    option_file = tmp_path / "options.yaml"
    report_path = tmp_path / "report.json"
    parameter_file.write_text(
        "\n".join(
            [
                "parameters:",
                "  - parameter_key: missing_reference",
                "    display_name: Fehlende Referenz",
                "    category: hvac",
                "    parameter_class: sizing",
                "    option_set_key: unknown_options",
                "    unit: '-'",
                "    is_variant_relevant: true",
                "    is_naming_relevant: false",
                "    is_export_relevant: true",
            ]
        ),
        encoding="utf-8",
    )
    option_file.write_text(
        "\n".join(
            [
                "option_sets:",
                "  - option_set_key: known_options",
                "    display_name: Bekannte Optionen",
                "    description: Test.",
                "    values:",
                "      - option_key: known_option",
                "        label: Bekannt",
                "        value: known",
                "        unit: '-'",
                "        is_active: true",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ImportValidationError) as excinfo:
        import_catalog(parameter_file, option_file, report_path=report_path)

    report_data = json.loads(report_path.read_text(encoding="utf-8"))
    assert any("nicht vorhandene Optionsgruppe" in error for error in excinfo.value.errors)
    assert report_data["status"] == "failed"
    assert report_data["counts"]["errors"] == 1
