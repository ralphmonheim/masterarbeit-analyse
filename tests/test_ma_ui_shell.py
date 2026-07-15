import importlib
import queue
from argparse import Namespace
from pathlib import Path
from types import MappingProxyType

import pandas as pd
from ma_ui.module_views.analyse_view import (
    COMMAND_OPTIONS,
    DEFAULT_COMMAND_INDEX,
    PLOT_TEMPLATE_STEP,
    add_session_overlay_line,
    get_session_overlay_lines,
    remove_session_overlay_line,
    safe_list_plot_overlay_sources,
)
from ma_ui.pages.assessment import economic_assumption_rows
from ma_ui.pages.home import workflow_phase_summary_rows, workflow_status_counts
from ma_ui.pages.weather import (
    created_weather_plot_paths,
    get_weather_session_id,
    weather_dataset_label,
    weather_dataset_rows,
    weather_dataset_type_label,
    weather_event_rows,
    weather_location_rows,
    weather_metric_rows,
    weather_plot_rows,
    weather_start_year,
    weather_status_rows,
)
from ma_ui.shared.workflow_context import workflow_context_rows

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
from ma_analyse.models import AnalysisConfig, AnalysisResult
from ma_building import load_business_integration_lod1_building_spec
from ma_database import DemoCatalog, DemoCatalogRecord
from ma_technical import load_business_integration_lod1_technical_spec
from ma_ui import app as ma_ui_app
from ma_ui import workflow_view
from ma_ui.app import (
    get_renderable_page_keys,
    has_module_view,
    is_module_info_active,
)
from ma_ui.components import created_file_rows, is_preview_image, preview_image_paths
from ma_ui.legacy_launchers import build_tkinter_analyse_command, launch_tkinter_analyse
from ma_ui.main_dashboard import dashboard_action_rows
from ma_ui.module_views import (
    analyse_view,
    assessment_view,
    building_view,
    dimensioning_view,
    export_ida_view,
    feedback_view,
    home_view,
    import_ida_view,
    module_info_view,
    parameters_view,
    simulation_setup_view,
    technical_view,
    variants_view,
    weather_view,
    zones_view,
)
from ma_ui.navigation import (
    CONFIGURATION_RETURN_PAGE_SESSION_KEY,
    CURRENT_PAGE_SESSION_KEY,
    MODULE_INFO_PAGE_SESSION_KEY,
    SCROLL_TO_TOP_SESSION_KEY,
    VIEW_MODE_SESSION_KEY,
    WORKFLOW_VIEW_MODE,
    WORKSPACE_VIEW_MODE,
    consume_scroll_to_top,
    get_navigation_page,
    get_navigation_pages,
    next_page_key,
    normalize_page_key,
    normalize_view_mode,
    previous_page_key,
    return_to_configuration_origin,
    select_page,
    select_related_configuration_page,
    set_module_info_active,
    toggle_view_mode,
)
from ma_ui.pages import weather as weather_page
from ma_ui.post_process_view import post_process_step_rows
from ma_ui.pre_process_view import pre_process_step_rows
from ma_ui.resource_status import ResourceSpec, resource_status, resource_status_rows, resource_statuses_for_step
from ma_ui.shared import normalize_table_for_streamlit
from ma_ui.state import ProjectState
from ma_ui.tkinter_app.module_views.analyse import app as tkinter_analyse_app
from ma_ui.tkinter_app.module_views.analyse.cli import parse_tkinter_analyse_args
from ma_ui.tkinter_app.module_views.analyse.pipeline_config import build_tkinter_analysis_config
from ma_ui.tkinter_app.module_views.analyse.restart import build_gui_restart_argv
from ma_ui.workflow_graph import (
    VISUAL_PHASES,
    cross_cutting_card_rows,
    feedback_path_rows,
    status_style,
    target_page_for_step,
    workflow_card_rows,
    workflow_cards_by_phase,
)
from ma_ui.workflow_view import (
    WORKFLOW_IMAGE_PATH,
    WORKFLOW_PDF_PATH,
    workflow_reference_asset_rows,
    workflow_step_rows,
)
from ma_variants.economic_analysis import import_economic_assumptions
from ma_weather import (
    WeatherCatalog,
    WeatherDataset,
    WeatherDatasetStatus,
    WeatherDiscoveryStatus,
    WeatherEvent,
    WeatherFileDiscovery,
    WeatherFileStatus,
    WeatherImportCheckStatus,
    WeatherLocation,
    WeatherMetrics,
    WeatherPlotResult,
    import_weather_location_catalog,
)
from ma_workflow import get_step
from ma_zones import load_business_integration_lod1_zone_spec


def test_combined_ui_package_branches_are_importable():
    package_names = (
        "ma_ui.app",
        "ma_ui.streamlit_app",
        "ma_ui.streamlit_app.app",
        "ma_ui.tkinter_app",
        "ma_ui.tkinter_app.module_views.analyse",
        "ma_ui.tkinter_app.module_views.analyse.app",
        "ma_ui.tkinter_app.module_views.analyse.selection",
    )

    imported = [importlib.import_module(package_name) for package_name in package_names]

    assert [module.__name__ for module in imported] == list(package_names)


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
    assert "core" in page_keys
    assert "project" in page_keys
    assert "zones" in page_keys
    assert "technical" in page_keys
    assert "dimensioning" in page_keys
    assert "analysis_core" in page_keys
    assert "standards_compliance" in page_keys
    assert "sensitivity" in page_keys
    assert "export_simulation" in page_keys
    assert "import_simulation" in page_keys
    assert "reporting" in page_keys
    assert "validation" in page_keys


def test_ui_navigation_follows_the_canonical_phase_2_input_order():
    page_keys = [page.page_key for page in get_navigation_pages()]

    assert page_keys.index("weather") < page_keys.index("building") < page_keys.index("technical")
    assert page_keys.index("technical") < page_keys.index("zones") < page_keys.index("parameters")


def test_ui_navigation_page_metadata():
    analyse_page = get_navigation_page("analyse")
    weather_page = get_navigation_page("weather")
    variants_page = get_navigation_page("variants")
    import_page = get_navigation_page("import_simulation")

    assert analyse_page.module_key == "ma_analyse.stage_2_optimization"
    assert analyse_page.status == "partial"
    assert weather_page.module_key == "ma_weather"
    assert weather_page.status == "partial"
    assert variants_page.status == "planned"
    assert import_page.status == "planned"
    assert get_navigation_page("import_ida") == import_page
    assert get_navigation_page("ida_import") == import_page


def test_navigation_statuses_follow_central_workflow_catalog():
    page_to_step = {
        "parameters": "parameters",
        "weather": "weather",
        "building": "building",
        "variants": "variants",
        "simulation_setup": "simulation_setup",
        "export_simulation": "export_simulation",
        "import_simulation": "import_simulation",
        "analyse": "optimization",
        "assessment": "assessment",
        "feedback": "feedback",
    }

    for page_key, step_key in page_to_step.items():
        assert get_navigation_page(page_key).status == get_step(step_key).status


def test_renderable_pages_include_variants():
    page_keys = get_renderable_page_keys()

    assert page_keys[0] == "home"
    assert "variants" in page_keys
    assert "weather" in page_keys
    assert "export_simulation" in page_keys
    assert "import_simulation" in page_keys
    assert "documentation" in page_keys


def test_navigation_normalizes_unknown_session_page_key():
    assert CURRENT_PAGE_SESSION_KEY == "ma_ui_current_page"
    assert VIEW_MODE_SESSION_KEY == "ma_ui_view_mode"
    assert SCROLL_TO_TOP_SESSION_KEY == "ma_ui_scroll_to_top"
    assert normalize_page_key("analyse", ("home", "analyse")) == "analyse"
    assert normalize_page_key(
        "export_ida",
        ("home", "export_simulation"),
    ) == "export_simulation"
    assert normalize_page_key("missing", ("home", "analyse")) == "home"
    assert normalize_page_key(None, ("home", "analyse")) == "home"
    assert normalize_view_mode(WORKFLOW_VIEW_MODE) == WORKFLOW_VIEW_MODE
    assert normalize_view_mode("missing") == WORKSPACE_VIEW_MODE


