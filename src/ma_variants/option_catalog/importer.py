"""Importer fuer Optionsgruppen und Optionswerte."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..importing.io import load_config_file
from .models import OptionSet, OptionValue

OPTION_SET_REQUIRED_FIELDS = (
    "option_set_key",
    "display_name",
    "description",
)
OPTION_VALUE_REQUIRED_FIELDS = (
    "option_key",
    "label",
    "value",
    "unit",
    "is_active",
)


def _missing_fields(raw_item: dict[str, Any], required_fields: tuple[str, ...]) -> list[str]:
    return [field for field in required_fields if field not in raw_item]


def import_options(config_path: str | Path) -> tuple[list[OptionSet], list[OptionValue], list[str]]:
    """Laedt Optionsgruppen und Optionswerte aus einer Konfiguration."""
    data = load_config_file(config_path)
    raw_option_sets = data.get("option_sets")
    if not isinstance(raw_option_sets, list):
        return [], [], ["Konfiguration muss eine Liste 'option_sets' enthalten."]

    option_sets: list[OptionSet] = []
    option_values: list[OptionValue] = []
    errors: list[str] = []
    seen_option_set_keys: set[str] = set()
    seen_option_keys: set[str] = set()

    for set_index, raw_option_set in enumerate(raw_option_sets, start=1):
        set_label = f"option_sets[{set_index}]"
        if not isinstance(raw_option_set, dict):
            errors.append(f"{set_label} muss ein Objekt sein.")
            continue

        missing = _missing_fields(raw_option_set, OPTION_SET_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{set_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue

        option_set_key = str(raw_option_set["option_set_key"]).strip()
        if option_set_key in seen_option_set_keys:
            errors.append(f"Doppelter option_set_key '{option_set_key}'.")
            continue
        seen_option_set_keys.add(option_set_key)

        try:
            option_sets.append(OptionSet(**{field: raw_option_set[field] for field in OPTION_SET_REQUIRED_FIELDS}))
        except ValueError as exc:
            errors.append(f"{set_label}: {exc}")
            continue

        raw_values = raw_option_set.get("values")
        if not isinstance(raw_values, list) or not raw_values:
            errors.append(f"{set_label} muss eine nicht leere Liste 'values' enthalten.")
            continue

        for value_index, raw_value in enumerate(raw_values, start=1):
            value_label = f"{set_label}.values[{value_index}]"
            if not isinstance(raw_value, dict):
                errors.append(f"{value_label} muss ein Objekt sein.")
                continue

            value_missing = _missing_fields(raw_value, OPTION_VALUE_REQUIRED_FIELDS)
            if value_missing:
                errors.append(f"{value_label} fehlt Pflichtfeld(er): {', '.join(value_missing)}.")
                continue

            option_key = str(raw_value["option_key"]).strip()
            if option_key in seen_option_keys:
                errors.append(f"Doppelter option_key '{option_key}'.")
                continue
            seen_option_keys.add(option_key)

            payload = {field: raw_value[field] for field in OPTION_VALUE_REQUIRED_FIELDS}
            payload["option_set_key"] = option_set_key
            try:
                option_values.append(OptionValue(**payload))
            except ValueError as exc:
                errors.append(f"{value_label}: {exc}")

    return option_sets, option_values, errors
