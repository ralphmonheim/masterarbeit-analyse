"""Importer fuer kleine Systemtemplate-Konfigurationen."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..importing.io import load_config_file
from .models import (
    DependencyRule,
    SystemCatalogImportResult,
    SystemTemplate,
    SystemTemplateValue,
)

SYSTEM_TEMPLATE_REQUIRED_FIELDS = (
    "system_template_key",
    "display_name",
    "system_type",
    "description",
    "is_active",
)
SYSTEM_TEMPLATE_VALUE_REQUIRED_FIELDS = (
    "parameter_key",
    "value",
    "unit",
)
DEPENDENCY_RULE_REQUIRED_FIELDS = (
    "rule_key",
    "system_template_key",
    "required_system_template_key",
    "description",
    "is_active",
)


def _missing_fields(raw_item: dict[str, Any], required_fields: tuple[str, ...]) -> list[str]:
    return [field for field in required_fields if field not in raw_item]


def import_system_catalog(config_path: str | Path) -> SystemCatalogImportResult:
    """Laedt Systemtemplates, Templatewerte und einfache Abhaengigkeitsregeln."""
    path = Path(config_path)
    data = load_config_file(path)
    raw_templates = data.get("system_templates")
    raw_rules = data.get("dependency_rules", [])

    if not isinstance(raw_templates, list):
        return SystemCatalogImportResult([], [], [], ["Konfiguration muss eine Liste 'system_templates' enthalten."], path)
    if not isinstance(raw_rules, list):
        return SystemCatalogImportResult([], [], [], ["'dependency_rules' muss eine Liste sein."], path)

    templates: list[SystemTemplate] = []
    template_values: list[SystemTemplateValue] = []
    dependency_rules: list[DependencyRule] = []
    errors: list[str] = []
    seen_template_keys: set[str] = set()
    seen_template_value_keys: set[tuple[str, str]] = set()
    seen_rule_keys: set[str] = set()

    for template_index, raw_template in enumerate(raw_templates, start=1):
        template_label = f"system_templates[{template_index}]"
        if not isinstance(raw_template, dict):
            errors.append(f"{template_label} muss ein Objekt sein.")
            continue

        missing = _missing_fields(raw_template, SYSTEM_TEMPLATE_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{template_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue

        template_key = str(raw_template["system_template_key"]).strip()
        if template_key in seen_template_keys:
            errors.append(f"Doppelter system_template_key '{template_key}'.")
            continue
        seen_template_keys.add(template_key)

        try:
            templates.append(
                SystemTemplate(
                    **{field: raw_template[field] for field in SYSTEM_TEMPLATE_REQUIRED_FIELDS}
                )
            )
        except ValueError as exc:
            errors.append(f"{template_label}: {exc}")
            continue

        raw_values = raw_template.get("values")
        if not isinstance(raw_values, list) or not raw_values:
            errors.append(f"{template_label} muss eine nicht leere Liste 'values' enthalten.")
            continue

        for value_index, raw_value in enumerate(raw_values, start=1):
            value_label = f"{template_label}.values[{value_index}]"
            if not isinstance(raw_value, dict):
                errors.append(f"{value_label} muss ein Objekt sein.")
                continue

            value_missing = _missing_fields(raw_value, SYSTEM_TEMPLATE_VALUE_REQUIRED_FIELDS)
            if value_missing:
                errors.append(f"{value_label} fehlt Pflichtfeld(er): {', '.join(value_missing)}.")
                continue

            parameter_key = str(raw_value["parameter_key"]).strip()
            unique_value_key = (template_key, parameter_key)
            if unique_value_key in seen_template_value_keys:
                errors.append(
                    f"Doppelter Systemtemplate-Wert fuer Template '{template_key}' "
                    f"und Parameter '{parameter_key}'."
                )
                continue
            seen_template_value_keys.add(unique_value_key)

            payload = {field: raw_value[field] for field in SYSTEM_TEMPLATE_VALUE_REQUIRED_FIELDS}
            payload["system_template_key"] = template_key
            payload["value_source"] = raw_value.get("value_source", "template")
            try:
                template_values.append(SystemTemplateValue(**payload))
            except ValueError as exc:
                errors.append(f"{value_label}: {exc}")

    for rule_index, raw_rule in enumerate(raw_rules, start=1):
        rule_label = f"dependency_rules[{rule_index}]"
        if not isinstance(raw_rule, dict):
            errors.append(f"{rule_label} muss ein Objekt sein.")
            continue

        missing = _missing_fields(raw_rule, DEPENDENCY_RULE_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{rule_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue

        rule_key = str(raw_rule["rule_key"]).strip()
        if rule_key in seen_rule_keys:
            errors.append(f"Doppelter rule_key '{rule_key}'.")
            continue
        seen_rule_keys.add(rule_key)

        try:
            dependency_rules.append(
                DependencyRule(**{field: raw_rule[field] for field in DEPENDENCY_RULE_REQUIRED_FIELDS})
            )
        except ValueError as exc:
            errors.append(f"{rule_label}: {exc}")

    for dependency_rule in dependency_rules:
        if dependency_rule.system_template_key not in seen_template_keys:
            errors.append(
                "DependencyRule "
                f"'{dependency_rule.rule_key}' referenziert nicht vorhandenes Template "
                f"'{dependency_rule.system_template_key}'."
            )
        if dependency_rule.required_system_template_key not in seen_template_keys:
            errors.append(
                "DependencyRule "
                f"'{dependency_rule.rule_key}' referenziert nicht vorhandenes erforderliches Template "
                f"'{dependency_rule.required_system_template_key}'."
            )

    return SystemCatalogImportResult(
        system_templates=templates,
        system_template_values=template_values,
        dependency_rules=dependency_rules,
        errors=errors,
        source_path=path,
    )
