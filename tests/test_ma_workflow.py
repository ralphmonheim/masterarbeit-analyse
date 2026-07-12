from ma_analyse.models import AnalysisConfig, AnalysisResult
from ma_workflow import (
    get_dashboard_action,
    get_module_definition,
    get_step,
    get_workflow_step,
    list_cross_cutting_steps,
    list_dashboard_actions,
    list_feedback_targets,
    list_module_definitions,
    list_post_process_steps,
    list_pre_process_steps,
    list_steps,
    list_workflow_phases,
    list_workflow_steps,
    run_analysis_action,
    steps_by_phase,
)


def test_workflow_steps_cover_main_phases():
    phases = steps_by_phase()

    assert tuple(phases) == tuple(f"phase_{index}" for index in range(7))
    assert [phase.order for phase in list_workflow_phases()] == list(range(7))


def test_workflow_contains_analysis_step():
    analysis_step = get_workflow_step("analyse")

    assert analysis_step.step_key == "optimization"
    assert analysis_step.module_key == "ma_analyse.stage_2_optimization"
    assert analysis_step.status == "partial"


def test_workflow_statuses_reflect_current_module_implementation():
    assert get_workflow_step("building").status == "partial"
    assert get_workflow_step("zones").status == "partial"
    assert get_workflow_step("technical").status == "partial"
    assert get_workflow_step("parameters").status == "partial"
    assert get_workflow_step("dimensioning").status == "partial"
    assert get_workflow_step("data_preparation").status == "partial"
    assert get_workflow_step("optimization").status == "partial"
    assert get_workflow_step("standards_compliance").status == "planned"
    assert get_workflow_step("sensitivity").status == "planned"
    assert get_workflow_step("variants").status == "planned"
    assert get_workflow_step("ida_import").status == "planned"
    assert get_workflow_step("economy").status == "planned"
    assert get_workflow_step("sustainability").status == "planned"
    assert get_workflow_step("assessment").status == "planned"
    assert get_workflow_step("validation").status == "planned"


def test_phase_2_input_steps_follow_p013_s2_order():
    phase_2_steps = [step.step_key for step in list_workflow_steps() if step.phase_key == "phase_2"]

    assert phase_2_steps[:5] == ["weather", "building", "technical", "zones", "parameters"]


def test_partial_modules_reflect_current_module_implementation():
    partial_modules = {
        module.module_key
        for module in list_module_definitions()
        if module.status == "partial"
    }
    available_modules = {
        module.module_key
        for module in list_module_definitions()
        if module.status == "available"
    }

    assert partial_modules == {
        "ma_building",
        "ma_weather",
        "ma_analyse",
        "ma_analyse.data_preparation",
        "ma_analyse.stage_1_dimensioning",
        "ma_analyse.stage_2_optimization",
        "ma_zones",
        "ma_technical",
        "ma_parameters",
    }
    assert available_modules == {"project_documentation"}


def test_workflow_catalog_documents_parameter_variant_and_run_contracts():
    parameters = get_module_definition("ma_parameters")
    dimensioning = get_module_definition("ma_analyse.stage_1_dimensioning")
    variants = get_module_definition("ma_variants")
    simulation_setup = get_module_definition("ma_simulation_setup")

    parameter_text = " ".join((*parameters.outputs, parameters.next_step))
    dimensioning_text = " ".join((*dimensioning.outputs, dimensioning.next_step))
    variant_text = " ".join((*variants.inputs, *variants.outputs, variants.next_step))
    run_text = " ".join((*simulation_setup.inputs, *simulation_setup.outputs, simulation_setup.next_step))

    assert "BaselineParameterSnapshot" in parameter_text
    assert "ParameterVariationSpecification" in parameter_text
    assert "ReferenceDimensioningResult" in dimensioning_text
    assert "VariantVerification" in dimensioning_text
    assert "VariantSpace" in variant_text
    assert "VariantCatalog" in variant_text
    assert "VariantSelection" in variant_text
    assert "VariantGeneration" in variant_text
    assert "RunManifest" in run_text
    assert "RUN -> VAR" in run_text
    assert "SimulationCase" not in variant_text
    assert "SimulationCase" not in run_text


