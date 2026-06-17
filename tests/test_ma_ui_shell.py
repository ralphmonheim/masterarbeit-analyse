from pathlib import Path

from ma_analyse.analysis_ui import (
    build_analysis_config,
    build_catalog_overlay_line,
    build_plot_template_options,
    build_template_time_options,
    first_selected_value,
    parse_overlay_lines_text,
    plot_template_requires_single_room,
    plot_template_supports_overlays,
    room_text_from_selection,
    room_values_from_template_selection,
    split_csv_text,
    variant_selection_from_scope,
    variant_text_from_selection,
)
from ma_analyse.analysis_wizard import (
    AnalysisWizardState,
    analysis_step_complete,
    analysis_step_summary,
    backend_command,
    first_incomplete_step,
    room_selection_disabled,
    sanitize_comfort_output,
    visible_analysis_steps,
)
from ma_ui.app import get_renderable_page_keys
from ma_ui.components import created_file_rows, is_preview_image, preview_image_paths
from ma_ui.legacy_launchers import build_tkinter_analyse_command, launch_tkinter_analyse
from ma_ui.main_dashboard import dashboard_action_rows
from ma_ui.module_views import (
    analyse_view,
    assessment_view,
    building_view,
    export_ida_view,
    feedback_view,
    home_view,
    import_ida_view,
    parameters_view,
    simulation_setup_view,
    variants_view,
    weather_view,
)
from ma_ui.module_views.analyse_view import (
    COMMAND_OPTIONS,
    DEFAULT_COMMAND_INDEX,
    PLOT_TEMPLATE_STEP,
    add_session_overlay_line,
    get_session_overlay_lines,
    remove_session_overlay_line,
    safe_list_plot_overlay_sources,
)
from ma_ui.navigation import (
    CURRENT_PAGE_SESSION_KEY,
    get_navigation_page,
    get_navigation_pages,
    next_page_key,
    normalize_page_key,
    previous_page_key,
)
from ma_ui.pages.assessment import economic_assumption_rows
from ma_ui.pages.home import workflow_phase_summary_rows, workflow_status_counts
from ma_ui.pages.weather import (
    created_weather_plot_paths,
    weather_dataset_rows,
    weather_metric_rows,
    weather_plot_rows,
    weather_start_year,
)
from ma_ui.post_process_view import post_process_step_rows
from ma_ui.pre_process_view import pre_process_step_rows
from ma_ui.resource_status import ResourceSpec, resource_status, resource_status_rows, resource_statuses_for_step
from ma_ui.shared import normalize_table_for_streamlit
from ma_ui.shared.workflow_context import workflow_context_rows
from ma_ui.state import ProjectState
from ma_ui.workflow_graph import (
    VISUAL_PHASES,
    feedback_path_rows,
    status_style,
    target_page_for_step,
    workflow_card_rows,
    workflow_cards_by_phase,
)
from ma_ui.workflow_view import workflow_step_rows
from ma_variants.economic_analysis import import_economic_assumptions
from ma_weather import WeatherDataset, WeatherMetrics, WeatherPlotResult


def test_ui_navigation_contains_home_and_analysis():
    pages = get_navigation_pages()
    page_keys = {page.page_key for page in pages}

    assert "home" in page_keys
    assert "parameters" in page_keys
    assert "analyse" in page_keys
    assert "variants" in page_keys
    assert "weather" in page_keys
    assert "assessment" in page_keys
    assert "feedback" in page_keys


def test_ui_navigation_page_metadata():
    analyse_page = get_navigation_page("analyse")
    weather_page = get_navigation_page("weather")

    assert analyse_page.module_key == "ma_analyse"
    assert analyse_page.status == "partial"
    assert weather_page.module_key == "ma_weather"
    assert weather_page.status == "partial"


def test_renderable_pages_include_variants():
    assert get_renderable_page_keys() == (
        "home",
        "parameters",
        "weather",
        "building",
        "variants",
        "simulation_setup",
        "export_ida",
        "import_ida",
        "analyse",
        "assessment",
        "feedback",
    )


