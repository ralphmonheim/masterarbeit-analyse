import csv
import json
from pathlib import Path

from ma_variants.economic_analysis import (
    calculate_variant_costs,
    export_variant_cost_results_csv,
    export_variant_cost_results_json,
    import_economic_assumptions,
)
from ma_variants.simulation_results import VariantMetricsResult
from ma_variants.system_catalog import import_system_catalog
from ma_variants.variant_manager import Variant

FIXED_EXPORTED_AT = "2026-06-03T16:00:00+00:00"


def _variant(variant_key="variant_a"):
    return Variant(variant_key=variant_key, variant_name="Variante A", status="selected")


def _simulation_metrics(variant_key="variant_a"):
    return VariantMetricsResult(
        variant_key=variant_key,
        variant_name="Variante A",
        result_dir=Path("data/database/variant_a_nutzdaten"),
        room_metrics=[],
        summary_metrics={
            "heating_energy_kwh": 1000,
            "cooling_energy_kwh": 500,
        },
        metadata={"source": "test"},
    )


def test_import_economic_assumptions_loads_example_values():
    assumptions, errors = import_economic_assumptions("config/economic/example_economic_assumptions.yaml")

    assert errors == []
    assert [cost.system_type for cost in assumptions.generic_system_costs] == [
        "heating",
        "cooling",
        "pv",
        "ventilation",
    ]
    assert [price.energy_carrier for price in assumptions.energy_prices] == [
        "heating_energy",
        "cooling_energy",
    ]
    assert assumptions.economic_scenarios[0].scenario_key == "example_20y"


def test_import_economic_assumptions_reports_duplicate_and_missing_references(tmp_path):
    config_path = tmp_path / "invalid_economic.yaml"
    config_path.write_text(
        """
generic_system_costs:
  - system_type: heating
    display_name: Generisches Heizsystem
    investment_cost_eur: 100
    maintenance_cost_eur_per_year: 10
    lifetime_years: 20
  - system_type: heating
    display_name: Doppeltes Heizsystem
    investment_cost_eur: 120
    maintenance_cost_eur_per_year: 12
    lifetime_years: 20
energy_prices:
  - energy_carrier: heating_energy
    price_eur_per_kwh: 0.2
economic_scenarios:
  - scenario_key: base
    display_name: Basis
    observation_period_years: 20
    heating_energy_carrier: heating_energy
    cooling_energy_carrier: cooling_energy
    default_heating_energy_kwh_per_year: 1000
    default_cooling_energy_kwh_per_year: 500
""",
        encoding="utf-8",
    )

    _assumptions, errors = import_economic_assumptions(config_path)

    assert any("Doppelter system_type 'heating'" in error for error in errors)
    assert any("fehlenden Energiepreis 'cooling_energy'" in error for error in errors)


def test_calculate_variant_costs_uses_simulation_metrics_when_available():
    assumptions, errors = import_economic_assumptions("config/economic/example_economic_assumptions.yaml")
    assert errors == []

    result = calculate_variant_costs(
        variant=_variant(),
        assumptions=assumptions,
        selected_system_types=["heating", "cooling"],
        simulation_metrics=_simulation_metrics(),
    )

    assert result.investment_cost_eur == 68000
    assert result.maintenance_cost_eur_per_year == 1670
    assert result.maintenance_cost_total_eur == 33400
    assert result.energy_cost_eur_per_year == 300
    assert result.energy_cost_total_eur == 6000
    assert result.replacement_cost_eur == 26000
    assert result.total_cost_eur == 133400
    assert result.heating_energy_kwh_per_year == 1000
    assert result.cooling_energy_kwh_per_year == 500
    assert result.uses_simulation_results is True
    assert result.uses_example_energy_values is False


def test_calculate_variant_costs_marks_default_energy_values():
    assumptions, errors = import_economic_assumptions("config/economic/example_economic_assumptions.yaml")
    assert errors == []

    result = calculate_variant_costs(
        variant=_variant(),
        assumptions=assumptions,
        selected_system_types=["pv"],
    )

    assert result.investment_cost_eur == 21000
    assert result.maintenance_cost_total_eur == 5200
    assert result.energy_cost_eur_per_year == 3000
    assert result.energy_cost_total_eur == 60000
    assert result.total_cost_eur == 86200
    assert result.uses_simulation_results is False
    assert result.uses_example_energy_values is True
    assert "Heizenergie nutzt Beispielwert aus dem Szenario." in result.assumption_notes


def test_calculate_variant_costs_can_use_system_template_keys():
    assumptions, errors = import_economic_assumptions("config/economic/example_economic_assumptions.yaml")
    assert errors == []
    system_catalog = import_system_catalog("config/systems/example_system_templates.yaml")

    result = calculate_variant_costs(
        variant=_variant(),
        assumptions=assumptions,
        selected_system_template_keys=["PV_01", "VENT_01"],
        system_templates=system_catalog.system_templates,
    )

    assert result.selected_system_types == ["pv", "ventilation"]
    assert result.investment_cost_eur == 52000
    assert result.maintenance_cost_eur_per_year == 1360


def test_export_variant_cost_results_as_json_and_csv(tmp_path):
    assumptions, errors = import_economic_assumptions("config/economic/example_economic_assumptions.yaml")
    assert errors == []
    result = calculate_variant_costs(
        variant=_variant(),
        assumptions=assumptions,
        selected_system_types=["heating"],
        simulation_metrics=_simulation_metrics(),
    )

    json_path = export_variant_cost_results_json(
        [result],
        tmp_path / "economic_results.json",
        exported_at=FIXED_EXPORTED_AT,
    )
    csv_path = export_variant_cost_results_csv([result], tmp_path / "economic_results.csv")

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["exported_at"] == FIXED_EXPORTED_AT
    assert payload["result_count"] == 1
    assert payload["results"][0]["variant_key"] == "variant_a"
    with csv_path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    assert rows[0]["variant_key"] == "variant_a"
    assert rows[0]["selected_system_types"] == "heating"
