"""Datenmodelle fuer Parameterdefinitionen."""

from __future__ import annotations

from dataclasses import dataclass

from ..validation import require_bool, require_non_empty


@dataclass(frozen=True, slots=True)
class Parameter:
    """Beschreibt einen technisch referenzierbaren Projektparameter."""

    parameter_key: str
    display_name: str
    category: str
    parameter_class: str
    option_set_key: str
    unit: str
    is_variant_relevant: bool
    is_naming_relevant: bool
    is_export_relevant: bool

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.parameter_key, "parameter_key", model_name)
        require_non_empty(self.display_name, "display_name", model_name)
        require_non_empty(self.category, "category", model_name)
        require_non_empty(self.parameter_class, "parameter_class", model_name)
        require_non_empty(self.option_set_key, "option_set_key", model_name)
        require_non_empty(self.unit, "unit", model_name)
        require_bool(self.is_variant_relevant, "is_variant_relevant", model_name)
        require_bool(self.is_naming_relevant, "is_naming_relevant", model_name)
        require_bool(self.is_export_relevant, "is_export_relevant", model_name)
