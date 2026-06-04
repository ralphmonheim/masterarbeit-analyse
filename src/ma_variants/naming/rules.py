"""Laden und Validieren einfacher Namensregeln."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..importing.io import load_config_file
from ..validation import require_bool, require_non_empty, require_present


@dataclass(frozen=True, slots=True)
class NamingRulePart:
    """Beschreibt einen Parameterteil im generierten Variantennamen."""

    parameter_key: str
    option_tokens: dict[str, str]

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.parameter_key, "parameter_key", model_name)
        require_present(self.option_tokens, "option_tokens", model_name)
        if not isinstance(self.option_tokens, dict) or not self.option_tokens:
            raise ValueError("NamingRulePart.option_tokens muss ein nicht leeres Objekt sein.")
        for option_key, token in self.option_tokens.items():
            require_non_empty(option_key, "option_tokens option_key", model_name)
            require_non_empty(token, f"option_tokens[{option_key}]", model_name)


@dataclass(frozen=True, slots=True)
class NamingRules:
    """Konfiguration fuer kurze, reproduzierbare Variantennamen."""

    prefix: str
    index_width: int
    separator: str
    include_index: bool
    parts: list[NamingRulePart]

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.prefix, "prefix", model_name)
        require_non_empty(self.separator, "separator", model_name)
        require_bool(self.include_index, "include_index", model_name)
        if not isinstance(self.index_width, int) or self.index_width < 1:
            raise ValueError("NamingRules.index_width muss eine positive ganze Zahl sein.")
        if not self.parts:
            raise ValueError("NamingRules.parts darf nicht leer sein.")


def load_naming_rules(config_path: str | Path) -> NamingRules:
    """Laedt Namensregeln aus einer kleinen YAML- oder JSON-Datei."""
    data = load_config_file(config_path)
    raw_rules = data.get("naming")
    if not isinstance(raw_rules, dict):
        raise ValueError("Konfiguration muss ein Objekt 'naming' enthalten.")

    raw_parts = raw_rules.get("parts")
    if not isinstance(raw_parts, list):
        raise ValueError("naming.parts muss eine Liste sein.")

    parts = [
        NamingRulePart(
            parameter_key=raw_part.get("parameter_key", ""),
            option_tokens=raw_part.get("option_tokens", {}),
        )
        for raw_part in raw_parts
    ]
    return NamingRules(
        prefix=raw_rules.get("prefix", "V"),
        index_width=raw_rules.get("index_width", 3),
        separator=raw_rules.get("separator", "_"),
        include_index=raw_rules.get("include_index", True),
        parts=parts,
    )
