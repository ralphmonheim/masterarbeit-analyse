import json
from dataclasses import replace

from ma_variants.importing.catalog import import_catalog
from ma_variants.variant_manager import (
    calculate_theoretical_variant_count,
    export_variants_to_json,
    generate_variants,
)


def _load_example_catalog(tmp_path):
    return import_catalog(
        "config/parameters/example_parameters.yaml",
        "config/options/example_options.yaml",
        report_path=tmp_path / "import_report.json",
    )


def test_calculate_theoretical_variant_count_from_example_catalog(tmp_path):
    catalog = _load_example_catalog(tmp_path)

    count = calculate_theoretical_variant_count(catalog.parameters, catalog.option_values)

    assert count == 8


def test_variant_count_ignores_inactive_options(tmp_path):
    catalog = _load_example_catalog(tmp_path)
    option_values = [
        replace(option_value, is_active=False)
        if option_value.option_key == "cooling_setpoint_26"
        else option_value
        for option_value in catalog.option_values
    ]

    count = calculate_theoretical_variant_count(catalog.parameters, option_values)

    assert count == 4


def test_variant_count_ignores_non_variant_relevant_parameters(tmp_path):
    catalog = _load_example_catalog(tmp_path)
    parameters = [
        replace(parameter, is_variant_relevant=False)
        if parameter.parameter_key == "cooling_setpoint_level"
        else parameter
        for parameter in catalog.parameters
    ]

    count = calculate_theoretical_variant_count(parameters, catalog.option_values)

    assert count == 4


def test_generate_variants_from_example_catalog(tmp_path):
    catalog = _load_example_catalog(tmp_path)

    variants = generate_variants(catalog.parameters, catalog.option_values)

    first_variant, first_values = variants[0]
    assert len(variants) == 8
    assert first_variant.variant_key == "variant_0001"
    assert first_variant.status == "generated"
    assert [value.parameter_key for value in first_values] == [
        "heating_capacity_factor",
        "ventilation_control_mode",
        "cooling_setpoint_level",
    ]
    assert [value.option_key for value in first_values] == [
        "heating_capacity_100",
        "ventilation_co2",
        "cooling_setpoint_24",
    ]


def test_export_variants_to_json(tmp_path):
    catalog = _load_example_catalog(tmp_path)
    variants = generate_variants(catalog.parameters, catalog.option_values)
    output_path = tmp_path / "variants.json"

    exported_path = export_variants_to_json(variants, output_path)

    payload = json.loads(exported_path.read_text(encoding="utf-8"))
    assert payload["variant_count"] == 8
    assert payload["variants"][0]["variant_key"] == "variant_0001"
    assert len(payload["variants"][0]["values"]) == 3