def test_navigation_normalizes_unknown_session_page_key():
    assert CURRENT_PAGE_SESSION_KEY == "ma_ui_current_page"
    assert normalize_page_key("analyse", ("home", "analyse")) == "analyse"
    assert normalize_page_key("missing", ("home", "analyse")) == "home"
    assert normalize_page_key(None, ("home", "analyse")) == "home"


def test_navigation_previous_and_next_page_keys_are_stable():
    page_keys = ("home", "parameters", "weather")

    assert previous_page_key("home", page_keys) == "home"
    assert previous_page_key("weather", page_keys) == "parameters"
    assert next_page_key("home", page_keys) == "parameters"
    assert next_page_key("weather", page_keys) == "weather"
    assert next_page_key("missing", page_keys) == "parameters"


def test_module_views_are_importable():
    renderers = (
        home_view.render,
        parameters_view.render,
        weather_view.render,
        building_view.render,
        variants_view.render,
        simulation_setup_view.render,
        export_ida_view.render,
        import_ida_view.render,
        analyse_view.render,
        assessment_view.render,
        feedback_view.render,
    )

    assert all(callable(renderer) for renderer in renderers)


def test_dashboard_and_workflow_rows_cover_target_structure():
    dashboard_rows = dashboard_action_rows()
    workflow_rows = workflow_step_rows()
    pre_process_rows = pre_process_step_rows()
    post_process_rows = post_process_step_rows()

    assert any(row["Aktion"] == "open_simulation_setup" for row in dashboard_rows)
    assert any(row["Modul"] == "ma_simulation_setup" for row in workflow_rows)
    assert pre_process_rows[-1]["Modul"] == "ma_export_ida"
    assert post_process_rows[0]["Modul"] == "ma_import_ida"


def test_home_page_summarizes_workflow_status_and_phases():
    rows = workflow_step_rows()
    status_counts = workflow_status_counts(rows)
    phase_rows = workflow_phase_summary_rows(rows)

    assert status_counts["available"] >= 1
    assert status_counts["planned"] >= 1
    assert any(row["Phase"] == "Pre-Process" for row in phase_rows)
    assert any("ma_export_ida" in row["Module"] for row in phase_rows)


def test_workflow_graph_groups_steps_by_visual_phase():
    cards = workflow_card_rows(available_page_keys=get_renderable_page_keys())
    grouped = workflow_cards_by_phase(cards)

    assert VISUAL_PHASES == ("Pre-Process", "Simulation", "Post-Process", "Assessment", "Feedback/Abschluss")
    assert any(card.step_key == "parameters" for card in grouped["Pre-Process"])
    assert any(card.step_key == "simulation" for card in grouped["Simulation"])
    assert any(card.step_key == "analyse" for card in grouped["Post-Process"])
    assert any(card.step_key == "assessment" for card in grouped["Assessment"])
    assert any(card.step_key == "feedback" for card in grouped["Feedback/Abschluss"])


def test_workflow_graph_uses_stable_status_styles():
    assert status_style("available")["label"] == "Verfuegbar"
    assert status_style("partial")["background"].startswith("#")
    assert status_style("unknown")["label"] == "Unklar"


def test_workflow_graph_maps_steps_to_renderable_pages():
    page_keys = get_renderable_page_keys()

    assert target_page_for_step("parameters", page_keys) == "parameters"
    assert target_page_for_step("ida_export", page_keys) == "export_ida"
    assert target_page_for_step("ida_import", page_keys) == "import_ida"
    assert target_page_for_step("simulation", page_keys) is None


def test_workflow_graph_feedback_paths_target_existing_pages():
    page_keys = set(get_renderable_page_keys())
    rows = feedback_path_rows()

    assert {row["Frage"] for row in rows} == {"Model good?", "Data good?", "Room for Optimization?"}
    assert all(row["Zielseite"] in page_keys for row in rows)


def test_graphical_workflow_is_home_only():
    home_source = Path("src/ma_ui/pages/home.py").read_text(encoding="utf-8")
    module_sources = [
        path.read_text(encoding="utf-8")
        for path in Path("src/ma_ui/module_views").glob("*.py")
        if path.name != "home_view.py"
    ]

    assert "Grafischer Workflow" in home_source
    assert "Iterationspfade" in home_source
    assert "ma_ui.workflow_graph" in home_source
    assert all("ma_ui.workflow_graph" not in source for source in module_sources)
    assert all("Grafischer Workflow" not in source for source in module_sources)
    assert all("Iterationspfade" not in source for source in module_sources)


