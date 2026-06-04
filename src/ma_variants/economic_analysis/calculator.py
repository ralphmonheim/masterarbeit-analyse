"""Einfache generische Kostenberechnung fuer Varianten."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .models import EconomicAssumptions, EconomicScenario, EnergyPrice, GenericSystemCost, VariantCostResult

if TYPE_CHECKING:
    from ..simulation_results import VariantMetricsResult
    from ..system_catalog import SystemTemplate
    from ..variant_manager import Variant


def _by_key(items: list[GenericSystemCost]) -> dict[str, GenericSystemCost]:
    return {item.system_type: item for item in items}


def _prices_by_carrier(energy_prices: list[EnergyPrice]) -> dict[str, EnergyPrice]:
    return {energy_price.energy_carrier: energy_price for energy_price in energy_prices}


def _scenario_by_key(scenarios: list[EconomicScenario], scenario_key: str | None) -> EconomicScenario:
    if not scenarios:
        raise ValueError("Es ist kein EconomicScenario vorhanden.")
    if scenario_key is None:
        return scenarios[0]
    for scenario in scenarios:
        if scenario.scenario_key == scenario_key:
            return scenario
    raise ValueError(f"EconomicScenario nicht gefunden: {scenario_key}")


def _selected_system_types(
    selected_system_types: list[str] | None,
    selected_system_template_keys: list[str] | None,
    system_templates: list[SystemTemplate] | None,
) -> list[str]:
    if selected_system_types is not None:
        return list(dict.fromkeys(selected_system_types))
    if selected_system_template_keys is None or system_templates is None:
        return []
    template_by_key = {system_template.system_template_key: system_template for system_template in system_templates}
    return list(
        dict.fromkeys(
            template_by_key[template_key].system_type
            for template_key in selected_system_template_keys
            if template_key in template_by_key
        )
    )


def _replacement_cost(
    *,
    investment_cost_eur: float,
    lifetime_years: int,
    observation_period_years: int,
) -> float:
    replacement_count = max(0, (observation_period_years - 1) // lifetime_years)
    return float(investment_cost_eur * replacement_count)


def _simulation_energy_values(
    simulation_metrics: VariantMetricsResult | None,
) -> tuple[float | None, float | None]:
    if simulation_metrics is None:
        return None, None
    heating_energy = simulation_metrics.summary_metrics.get("heating_energy_kwh")
    cooling_energy = simulation_metrics.summary_metrics.get("cooling_energy_kwh")
    return (
        float(heating_energy) if heating_energy is not None else None,
        float(cooling_energy) if cooling_energy is not None else None,
    )


def calculate_variant_costs(
    variant: Variant,
    assumptions: EconomicAssumptions,
    scenario_key: str | None = None,
    selected_system_types: list[str] | None = None,
    selected_system_template_keys: list[str] | None = None,
    system_templates: list[SystemTemplate] | None = None,
    simulation_metrics: VariantMetricsResult | None = None,
) -> VariantCostResult:
    """Berechnet einfache generische Kosten fuer eine Variante."""
    scenario = _scenario_by_key(assumptions.economic_scenarios, scenario_key)
    system_types = _selected_system_types(selected_system_types, selected_system_template_keys, system_templates)
    system_cost_by_type = _by_key(assumptions.generic_system_costs)
    price_by_carrier = _prices_by_carrier(assumptions.energy_prices)
    notes: list[str] = []

    selected_costs: list[GenericSystemCost] = []
    for system_type in system_types:
        system_cost = system_cost_by_type.get(system_type)
        if system_cost is None:
            notes.append(f"Keine generische Kostenannahme fuer Systemtyp '{system_type}' vorhanden.")
            continue
        selected_costs.append(system_cost)
        if system_cost.is_example_value:
            notes.append(f"Systemkosten fuer '{system_type}' sind Beispielwerte.")

    heating_price = price_by_carrier.get(scenario.heating_energy_carrier)
    cooling_price = price_by_carrier.get(scenario.cooling_energy_carrier)
    if heating_price is None:
        raise ValueError(f"Energiepreis fehlt: {scenario.heating_energy_carrier}")
    if cooling_price is None:
        raise ValueError(f"Energiepreis fehlt: {scenario.cooling_energy_carrier}")
    if heating_price.is_example_value:
        notes.append(f"Energiepreis '{heating_price.energy_carrier}' ist ein Beispielwert.")
    if cooling_price.is_example_value:
        notes.append(f"Energiepreis '{cooling_price.energy_carrier}' ist ein Beispielwert.")
    if scenario.is_example_value:
        notes.append(f"Szenario '{scenario.scenario_key}' enthaelt Beispielannahmen.")

    simulation_heating_energy, simulation_cooling_energy = _simulation_energy_values(simulation_metrics)
    uses_simulation_results = simulation_heating_energy is not None or simulation_cooling_energy is not None
    uses_example_energy_values = simulation_heating_energy is None or simulation_cooling_energy is None

    heating_energy = (
        simulation_heating_energy
        if simulation_heating_energy is not None
        else scenario.default_heating_energy_kwh_per_year
    )
    cooling_energy = (
        simulation_cooling_energy
        if simulation_cooling_energy is not None
        else scenario.default_cooling_energy_kwh_per_year
    )
    if simulation_heating_energy is None:
        notes.append("Heizenergie nutzt Beispielwert aus dem Szenario.")
    if simulation_cooling_energy is None:
        notes.append("Kuehlenergie nutzt Beispielwert aus dem Szenario.")

    investment_cost = float(sum(system_cost.investment_cost_eur for system_cost in selected_costs))
    maintenance_cost_per_year = float(
        sum(system_cost.maintenance_cost_eur_per_year for system_cost in selected_costs)
    )
    maintenance_cost_total = maintenance_cost_per_year * scenario.observation_period_years
    replacement_cost = float(
        sum(
            _replacement_cost(
                investment_cost_eur=system_cost.investment_cost_eur,
                lifetime_years=system_cost.lifetime_years,
                observation_period_years=scenario.observation_period_years,
            )
            for system_cost in selected_costs
        )
    )
    energy_cost_per_year = float(
        heating_energy * heating_price.price_eur_per_kwh
        + cooling_energy * cooling_price.price_eur_per_kwh
    )
    energy_cost_total = energy_cost_per_year * scenario.observation_period_years
    total_cost = investment_cost + maintenance_cost_total + replacement_cost + energy_cost_total

    return VariantCostResult(
        variant_key=variant.variant_key,
        variant_name=variant.variant_name,
        scenario_key=scenario.scenario_key,
        selected_system_types=system_types,
        investment_cost_eur=round(investment_cost, 2),
        maintenance_cost_eur_per_year=round(maintenance_cost_per_year, 2),
        maintenance_cost_total_eur=round(maintenance_cost_total, 2),
        energy_cost_eur_per_year=round(energy_cost_per_year, 2),
        energy_cost_total_eur=round(energy_cost_total, 2),
        replacement_cost_eur=round(replacement_cost, 2),
        total_cost_eur=round(total_cost, 2),
        observation_period_years=scenario.observation_period_years,
        heating_energy_kwh_per_year=round(float(heating_energy), 3),
        cooling_energy_kwh_per_year=round(float(cooling_energy), 3),
        uses_simulation_results=uses_simulation_results,
        uses_example_energy_values=uses_example_energy_values,
        assumption_notes=list(dict.fromkeys(notes)),
    )


def calculate_variant_costs_for_variants(
    variants: list[Variant],
    assumptions: EconomicAssumptions,
    scenario_key: str | None = None,
    selected_system_types_by_variant: dict[str, list[str]] | None = None,
    selected_system_template_keys_by_variant: dict[str, list[str]] | None = None,
    system_templates: list[SystemTemplate] | None = None,
    simulation_metrics_by_variant: dict[str, VariantMetricsResult] | None = None,
) -> list[VariantCostResult]:
    """Berechnet generische Kosten fuer mehrere Varianten."""
    return [
        calculate_variant_costs(
            variant=variant,
            assumptions=assumptions,
            scenario_key=scenario_key,
            selected_system_types=(selected_system_types_by_variant or {}).get(variant.variant_key),
            selected_system_template_keys=(selected_system_template_keys_by_variant or {}).get(variant.variant_key),
            system_templates=system_templates,
            simulation_metrics=(simulation_metrics_by_variant or {}).get(variant.variant_key),
        )
        for variant in variants
    ]
