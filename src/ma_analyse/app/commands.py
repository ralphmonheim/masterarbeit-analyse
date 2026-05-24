"""Ausfuehrungslogik fuer die ma_analyse-Befehle."""

from __future__ import annotations

import argparse
import os
import time

from ..analysis.comfort.main import get_run_id, process_analysis, process_overview, process_plots
from ..analysis.cooling import main as compare_cooling_comparison
from ..analysis.excel import build_excel_report
from ..analysis.heating import main as compare_heating_comparison
from ..core.config import ROOMS
from ..core.logging import format_duration, timed_step
from ..preprocessing.prepare import process_all_variants

STEP_SEQUENCE = ["prepare", "plots", "overview", "analysis", "analyze", "heating", "cooling"]
DATABASE_STEPS = {"plots", "overview", "analysis", "analyze", "heating", "cooling"}
STEP_TITLES = {
    "prepare": "prepare (Rohdaten aufbereiten)",
    "plots": "plots (Einzelne Raumdiagramme)",
    "overview": "overview (PDF-Uebersicht)",
    "analysis": "analysis (Behaglichkeitsanalyse)",
    "analyze": "analyze_data (Excel-Auswertung)",
    "heating": "heating (Heizvergleich)",
    "cooling": "cooling (Kuehlvergleich)",
}
COMMAND_TO_INTERNAL_STEP = {
    "prepare": "prepare",
    "plots": "plots",
    "overview": "overview",
    "analysis": "analysis",
    "analyze_data": "analyze",
    "analyze-data": "analyze",
    "heating": "heating",
    "cooling": "cooling",
}

COMFORT_OUTPUT_TYPES = {
    "plot": {
        "steps": ["plots"],
        "plot_single": True,
        "plot_overview": False,
        "analysis_individual": False,
        "analysis_overview": False,
    },
    "plot_overview": {
        "steps": ["overview"],
        "plot_single": False,
        "plot_overview": True,
        "analysis_individual": False,
        "analysis_overview": False,
    },
    "plot_analysis": {
        "steps": ["plots", "analysis"],
        "plot_single": True,
        "plot_overview": False,
        "analysis_individual": True,
        "analysis_overview": False,
    },
    "plot_analysis_overview": {
        "steps": ["plots", "overview", "analysis"],
        "plot_single": True,
        "plot_overview": True,
        "analysis_individual": True,
        "analysis_overview": True,
    },
}


def get_comfort_output_settings(output_type):
    """Uebersetzt Comfort-Unterbefehle in interne Pipeline-Schritte."""
    if output_type not in COMFORT_OUTPUT_TYPES:
        raise ValueError(f"Ungültiger output_type: {output_type}. Erwartet: {', '.join(COMFORT_OUTPUT_TYPES)}")
    return COMFORT_OUTPUT_TYPES[output_type]


def run_prepare(args):
    """Fuehrt den prepare-Befehl aus und erzeugt Nutzdaten."""
    process_all_variants(
        args.input_dir,
        args.rooms,
        args.datenbank_dir,
        debug=args.debug,
        selected_variants=args.variants,
        export_format=getattr(args, "export_format", "csv"),
    )


def run_plots(args):
    """Fuehrt Comfort-Einzelplots aus."""
    process_plots(
        datenbank_dir=args.datenbank_dir,
        rooms=args.rooms,
        run_id=args.run_id,
        output_root=args.output_root,
        variant_dirs=args.variants,
        debug=args.debug,
        output_subdir=getattr(args, "plot_output_subdir", None),
    )


def run_overview(args):
    """Fuehrt Comfort-PDF-Uebersichten aus."""
    process_overview(
        datenbank_dir=args.datenbank_dir,
        rooms=args.rooms,
        run_id=args.run_id,
        output_root=args.output_root,
        variant_dirs=args.variants,
        debug=args.debug,
    )