def test_navigation_toggles_view_mode():
    session_state: dict[str, object] = {}

    assert toggle_view_mode(session_state) == WORKFLOW_VIEW_MODE
    assert session_state[VIEW_MODE_SESSION_KEY] == WORKFLOW_VIEW_MODE
    assert toggle_view_mode(session_state) == WORKSPACE_VIEW_MODE
    assert session_state[VIEW_MODE_SESSION_KEY] == WORKSPACE_VIEW_MODE


def test_navigation_previous_and_next_page_keys_are_stable():
    page_keys = ("home", "parameters", "weather")

    assert previous_page_key("home", page_keys) == "home"
    assert previous_page_key("weather", page_keys) == "parameters"
    assert next_page_key("home", page_keys) == "parameters"
    assert next_page_key("weather", page_keys) == "weather"
    assert next_page_key("missing", page_keys) == "parameters"


def test_module_info_mode_is_only_active_for_registered_module_views():
    assert has_module_view("weather") is True
    assert has_module_view("analyse") is True
    assert has_module_view("variants") is True
    assert has_module_view("assessment") is True
    assert has_module_view("parameters") is True
    assert has_module_view("project") is True
    assert has_module_view("workflow") is True
    assert has_module_view("building") is True
    assert has_module_view("zones") is True
    assert has_module_view("technical") is True
    assert has_module_view("dimensioning") is True
    assert has_module_view("home") is False
    assert is_module_info_active("weather", "weather") is True
    assert is_module_info_active("weather", "analyse") is False
    assert is_module_info_active("parameters", "parameters") is True


def test_page_renderer_switches_between_module_view_and_info(monkeypatch):
    calls: list[str] = []
    monkeypatch.setitem(
        ma_ui_app._PAGE_RENDERERS,
        "weather",
        lambda: calls.append("module-view"),
    )
    monkeypatch.setattr(
        ma_ui_app.module_info_view,
        "render",
        lambda module_key: calls.append(f"info:{module_key}"),
    )

    weather_page = get_navigation_page("weather")
    ma_ui_app._render_page(weather_page)
    ma_ui_app._render_page(weather_page, show_module_info=True)
    ma_ui_app._render_page(get_navigation_page("parameters"), show_module_info=True)
    ma_ui_app._render_page(weather_page, view_mode=WORKFLOW_VIEW_MODE)

    assert calls == [
        "module-view",
        "info:ma_weather",
        "info:ma_parameters",
        "module-view",
    ]


def test_stale_workflow_mode_does_not_render_project_as_module_info(monkeypatch):
    calls: list[str] = []
    monkeypatch.setitem(
        ma_ui_app._PAGE_RENDERERS,
        "project",
        lambda: calls.append("project-view"),
    )
    monkeypatch.setattr(
        ma_ui_app.module_info_view,
        "render",
        lambda module_key: calls.append(f"info:{module_key}"),
    )

    ma_ui_app._render_page(get_navigation_page("project"), view_mode=WORKFLOW_VIEW_MODE)

    assert calls == ["project-view"]


def test_workflow_home_renders_home_overview(monkeypatch):
    streamlit_app = importlib.import_module("ma_ui.streamlit_app.app")
    calls: list[str] = []
    monkeypatch.setattr(streamlit_app.home_view, "render", lambda: calls.append("home-view"))
    monkeypatch.setattr(
        streamlit_app.module_info_view,
        "render",
        lambda module_key: calls.append(f"info:{module_key}"),
    )

    streamlit_app._render_page(get_navigation_page("home"), view_mode=WORKFLOW_VIEW_MODE)

    assert calls == ["home-view"]


def test_workflow_module_page_uses_workflow_renderer(monkeypatch):
    streamlit_app = importlib.import_module("ma_ui.streamlit_app.app")
    calls: list[str] = []
    monkeypatch.setitem(streamlit_app._PAGE_RENDERERS, "workflow", lambda: calls.append("workflow-view"))
    monkeypatch.setattr(streamlit_app.workflow_view, "render", lambda: calls.append("workflow-view"))

    streamlit_app._render_page(get_navigation_page("workflow"))
    streamlit_app._render_page(get_navigation_page("workflow"), view_mode=WORKFLOW_VIEW_MODE)

    assert calls == ["workflow-view", "workflow-view"]


def test_page_navigation_and_info_toggle_update_session_state():
    session_state: dict[str, object] = {}

    set_module_info_active(session_state, "weather", active=True)
    assert session_state[MODULE_INFO_PAGE_SESSION_KEY] == "weather"
    assert SCROLL_TO_TOP_SESSION_KEY not in session_state

    select_page(session_state, "variants")
    assert session_state[CURRENT_PAGE_SESSION_KEY] == "variants"
    assert MODULE_INFO_PAGE_SESSION_KEY not in session_state
    assert session_state[SCROLL_TO_TOP_SESSION_KEY] is True
    assert consume_scroll_to_top(session_state) is True
    assert consume_scroll_to_top(session_state) is False


def test_configuration_links_store_return_page_and_normal_navigation_clears_it():
    session_state: dict[str, object] = {}

    select_related_configuration_page(
        session_state,
        "parameters",
        return_page_key="variants",
    )

    assert session_state[CURRENT_PAGE_SESSION_KEY] == "parameters"
    assert session_state[CONFIGURATION_RETURN_PAGE_SESSION_KEY] == "variants"
    assert session_state[SCROLL_TO_TOP_SESSION_KEY] is True
    assert consume_scroll_to_top(session_state) is True
    assert return_to_configuration_origin(session_state) == "variants"
    assert session_state[CURRENT_PAGE_SESSION_KEY] == "variants"
    assert CONFIGURATION_RETURN_PAGE_SESSION_KEY not in session_state
    assert session_state[SCROLL_TO_TOP_SESSION_KEY] is True

    select_related_configuration_page(session_state, "project", return_page_key="variants")
    select_page(session_state, "home")
    assert CONFIGURATION_RETURN_PAGE_SESSION_KEY not in session_state
    assert session_state[SCROLL_TO_TOP_SESSION_KEY] is True

    set_module_info_active(session_state, "variants", active=True)
    set_module_info_active(session_state, "variants", active=False)
    assert MODULE_INFO_PAGE_SESSION_KEY not in session_state


def test_module_views_are_importable():
    renderers = (
        home_view.render,
        parameters_view.render,
        weather_view.render,
        building_view.render,
        zones_view.render,
        technical_view.render,
        dimensioning_view.render,
        variants_view.render,
        simulation_setup_view.render,
        export_ida_view.render,
        import_ida_view.render,
        analyse_view.render,
        assessment_view.render,
        feedback_view.render,
        module_info_view.render,
        workflow_view.render,
    )

    assert all(callable(renderer) for renderer in renderers)


def test_building_view_exposes_business_integration_lod1_spec():
    option_rows = building_view.building_spec_option_rows()
    option_keys = {row["Schluessel"] for row in option_rows}

    assert "business_integration_lod1" in option_keys

    spec = load_business_integration_lod1_building_spec()
    summary_rows = building_view.building_spec_summary_rows(spec)
    summary_by_key = {row["Kennwert"]: row["Wert"] for row in summary_rows}

    assert summary_by_key["Eingabe-LoD"] == "LOD-1"
    assert summary_by_key["U-Wert Aussenwand [W/m2K]"] == 0.24
    assert summary_by_key["Fensteranteil [%]"] == 25.0


def test_building_construction_rows_resolve_demo_material_layers():
    catalog = DemoCatalog(
        catalog_id="CAT-TEST-UI",
        catalog_version="test",
        records_by_category=MappingProxyType(
            {
                "materials": (
                    DemoCatalogRecord(
                        category="materials",
                        record_id="MAT-TEST-UI",
                        label="Neutrales Testmaterial",
                        data=MappingProxyType(
                            {"verification_status": "draft_unverified", "confirmation_status": "unconfirmed"}
                        ),
                    ),
                )
            }
        ),
        construction_layers=(
            MappingProxyType(
                {
                    "construction_id": "CON-TEST-UI",
                    "material_ref": "MAT-TEST-UI",
                    "layer_no": 1,
                    "thickness_m": 0.1,
                    "layer_function": "test_only",
                }
            ),
        ),
    )

    rows = building_view._construction_layer_rows(catalog, "CON-TEST-UI")

    assert len(rows) == 1
    assert rows[0]["Material"] == "Neutrales Testmaterial"


