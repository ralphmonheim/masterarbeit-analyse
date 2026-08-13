"""Regressionstests für P037-Dokumentations- und Informationsverträge."""

from __future__ import annotations

from ma_ui.streamlit_app.navigation import (
    CURRENT_PAGE_SESSION_KEY,
    MODULE_INFO_PAGE_SESSION_KEY,
    WORKFLOW_HELP_PAGE_SESSION_KEY,
    select_page,
    set_module_info_active,
    set_workflow_help_active,
)
from ma_ui.streamlit_app.pages.home import PROCESS_AREA_ORDER, module_overview_rows
from ma_ui.streamlit_app.workflow_graph import workflow_card_rows
from ma_workflow import (
    list_module_definitions,
    load_workflow_module_guide,
    missing_workflow_module_guides,
    workflow_module_summary,
)


def test_every_catalog_module_has_a_complete_workflow_guide():
    assert missing_workflow_module_guides() == ()

    for module in list_module_definitions():
        guide = load_workflow_module_guide(module.module_key)
        assert f"Modul-ID: `{module.module_key}`" in guide.markdown
        assert "## Rolle im Ablauf" in guide.markdown
        assert "## Fachliche Eingänge" in guide.markdown
        assert "## Ausgänge und Übergaben" in guide.markdown
        assert "## Bedien- und Ablaufhinweis" in guide.markdown
        assert "Aktiver Plan" not in guide.markdown


def test_workflow_card_summary_is_read_from_the_module_guide():
    card = next(card for card in workflow_card_rows() if card.module_key == "ma_building")

    assert card.description == workflow_module_summary("ma_building")
    assert "Bauteile" in card.description


def test_workspace_module_overview_uses_the_four_process_areas():
    rows = module_overview_rows()

    assert set(row["Prozessbereich"] for row in rows) == set(PROCESS_AREA_ORDER)
    assert any(row["Modul-Key"] == "ma_project" and row["Prozessbereich"] == "PreProcess" for row in rows)
    assert any(row["Modul-Key"] == "ida_ice" and row["Prozessbereich"] == "Kernprozess" for row in rows)
    assert any(row["Modul-Key"] == "ma_data_preparation" and row["Prozessbereich"] == "PostProcess" for row in rows)
    assert any(row["Modul-Key"] == "ma_validation" and row["Prozessbereich"] == "Querschnittsmodule" for row in rows)


def test_technical_info_and_workflow_help_are_exclusive_and_cleared_on_navigation():
    session_state: dict[str, object] = {}

    set_module_info_active(session_state, "weather", active=True)
    assert session_state[MODULE_INFO_PAGE_SESSION_KEY] == "weather"

    set_workflow_help_active(session_state, "weather", active=True)
    assert session_state[WORKFLOW_HELP_PAGE_SESSION_KEY] == "weather"
    assert MODULE_INFO_PAGE_SESSION_KEY not in session_state

    select_page(session_state, "building")
    assert session_state[CURRENT_PAGE_SESSION_KEY] == "building"
    assert MODULE_INFO_PAGE_SESSION_KEY not in session_state
    assert WORKFLOW_HELP_PAGE_SESSION_KEY not in session_state
