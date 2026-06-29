"""AnalysisConfig-Adapter fuer die Tkinter-Analyse."""

from __future__ import annotations

from typing import Any

from ma_analyse.analysis_ui import build_analysis_config
from ma_analyse.models import AnalysisConfig

TKINTER_COMMAND_STEPS = {
    "prepare": "prepare",
    "comfort": "comfort",
    "analyze_data": "analyze_data",
    "heating": "heating",
    "cooling": "cooling",
    "plot-template": "plot-template",
    "all": "all",
}


def build_tkinter_analysis_config(
    *,
    args,
    selected_command: str,
    variants: list[str],
    rooms: list[str],
    heating_mode: str,
    prepare_options: dict[str, object] | None = None,
    comfort_output_type: str | None = None,
    heating_options: dict[str, object] | None = None,
    plot_template_options: dict[str, Any] | None = None,
) -> AnalysisConfig:
    """Baut den UI-neutralen Analyseauftrag aus dem Tkinter-Zustand."""
    step = TKINTER_COMMAND_STEPS.get(selected_command, selected_command)
    prepare_options = prepare_options or {}
    heating_options = heating_options or {}
    plot_template_options = plot_template_options or {}
    plot_template_mode = str(plot_template_options.get("output_mode") or "single")
    plot_template = (
        str(plot_template_options.get("template"))
        if selected_command == "plot-template" and plot_template_options.get("template")
        else None
    )

    return build_analysis_config(
        step=step,
        input_dir=args.input_dir,
        database_dir=args.datenbank_dir,
        output_root=args.output_root,
        run_id=getattr(args, "run_id", None),
        variants=variants,
        rooms=rooms,
        debug=bool(getattr(args, "debug", True)),
        export_format=str(prepare_options.get("export_format") or "csv"),
        comfort_output_type=comfort_output_type,
        load_kind=selected_command if selected_command in {"heating", "cooling"} else None,
        view=str(heating_options.get("view") or "bar"),
        month=heating_options.get("month"),
        week=heating_options.get("week"),
        day=heating_options.get("day"),
        variant_mode=heating_mode or None,
        series_layout=heating_options.get("series_layout"),
        plot_template=plot_template,
        plot_template_mode=plot_template_mode,
        plot_template_options=plot_template_options.copy(),
    )


__all__ = ["TKINTER_COMMAND_STEPS", "build_tkinter_analysis_config"]
