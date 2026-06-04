"""Namensregeln und einfache Variantennamensgenerierung."""

from .generator import (
    DuplicateVariantNameError,
    apply_variant_names,
    assert_unique_variant_names,
    generate_variant_name,
)
from .rules import NamingRulePart, NamingRules, load_naming_rules

__all__ = [
    "DuplicateVariantNameError",
    "NamingRulePart",
    "NamingRules",
    "apply_variant_names",
    "assert_unique_variant_names",
    "generate_variant_name",
    "load_naming_rules",
]
