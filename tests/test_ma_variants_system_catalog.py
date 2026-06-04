import pytest

from ma_variants.system_catalog import (
    SystemTemplateResolutionError,
    import_system_catalog,
    resolve_system_templates_for_variant,
    resolve_system_templates_for_variants,
)
from ma_variants.variant_manager import Variant, VariantValue


def _variant_with_templates(*template_keys: str) -> tuple[Variant, list[VariantValue]]:
    variant = Variant(
        variant_key="variant_system_0001",
        variant_name="Systemtemplate Variante",
        status="selected",
    )
    variant_values = [
        VariantValue(
            variant_key=variant.variant_key,
            parameter_key=f"{template_key.lower()}_template",
            option_key=template_key,
            resolved_value=template_key,
        )
        for template_key in template_keys
    ]
    return variant, variant_values


def test_import_system_catalog_loads_example_systems():
    result = import_system_catalog("config/systems/example_system_templates.yaml")

    assert result.errors == []
    assert [template.system_template_key for template in result.system_templates] == [
        "HEAT_01",
        "COOL_01",
        "PV_01",
        "VENT_01",
    ]
    assert len(result.system_template_values) == 13
    assert result.dependency_rules[0].rule_key == "cooling_requires_ventilation"


def test_resolve_system_template_expands_pv_template_values():
    catalog = import_system_catalog("config/systems/example_system_templates.yaml")
    variant, variant_values = _variant_with_templates("PV_01")

    resolution = resolve_system_templates_for_variant(
        variant=variant,
        variant_values=variant_values,
        system_templates=catalog.system_templates,
        system_template_values=catalog.system_template_values,
        dependency_rules=catalog.dependency_rules,
    )

    assert resolution.selected_template_keys == ["PV_01"]
    resolved_by_parameter = {
        resolved_value.parameter_key: resolved_value.resolved_value
        for resolved_value in resolution.resolved_values
    }
    assert resolved_by_parameter == {
        "pv_area_m2": 72,
        "pv_tilt_deg": 30,
        "pv_azimuth_deg": 180,
        "pv_peak_power_kwp": 14.4,
    }


def test_resolve_system_template_checks_dependency_rules():
    catalog = import_system_catalog("config/systems/example_system_templates.yaml")
    variant, variant_values = _variant_with_templates("COOL_01")

    with pytest.raises(SystemTemplateResolutionError, match="VENT_01"):
        resolve_system_templates_for_variant(
            variant=variant,
            variant_values=variant_values,
            system_templates=catalog.system_templates,
            system_template_values=catalog.system_template_values,
            dependency_rules=catalog.dependency_rules,
        )


def test_resolve_system_template_allows_dependency_when_required_template_is_selected():
    catalog = import_system_catalog("config/systems/example_system_templates.yaml")
    variant, variant_values = _variant_with_templates("COOL_01", "VENT_01")

    resolution = resolve_system_templates_for_variant(
        variant=variant,
        variant_values=variant_values,
        system_templates=catalog.system_templates,
        system_template_values=catalog.system_template_values,
        dependency_rules=catalog.dependency_rules,
    )

    assert resolution.dependency_warnings == []
    assert resolution.selected_template_keys == ["COOL_01", "VENT_01"]
    assert {resolved_value.parameter_key for resolved_value in resolution.resolved_values} == {
        "cooling_system_type",
        "cooling_supply_temperature_degC",
        "cooling_nominal_power_kw",
        "ventilation_system_type",
        "ventilation_airflow_m3h",
        "ventilation_heat_recovery_efficiency",
    }


def test_resolve_system_templates_for_variants_returns_mapping():
    catalog = import_system_catalog("config/systems/example_system_templates.yaml")
    variant, variant_values = _variant_with_templates("HEAT_01", "PV_01")

    resolutions = resolve_system_templates_for_variants(
        [(variant, variant_values)],
        system_templates=catalog.system_templates,
        system_template_values=catalog.system_template_values,
        dependency_rules=catalog.dependency_rules,
    )

    assert set(resolutions) == {"variant_system_0001"}
    assert resolutions["variant_system_0001"].selected_template_keys == ["HEAT_01", "PV_01"]