def test_technical_topic_options_include_not_installed():
    assert technical_view._technical_option_label((), "not_installed") == "Nicht vorhanden"
    assert technical_view._technical_option_label((), "present_without_demo_record") == "Vorhanden, noch ohne Demo-Datensatz"


def test_building_zones_and_technical_views_are_registered():
    assert ma_ui_app._PAGE_RENDERERS["building"] is building_view.render
    assert ma_ui_app._PAGE_RENDERERS["zones"] is zones_view.render
    assert ma_ui_app._PAGE_RENDERERS["technical"] is technical_view.render

    zone_rows = zones_view.zones_scope_rows()
    technical_rows = technical_view.technical_scope_rows()

    assert any(row["Stand"] == "Raumdaten" for row in zone_rows)
    assert any(row["Stand"] == "Zonenanforderungen" for row in technical_rows)


def test_zones_and_technical_views_show_lod1_demo_data():
    zone_spec = load_business_integration_lod1_zone_spec()
    technical_spec = load_business_integration_lod1_technical_spec()

    zone_summary = {row["Kennwert"]: row["Wert"] for row in zones_view.zone_summary_rows(zone_spec)}
    technical_summary = {row["Kennwert"]: row["Wert"] for row in technical_view.technical_summary_rows(technical_spec)}

    assert zone_summary["Eingabe-LoD"] == "LOD-1"
    assert zone_summary["Zonen"] == 1
    assert technical_summary["Eingabe-LoD"] == "LOD-1"
    assert technical_summary["Systeme"] == 3


def test_dimensioning_view_is_registered_and_uses_lod1_result():
    from ma_analyse.stage_1_dimensioning import run_business_integration_lod1_reference_dimensioning

    assert ma_ui_app._PAGE_RENDERERS["dimensioning"] is dimensioning_view.render

    result = run_business_integration_lod1_reference_dimensioning()
    summary_rows = {
        row["Kennwert"]: row["Wert"]
        for row in dimensioning_view.dimensioning_summary_rows(result)
    }

    assert summary_rows["Status"] == "evaluated"
    assert summary_rows["Heizlast gesamt"] == 1701.6


def test_dashboard_and_workflow_rows_cover_target_structure():
    dashboard_rows = dashboard_action_rows()
    workflow_rows = workflow_step_rows()
    asset_rows = workflow_reference_asset_rows()
    pre_process_rows = pre_process_step_rows()
    post_process_rows = post_process_step_rows()

    assert any(row["Aktion"] == "open_simulation_setup" for row in dashboard_rows)
    assert any(row["Modul"] == "ma_simulation_setup" for row in workflow_rows)
    assert WORKFLOW_IMAGE_PATH.name == "masterarbeit_workflow.png"
    assert WORKFLOW_PDF_PATH.name == "masterarbeit_workflow.pdf"
    assert all(row["Vorhanden"] is True for row in asset_rows)
    assert pre_process_rows[-1]["Modul"] == "ma_export_simulation"
    assert post_process_rows[0]["Modul"] == "ma_import_simulation"


def test_home_page_summarizes_workflow_status_and_phases():
    rows = workflow_step_rows()
    status_counts = workflow_status_counts(rows)
    phase_rows = workflow_phase_summary_rows(rows)

    assert status_counts["available"] >= 1
    assert status_counts["planned"] >= 1
    assert any(row["Phase"].startswith("Phase 0") for row in phase_rows)
    assert any("ma_export_simulation" in row["Module"] for row in phase_rows)


def test_workflow_graph_groups_steps_by_visual_phase():
    cards = workflow_card_rows(available_page_keys=get_renderable_page_keys())
    grouped = workflow_cards_by_phase(cards)

    assert len(VISUAL_PHASES) == 7
    assert VISUAL_PHASES[0].startswith("Phase 0")
    assert VISUAL_PHASES[-1].startswith("Phase 6")
    assert any(card.step_key == "parameters" for card in grouped[VISUAL_PHASES[2]])
    assert any(card.step_key == "simulation" for card in grouped[VISUAL_PHASES[4]])
    assert any(card.step_key == "optimization" for card in grouped[VISUAL_PHASES[4]])
    assert any(card.step_key == "standards_compliance" for card in grouped[VISUAL_PHASES[4]])
    assert any(card.step_key == "sensitivity" for card in grouped[VISUAL_PHASES[4]])
    assert any(card.step_key == "economy" for card in grouped[VISUAL_PHASES[5]])
    assert any(card.step_key == "sustainability" for card in grouped[VISUAL_PHASES[5]])
    assert any(card.step_key == "assessment" for card in grouped[VISUAL_PHASES[5]])


def test_workflow_graph_exposes_cross_cutting_modules_separately():
    cards = cross_cutting_card_rows(available_page_keys=get_renderable_page_keys())

    assert [card.module_key for card in cards] == ["ma_validation", "ma_feedback"]
    assert all(card.visual_phase == "Phasenuebergreifend" for card in cards)
    assert all(card.target_page_key for card in cards)


def test_workflow_graph_uses_stable_status_styles():
    assert status_style("available")["label"] == "Verfuegbar"
    assert status_style("partial")["background"].startswith("#")
    assert status_style("unknown")["label"] == "Unklar"


def test_workflow_graph_maps_steps_to_renderable_pages():
    page_keys = get_renderable_page_keys()

    assert target_page_for_step("parameters", page_keys) == "parameters"
    assert target_page_for_step("export_ida", page_keys) == "export_simulation"
    assert target_page_for_step("import_ida", page_keys) == "import_simulation"
    assert target_page_for_step("ida_export", page_keys) == "export_simulation"
    assert target_page_for_step("ida_import", page_keys) == "import_simulation"
    assert target_page_for_step("simulation", page_keys) == "ida_ice"


def test_workflow_graph_feedback_paths_target_existing_pages():
    page_keys = set(get_renderable_page_keys())
    rows = feedback_path_rows()

    assert {row["Frage"] for row in rows} == {"Model good?", "Data good?", "Room for Optimization?"}
    assert all(row["Zielseite"] in page_keys for row in rows)


def test_workflow_reference_is_only_on_workflow_page():
    home_source = Path("src/ma_ui/streamlit_app/pages/home.py").read_text(encoding="utf-8")
    workflow_source = Path("src/ma_ui/streamlit_app/workflow_view.py").read_text(encoding="utf-8")
    module_sources = [
        path.read_text(encoding="utf-8")
        for path in Path("src/ma_ui/streamlit_app/module_views").glob("*.py")
        if path.name != "home_view.py"
    ]

    assert "Grafischer Workflow" not in home_source
    assert "Masterarbeit Workflow" not in home_source
    assert "Masterarbeit Modul-Ansicht" in home_source
    assert "Modul-Ansicht" in home_source
    assert "Workflow-Referenzdiagramm" not in home_source
    assert "render_workflow_reference" not in home_source
    assert "render_workflow_reference()" in workflow_source
    assert "Workflow-Referenzdiagramm" in workflow_source
    assert "Iterationspfade" in home_source
    assert "ma_ui.streamlit_app.workflow_graph" in home_source
    assert all("ma_ui.streamlit_app.workflow_graph" not in source for source in module_sources)
    assert all("Modul-Ansicht" not in source for source in module_sources)
    assert all("Iterationspfade" not in source for source in module_sources)


def test_ui_uses_top_navigation_instead_of_sidebar_radio():
    app_source = Path("src/ma_ui/streamlit_app/app.py").read_text(encoding="utf-8")

    assert "st.sidebar.radio" not in app_source
    assert "streamlit_html" not in app_source
    assert "st.iframe" not in app_source
    assert "components.html" in app_source
    assert "height=0" not in app_source
    assert "height=1" in app_source
    assert "Start" in app_source
    assert "Zurueck" in app_source
    assert "Weiter" in app_source
    assert "mode_column" not in app_source
    assert 'current_page_key == "home"' in app_source
    assert 'current_page_key == "workflow"' in app_source
    assert '"Workflow"' in app_source
    assert '"Bearbeitung"' in app_source
    assert "Infokarte" in app_source
    assert "Modulansicht" in app_source


