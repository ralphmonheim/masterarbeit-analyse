from ma_analyse import services
from ma_analyse.models import AnalysisConfig, AnalysisResult, AnalysisStepResult
from ma_analyse.services import (
    get_plot_template_ui_defaults,
    get_plot_template_ui_spec,
    list_analysis_rooms,
    list_analysis_variants,
    list_plot_overlay_sources,
    run_analysis,
)


def _missing_database_errors(database_dir):
    return [
        f"X Verzeichnis mit aufbereiteten Daten nicht gefunden: {database_dir}",
        "  Fuehren Sie zuerst 'prepare' aus oder waehlen Sie in der GUI auch prepare.",
    ]


def test_analysis_config_normalizes_paths_and_sequences(tmp_path):
    config = AnalysisConfig(
        steps=["prepare"],
        input_dir=tmp_path / "ida_imports",
        database_dir=tmp_path / "database",
        output_root=tmp_path / "output",
        variants=("Variant_A",),
        rooms=("101 lobby",),
    )

    assert config.steps == ("prepare",)
    assert config.input_dir == tmp_path / "ida_imports"
    assert config.database_dir == tmp_path / "database"
    assert config.output_root == tmp_path / "output"
    assert config.variants == ["Variant_A"]
    assert config.rooms == ["101 lobby"]


def test_build_runtime_options_normalizes_service_values(tmp_path):
    plot_options = {
        "template": "heating-overlay",
        "setpoint_min": 20,
        "setpoint_max": 25,
        "temperature_ymin": -15,
        "temperature_ymax": 35,
        "outdoor_column": "tout",
        "show_setpoint_band": False,
        "overlay_lines": [{"source": "csv", "column": "custom_power"}],
        "primary_axis_mode": "manual",
        "primary_ymin": 0,
        "primary_ymax": 10,
    }
    config = AnalysisConfig(
        steps=["plot-template"],
        input_dir=tmp_path / "ida_imports",
        database_dir=tmp_path / "database",
        output_root=tmp_path / "output",
        variants=("Variant_A",),
        rooms=("208 office",),
        view="year",
        variant_mode="single",
        series_layout="combined",
        plot_template_options=plot_options,
    )

    runtime_options = services._build_runtime_options(config)

    assert runtime_options.input_dir == tmp_path / "ida_imports"
    assert runtime_options.database_dir == tmp_path / "database"
    assert runtime_options.output_root == tmp_path / "output"
    assert runtime_options.variants == ["Variant_A"]
    assert runtime_options.rooms == ["208 office"]
    assert runtime_options.view == "year"
    assert runtime_options.variant_mode == "single"
    assert runtime_options.series_layout == "combined"
    assert runtime_options.template == "heating-overlay"
    assert runtime_options.setpoint_min == 20.0
    assert runtime_options.show_setpoint_band is False
    assert runtime_options.overlay_lines == [{"source": "csv", "column": "custom_power"}]
    assert runtime_options.primary_axis_mode == "manual"
    assert runtime_options.plot_template_options == plot_options
    assert runtime_options.plot_template_options is not plot_options


def test_build_legacy_args_keeps_existing_namespace_contract(tmp_path):
    config = AnalysisConfig(
        steps=("plot_template",),
        input_dir=tmp_path / "ida_imports",
        database_dir=tmp_path / "database",
        output_root=tmp_path / "output",
        run_id="test-run",
        variants=["Variant_A"],
        rooms=["208 office"],
        export_format="both",
        view="month",
        month="Jan",
        variant_mode="compare",
        series_layout="separate",
        plot_template="heating-month",
        plot_template_mode="compare",
        plot_template_options={"setpoint_min": 19.5, "fixed_overlays": []},
    )

    runtime_options = services._build_runtime_options(config)
    args = services._build_legacy_args(runtime_options)

    assert args.input_dir == str(tmp_path / "ida_imports")
    assert args.datenbank_dir == str(tmp_path / "database")
    assert args.output_root == str(tmp_path / "output")
    assert args.output_root_explicit is True
    assert args.run_id == "test-run"
    assert args.variants == ["Variant_A"]
    assert args.rooms == ["208 office"]
    assert args.export_format == "both"
    assert args.view == "month"
    assert args.month == "Jan"
    assert args.heating_mode == "compare"
    assert args.heating_series_layout == "separate"
    assert args.template == "heating-month"
    assert args.plot_template_mode == "compare"
    assert args.setpoint_min == 19.5
    assert args.fixed_overlays == []


