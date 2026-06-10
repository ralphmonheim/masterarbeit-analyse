from pathlib import Path

from ma_ui.app import get_renderable_page_keys
from ma_ui.components import created_file_rows
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
    build_analysis_config,
    build_catalog_overlay_line,
    build_plot_template_options,
    first_selected_value,
    parse_overlay_lines_text,
    room_text_from_selection,
    safe_list_plot_overlay_sources,
    split_csv_text,
    variant_selection_from_scope,
    variant_text_from_selection,
)
from ma_ui.navigation import get_navigation_page, get_navigation_pages
from ma_ui.pages.assessment import economic_assumption_rows
from ma_ui.pages.weather import weather_dataset_rows
from ma_ui.post_process_view import post_process_step_rows
from ma_ui.pre_process_view import pre_process_step_rows
from ma_ui.shared.workflow_context import workflow_context_rows
from ma_ui.state import ProjectState
from ma_ui.workflow_view import workflow_step_rows
from ma_variants.economic_analysis import import_economic_assumptions
from ma_weather import WeatherDataset


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

    assert analyse_page.module_key == "ma_analyse"
    assert analyse_page.status == "partial"


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


def test_workflow_context_rows_show_module_status_and_action():
    rows = workflow_context_rows(("parameters", "ida_export"))

    assert rows[0]["Modul"] == "ma_parameters"
    assert rows[0]["Dashboard-Aktion"] == "Parameter oeffnen"
    assert rows[1]["Modul"] == "ma_export_ida"
    assert rows[1]["Status"] == "partial"


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


def test_analyse_view_uses_first_selected_value_with_fallback():
    assert first_selected_value(["Variant_B"], ["Variant_A"]) == "Variant_B"
    assert first_selected_value([], ["Variant_A"]) == "Variant_A"
    assert first_selected_value([], []) is None


def test_analyse_view_builds_catalog_overlay_line():
    assert build_catalog_overlay_line("csv", "custom_power", "", "heat") == {
        "source": "csv",
        "column": "custom_power",
        "label": "custom_power",
        "axis": "heat",
    }
    assert build_catalog_overlay_line("invalid", "custom_power", "Custom", "heat") is None
    assert build_catalog_overlay_line("csv", "", "Custom", "heat") is None


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
    )

    assert options["template"] == "heating-overlay"
    assert options["month"] == "Feb"
    assert options["show_setpoint_band"] is True
    assert options["show_outdoor_temperature"] is False
    assert options["overlay_lines"][0]["column"] == "zone_energy_q_heat"


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


def test_economic_assumption_rows_use_existing_importer():
    assumptions, errors = import_economic_assumptions("config/ma_variants/economic/example_economic_assumptions.yaml")

    rows = economic_assumption_rows(assumptions)

    assert errors == []
    assert len(rows["system_costs"]) == 4
    assert len(rows["energy_prices"]) == 2
    assert rows["scenarios"][0]["scenario_key"] == "example_20y"