def test_weather_dataset_actions_are_in_dataset_section():
    weather_source = Path("src/ma_ui/streamlit_app/pages/weather.py").read_text(encoding="utf-8")
    render_source = weather_source.split("def render()", maxsplit=1)[1]
    top_selection_source = render_source.split("if not active_datasets:", maxsplit=1)[0]
    actions_source = weather_source.split("def _render_weather_dataset_actions", maxsplit=1)[1].split(
        "def _render_weather_import_panel",
        maxsplit=1,
    )[0]
    import_panel_source = weather_source.split("def _render_weather_import_panel", maxsplit=1)[1].split(
        "def _render_weather_discoveries",
        maxsplit=1,
    )[0]
    scan_panel_source = weather_source.split("def _render_weather_scan_panel", maxsplit=1)[1].split(
        "def _render_weather_validation_panel",
        maxsplit=1,
    )[0]
    validation_panel_source = weather_source.split("def _render_weather_validation_panel", maxsplit=1)[1].split(
        "def _render_weather_discovery_validation_result",
        maxsplit=1,
    )[0]
    dataset_section_source = weather_source.split("def _render_weather_dataset_section", maxsplit=1)[1].split(
        "def _render_critical_weather_events",
        maxsplit=1,
    )[0]

    assert "Bestand und Validierung pruefen" not in top_selection_source
    assert "WEATHER_DATASET_ACTION_IMPORT" in actions_source
    assert "WEATHER_DATASET_ACTION_SCAN" in actions_source
    assert "WEATHER_DATASET_ACTION_VALIDATE" in actions_source
    assert '"Import"' in weather_source
    assert '"Scannen"' in weather_source
    assert '"Pruefen"' in weather_source
    assert "st.columns(3)" in actions_source
    assert "_toggle_weather_dataset_action" in actions_source
    assert "_weather_dataset_action_button_type" not in weather_source
    assert "Aktive Ansicht:" not in actions_source
    assert "type=" not in actions_source
    assert "_run_weather_input_discovery" not in actions_source
    assert '"Datensatzbestand pruefen"' in actions_source
    assert "_run_weather_catalog_validation(catalog)" in actions_source
    assert "_run_weather_input_discovery(catalog, location_catalog)" in scan_panel_source
    assert "_run_weather_catalog_validation(catalog)" not in validation_panel_source
    assert "Parameter pruefen" in validation_panel_source
    assert '"Key-Parameter pruefen"' not in validation_panel_source
    assert "_render_weather_dataset_actions(catalog, location_catalog)" in dataset_section_source
    assert "active_action = _active_weather_dataset_action()" in dataset_section_source
    assert "if active_action == WEATHER_DATASET_ACTION_IMPORT" in dataset_section_source
    assert "if active_action == WEATHER_DATASET_ACTION_SCAN" in dataset_section_source
    assert "if active_action == WEATHER_DATASET_ACTION_VALIDATE" in dataset_section_source
    assert "_render_weather_import_panel()" in dataset_section_source
    assert "_render_weather_scan_panel(catalog, location_catalog)" in dataset_section_source
    assert "_render_weather_validation_panel(catalog, location_catalog, status_by_key)" in dataset_section_source
    assert "stage_weather_input_file" in import_panel_source
    assert "selected_location_id" not in import_panel_source
    assert "edited_location_id" not in import_panel_source
    assert "Gefundene lokale TRY-Dateien" in weather_source
    assert "Ort / Vorschlag" in weather_source
    assert "active_column, open_column = st.columns(2)" in dataset_section_source


def test_weather_dataset_default_columns_only_affect_active_table():
    weather_source = Path("src/ma_ui/streamlit_app/pages/weather.py").read_text(encoding="utf-8")
    active_source = weather_source.split("def _render_active_weather_datasets", maxsplit=1)[1].split(
        "def _render_weather_dataset_section",
        maxsplit=1,
    )[0]
    open_source = weather_source.split("def _render_open_weather_datasets", maxsplit=1)[1].split(
        "def _render_active_weather_datasets",
        maxsplit=1,
    )[0]
    discovery_source = weather_source.split("def _render_weather_discoveries", maxsplit=1)[1].split(
        "def _render_weather_scan_panel",
        maxsplit=1,
    )[0]
    dataset_section_source = weather_source.split("def _render_weather_dataset_section", maxsplit=1)[1].split(
        "def _save_generated_weather_plot",
        maxsplit=1,
    )[0]

    assert weather_page.WEATHER_DATASET_DEFAULT_COLUMNS == (
        "Name",
        "Ort",
        "Quelle",
        "Jahrtyp",
        "Datensatztyp",
        "Szenario",
    )
    assert "_weather_dataset_default_table(rows)" in active_source
    assert "active_metric_column, location_metric_column, open_metric_column = st.columns(3)" in dataset_section_source
    assert 'st.metric("Aktive Wetterdatensaetze", len(active_datasets))' in dataset_section_source
    assert 'st.metric("Abgebildete Staedte", _active_weather_location_count(active_datasets))' in dataset_section_source
    assert 'st.metric("Offene Wetterdatensaetze", len(open_rows))' in dataset_section_source
    assert "_weather_dataset_default_table" not in open_source
    assert "_weather_dataset_default_table" not in discovery_source


def test_weather_map_uses_shared_ui_asset_path():
    expected_path = Path.cwd() / "src/ma_ui/assets/weather/klimaregionen_deutschland.png"

    assert weather_page.WEATHER_MAP_IMAGE_PATH == expected_path
    assert expected_path in weather_page.WEATHER_MAP_IMAGE_CANDIDATES
    assert expected_path.exists()


def test_weather_city_selection_starts_without_default():
    weather_source = Path("src/ma_ui/streamlit_app/pages/weather.py").read_text(encoding="utf-8")
    selection_source = weather_source.split("def _render_weather_selection", maxsplit=1)[1].split(
        "def weather_source_rows",
        maxsplit=1,
    )[0]

    assert weather_page.WEATHER_SELECTION_MODE_OPTIONS == ("Stadt", "Klimaregion")
    assert '"Auswahl"' in selection_source
    assert "WEATHER_SELECTION_MODE_OPTIONS" in selection_source
    assert "WEATHER_SELECTION_MODE_CITY" in selection_source
    assert 'placeholder="Stadt auswaehlen"' in selection_source
    assert 'placeholder="Klimaregion auswaehlen"' in selection_source
    assert "index=None" in selection_source


def test_weather_selection_uses_dataset_type_prefilter_and_slim_labels():
    weather_source = Path("src/ma_ui/streamlit_app/pages/weather.py").read_text(encoding="utf-8")
    label_source = weather_source.split("def weather_dataset_label", maxsplit=1)[1].split(
        "def weather_location_label",
        maxsplit=1,
    )[0]
    selection_source = weather_source.split("def _render_weather_selection", maxsplit=1)[1].split(
        "def weather_source_rows",
        maxsplit=1,
    )[0]
    dataset_section_source = weather_source.split("def _render_weather_dataset_section", maxsplit=1)[1].split(
        "def _render_critical_weather_events",
        maxsplit=1,
    )[0]

    assert weather_page.WEATHER_DATASET_TYPE_FILTER_OPTIONS == ("Jahr", "Sommer", "Winter")
    assert '"Datensatztyp"' in selection_source
    assert "st.segmented_control(" in selection_source
    assert 'st.selectbox(\n            "Datensatztyp"' not in selection_source
    assert "WEATHER_DATASET_TYPE_FILTER_OPTIONS" in selection_source
    assert 'selection_mode="single"' in selection_source
    assert "required=True" in selection_source
    assert "_datasets_for_weather_dataset_type(selectable_datasets, selected_dataset_type)" in selection_source
    assert "return dataset.display_name" in label_source
    assert "Empfohlen:" not in label_source
    assert "status.status_label" not in label_source
    assert "Bei Stadtauswahl werden standortgenaue Datensaetze bevorzugt" in selection_source
    assert "Bei Klimaregionsauswahl werden nur Referenzdatensaetze" in selection_source
    assert "Bei Stadtauswahl werden standortgenaue Datensaetze bevorzugt" in dataset_section_source
    assert "Referenzdatensatz der Klimaregion steht zuerst" not in weather_source
    assert "Standortgenaue Datensaetze werden zusaetzlich zur Referenz angezeigt." not in selection_source


