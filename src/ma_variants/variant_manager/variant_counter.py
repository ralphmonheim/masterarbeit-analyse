"""Berechnung der theoretischen Variantenanzahl."""

from __future__ import annotations

from collections import defaultdict

from ..option_catalog import OptionValue
from ..parameter_catalog import Parameter


def group_active_options_by_set(option_values: list[OptionValue]) -> dict[str, list[OptionValue]]:
    """Gruppiert aktive Optionswerte nach Optionsgruppe."""
    options_by_set: dict[str, list[OptionValue]] = defaultdict(list)
    for option_value in option_values:
        if option_value.is_active:
            options_by_set[option_value.option_set_key].append(option_value)
    return dict(options_by_set)


def get_variant_relevant_parameters(parameters: list[Parameter]) -> list[Parameter]:
    """Filtert Parameter, die fuer Variantenkombinationen relevant sind."""
    return [parameter for parameter in parameters if parameter.is_variant_relevant]


def calculate_theoretical_variant_count(parameters: list[Parameter], option_values: list[OptionValue]) -> int:
    """Berechnet das Produkt aktiver Optionswerte je variantenrelevantem Parameter."""
    relevant_parameters = get_variant_relevant_parameters(parameters)
    if not relevant_parameters:
        return 0

    options_by_set = group_active_options_by_set(option_values)
    variant_count = 1
    for parameter in relevant_parameters:
        active_options = options_by_set.get(parameter.option_set_key, [])
        if not active_options:
            return 0
        variant_count *= len(active_options)

    return variant_count
