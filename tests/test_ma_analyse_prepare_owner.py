import argparse

from ma_analyse.app import commands


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
