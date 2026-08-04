from pathlib import Path

import ma_dimensionierung
from ma_analyse import stage_1_dimensioning as legacy_dimensioning

DIRECT_CONSUMERS = (
    Path("src/ma_ui/streamlit_app/module_views/dimensioning_view.py"),
    Path("src/ma_variants/small_office_v1.py"),
    Path("src/ma_workflow/small_office_v1_preprocess.py"),
)


def test_prepared_namespace_reexports_identical_dimensioning_objects():
    public_names = (
        "DEFAULT_HEATING_OUTDOOR_TEMPERATURE_C",
        "DEFAULT_PERSON_SENSIBLE_GAIN_W",
        "DimensioningStatus",
        "DimensioningStep",
        "ReferenceDimensioningResult",
        "dimensioning_message_rows",
        "dimensioning_step_rows",
        "dimensioning_summary_rows",
        "run_business_integration_lod1_reference_dimensioning",
        "run_lod1_reference_dimensioning",
    )

    for name in public_names:
        assert getattr(ma_dimensionierung, name) is getattr(legacy_dimensioning, name)


def test_prepared_namespace_does_not_claim_analysis_output_requirements():
    assert "OutputRequirementProfile" not in ma_dimensionierung.__all__
    assert "default_output_requirements" not in ma_dimensionierung.__all__
    assert not hasattr(ma_dimensionierung, "OutputRequirementProfile")
    assert not hasattr(ma_dimensionierung, "default_output_requirements")


def test_prepared_namespace_preserves_reference_result_parity():
    current = ma_dimensionierung.run_business_integration_lod1_reference_dimensioning()
    legacy = legacy_dimensioning.run_business_integration_lod1_reference_dimensioning()

    assert current.__class__ is legacy.__class__
    assert current.status is legacy.status
    assert current.result_id == legacy.result_id
    assert current.source_snapshot_id == legacy.source_snapshot_id
    assert current.source_snapshot_version == legacy.source_snapshot_version
    assert current.heating_transmission_load_w == legacy.heating_transmission_load_w
    assert current.heating_ventilation_load_w == legacy.heating_ventilation_load_w
    assert current.heating_total_load_w == legacy.heating_total_load_w
    assert current.cooling_internal_load_w == legacy.cooling_internal_load_w
    assert current.ventilation_volume_flow_m3_h == legacy.ventilation_volume_flow_m3_h
    assert current.steps == legacy.steps
    assert tuple(message.code for message in current.messages) == tuple(
        message.code for message in legacy.messages
    )


def test_direct_dimensioning_consumers_use_the_prepared_namespace():
    for path in DIRECT_CONSUMERS:
        source = path.read_text(encoding="utf-8")
        assert "from ma_dimensionierung import" in source
        assert "from ma_analyse.stage_1_dimensioning import" not in source
