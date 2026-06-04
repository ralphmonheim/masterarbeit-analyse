"""Produktkatalog fuer spaetere detaillierte Variantenbewertungen."""

from .importer import ProductCatalogImportResult, import_products
from .models import Product, ProductProperty

__all__ = [
    "Product",
    "ProductCatalogImportResult",
    "ProductProperty",
    "import_products",
]
