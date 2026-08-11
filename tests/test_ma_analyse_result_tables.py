from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from ma_analyse import services
from ma_analyse.analysis.excel import build_analysis_table_bundle, build_excel_report
from ma_analyse.analysis.tables.excel_report import prepare_result_dataframe, summarize_room_metrics
from ma_analyse.analysis.tables.schema import LEGACY_OUTPUT_COLUMNS
from ma_analyse.analysis_wizard import AnalysisWizardState, section_complete, section_summary
from ma_analyse.models import AnalysisConfig
from ma_analyse.stage_3_standards_verification import build_verification_readiness_items
from ma_ui.streamlit_app.module_views import analyse_view as analyse_view_module
from ma_ui.streamlit_app.module_views.analyse_view import (
    DATABASE_DIR_WIDGET_KEY,
    POWER_DISPLAY_WIDGET_KEY,
    _command_produces_analysis_tables,
    _power_area_required,
    _power_source_context_id,
    _room_area_widget_key,
    _unique_room_area_mapping,
    selected_reference_areas_m2,
)


def _room_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "time": [0, 1, 2],
            "zone_energy_q_heat": [100.0, 200.0, 50.0],
            "zone_energy_q_cool": [-20.0, -40.0, 0.0],
            "temperatures_top": [21.0, 22.0, 23.0],
        }
    )


def _write_room_database(database_dir: Path) -> None:
    variant_dir = database_dir / "Variant_A_nutzdaten"
    variant_dir.mkdir(parents=True)
    _room_frame().to_csv(variant_dir / "101_lobby.csv", index=False)


def test_room_summary_keeps_w_and_derives_w_per_m2_from_reference_area():
    row = summarize_room_metrics(
        _room_frame(),
        "Variant A",
        "101 lobby",
        reference_area_m2=20.0,
        power_display_mode="both",
        power_source_unit="w",
    )

    assert row["max_q_heat"] == 200.0
    assert row["max_q_heat_per_m2"] == 10.0
    assert row["evaluation_hours"] == 3
    assert row["specific_power_status"] == "teilweise auswertbar"


def test_specific_values_remain_not_evaluable_without_area():
    row = summarize_room_metrics(_room_frame(), "Variant A", "101 lobby", power_source_unit="w")
    table = prepare_result_dataframe([row], "both")

    assert row["max_q_heat_per_m2"] is None
    assert row["specific_power_status"] == "nicht auswertbar: Bezugsfläche fehlt"
    assert "Max. Heizleistung [W]" in table.columns
    assert "Max. Heizleistung [W/m²]" in table.columns


def test_power_display_mode_controls_visible_columns():
    row = summarize_room_metrics(
        _room_frame(),
        "Variant A",
        "101 lobby",
        reference_area_m2=20.0,
        power_source_unit="w",
    )

    absolute = prepare_result_dataframe([row], "absolute")
    specific = prepare_result_dataframe([row], "specific")

    assert "Max. Heizleistung [W]" in absolute.columns
    assert "Max. Heizleistung [W/m²]" not in absolute.columns
    assert "Max. Heizleistung [W]" not in specific.columns
    assert "Max. Heizleistung [W/m²]" in specific.columns


def test_bundle_separates_evaluation_hours_usage_hours_and_norm_readiness(tmp_path):
    database_dir = tmp_path / "database"
    _write_room_database(database_dir)

    bundle = build_analysis_table_bundle(
        database_dir,
        selected_variants=["Variant_A"],
        rooms=["101 lobby"],
        reference_areas_m2={"101 lobby": 20.0},
        power_source_unit="w",
    )

    assert bundle.summary.loc[0, "Auswertungsstunden [h]"] == 3
    usage_row = bundle.calculation_boundaries.loc[bundle.calculation_boundaries["Prüfpunkt"] == "Nutzungsstunden"].iloc[
        0
    ]
    assert usage_row["Status"] == "nicht auswertbar"
    assert set(bundle.verification_readiness["Stage-3-Status"]) == {"NOT_EVALUABLE"}