def test_execute_legacy_analysis_calls_run_all(tmp_path, monkeypatch):
    captured = {}
    database_dir = tmp_path / "database"
    database_dir.mkdir()

    def fake_run_all(args):
        captured["args"] = args
        print("all called")

    monkeypatch.setattr(services, "run_all", fake_run_all)
    runtime_options = services._build_runtime_options(
        AnalysisConfig(
            steps=("all",),
            database_dir=database_dir,
            output_root=tmp_path / "output",
            rooms=["101 lobby"],
        )
    )

    result = services._execute_legacy_analysis(runtime_options, ("all",))

    assert result.success is True
    assert result.errors == []
    assert "all called" in result.log_text
    assert captured["args"].datenbank_dir == str(database_dir)


def test_execute_legacy_analysis_maps_comfort_command(tmp_path, monkeypatch):
    captured = {}
    database_dir = tmp_path / "database"
    database_dir.mkdir()

    def fake_execute_steps(args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        print("comfort called")

    monkeypatch.setattr(services, "execute_steps", fake_execute_steps)
    runtime_options = services._build_runtime_options(
        AnalysisConfig(
            steps=("comfort",),
            database_dir=database_dir,
            output_root=tmp_path / "output",
            variants=["Variant_A"],
            rooms=["208 office"],
            comfort_output_type="plot",
        )
    )

    result = services._execute_legacy_analysis(runtime_options, ("comfort",))

    assert result.success is True
    assert result.errors == []
    assert "comfort called" in result.log_text
    assert captured["kwargs"]["steps"] == ("plots",)
    assert captured["kwargs"]["variants"] == ["Variant_A"]
    assert captured["kwargs"]["rooms"] == ["208 office"]
    assert captured["kwargs"]["comfort_options"]["plot_single"] is True
    assert captured["kwargs"]["comfort_options"]["plot_overview"] is False


def test_execute_legacy_analysis_passes_plot_template_options(tmp_path, monkeypatch):
    captured = {}
    database_dir = tmp_path / "database"
    database_dir.mkdir()
    plot_options = {
        "template": "heating-overlay",
        "setpoint_min": 20.0,
        "overlay_lines": [{"source": "csv", "column": "custom_power"}],
    }

    def fake_execute_steps(args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs

    monkeypatch.setattr(services, "execute_steps", fake_execute_steps)
    runtime_options = services._build_runtime_options(
        AnalysisConfig(
            steps=("plot_template",),
            database_dir=database_dir,
            output_root=tmp_path / "output",
            variants=["Variant_A"],
            rooms=["208 office"],
            export_format="both",
            plot_template_options=plot_options,
        )
    )

    result = services._execute_legacy_analysis(runtime_options, ("plot_template",))

    assert result.success is True
    assert result.errors == []
    assert captured["args"].template == "heating-overlay"
    assert captured["kwargs"]["steps"] == ("plot_template",)
    assert captured["kwargs"]["prepare_options"] == {"export_format": "both"}
    assert captured["kwargs"]["plot_template_options"] == runtime_options.plot_template_options


def test_execute_legacy_analysis_converts_system_exit(tmp_path, monkeypatch):
    database_dir = tmp_path / "database"
    database_dir.mkdir()

    def fake_execute_steps(_args, **_kwargs):
        print("before exit")
        raise SystemExit(3)

    monkeypatch.setattr(services, "execute_steps", fake_execute_steps)
    runtime_options = services._build_runtime_options(
        AnalysisConfig(
            steps=("analysis",),
            database_dir=database_dir,
            output_root=tmp_path / "output",
            rooms=["101 lobby"],
        )
    )

    result = services._execute_legacy_analysis(runtime_options, ("analysis",))

    assert result.success is False
    assert result.errors == ["Analyse wurde mit Exit-Code 3 beendet."]
    assert "before exit" in result.log_text


def test_execute_legacy_analysis_checks_precondition_before_execute_steps(tmp_path, monkeypatch):
    missing_database = tmp_path / "missing_database"

    def fail_execute_steps(_args, **_kwargs):
        raise AssertionError("execute_steps darf bei fehlenden Nutzdaten nicht laufen.")

    monkeypatch.setattr(services, "execute_steps", fail_execute_steps)
    runtime_options = services._build_runtime_options(
        AnalysisConfig(
            steps=("analysis",),
            database_dir=missing_database,
            output_root=tmp_path / "output",
            rooms=["101 lobby"],
        )
    )

    result = services._execute_legacy_analysis(runtime_options, ("analysis",))
    expected_errors = _missing_database_errors(missing_database)

    assert result.success is False
    assert result.errors == expected_errors
    assert result.log_text == "\n".join(expected_errors)


def test_execute_legacy_analysis_checks_all_profile_data_steps(tmp_path, monkeypatch):
    missing_database = tmp_path / "missing_database"

    def fail_run_all(_args):
        raise AssertionError("run_all darf bei fehlenden Nutzdaten nicht laufen.")

    monkeypatch.setattr(services, "run_all", fail_run_all)
    runtime_options = services._build_runtime_options(
        AnalysisConfig(
            steps=("all",),
            database_dir=missing_database,
            output_root=tmp_path / "output",
            rooms=["101 lobby"],
        )
    )

    result = services._execute_legacy_analysis(runtime_options, ("all",))
    expected_errors = _missing_database_errors(missing_database)

    assert result.success is False
    assert result.errors == expected_errors
    assert result.log_text == "\n".join(expected_errors)


def test_run_analysis_rejects_unknown_step(tmp_path):
    config = AnalysisConfig(
        steps=("does-not-exist",),
        input_dir=tmp_path / "ida_imports",
        database_dir=tmp_path / "database",
        output_root=tmp_path / "output",
        rooms=["101 lobby"],
    )

    result = run_analysis(config)

    assert isinstance(result, AnalysisResult)
    assert result.success is False
    assert result.steps == ("does_not_exist",)
    assert result.errors
    assert result.step_results == [
        AnalysisStepResult(
            step="does_not_exist",
            success=False,
            errors=result.errors,
        )
    ]


def test_run_analysis_returns_result_for_missing_database(tmp_path):
    missing_database = tmp_path / "missing_database"
    config = AnalysisConfig(
        steps=("analysis",),
        input_dir=tmp_path / "ida_imports",
        database_dir=missing_database,
        output_root=tmp_path / "output",
        rooms=["101 lobby"],
        variants=["Variant_A"],
        debug=False,
    )

    result = run_analysis(config)

    assert result.success is False
    assert result.steps == ("analysis",)
    expected_errors = _missing_database_errors(missing_database)
    assert result.errors == expected_errors
    assert result.log_text == "\n".join(expected_errors)
    assert len(result.step_results) == 1
    assert result.step_results[0].step == "analysis"
    assert result.step_results[0].success is False
    assert result.step_results[0].errors == result.errors
    assert result.step_results[0].log_text == result.log_text


def test_run_analysis_accepts_cli_step_aliases(tmp_path):
    missing_database = tmp_path / "missing_database"
    config = AnalysisConfig(
        steps=("analyze-data",),
        input_dir=tmp_path / "ida_imports",
        database_dir=missing_database,
        output_root=tmp_path / "output",
        rooms=["101 lobby"],
        variants=["Variant_A"],
    )

    result = run_analysis(config)

    assert result.success is False
    assert result.steps == ("analyze",)
    assert result.errors == _missing_database_errors(missing_database)
    assert result.step_results[0].step == "analyze"
    assert result.step_results[0].success is False


def test_list_analysis_variants_uses_input_for_prepare(tmp_path):
    input_dir = tmp_path / "ida_imports"
    variant_dir = input_dir / "Variant_A_rohdaten" / "208 office"
    variant_dir.mkdir(parents=True)

    variants = list_analysis_variants("prepare", input_dir, tmp_path / "database")

    assert variants == ["Variant_A"]


def test_list_analysis_variants_uses_database_for_analysis(tmp_path):
    database_dir = tmp_path / "database"
    (database_dir / "Variant_A_nutzdaten").mkdir(parents=True)
    (database_dir / "ignore_me").mkdir()

    variants = list_analysis_variants("analyze-data", tmp_path / "ida_imports", database_dir)

    assert variants == ["Variant_A"]


def test_list_analysis_rooms_returns_defaults():
    rooms = list_analysis_rooms()

    assert "208 office" in rooms


def test_get_plot_template_ui_spec_returns_plain_dict():
    spec = get_plot_template_ui_spec("heating-overlay")

    assert spec["name"] == "heating-overlay"
    assert spec["view"] == "year"
    assert spec["supports_overlays"] is True
    assert spec["requires_single_room"] is True


def test_get_plot_template_ui_spec_falls_back_for_unknown_template():
    spec = get_plot_template_ui_spec("unknown-template")

    assert spec == {
        "name": "unknown-template",
        "metric": "",
        "view": "",
        "supports_overlays": False,
        "requires_single_room": True,
    }


def test_get_plot_template_ui_defaults_reads_existing_template_defaults():
    defaults = get_plot_template_ui_defaults("heating-overlay")

    assert defaults["show_setpoint_band"] is True
    assert defaults["default_overlays"][0]["id"] == "outdoor_temperature"


def test_list_plot_overlay_sources_reads_csv_and_aux_columns(tmp_path):
    database_dir = tmp_path / "database"
    input_dir = tmp_path / "ida_imports"
    variant_name = "Variant_A"
    room_name = "208 office"

    database_variant_dir = database_dir / f"{variant_name}_nutzdaten"
    database_variant_dir.mkdir(parents=True)
    (database_variant_dir / "208_office.csv").write_text(
        "time,zone_energy_q_heat,custom_power,room_temperature\n"
        "2026-01-01 00:00,1.0,2.0,21.0\n",
        encoding="utf-8",
    )

    input_variant_dir = input_dir / f"{variant_name}_rohdaten"
    input_variant_dir.mkdir(parents=True)
    (input_variant_dir / "REPORT-AUX.prn").write_text(
        "time tair custom_aux\n"
        "0 5.0 9.0\n",
        encoding="utf-8",
    )

    catalog = list_plot_overlay_sources(database_dir, input_dir, variant_name, room_name)

    assert "custom_power" in catalog["csv"]
    assert "room_temperature" in catalog["csv"]
    assert "zone_energy_q_heat" not in catalog["csv"]
    assert "custom_aux" in catalog["aux"]
    assert "tair" not in catalog["aux"]


def test_list_plot_overlay_sources_returns_empty_catalog_for_missing_data(tmp_path):
    catalog = list_plot_overlay_sources(
        database_dir=tmp_path / "database",
        input_dir=tmp_path / "ida_imports",
        variant_name="Variant_A",
        room_name="208 office",
    )

    assert catalog == {"csv": [], "aux": []}


def test_run_analysis_prepare_without_input_completes_with_log(tmp_path):
    input_dir = tmp_path / "ida_imports"
    database_dir = tmp_path / "database"
    input_dir.mkdir()

    config = AnalysisConfig(
        steps=("prepare",),
        input_dir=input_dir,
        database_dir=database_dir,
        output_root=tmp_path / "output",
        rooms=["101 lobby"],
        debug=False,
    )

    result = run_analysis(config)

    assert result.success is True
    assert result.steps == ("prepare",)
    assert "Keine verarbeitbaren Variantenordner" in result.log_text
    assert database_dir.exists()
    assert result.step_results[0].step == "prepare"
    assert result.step_results[0].success is True


def test_run_analysis_collects_created_files(tmp_path, monkeypatch):
    output_root = tmp_path / "output"
    database_dir = tmp_path / "database"
    database_dir.mkdir()

    def fake_execute_steps(args, **_kwargs):
        output_path = output_root / "report.txt"
        database_path = database_dir / "table.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        database_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("report", encoding="utf-8")
        database_path.write_text("table", encoding="utf-8")

    monkeypatch.setattr(services, "execute_steps", fake_execute_steps)

    config = AnalysisConfig(
        steps=("analysis",),
        database_dir=database_dir,
        output_root=output_root,
        rooms=["101 lobby"],
    )

    result = run_analysis(config)

    assert result.success is True
    assert result.created_files == sorted(
        [
            (database_dir / "table.csv").resolve(),
            (output_root / "report.txt").resolve(),
        ]
    )
    assert result.step_results == [
        AnalysisStepResult(
            step="analysis",
            success=True,
            created_files=result.created_files,
            log_text=result.log_text,
        )
    ]
