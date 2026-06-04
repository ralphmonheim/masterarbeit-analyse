"""Datenmodelle fuer generische Wirtschaftlichkeitsannahmen."""

from __future__ import annotations

from dataclasses import dataclass

from ..validation import require_bool, require_non_empty


@dataclass(frozen=True, slots=True)
class GenericSystemCost:
    """Generische Kostenannahmen fuer einen Systemtyp."""

    system_type: str
    display_name: str
    investment_cost_eur: float
    maintenance_cost_eur_per_year: float
    lifetime_years: int
    is_example_value: bool = True

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.system_type, "system_type", model_name)
        require_non_empty(self.display_name, "display_name", model_name)
        require_bool(self.is_example_value, "is_example_value", model_name)
        if self.investment_cost_eur < 0:
            raise ValueError("GenericSystemCost.investment_cost_eur darf nicht negativ sein.")
        if self.maintenance_cost_eur_per_year < 0:
            raise ValueError("GenericSystemCost.maintenance_cost_eur_per_year darf nicht negativ sein.")
        if self.lifetime_years <= 0:
            raise ValueError("GenericSystemCost.lifetime_years muss groesser als 0 sein.")


@dataclass(frozen=True, slots=True)
class EnergyPrice:
    """Generische Energiepreisannahme."""

    energy_carrier: str
    price_eur_per_kwh: float
    is_example_value: bool = True

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.energy_carrier, "energy_carrier", model_name)
        require_bool(self.is_example_value, "is_example_value", model_name)
        if self.price_eur_per_kwh < 0:
            raise ValueError("EnergyPrice.price_eur_per_kwh darf nicht negativ sein.")


@dataclass(frozen=True, slots=True)
class EconomicScenario:
    """Szenario fuer eine einfache Betrachtungszeitraum-Rechnung."""

    scenario_key: str
    display_name: str
    observation_period_years: int
    heating_energy_carrier: str
    cooling_energy_carrier: str
    default_heating_energy_kwh_per_year: float
    default_cooling_energy_kwh_per_year: float
    is_example_value: bool = True

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.scenario_key, "scenario_key", model_name)
        require_non_empty(self.display_name, "display_name", model_name)
        require_non_empty(self.heating_energy_carrier, "heating_energy_carrier", model_name)
        require_non_empty(self.cooling_energy_carrier, "cooling_energy_carrier", model_name)
        require_bool(self.is_example_value, "is_example_value", model_name)
        if self.observation_period_years <= 0:
            raise ValueError("EconomicScenario.observation_period_years muss groesser als 0 sein.")
        if self.default_heating_energy_kwh_per_year < 0:
            raise ValueError("EconomicScenario.default_heating_energy_kwh_per_year darf nicht negativ sein.")
        if self.default_cooling_energy_kwh_per_year < 0:
            raise ValueError("EconomicScenario.default_cooling_energy_kwh_per_year darf nicht negativ sein.")


@dataclass(frozen=True, slots=True)
class EconomicAssumptions:
    """Gebündelte Annahmen fuer die generische Wirtschaftlichkeitsanalyse."""

    generic_system_costs: list[GenericSystemCost]
    energy_prices: list[EnergyPrice]
    economic_scenarios: list[EconomicScenario]


@dataclass(frozen=True, slots=True)
class VariantCostResult:
    """Ergebnis einer einfachen Wirtschaftlichkeitsbewertung je Variante."""

    variant_key: str
    variant_name: str
    scenario_key: str
    selected_system_types: list[str]
    investment_cost_eur: float
    maintenance_cost_eur_per_year: float
    maintenance_cost_total_eur: float
    energy_cost_eur_per_year: float
    energy_cost_total_eur: float
    replacement_cost_eur: float
    total_cost_eur: float
    observation_period_years: int
    heating_energy_kwh_per_year: float
    cooling_energy_kwh_per_year: float
    uses_simulation_results: bool
    uses_example_energy_values: bool
    assumption_notes: list[str]
