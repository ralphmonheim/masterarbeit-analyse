import argparse

from ma_analyse.app import commands
from ma_analyse.app.commands import build_runtime_args


def test_run_prepare_delegates_known_ida_tree_to_data_preparation(monkeypatch, tmp_path):
    args = argparse.Namespace(
        input_dir=tmp_path / "input",
        datenbank_dir=tmp_path / "database",
        rooms=[],
        debug=False,
        variants=None,
        export_format="csv",
    )
    source = tmp_path / "input" / "Masterthesis_Dimensionierung_5Z" / "energy" / "zone.IAQ.prn"
    source.parent.mkdir(parents=True)
    source.write_text("# time order value\n0 1 1\n1 1 2\n", encoding="utf-8")
    captured = {}

    def fake_prepare(input_root, output_root, *, resume_existing=False):
        captured["call"] = (input_root, output_root, resume_existing)
        return {}

    monkeypatch.setattr(commands, "prepare_known_ida_results", fake_prepare)
    monkeypatch.setattr(commands, "process_all_variants", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("legacy called")))

    commands.run_prepare(args)

    assert captured["call"] == (args.input_dir, args.datenbank_dir, True)


def test_run_prepare_keeps_legacy_fallback(monkeypatch, tmp_path):
    args = argparse.Namespace(
        input_dir=tmp_path / "input",
        datenbank_dir=tmp_path / "database",
        rooms=["101 lobby"],
        debug=False,
        variants=["Dimensionierung"],
        export_format="both",
    )
    args.input_dir.mkdir()
    captured = {}

    monkeypatch.setattr(commands, "process_all_variants", lambda *positional, **keywords: captured.update({"args": positional, "kwargs": keywords}))

    commands.run_prepare(args)

    assert captured["args"][:3] == (args.input_dir, args.rooms, args.datenbank_dir)
    assert captured["kwargs"]["export_format"] == "both"


def test_run_prepare_uses_new_energy_layout_before_old_known_sources(monkeypatch, tmp_path):
    args = argparse.Namespace(
        input_dir=tmp_path / "input",
        datenbank_dir=tmp_path / "database",
        rooms=["101 lobby"],
        rooms_explicit=False,
        debug=False,
        variants=["new_variant"],
        export_format="csv",
    )
    energy_dir = args.input_dir / "new_variant" / "energy"
    energy_dir.mkdir(parents=True)
    for source_name in ("HEAT_BALANCE", "IAQ", "LOCAL-DE-COMF-DIAG-T", "TEMPERATURES", "ZONE-ENERGY"):
        (energy_dir / f"101 Lobby.{source_name}.prn").write_text("# time order value\n0 1 1\n", encoding="utf-8")
    captured = {}

    monkeypatch.setattr(
        commands,
        "prepare_energy_layout_variant_data",
        lambda variant_dir, rooms, output_dir, **kwargs: captured.update(
            {"variant_dir": variant_dir, "rooms": rooms, "output_dir": output_dir}
        )
        or {"variant_name": "new_variant", "processed_rooms": 1, "rows": 8760},
    )
    monkeypatch.setattr(commands, "prepare_known_ida_results", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("known called")))

    commands.run_prepare(args)

    assert captured == {
        "variant_dir": args.input_dir / "new_variant",
        "rooms": None,
        "output_dir": args.datenbank_dir,
    }


def test_run_prepare_keeps_explicit_cli_room_selection_for_energy_layout(monkeypatch, tmp_path):
    args = argparse.Namespace(
        input_dir=tmp_path / "input",
        datenbank_dir=tmp_path / "database",
        rooms=["101 Lobby"],
        rooms_explicit=True,
        debug=False,
        variants=None,
        export_format="csv",
    )
    energy_dir = args.input_dir / "EnergyVariant" / "energy"
    energy_dir.mkdir(parents=True)
    for source_name in ("HEAT_BALANCE", "IAQ", "LOCAL-DE-COMF-DIAG-T", "TEMPERATURES", "ZONE-ENERGY"):
        (energy_dir / f"101 Lobby.{source_name}.prn").write_text("# time order value\n0 1 1\n", encoding="utf-8")
    captured = {}
    monkeypatch.setattr(
        commands,
        "prepare_energy_layout_variant_data",
        lambda _variant_dir, rooms, _database_dir, **_kwargs: captured.update({"rooms": rooms})
        or {"variant_name": "EnergyVariant", "processed_rooms": 1, "rows": 1},
    )

    commands.run_prepare(args)

    assert captured["rooms"] == ["101 Lobby"]