def test_ui_uses_top_navigation_instead_of_sidebar_radio():
    app_source = Path("src/ma_ui/app.py").read_text(encoding="utf-8")

    assert "st.sidebar.radio" not in app_source
    assert "Start" in app_source
    assert "Zurueck" in app_source
    assert "Weiter" in app_source


def test_streamlit_width_api_is_current():
    source_paths = list(Path("src/ma_ui").rglob("*.py")) + list(Path("src/ma_variants/ui").rglob("*.py"))
    sources = [path.read_text(encoding="utf-8") for path in source_paths]

    assert all("use_container_width" not in source for source in sources)


def test_normalize_table_for_streamlit_converts_mixed_object_columns():
    rows = [
        {"name": "numeric", "value": 1, "active": True},
        {"name": "text", "value": "co2", "active": False},
    ]

    dataframe = normalize_table_for_streamlit(rows)

    assert dataframe["value"].tolist() == ["1", "co2"]
    assert dataframe["name"].tolist() == ["numeric", "text"]


def test_workflow_context_rows_show_module_status_and_action():
    rows = workflow_context_rows(("parameters", "ida_export"))

    assert rows[0]["Modul"] == "ma_parameters"
    assert rows[0]["Dashboard-Aktion"] == "Parameter oeffnen"
    assert rows[1]["Modul"] == "ma_export_ida"
    assert rows[1]["Status"] == "partial"


def test_resource_status_detects_existing_file(tmp_path):
    config_file = tmp_path / "config" / "example.yaml"
    config_file.parent.mkdir()
    config_file.write_text("example: true", encoding="utf-8")

    status = resource_status(
        ResourceSpec("Beispiel", "config/example.yaml", "Test"),
        project_root=tmp_path,
    )

    assert status.exists is True
    assert status.status == "vorhanden"
    assert status.file_count == 1
    assert status.directory_count == 0


def test_resource_status_treats_gitkeep_only_directory_as_structure(tmp_path):
    data_dir = tmp_path / "data" / "module"
    data_dir.mkdir(parents=True)
    (data_dir / ".gitkeep").write_text("", encoding="utf-8")

    status = resource_status(
        ResourceSpec("Datenordner", "data/module", "Test"),
        project_root=tmp_path,
    )

    assert status.exists is True
    assert status.status == "Struktur vorhanden"
    assert status.file_count == 0


def test_resource_status_counts_nested_files_and_directories(tmp_path):
    nested_dir = tmp_path / "data" / "module" / "variant" / "room"
    nested_dir.mkdir(parents=True)
    (nested_dir / "ZONE-ENERGY.prn").write_text("time,value", encoding="utf-8")
    (nested_dir / "__pycache__").mkdir()

    status = resource_status(
        ResourceSpec("Datenordner", "data/module", "Test"),
        project_root=tmp_path,
    )

    assert status.status == "vorhanden"
    assert status.file_count == 1
    assert status.directory_count == 2


def test_resource_status_rows_cover_p005_placeholder_views():
    assert resource_status_rows("parameters")
    assert resource_status_rows("building")
    assert resource_status_rows("simulation_setup")
    assert resource_status_rows("ida_export")
    assert resource_status_rows("ida_import")
    assert resource_status_rows("feedback")
    assert resource_statuses_for_step("unknown") == ()


def test_project_state_uses_independent_lists():
    first_state = ProjectState(selected_rooms=["101 lobby"])
    second_state = ProjectState()
    second_state.selected_variants.append("Variant_A")

    assert first_state.selected_rooms == ["101 lobby"]
    assert first_state.selected_variants == []
    assert second_state.selected_variants == ["Variant_A"]


def test_project_state_accepts_paths():
    state = ProjectState(
        project_folder=Path("project"),
        result_folder=Path("data/ma_analyse/ida_imports"),
    )

    assert state.project_folder == Path("project")
    assert state.result_folder == Path("data/ma_analyse/ida_imports")


