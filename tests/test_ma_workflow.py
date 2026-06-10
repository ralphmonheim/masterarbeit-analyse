from ma_analyse.models import AnalysisConfig, AnalysisResult
from ma_workflow import (
    get_dashboard_action,
    get_step,
    get_workflow_step,
    list_dashboard_actions,
    list_feedback_targets,
    list_post_process_steps,
    list_pre_process_steps,
    list_steps,
    list_workflow_steps,
    run_analysis_action,
    steps_by_phase,
)


def test_workflow_steps_cover_main_phases():
    phases = steps_by_phase()

    assert "Pre-Process" in phases
    assert "Simulation" in phases
    assert "Post-Process" in phases
    assert "Feedback" in phases


def test_workflow_contains_analysis_step():
    analysis_step = get_workflow_step("analyse")

    assert analysis_step.module_key == "ma_analyse"
    assert analysis_step.status == "available"


def test_workflow_steps_have_unique_keys():
    steps = list_workflow_steps()
    step_keys = [step.step_key for step in steps]

    assert len(step_keys) == len(set(step_keys))


def test_workflow_manager_delegates_to_existing_catalog():
    assert list_steps() == list_workflow_steps()
    assert get_step("simulation_setup").module_key == "ma_simulation_setup"


def test_dashboard_actions_cover_target_commands():
    actions = list_dashboard_actions()
    action_keys = {action.action_key for action in actions}

    assert "open_simulation_setup" in action_keys
    assert "run_ida_export" in action_keys
    assert "run_analysis" in action_keys
    assert get_dashboard_action("run_analysis").step_key == "analyse"


def test_pre_and_post_process_runners_return_expected_phases():
    pre_process_steps = list_pre_process_steps()
    post_process_steps = list_post_process_steps()

    assert {step.phase for step in pre_process_steps} == {"Pre-Process"}
    assert {step.phase for step in post_process_steps} == {"Post-Process"}
    assert pre_process_steps[-1].step_key == "ida_export"
    assert post_process_steps[0].step_key == "ida_import"


def test_feedback_targets_include_pre_process_modules():
    targets = list_feedback_targets()

    assert "ma_variants" in targets
    assert "ma_simulation_setup" in targets


def test_analysis_workflow_action_uses_service_facade(tmp_path):
    config = AnalysisConfig(
        steps=("analysis",),
        input_dir=tmp_path / "ida_imports",
        database_dir=tmp_path / "missing_database",
        output_root=tmp_path / "output",
        rooms=["101 lobby"],
        variants=["Variant_A"],
    )

    result = run_analysis_action(config)

    assert isinstance(result, AnalysisResult)
    assert result.success is False
    assert result.steps == ("analysis",)
