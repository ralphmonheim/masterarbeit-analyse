"""Manuell anpassbare Diagramm-Vorlagen fuer Analyseausgaben."""

import math
import shutil
import uuid
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from ...core.config import INPUT_DIR, TEST_OUTPUT_DIR
from ..components.runtime import get_run_id
from .barplots import build_bar_template, validate_bar_template_request
from .catalog import (
    COMFORT_ANALYSIS_OVERVIEW_TEMPLATE,
    COMFORT_ANALYSIS_TEMPLATE,
    COMFORT_PLOT_OVERVIEW_TEMPLATE,
    COMFORT_PLOT_TEMPLATE,
    COOLING_ABSOLUTE_DAY_TEMPLATE,
    COOLING_ABSOLUTE_MONTH_TEMPLATE,
    COOLING_ABSOLUTE_WEEK_TEMPLATE,
    COOLING_ABSOLUTE_YEAR_TEMPLATE,
    COOLING_BAR_TEMPLATE,
    COOLING_DAY_TEMPLATE,
    COOLING_MONTH_TEMPLATE,
    COOLING_WEEK_TEMPLATE,
    COOLING_YEAR_TEMPLATE,
    ENERGY_BALANCE_DAY_TEMPLATE,
    ENERGY_BALANCE_MONTH_TEMPLATE,
    ENERGY_BALANCE_WEEK_TEMPLATE,
    ENERGY_BALANCE_YEAR_TEMPLATE,
    HEATING_BAR_TEMPLATE,
    HEATING_DAY_TEMPLATE,
    HEATING_MONTH_TEMPLATE,
    HEATING_OVERLAY_TEMPLATE,
    HEATING_WEEK_TEMPLATE,
    HEATING_YEAR_TEMPLATE,
    INTERNAL_LOADS_DAY_TEMPLATE,
    INTERNAL_LOADS_MONTH_TEMPLATE,
    INTERNAL_LOADS_MONTHLY_SUM_TEMPLATE,
    INTERNAL_LOADS_ROOM_COMPARISON_TEMPLATE,
    INTERNAL_LOADS_WEEK_TEMPLATE,
    INTERNAL_LOADS_YEAR_TEMPLATE,
    PLOT_TEMPLATE_CHOICES,
    THERMAL_ROOM_CLIMATE_DAY_TEMPLATE,
    THERMAL_ROOM_CLIMATE_MONTH_TEMPLATE,
    THERMAL_ROOM_CLIMATE_WEEK_TEMPLATE,
    THERMAL_ROOM_CLIMATE_YEAR_TEMPLATE,
    TIMELINE_TEMPLATE_CHOICES,
    get_plot_template_spec,
    is_bar_template,
    is_comfort_template,
    is_energy_balance_template,
    is_internal_loads_template,
    is_thermal_room_climate_template,
    is_time_filtered_template,
    template_requires_single_room,
    template_uses_overlay_options,
)
from .comfort import build_comfort_template, validate_comfort_template_request
from .energy_balance import build_energy_balance_template, validate_energy_balance_template_request
from .heating_year import (
    DEFAULT_OUTDOOR_COLUMN,
    DEFAULT_SETPOINT_MAX,
    DEFAULT_SETPOINT_MIN,
    DEFAULT_SHOW_OPERATIVE_TEMPERATURE,
    DEFAULT_SHOW_OUTDOOR_TEMPERATURE,
    DEFAULT_SHOW_SETPOINT_BAND,
    DEFAULT_TEMPERATURE_YMAX,
    DEFAULT_TEMPERATURE_YMIN,
    build_heating_year_template,
    list_heating_year_overlay_sources,
    load_hourly_prn_series,
    validate_template_request,
)
from .internal_loads import build_internal_loads_template, validate_internal_loads_template_request
from .room_climate import build_room_climate_template, validate_room_climate_template_request
from .timeline import build_timeline_template


def _flatten_output_files(result) -> list[str]:
    return [str(path) for path in result] if isinstance(result, list) else [str(result)]