def run_analysis(args, run_id=None, output_individual=True, output_overview=True):
    """Fuehrt die Comfort-Zonenanalyse aus und protokolliert die Tabelle."""
    result = process_analysis(
        datenbank_dir=args.datenbank_dir,
        rooms=args.rooms,
        run_id=run_id,
        output_root=args.output_root,
        variant_dirs=args.variants,
        debug=args.debug,
        output_individual=output_individual,
        output_overview=output_overview,
    )
    if result is None:
        print("X Keine Ergebnisse erzeugt")
        raise SystemExit(1)

    print(result.to_string(index=False))


def run_analyze(args):
    """Fuehrt analyze_data aus und mappt GUI-Ausgabearten auf Excel-Modi."""
    layout_mode = getattr(args, "heating_series_layout", None)
    if layout_mode == "separate":
        variant_mode = "single"
    elif layout_mode == "combined":
        variant_mode = "compare"
    else:
        variant_mode = getattr(args, "heating_mode", None)
        if variant_mode is None:
            variant_mode = "compare" if getattr(args, "variant_mode_explicit", False) else "single"

    output_files = build_excel_report(
        args.datenbank_dir,
        output_root=args.output_root,
        debug=args.debug,
        run_id=args.run_id,
        selected_variants=args.variants,
        rooms=args.rooms,
        variant_mode=variant_mode,
    )
    if isinstance(output_files, list):
        for output_file in output_files:
            print(f"Excel-Ausgabe erstellt: {output_file}")
        return
    print(f"Excel-Ausgabe erstellt: {output_files}")


def run_heating(args):
    """Fuehrt den Heating-Vergleich mit den gewaehlten Zeit-/Layoutoptionen aus."""
    compare_heating_comparison(
        args.datenbank_dir,
        debug=args.debug,
        selected_variants=args.variants,
        rooms=args.rooms,
        view=getattr(args, "view", "bar"),
        month=getattr(args, "month", None),
        week=getattr(args, "week", None),
        day=getattr(args, "day", None),
        variant_mode=getattr(args, "heating_mode", None) or "compare",
        series_layout=getattr(args, "heating_series_layout", None) or "separate",
        output_root=getattr(args, "output_root", None),
        run_id=getattr(args, "run_id", None),
    )


def run_cooling(args):
    """Fuehrt den Cooling-Vergleich mit den gewaehlten Zeit-/Layoutoptionen aus."""
    view = getattr(args, "view", "year")
    compare_cooling_comparison(
        args.datenbank_dir,
        debug=args.debug,
        selected_variants=args.variants,
        rooms=args.rooms,
        view=view,
        month=getattr(args, "month", None),
        week=getattr(args, "week", None),
        day=getattr(args, "day", None),
        variant_mode=getattr(args, "heating_mode", None) or "compare",
        series_layout=getattr(args, "heating_series_layout", None) or "separate",
        output_root=getattr(args, "output_root", None),
        run_id=getattr(args, "run_id", None),
    )


def run_comfort(args):
    """Fuehrt den Comfort-Unterbefehl ueber die gemeinsame Pipeline aus."""
    output_type = getattr(args, "output_type", "plot_analysis_overview")
    settings = get_comfort_output_settings(output_type)
    execute_steps(
        args,
        steps=settings["steps"],
        variants=args.variants,
        rooms=args.rooms,
        comfort_options=settings,
    )


def ensure_required_data(args, steps):
    """Bricht Analyse-/Plotbefehle ab, wenn vorherige Nutzdaten fehlen."""
    if not any(step in DATABASE_STEPS for step in steps):
        return

    if os.path.exists(args.datenbank_dir):
        return

    if "prepare" in steps:
        return

    print(f"X Verzeichnis mit aufbereiteten Daten nicht gefunden: {args.datenbank_dir}")
    print("  Fuehren Sie zuerst 'prepare' aus oder waehlen Sie in der GUI auch prepare.")
    raise SystemExit(1)


