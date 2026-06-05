import csv
import json
from dataclasses import replace

from ma_variants.importing.catalog import import_catalog
from ma_variants.naming import apply_variant_names, load_naming_rules
from ma_variants.reporting import (
    build_variant_export_report,
    export_selected_variants_csv,
    export_selected_variants_json,
    export_variant_overview,
)
from ma_variants.selection import select_variants_by_key
from ma_variants.variant_manager import generate_variants

FIXED_EXPORTED_AT = "2026-06-03T12:00:00+00:00"


def _load_example_export_data(tmp_path):
    catalog = import_catalog(
        "config/ma_variants/parameters/example_parameters.yaml",
        "config/ma_variants/options/example_options.yaml",
        report_path=tmp_path / "import_report.json",
    )
    all_variants = generate_variants(catalog.parameters, catalog.option_values)
    selected_variants = select_variants_by_key(
        all_variants,
        ["variant_0001", "variant_0005", "variant_0008"],
    )
    naming_rules = load_naming_rules("config/ma_variants/naming/example_naming_rules.yaml")
    named_variants = apply_variant_names(selected_variants, naming_rules)
    return catalog, all_variants, named_variants


def test_export_selected_variants_json(tmp_path):
    _catalog, _all_variants, selected_variants = _load_example_export_data(tmp_path)

    output_path = export_selected_variants_json(
        selected_variants,
        tmp_path / "selected_variants.json",
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["variant_count"] == 3
    assert payload["variants"][0]["variant_name"] == "V001_CL24_VCO2_H100"
    assert len(payload["variants"][0]["values"]) == 3


def test_export_selected_variants_csv(tmp_path):
    _catalog, _all_variants, selected_variants = _load_example_export_data(tmp_path)

    output_path = export_selected_variants_csv(
        selected_variants,
        tmp_path / "selected_variants.csv",
    )

    with output_path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert len(rows) == 9
    assert rows[0] == {
        "variant_key": "variant_0001",
        "variant_name": "V001_CL24_VCO2_H100",
        "status": "generated",
        "parameter_key": "heating_capacity_factor",
        "option_key": "heating_capacity_100",
        "resolved_value": "100",
    }


def test_build_variant_export_report(tmp_path):
    catalog, all_variants, selected_variants = _load_example_export_data(tmp_path)

    report = build_variant_export_report(
        all_variants=all_variants,
        selected_variants=selected_variants,
        parameters=catalog.parameters,
        option_sets=catalog.option_sets,
        option_values=catalog.option_values,
        exported_at=FIXED_EXPORTED_AT,
    )

    assert report.total_variant_count == 8
    assert report.selected_variant_count == 3
    assert report.exported_at == FIXED_EXPORTED_AT
    assert report.missing_data_notes == []
    assert [entry["parameter_key"] for entry in report.used_parameters] == [
        "heating_capacity_factor",
        "ventilation_control_mode",
        "cooling_setpoint_level",
    ]
    assert [entry["option_set_key"] for entry in report.used_option_sets] == [
        "heating_capacity_factors",
        "ventilation_control_modes",
        "cooling_setpoint_levels",
    ]


def test_build_variant_export_report_notes_missing_catalog_entries(tmp_path):
    catalog, all_variants, selected_variants = _load_example_export_data(tmp_path)
    variant, variant_values = selected_variants[0]
    broken_values = [
        replace(
            variant_values[0],
            parameter_key="unknown_parameter",
            option_key="unknown_option",
        )
    ]

    report = build_variant_export_report(
        all_variants=all_variants,
        selected_variants=[(variant, broken_values)],
        parameters=catalog.parameters,
        option_sets=catalog.option_sets[1:],
        option_values=catalog.option_values,
        exported_at=FIXED_EXPORTED_AT,
    )

    assert any("unknown_parameter" in note for note in report.missing_data_notes)
    assert any("unknown_option" in note for note in report.missing_data_notes)


def test_export_variant_overview_creates_all_files(tmp_path):
    catalog, all_variants, selected_variants = _load_example_export_data(tmp_path)

    result = export_variant_overview(
        all_variants=all_variants,
        selected_variants=selected_variants,
        parameters=catalog.parameters,
        option_sets=catalog.option_sets,
        option_values=catalog.option_values,
        output_dir=tmp_path / "exports",
        exported_at=FIXED_EXPORTED_AT,
    )

    assert result.json_path.exists()
    assert result.csv_path.exists()
    assert result.report_path.exists()
    assert result.report.total_variant_count == 8
    assert result.report.selected_variant_count == 3

    report_payload = json.loads(result.report_path.read_text(encoding="utf-8"))
    assert report_payload["exported_at"] == FIXED_EXPORTED_AT
