import argparse

import pytest

from ma_analyse.app.commands import (
    PipelinePreconditionResult,
    PipelineRuntimeArgs,
    build_runtime_args,
    check_required_data,
    ensure_required_data,
)
from ma_analyse.core.config import ROOMS


def _base_args(**overrides):
    values = {
        "input_dir": "input",
        "datenbank_dir": "database",
        "output_root": "output",
        "output_root_explicit": True,
        "run_id": "run-1",
        "debug": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def test_build_runtime_args_returns_pipeline_runtime_args():
    runtime_args = build_runtime_args(
        _base_args(),
        variants=["Variant_A"],
        rooms=["208 office"],
    )

    assert isinstance(runtime_args, PipelineRuntimeArgs)
    assert not isinstance(runtime_args, argparse.Namespace)
    assert runtime_args.input_dir == "input"
    assert runtime_args.datenbank_dir == "database"
    assert runtime_args.output_root == "output"
    assert runtime_args.output_root_explicit is True
    assert runtime_args.run_id == "run-1"
    assert runtime_args.variants == ["Variant_A"]
    assert runtime_args.rooms == ["208 office"]


def test_build_runtime_args_keeps_default_profiles():
    runtime_args = build_runtime_args(_base_args())

    assert runtime_args.export_format == "csv"
    assert runtime_args.view == "bar"
    assert runtime_args.month is None
    assert runtime_args.week is None
    assert runtime_args.day is None
    assert runtime_args.heating_series_layout == "separate"
    assert runtime_args.heating_mode == "compare"
    assert runtime_args.rooms == ROOMS
    assert runtime_args.rooms is not ROOMS
    assert runtime_args.plot_single is True
    assert runtime_args.plot_overview is True
    assert runtime_args.analysis_individual is True
    assert runtime_args.analysis_overview is True


def test_build_runtime_args_applies_prepare_heating_comfort_and_plot_options():
    runtime_args = build_runtime_args(
        _base_args(
            view="year",
            month="Jan",
            week=3,
            day=2,
            heating_series_layout="combined",
            heating_mode="single",
            export_format="excel",
            template="heating-year",
            plot_template_mode="single",
            setpoint_min=21.0,
        ),
        heating_mode=None,
        prepare_options={"export_format": "both"},
        comfort_options={
            "plot_single": False,
            "plot_overview": True,
            "analysis_individual": False,
            "analysis_overview": True,
        },
        heating_options={
            "view": "week",
            "month": None,
            "week": 12,
            "day": None,
            "series_layout": "separate",
        },
        plot_template_options={
            "template": "heating-overlay",
            "output_mode": "compare",
            "setpoint_min": 19.0,
            "fixed_overlays": [],
            "month": "Feb",
            "week": None,
            "day": 14,
        },
    )

    assert runtime_args.export_format == "both"
    assert runtime_args.view == "week"
    assert runtime_args.month == "Feb"
    assert runtime_args.week is None
    assert runtime_args.day == 14
    assert runtime_args.heating_series_layout == "separate"
    assert runtime_args.heating_mode == "single"
    assert runtime_args.plot_single is False
    assert runtime_args.plot_overview is True
    assert runtime_args.analysis_individual is False
    assert runtime_args.analysis_overview is True
    assert runtime_args.template == "heating-overlay"
    assert runtime_args.plot_template_mode == "compare"
    assert runtime_args.setpoint_min == 19.0
    assert runtime_args.fixed_overlays == []


def test_pipeline_runtime_args_remains_mutable_for_run_all_compatibility():
    runtime_args = build_runtime_args(_base_args())

    runtime_args.run_id = "shared-run"

    assert runtime_args.run_id == "shared-run"


def test_check_required_data_allows_steps_without_database_requirement(tmp_path):
    missing_database = tmp_path / "missing_database"

    result = check_required_data(_base_args(datenbank_dir=missing_database), ["prepare"])

    assert result == PipelinePreconditionResult(ok=True, messages=[])


def test_check_required_data_allows_prepare_combined_with_database_step(tmp_path):
    missing_database = tmp_path / "missing_database"

    result = check_required_data(_base_args(datenbank_dir=missing_database), ["prepare", "analysis"])

    assert result == PipelinePreconditionResult(ok=True, messages=[])


def test_check_required_data_allows_existing_database(tmp_path):
    database_dir = tmp_path / "database"
    database_dir.mkdir()

    result = check_required_data(_base_args(datenbank_dir=database_dir), ["analysis"])

    assert result == PipelinePreconditionResult(ok=True, messages=[])


def test_check_required_data_reports_missing_database(tmp_path):
    missing_database = tmp_path / "missing_database"

    result = check_required_data(_base_args(datenbank_dir=missing_database), ["analysis"])

    assert result == PipelinePreconditionResult(
        ok=False,
        messages=[
            f"X Verzeichnis mit aufbereiteten Daten nicht gefunden: {missing_database}",
            "  Fuehren Sie zuerst 'prepare' aus oder waehlen Sie in der GUI auch prepare.",
        ],
    )


def test_ensure_required_data_keeps_legacy_system_exit(tmp_path, capsys):
    missing_database = tmp_path / "missing_database"

    with pytest.raises(SystemExit) as exc_info:
        ensure_required_data(_base_args(datenbank_dir=missing_database), ["analysis"])

    assert exc_info.value.code == 1
    output = capsys.readouterr().out
    assert f"X Verzeichnis mit aufbereiteten Daten nicht gefunden: {missing_database}" in output
    assert "Fuehren Sie zuerst 'prepare' aus" in output
