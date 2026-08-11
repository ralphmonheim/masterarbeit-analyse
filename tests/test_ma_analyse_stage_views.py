from datetime import UTC, datetime

import pandas as pd

from ma_analyse.models import AnalysisResult
from ma_analyse.stage_views import analysis_stage_overview_rows, build_analysis_stage_views
from ma_project import Project, ProjectIdentity, ProjectLocation
from ma_ui.streamlit_app.module_views.analyse_view import (
    LAST_ANALYSIS_RESULT_SESSION_KEY,
    LAST_ANALYSIS_WORKSPACE_ID_SESSION_KEY,
    OUTPUT_ROOT_DEFAULT_SESSION_KEY,
    OUTPUT_ROOT_WIDGET_KEY,
    analysis_output_root,
    analysis_result_for_active_workspace,
    store_analysis_result,
)
from ma_ui.streamlit_app.state.workspace_state import set_active_workspace
from ma_workspace import create_project_workspace


def test_stage_views_keep_current_analysis_in_optimization(tmp_path):
    table = pd.DataFrame([{"Kennwert": "Heizlast", "Wert": 1200.0}])
    result = AnalysisResult(
        success=True,
        steps=("heating",),
        created_files=[tmp_path / "heating.png"],
        summary_table=table,
        detail_tables={"Raeume": table},
        warnings=["Beispielhinweis"],
    )

    views = build_analysis_stage_views(result)
    optimization = next(view for view in views if view.stage_key == "optimization")

    assert [view.stage_key for view in views] == [
        "dimensioning",
        "optimization",
        "standards_verification",
        "sensitivity",
    ]
    assert optimization.status == "completed"
    assert optimization.result is result


def test_stage_views_mark_missing_norm_and_sensitivity_contracts_as_not_evaluable():
    views = build_analysis_stage_views()
    rows = analysis_stage_overview_rows(views)

    assert rows[0]["Stufe"] == "Dimensionierung"
    assert rows[1]["Status"] == "not_run"
    assert rows[2]["Status"] == "not_evaluable"
    assert rows[3]["Status"] == "not_evaluable"
    assert "keine produktiven Normregeln" in " ".join(views[2].limits)
    assert views[2].result is not None
    assert {row["Stage-3-Status"] for row in views[2].result.summary_table} == {"NOT_EVALUABLE"}


def test_analysis_output_root_uses_active_project_workspace(tmp_path):
    timestamp = datetime(2026, 8, 11, 10, 0, tzinfo=UTC)
    project = Project(
        identity=ProjectIdentity(project_id="PRJ-654321", title="Analyse-Demo", short_name="Demo"),
        created_at=timestamp,
        updated_at=timestamp,
        location=ProjectLocation(country_code="DE", city="Teststadt"),
    )
    workspace = create_project_workspace(
        project,
        tmp_path.resolve(),
        simulation_program_key="ida_ice",
    )
    state: dict[str, object] = {}
    set_active_workspace(state, workspace)

    output_root = analysis_output_root(state)

    assert output_root == str(workspace.paths.output / "ma_analyse")
    assert state[OUTPUT_ROOT_WIDGET_KEY] == output_root
    assert state[OUTPUT_ROOT_DEFAULT_SESSION_KEY] == output_root


def test_analysis_output_root_keeps_manual_override(tmp_path):
    manual_root = tmp_path / "manual-output"
    state: dict[str, object] = {OUTPUT_ROOT_WIDGET_KEY: str(manual_root)}

    assert analysis_output_root(state) == str(manual_root)


def test_analysis_output_root_replaces_repository_default_for_active_workspace(tmp_path):
    timestamp = datetime(2026, 8, 11, 10, 0, tzinfo=UTC)
    project = Project(
        identity=ProjectIdentity("PRJ-654322", "Analyse-Demo-2", "Demo2"),
        created_at=timestamp,
        updated_at=timestamp,
        location=ProjectLocation(country_code="DE", city="Teststadt"),
    )
    workspace = create_project_workspace(project, tmp_path.resolve(), simulation_program_key="ida_ice")
    state: dict[str, object] = {OUTPUT_ROOT_WIDGET_KEY: "data/ma_analyse/output"}
    set_active_workspace(state, workspace)

    assert analysis_output_root(state) == str(workspace.paths.output / "ma_analyse")


def test_analysis_result_is_available_in_its_active_workspace(tmp_path):
    timestamp = datetime(2026, 8, 11, 10, 0, tzinfo=UTC)
    project = Project(
        identity=ProjectIdentity("PRJ-654323", "Analyse-Demo-3", "Demo3"),
        created_at=timestamp,
        updated_at=timestamp,
        location=ProjectLocation(country_code="DE", city="Teststadt"),
    )
    workspace = create_project_workspace(project, tmp_path.resolve(), simulation_program_key="ida_ice")
    state: dict[str, object] = {}
    set_active_workspace(state, workspace)
    result = AnalysisResult(success=True, steps=("heating",))

    store_analysis_result(result, state)

    assert analysis_result_for_active_workspace(state) is result
    assert state[LAST_ANALYSIS_WORKSPACE_ID_SESSION_KEY] == "PRJ-654323"


def test_analysis_result_is_discarded_after_workspace_change(tmp_path):
    timestamp = datetime(2026, 8, 11, 10, 0, tzinfo=UTC)
    first_project = Project(
        identity=ProjectIdentity("PRJ-654324", "Analyse-Demo-4", "Demo4"),
        created_at=timestamp,
        updated_at=timestamp,
        location=ProjectLocation(country_code="DE", city="Teststadt"),
    )
    second_project = Project(
        identity=ProjectIdentity("PRJ-654325", "Analyse-Demo-5", "Demo5"),
        created_at=timestamp,
        updated_at=timestamp,
        location=ProjectLocation(country_code="DE", city="Teststadt"),
    )
    first_workspace = create_project_workspace(
        first_project,
        tmp_path.resolve(),
        simulation_program_key="ida_ice",
    )
    second_workspace = create_project_workspace(
        second_project,
        tmp_path.resolve(),
        simulation_program_key="ida_ice",
    )
    state: dict[str, object] = {}
    set_active_workspace(state, first_workspace)
    store_analysis_result(AnalysisResult(success=True, steps=("heating",)), state)

    set_active_workspace(state, second_workspace)

    assert analysis_result_for_active_workspace(state) is None
    assert LAST_ANALYSIS_RESULT_SESSION_KEY not in state
    assert LAST_ANALYSIS_WORKSPACE_ID_SESSION_KEY not in state
