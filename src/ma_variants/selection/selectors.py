"""Manuelle, regelbasierte und reproduzierbare Zufallsauswahl."""

from __future__ import annotations

from random import Random
from typing import Iterable

from ..variant_manager import Variant, VariantValue

GeneratedVariant = tuple[Variant, list[VariantValue]]


def select_variants_by_key(
    generated_variants: list[GeneratedVariant],
    variant_keys: Iterable[str],
) -> list[GeneratedVariant]:
    """Waehlt Varianten in der Reihenfolge der uebergebenen Variantenschluessel."""
    variants_by_key = {variant.variant_key: (variant, values) for variant, values in generated_variants}
    selected: list[GeneratedVariant] = []
    missing_keys: list[str] = []

    for variant_key in variant_keys:
        if variant_key not in variants_by_key:
            missing_keys.append(variant_key)
            continue
        selected.append(variants_by_key[variant_key])

    if missing_keys:
        raise ValueError(f"Unbekannte variant_key Werte: {', '.join(missing_keys)}")

    return selected


def _normalize_allowed_options(option_keys: str | Iterable[str]) -> set[str]:
    if isinstance(option_keys, str):
        return {option_keys}
    return set(option_keys)


def filter_variants_by_options(
    generated_variants: list[GeneratedVariant],
    criteria: dict[str, str | Iterable[str]],
) -> list[GeneratedVariant]:
    """Filtert Varianten nach Parameter-Key und erlaubten Option-Keys."""
    normalized_criteria = {
        parameter_key: _normalize_allowed_options(option_keys) for parameter_key, option_keys in criteria.items()
    }
    selected: list[GeneratedVariant] = []

    for variant, values in generated_variants:
        option_by_parameter = {value.parameter_key: value.option_key for value in values}
        if all(
            option_by_parameter.get(parameter_key) in allowed_options
            for parameter_key, allowed_options in normalized_criteria.items()
        ):
            selected.append((variant, values))

    return selected


def random_select_variants(
    generated_variants: list[GeneratedVariant],
    count: int,
    random_seed: int,
) -> list[GeneratedVariant]:
    """Waehlt reproduzierbar eine zufaellige Teilmenge erzeugter Varianten."""
    if count < 0:
        raise ValueError("count darf nicht negativ sein.")
    if count >= len(generated_variants):
        return list(generated_variants)

    random = Random(random_seed)
    return random.sample(generated_variants, count)
