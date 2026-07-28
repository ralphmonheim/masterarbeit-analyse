from dataclasses import replace

import yaml

from ma_analyse.stage_1_dimensioning import run_lod1_reference_dimensioning
from ma_building import load_small_office_5z_endvariant_02_building_spec, validate_building_spec
from ma_parameters import (
    build_small_office_5z_v1_baseline_parameter_snapshot,
    build_small_office_5z_v1_parameter_snapshot,
    validate_baseline_parameter_snapshot,
    validate_parameter_snapshot,
)
from ma_technical import load_small_office_5z_endvariant_02_technical_spec, validate_technical_spec
from ma_validation import ReleaseStatus
from ma_variants import (
    build_small_office_v1_optimization_cases,
    build_small_office_v1_sensitivity_cases,
    load_small_office_v1_study,
)
from ma_workflow import run_small_office_v1_preprocess, small_office_v1_summary_rows
from ma_zones import (
    load_small_office_5z_endvariant_02_zone_spec,
    validate_technical_zone_integration,
    validate_zone_spec,
)


def _diagnostic_projection(result):
    return tuple(
        (message.severity, message.code, message.message, message.location)
        for message in result.messages
    )


def test_small_office_v1_uses_exact_endvariant_02_room_and_zone_geometry():
    building = load_small_office_5z_endvariant_02_building_spec()
    zones = load_small_office_5z_endvariant_02_zone_spec()
    technical = load_small_office_5z_endvariant_02_technical_spec()

    assert validate_building_spec(building).release_status is ReleaseStatus.RELEASED
    assert validate_zone_spec(zones, building_spec=building).release_status is ReleaseStatus.RELEASED
    assert validate_technical_spec(technical).release_status is ReleaseStatus.RELEASED
    assert validate_technical_zone_integration(zones, technical).release_status is ReleaseStatus.RELEASED
    assert len(building.spaces) == 29
    assert len(zones.zones) == 5
    assert sum(space.floor_area_m2 for space in building.spaces) == 516.842
    assert sum(space.volume_m3 for space in building.spaces) == 1677.64455
    assert sum(zone.floor_area_m2 for zone in zones.zones) == 516.842
    assert building.spaces[0].name == "101 Lobby"
    assert "zweigeschossig" in " ".join(item.text for item in building.assumptions)


def test_zone_owned_technical_integration_matches_legacy_diagnostics():
    zones = load_small_office_5z_endvariant_02_zone_spec()
    technical = load_small_office_5z_endvariant_02_technical_spec()
    invalid = replace(
        technical,
        project_id="OTHER-PROJECT",
        building_id="OTHER-BUILDING",
        source_zone_model_id="OTHER-ZONE-MODEL",
        systems=(
            replace(technical.systems[0], served_zone_ids=("UNKNOWN-ZONE",)),
            *technical.systems[1:],
        ),
    )

    legacy = validate_technical_spec(invalid, zone_spec=zones)
    zone_owned = validate_technical_zone_integration(zones, invalid)

    assert _diagnostic_projection(zone_owned) == _diagnostic_projection(legacy)
    assert zone_owned.release_status is legacy.release_status is ReleaseStatus.BLOCKED


def test_small_office_v1_builds_30_uniform_optimization_cases_and_8_sensitivity_cases():
    snapshot = build_small_office_5z_v1_parameter_snapshot()
    baseline = build_small_office_5z_v1_baseline_parameter_snapshot()
    dimensioning = run_lod1_reference_dimensioning(snapshot)
    study = load_small_office_v1_study()
    optimization = build_small_office_v1_optimization_cases(baseline, dimensioning, study)
    sensitivity = build_small_office_v1_sensitivity_cases(baseline, study, optimization)

    assert validate_parameter_snapshot(snapshot).release_status is ReleaseStatus.RELEASED
    assert validate_baseline_parameter_snapshot(baseline).release_status is ReleaseStatus.RELEASED
    assert len(optimization) == 30
    assert len(sensitivity) == 8
    assert optimization[0].case_id == "OPT-SB01-F100"
    assert optimization[-1].case_id == "OPT-SB05-F050"

    for case in optimization:
        heating_values = {
            value.value for value in case.variant.values if value.parameter_key.endswith(".heating_setpoint_c")
        }
        cooling_values = {
            value.value for value in case.variant.values if value.parameter_key.endswith(".cooling_setpoint_c")
        }
        assert heating_values == {case.band.heating_setpoint_c}
        assert cooling_values == {case.band.cooling_setpoint_c}

    reference = optimization[0]
    half_capacity = next(case for case in optimization if case.case_id == "OPT-SB01-F050")
    assert half_capacity.heating_capacity_w == round(reference.heating_capacity_w * 0.5, 2)
    assert half_capacity.cooling_capacity_w == round(reference.cooling_capacity_w * 0.5, 2)
    assert {case.parent_variant_id for case in sensitivity} == {"OPT-SB01-F100"}


def test_small_office_v1_runner_materializes_draft_packages_and_module_reports(tmp_path):
    result = run_small_office_v1_preprocess(run_id="TEST-SMALLOFFICE-V1", output_root=tmp_path)

    assert result.has_critical_error is False
    assert [step.step_key for step in result.steps] == [
        "project",
        "weather",
        "building",
        "zones",
        "technical",
        "parameters",
        "dimensioning",
        "parameter_variations",
        "variants",
        "simulation_setup",
    ]
    assert len(result.optimization_cases) == 30
    assert len(result.sensitivity_cases) == 8
    assert len(list((result.output_directory / "optimization").iterdir())) == 30
    assert len(list((result.output_directory / "sensitivity").iterdir())) == 8
    assert len(list((result.output_directory / "modules").glob("*.yaml"))) == 10
    assert (result.output_directory / "timings.csv").is_file()
    assert (result.output_directory / "diagnostics.yaml").is_file()
    assert (result.output_directory / "manual_v1_acceptance.md").is_file()

    reference_manifest = yaml.safe_load(
        (
            result.output_directory
            / "optimization"
            / "RUN-OPT-SB01-F100"
            / "run_manifest.yaml"
        ).read_text(encoding="utf-8")
    )
    assert reference_manifest["run"]["status"] == "draft"
    assert reference_manifest["simulation_setup"]["weather_key"] == "TRY_FFM_2015_JAHR"
    assert reference_manifest["simulation_setup"]["occupancy_start_hour"] == 7.0
    assert reference_manifest["simulation_setup"]["occupancy_end_hour"] == 18.0
    assert (
        result.output_directory
        / "sensitivity"
        / "RUN-SENS-OCC-OCC_EXTENDED"
        / "simulation_setup.yaml"
    ).is_file()


def test_small_office_v1_summary_is_available_to_streamlit_without_starting_a_run():
    rows = {row["Merkmal"]: row["Wert"] for row in small_office_v1_summary_rows()}

    assert rows["Zonen"] == 5
    assert rows["Optimierungsfaelle"] == 30
    assert rows["Wetter-Sensitivitaet"] == 4
    assert rows["Belegungs-Sensitivitaet"] == 4
