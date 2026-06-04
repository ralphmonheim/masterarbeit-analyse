"""Datenmodelle fuer technische Systemtemplates."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..validation import require_bool, require_non_empty, require_present


@dataclass(frozen=True, slots=True)
class SystemTemplate:
    """Beschreibt eine wiederverwendbare technische Systemvorlage."""

    system_template_key: str
    display_name: str
    system_type: str
    description: str
    is_active: bool

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.system_template_key, "system_template_key", model_name)
        require_non_empty(self.display_name, "display_name", model_name)
        require_non_empty(self.system_type, "system_type", model_name)
        require_non_empty(self.description, "description", model_name)
        require_bool(self.is_active, "is_active", model_name)


@dataclass(frozen=True, slots=True)
class SystemTemplateValue:
    """Beschreibt einen konkreten Parameterwert innerhalb eines Systemtemplates."""

    system_template_key: str
    parameter_key: str
    value: Any
    unit: str
    value_source: str = "template"

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.system_template_key, "system_template_key", model_name)
        require_non_empty(self.parameter_key, "parameter_key", model_name)
        require_present(self.value, "value", model_name)
        require_non_empty(self.unit, "unit", model_name)
        require_non_empty(self.value_source, "value_source", model_name)


@dataclass(frozen=True, slots=True)
class DependencyRule:
    """Beschreibt eine einfache Template-Abhaengigkeit."""

    rule_key: str
    system_template_key: str
    required_system_template_key: str
    description: str
    is_active: bool

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.rule_key, "rule_key", model_name)
        require_non_empty(self.system_template_key, "system_template_key", model_name)
        require_non_empty(self.required_system_template_key, "required_system_template_key", model_name)
        require_non_empty(self.description, "description", model_name)
        require_bool(self.is_active, "is_active", model_name)


@dataclass(frozen=True, slots=True)
class ResolvedSystemTemplateValue:
    """Ein auf eine konkrete Variante aufgeloester Systemtemplate-Wert."""

    variant_key: str
    system_template_key: str
    parameter_key: str
    resolved_value: Any
    unit: str
    value_source: str


@dataclass(frozen=True, slots=True)
class SystemTemplateResolution:
    """Ergebnis der Template-Aufloesung fuer eine Variante."""

    variant_key: str
    selected_template_keys: list[str]
    resolved_values: list[ResolvedSystemTemplateValue]
    dependency_warnings: list[str]


@dataclass(frozen=True, slots=True)
class SystemCatalogImportResult:
    """Ergebnis eines Systemtemplate-Imports."""

    system_templates: list[SystemTemplate]
    system_template_values: list[SystemTemplateValue]
    dependency_rules: list[DependencyRule]
    errors: list[str]
    source_path: Path | None = None