def _build_comparison_sheet(
    image_files: list[str],
    *,
    output_root,
    run_id: str,
    template: str,
) -> str:
    if not image_files:
        raise ValueError("Keine Einzelansichten fuer den Plot-Template-Vergleich erzeugt.")
    non_raster_files = [
        image_file
        for image_file in image_files
        if Path(image_file).suffix.lower() not in {".png", ".jpg", ".jpeg"}
    ]
    if non_raster_files:
        raise ValueError(
            "compare konnte fuer dieses Template keine gemeinsame Rastergrafik erzeugen: "
            + ", ".join(Path(path).name for path in non_raster_files)
        )

    column_count = min(2, len(image_files))
    row_count = math.ceil(len(image_files) / column_count)
    figure, axes = plt.subplots(
        row_count,
        column_count,
        figsize=(12.8 * column_count, 7.2 * row_count),
        squeeze=False,
    )
    for axis, image_file in zip(axes.flat, image_files, strict=False):
        axis.imshow(plt.imread(image_file))
        path = Path(image_file)
        axis.set_title(f"{path.parent.name} | {path.stem}", fontsize=10)
        axis.axis("off")
    for axis in list(axes.flat)[len(image_files) :]:
        axis.axis("off")
    figure.suptitle(f"Plot-Template Vergleich: {template}", fontsize=15, fontweight="bold")
    figure.tight_layout(rect=(0, 0, 1, 0.97))

    output_dir = Path(output_root or TEST_OUTPUT_DIR) / "PlotTemplates" / run_id / "Compare"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{template.replace('-', '_')}_compare.png"
    figure.savefig(output_file, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return str(output_file)


def build_plot_template(
    datenbank_dir,
    input_dir=INPUT_DIR,
    output_root=None,
    selected_variants=None,
    rooms=None,
    template=HEATING_YEAR_TEMPLATE,
    output_mode="single",
    setpoint_min=DEFAULT_SETPOINT_MIN,
    setpoint_max=DEFAULT_SETPOINT_MAX,
    temperature_ymin=DEFAULT_TEMPERATURE_YMIN,
    temperature_ymax=DEFAULT_TEMPERATURE_YMAX,
    outdoor_column=DEFAULT_OUTDOOR_COLUMN,
    show_setpoint_band=DEFAULT_SHOW_SETPOINT_BAND,
    show_outdoor_temperature=DEFAULT_SHOW_OUTDOOR_TEMPERATURE,
    show_operative_temperature=DEFAULT_SHOW_OPERATIVE_TEMPERATURE,
    overlay_lines=None,
    fixed_overlays=None,
    primary_axis_mode="automatic",
    primary_ymin=None,
    primary_ymax=None,
    secondary_axis_mode="automatic",
    secondary_ymin=None,
    secondary_ymax=None,
    month=None,
    week=None,
    day=None,
    run_id=None,
    plot_template_config_path=None,
    debug=False,
):
    """Fuehrt das passende Plot-Template anhand des Template-Namens aus."""
    spec = get_plot_template_spec(template)
    native_compare = template in {HEATING_YEAR_TEMPLATE, HEATING_OVERLAY_TEMPLATE} or (
        spec is not None and spec.metric in {"heating", "cooling", "cooling_absolute"}
    )

    if output_mode == "compare" and not native_compare:
        resolved_run_id = get_run_id("plot_template", run_id=run_id)
        source_template = {
            COMFORT_PLOT_OVERVIEW_TEMPLATE: COMFORT_PLOT_TEMPLATE,
            COMFORT_ANALYSIS_OVERVIEW_TEMPLATE: COMFORT_ANALYSIS_TEMPLATE,
        }.get(template, template)
        temporary_parent = Path(output_root or TEST_OUTPUT_DIR) / "PlotTemplates" / resolved_run_id
        temporary_parent.mkdir(parents=True, exist_ok=True)
        temporary_root = temporary_parent / f"_compare_source_{uuid.uuid4().hex}"
        temporary_root.mkdir(parents=True, exist_ok=False)
        try:
            result = build_plot_template(
                datenbank_dir=datenbank_dir,
                input_dir=input_dir,
                output_root=str(temporary_root),
                selected_variants=selected_variants,
                rooms=rooms,
                template=source_template,
                output_mode="single",
                setpoint_min=setpoint_min,
                setpoint_max=setpoint_max,
                temperature_ymin=temperature_ymin,
                temperature_ymax=temperature_ymax,
                outdoor_column=outdoor_column,
                show_setpoint_band=show_setpoint_band,
                show_outdoor_temperature=show_outdoor_temperature,
                show_operative_temperature=show_operative_temperature,
                overlay_lines=overlay_lines,
                fixed_overlays=fixed_overlays,
                primary_axis_mode=primary_axis_mode,
                primary_ymin=primary_ymin,
                primary_ymax=primary_ymax,
                secondary_axis_mode=secondary_axis_mode,
                secondary_ymin=secondary_ymin,
                secondary_ymax=secondary_ymax,
                month=month,
                week=week,
                day=day,
                run_id=resolved_run_id,
                plot_template_config_path=plot_template_config_path,
                debug=debug,
            )
            return _build_comparison_sheet(
                _flatten_output_files(result),
                output_root=output_root,
                run_id=resolved_run_id,
                template=template,
            )
        finally:
            shutil.rmtree(temporary_root, ignore_errors=True)

    if (
        output_mode == "single"
        and template_requires_single_room(template)
        and rooms
        and len(rooms) > 1
    ):
        output_files = []
        for room in rooms:
            result = build_plot_template(
                datenbank_dir=datenbank_dir,
                input_dir=input_dir,
                output_root=output_root,
                selected_variants=selected_variants,
                rooms=[room],
                template=template,
                output_mode=output_mode,
                setpoint_min=setpoint_min,
                setpoint_max=setpoint_max,
                temperature_ymin=temperature_ymin,
                temperature_ymax=temperature_ymax,
                outdoor_column=outdoor_column,
                show_setpoint_band=show_setpoint_band,
                show_outdoor_temperature=show_outdoor_temperature,
                show_operative_temperature=show_operative_temperature,
                overlay_lines=overlay_lines,
                fixed_overlays=fixed_overlays,
                primary_axis_mode=primary_axis_mode,
                primary_ymin=primary_ymin,
                primary_ymax=primary_ymax,
                secondary_axis_mode=secondary_axis_mode,
                secondary_ymin=secondary_ymin,
                secondary_ymax=secondary_ymax,
                month=month,
                week=week,
                day=day,
                run_id=run_id,
                plot_template_config_path=plot_template_config_path,
                debug=debug,
            )
            output_files.extend(result if isinstance(result, list) else [result])
        return output_files

    if template in {HEATING_YEAR_TEMPLATE, HEATING_OVERLAY_TEMPLATE}:
        if template == HEATING_YEAR_TEMPLATE:
            show_setpoint_band = False
            show_outdoor_temperature = False
            show_operative_temperature = False
            overlay_lines = None
            fixed_overlays = []

        return build_heating_year_template(
            datenbank_dir=datenbank_dir,
            input_dir=input_dir,
            output_root=output_root,
            selected_variants=selected_variants,
            rooms=rooms,
            template=template,
            setpoint_min=setpoint_min,
            setpoint_max=setpoint_max,
            temperature_ymin=temperature_ymin,
            temperature_ymax=temperature_ymax,
            outdoor_column=outdoor_column,
            show_setpoint_band=show_setpoint_band,
            show_outdoor_temperature=show_outdoor_temperature,
            show_operative_temperature=show_operative_temperature,
            overlay_lines=overlay_lines,
            fixed_overlays=fixed_overlays,
            output_mode=output_mode,
            primary_axis_mode=primary_axis_mode,
            primary_ymin=primary_ymin,
            primary_ymax=primary_ymax,
            secondary_axis_mode=secondary_axis_mode,
            secondary_ymin=secondary_ymin,
            secondary_ymax=secondary_ymax,
            run_id=run_id,
            debug=debug,
        )

    if is_internal_loads_template(template):
        return build_internal_loads_template(
            datenbank_dir=datenbank_dir,
            output_root=output_root,
            selected_variants=selected_variants,
            rooms=rooms,
            template=template,
            month=month,
            week=week,
            day=day,
            run_id=run_id,
            debug=debug,
        )

    if is_comfort_template(template):
        return build_comfort_template(
            datenbank_dir=datenbank_dir,
            output_root=output_root,
            selected_variants=selected_variants,
            rooms=rooms,
            template=template,
            run_id=run_id,
            plot_template_config=plot_template_config_path,
            debug=debug,
        )

    if is_bar_template(template):
        return build_bar_template(
            datenbank_dir=datenbank_dir,
            output_root=output_root,
            selected_variants=selected_variants,
            rooms=rooms,
            template=template,
            run_id=run_id,
            debug=debug,
        )

    if is_thermal_room_climate_template(template):
        return build_room_climate_template(
            datenbank_dir=datenbank_dir,
            input_dir=input_dir,
            output_root=output_root,
            selected_variants=selected_variants,
            rooms=rooms,
            template=template,
            setpoint_min=setpoint_min,
            setpoint_max=setpoint_max,
            month=month,
            week=week,
            day=day,
            run_id=run_id,
            debug=debug,
        )

    if is_energy_balance_template(template):
        return build_energy_balance_template(
            datenbank_dir=datenbank_dir,
            input_dir=input_dir,
            output_root=output_root,
            selected_variants=selected_variants,
            rooms=rooms,
            template=template,
            month=month,
            week=week,
            day=day,
            run_id=run_id,
            debug=debug,
        )

    return build_timeline_template(
        datenbank_dir=datenbank_dir,
        output_root=output_root,
        selected_variants=selected_variants,
        rooms=rooms,
        template=template,
        month=month,
        week=week,
        day=day,
        output_mode=output_mode,
        primary_axis_mode=primary_axis_mode,
        primary_ymin=primary_ymin,
        primary_ymax=primary_ymax,
        run_id=run_id,
        debug=debug,
    )


__all__ = [
    "COMFORT_ANALYSIS_OVERVIEW_TEMPLATE",
    "COMFORT_ANALYSIS_TEMPLATE",
    "COMFORT_PLOT_OVERVIEW_TEMPLATE",
    "COMFORT_PLOT_TEMPLATE",
    "COOLING_ABSOLUTE_DAY_TEMPLATE",
    "COOLING_ABSOLUTE_MONTH_TEMPLATE",
    "COOLING_ABSOLUTE_WEEK_TEMPLATE",
    "COOLING_ABSOLUTE_YEAR_TEMPLATE",
    "COOLING_BAR_TEMPLATE",
    "COOLING_DAY_TEMPLATE",
    "COOLING_MONTH_TEMPLATE",
    "COOLING_WEEK_TEMPLATE",
    "COOLING_YEAR_TEMPLATE",
    "ENERGY_BALANCE_DAY_TEMPLATE",
    "ENERGY_BALANCE_MONTH_TEMPLATE",
    "ENERGY_BALANCE_WEEK_TEMPLATE",
    "ENERGY_BALANCE_YEAR_TEMPLATE",
    "DEFAULT_OUTDOOR_COLUMN",
    "DEFAULT_SETPOINT_MAX",
    "DEFAULT_SETPOINT_MIN",
    "DEFAULT_SHOW_OPERATIVE_TEMPERATURE",
    "DEFAULT_SHOW_OUTDOOR_TEMPERATURE",
    "DEFAULT_SHOW_SETPOINT_BAND",
    "DEFAULT_TEMPERATURE_YMAX",
    "DEFAULT_TEMPERATURE_YMIN",
    "HEATING_DAY_TEMPLATE",
    "HEATING_BAR_TEMPLATE",
    "HEATING_MONTH_TEMPLATE",
    "HEATING_WEEK_TEMPLATE",
    "HEATING_YEAR_TEMPLATE",
    "INTERNAL_LOADS_DAY_TEMPLATE",
    "INTERNAL_LOADS_MONTH_TEMPLATE",
    "INTERNAL_LOADS_MONTHLY_SUM_TEMPLATE",
    "INTERNAL_LOADS_ROOM_COMPARISON_TEMPLATE",
    "INTERNAL_LOADS_WEEK_TEMPLATE",
    "INTERNAL_LOADS_YEAR_TEMPLATE",
    "PLOT_TEMPLATE_CHOICES",
    "THERMAL_ROOM_CLIMATE_DAY_TEMPLATE",
    "THERMAL_ROOM_CLIMATE_MONTH_TEMPLATE",
    "THERMAL_ROOM_CLIMATE_WEEK_TEMPLATE",
    "THERMAL_ROOM_CLIMATE_YEAR_TEMPLATE",
    "TIMELINE_TEMPLATE_CHOICES",
    "build_bar_template",
    "build_comfort_template",
    "build_plot_template",
    "build_energy_balance_template",
    "build_heating_year_template",
    "build_internal_loads_template",
    "build_room_climate_template",
    "build_timeline_template",
    "get_plot_template_spec",
    "is_bar_template",
    "is_comfort_template",
    "is_energy_balance_template",
    "is_internal_loads_template",
    "is_time_filtered_template",
    "is_thermal_room_climate_template",
    "list_heating_year_overlay_sources",
    "load_hourly_prn_series",
    "template_requires_single_room",
    "template_uses_overlay_options",
    "validate_bar_template_request",
    "validate_comfort_template_request",
    "validate_energy_balance_template_request",
    "validate_internal_loads_template_request",
    "validate_room_climate_template_request",
    "validate_template_request",
]