def test_weather_selection_context_uses_short_labels():
    weather_source = Path("src/ma_ui/streamlit_app/pages/weather.py").read_text(encoding="utf-8")
    map_source = weather_source.split("def _render_weather_map", maxsplit=1)[1].split(
        "def _display_path",
        maxsplit=1,
    )[0]
    context_source = weather_source.split("def _render_location_context", maxsplit=1)[1].split(
        "def _render_unselected_weather_context",
        maxsplit=1,
    )[0]
    unselected_source = weather_source.split("def _render_unselected_weather_context", maxsplit=1)[1].split(
        "def _render_weather_selection",
        maxsplit=1,
    )[0]
    selection_source = weather_source.split("def _render_weather_selection", maxsplit=1)[1].split(
        "def weather_source_rows",
        maxsplit=1,
    )[0]

    assert '"Klimaregionen Deutschland"' in map_source
    assert '"TRY-Klimaregionen Deutschland"' not in map_source
    assert '"**Klimaregion:** {_weather_region_display_code(region)}"' in context_source
    assert '"**Referenzstandort:** {reference_location.location_name}"' in context_source
    assert '"TRY-Referenzstandort:"' not in context_source
    assert "st.segmented_control(" in unselected_source
    assert '"**Referenzstandort:** -"' in unselected_source
    assert "index=None" in selection_source
    assert "return _render_unselected_weather_context(WEATHER_SELECTION_MODE_CITY)" in selection_source
    assert "return _render_unselected_weather_context(WEATHER_SELECTION_MODE_REGION)" in selection_source
    assert "Bitte zuerst eine Stadt auswaehlen." in weather_source
    assert "Bitte zuerst eine Klimaregion auswaehlen." in weather_source
    assert "Noch keine Stadt ausgewaehlt" in weather_source
    assert "Noch keine Klimaregion ausgewaehlt" in weather_source
    assert "WEATHER_KEY_WIDGET_KEY" in weather_source
    assert "_placeholder" in weather_source


def test_weather_base_statuses_validate_local_imports(monkeypatch):
    regular_dataset = WeatherDataset(
        weather_key="TRY_REGULAR",
        display_name="Regular TRY",
        file_path=Path("data/ma_weather/input/regular.dat"),
        file_format="TRY",
        source="DWD TRY",
        location="Frankfurt",
        year_type="reference_year",
    )
    local_dataset = WeatherDataset(
        weather_key="TRY_LOCAL",
        display_name="Local TRY",
        file_path=Path("data/ma_weather/input/custom/TRY_LOCAL/local.dat"),
        file_format="TRY",
        source="Lokaler Import",
        location="Frankfurt",
        year_type="reference_year",
    )
    calls: list[tuple[str, bool]] = []

    def fake_inspect_weather_dataset_status(
        dataset: WeatherDataset,
        *,
        validate_file: bool = False,
        **_: object,
    ) -> WeatherDatasetStatus:
        calls.append((dataset.weather_key, validate_file))
        return WeatherDatasetStatus(
            weather_key=dataset.weather_key,
            display_name=dataset.display_name,
            file_path=dataset.file_path,
            file_exists=True,
            file_status=WeatherFileStatus.AVAILABLE,
        )

    monkeypatch.setattr(weather_page, "inspect_weather_dataset_status", fake_inspect_weather_dataset_status)

    statuses = weather_page._base_statuses(WeatherCatalog([regular_dataset, local_dataset]))

    assert [status.weather_key for status in statuses] == ["TRY_REGULAR", "TRY_LOCAL"]
    assert calls == [("TRY_REGULAR", False), ("TRY_LOCAL", True)]


def test_weather_regular_dataset_filter_excludes_open_statuses():
    selectable_dataset = WeatherDataset(
        weather_key="TRY_OK",
        display_name="OK TRY",
        file_path=Path("data/ma_weather/input/ok.dat"),
        file_format="TRY",
        source="DWD TRY",
        location="Frankfurt",
        year_type="reference_year",
    )
    open_dataset = WeatherDataset(
        weather_key="TRY_OPEN",
        display_name="Open TRY",
        file_path=Path("data/ma_weather/input/custom/TRY_OPEN/open.dat"),
        file_format="TRY",
        source="Lokaler Import",
        location="Frankfurt",
        year_type="reference_year",
    )
    status_by_key = {
        "TRY_OPEN": WeatherDatasetStatus(
            weather_key="TRY_OPEN",
            display_name="Open TRY",
            file_path=open_dataset.file_path,
            file_exists=True,
            file_status=WeatherFileStatus.AVAILABLE,
            import_status=WeatherImportCheckStatus.ERROR,
            error_count=1,
        )
    }

    datasets = weather_page._regularly_selectable_datasets([selectable_dataset, open_dataset], status_by_key)

    assert datasets == [selectable_dataset]


def test_tkinter_analyse_defaults_to_plot_template_command():
    assert tkinter_analyse_app.DEFAULT_COMMAND == "plot-template"


def test_tkinter_analyse_restart_argv_uses_ma_ui_module(monkeypatch):
    monkeypatch.setattr("ma_ui.tkinter_app.module_views.analyse.restart.sys.executable", "python")
    args = Namespace(
        input_dir="data/input",
        datenbank_dir="data/database",
        output_root="data/output",
        run_id="run-1",
        variants=["Variant_A", "Variant_B"],
        rooms=["101 lobby"],
        view="week",
        month=None,
        week=7,
        day=None,
        heating_mode="single",
        heating_series_layout="combined",
        export_format="both",
        template="heating-overlay",
        debug=False,
        show_setpoint_band=False,
        show_outdoor_temperature=False,
        show_operative_temperature=False,
        gui_window_geometry={"x": 10, "y": 20, "width": 1200, "height": 700},
        gui_window_maximized=True,
    )

    argv = build_gui_restart_argv(args, refresh_port=54321)

    assert argv[:3] == ["python", "-m", "ma_ui.tkinter_app.module_views.analyse"]
    assert "--gui-refresh-port" in argv
    assert "54321" in argv
    assert "--gui-window-maximized" in argv
    assert "1" in argv
    assert "--no-debug" in argv
    assert "--variants" in argv
    assert "Variant_A,Variant_B" in argv


def test_tkinter_analysis_config_maps_gui_state_to_service_config(tmp_path):
    args = Namespace(
        input_dir=tmp_path / "ida_imports",
        datenbank_dir=tmp_path / "database",
        output_root=tmp_path / "output",
        run_id="run-1",
        debug=False,
    )

    config = build_tkinter_analysis_config(
        args=args,
        selected_command="plot-template",
        variants=["Variant_A"],
        rooms=["101 lobby", "208 office"],
        heating_mode="compare",
        prepare_options={"export_format": "both"},
        heating_options={
            "view": "week",
            "month": "Feb",
            "week": 7,
            "day": None,
            "series_layout": "combined",
        },
        plot_template_options={
            "template": "heating-overlay",
            "output_mode": "compare",
            "week": 7,
        },
    )

    assert isinstance(config, AnalysisConfig)
    assert config.steps == ("plot-template",)
    assert config.input_dir == tmp_path / "ida_imports"
    assert config.database_dir == tmp_path / "database"
    assert config.output_root == tmp_path / "output"
    assert config.run_id == "run-1"
    assert config.debug is False
    assert config.variants == ["Variant_A"]
    assert config.rooms == ["101 lobby", "208 office"]
    assert config.export_format == "both"
    assert config.variant_mode == "compare"
    assert config.view == "week"
    assert config.month == "Feb"
    assert config.week == 7
    assert config.series_layout == "combined"
    assert config.plot_template == "heating-overlay"
    assert config.plot_template_mode == "compare"
    assert config.load_kind is None


def test_tkinter_analysis_config_maps_comfort_command(tmp_path):
    args = Namespace(
        input_dir=tmp_path / "ida_imports",
        datenbank_dir=tmp_path / "database",
        output_root=tmp_path / "output",
        run_id=None,
        debug=True,
    )

    config = build_tkinter_analysis_config(
        args=args,
        selected_command="comfort",
        variants=["Variant_A"],
        rooms=["101 lobby"],
        heating_mode="",
        comfort_output_type="plot_analysis_overview",
    )

    assert config.steps == ("comfort",)
    assert config.comfort_output_type == "plot_analysis_overview"
    assert config.variant_mode is None
    assert config.export_format == "csv"
    assert config.load_kind is None


