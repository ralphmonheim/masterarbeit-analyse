"""Services fuer die schreibgeschuetzte Parameter- und Optionsdemo."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from ma_core import ConfigurationSaveResult, ConfigurationSource, list_configuration_files, save_yaml_configuration

from .catalogs import OptionSet, OptionValue, Parameter, import_catalog
from .models import ParameterOptionSelection

DEFAULT_PARAMETER_CONFIG = Path("config/ma_variants/parameters/example_parameters.yaml")
DEFAULT_OPTION_CONFIG = Path("config/ma_variants/options/example_options.yaml")
LOCAL_OPTION_DIR = Path("data/ma_parameters/config/options")


def load_parameter_catalog(
    parameter_config: str | Path = DEFAULT_PARAMETER_CONFIG,
    option_config: str | Path = DEFAULT_OPTION_CONFIG,
    *,
    option_is_template: bool = True,
) -> tuple[list[Parameter], list[OptionSet], list[OptionValue], ParameterOptionSelection]:
    """Laedt die bestehenden Kataloge und leitet die aktive Optionsauswahl ab."""
    catalog = import_catalog(parameter_config, option_config, report_path=None)
    active_by_set: dict[str, tuple[str, ...]] = {}
    for option_set in catalog.option_sets:
        active_by_set[option_set.option_set_key] = tuple(
            option.option_key
            for option in catalog.option_values
            if option.option_set_key == option_set.option_set_key and option.is_active
        )
    selection = ParameterOptionSelection(
        active_option_keys_by_set=active_by_set,
        source=ConfigurationSource(path=Path(option_config), is_template=option_is_template),
    )
    validate_option_selection(catalog.parameters, catalog.option_sets, catalog.option_values, selection)
    return catalog.parameters, catalog.option_sets, catalog.option_values, selection


def validate_option_selection(
    parameters: list[Parameter],
    option_sets: list[OptionSet],
    option_values: list[OptionValue],
    selection: ParameterOptionSelection,
) -> None:
    """Validiert Vollstaendigkeit und Referenzen der aktiven Optionswerte."""
    known_sets = {option_set.option_set_key for option_set in option_sets}
    unknown_sets = set(selection.active_option_keys_by_set) - known_sets
    if unknown_sets:
        raise ValueError(f"Unbekannte Optionsgruppen: {', '.join(sorted(unknown_sets))}")

    options_by_set: dict[str, set[str]] = {option_set_key: set() for option_set_key in known_sets}
    for option in option_values:
        if option.option_set_key not in known_sets:
            raise ValueError(f"Optionswert '{option.option_key}' verweist auf eine unbekannte Optionsgruppe.")
        options_by_set[option.option_set_key].add(option.option_key)

    for option_set_key, selected_keys in selection.active_option_keys_by_set.items():
        unknown_options = set(selected_keys) - options_by_set[option_set_key]
        if unknown_options:
            raise ValueError(f"Unbekannte Optionswerte in '{option_set_key}': {', '.join(sorted(unknown_options))}")

    relevant_sets = {parameter.option_set_key for parameter in parameters if parameter.is_variant_relevant}
    for option_set_key in sorted(relevant_sets):
        if option_set_key not in known_sets:
            raise ValueError(f"Variantenrelevante Optionsgruppe fehlt: {option_set_key}")
        if not selection.active_option_keys_by_set.get(option_set_key):
            raise ValueError(
                f"Variantenrelevante Optionsgruppe '{option_set_key}' benoetigt mindestens einen aktiven Wert."
            )


def apply_option_selection(
    parameters: list[Parameter],
    option_sets: list[OptionSet],
    option_values: list[OptionValue],
    selection: ParameterOptionSelection,
) -> list[OptionValue]:
    """Uebertraegt die Auswahl auf unveraenderliche Optionsobjekte."""
    validate_option_selection(parameters, option_sets, option_values, selection)
    return [
        replace(
            option,
            is_active=option.option_key in selection.active_option_keys_by_set.get(option.option_set_key, ()),
        )
        for option in option_values
    ]


def option_configuration_payload(
    option_sets: list[OptionSet],
    option_values: list[OptionValue],
    selection: ParameterOptionSelection,
    *,
    parameters: list[Parameter],
) -> dict[str, Any]:
    """Erzeugt die formatneutrale Nutzlast der Optionsauswahl."""
    selected_values = apply_option_selection(parameters, option_sets, option_values, selection)
    return {
        "option_sets": [
            {
                "option_set_key": option_set.option_set_key,
                "display_name": option_set.display_name,
                "description": option_set.description,
                "values": [
                    {
                        "option_key": option.option_key,
                        "label": option.label,
                        "value": option.value,
                        "unit": option.unit,
                        "is_active": option.is_active,
                    }
                    for option in selected_values
                    if option.option_set_key == option_set.option_set_key
                ],
            }
            for option_set in option_sets
        ]
    }


def save_option_selection(
    parameters: list[Parameter],
    option_sets: list[OptionSet],
    option_values: list[OptionValue],
    selection: ParameterOptionSelection,
    *,
    file_name: str,
    overwrite_existing: bool = False,
    overwrite_confirmed: bool = False,
    target_dir: str | Path = LOCAL_OPTION_DIR,
) -> ConfigurationSaveResult:
    """Speichert eine lokale Optionsauswahl, niemals die Parameterdefinitionen."""
    return save_yaml_configuration(
        option_configuration_payload(
            option_sets,
            option_values,
            selection,
            parameters=parameters,
        ),
        target_dir=target_dir,
        file_name=file_name,
        source=selection.source,
        overwrite_existing=overwrite_existing,
        overwrite_confirmed=overwrite_confirmed,
    )


def list_local_option_files(target_dir: str | Path = LOCAL_OPTION_DIR) -> tuple[Path, ...]:
    return list_configuration_files(target_dir)
