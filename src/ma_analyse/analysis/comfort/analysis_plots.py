"""Analyseplots fuer Comfort-Zonenklassifizierung."""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from ..components.figures import get_figure_size_inches
from ..components.rooms import get_room_data_file
from ..components.runtime import annotate_timestamp
from ..components.variants import get_variant_display_name
from .data import load_room_csv
from .zones import COMFORT_HIGH, COMFORT_NORMAL, build_zone_masks, count_points_in_zone


def create_zone_plot(
    room_data, room_name, output_file, comfort_high_count, comfort_normal_count, outside_count, debug=False
):
    """Erstellt pro Raum einen Plot mit farblich getrennten Komfortklassen."""
    comfort_high_mask, comfort_normal_only_mask, outside_mask = build_zone_masks(room_data)
    total_points = len(room_data)

    def format_count_with_percentage(count):
        percentage = (count / total_points * 100) if total_points else 0.0
        return f"{count} ({percentage:.1f}%)"

    fig, ax = plt.subplots(figsize=get_figure_size_inches("comfort.plot_analysis.png", (8, 6)))

    ax.add_patch(
        Polygon(
            COMFORT_NORMAL,
            closed=True,
            alpha=0.12,
            facecolor="gold",
            edgecolor="orange",
            linewidth=1,
            label="noch Behaglich-Zone",
        )
    )
    ax.add_patch(
        Polygon(
            COMFORT_HIGH,
            closed=True,
            alpha=0.2,
            facecolor="green",
            edgecolor="darkgreen",
            linewidth=1,
            label="Behaglich-Zone",
        )
    )

    if outside_mask.any():
        pts = room_data.loc[outside_mask]
        ax.scatter(
            pts["top"],
            pts["relhum"],
            s=8,
            alpha=0.35,
            color="crimson",
            label=f"außerhalb beider Zonen: {format_count_with_percentage(outside_count)}",
        )

    if comfort_normal_only_mask.any():
        pts = room_data.loc[comfort_normal_only_mask]
        ax.scatter(
            pts["top"],
            pts["relhum"],
            s=8,
            alpha=0.35,
            color="goldenrod",
            label=f"noch Behaglich: {format_count_with_percentage(comfort_normal_count)}",
        )

    if comfort_high_mask.any():
        pts = room_data.loc[comfort_high_mask]
        ax.scatter(
            pts["top"],
            pts["relhum"],
            s=8,
            alpha=0.35,
            color="seagreen",
            label=f"Behaglich: {format_count_with_percentage(comfort_high_count)}",
        )

    ax.set_title(room_name, fontsize=12, fontweight="bold")
    ax.set_xlabel("Operative Temperatur (°C)")
    ax.set_ylabel("Relative Raumluftfeuchte (%)")
    ax.set_xlim(14, 38)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(loc="upper right", fontsize=8)

    summary_text = (
        f"Gesamt: {total_points}\n"
        f"Behaglich: {format_count_with_percentage(comfort_high_count)}\n"
        f"noch Behaglich: {format_count_with_percentage(comfort_normal_count)}\n"
        f"außerhalb: {format_count_with_percentage(outside_count)}"
    )
    ax.text(
        0.02,
        0.98,
        summary_text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85, "edgecolor": "lightgray"},
    )

    plt.tight_layout()
    annotate_timestamp(fig)
    plt.savefig(output_file, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    if debug:
        print(f"    + Zone-Plot gespeichert: {output_file}")


def create_analysis_overview_pdf(variant_data_dir, rooms, output_file, debug=False):
    """Erstellt PDF-Übersicht mit 5 Zone-Plots für eine Variante."""
    variant_name = get_variant_display_name(variant_data_dir)

    if debug:
        print(f"  Erstelle Analyse-Übersicht für Variante: {variant_name}")

    fig, axes = plt.subplots(1, 5, figsize=get_figure_size_inches("comfort.plot_analysis_overview.pdf", (28, 6.5)))
    fig.suptitle(
        f"Behaglichkeits-Analyse: {variant_name}\nOperative Temperatur vs. Relative Luftfeuchte mit Komfortzonen",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )

    for idx, room_name in enumerate(rooms):
        csv_file = get_room_data_file(variant_data_dir, room_name)
        ax = axes[idx]

        if debug:
            print(f"    Raum: {room_name}")

        if os.path.exists(csv_file):
            room_data = load_room_csv(csv_file, debug=debug)
            if room_data is not None and not room_data.empty:
                # Zone-Masken und Zählungen für diesen Raum berechnen
                comfort_high_mask, comfort_normal_only_mask, outside_mask = build_zone_masks(room_data)
                comfort_high_count = count_points_in_zone(room_data, COMFORT_HIGH)
                comfort_normal_count = count_points_in_zone(room_data, COMFORT_NORMAL)
                outside_count = int(outside_mask.sum())
                total_points = len(room_data)

                def format_count_with_percentage(count, total=total_points):
                    percentage = (count / total * 100) if total else 0.0
                    return f"{count} ({percentage:.1f}%)"

                # Zeichne Komfortzonen und Punkte direkt in das Subplot
                ax.add_patch(
                    Polygon(COMFORT_NORMAL, closed=True, alpha=0.12, facecolor="gold", edgecolor="orange", linewidth=1)
                )
                ax.add_patch(
                    Polygon(COMFORT_HIGH, closed=True, alpha=0.2, facecolor="green", edgecolor="darkgreen", linewidth=1)
                )

                if outside_mask.any():
                    pts = room_data.loc[outside_mask]
                    ax.scatter(pts["top"], pts["relhum"], s=5, alpha=0.35, color="crimson")

                if comfort_normal_only_mask.any():
                    pts = room_data.loc[comfort_normal_only_mask]
                    ax.scatter(pts["top"], pts["relhum"], s=5, alpha=0.35, color="goldenrod")

                if comfort_high_mask.any():
                    pts = room_data.loc[comfort_high_mask]
                    ax.scatter(pts["top"], pts["relhum"], s=5, alpha=0.35, color="seagreen")

                ax.set_title(f"{room_name}", fontsize=11, fontweight="bold")
                summary_text = (
                    f"Gesamt: {total_points}\n"
                    f"Behaglich: {format_count_with_percentage(comfort_high_count)}\n"
                    f"noch Behaglich: {format_count_with_percentage(comfort_normal_count)}\n"
                    f"außerhalb: {format_count_with_percentage(outside_count)}"
                )
                ax.text(
                    0.02,
                    0.98,
                    summary_text,
                    transform=ax.transAxes,
                    va="top",
                    ha="left",
                    fontsize=7,
                    bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85, "edgecolor": "lightgray"},
                )
            else:
                ax.text(
                    0.5,
                    0.5,
                    f"{room_name}\nKeine Daten",
                    ha="center",
                    va="center",
                    transform=ax.transAxes,
                    fontsize=10,
                    color="red",
                )
                ax.set_title(room_name, fontsize=11, fontweight="bold")
        else:
            ax.text(
                0.5,
                0.5,
                f"{room_name}\nDaten nicht gefunden",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=10,
                color="red",
            )
            ax.set_title(room_name, fontsize=11, fontweight="bold")
            if debug:
                print(f"    ✗ CSV nicht gefunden: {csv_file}")

        # Standardisierte Achsen für alle Plots
        ax.set_xlabel("Operative Temperatur (°C)", fontsize=9)
        ax.set_ylabel("Relative Raumluftfeuchte (%)", fontsize=9)
        ax.set_xlim(14, 38)
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3, linestyle="--")

    plt.tight_layout(rect=(0, 0, 1, 0.96))  # type: ignore
    annotate_timestamp(fig)
    plt.savefig(output_file, format="pdf", dpi=150)
    plt.close()
    print(f"    + Analyse-Übersicht erstellt: {output_file}")
