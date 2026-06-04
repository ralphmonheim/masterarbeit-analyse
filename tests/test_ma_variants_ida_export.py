import json
from dataclasses import replace

from ma_variants.ida_export import export_ida_variant_structure, load_ida_export_settings
from ma_variants.system_catalog import import_system_catalog, resolve_system_templates_for_variant
from ma_variants.variant_manager import Variant, VariantValue

FIXED_EXPORT_TIME = "2026-06-03T14:00:00+00:00"


def _variant_with_values(
    variant_key: str = "variant_0001",
    variant_name: str = "IDA Export Variante",
    status: str = "selected",
) -> tuple[Variant, list[VariantValue]]:
    variant = Variant(
        variant_key=variant_key,
        variant_name=variant_name,
        status=status,
    )
    variant_values = [
        VariantValue(
            variant_key=variant.variant_key,
            parameter_key="pv_system_template",
            option_key="PV_01",
            resolved_value="PV_01",
        )
    ]
    return variant, variant_values


def test_ida_export_creates_variant_folder_and_required_files(tmp_path):
    settings = load_ida_export_settings("config/export/example_ida_export.yaml")
    settings = replace(settings, output_root=tmp_path / "ida_exports")
    variant, variant_values = _variant_with_values()
    system_catalog = import_system_catalog("config/systems/example_system_templates.yaml")
    resolution = resolve_system_templates_for_variant(
        variant=variant,
        variant_values=variant_values,
        system_templates=system_catalog.system_templates,
        system_template_values=system_catalog.system_template_values,
        dependency_rules=system_catalog.dependency_rules,
    )

    result = export_ida_variant_structure(
        selected_variants=[(variant, variant_values)],
        settings=settings,
        system_template_resolutions={variant.variant_key: resolution},
        export_time=FIXED_EXPORT_TIME,
    )

    assert result.output_root == tmp_path / "ida_exports"
    variant_result = result.variant_exports[0]
    assert variant_result.export_dir == tmp_path / "ida_exports" / "variant_0001"
    assert variant_result.metadata_path.exists()
    assert variant_result.resolved_parameters_path.exists()
    assert variant_result.export_log_path.exists()

    metadata = json.loads(variant_result.metadata_path.read_text(encoding="utf-8"))
    assert metadata == {
        "variant_key": "variant_0001",
        "variant_name": "IDA Export Variante",
        "export_time": FIXED_EXPORT_TIME,
        "status": "selected",
        "source_config": "config/export/example_ida_export.yaml",
    }


def test_ida_export_writes_resolved_variant_and_system_parameters(tmp_path):
    settings = load_ida_export_settings("config/export/example_ida_export.yaml")
    settings = replace(settings, output_root=tmp_path / "ida_exports")
    variant, variant_values = _variant_with_values()
    system_catalog = import_system_catalog("config/systems/example_system_templates.yaml")
    resolution = resolve_system_templates_for_variant(
        variant=variant,
        variant_values=variant_values,
        system_templates=system_catalog.system_templates,
        system_template_values=system_catalog.system_template_values,
        dependency_rules=system_catalog.dependency_rules,
    )

    result = export_ida_variant_structure(
        selected_variants=[(variant, variant_values)],
        settings=settings,
        system_template_resolutions={variant.variant_key: resolution},
        export_time=FIXED_EXPORT_TIME,
    )

    payload = json.loads(result.variant_exports[0].resolved_parameters_path.read_text(encoding="utf-8"))
    assert payload["selected_system_templates"] == ["PV_01"]
    assert len(payload["parameters"]) == 5
    resolved_by_parameter = {
        parameter["parameter_key"]: parameter["resolved_value"]
        for parameter in payload["parameters"]
    }
    assert resolved_by_parameter["pv_system_template"] == "PV_01"
    assert resolved_by_parameter["pv_area_m2"] == 72
    assert resolved_by_parameter["pv_peak_power_kwp"] == 14.4


def test_ida_export_log_documents_no_ida_file_changes(tmp_path):
    settings = load_ida_export_settings("config/export/example_ida_export.yaml")
    settings = replace(settings, output_root=tmp_path / "ida_exports")
    variant, variant_values = _variant_with_values()

    result = export_ida_variant_structure(
        selected_variants=[(variant, variant_values)],
        settings=settings,
        export_time=FIXED_EXPORT_TIME,
    )

    log_text = result.variant_exports[0].export_log_path.read_text(encoding="utf-8")
    assert "No existing IDA ICE files were modified." in log_text
    assert "IDA ICE variant manager was not started." in log_text
    assert "No simulation was started from Python." in log_text


def test_ida_export_creates_safe_folders_for_multiple_variants(tmp_path):
    settings = load_ida_export_settings("config/export/example_ida_export.yaml")
    settings = replace(
        settings,
        output_root=tmp_path / "ida_exports",
        variant_folder_template="{variant_key}_{variant_name}",
    )
    first_variant = _variant_with_values("variant_0001", "Name mit Leerzeichen")
    second_variant = _variant_with_values("variant_0002", "Name/mit:ungueltigen*Zeichen")

    result = export_ida_variant_structure(
        selected_variants=[first_variant, second_variant],
        settings=settings,
        export_time=FIXED_EXPORT_TIME,
    )

    assert [variant_result.export_dir.name for variant_result in result.variant_exports] == [
        "variant_0001_Name_mit_Leerzeichen",
        "variant_0002_Name_mit_ungueltigen_Zeichen",
    ]
    assert all(variant_result.metadata_path.exists() for variant_result in result.variant_exports)
