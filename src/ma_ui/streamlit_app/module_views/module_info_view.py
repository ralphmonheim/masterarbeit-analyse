"""Technische Modulinfo ohne fachliche Ablaufhilfe oder Plan-Duplikate."""

from __future__ import annotations

import streamlit as st

from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_workflow import ModuleDefinition, get_module_definition

STATUS_LABELS = {
    "available": "Verfuegbar",
    "partial": "Teilweise umgesetzt",
    "planned": "Geplant",
    "manual": "Manuell / extern",
}

TECHNICAL_STATUS_MESSAGES = {
    "available": "Der technische V1-Umfang ist im Projektbestand verfügbar.",
    "partial": "Der technische V1-Umfang ist teilweise umgesetzt; Test- und Vertragsgrenzen bleiben sichtbar.",
    "planned": "Der technische V1-Umfang ist geplant und nicht als ausführbare Funktion zu verstehen.",
    "manual": "Der Schritt liegt außerhalb des Python-Projekts und bleibt manuell oder extern.",
}

ACTIVE_PLAN_BY_MODULE_KEY = {
    "ma_weather": "P008",
    "ma_project": "P011",
    "ma_building": "P012",
    "ma_zones": "P013",
    "ma_technical": "P014",
    "ma_parameters": "P015",
    "ma_parameters.variation_specification": "P015",
    "ma_analyse.stage_1_dimensioning": "P016",
    "ma_variants": "P017",
    "ma_simulation_setup": "P018",
    "ma_analyse.stage_2_optimization": "P019",
    "ma_analyse.stage_3_standards_verification": "P020",
    "ma_analyse.stage_4_sensitivity": "P021",
    "ma_economy": "P022",
    "ma_sustainability": "P023",
    "ma_assessment": "P024",
    "ma_reporting": "P025",
    "ma_data_export": "P026",
    "ma_validation": "P027",
    "ma_feedback": "P027",
    "ma_ui": "P037",
    "ma_workflow": "P037",
    "ma_export_simulation": "P009",
    "ma_import_simulation": "P009",
    "ma_data_preparation": "P036",
    "ma_analyse": "P029",
    "project_documentation": "P037",
    "ma_core": "P010",
    "ma_database": "P010",
    "ida_ice": "P009",
}

TEST_REFERENCE_BY_MODULE_KEY = {
    "ma_ui": "UI- und Navigationstests unter tests/test_ma_ui_shell.py.",
    "ma_workflow": "Workflow- und Katalogtests unter tests/.",
    "project_documentation": "Dokument-, Link- und Governanceprüfungen.",
}


def _render_text_list(title: str, values: tuple[str, ...]) -> None:
    if not values:
        return
    st.subheader(title)
    for value in values:
        st.markdown(f"- {value}")


def render_module_definition(module: ModuleDefinition) -> None:
    """Zeigt technische Metadaten, Schnittstellen und aktive Planreferenzen."""
    render_page_header(f"Technische Modulinfo: {module.label}", module.purpose)
    status_label = STATUS_LABELS.get(module.status, module.status)
    metric_columns = st.columns(3)
    metric_columns[0].metric("Status", status_label)
    metric_columns[1].metric("Bereich", module.category)
    metric_columns[2].metric("Python-Paket", module.python_package or "kein Paket")

    st.subheader("Implementierungsstand")
    st.info(TECHNICAL_STATUS_MESSAGES.get(module.status, "Der technische Status steht im zentralen Modulkatalog."))
    st.markdown(f"**Aktiver Plan:** {ACTIVE_PLAN_BY_MODULE_KEY.get(module.module_key, 'kein aktiver Plan hinterlegt')}")
    st.markdown(f"**Technische Restarbeit:** {module.next_step}")
    st.markdown(
        "**Testbezug:** "
        + TEST_REFERENCE_BY_MODULE_KEY.get(
            module.module_key,
            "Modultests und relevante Integrationsprüfungen liegen unter tests/.",
        )
    )

    if module.inputs or module.outputs:
        input_column, output_column = st.columns(2)
        with input_column:
            _render_text_list("Technische Eingaben", module.inputs)
        with output_column:
            _render_text_list("Technische Ausgaben", module.outputs)
    _render_text_list("Schnittstellengrenzen", module.boundaries)
    _render_text_list("Abhaengigkeiten", module.dependencies)


def render(module_key: str) -> None:
    """Laedt und zeigt eine Moduldefinition aus dem zentralen Katalog."""
    render_module_definition(get_module_definition(module_key))
