"""Materialkatalog fuer spaetere detaillierte Variantenbewertungen."""

from .importer import MaterialCatalogImportResult, import_materials
from .models import Material, MaterialProperty

__all__ = [
    "Material",
    "MaterialCatalogImportResult",
    "MaterialProperty",
    "import_materials",
]
