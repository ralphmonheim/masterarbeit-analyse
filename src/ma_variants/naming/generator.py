"""Einfache, reproduzierbare Namensgenerierung fuer Varianten."""

from __future__ import annotations

from dataclasses import replace

from ..variant_manager import Variant, VariantValue
from .rules import NamingRules

GeneratedVariant = tuple[Variant, list[VariantValue]]


class DuplicateVariantNameError(ValueError):
    """Fehler fuer doppelte generierte Variantennamen."""


def generate_variant_name(index: int, variant_values: list[VariantValue], naming_rules: NamingRules) -> str:
    """Erzeugt einen kurzen Namen aus Index und konfigurierten Optionstokens."""
    values_by_parameter = {variant_value.parameter_key: variant_value for variant_value in variant_values}
    name_parts: list[str] = []

    if naming_rules.include_index:
        name_parts.append(f"{naming_rules.prefix}{index:0{naming_rules.index_width}d}")
    else:
        name_parts.append(naming_rules.prefix)

    for rule_part in naming_rules.parts:
        variant_value = values_by_parameter.get(rule_part.parameter_key)
        if variant_value is None:
            raise ValueError(f"Parameter '{rule_part.parameter_key}' fehlt in Variantendaten.")
        token = rule_part.option_tokens.get(variant_value.option_key)
        if token is None:
            raise ValueError(
                f"Kein Namenstoken fuer option_key '{variant_value.option_key}' "
                f"bei parameter_key '{rule_part.parameter_key}'."
            )
        name_parts.append(token)

    return naming_rules.separator.join(name_parts)


def assert_unique_variant_names(generated_variants: list[GeneratedVariant]) -> None:
    """Prueft, ob alle Variantennamen eindeutig sind."""
    seen_names: set[str] = set()
    duplicate_names: set[str] = set()
    for variant, _values in generated_variants:
        if variant.variant_name in seen_names:
            duplicate_names.add(variant.variant_name)
        seen_names.add(variant.variant_name)

    if duplicate_names:
        raise DuplicateVariantNameError(f"Doppelte Variantennamen: {', '.join(sorted(duplicate_names))}")


def apply_variant_names(
    generated_variants: list[GeneratedVariant],
    naming_rules: NamingRules,
) -> list[GeneratedVariant]:
    """Ersetzt lesbare Variantennamen durch reproduzierbare Namen gemaess Regeln."""
    named_variants = [
        (
            replace(variant, variant_name=generate_variant_name(index, values, naming_rules)),
            values,
        )
        for index, (variant, values) in enumerate(generated_variants, start=1)
    ]
    assert_unique_variant_names(named_variants)
    return named_variants
