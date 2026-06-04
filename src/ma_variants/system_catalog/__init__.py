"""Systemtemplates und einfache Template-Aufloesung."""

from .importer import import_system_catalog
from .models import (
    DependencyRule,
    ResolvedSystemTemplateValue,
    SystemCatalogImportResult,
    SystemTemplate,
    SystemTemplateResolution,
    SystemTemplateValue,
)
from .resolver import (
    SystemTemplateResolutionError,
    find_referenced_system_templates,
    resolve_system_templates_for_variant,
    resolve_system_templates_for_variants,
)

__all__ = [
    "DependencyRule",
    "ResolvedSystemTemplateValue",
    "SystemCatalogImportResult",
    "SystemTemplate",
    "SystemTemplateResolution",
    "SystemTemplateResolutionError",
    "SystemTemplateValue",
    "find_referenced_system_templates",
    "import_system_catalog",
    "resolve_system_templates_for_variant",
    "resolve_system_templates_for_variants",
]