def test_excel_report_contains_shared_tables_and_no_fake_din_metric(tmp_path):
    database_dir = tmp_path / "database"
    output_root = tmp_path / "output"
    _write_room_database(database_dir)

    output_file = build_excel_report(
        database_dir,
        output_root=output_root,
        run_id="RUN-001",
        selected_variants=["Variant_A"],
        rooms=["101 lobby"],
        variant_mode="compare",
        reference_areas_m2={"101 lobby": 20.0},
        power_source_unit="w",
    )

    workbook = pd.ExcelFile(output_file)
    assert workbook.sheet_names == [
        "metrics",
        "metrics_v2",
        "data_inventory",
        "calculation_limits",
        "verification_readiness",
    ]
    legacy_metrics = pd.read_excel(output_file, sheet_name="metrics")
    metrics = pd.read_excel(output_file, sheet_name="metrics_v2")
    assert legacy_metrics.columns.tolist() == LEGACY_OUTPUT_COLUMNS
    assert pd.isna(legacy_metrics.loc[0, "In use, h"])
    assert pd.isna(legacy_metrics.loc[0, "DIN 4108-2 over-temperature degree hours, h Deg-C"])
    assert "Max. Heizleistung [W]" in metrics.columns
    assert "Max. Heizleistung [W/m²]" in metrics.columns
    assert not any("DIN 4108" in column for column in metrics.columns)


def test_run_analysis_populates_tables_for_analyze_step(tmp_path, monkeypatch):
    database_dir = tmp_path / "database"
    _write_room_database(database_dir)
    monkeypatch.setattr(
        services,
        "_execute_legacy_analysis",
        lambda *_args, **_kwargs: services.LegacyExecutionResult(success=True, errors=[], log_text="ok"),
    )

    result = services.run_analysis(
        AnalysisConfig(
            steps=("analyze",),
            database_dir=database_dir,
            output_root=tmp_path / "output",
            variants=["Variant_A"],
            rooms=["101 lobby"],
            reference_areas_m2={"101 lobby": 20.0},
            power_source_unit="w",
        )
    )

    assert result.success is True
    assert result.summary_table.loc[0, "Max. Heizleistung [W/m²]"] == 10.0
    assert set(result.detail_tables) == {"Dateninventar", "Berechnungsgrenzen", "Nachweisbereitschaft"}


def test_stage3_readiness_has_no_activated_rule_or_pass_result():
    items = build_verification_readiness_items()

    assert {item.stage3_status for item in items} == {"NOT_EVALUABLE"}
    assert all("pass" not in item.stage3_status.casefold() for item in items)
    assert all(
        "rule_not_defined" in item.method_status or "values_not_released" in item.method_status for item in items
    )
    assert all(item.rights_status == "norm_content_not_released" for item in items)
    assert all(item.content_access_status == "machine_content_access_blocked" for item in items)


def test_selected_reference_areas_uses_positive_manual_values():
    state = {
        POWER_DISPLAY_WIDGET_KEY: "Beides",
        _room_area_widget_key("101 lobby"): 65.4,
        _room_area_widget_key("109 office"): 0.0,
    }

    assert selected_reference_areas_m2(("101 lobby", "109 office"), state) == {"101 lobby": 65.4}


def test_unverified_power_unit_keeps_raw_value_but_not_w_claim():
    row = summarize_room_metrics(_room_frame(), "Variant A", "101 lobby", reference_area_m2=20.0)
    table = prepare_result_dataframe([row], "both")

    assert row["raw_max_q_heat"] == 200.0
    assert row["max_q_heat"] is None
    assert row["max_q_heat_per_m2"] is None
    assert row["specific_power_status"] == "nicht auswertbar: Quelleneinheit nicht bestätigt"
    assert table.loc[0, "Einheitenstatus"] == "nicht bestätigt"


def test_w_per_m2_source_derives_absolute_value_with_area():
    row = summarize_room_metrics(
        _room_frame(),
        "Variant A",
        "101 lobby",
        reference_area_m2=20.0,
        power_source_unit="w_per_m2",
    )

    assert row["max_q_heat_per_m2"] == 200.0
    assert row["max_q_heat"] == 4000.0


@pytest.mark.parametrize(
    ("values", "algebraic_max", "algebraic_min", "absolute_peak"),
    [
        ([-20.0, -40.0, 0.0], 0.0, -40.0, 40.0),
        ([20.0, 40.0, 0.0], 40.0, 0.0, 40.0),
        ([-20.0, 40.0, 0.0], 40.0, -20.0, 40.0),
        ([float("nan"), float("nan")], None, None, None),
    ],
)
def test_cooling_metrics_separate_raw_extrema_and_absolute_peak(
    values,
    algebraic_max,
    algebraic_min,
    absolute_peak,
):
    frame = pd.DataFrame({"time": range(len(values)), "zone_energy_q_cool": values})
    row = summarize_room_metrics(frame, "Variant A", "101 lobby", power_source_unit="w")

    assert row["max_q_cool"] == algebraic_max
    assert row["min_q_cool"] == algebraic_min
    assert row["peak_abs_q_cool"] == absolute_peak


