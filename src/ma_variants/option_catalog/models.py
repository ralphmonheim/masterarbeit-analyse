"""Datenmodelle fuer Optionsgruppen und Optionswerte."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..validation import require_bool, require_non_empty, require_present


@dataclass(frozen=True, slots=True)
class OptionSet:
    """Buendelt moegliche Werte fuer einen Parameter."""

    option_set_key: str
    display_name: str
    description: str

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.option_set_key, "option_set_key", model_name)
        require_non_empty(self.display_name, "display_name", model_name)
        require_non_empty(self.description, "description", model_name)


@dataclass(frozen=True, slots=True)
class OptionValue:
    """Beschreibt einen waehlbaren Wert innerhalb einer Optionsgruppe."""

    option_key: str
    option_set_key: str
    label: str
    value: Any
    unit: str
    is_active: bool

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.option_key, "option_key", model_name)
        require_non_empty(self.option_set_key, "option_set_key", model_name)
        require_non_empty(self.label, "label", model_name)
        require_present(self.value, "value", model_name)
        require_non_empty(self.unit, "unit", model_name)
        require_bool(self.is_active, "is_active", model_name)