def test_tkinter_analysis_config_maps_load_kind_for_heating(tmp_path):
    args = Namespace(
        input_dir=tmp_path / "ida_imports",
        datenbank_dir=tmp_path / "database",
        output_root=tmp_path / "output",
        run_id="",
        debug=True,
    )

    config = build_tkinter_analysis_config(
        args=args,
        selected_command="heating",
        variants=["Variant_A", "Variant_B"],
        rooms=["101 lobby"],
        heating_mode="compare",
        heating_options={"view": "year", "series_layout": "separate"},
    )

    assert config.steps == ("heating",)
    assert config.load_kind == "heating"
    assert config.variants == ["Variant_A", "Variant_B"]
    assert config.rooms == ["101 lobby"]
    assert config.run_id is None
    assert config.variant_mode == "compare"
    assert config.view == "year"
    assert config.series_layout == "separate"


def test_tkinter_pipeline_worker_uses_workflow_action(monkeypatch, tmp_path):
    captured: dict[str, AnalysisConfig] = {}

    def fake_run_analysis_action(config):
        captured["config"] = config
        return AnalysisResult(
            success=True,
            steps=config.steps,
            log_text="service log",
            created_files=[tmp_path / "out.png"],
        )

    monkeypatch.setattr(
        "ma_ui.tkinter_app.module_views.analyse.pipeline_runner.run_analysis_action",
        fake_run_analysis_action,
    )
    monkeypatch.setattr(
        "ma_ui.tkinter_app.module_views.analyse.pipeline_runner.should_log_command",
        lambda _command: False,
    )
    gui = object.__new__(tkinter_analyse_app.PipelineGUI)
    gui.pipeline_queue = queue.Queue()
    config = AnalysisConfig(
        steps=("prepare",),
        input_dir=tmp_path / "input",
        database_dir=tmp_path / "database",
        output_root=tmp_path / "output",
        rooms=["101 lobby"],
    )

    gui._run_pipeline_worker("prepare", config)

    messages = []
    while not gui.pipeline_queue.empty():
        messages.append(gui.pipeline_queue.get_nowait())

    assert captured["config"] is config
    assert messages[-1] == ("done", ("prepare", True))
    assert any(message_type == "log" and "service log" in payload for message_type, payload in messages)
    assert any(message_type == "log" and "Erzeugte Dateien:" in payload for message_type, payload in messages)


def test_tkinter_pipeline_worker_reports_service_errors(monkeypatch, tmp_path):
    def fake_run_analysis_action(config):
        return AnalysisResult(
            success=False,
            steps=config.steps,
            errors=["Backendfehler"],
        )

    monkeypatch.setattr(
        "ma_ui.tkinter_app.module_views.analyse.pipeline_runner.run_analysis_action",
        fake_run_analysis_action,
    )
    monkeypatch.setattr(
        "ma_ui.tkinter_app.module_views.analyse.pipeline_runner.should_log_command",
        lambda _command: False,
    )
    gui = object.__new__(tkinter_analyse_app.PipelineGUI)
    gui.pipeline_queue = queue.Queue()
    config = AnalysisConfig(
        steps=("heating",),
        input_dir=tmp_path / "input",
        database_dir=tmp_path / "database",
        output_root=tmp_path / "output",
        rooms=["101 lobby"],
    )

    gui._run_pipeline_worker("heating", config)

    messages = []
    while not gui.pipeline_queue.empty():
        messages.append(gui.pipeline_queue.get_nowait())

    assert messages[-1] == ("done", ("heating", False))
    assert any(message_type == "log" and "Backendfehler" in payload for message_type, payload in messages)


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
    assert rows[1]["Modul"] == "ma_export_simulation"
    assert rows[1]["Status"] == "planned"


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


def test_resource_status_rows_cover_module_information_views():
    assert resource_status_rows("parameters")
    assert resource_status_rows("building")
    assert resource_status_rows("simulation_setup")
    assert resource_status_rows("export_simulation")
    assert resource_status_rows("import_simulation")
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

    assert visible_analysis_steps(state) == ("command", "variants", "export", "run")


