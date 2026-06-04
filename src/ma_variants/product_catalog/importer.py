"""Importer fuer Produktkataloge aus YAML, JSON oder CSV."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from ..importing.io import load_config_file
from .models import Product, ProductCatalogImportResult, ProductProperty

PRODUCT_REQUIRED_FIELDS = (
    "product_key",
    "product_type",
    "manufacturer",
    "product_name",
    "nominal_power",
    "price",
    "currency",
    "gwp_value",
    "gwp_unit",
    "product_url",
    "document_path",
    "source",
    "data_quality",
)
PRODUCT_PROPERTY_REQUIRED_FIELDS = (
    "product_key",
    "property_key",
    "value",
    "unit",
    "source",
    "data_quality",
)
PRODUCT_NUMERIC_FIELDS = {"nominal_power", "price", "gwp_value"}


def _missing_fields(raw_item: dict[str, Any], required_fields: tuple[str, ...]) -> list[str]:
    return [field for field in required_fields if field not in raw_item]


def _coerce_product_payload(raw_item: dict[str, Any]) -> dict[str, Any]:
    payload = {field: raw_item[field] for field in PRODUCT_REQUIRED_FIELDS}
    for field in PRODUCT_NUMERIC_FIELDS:
        payload[field] = float(payload[field])
    return payload


def _load_raw_products(config_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    if config_path.suffix.lower() == ".csv":
        with config_path.open(encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file)), [], []

    data = load_config_file(config_path)
    raw_products = data.get("products")
    if not isinstance(raw_products, list):
        return [], [], ["Konfiguration muss eine Liste 'products' enthalten."]

    raw_properties = data.get("product_properties", [])
    if not isinstance(raw_properties, list):
        return raw_products, [], ["Konfiguration 'product_properties' muss eine Liste sein."]
    return raw_products, raw_properties, []


def _import_product_properties(
    raw_items: list[dict[str, Any]],
    known_product_keys: set[str],
) -> tuple[list[ProductProperty], list[str]]:
    properties: list[ProductProperty] = []
    errors: list[str] = []
    seen_keys: set[tuple[str, str]] = set()

    for index, raw_item in enumerate(raw_items, start=1):
        item_label = f"product_properties[{index}]"
        if not isinstance(raw_item, dict):
            errors.append(f"{item_label} muss ein Objekt sein.")
            continue

        missing = _missing_fields(raw_item, PRODUCT_PROPERTY_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{item_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue

        product_key = str(raw_item["product_key"]).strip()
        property_key = str(raw_item["property_key"]).strip()
        if product_key not in known_product_keys:
            errors.append(f"{item_label} referenziert unbekannten product_key '{product_key}'.")
            continue
        if (product_key, property_key) in seen_keys:
            errors.append(f"Doppelte ProductProperty '{product_key}/{property_key}'.")
            continue
        seen_keys.add((product_key, property_key))

        try:
            properties.append(
                ProductProperty(**{field: raw_item[field] for field in PRODUCT_PROPERTY_REQUIRED_FIELDS})
            )
        except ValueError as exc:
            errors.append(f"{item_label}: {exc}")
    return properties, errors


def import_products(config_path: str | Path) -> ProductCatalogImportResult:
    """Laedt Produkte und optionale Produkteigenschaften aus YAML, JSON oder CSV."""
    path = Path(config_path)
    raw_products, raw_properties, errors = _load_raw_products(path)
    products: list[Product] = []
    seen_product_keys: set[str] = set()

    for index, raw_item in enumerate(raw_products, start=1):
        item_label = f"products[{index}]"
        if not isinstance(raw_item, dict):
            errors.append(f"{item_label} muss ein Objekt sein.")
            continue

        missing = _missing_fields(raw_item, PRODUCT_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{item_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue

        product_key = str(raw_item["product_key"]).strip()
        if product_key in seen_product_keys:
            errors.append(f"Doppelter product_key '{product_key}'.")
            continue
        seen_product_keys.add(product_key)

        try:
            products.append(Product(**_coerce_product_payload(raw_item)))
        except (TypeError, ValueError) as exc:
            errors.append(f"{item_label}: {exc}")

    product_properties, property_errors = _import_product_properties(raw_properties, seen_product_keys)
    errors.extend(property_errors)

    return ProductCatalogImportResult(
        products=products,
        product_properties=product_properties,
        errors=errors,
        source_path=path,
    )
