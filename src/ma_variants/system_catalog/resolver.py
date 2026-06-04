"""Aufloesung generischer Systemtemplate-Entscheidungen."""

from __future__ import annotations

from ..variant_manager import Variant, VariantValue
from .models import (
    DependencyRule,
    ResolvedSystemTemplateValue,
    SystemTemplate,
    SystemTemplateResolution,
    SystemTemplateValue,
)


class SystemTemplateResolutionError(ValueError):
    """Fehler bei der Systemtemplate-Aufloesung."""


def _unique_in_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def find_referenced_system_templates(
    variant_values: list[VariantValue],
    system_templates: list[SystemTemplate],
) -> list[str]:
    """Findet Systemtemplates, auf die eine Variante ueber Option oder Wert verweist."""
    active_template_keys = {
        system_template.system_template_key
        for system_template in system_templates
        if system_template.is_active
    }
    referenced_keys: list[str] = []
    for variant_value in variant_values:
        candidate_keys = [
            variant_value.option_key,
            str(variant_value.resolved_value),
        ]
        referenced_keys.extend(candidate_key for candidate_key in candidate_keys if candidate_key in active_template_keys)
    return _unique_in_order(referenced_keys)


def _dependency_warnings(
    selected_template_keys: list[str],
    dependency_rules: list[DependencyRule],
) -> list[str]:
    selected_key_set = set(selected_template_keys)
    warnings: list[str] = []
    for dependency_rule in dependency_rules:
        if not dependency_rule.is_active:
            continue
        if dependency_rule.system_template_key not in selected_key_set:
            continue
        if dependency_rule.required_system_template_key in selected_key_set:
            continue
        warnings.append(
            f"Template '{dependency_rule.system_template_key}' benoetigt "
            f"'{dependency_rule.required_system_template_key}': {dependency_rule.description}"
        )
    return warnings


def resolve_system_templates_for_variant(
    variant: Variant,
    variant_values: list[VariantValue],
    system_templates: list[SystemTemplate],
    system_template_values: list[SystemTemplateValue],
    dependency_rules: list[DependencyRule] | None = None,
    fail_on_dependency_warnings: bool = True,
) -> SystemTemplateResolution:
    """Loest referenzierte Systemtemplates einer Variante zu konkreten Parameterwerten auf."""
    selected_template_keys = find_referenced_system_templates(variant_values, system_templates)
    warnings = _dependency_warnings(selected_template_keys, dependency_rules or [])
    if warnings and fail_on_dependency_warnings:
        raise SystemTemplateResolutionError("; ".join(warnings))

    values_by_template: dict[str, list[SystemTemplateValue]] = {}
    for template_value in system_template_values:
        values_by_template.setdefault(template_value.system_template_key, []).append(template_value)

    resolved_values = [
        ResolvedSystemTemplateValue(
            variant_key=variant.variant_key,
            system_template_key=template_key,
            parameter_key=template_value.parameter_key,
            resolved_value=template_value.value,
            unit=template_value.unit,
            value_source=template_value.value_source,
        )
        for template_key in selected_template_keys
        for template_value in values_by_template.get(template_key, [])
    ]

    return SystemTemplateResolution(
        variant_key=variant.variant_key,
        selected_template_keys=selected_template_keys,
        resolved_values=resolved_values,
        dependency_warnings=warnings,
    )


def resolve_system_templates_for_variants(
    generated_variants: list[tuple[Variant, list[VariantValue]]],
    system_templates: list[SystemTemplate],
    system_template_values: list[SystemTemplateValue],
    dependency_rules: list[DependencyRule] | None = None,
    fail_on_dependency_warnings: bool = True,
) -> dict[str, SystemTemplateResolution]:
    """Loest Systemtemplates fuer mehrere Varianten auf."""
    return {
        variant.variant_key: resolve_system_templates_for_variant(
            variant=variant,
            variant_values=variant_values,
            system_templates=system_templates,
            system_template_values=system_template_values,
            dependency_rules=dependency_rules,
            fail_on_dependency_warnings=fail_on_dependency_warnings,
        )
        for variant, variant_values in generated_variants
    }
