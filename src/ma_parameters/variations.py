"""Referenzkonfigurationen fuer den kontrollierten Variantenraum.

Die Baseline bleibt unveraendert. Dieses Modul beschreibt ausschliesslich,
welche ihrer Werte in einer Variantenstudie veraendert werden duerfen.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ma_core import load_configuration_file

from .models import BaselineParameterSnapshot

DEFAULT_REFERENCE_VARIATION_CONFIG = Path(
    "config/ma_parameters/reference_variations/business_integration_lod1_zone_only.yaml"
)


@dataclass(frozen=True, slots=True)
class VariationArea:
    """Ein Eingabebereich mit expliziter Freigabe oder Sperre."""

    module_key: str
    label: str
    is_locked: bool
    lock_reason: str


@dataclass(frozen=True, slots=True)
class VariationOption:
    """Eine fachlich erlaubte Auspraegung einer Variationsdimension."""

    option_key: str
    label: str
    value: object
    unit: str


@dataclass(frozen=True, slots=True)
class VariationDimension:
    """Ein Parameter oder mehrere fest gekoppelte Parameter."""

    dimension_key: str
    module_key: str
    label: str
    scope_id: str
    target_parameter_keys: tuple[str, ...]
    value_mode: str
    options: tuple[VariationOption, ...]
    is_dimensioning_relevant: bool
    coupling_key: str = ""
    description: str = ""

    @property
    def is_coupled(self) -> bool:
        return len(self.target_parameter_keys) > 1


@dataclass(frozen=True, slots=True)
class ParameterVariationSpecification:
    """Freigegebener Raum fuer eine Variantenstudie."""

    specification_id: str
    baseline_snapshot_id: str
    baseline_content_hash: str
    study_mode: str
    areas: tuple[VariationArea, ...]
    dimensions: tuple[VariationDimension, ...]
    description: str = ""

    @property
    def unlocked_dimensions(self) -> tuple[VariationDimension, ...]:
        locked_modules = {area.module_key for area in self.areas if area.is_locked}
        return tuple(dimension for dimension in self.dimensions if dimension.module_key not in locked_modules)


def load_reference_variation_specification(
    baseline: BaselineParameterSnapshot,
    config_path: str | Path = DEFAULT_REFERENCE_VARIATION_CONFIG,
) -> ParameterVariationSpecification:
    """Laedt die versionierte Thesis-Referenz: nur Zonen sind variierbar."""
    raw = load_configuration_file(config_path)
    areas = tuple(
        VariationArea(
            module_key=str(item["module_key"]),
            label=str(item["label"]),
            is_locked=bool(item["is_locked"]),
            lock_reason=str(item.get("lock_reason", "")),
        )
        for item in _required_list(raw, "areas")
    )
    dimensions = tuple(_dimension_from_raw(item, baseline) for item in _required_list(raw, "dimensions"))
    _validate_reference_specification(areas, dimensions, baseline)
    return ParameterVariationSpecification(
        specification_id=str(raw["specification_id"]),
        baseline_snapshot_id=baseline.snapshot_id,
        baseline_content_hash=baseline.content_hash,
        study_mode=str(raw.get("study_mode", "variant_study")),
        areas=areas,
        dimensions=dimensions,
        description=str(raw.get("description", "")),
    )


def variation_area_rows(specification: ParameterVariationSpecification) -> list[dict[str, object]]:
    """Bereitet den Sperrstatus fuer die Parameteransicht auf."""
    return [
        {
            "Modulbereich": area.label,
            "Modul": area.module_key,
            "Werte dieses Bereichs fuer Varianten sperren": area.is_locked,
            "Begruendung": area.lock_reason,
        }
        for area in specification.areas
    ]


def variation_dimension_rows(specification: ParameterVariationSpecification) -> list[dict[str, object]]:
    """Zeigt jede zulässige Variationsdimension genau einmal."""
    locked_modules = {area.module_key for area in specification.areas if area.is_locked}
    rows: list[dict[str, object]] = []
    for dimension in specification.dimensions:
        rows.append(
            {
                "Modulbereich": dimension.module_key,
                "Parameter": dimension.label,
                "Scope": dimension.scope_id,
                "Werteform": dimension.value_mode,
                "Moegliche Werte": ", ".join(option.label for option in dimension.options),
                "Gekoppelte Zielwerte": ", ".join(dimension.target_parameter_keys),
                "Fuer Varianten gesperrt": dimension.module_key in locked_modules,
                "Dimensionsrelevant": dimension.is_dimensioning_relevant,
                "Beschreibung": dimension.description,
            }
        )
    return rows


def _required_list(raw: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = raw.get(key)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"Referenzkonfiguration benoetigt eine Liste '{key}'.")
    return value


def _required_string_list(raw: dict[str, Any], key: str) -> tuple[str, ...]:
    value = raw.get(key)
    if not isinstance(value, list) or not all(str(item).strip() for item in value):
        raise ValueError(f"Referenzkonfiguration benoetigt eine nicht leere Liste '{key}'.")
    return tuple(str(item) for item in value)


def _dimension_from_raw(raw: dict[str, Any], baseline: BaselineParameterSnapshot) -> VariationDimension:
    target_parameter_keys = _required_string_list(raw, "target_parameter_keys")
    options = tuple(
        VariationOption(
            option_key=str(option["option_key"]),
            label=str(option["label"]),
            value=option["value"],
            unit=str(option["unit"]),
        )
        for option in _required_list(raw, "options")
    )
    return VariationDimension(
        dimension_key=str(raw["dimension_key"]),
        module_key=str(raw["module_key"]),
        label=str(raw["label"]),
        scope_id=str(raw["scope_id"]),
        target_parameter_keys=target_parameter_keys,
        value_mode=str(raw["value_mode"]),
        options=options,
        is_dimensioning_relevant=bool(raw.get("is_dimensioning_relevant", False)),
        coupling_key=str(raw.get("coupling_key", "")),
        description=str(raw.get("description", "")),
    )


def _validate_reference_specification(
    areas: tuple[VariationArea, ...],
    dimensions: tuple[VariationDimension, ...],
    baseline: BaselineParameterSnapshot,
) -> None:
    if len({area.module_key for area in areas}) != len(areas):
        raise ValueError("Jeder Modulbereich darf nur einmal vorkommen.")
    if len({dimension.dimension_key for dimension in dimensions}) != len(dimensions):
        raise ValueError("Jede Variationsdimension benoetigt einen eindeutigen Key.")
    known_keys = {value.parameter_key for value in baseline.parameter_values}
    for dimension in dimensions:
        if dimension.module_key not in {area.module_key for area in areas}:
            raise ValueError(f"Variationsdimension '{dimension.dimension_key}' hat keinen Modulbereich.")
        missing_keys = set(dimension.target_parameter_keys) - known_keys
        if missing_keys:
            raise ValueError(
                f"Variationsdimension '{dimension.dimension_key}' referenziert unbekannte Baseline-Werte: "
                f"{', '.join(sorted(missing_keys))}."
            )
        if not dimension.options:
            raise ValueError(f"Variationsdimension '{dimension.dimension_key}' benoetigt Optionen.")
