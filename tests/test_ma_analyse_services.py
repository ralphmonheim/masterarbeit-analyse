from ma_analyse import services
from ma_analyse.models import AnalysisConfig, AnalysisResult
from ma_analyse.services import list_analysis_rooms, list_analysis_variants, list_plot_overlay_sources, run_analysis


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


def test_run_analysis_returns_result_for_missing_database(tmp_path):
    config = AnalysisConfig(
        steps=("analysis",),
        input_dir=tmp_path / "ida_imports",
        database_dir=tmp_path / "missing_database",
        output_root=tmp_path / "output",
        rooms=["101 lobby"],
        variants=["Variant_A"],
        debug=False,
    )

    result = run_analysis(config)

    assert result.success is False
    assert result.steps == ("analysis",)
    assert result.errors == ["Analyse wurde mit Exit-Code 1 beendet."]
    assert "Verzeichnis mit aufbereiteten Daten nicht gefunden" in result.log_text


def test_run_analysis_accepts_cli_step_aliases(tmp_path):
    config = AnalysisConfig(
        steps=("analyze-data",),
        input_dir=tmp_path / "ida_imports",
        database_dir=tmp_path / "missing_database",
        output_root=tmp_path / "output",
        rooms=["101 lobby"],
        variants=["Variant_A"],
    )

    result = run_analysis(config)

    assert result.success is False
    assert result.steps == ("analyze",)
    assert result.errors == ["Analyse wurde mit Exit-Code 1 beendet."]


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


def test_run_analysis_collects_created_files(tmp_path, monkeypatch):
    output_root = tmp_path / "output"
    database_dir = tmp_path / "database"

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
