from ma_parameters import (
    build_baseline_parameter_snapshot_from_input_package,
    build_business_integration_lod1_parameter_snapshot,
    build_lod1_parameter_input_package,
)
from ma_simulation_setup import SimulationRunStatus, build_run_manifest, materialize_run_package
from ma_variants.preprocess import VariationValue, build_baseline_variant, build_explicit_variant


def _baseline_snapshot():
    source_snapshot = build_business_integration_lod1_parameter_snapshot()
    input_package = build_lod1_parameter_input_package(
        source_snapshot,
        package_id="PARAM-P018-INPUT-0001",
        package_version="V1",
        require_weather=False,
    )
    return build_baseline_parameter_snapshot_from_input_package(
        input_package,
        snapshot_id="PARAM-P018-BASELINE-0001",
        snapshot_version="V1",
    )


def test_released_run_package_materializes_baseline_and_explicit_variant(tmp_path):
    snapshot = _baseline_snapshot()
    baseline = build_baseline_variant(snapshot)
    variant = build_explicit_variant(
        snapshot,
        variant_id="VAR-HEATING-SETPOINT-0001",
        label="Heizsollwert 21 Grad C",
        values=(VariationValue("ZONE-BI-LOD1-0001.heating_setpoint_c", 21.0, "degC"),),
    )

    baseline_manifest = build_run_manifest(snapshot, baseline, run_id="RUN-BASELINE-0001", release=True)
    manifest = build_run_manifest(snapshot, variant, run_id="RUN-VARIANT-0001", release=True)
    run_dir = materialize_run_package(manifest, variant, tmp_path)

    assert baseline_manifest.run.variant_id == "VAR-BASELINE"
    assert manifest.run.status is SimulationRunStatus.RELEASED_FOR_SIMULATION
    assert {requirement.profile_id for requirement in manifest.output_requirements} == {
        "OUT-LOAD",
        "OUT-COMFORT",
        "OUT-PEAK",
    }
    assert (run_dir / "run_manifest.yaml").is_file()
    assert (run_dir / "variant_config.yaml").is_file()
    assert (run_dir / "simulation_input.yaml").is_file()
    assert (run_dir / "preparation_report.md").is_file()


def test_run_manifest_rejects_variant_from_other_baseline():
    snapshot = _baseline_snapshot()
    foreign_snapshot = _baseline_snapshot()
    variant = build_baseline_variant(foreign_snapshot)

    foreign_variant = type(variant)(
        variant_id=variant.variant_id,
        label=variant.label,
        baseline_snapshot_id="FOREIGN-SNAPSHOT",
        baseline_content_hash=variant.baseline_content_hash,
    )

    try:
        build_run_manifest(snapshot, foreign_variant, run_id="RUN-INVALID-0001")
    except ValueError as error:
        assert "referenziert nicht" in str(error)
    else:
        raise AssertionError("Eine fremde Baseline muss den Run-Aufbau blockieren.")