def test_analyse_view_splits_csv_text():
    assert split_csv_text(" Variant_A, Variant_B ,, ") == ["Variant_A", "Variant_B"]


def test_analyse_view_defaults_to_plot_template():
    assert PLOT_TEMPLATE_STEP in COMMAND_OPTIONS
    assert COMMAND_OPTIONS[DEFAULT_COMMAND_INDEX] == PLOT_TEMPLATE_STEP
    assert PLOT_TEMPLATE_STEP == "plot-template-analyse"
    assert backend_command(PLOT_TEMPLATE_STEP) == "plot-template"


def test_analysis_wizard_initially_shows_command_only():
    state = AnalysisWizardState()

    assert visible_analysis_steps(state) == ("command",)
    assert first_incomplete_step(state, ("command",)) == "command"


def test_analysis_wizard_uses_tkinter_visibility_for_prepare():
    state = AnalysisWizardState(command="prepare")

    assert visible_analysis_steps(state) == ("command", "export", "variants", "run")


def test_analysis_wizard_hides_load_options_until_subcommand_is_selected():
    state = AnalysisWizardState(command="heating")

    assert visible_analysis_steps(state) == (
        "command",
        "subcommand",
        "export",
        "template_diagram",
        "variants",
        "rooms",
        "run",
    )

    timeline_state = AnalysisWizardState(command="heating", load_subcommand="timeline")

    assert visible_analysis_steps(timeline_state) == (
        "command",
        "subcommand",
        "export",
        "template_diagram",
        "variants",
        "rooms",
        "run",
    )


def test_analysis_wizard_uses_comfort_subcommand_without_analysis_level():
    state = AnalysisWizardState(command="comfort")

    assert visible_analysis_steps(state) == (
        "command",
        "subcommand",
        "template_diagram",
        "variants",
        "rooms",
        "run",
    )


def test_analysis_wizard_keeps_all_comfort_outputs_available():
    assert sanitize_comfort_output("Analyse Raum", "plot_analysis") == "plot_analysis"
    assert sanitize_comfort_output("Analyse Variante", "plot_analysis") == "plot_analysis"
    assert sanitize_comfort_output("Analyse Variante", "plot_overview") == "plot_overview"


def test_analysis_wizard_uses_room_scope_for_comfort_rooms():
    state = AnalysisWizardState(command="comfort", room_scope="Alle Räume", room_count=2)

    assert room_selection_disabled(state) is False
    assert analysis_step_complete(state, "rooms", room_selection_disabled=True) is True


def test_analysis_wizard_groups_plot_template_options_in_template_diagram():
    state = AnalysisWizardState(command=PLOT_TEMPLATE_STEP, plot_template="heating-overlay")

    assert visible_analysis_steps(state, template_supports_overlays=False) == (
        "command",
        "subcommand",
        "export",
        "template_diagram",
        "variants",
        "rooms",
        "run",
    )
    assert visible_analysis_steps(state, template_supports_overlays=True) == (
        "command",
        "subcommand",
        "export",
        "template_diagram",
        "variants",
        "rooms",
        "run",
    )


def test_analysis_wizard_completes_heating_timeline_like_tkinter():
    incomplete = AnalysisWizardState(command="heating", load_subcommand="timeline", variant_mode="compare")

    assert analysis_step_complete(incomplete, "template_diagram", template_view="") is False

    complete = AnalysisWizardState(
        command="heating",
        load_subcommand="timeline",
        variant_mode="compare",
        series_layout="combined",
        view="week",
        week=7,
    )

    assert analysis_step_complete(complete, "template_diagram", template_view="") is True
    assert analysis_step_summary(complete, "export") == "compare, combined"
    assert analysis_step_summary(complete, "template_diagram") == "Woche 7"


def test_analysis_wizard_places_single_compare_in_export():
    state = AnalysisWizardState(
        command="plot-template-analyse",
        plot_template_group="heating",
        plot_template_mode="single",
        plot_template="heating-year",
        view="year",
    )

    assert analysis_step_complete(state, "subcommand") is True
    assert analysis_step_complete(state, "export") is True
    assert analysis_step_summary(state, "export") == "single"


