"""Gemeinsamer Streamlit-Zustand fuer Projekt, Parameter und Varianten."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import MutableMapping

from ma_core import ConfigurationSource
from ma_parameters import (
    DEFAULT_PARAMETER_CONFIG,
    ParameterOptionSelection,
    apply_option_selection,
    load_parameter_catalog,
)
from ma_project import (
    SimulationProgramProfile,
    VariantNamingProfile,
    load_simulation_program_profiles,
    load_variant_naming_profile,
)
from ma_variants.option_catalog import OptionSet, OptionValue
from ma_variants.parameter_catalog import Parameter
from ma_variants.ui import VariantUiData, build_variant_ui_data

CONFIGURATION_STATE_SESSION_KEY = "ma_ui_p028_configuration_state"


@dataclass(slots=True)
class ConfigurationState:
    """Buendelt den gemeinsamen Arbeitsstand der drei Demo-Ansichten."""

    simulation_programs: list[SimulationProgramProfile]
    active_program_key: str
    simulation_program_source: ConfigurationSource
    naming_profile: VariantNamingProfile
    naming_source: ConfigurationSource
    parameters: list[Parameter]
    option_sets: list[OptionSet]
    option_values: list[OptionValue]
    option_selection: ParameterOptionSelection
    parameter_source: ConfigurationSource


def load_default_configuration_state() -> ConfigurationState:
    """Initialisiert den Sitzungsstand aus den versionierten Vorlagen."""
    programs, active_program_key, program_source = load_simulation_program_profiles()
    naming_profile, naming_source = load_variant_naming_profile()
    parameters, option_sets, option_values, option_selection = load_parameter_catalog()
    return ConfigurationState(
        simulation_programs=programs,
        active_program_key=active_program_key,
        simulation_program_source=program_source,
        naming_profile=naming_profile,
        naming_source=naming_source,
        parameters=parameters,
        option_sets=option_sets,
        option_values=option_values,
        option_selection=option_selection,
        parameter_source=ConfigurationSource(path=Path(DEFAULT_PARAMETER_CONFIG), is_template=True),
    )


def get_configuration_state(
    session_state: MutableMapping[str, object],
) -> ConfigurationState:
    """Liefert den vorhandenen Zustand oder initialisiert ihn beim Direkteinstieg."""
    current = session_state.get(CONFIGURATION_STATE_SESSION_KEY)
    if isinstance(current, ConfigurationState):
        return current
    state = load_default_configuration_state()
    session_state[CONFIGURATION_STATE_SESSION_KEY] = state
    return state


def build_current_variant_ui_data(state: ConfigurationState) -> VariantUiData:
    """Erzeugt den Variantenraum aus der aktuell gemeinsam verwendeten Auswahl."""
    selected_option_values = apply_option_selection(
        state.parameters,
        state.option_sets,
        state.option_values,
        state.option_selection,
    )
    return build_variant_ui_data(
        state.parameters,
        state.option_sets,
        selected_option_values,
    )
