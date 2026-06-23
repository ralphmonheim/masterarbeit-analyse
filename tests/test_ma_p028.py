from pathlib import Path

import pandas as pd
import pytest

from ma_core import ConfigurationSource
from ma_parameters import (
    ParameterOptionSelection,
    apply_option_selection,
    load_parameter_catalog,
    save_option_selection,
    validate_option_selection,
)
from ma_project import (
    SimulationProgramProfile,
    load_simulation_program_profiles,
    load_variant_naming_profile,
    save_simulation_program_profiles,
)
from ma_ui.module_views.project_view import naming_profile_from_rows, naming_token_rows
from ma_ui.state import (
    CONFIGURATION_STATE_SESSION_KEY,
    build_current_variant_ui_data,
    get_configuration_state,
)
from ma_variants.ui import apply_naming_profile_to_ui_data, build_variant_ui_data


def test_p028_default_files_produce_expected_demo_scope():
    parameters, option_sets, option_values, selection = load_parameter_catalog()
    selected_values = apply_option_selection(parameters, option_sets, option_values, selection)
    ui_data = build_variant_ui_data(parameters, option_sets, selected_values)
    naming_profile, _source = load_variant_naming_profile()
    named_data = apply_naming_profile_to_ui_data(ui_data, naming_profile)

    assert len(parameters) == 3
    assert len(option_values) == 6
    assert len(named_data.generated_variants) == 8
    assert named_data.generated_variants[0][0].variant_name == "V001_CL24_VCO2_H100"


def test_option_selection_changes_variant_count_reproducibly():
    parameters, option_sets, option_values, default_selection = load_parameter_catalog()
    selection = ParameterOptionSelection(
        active_option_keys_by_set={
            **default_selection.active_option_keys_by_set,
            "heating_capacity_factors": ("heating_capacity_100",),
        },
        source=default_selection.source,
    )

    selected_values = apply_option_selection(parameters, option_sets, option_values, selection)
    first = build_variant_ui_data(parameters, option_sets, selected_values)
    second = build_variant_ui_data(parameters, option_sets, selected_values)

    assert first.theoretical_variant_count == 4
    assert first.generated_variants == second.generated_variants


def test_option_selection_blocks_empty_and_unknown_values():
    parameters, option_sets, option_values, default_selection = load_parameter_catalog()
    empty_selection = ParameterOptionSelection(
        active_option_keys_by_set={
            **default_selection.active_option_keys_by_set,
            "cooling_setpoint_levels": (),
        },
        source=default_selection.source,
    )
    unknown_selection = ParameterOptionSelection(
        active_option_keys_by_set={
            **default_selection.active_option_keys_by_set,
            "cooling_setpoint_levels": ("unknown",),
        },
        source=default_selection.source,
    )

    with pytest.raises(ValueError, match="mindestens einen aktiven Wert"):
        validate_option_selection(parameters, option_sets, option_values, empty_selection)
    with pytest.raises(ValueError, match="Unbekannte Optionswerte"):
        validate_option_selection(parameters, option_sets, option_values, unknown_selection)


def test_naming_editor_roundtrip_preserves_expected_preview():
    profile, _source = load_variant_naming_profile()
    edited_profile = naming_profile_from_rows(
        prefix=profile.prefix,
        index_width=profile.index_width,
        separator=profile.separator,
        include_index=profile.include_index,
        editor_value=pd.DataFrame(naming_token_rows(profile)),
    )
    parameters, option_sets, option_values, selection = load_parameter_catalog()
    ui_data = build_variant_ui_data(
        parameters,
        option_sets,
        apply_option_selection(parameters, option_sets, option_values, selection),
    )

    named_data = apply_naming_profile_to_ui_data(ui_data, edited_profile)

    assert named_data.generated_variants[0][0].variant_name == "V001_CL24_VCO2_H100"


def test_naming_blocks_missing_tokens():
    profile, _source = load_variant_naming_profile()
    rows = naming_token_rows(profile)
    rows = [row for row in rows if row["option_key"] != "cooling_setpoint_26"]
    edited_profile = naming_profile_from_rows(
        prefix=profile.prefix,
        index_width=profile.index_width,
        separator=profile.separator,
        include_index=profile.include_index,
        editor_value=pd.DataFrame(rows),
    )
    parameters, option_sets, option_values, selection = load_parameter_catalog()
    ui_data = build_variant_ui_data(
        parameters,
        option_sets,
        apply_option_selection(parameters, option_sets, option_values, selection),
    )

    with pytest.raises(ValueError, match="Kein Namenstoken"):
        apply_naming_profile_to_ui_data(ui_data, edited_profile)


def test_program_and_option_workfiles_are_saved_without_changing_templates(tmp_path):
    programs, active_key, program_source = load_simulation_program_profiles()
    parameters, option_sets, option_values, selection = load_parameter_catalog()

    program_result = save_simulation_program_profiles(
        programs,
        active_key,
        file_name="programs.yaml",
        target_dir=tmp_path / "programs",
    )
    option_result = save_option_selection(
        parameters,
        option_sets,
        option_values,
        selection,
        file_name="options.yaml",
        target_dir=tmp_path / "options",
    )

    assert program_source.is_template is True
    assert program_result.path.exists()
    assert option_result.path.exists()


def test_program_profile_keys_must_be_unique(tmp_path):
    programs = [
        SimulationProgramProfile("ida_ice", "IDA ICE"),
        SimulationProgramProfile("ida_ice", "IDA ICE Kopie"),
    ]

    with pytest.raises(ValueError, match="eindeutig"):
        save_simulation_program_profiles(
            programs,
            "ida_ice",
            file_name="programs.yaml",
            target_dir=tmp_path,
        )


def test_direct_ui_entry_initializes_shared_state_once():
    session_state: dict[str, object] = {}

    first = get_configuration_state(session_state)
    second = get_configuration_state(session_state)
    ui_data = build_current_variant_ui_data(first)

    assert first is second
    assert session_state[CONFIGURATION_STATE_SESSION_KEY] is first
    assert ui_data.theoretical_variant_count == 8
    assert first.option_selection.source == ConfigurationSource(
        path=Path("config/ma_variants/options/example_options.yaml"),
        is_template=True,
    )