def build_runtime_args(
    args,
    variants=None,
    rooms=None,
    heating_mode=None,
    prepare_options=None,
    comfort_options=None,
    heating_options=None,
    plot_output_subdir=None,
):
    """Baut ein einheitliches Argumentobjekt fuer interne Pipeline-Schritte."""
    comfort_defaults = {
        "plot_single": True,
        "plot_overview": True,
        "analysis_individual": True,
        "analysis_overview": True,
    }
    if comfort_options:
        comfort_defaults.update(comfort_options)

    heating_defaults = {
        "view": getattr(args, "view", "bar"),
        "month": getattr(args, "month", None),
        "week": getattr(args, "week", None),
        "day": getattr(args, "day", None),
        "series_layout": getattr(args, "heating_series_layout", None) or "separate",
    }
    if heating_options:
        heating_defaults.update(heating_options)

    prepare_defaults = {
        "export_format": getattr(args, "export_format", "csv"),
    }
    if prepare_options:
        prepare_defaults.update(prepare_options)

    return argparse.Namespace(
        input_dir=args.input_dir,
        datenbank_dir=args.datenbank_dir,
        output_root=args.output_root,
        run_id=args.run_id,
        debug=args.debug,
        variants=variants,
        rooms=rooms if rooms is not None else ROOMS.copy(),
        view=heating_defaults["view"],
        month=heating_defaults["month"],
        week=heating_defaults["week"],
        day=heating_defaults["day"],
        heating_series_layout=heating_defaults["series_layout"],
        heating_mode=heating_mode or getattr(args, "heating_mode", None) or "compare",
        plot_single=comfort_defaults["plot_single"],
        plot_overview=comfort_defaults["plot_overview"],
        analysis_individual=comfort_defaults["analysis_individual"],
        analysis_overview=comfort_defaults["analysis_overview"],
        plot_output_subdir=plot_output_subdir,
        export_format=prepare_defaults["export_format"],
    )


def execute_steps(
    args,
    steps,
    variants=None,
    rooms=None,
    heating_mode=None,
    prepare_options=None,
    comfort_options=None,
    heating_options=None,
    plot_output_subdir=None,
):
    """Fuehrt eine geordnete Teilmenge der Pipeline-Schritte aus."""
    selected_steps = [step for step in STEP_SEQUENCE if step in steps]
    ensure_required_data(args, selected_steps)

    runtime_args = build_runtime_args(
        args,
        variants=variants,
        rooms=rooms,
        heating_mode=heating_mode,
        prepare_options=prepare_options,
        comfort_options=comfort_options,
        heating_options=heating_options,
        plot_output_subdir=plot_output_subdir,
    )

    print("\n" + "=" * 70)
    print("PIPELINE GESTARTET")
    print("=" * 70)

    pipeline_start = time.perf_counter()
    total_steps = len(selected_steps)
    for index, step in enumerate(selected_steps, start=1):
        if step == "plots" and not runtime_args.plot_single:
            continue
        if step == "overview" and not runtime_args.plot_overview:
            continue

        step_title = STEP_TITLES[step]
        print(f"\nSchritt {index}/{total_steps}: {step_title}")
        print("-" * 70)

        with timed_step(step_title):
            if step == "prepare":
                run_prepare(runtime_args)
                continue

            if step == "plots":
                run_plots(runtime_args)
                continue

            if step == "overview":
                run_overview(runtime_args)
                continue

            if step == "analysis":
                run_analysis(
                    runtime_args,
                    run_id=runtime_args.run_id,
                    output_individual=runtime_args.analysis_individual,
                    output_overview=runtime_args.analysis_overview,
                )
                continue

            if step == "analyze":
                run_analyze(runtime_args)
                continue

            if step == "heating":
                run_heating(runtime_args)
                continue

            if step == "cooling":
                run_cooling(runtime_args)
                continue

    print("\n" + "=" * 70)
    print(f"Gesamtlaufzeit Pipeline: {format_duration(time.perf_counter() - pipeline_start)}")
    print("PIPELINE ABGESCHLOSSEN")
    print("=" * 70)


