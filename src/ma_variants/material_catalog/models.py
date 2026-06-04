"""Datenmodelle fuer Materialkataloge."""

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
class Material:
    """Beschreibt ein Material fuer spaetere Detailbewertungen."""

    material_key: str
    material_group: str
    material_name: str
    density: float
    lambda_value: float
    specific_heat_capacity: float
    price: float
    gwp_value: float
    gwp_unit: str
    document_path: str
    source: str
    data_quality: str

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.material_key, "material_key", model_name)
        require_non_empty(self.material_group, "material_group", model_name)
        require_non_empty(self.material_name, "material_name", model_name)
        _require_non_negative_number(self.density, "density", model_name)
        _require_non_negative_number(self.lambda_value, "lambda_value", model_name)
        _require_non_negative_number(self.specific_heat_capacity, "specific_heat_capacity", model_name)
        _require_non_negative_number(self.price, "price", model_name)
        _require_non_negative_number(self.gwp_value, "gwp_value", model_name)
        require_non_empty(self.gwp_unit, "gwp_unit", model_name)
        require_non_empty(self.document_path, "document_path", model_name)
        require_non_empty(self.source, "source", model_name)
        require_non_empty(self.data_quality, "data_quality", model_name)


@dataclass(frozen=True, slots=True)
class MaterialProperty:
    """Erweiterbare Materialeigenschaft."""

    material_key: str
    property_key: str
    value: Any
    unit: str
    source: str
    data_quality: str

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.material_key, "material_key", model_name)
        require_non_empty(self.property_key, "property_key", model_name)
        require_present(self.value, "value", model_name)
        require_non_empty(self.unit, "unit", model_name)
        require_non_empty(self.source, "source", model_name)
        require_non_empty(self.data_quality, "data_quality", model_name)


@dataclass(frozen=True, slots=True)
class MaterialCatalogImportResult:
    """Ergebnis eines Materialkatalogimports."""

    materials: list[Material]
    material_properties: list[MaterialProperty]
    errors: list[str]
    source_path: Path | None = None