def test_analysis_wizard_hides_load_options_until_subcommand_is_selected():
    state = AnalysisWizardState(command="heating")

    assert visible_analysis_steps(state) == (
        "command",
        "subcommand",
        "template_diagram",
        "variants",
        "rooms",
        "export",
        "run",
    )

    timeline_state = AnalysisWizardState(command="heating", load_subcommand="timeline")

    assert visible_analysis_steps(timeline_state) == (
        "command",
        "subcommand",
        "template_diagram",
        "variants",
        "rooms",
        "export",
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
        "export",
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


def test_analysis_wizard_places_optional_overlay_after_template_selection():
    state = AnalysisWizardState(command=PLOT_TEMPLATE_STEP, plot_template="heating-overlay")

    assert visible_analysis_steps(state, template_supports_overlays=False) == (
        "command",
        "subcommand",
        "template_diagram",
        "variants",
        "rooms",
        "export",
        "run",
    )
    overlay_state = AnalysisWizardState(
        command=PLOT_TEMPLATE_STEP,
        plot_template="heating-overlay",
        overlay_enabled=True,
    )
    assert visible_analysis_steps(overlay_state, template_supports_overlays=True) == (
        "command",
        "subcommand",
        "template_diagram",
        "overlays",
        "variants",
        "rooms",
        "export",
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
        plot_template_mode="single",
        plot_template="heating-year",
        view="year",
    )

    assert analysis_step_complete(state, "subcommand") is True
    assert analysis_step_complete(state, "export") is True
    assert analysis_step_summary(state, "export") == "single"


def test_analysis_wizard_validates_manual_axis_ranges():
    invalid = AnalysisWizardState(
        command=PLOT_TEMPLATE_STEP,
        plot_template="heating-year",
        view="year",
        primary_axis_mode="manual",
        primary_ymin=1000,
        primary_ymax=100,
    )
    valid = AnalysisWizardState(
        command=PLOT_TEMPLATE_STEP,
        plot_template="heating-year",
        view="year",
        primary_axis_mode="manual",
        primary_ymin=0,
        primary_ymax=1000,
    )

    assert analysis_step_complete(invalid, "template_diagram") is False
    assert analysis_step_complete(valid, "template_diagram") is True


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

    assert command == ("python", "-m", "ma_ui.tkinter_app.module_views.analyse")


def test_tkinter_analyse_parser_builds_gui_args():
    args = parse_tkinter_analyse_args(
        [
            "--variants",
            "Variant_A,Variant_B",
            "--rooms",
            "101 lobby,208 office",
            "--output-root",
            "data/test_output/gui",
            "--heating-mode",
            "single",
            "--series-layout",
            "combined",
            "--export-format",
            "both",
            "--gui-window-maximized",
            "1",
        ]
    )

    assert args.command == "gui"
    assert args.variants == ["Variant_A", "Variant_B"]
    assert args.rooms == ["101 lobby", "208 office"]
    assert args.output_root == "data/test_output/gui"
    assert args.output_root_explicit is True
    assert args.variant_mode_explicit is True
    assert args.series_layout_explicit is True
    assert args.heating_mode == "single"
    assert args.heating_series_layout == "combined"
    assert args.export_format == "both"
    assert args.gui_window_maximized == 1


def test_tkinter_analyse_launcher_returns_process_id(monkeypatch, tmp_path):
    calls: dict[str, object] = {}

    class FakeProcess:
        pid = 1234

    def fake_popen(command, cwd=None):
        calls["command"] = command
        calls["cwd"] = cwd
        return FakeProcess()

    monkeypatch.setattr("ma_ui.tkinter_app.launcher.subprocess.Popen", fake_popen)

    result = launch_tkinter_analyse(python_executable="python", cwd=tmp_path)

    assert result.success is True
    assert result.process_id == 1234
    assert calls["command"] == ("python", "-m", "ma_ui.tkinter_app.module_views.analyse")
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


def test_analyse_view_builds_analysis_config_from_selection_lists():
    config = build_analysis_config(
        step="heating",
        input_dir="data/ma_analyse/ida_imports",
        database_dir="data/ma_analyse/database",
        output_root="data/ma_analyse/output",
        run_id=None,
        variants=["Variant_A", " Variant_B ", ""],
        rooms=["101 lobby", " 208 office "],
        debug=True,
        load_kind="heating",
    )

    assert config.run_id is None
    assert config.variants == ["Variant_A", "Variant_B"]
    assert config.rooms == ["101 lobby", "208 office"]
    assert config.load_kind == "heating"


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
    assert rows[0]["Rolle"] == "Nicht zugeordnet"
    assert rows[0]["Datensatztyp"] == "Jahr"
    assert rows[0]["Datensatzstatus"] == "Nicht geprueft"


def test_weather_dataset_default_table_keeps_source_rows_broad():
    dataset = WeatherDataset(
        weather_key="TRY_TEST",
        display_name="Test TRY",
        file_path=Path("data/ma_weather/input/missing.dat"),
        file_format="TRY",
        source="DWD",
        location="Frankfurt",
        year_type="reference_year",
        climate_scenario="present",
    )

    rows = weather_dataset_rows([dataset])
    default_table = weather_page._weather_dataset_default_table(rows)

    assert tuple(default_table.columns) == weather_page.WEATHER_DATASET_DEFAULT_COLUMNS
    assert rows[0]["weather_key"] == "TRY_TEST"
    assert "Format" in rows[0]
    assert "Rolle" in rows[0]
    assert "Datensatzstatus" in rows[0]
    assert "Datei" in rows[0]
    assert "Aktiviert" in rows[0]
    assert "Projekt-Default" in rows[0]
    assert "weather_key" not in default_table.columns


def test_active_weather_location_count_uses_unique_non_empty_locations():
    datasets = [
        WeatherDataset(
            weather_key="TRY_FFM_2015_JAHR",
            display_name="Frankfurt Jahr",
            file_path=Path("data/ma_weather/input/ffm_jahr.dat"),
            file_format="TRY",
            source="DWD",
            location="Frankfurt am Main",
            year_type="reference_year",
        ),
        WeatherDataset(
            weather_key="TRY_FFM_2015_SOMM",
            display_name="Frankfurt Sommer",
            file_path=Path("data/ma_weather/input/ffm_somm.dat"),
            file_format="TRY",
            source="DWD",
            location="Frankfurt am Main",
            year_type="summer_extreme",
        ),
        WeatherDataset(
            weather_key="TRY_MA_2015_JAHR",
            display_name="Mannheim Jahr",
            file_path=Path("data/ma_weather/input/ma_jahr.dat"),
            file_format="TRY",
            source="DWD",
            location=" Mannheim ",
            year_type="reference_year",
        ),
        WeatherDataset(
            weather_key="TRY_EMPTY",
            display_name="Ohne Ort",
            file_path=Path("data/ma_weather/input/empty.dat"),
            file_format="TRY",
            source="DWD",
            location="",
            year_type="reference_year",
        ),
    ]

    assert weather_page._active_weather_location_count(datasets) == 2


def test_weather_dataset_label_shows_dataset_type():
    summer_dataset = WeatherDataset(
        weather_key="TRY_TEST_SOMM",
        display_name="Test Sommer",
        file_path=Path("data/ma_weather/input/test_somm.dat"),
        file_format="TRY",
        source="DWD",
        location="Testort",
        year_type="summer_extreme",
    )
    winter_dataset = WeatherDataset(
        weather_key="TRY_TEST_WINT",
        display_name="Test Winter",
        file_path=Path("data/ma_weather/input/test_wint.dat"),
        file_format="TRY",
        source="DWD",
        location="Testort",
        year_type="winter_extreme",
    )

    assert weather_dataset_type_label(summer_dataset) == "Sommer"
    assert weather_dataset_type_label(winter_dataset) == "Winter"
    assert weather_dataset_label(summer_dataset) == "Test Sommer"
    assert weather_dataset_label(winter_dataset) == "Test Winter"


def test_weather_dataset_type_filter_keeps_only_selected_type():
    datasets = [
        WeatherDataset(
            weather_key="TRY_TEST_JAHR",
            display_name="Test Jahr",
            file_path=Path("data/ma_weather/input/test_jahr.dat"),
            file_format="TRY",
            source="DWD",
            location="Testort",
            year_type="reference_year",
        ),
        WeatherDataset(
            weather_key="TRY_TEST_SOMM",
            display_name="Test Sommer",
            file_path=Path("data/ma_weather/input/test_somm.dat"),
            file_format="TRY",
            source="DWD",
            location="Testort",
            year_type="summer_extreme",
        ),
        WeatherDataset(
            weather_key="TRY_TEST_WINT",
            display_name="Test Winter",
            file_path=Path("data/ma_weather/input/test_wint.dat"),
            file_format="TRY",
            source="DWD",
            location="Testort",
            year_type="winter_extreme",
        ),
    ]

    year_datasets = weather_page._datasets_for_weather_dataset_type(datasets, "Jahr")
    summer_datasets = weather_page._datasets_for_weather_dataset_type(datasets, "Sommer")
    winter_datasets = weather_page._datasets_for_weather_dataset_type(datasets, "Winter")

    assert [dataset.weather_key for dataset in year_datasets] == ["TRY_TEST_JAHR"]
    assert [dataset.weather_key for dataset in summer_datasets] == ["TRY_TEST_SOMM"]
    assert [dataset.weather_key for dataset in winter_datasets] == ["TRY_TEST_WINT"]


def test_weather_status_rows_show_open_dataset_context():
    status = WeatherDatasetStatus(
        weather_key="TRY_MISSING",
        display_name="Missing TRY",
        file_path=Path("data/ma_weather/input/missing.dat"),
        file_exists=False,
        file_status=WeatherFileStatus.MISSING,
        import_status=WeatherImportCheckStatus.NOT_CHECKED,
        error_count=1,
        messages=("Lokale TRY-Datei fehlt.",),
    )

    rows = weather_status_rows([status])

    assert rows[0]["weather_key"] == "TRY_MISSING"
    assert rows[0]["Typ"] == "Katalogdatensatz"
    assert rows[0]["Status"] == "Datei fehlt"
    assert rows[0]["Fehler"] == 1
    assert rows[0]["Hinweise"] == "Lokale TRY-Datei fehlt."


def test_weather_open_discovery_rows_mark_scan_drafts():
    discovery = WeatherFileDiscovery(
        weather_key="",
        display_name="",
        file_path=Path("data/ma_weather/input/TRY_000000000000/TRY2015_000000000000_Jahr.dat"),
        try_folder_key="TRY_000000000000",
        try_id="000000000000",
        year=2015,
        dataset_type="Jahr",
        year_type="reference_year",
        climate_scenario="present",
        dataset_role="",
        location_id="",
        reference_location_id="",
        location_name="",
        selection_priority=10,
        metadata={"rechtswert_m": "494997", "hochwert_m": "084777"},
        missing_fields=("location_id", "weather_key", "display_name", "dataset_role"),
        messages=("Keine Standortzuordnung vorhanden.",),
        status=WeatherDiscoveryStatus.OPEN,
    )

    rows = weather_page.weather_open_discovery_rows([discovery])

    assert rows[0]["Typ"] == "Scan-Entwurf"
    assert rows[0]["Status"] == "offen"
    assert rows[0]["Datei"] == "data/ma_weather/input/TRY_000000000000/TRY2015_000000000000_Jahr.dat"
    assert rows[0]["Offene Punkte"] == "Stadt"
    assert rows[0]["Fehler"] == 4


def test_weather_discovery_file_value_rows_show_read_file_context():
    discovery = WeatherFileDiscovery(
        weather_key="TRY_TEST_2015_JAHR",
        display_name="Test",
        file_path=Path("data/ma_weather/input/TRY_000000000000/TRY2015_000000000000_Jahr.dat"),
        try_folder_key="TRY_000000000000",
        try_id="000000000000",
        year=2015,
        dataset_type="Jahr",
        year_type="reference_year",
        climate_scenario="present",
        dataset_role="try_reference",
        location_id="LOC_TEST",
        reference_location_id="LOC_TEST",
        location_name="Testort",
        selection_priority=10,
        metadata={
            "rechtswert_m": "494997",
            "hochwert_m": "084777",
            "hoehenlage_m": "99",
            "try_type": "mittleres Jahr",
            "reference_period": "2015",
        },
    )

    rows = weather_page.weather_discovery_file_value_rows(discovery)
    values = {row["Feld"]: row["Gelesener Wert"] for row in rows}

    assert values["Dateiname"] == "TRY2015_000000000000_Jahr.dat"
    assert values["TRY-Ordner"] == "TRY_000000000000"
    assert values["Bezugsjahr"] == 2015
    assert values["Rechtswert"] == "494997"
    assert values["Hoehenlage"] == "99"


def test_weather_discovery_overview_hides_unconfirmed_coordinate_suggestions():
    suggested_discovery = WeatherFileDiscovery(
        weather_key="",
        display_name="",
        file_path=Path("data/ma_weather/input/TRY_524031130658/TRY2015_524031130658_Jahr.dat"),
        try_folder_key="TRY_524031130658",
        try_id="524031130658",
        year=2015,
        dataset_type="Jahr",
        year_type="reference_year",
        climate_scenario="present",
        dataset_role="",
        location_id="",
        reference_location_id="",
        location_name="",
        selection_priority=10,
        metadata={
            "suggested_location_name": "Hamburg",
            "suggested_location_id": "LOC_001",
            "location_resolution_source": "try_coordinates",
            "location_resolution_status": "suggested",
        },
        missing_fields=("location_id",),
        status=WeatherDiscoveryStatus.OPEN,
    )
    confirmed_discovery = WeatherFileDiscovery(
        weather_key="TRY_MA_2015_JAHR",
        display_name="TRY Mannheim 2015 Jahr",
        file_path=Path("data/ma_weather/input/TRY_494997084777/TRY2015_494997084777_Jahr.dat"),
        try_folder_key="TRY_494997084777",
        try_id="494997084777",
        year=2015,
        dataset_type="Jahr",
        year_type="reference_year",
        climate_scenario="present",
        dataset_role="try_reference",
        location_id="LOC_053",
        reference_location_id="LOC_053",
        location_name="Mannheim",
        selection_priority=10,
        metadata={
            "location_resolution_source": "file_reference",
            "location_resolution_status": "confirmed",
        },
    )

    rows = weather_page._weather_discovery_overview_rows([suggested_discovery, confirmed_discovery])

    assert rows[0]["Ort / Vorschlag"] == "offen"
    assert rows[0]["Offene Punkte"] == "Stadt"
    assert rows[1]["Ort / Vorschlag"] == "Mannheim"


def test_weather_discovery_key_parameter_rows_keep_editable_targets_together():
    discovery = WeatherFileDiscovery(
        weather_key="TRY_TEST_2015_JAHR",
        display_name="Test",
        file_path=Path("data/ma_weather/input/TRY_000000000000/TRY2015_000000000000_Jahr.dat"),
        try_folder_key="TRY_000000000000",
        try_id="000000000000",
        year=2015,
        dataset_type="Jahr",
        year_type="reference_year",
        climate_scenario="present",
        dataset_role="try_reference",
        location_id="LOC_TEST",
        reference_location_id="LOC_TEST",
        location_name="Testort",
        selection_priority=10,
        metadata={"rechtswert_m": "494997", "hochwert_m": "084777"},
    )
    locations = {
        "LOC_TEST": WeatherLocation(
            location_id="LOC_TEST",
            location_name="Testort",
            normalized_name="testort",
            region_id="TRY_TEST",
            reference_location_id="LOC_TEST",
            is_reference_location=True,
        )
    }

    rows = weather_page.weather_discovery_key_parameter_rows(discovery, locations)
    rows_by_field = {str(row["Feld"]): row for row in rows}

    assert list(rows_by_field["Stadt"]) == ["Feld", "Wert"]
    assert "Dateiname" not in rows_by_field
    assert rows_by_field["Stadt"]["Wert"] == "LOC_TEST - Testort"
    assert rows_by_field["Bezugsjahr"]["Wert"] == 2015
    assert rows_by_field["Datensatztyp"]["Wert"] == "Jahr"
    assert rows_by_field["Szenario"]["Wert"] == "Gegenwart"
    assert "Rolle" not in rows_by_field
    assert "weather_key" not in rows_by_field
    assert "Anzeigename" not in rows_by_field


def test_weather_validation_mask_uses_no_artificial_defaults():
    weather_source = Path("src/ma_ui/streamlit_app/pages/weather.py").read_text(encoding="utf-8")
    validation_source = weather_source.split("def _render_weather_validation_panel", maxsplit=1)[1].split(
        "def _render_weather_discovery_validation_result",
        maxsplit=1,
    )[0]
    parameter_view_source = validation_source.split("discoveries_by_path", maxsplit=1)[1]

    assert '"Gefundene lokale TRY-Dateien"' in weather_source
    assert "WEATHER_VALIDATION_VIEW_KEYS" in weather_source
    assert '"Parameter pruefen"' in weather_source
    assert '"Key-Parameter pruefen"' not in weather_source
    assert "st.data_editor" in validation_source
    assert "weather_discovery_key_parameter_rows" in validation_source
    assert "_render_weather_discoveries()" not in parameter_view_source
    assert '"Aenderungen uebernehmen"' in validation_source
    assert '"Entwurf pruefen"' in validation_source
    assert '"Geprueften Entwurf registrieren"' in validation_source
    assert "_updated_discovery_from_key_parameter_rows" in validation_source
    assert "validate_weather_file_discovery(" in validation_source
    assert "selected_discovery.year or 2015" not in validation_source
    assert "st.number_input(" not in validation_source
    assert "_run_weather_catalog_validation(catalog)" not in validation_source


def test_weather_event_rows_are_stable_for_ui():
    event = WeatherEvent(
        event_id="TRY_TEST_hottest_day_2045070100_2045070123",
        event_type="hottest_day",
        weather_key="TRY_TEST",
        start_time=pd.Timestamp("2045-07-01 00:00").to_pydatetime(),
        end_time=pd.Timestamp("2045-07-01 23:00").to_pydatetime(),
        value=31.234,
        unit="Grad C",
        reason="Testereignis",
    )

    rows = weather_event_rows([event])

    assert rows == [
        {
            "Ereignis-ID": "TRY_TEST_hottest_day_2045070100_2045070123",
            "Typ": "hottest_day",
            "weather_key": "TRY_TEST",
            "Start": "2045-07-01T00:00:00",
            "Ende": "2045-07-01T23:00:00",
            "Kennwert": 31.23,
            "Einheit": "Grad C",
            "Begruendung": "Testereignis",
        }
    ]


def test_weather_location_rows_show_reference_context():
    catalog = import_weather_location_catalog()

    rows = weather_location_rows(catalog)
    frankfurt_row = next(row for row in rows if row["Standort-ID"] == "LOC_049")

    assert frankfurt_row["Stadt"] == "Frankfurt (Main)"
    assert frankfurt_row["Klimaregion"] == "TRY12"
    assert frankfurt_row["TRY-Referenzstandort"] == "Mannheim"


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
        weather_key="TRY_FFM_2045_JAHR",
        display_name="TRY Frankfurt 2045 Jahr",
        file_path=Path("data/ma_weather/input/TRY_501262086894/TRY2045_501262086894_Jahr.dat"),
        file_format="TRY",
        source="DWD",
        location="Frankfurt",
        year_type="future_year",
    )

    assert weather_start_year(dataset) == 2045


def test_weather_session_id_is_stable_for_current_ui_session():
    session_state: dict[str, object] = {}

    first = get_weather_session_id(session_state)
    second = get_weather_session_id(session_state)

    assert first == second
    assert first.startswith("session_")


def test_economic_assumption_rows_use_existing_importer():
    assumptions, errors = import_economic_assumptions("config/ma_variants/economic/example_economic_assumptions.yaml")

    rows = economic_assumption_rows(assumptions)

    assert errors == []
    assert len(rows["system_costs"]) == 4
    assert len(rows["energy_prices"]) == 2
    assert rows["scenarios"][0]["scenario_key"] == "example_20y"
