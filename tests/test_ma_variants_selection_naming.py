import json

import pytest

from ma_variants.importing.catalog import import_catalog
from ma_variants.naming import (
    DuplicateVariantNameError,
    NamingRulePart,
    NamingRules,
    apply_variant_names,
    load_naming_rules,
)
from ma_variants.selection import (
    filter_variants_by_options,
    random_select_variants,
    select_variants_by_key,
)
from ma_variants.variant_manager import export_variants_to_json, generate_variants


def _load_example_variants(tmp_path):
    catalog = import_catalog(
        "config/parameters/example_parameters.yaml",
        "config/options/example_options.yaml",
        report_path=tmp_path / "import_report.json",
    )
    return generate_variants(catalog.parameters, catalog.option_values)


def test_select_variants_by_key_preserves_requested_order(tmp_path):
    variants = _load_example_variants(tmp_path)

    selected = select_variants_by_key(variants, ["variant_0005", "variant_0001"])

    assert [variant.variant_key for variant, _values in selected] == ["variant_0005", "variant_0001"]


def test_select_variants_by_key_reports_missing_key(tmp_path):
    variants = _load_example_variants(tmp_path)

    with pytest.raises(ValueError, match="variant_9999"):
        select_variants_by_key(variants, ["variant_9999"])


def test_filter_variants_by_options_uses_parameter_and_option_keys(tmp_path):
    variants = _load_example_variants(tmp_path)

    selected = filter_variants_by_options(
        variants,
        {
            "heating_capacity_factor": "heating_capacity_80",
            "ventilation_control_mode": ["ventilation_co2"],
        },
    )

    assert [variant.variant_key for variant, _values in selected] == ["variant_0005", "variant_0006"]


def test_random_select_variants_is_reproducible(tmp_path):
    variants = _load_example_variants(tmp_path)

    first_selection = random_select_variants(variants, count=3, random_seed=42)
    second_selection = random_select_variants(variants, count=3, random_seed=42)

    assert [variant.variant_key for variant, _values in first_selection] == [
        variant.variant_key for variant, _values in second_selection
    ]
    assert len(first_selection) == 3


def test_apply_variant_names_uses_naming_rules(tmp_path):
    variants = _load_example_variants(tmp_path)
    naming_rules = load_naming_rules("config/naming/example_naming_rules.yaml")
    selected = select_variants_by_key(variants, ["variant_0001", "variant_0005", "variant_0008"])

    named_variants = apply_variant_names(selected, naming_rules)

    assert [variant.variant_name for variant, _values in named_variants] == [
        "V001_CL24_VCO2_H100",
        "V002_CL24_VCO2_H080",
        "V003_CL26_VTMP_H080",
    ]


def test_apply_variant_names_rejects_duplicates(tmp_path):
    variants = _load_example_variants(tmp_path)
    naming_rules = NamingRules(
        prefix="V",
        index_width=3,
        separator="_",
        include_index=False,
        parts=[
            NamingRulePart(
                parameter_key="cooling_setpoint_level",
                option_tokens={
                    "cooling_setpoint_24": "CL",
                    "cooling_setpoint_26": "CL",
                },
            )
        ],
    )
    selected = select_variants_by_key(variants, ["variant_0001", "variant_0002"])

    with pytest.raises(DuplicateVariantNameError):
        apply_variant_names(selected, naming_rules)


def test_export_selected_named_variants_to_json(tmp_path):
    variants = _load_example_variants(tmp_path)
    naming_rules = load_naming_rules("config/naming/example_naming_rules.yaml")
    selected = select_variants_by_key(variants, ["variant_0001", "variant_0005", "variant_0008"])
    named_variants = apply_variant_names(selected, naming_rules)

    output_path = export_variants_to_json(named_variants, tmp_path / "selected_named_variants.json")

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["variant_count"] == 3
    assert payload["variants"][0]["variant_name"] == "V001_CL24_VCO2_H100"
