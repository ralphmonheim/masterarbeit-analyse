"""Read-only demo catalogs for selectable example records."""

from .catalog import (
    CatalogSelection,
    DemoCatalog,
    DemoCatalogRecord,
    load_demo_catalog,
    select_demo_record,
)

__all__ = [
    "CatalogSelection",
    "DemoCatalog",
    "DemoCatalogRecord",
    "load_demo_catalog",
    "select_demo_record",
]
