"""Importer fuer generische Wirtschaftlichkeitsannahmen."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..importing.io import load_config_file
from .models import EconomicAssumptions, EconomicScenario, EnergyPrice, GenericSystemCost

GENERIC_SYSTEM_COST_REQUIRED_FIELDS = (
    "system_type",
    "display_name",
    "investment_cost_eur",
    "maintenance_cost_eur_per_year",
    "lifetime_years",
)
ENERGY_PRICE_REQUIRED_FIELDS = (
    "energy_carrier",
    "price_eur_per_kwh",
)
ECONOMIC_SCENARIO_REQUIRED_FIELDS = (
    "scenario_key",
    "display_name",
    "observation_period_years",
    "heating_energy_carrier",
    "cooling_energy_carrier",
    "default_heating_energy_kwh_per_year",
    "default_cooling_energy_kwh_per_year",
)


def _missing_fields(raw_item: dict[str, Any], required_fields: tuple[str, ...]) -> list[str]:
    return [field for field in required_fields if field not in raw_item]


def _require_list(data: dict[str, Any], key: str) -> tuple[list[Any], list[str]]:
    raw_items = data.get(key)
    if not isinstance(raw_items, list):
        return [], [f"Konfiguration muss eine Liste '{key}' enthalten."]
    return raw_items, []


def _import_generic_system_costs(raw_items: list[Any]) -> tuple[list[GenericSystemCost], list[str]]:
    costs: list[GenericSystemCost] = []
    errors: list[str] = []
    seen_keys: set[str] = set()
    for index, raw_item in enumerate(raw_items, start=1):
        item_label = f"generic_system_costs[{index}]"
        if not isinstance(raw_item, dict):
            errors.append(f"{item_label} muss ein Objekt sein.")
            continue
        missing = _missing_fields(raw_item, GENERIC_SYSTEM_COST_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{item_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue
        system_type = str(raw_item["system_type"]).strip()
        if system_type in seen_keys:
            errors.append(f"Doppelter system_type '{system_type}'.")
            continue
        seen_keys.add(system_type)
        try:
            payload = {field: raw_item[field] for field in GENERIC_SYSTEM_COST_REQUIRED_FIELDS}
            payload["is_example_value"] = raw_item.get("is_example_value", True)
            costs.append(GenericSystemCost(**payload))
        except (TypeError, ValueError) as exc:
            errors.append(f"{item_label}: {exc}")
    return costs, errors


def _import_energy_prices(raw_items: list[Any]) -> tuple[list[EnergyPrice], list[str]]:
    prices: list[EnergyPrice] = []
    errors: list[str] = []
    seen_keys: set[str] = set()
    for index, raw_item in enumerate(raw_items, start=1):
        item_label = f"energy_prices[{index}]"
        if not isinstance(raw_item, dict):
            errors.append(f"{item_label} muss ein Objekt sein.")
            continue
        missing = _missing_fields(raw_item, ENERGY_PRICE_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{item_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue
        energy_carrier = str(raw_item["energy_carrier"]).strip()
        if energy_carrier in seen_keys:
            errors.append(f"Doppelter energy_carrier '{energy_carrier}'.")
            continue
        seen_keys.add(energy_carrier)
        try:
            payload = {field: raw_item[field] for field in ENERGY_PRICE_REQUIRED_FIELDS}
            payload["is_example_value"] = raw_item.get("is_example_value", True)
            prices.append(EnergyPrice(**payload))
        except (TypeError, ValueError) as exc:
            errors.append(f"{item_label}: {exc}")
    return prices, errors


def _import_economic_scenarios(raw_items: list[Any]) -> tuple[list[EconomicScenario], list[str]]:
    scenarios: list[EconomicScenario] = []
    errors: list[str] = []
    seen_keys: set[str] = set()
    for index, raw_item in enumerate(raw_items, start=1):
        item_label = f"economic_scenarios[{index}]"
        if not isinstance(raw_item, dict):
            errors.append(f"{item_label} muss ein Objekt sein.")
            continue
        missing = _missing_fields(raw_item, ECONOMIC_SCENARIO_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{item_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue
        scenario_key = str(raw_item["scenario_key"]).strip()
        if scenario_key in seen_keys:
            errors.append(f"Doppelter scenario_key '{scenario_key}'.")
            continue
        seen_keys.add(scenario_key)
        try:
            payload = {field: raw_item[field] for field in ECONOMIC_SCENARIO_REQUIRED_FIELDS}
            payload["is_example_value"] = raw_item.get("is_example_value", True)
            scenarios.append(EconomicScenario(**payload))
        except (TypeError, ValueError) as exc:
            errors.append(f"{item_label}: {exc}")
    return scenarios, errors


def import_economic_assumptions(config_path: str | Path) -> tuple[EconomicAssumptions, list[str]]:
    """Laedt generische Kostenannahmen aus YAML oder JSON."""
    data = load_config_file(config_path)
    all_errors: list[str] = []

    raw_costs, errors = _require_list(data, "generic_system_costs")
    all_errors.extend(errors)
    raw_prices, errors = _require_list(data, "energy_prices")
    all_errors.extend(errors)
    raw_scenarios, errors = _require_list(data, "economic_scenarios")
    all_errors.extend(errors)

    costs, errors = _import_generic_system_costs(raw_costs)
    all_errors.extend(errors)
    prices, errors = _import_energy_prices(raw_prices)
    all_errors.extend(errors)
    scenarios, errors = _import_economic_scenarios(raw_scenarios)
    all_errors.extend(errors)
    price_keys = {energy_price.energy_carrier for energy_price in prices}
    for scenario in scenarios:
        if scenario.heating_energy_carrier not in price_keys:
            all_errors.append(
                f"EconomicScenario '{scenario.scenario_key}' referenziert fehlenden Energiepreis "
                f"'{scenario.heating_energy_carrier}'."
            )
        if scenario.cooling_energy_carrier not in price_keys:
            all_errors.append(
                f"EconomicScenario '{scenario.scenario_key}' referenziert fehlenden Energiepreis "
                f"'{scenario.cooling_energy_carrier}'."
            )

    return (
        EconomicAssumptions(
            generic_system_costs=costs,
            energy_prices=prices,
            economic_scenarios=scenarios,
        ),
        all_errors,
    )
