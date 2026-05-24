"""Einzel- und Uebersichtsplots fuer Comfort-Auswertungen."""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Polygon

from ..components.figures import get_figure_size_inches
from ..components.rooms import get_room_data_file
from ..components.runtime import annotate_timestamp
from ..components.variants import get_variant_display_name
from .data import load_room_csv
from .zones import COMFORT_HIGH, COMFORT_NORMAL


def create_scatter_plot(room_data, room_name, ax):
    """Zeichnet einen Comfort-Scatterplot mit Komfortzonen in eine Achse."""
    """Erstellt Scatterplot für einen Raum mit Komfortzonen."""
    if room_data is None or room_data.empty:
        ax.text(
            0.5,
            0.5,
            f"{room_name}\nKeine Daten verfügbar",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=10,
            color="red",
        )
        ax.set_title(room_name, fontsize=11, fontweight="bold")
        ax.set_xlabel("Operative Temperatur (°C)")
        ax.set_ylabel("Relative Raumluftfeuchte (%)")
        ax.grid(True, alpha=0.3, linestyle="--")
        return

    # Zeichne Komfortzonen
    poly_normal = Polygon(
        COMFORT_NORMAL,
        closed=True,
        alpha=0.15,
        facecolor="yellow",
        edgecolor="orange",
        label="noch Behaglich",
        linewidth=1,
    )
    poly_high = Polygon(
        COMFORT_HIGH, closed=True, alpha=0.3, facecolor="green", edgecolor="darkgreen", label="Behaglich", linewidth=1
    )
    ax.add_patch(poly_normal)  # Zuerst zeichnen (Hintergrund)
    ax.add_patch(poly_high)  # Dann zeichnen (Vordergrund)

    # Scatterplot
    sns.scatterplot(
        data=room_data,
        x="top",
        y="relhum",
        alpha=0.3,
        s=5,
        color="steelblue",
        label="Messdaten",
        ax=ax,
        zorder=10,
        edgecolor=None,
    )
    ax.set_title(f"{room_name}", fontsize=11, fontweight="bold")
    ax.set_xlabel("Operative Temperatur (°C)", fontsize=9)
    ax.set_ylabel("Relative Raumluftfeuchte (%)", fontsize=9)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(loc="upper right", fontsize=8)

    # Achsen-Limits mit flexibler Anpassung
    x_min, x_max = 14, 38
    y_min, y_max = 0, 100

    # Wenn Daten außerhalb der vorgesehenen Bereiche liegen, anpassen
    if room_data["top"].min() < x_min:
        x_min = room_data["top"].min() - 1
    if room_data["top"].max() > x_max:
        x_max = room_data["top"].max() + 1
    if room_data["relhum"].min() < y_min:
        y_min = room_data["relhum"].min() - 5
    if room_data["relhum"].max() > y_max:
        y_max = room_data["relhum"].max() + 5

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)


def create_room_plot(room_data, room_name, output_file, debug=False):
    """Erstellt ein Raumdiagramm und speichert es als PNG."""
    if debug:
        print(f"    Erstelle Diagramm für {room_name}")

    fig, ax = plt.subplots(figsize=get_figure_size_inches("comfort.plot.png", (8, 6)))
    create_scatter_plot(room_data, room_name, ax)

    plt.tight_layout()
    annotate_timestamp(fig)
    # Konkrete Dateiablage je Raum. Das Ziel wird in process_all_variants
    # aus Laufordner + Variante + Dateiname aufgebaut.
    plt.savefig(output_file, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    if debug:
        print(f"      + PNG gespeichert: {output_file}")


def create_overview_pdf(variant_data_dir, rooms, output_file, debug=False):
    """Erstellt PDF-Übersicht mit 5 Behaglichkeitsdiagrammen für eine Variante."""
    variant_name = get_variant_display_name(variant_data_dir)

    if debug:
        print(f"  Erstelle PDF-Übersicht für Variante: {variant_name}")

    fig, axes = plt.subplots(1, 5, figsize=get_figure_size_inches("comfort.plot_overview.pdf", (28, 6.5)))
    fig.suptitle(
        f"Behaglichkeitsanalyse: {variant_name}\nOperative Temperatur vs. Relative Luftfeuchte",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )

    for idx, room_name in enumerate(rooms):
        csv_file = get_room_data_file(variant_data_dir, room_name)

        if debug:
            print(f"    Raum: {room_name}")

        if os.path.exists(csv_file):
            room_data = load_room_csv(csv_file, debug=debug)
            create_scatter_plot(room_data, room_name, axes[idx])
        else:
            axes[idx].text(
                0.5,
                0.5,
                f"{room_name}\nDaten nicht gefunden",
                ha="center",
                va="center",
                transform=axes[idx].transAxes,
                fontsize=10,
                color="red",
            )
            axes[idx].set_title(room_name, fontsize=11, fontweight="bold")
            if debug:
                print(f"  X CSV nicht gefunden: {csv_file}")

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # type: ignore
    annotate_timestamp(plt.gcf())
    plt.savefig(output_file, format="pdf", dpi=150)
    plt.close()
    print(f"    + PDF-Übersicht erstellt: {output_file}")
