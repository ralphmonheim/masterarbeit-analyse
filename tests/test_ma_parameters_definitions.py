"""Tests fuer den additiven P015-S5A-Definitionskern."""

from __future__ import annotations

import pytest

from ma_parameters import (
    ParameterDataType,
    ParameterDefinition,
    ParameterDerivationStatus,
    ParameterEditability,
    ParameterGroup,
    ParameterInventoryStatus,
    ParameterModule,
    ParameterVariantCapability,
    load_parameter_inventory,
    parameter_inventory_summary,
    parameter_inventory_table_rows,
)


def test_parameter_definition_keeps_status_axes_separate():
    definition = ParameterDefinition(
        definition_key="zones.thermal_control.heating_setpoint",
        module=ParameterModule.ZONES,
        category="THERMAL_CONTROL",
        group_type="ZONE_THERMAL_CONTROL",
        parameter_name="heating_setpoint",
        display_name="Heizsollwert",
        datatype=ParameterDataType.NUMBER,
        unit="°C",
        lod_min=1,
        lod_max=3,
        allowed_source_types=("user", "reference_model"),
        default_editability=ParameterEditability.EDITABLE,
        default_variant_capability=ParameterVariantCapability.CONDITIONAL,
    )

    assert definition.module is ParameterModule.ZONES
    assert definition.applies_to_lod(2)
    assert not definition.applies_to_lod(4)
    assert definition.derivation_status is ParameterDerivationStatus.DIRECT


def test_derived_parameter_definition_must_be_fixed_and_not_variant_capable():
    with pytest.raises(ValueError, match="Abgeleitete Parameter"):
        ParameterDefinition(
            definition_key="building.geometry.window_wall_ratio",
            module="BUILDING",
            category="GEOMETRY",
            group_type="BUILDING_GEOMETRY",
            parameter_name="window_wall_ratio",
            display_name="Fensterflächenanteil",
            datatype="number",
            unit="-",
            lod_min=2,
            lod_max=3,
            allowed_source_types=("derived",),
            default_editability="editable",
            default_variant_capability="not_capable",
            derivation_status="derived",
        )


def test_variant_capable_parameter_definition_cannot_be_fixed():
    with pytest.raises(ValueError, match="Variantenfaehige"):
        ParameterDefinition(
            definition_key="technology.system.efficiency",
            module="TECHNOLOGY",
            category="PERFORMANCE",
            group_type="TECHNICAL_SYSTEM",
            parameter_name="efficiency",
            display_name="Wirkungsgrad",
            datatype="number",
            unit="-",
            lod_min=1,
            lod_max=3,
            allowed_source_types=("user",),
            default_editability="fixed",
            default_variant_capability="capable",
        )


def test_parameter_group_accepts_repeatable_object_groups():
    group = ParameterGroup(
        group_id="FE01",
        module="BUILDING",
        category="WINDOWS",
        group_type="WINDOW_TYPE",
        display_name="Fenstertyp FE01",
        instance_type="window_type",
        repeatable=True,
    )

    assert group.module is ParameterModule.BUILDING
    assert group.repeatable is True


def test_parameter_inventory_describes_current_preview_without_a_fixed_limit():
    entries = load_parameter_inventory()
    summary = parameter_inventory_summary(entries)
    rows = parameter_inventory_table_rows(entries)

    # 84 dokumentiert ausschliesslich den zum Inventurzeitpunkt beobachteten
    # LoD-1-Vorschauumfang; es ist keine programmatische Parametergrenze.
    assert summary["observed_current_entries"] == 84
    assert {entry.status for entry in entries} >= {
        ParameterInventoryStatus.EXISTS,
        ParameterInventoryStatus.MISSING,
        ParameterInventoryStatus.PARTIAL,
        ParameterInventoryStatus.METADATA,
        ParameterInventoryStatus.DERIVED,
    }
    assert any(row["Zielparameter"] == "weather.weather_dataset" for row in rows)
    assert not any(
        row["Bestehender Parameter"] == "weather.weather_key"
        and row["Inventarstatus"] != ParameterInventoryStatus.EXISTS.value
        for row in rows
    )


def test_inventory_entries_do_not_allow_observed_missing_parameters():
    entries = load_parameter_inventory()

    assert all(
        not (entry.status is ParameterInventoryStatus.MISSING and entry.observed_count)
        for entry in entries
    )