def test_specific_mode_keeps_absolute_fallback_when_area_is_missing():
    row = summarize_room_metrics(_room_frame(), "Variant A", "101 lobby", power_source_unit="w")
    table = prepare_result_dataframe([row], "specific")

    assert "Max. Heizleistung [W]" in table.columns
    assert table.loc[0, "Max. Heizleistung [W]"] == 200.0


def test_room_area_widget_key_is_bound_to_building_context():
    assert _room_area_widget_key("101 lobby", "PRJ-1:BLD-V1") != _room_area_widget_key("101 lobby", "PRJ-2:BLD-V1")


def test_duplicate_room_names_are_not_automatically_mapped():
    spaces = (
        SimpleNamespace(space_id="SPACE-1", name="office", floor_area_m2=20.0),
        SimpleNamespace(space_id="SPACE-2", name="office", floor_area_m2=30.0),
    )
    areas = _unique_room_area_mapping(spaces)

    assert "office" not in areas
    assert areas["SPACE-1"] == 20.0
    assert areas["SPACE-2"] == 30.0


@pytest.mark.parametrize(
    ("display_mode", "source_unit", "expected"),
    [
        ("absolute", "w", False),
        ("absolute", "w_per_m2", True),
        ("specific", "w", True),
        ("specific", "w_per_m2", False),
        ("both", "w", True),
        ("both", "w_per_m2", True),
        ("both", "unverified", False),
    ],
)
def test_area_input_is_requested_only_for_required_conversion(display_mode, source_unit, expected):
    assert _power_area_required(display_mode, source_unit) is expected


def test_power_options_are_visible_for_analyze_and_all_only():
    assert _command_produces_analysis_tables("analyze_data") is True
    assert _command_produces_analysis_tables("all") is True
    assert _command_produces_analysis_tables("heating") is False


def test_all_export_section_renders_power_options(monkeypatch):
    calls = []
    monkeypatch.setattr(analyse_view_module, "_render_power_output_options", lambda state: calls.append(state.command))
    monkeypatch.setattr(analyse_view_module, "_render_advanced_paths", lambda: ("", "", "", ""))
    monkeypatch.setattr(analyse_view_module.st, "selectbox", lambda *_args, **_kwargs: "combined")
    monkeypatch.setattr(analyse_view_module.st, "caption", lambda *_args, **_kwargs: None)

    analyse_view_module._render_export_section(SimpleNamespace(command="all"))

    assert calls == ["all"]


def test_all_wizard_requires_and_summarizes_excel_layout():
    incomplete = AnalysisWizardState(command="all")
    complete = AnalysisWizardState(command="all", series_layout="combined")

    assert section_complete(incomplete, "export") is False
    assert section_summary(incomplete, "export") == "nicht gewählt"
    assert section_complete(complete, "export") is True
    assert section_summary(complete, "export") == "Excel combined"


def test_power_unit_context_changes_with_database_or_variant():
    state_a = SimpleNamespace(selected_variants=("Variant_A",))
    state_b = SimpleNamespace(selected_variants=("Variant_B",))
    session = {DATABASE_DIR_WIDGET_KEY: "database-a"}

    first = _power_source_context_id(state_a, session)
    session[DATABASE_DIR_WIDGET_KEY] = "database-b"

    assert _power_source_context_id(state_a, session) != first
    assert _power_source_context_id(state_b, {DATABASE_DIR_WIDGET_KEY: "database-a"}) != first


def test_run_analysis_populates_tables_for_all_step(tmp_path, monkeypatch):
    database_dir = tmp_path / "database"
    _write_room_database(database_dir)
    monkeypatch.setattr(
        services,
        "_execute_legacy_analysis",
        lambda *_args, **_kwargs: services.LegacyExecutionResult(success=True, errors=[], log_text="ok"),
    )

    result = services.run_analysis(
        AnalysisConfig(
            steps=("all",),
            database_dir=database_dir,
            output_root=tmp_path / "output",
            variants=["Variant_A"],
            rooms=["101 lobby"],
            reference_areas_m2={"101 lobby": 20.0},
            power_source_unit="w",
        )
    )

    assert result.summary_table is not None
    assert result.detail_tables
