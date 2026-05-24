"""Gemeinsame Datei-, Zeit- und Benennungslogik fuer Energy-Auswertungen."""

from __future__ import annotations

from dataclasses import dataclass

from ..components.runtime import (
    build_compare_run_output_dir,
    build_energy_plot_filename,
    build_variant_run_output_dir,
    get_dated_output_prefix,
)
from ..components.time_windows import build_energy_plot_subtitle, build_energy_time_axis_config
from ..components.time_windows import validate_time_selection as validate_component_time_selection


@dataclass(frozen=True)
class EnergyOutputSpec:
    """Beschreibt die ausgabespezifischen Unterschiede zwischen Heating und Cooling."""

    metric: str
    output_prefix_label: str
    combined_output_dir: str
    time_selection_label: str
    year_subtitle: str
    year_tick_mode: str = "1000h"


def get_output_prefix(spec: EnergyOutputSpec, reference_time=None) -> str:
    """Erzeugt den Tagespraefix fuer Energy-Ausgabedateien und -ordner."""
    return get_dated_output_prefix(spec.output_prefix_label, reference_time)


def validate_time_selection(spec: EnergyOutputSpec, view, month=None, week=None, day=None) -> bool:
    """Prueft Zeitangaben mit dem passenden Namen der Energy-Auswertung."""
    return validate_component_time_selection(
        view,
        month=month,
        week=week,
        day=day,
        label=spec.time_selection_label,
    )


def build_run_output_dir(variant_dir, run_id, output_root=None) -> str:
    """Baut den variantenbezogenen Laufordner fuer Energy-Einzelplots."""
    return build_variant_run_output_dir(variant_dir, run_id, output_root=output_root)


def build_compare_output_dir(spec: EnergyOutputSpec, run_id, output_root=None) -> str:
    """Baut den gemeinsamen Laufordner fuer Energy-Variantenvergleiche."""
    return build_compare_run_output_dir(run_id, spec.combined_output_dir, output_root=output_root)


def build_variant_plot_filename(spec: EnergyOutputSpec, view, time_window=None) -> str:
    """Dateiname fuer separate Raumplots einer Energy-Auswertung."""
    return build_energy_plot_filename(spec.metric, view, "rooms_separate", time_window=time_window)


def build_single_series_plot_filename(spec: EnergyOutputSpec, room, view, time_window=None) -> str:
    """Dateiname fuer einen einzelnen Raum-Zeitreihenplot."""
    return build_energy_plot_filename(spec.metric, view, "single", room=room, time_window=time_window)


def build_combined_plot_filename(spec: EnergyOutputSpec, room, view, time_window=None) -> str:
    """Dateiname fuer einen Variantenvergleich eines einzelnen Raums."""
    return build_energy_plot_filename(spec.metric, view, "variants_combined", room=room, time_window=time_window)


def build_plot_subtitle(spec: EnergyOutputSpec, view, month_name=None, week_number=None, day_number=None) -> str:
    """Kurzer Zeitraumtext fuer Energy-Diagramme."""
    return build_energy_plot_subtitle(
        view,
        month_name=month_name,
        week_number=week_number,
        day_number=day_number,
        year_text=spec.year_subtitle,
    )


def build_time_axis_config(spec: EnergyOutputSpec, view, time_window=None) -> dict:
    """Zeitachsenkonfiguration fuer Energy-Zeitreihen."""
    return build_energy_time_axis_config(view, time_window=time_window, year_tick_mode=spec.year_tick_mode)
