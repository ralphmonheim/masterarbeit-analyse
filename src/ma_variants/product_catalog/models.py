"""Datenmodelle fuer Produktkataloge."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..validation import require_non_empty, require_present


def _require_non_negative_number(value: float, field_name: str, model_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{model_name}.{field_name} muss ein Zahlenwert sein.")
    if value < 0:
        raise ValueError(f"{model_name}.{field_name} darf nicht negativ sein.")


@dataclass(frozen=True, slots=True)
class Product:
    """Beschreibt ein generisches oder konkretes Produkt fuer Variantenbewertungen."""

    product_key: str
    product_type: str
    manufacturer: str
    product_name: str
    nominal_power: float
    price: float
    currency: str
    gwp_value: float
    gwp_unit: str
    product_url: str
    document_path: str
    source: str
    data_quality: str

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.product_key, "product_key", model_name)
        require_non_empty(self.product_type, "product_type", model_name)
        require_non_empty(self.manufacturer, "manufacturer", model_name)
        require_non_empty(self.product_name, "product_name", model_name)
        _require_non_negative_number(self.nominal_power, "nominal_power", model_name)
        _require_non_negative_number(self.price, "price", model_name)
        require_non_empty(self.currency, "currency", model_name)
        _require_non_negative_number(self.gwp_value, "gwp_value", model_name)
        require_non_empty(self.gwp_unit, "gwp_unit", model_name)
        require_non_empty(self.product_url, "product_url", model_name)
        require_non_empty(self.document_path, "document_path", model_name)
        require_non_empty(self.source, "source", model_name)
        require_non_empty(self.data_quality, "data_quality", model_name)


@dataclass(frozen=True, slots=True)
class ProductProperty:
    """Erweiterbare Produkteigenschaft ohne feste Produkttabelle aufzublaehen."""

    product_key: str
    property_key: str
    value: Any
    unit: str
    source: str
    data_quality: str

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.product_key, "product_key", model_name)
        require_non_empty(self.property_key, "property_key", model_name)
        require_present(self.value, "value", model_name)
        require_non_empty(self.unit, "unit", model_name)
        require_non_empty(self.source, "source", model_name)
        require_non_empty(self.data_quality, "data_quality", model_name)


@dataclass(frozen=True, slots=True)
class ProductCatalogImportResult:
    """Ergebnis eines Produktkatalogimports."""

    products: list[Product]
    product_properties: list[ProductProperty]
    errors: list[str]
    source_path: Path | None = None