def test_run_prepare_processes_each_layout_in_a_mixed_input_tree(monkeypatch, tmp_path):
    args = argparse.Namespace(
        input_dir=tmp_path / "input",
        datenbank_dir=tmp_path / "database",
        rooms=["101 lobby"],
        rooms_explicit=False,
        debug=False,
        variants=None,
        export_format="csv",
    )
    energy_dir = args.input_dir / "EnergyVariant" / "energy"
    energy_dir.mkdir(parents=True)
    for source_name in ("HEAT_BALANCE", "IAQ", "LOCAL-DE-COMF-DIAG-T", "TEMPERATURES", "ZONE-ENERGY"):
        (energy_dir / f"101 Lobby.{source_name}.prn").write_text("# time order value\n0 1 1\n", encoding="utf-8")
    known_energy_dir = args.input_dir / "Masterthesis_Dimensionierung_5Z" / "energy"
    known_energy_dir.mkdir(parents=True)
    for source_name in ("HEAT_BALANCE", "IAQ", "LOCAL-DE-COMF-DIAG-T", "TEMPERATURES", "ZONE-ENERGY"):
        (known_energy_dir / f"zone.{source_name}.prn").write_text("# time order value\n0 1 1\n", encoding="utf-8")
    (args.input_dir / "LegacyVariant" / "101 lobby").mkdir(parents=True)
    calls = []

    monkeypatch.setattr(
        commands,
        "prepare_energy_layout_variant_data",
        lambda variant_dir, *_args, **_kwargs: calls.append(("energy", variant_dir.name))
        or {"variant_name": variant_dir.name, "processed_rooms": 1, "rows": 1},
    )
    monkeypatch.setattr(
        commands,
        "prepare_known_ida_results",
        lambda *_args, **_kwargs: calls.append(("known", "Dimensionierung")) or {},
    )
    monkeypatch.setattr(
        commands,
        "process_all_variants",
        lambda *_args, **kwargs: calls.append(
            ("legacy", tuple(sorted(kwargs["excluded_variant_names"])))
        ),
    )

    commands.run_prepare(args)

    assert calls == [
        ("energy", "EnergyVariant"),
        ("known", "Dimensionierung"),
        ("legacy", ("EnergyVariant",)),
    ]


def test_service_pipeline_keeps_explicit_room_selection_for_energy_layout(monkeypatch, tmp_path):
    input_dir = tmp_path / "input"
    database_dir = tmp_path / "database"
    energy_dir = input_dir / "EnergyVariant" / "energy"
    energy_dir.mkdir(parents=True)
    for source_name in ("HEAT_BALANCE", "IAQ", "LOCAL-DE-COMF-DIAG-T", "TEMPERATURES", "ZONE-ENERGY"):
        (energy_dir / f"101 lobby.{source_name}.prn").write_text("# time order value\n0 1 1\n", encoding="utf-8")
    args = argparse.Namespace(
        input_dir=input_dir,
        datenbank_dir=database_dir,
        output_root=tmp_path / "output",
        output_root_explicit=True,
        run_id=None,
        debug=False,
        rooms=["101 lobby"],
        variants=None,
    )
    runtime_args = build_runtime_args(args, rooms=["101 lobby"])
    captured = {}
    monkeypatch.setattr(
        commands,
        "prepare_energy_layout_variant_data",
        lambda _variant_dir, rooms, _database_dir, **_kwargs: captured.update({"rooms": rooms})
        or {"variant_name": "EnergyVariant", "processed_rooms": 1, "rows": 1},
    )

    commands.run_prepare(runtime_args)

    assert runtime_args.rooms_explicit is True
    assert captured["rooms"] == ["101 lobby"]
