"""Datenmodelle fuer Varianten und Variantenwerte."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..validation import require_non_empty, require_present


@dataclass(frozen=True, slots=True)
class Variant:
    """Beschreibt eine konkrete Variante mit technischem Key und lesbarem Namen."""

    variant_key: str
    variant_name: str
    status: str

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.variant_key, "variant_key", model_name)
        require_non_empty(self.variant_name, "variant_name", model_name)
        require_non_empty(self.status, "status", model_name)


@dataclass(frozen=True, slots=True)
class VariantValue:
    """Verknuepft eine Variante mit einem Parameter und einem Optionswert."""

    variant_key: str
    parameter_key: str
    option_key: str
    resolved_value: Any

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.variant_key, "variant_key", model_name)
        require_non_empty(self.parameter_key, "parameter_key", model_name)
        require_non_empty(self.option_key, "option_key", model_name)
        require_present(self.resolved_value, "resolved_value", model_name)