def test_analysis_wizard_does_not_limit_comfort_outputs_by_analysis_level():
    room_state = AnalysisWizardState(
        command="comfort",
        comfort_subcommand="t_op_rel_hum",
        comfort_type="plot_analysis",
    )
    variant_state = AnalysisWizardState(
        command="comfort",
        comfort_subcommand="t_op_rel_hum",
        comfort_type="plot_analysis",
        analysis_level="Analyse Variante",
    )

    assert analysis_step_complete(room_state, "subcommand") is True
    assert analysis_step_complete(variant_state, "subcommand") is True
    assert analysis_step_complete(room_state, "template_diagram") is True
    assert analysis_step_complete(variant_state, "template_diagram") is True


def test_tkinter_analyse_launcher_uses_module_command():
    command = build_tkinter_analyse_command("python")

    assert command == ("python", "-m", "ma_analyse", "gui")


def test_tkinter_analyse_launcher_returns_process_id(monkeypatch, tmp_path):
    calls: dict[str, object] = {}

    class FakeProcess:
        pid = 1234

    def fake_popen(command, cwd=None):
        calls["command"] = command
        calls["cwd"] = cwd
        return FakeProcess()

    monkeypatch.setattr("ma_ui.legacy_launchers.subprocess.Popen", fake_popen)

    result = launch_tkinter_analyse(python_executable="python", cwd=tmp_path)

    assert result.success is True
    assert result.process_id == 1234
    assert calls["command"] == ("python", "-m", "ma_analyse", "gui")
    assert calls["cwd"] == str(tmp_path)


def test_analyse_view_variant_selection_uses_none_for_all_variants():
    assert variant_selection_from_scope("", "Alle Varianten") is None
    assert variant_selection_from_scope("Variant_A", "Mehrere Varianten") == ["Variant_A"]


def test_analyse_view_uses_selected_variants_before_manual_text():
    assert variant_text_from_selection("Mehrere Varianten", ["Variant_A", "Variant_B"], "Manual") == (
        "Variant_A,Variant_B"
    )
    assert variant_text_from_selection("Eine Variante", ["Variant_A", "Variant_B"], "Manual") == "Variant_A"
    assert variant_text_from_selection("Alle Varianten", ["Variant_A"], "Manual") == ""
    assert variant_text_from_selection("Mehrere Varianten", [], "Manual") == "Manual"


def test_analyse_view_uses_selected_rooms_before_manual_text():
    assert room_text_from_selection(["101 lobby", "208 office"], "Manual") == "101 lobby,208 office"
    assert room_text_from_selection([], "Manual") == "Manual"


def test_analyse_view_limits_single_room_template_selection():
    single_room_spec = {"requires_single_room": True}
    multi_room_spec = {"requires_single_room": False}

    assert room_values_from_template_selection(
        selected_rooms=["101 lobby", "208 office"],
        manual_value="",
        template_spec=single_room_spec,
    ) == ["101 lobby"]
    assert room_values_from_template_selection(
        selected_rooms=["101 lobby", "208 office"],
        manual_value="",
        template_spec=multi_room_spec,
    ) == ["101 lobby", "208 office"]


def test_analyse_view_uses_first_selected_value_with_fallback():
    assert first_selected_value(["Variant_B"], ["Variant_A"]) == "Variant_B"
    assert first_selected_value([], ["Variant_A"]) == "Variant_A"
    assert first_selected_value([], []) is None


def test_analyse_view_reads_template_spec_flags():
    assert plot_template_requires_single_room({"requires_single_room": True}) is True
    assert plot_template_requires_single_room({"requires_single_room": False}) is False
    assert plot_template_supports_overlays({"supports_overlays": True}) is True
    assert plot_template_supports_overlays({"supports_overlays": False}) is False


def test_analyse_view_builds_time_options_from_template_spec():
    assert build_template_time_options({"view": "year"}, month="Feb", week=7, day=15) == {
        "month": None,
        "week": None,
        "day": None,
    }
    assert build_template_time_options({"view": "month"}, month="Feb", week=7, day=15) == {
        "month": "Feb",
        "week": None,
        "day": None,
    }
    assert build_template_time_options({"view": "week"}, month="Feb", week=7, day=15) == {
        "month": None,
        "week": 7,
        "day": None,
    }
    assert build_template_time_options({"view": "day"}, month="Feb", week=7, day=15) == {
        "month": "Feb",
        "week": None,
        "day": 15,
    }


