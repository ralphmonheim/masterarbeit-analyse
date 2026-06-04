"""Importer fuer Parameterkonfigurationen."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..importing.io import load_config_file
from .models import Parameter

PARAMETER_REQUIRED_FIELDS = (
    "parameter_key",
    "display_name",
    "category",
    "parameter_class",
    "option_set_key",
    "unit",
    "is_variant_relevant",
    "is_naming_relevant",
    "is_export_relevant",
)


def _missing_fields(raw_item: dict[str, Any], required_fields: tuple[str, ...]) -> list[str]:
    return [field for field in required_fields if field not in raw_item]


def import_parameters(config_path: str | Path) -> tuple[list[Parameter], list[str]]:
    """Laedt Parameter und liefert gueltige Objekte plus Validierungsfehler."""
    data = load_config_file(config_path)
    raw_parameters = data.get("parameters")
    if not isinstance(raw_parameters, list):
        return [], ["Konfiguration muss eine Liste 'parameters' enthalten."]

    parameters: list[Parameter] = []
    errors: list[str] = []
    seen_keys: set[str] = set()

    for index, raw_parameter in enumerate(raw_parameters, start=1):
        item_label = f"parameters[{index}]"
        if not isinstance(raw_parameter, dict):
            errors.append(f"{item_label} muss ein Objekt sein.")
            continue

        missing = _missing_fields(raw_parameter, PARAMETER_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{item_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue

        parameter_key = str(raw_parameter["parameter_key"]).strip()
        if parameter_key in seen_keys:
            errors.append(f"Doppelter parameter_key '{parameter_key}'.")
            continue
        seen_keys.add(parameter_key)

        try:
            parameters.append(Parameter(**{field: raw_parameter[field] for field in PARAMETER_REQUIRED_FIELDS}))
        except ValueError as exc:
            errors.append(f"{item_label}: {exc}")

    return parameters, errors