def run_all(args):
    """Fuehrt das feste Ausgabeprofil fuer den Sammelbefehl ``all`` aus."""
    shared_run_id = get_run_id(command_name="all", run_id=args.run_id)
    args.run_id = shared_run_id

    steps = ["overview", "analysis", "heating", "cooling"]
    ensure_required_data(args, steps)

    variants = args.variants
    rooms = args.rooms if args.rooms is not None else ROOMS.copy()
    comfort_options = {
        "plot_single": False,
        "plot_overview": True,
        "analysis_individual": False,
        "analysis_overview": True,
    }
    year_separate_options = {
        "view": "year",
        "month": None,
        "week": None,
        "day": None,
        "series_layout": "separate",
    }
    bar_options = {
        "view": "bar",
        "month": None,
        "week": None,
        "day": None,
        "series_layout": "separate",
    }

    comfort_runtime_args = build_runtime_args(
        args,
        variants=variants,
        rooms=rooms,
        comfort_options=comfort_options,
    )
    load_single_args = build_runtime_args(
        args,
        variants=variants,
        rooms=rooms,
        heating_mode="single",
        heating_options=year_separate_options,
    )
    load_compare_args = build_runtime_args(
        args,
        variants=variants,
        rooms=rooms,
        heating_mode="compare",
        heating_options=year_separate_options,
    )
    load_bar_args = build_runtime_args(
        args,
        variants=variants,
        rooms=rooms,
        heating_mode="compare",
        heating_options=bar_options,
    )

    all_steps = [
        ("Comfort-Uebersicht", lambda: run_overview(comfort_runtime_args)),
        (
            "Analyse-Uebersicht",
            lambda: run_analysis(
                comfort_runtime_args,
                run_id=comfort_runtime_args.run_id,
                output_individual=False,
                output_overview=True,
            ),
        ),
        ("Heating Barplots", lambda: run_heating(load_bar_args)),
        ("Cooling Barplots", lambda: run_cooling(load_bar_args)),
        ("Heating Jahresplots single", lambda: run_heating(load_single_args)),
        ("Heating Jahresplots Raeume kombiniert", lambda: run_heating(load_compare_args)),
        ("Cooling Jahresplots single", lambda: run_cooling(load_single_args)),
        ("Cooling Jahresplots Raeume kombiniert", lambda: run_cooling(load_compare_args)),
    ]

    print("\n" + "=" * 70)
    print("ALL-PROFIL GESTARTET")
    print("=" * 70)
    print(f"Run-ID: {shared_run_id}")

    profile_start = time.perf_counter()
    total_steps = len(all_steps)
    for index, (title, runner) in enumerate(all_steps, start=1):
        print(f"\nSchritt {index}/{total_steps}: {title}")
        print("-" * 70)
        with timed_step(title):
            runner()

    print("\n" + "=" * 70)
    print(f"Gesamtlaufzeit all: {format_duration(time.perf_counter() - profile_start)}")
    print("ALL-PROFIL ABGESCHLOSSEN")
    print("=" * 70)


def dispatch_command(args):
    """Fuehrt den bereits geparsten CLI-Befehl aus."""
    if args.command == "prepare":
        with timed_step(STEP_TITLES["prepare"]):
            ensure_required_data(args, ["prepare"])
            run_prepare(args)
        return

    if args.command == "comfort":
        comfort_steps = get_comfort_output_settings(args.output_type)["steps"]
        ensure_required_data(args, comfort_steps)
        run_comfort(args)
        return

    if args.command in {"analyze-data", "analyze_data"}:
        with timed_step(STEP_TITLES["analyze"]):
            ensure_required_data(args, ["analyze"])
            run_analyze(args)
        return

    if args.command == "heating":
        with timed_step(STEP_TITLES["heating"]):
            ensure_required_data(args, ["heating"])
            run_heating(args)
        return

    if args.command == "cooling":
        with timed_step(STEP_TITLES["cooling"]):
            ensure_required_data(args, ["cooling"])
            run_cooling(args)
        return

    if args.command == "gui":
        from ..gui.app import run_gui

        run_gui(args)
        return

    if args.command == "all":
        run_all(args)