def test_analyse_view_builds_catalog_overlay_line():
    assert build_catalog_overlay_line("csv", "custom_power", "", "heat") == {
        "source": "csv",
        "column": "custom_power",
        "label": "custom_power",
        "axis": "heat",
    }
    assert build_catalog_overlay_line("invalid", "custom_power", "Custom", "heat") is None
    assert build_catalog_overlay_line("csv", "", "Custom", "heat") is None


def test_analyse_view_manages_free_overlay_lines_in_session_state():
    state: dict[str, object] = {}
    line = {"source": "csv", "column": "custom_power", "label": "Custom", "axis": "heat"}

    assert add_session_overlay_line(line, state) is True
    assert add_session_overlay_line(line, state) is False
    assert get_session_overlay_lines(state) == [line]
    assert remove_session_overlay_line(0, state) == []
    assert get_session_overlay_lines(state) == []


def test_analyse_view_rejects_invalid_free_overlay_line():
    state: dict[str, object] = {}

    assert add_session_overlay_line({"source": "bad", "column": "x", "label": "X", "axis": "heat"}, state) is False
    assert get_session_overlay_lines(state) == []


def test_analyse_view_safe_overlay_catalog_returns_empty_for_missing_data(tmp_path):
    catalog = safe_list_plot_overlay_sources(
        database_dir=str(tmp_path / "database"),
        input_dir=str(tmp_path / "ida_imports"),
        variant_name="Variant_A",
        room_name="208 office",
        outdoor_column="tair",
    )

    assert catalog == {"csv": [], "aux": []}


def test_analyse_view_builds_analysis_config_for_heating():
    config = build_analysis_config(
        step="heating",
        input_dir="data/ma_analyse/ida_imports",
        database_dir="data/ma_analyse/database",
        output_root="data/ma_analyse/output",
        run_id="manual_run",
        variants="Variant_A, Variant_B",
        rooms="101 lobby, 208 office",
        debug=True,
        view="week",
        week=7,
        variant_mode="compare",
        series_layout="combined",
    )

    assert config.steps == ("heating",)
    assert config.run_id == "manual_run"
    assert config.variants == ["Variant_A", "Variant_B"]
    assert config.rooms == ["101 lobby", "208 office"]
    assert config.view == "week"
    assert config.week == 7
    assert config.variant_mode == "compare"
    assert config.series_layout == "combined"


def test_analyse_view_builds_analysis_config_for_all_variants():
    config = build_analysis_config(
        step="heating",
        input_dir="data/ma_analyse/ida_imports",
        database_dir="data/ma_analyse/database",
        output_root="data/ma_analyse/output",
        run_id="",
        variants="",
        analysis_scope="Alle Varianten",
        rooms="208 office",
        debug=False,
    )

    assert config.variants is None


def test_analyse_view_builds_analysis_config_for_excel_analysis():
    config = build_analysis_config(
        step="analyze-data",
        input_dir="data/ma_analyse/ida_imports",
        database_dir="data/ma_analyse/database",
        output_root="data/ma_analyse/output",
        run_id="",
        variants="Variant_A",
        rooms="208 office",
        debug=False,
        series_layout="combined",
    )

    assert config.steps == ("analyze-data",)
    assert config.run_id is None
    assert config.series_layout == "combined"


def test_analyse_view_builds_plot_template_options():
    options = build_plot_template_options(
        template="heating-overlay",
        month="Feb",
        show_setpoint_band=True,
        show_outdoor_temperature=False,
        overlay_lines=[{"source": "csv", "column": "zone_energy_q_heat", "label": "Heizung", "axis": "heat"}],
        fixed_overlays=[{"source": "aux", "column": "tair", "label": "Aussenluft", "axis": "temperature"}],
    )

    assert options["template"] == "heating-overlay"
    assert options["month"] == "Feb"
    assert options["show_setpoint_band"] is True
    assert options["show_outdoor_temperature"] is False
    assert options["overlay_lines"][0]["column"] == "zone_energy_q_heat"
    assert options["fixed_overlays"][0]["column"] == "tair"


