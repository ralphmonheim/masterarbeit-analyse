from ma_variants.ui import (
    apply_naming_to_ui_data,
    list_result_files,
    load_variant_ui_data,
    option_value_rows,
    parameter_rows,
    run_variant_export,
    select_variants_by_method,
    select_variants_for_export,
    selection_method_by_label,
    selection_method_rows,
    variant_rows,
)


def test_load_variant_ui_data_uses_existing_catalog_and_variant_logic():
    ui_data = load_variant_ui_data()

    assert len(ui_data.parameters) == 3
    assert len(ui_data.option_sets) == 3
    assert len(ui_data.option_values) == 6
    assert ui_data.theoretical_variant_count == 8
    assert len(ui_data.generated_variants) == 8


def test_ui_table_rows_are_plain_records():
    ui_data = load_variant_ui_data()

    parameters = parameter_rows(ui_data.parameters)
    options = option_value_rows(ui_data.option_sets, ui_data.option_values)
    variants = variant_rows(ui_data.generated_variants)

    assert parameters[0]["parameter_key"] == "heating_capacity_factor"
    assert options[0]["option_set_name"] == "Heizleistungsfaktoren"
    assert variants[0]["variant_key"] == "variant_0001"
    assert "heating_capacity_factor=heating_capacity_100" in variants[0]["values"]


def test_select_variants_for_export_uses_variant_keys():
    ui_data = load_variant_ui_data()

    selected = select_variants_for_export(ui_data.generated_variants, ["variant_0002", "variant_0001"])

    assert [variant.variant_key for variant, _values in selected] == ["variant_0002", "variant_0001"]


def test_selection_methods_describe_implemented_and_prepared_choices():
    method_rows = selection_method_rows()

    assert method_rows[0]["method_key"] == "manual"
    assert selection_method_by_label("Manuell nach variant_key").method_key == "manual"
    assert any(row["method_key"] == "monte_carlo" and not row["is_implemented"] for row in method_rows)


def test_select_variants_by_method_supports_manual_random_and_filter():
    ui_data = load_variant_ui_data()

    manual = select_variants_by_method(
        ui_data.generated_variants,
        "manual",
        selected_variant_keys=["variant_0002", "variant_0001"],
    )
    random_a = select_variants_by_method(ui_data.generated_variants, "random", random_count=2, random_seed=7)
    random_b = select_variants_by_method(ui_data.generated_variants, "random", random_count=2, random_seed=7)
    filtered = select_variants_by_method(
        ui_data.generated_variants,
        "filter",
        filter_criteria={"heating_capacity_factor": ["heating_capacity_80"]},
    )

    assert [variant.variant_key for variant, _values in manual] == ["variant_0002", "variant_0001"]
    assert [variant.variant_key for variant, _values in random_a] == [
        variant.variant_key for variant, _values in random_b
    ]
    assert {value.option_key for _variant, values in filtered for value in values if value.parameter_key == "heating_capacity_factor"} == {
        "heating_capacity_80"
    }


def test_apply_naming_to_ui_data_uses_existing_naming_rules():
    ui_data = load_variant_ui_data()

    named_ui_data = apply_naming_to_ui_data(ui_data)
    names = [variant.variant_name for variant, _values in named_ui_data.generated_variants]

    assert names[0] == "V001_CL24_VCO2_H100"
    assert len(names) == len(set(names))


def test_run_variant_export_and_list_result_files(tmp_path):
    ui_data = load_variant_ui_data()
    selected = select_variants_for_export(ui_data.generated_variants, ["variant_0001"])

    export_result = run_variant_export(ui_data, selected, output_dir=tmp_path)
    result_files = list_result_files(tmp_path)

    assert export_result.json_path.exists()
    assert export_result.csv_path.exists()
    assert export_result.report_path.exists()
    assert {result_file.file_name for result_file in result_files} == {
        "selected_variants.csv",
        "selected_variants.json",
        "variant_report.json",
    }
