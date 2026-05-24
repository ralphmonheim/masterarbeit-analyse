"""Gemeinsame Laufzeit-, Datei- und Ausgabepfad-Helfer fuer Plots und Reports."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from ...core.config import OUTPUT_DIR, RUN_FOLDER_SUFFIX
from .variants import get_variant_display_name


def get_dated_output_prefix(label: str, reference_time: datetime | None = None) -> str:
    """Erzeugt einen Tagespraefix wie ``260524_Label``."""
    if reference_time is None:
        reference_time = datetime.now()
    return f"{reference_time.strftime('%y%m%d')}_{label}"


def get_run_id(command_name: str | None = None, run_id: str | None = None) -> str:
    """Gibt eine bestehende Lauf-ID zurueck oder erzeugt eine neue mit Befehlsnamen."""
    if run_id:
        return run_id
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    if command_name:
        return f"{timestamp}_{command_name}"
    return timestamp


def annotate_timestamp(fig, timestamp: str | None = None) -> None:
    """Fuegt einen Erstellungszeitstempel unten rechts auf einer Matplotlib-Figur ein."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fig.text(
        0.99,
        0.01,
        f"Erstellt: {timestamp}",
        ha="right",
        va="bottom",
        fontsize=8,
        color="black",
        alpha=0.65,
        transform=fig.transFigure,
    )


def sanitize_file_name(value: str) -> str:
    """Entfernt Zeichen, die in Dateinamen stoeren wuerden."""
    return value.replace(" ", "_").replace("/", "_").replace("\\", "_")


def ensure_output_run_suffix(run_id: str) -> str:
    """Ergaenzt das Standardsuffix fuer variantenbezogene Laufordner genau einmal."""
    if run_id.endswith(RUN_FOLDER_SUFFIX):
        return run_id
    return f"{run_id}{RUN_FOLDER_SUFFIX}"


def build_variant_run_output_dir(
    variant_dir: str | Path,
    run_id: str,
    output_root: str | Path | None = None,
    default_output_dir: str | Path = OUTPUT_DIR,
    append_run_suffix: bool = True,
) -> str:
    """Baut einen Laufordner im Schema ``<output_root>/<variante>/<run_id>``."""
    base_output_dir = output_root if output_root else default_output_dir
    effective_run_id = ensure_output_run_suffix(run_id) if append_run_suffix else run_id
    return os.path.join(str(base_output_dir), get_variant_display_name(variant_dir), effective_run_id)


def build_named_run_output_dir(
    name: str,
    run_id: str,
    output_root: str | Path | None = None,
    default_output_dir: str | Path = OUTPUT_DIR,
    append_run_suffix: bool = False,
) -> str:
    """Baut einen Laufordner mit einem festen Gruppennamen."""
    base_output_dir = output_root if output_root else default_output_dir
    effective_run_id = ensure_output_run_suffix(run_id) if append_run_suffix else run_id
    return os.path.join(str(base_output_dir), name, effective_run_id)


def build_compare_run_output_dir(
    run_id: str,
    combined_output_dir: str,
    output_root: str | Path | None = None,
    default_output_dir: str | Path = OUTPUT_DIR,
) -> str:
    """Baut den Laufordner fuer kombinierte Variantenvergleiche."""
    return build_named_run_output_dir(
        combined_output_dir,
        run_id,
        output_root=output_root,
        default_output_dir=default_output_dir,
        append_run_suffix=True,
    )


def build_energy_plot_filename(
    metric: str, view: str, role: str, room: str | None = None, time_window: dict | None = None
) -> str:
    """Baut konsistente Dateinamen fuer Heating-/Cooling-Zeitreihen."""
    if role == "rooms_separate":
        if view in {"bar", "year"}:
            return f"{metric}_{view}_rooms_separate.png"
        if time_window is None:
            raise ValueError("Fuer month/week/day wird ein time_window fuer den Dateinamen benoetigt.")
        return f"{metric}_{time_window['file_stub']}_rooms_separate.png"

    if room is None:
        raise ValueError("Fuer raumbezogene Dateinamen muss ein Raum uebergeben werden.")

    room_stub = sanitize_file_name(room)
    if role == "single":
        if view == "year":
            return f"{room_stub}_{metric}_year_single.png"
        if time_window is None:
            raise ValueError("Fuer month/week/day wird ein time_window fuer den Dateinamen benoetigt.")
        return f"{room_stub}_{metric}_{time_window['file_stub']}_single.png"

    if role == "variants_combined":
        if view == "year":
            return f"{room_stub}_{metric}_year_variants_combined.png"
        if time_window is None:
            raise ValueError("Fuer month/week/day wird ein time_window fuer den Dateinamen benoetigt.")
        return f"{room_stub}_{metric}_{time_window['file_stub']}_variants_combined.png"

    raise ValueError(f"Unbekannte Plot-Dateinamenrolle: {role}")