def test_analyse_view_parses_overlay_lines_text():
    overlay_lines = parse_overlay_lines_text(
        "csv,zone_energy_q_heat,Heizung,heat\n"
        "aux,tair,Aussenluft,temperature\n"
        "invalid,line\n"
        "csv,,Leer,heat"
    )

    assert overlay_lines == [
        {"source": "csv", "column": "zone_energy_q_heat", "label": "Heizung", "axis": "heat"},
        {"source": "aux", "column": "tair", "label": "Aussenluft", "axis": "temperature"},
    ]


def test_created_file_rows_reports_existing_files(tmp_path):
    result_file = tmp_path / "report.txt"
    result_file.write_text("content", encoding="utf-8")

    rows = created_file_rows([result_file])

    assert rows == [
        {
            "Datei": "report.txt",
            "Pfad": str(result_file),
            "Groesse Byte": 7,
            "Vorhanden": True,
        }
    ]


def test_preview_image_paths_reports_existing_images_only(tmp_path):
    image_file = tmp_path / "plot.PNG"
    text_file = tmp_path / "report.txt"
    missing_image = tmp_path / "missing.jpg"
    image_file.write_text("image", encoding="utf-8")
    text_file.write_text("text", encoding="utf-8")

    assert is_preview_image(image_file) is True
    assert is_preview_image(text_file) is False
    assert preview_image_paths([image_file, text_file, missing_image]) == [image_file]


def test_weather_dataset_rows_report_missing_local_file():
    dataset = WeatherDataset(
        weather_key="TRY_TEST",
        display_name="Test TRY",
        file_path=Path("data/ma_weather/input/missing.dat"),
        file_format="TRY",
        source="DWD",
        location="Frankfurt",
        year_type="reference_year",
    )

    rows = weather_dataset_rows([dataset])

    assert rows[0]["weather_key"] == "TRY_TEST"
    assert rows[0]["Datei vorhanden"] is False


def test_weather_ui_helpers_prepare_metrics_and_plot_rows(tmp_path):
    metrics = WeatherMetrics(
        mean_temperature_c=10.123,
        min_temperature_c=-5.0,
        max_temperature_c=31.0,
        mean_relative_humidity_pct=70.0,
        mean_wind_speed_m_s=2.5,
        max_wind_speed_m_s=7.0,
        global_radiation_kwh_m2a=1200.0,
        hours_above_25c=80,
        hours_above_30c=12,
        heating_degree_hours_kh=1234.56,
        cooling_degree_hours_kh=98.76,
    )
    image_path = tmp_path / "TRY_TEST_temperature_year.png"
    image_path.write_text("image", encoding="utf-8")
    plot_results = (
        WeatherPlotResult("temperature_year", image_path, "created"),
        WeatherPlotResult("wind_rose", None, "skipped", ("missing wind",)),
    )

    metric_rows = weather_metric_rows(metrics)
    plot_rows = weather_plot_rows(plot_results)

    assert metric_rows[0] == {"Kennwert": "Mittlere Temperatur [Grad C]", "Wert": 10.12}
    assert plot_rows[0]["Vorhanden"] is True
    assert plot_rows[1]["Hinweise"] == "missing wind"
    assert created_weather_plot_paths(plot_results) == [image_path]


def test_weather_start_year_uses_dataset_metadata():
    dataset = WeatherDataset(
        weather_key="TRY_FFM_2045",
        display_name="TRY Frankfurt 2045 Jahr",
        file_path=Path("data/ma_weather/input/TRY_501262086894/TRY2045_501262086894_Jahr.dat"),
        file_format="TRY",
        source="DWD",
        location="Frankfurt",
        year_type="future_year",
    )

    assert weather_start_year(dataset) == 2045


def test_economic_assumption_rows_use_existing_importer():
    assumptions, errors = import_economic_assumptions("config/ma_variants/economic/example_economic_assumptions.yaml")

    rows = economic_assumption_rows(assumptions)

    assert errors == []
    assert len(rows["system_costs"]) == 4
    assert len(rows["energy_prices"]) == 2
    assert rows["scenarios"][0]["scenario_key"] == "example_20y"
