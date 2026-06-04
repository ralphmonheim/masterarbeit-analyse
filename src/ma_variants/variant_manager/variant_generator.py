"""Erzeugung einfacher Variantenkombinationen."""

from __future__ import annotations

import json
from dataclasses import asdict
from itertools import product
from pathlib import Path

from ..option_catalog import OptionValue
from ..parameter_catalog import Parameter
from .models import Variant, VariantValue
from .variant_counter import get_variant_relevant_parameters, group_active_options_by_set


def build_variant_key(index: int) -> str:
    """Erzeugt einen stabilen einfachen Varianten-Key fuer Beispielvarianten."""
    return f"variant_{index:04d}"


def build_variant_name(index: int, selected_options: tuple[OptionValue, ...]) -> str:
    """Erzeugt einen lesbaren Beispielnamen aus aktiven Optionswerten."""
    option_labels = " / ".join(option_value.label for option_value in selected_options)
    return f"Variante {index:04d}: {option_labels}"


def generate_variants(
    parameters: list[Parameter],
    option_values: list[OptionValue],
    status: str = "generated",
) -> list[tuple[Variant, list[VariantValue]]]:
    """Erzeugt einfache In-Memory-Varianten aus aktiven Parameter-/Optionskombinationen."""
    relevant_parameters = get_variant_relevant_parameters(parameters)
    if not relevant_parameters:
        return []

    options_by_set = group_active_options_by_set(option_values)
    option_groups: list[list[OptionValue]] = []
    for parameter in relevant_parameters:
        active_options = options_by_set.get(parameter.option_set_key, [])
        if not active_options:
            return []
        option_groups.append(active_options)

    variants: list[tuple[Variant, list[VariantValue]]] = []
    for index, selected_options in enumerate(product(*option_groups), start=1):
        variant_key = build_variant_key(index)
        variant = Variant(
            variant_key=variant_key,
            variant_name=build_variant_name(index, selected_options),
            status=status,
        )
        values = [
            VariantValue(
                variant_key=variant_key,
                parameter_key=parameter.parameter_key,
                option_key=option_value.option_key,
                resolved_value=option_value.value,
            )
            for parameter, option_value in zip(relevant_parameters, selected_options, strict=True)
        ]
        variants.append((variant, values))

    return variants


def export_variants_to_json(
    generated_variants: list[tuple[Variant, list[VariantValue]]],
    output_path: str | Path,
) -> Path:
    """Exportiert erzeugte Beispielvarianten als JSON."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "variant_count": len(generated_variants),
        "variants": [
            {
                **asdict(variant),
                "values": [asdict(variant_value) for variant_value in variant_values],
            }
            for variant, variant_values in generated_variants
        ],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