def test_post_process_contains_separate_economy_sustainability_and_assessment_steps():
    step_keys = [step.step_key for step in list_post_process_steps()]

    assert step_keys[-3:] == ["economy", "sustainability", "assessment"]


def test_workflow_steps_have_unique_keys():
    steps = list_workflow_steps()
    step_keys = [step.step_key for step in steps]

    assert len(step_keys) == len(set(step_keys))


def test_module_definitions_are_unique_and_cover_every_workflow_step():
    modules = list_module_definitions()
    module_keys = [module.module_key for module in modules]
    page_keys = [module.page_key for module in modules]

    assert len(module_keys) == len(set(module_keys))
    assert len(page_keys) == len(set(page_keys))
    assert all(get_module_definition(step.module_key) for step in list_workflow_steps())


def test_cross_cutting_steps_are_validation_and_feedback():
    assert [step.step_key for step in list_cross_cutting_steps()] == ["validation", "feedback"]


def test_workflow_manager_delegates_to_existing_catalog():
    assert list_steps() == list_workflow_steps()
    assert get_step("simulation_setup").module_key == "ma_simulation_setup"


def test_dashboard_actions_cover_target_commands():
    actions = list_dashboard_actions()
    action_keys = {action.action_key for action in actions}

    assert "open_simulation_setup" in action_keys
    assert "run_simulation_export" in action_keys
    assert "run_data_preparation" in action_keys
    assert "run_optimization" in action_keys
    assert "run_standards_compliance" in action_keys
    assert "run_sensitivity" in action_keys
    assert get_dashboard_action("run_analysis").step_key == "optimization"
    assert get_dashboard_action("run_prepare").step_key == "data_preparation"
    assert get_dashboard_action("run_ida_export").step_key == "export_simulation"
    assert get_dashboard_action("run_ida_import").step_key == "import_simulation"


def test_pre_and_post_process_runners_return_expected_phases():
    pre_process_steps = list_pre_process_steps()
    post_process_steps = list_post_process_steps()

    assert {step.phase_key for step in pre_process_steps} == {"phase_2", "phase_3"}
    assert {step.phase_key for step in post_process_steps} == {"phase_4", "phase_5"}
    assert pre_process_steps[-1].step_key == "export_simulation"
    assert post_process_steps[0].step_key == "import_simulation"
    assert post_process_steps[1].step_key == "data_preparation"


def test_feedback_targets_include_pre_process_modules():
    targets = list_feedback_targets()

    assert "ma_variants" in targets
    assert "ma_simulation_setup" in targets
    assert "ma_zones" in targets
    assert "ma_technical" in targets


def test_historical_ida_keys_resolve_to_general_interfaces():
    assert get_workflow_step("export_ida").step_key == "export_simulation"
    assert get_workflow_step("import_ida").step_key == "import_simulation"
    assert get_workflow_step("ida_export").step_key == "export_simulation"
    assert get_workflow_step("ida_import").step_key == "import_simulation"
    assert get_module_definition("ma_export_ida").module_key == "ma_export_simulation"
    assert get_module_definition("ma_import_ida").module_key == "ma_import_simulation"


def test_historical_stage_3_name_resolves_to_standards_compliance():
    assert get_workflow_step("stage_3_verification").step_key == "standards_compliance"
    assert (
        get_module_definition("ma_analyse.stage_3_verification").module_key
        == "ma_analyse.stage_3_standards_compliance"
    )


def test_prepare_and_analyze_data_resolve_to_data_preparation_step():
    assert get_workflow_step("prepare").step_key == "data_preparation"
    assert get_workflow_step("analyze-data").step_key == "data_preparation"
    assert get_workflow_step("analyze_data").step_key == "data_preparation"


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
