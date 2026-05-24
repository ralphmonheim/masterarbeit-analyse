"""Erzeugt Comfort- und Behaglichkeitsdiagramme aus Raumdaten.

Eingaben:
    Aufbereitete Raum-CSV-Dateien aus ``1_Datenbank/<Variante>_nutzdaten``.

Ausgaben:
    Einzelraum-PNGs, PDF-Uebersichten und Analyseausgaben mit Komfortzonen.

Wichtige Annahmen:
    Comfort-Plots benoetigen operative Temperatur ``top`` und relative
    Luftfeuchte ``relhum``. Falls die Spalten aus ``prepare_data`` anders
    benannt sind, werden sie ueber ``PLOT_COLUMN_ALIASES`` zugeordnet.
"""

import argparse
import os
from datetime import datetime

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import importlib.util
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Polygon
from matplotlib.path import Path as MplPath


def load_output_format_helpers():
    """Laedt die zentrale Formatkonfiguration aus dem Unterstuetzung-Ordner."""
    helper_path = Path(__file__).resolve().parent / "Unterstützung" / "output_format_settings.py"
    spec = importlib.util.spec_from_file_location("support_output_format_settings", helper_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Ausgabeformat-Helfer konnten nicht geladen werden: {helper_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


OUTPUT_FORMATS = load_output_format_helpers()
get_figure_size_inches = OUTPUT_FORMATS.get_figure_size_inches

# ============================================================================
# Konfiguration
# ============================================================================
ROOMS = ["101 lobby", "109 office", "113 meeting", "208 office", "214 meeting"]

DATENBANK_DIR = "1_Datenbank"
# Zentrales Ausgabe-Root für alle erzeugten Bilddateien.
# Darunter wird automatisch pro Skriptlauf ein eigener Unterordner angelegt,
# damit alte Ergebnisse nicht überschrieben werden.
OUTPUT_DIR = "2_Output"
# Variantenbezogene Laufordner im Output enden konsistent auf "_output".
RUN_FOLDER_SUFFIX = "_output"
# Unterordner für Behaglichkeits-Analyse-Plots innerhalb des Laufordners.
PLOT_SUBDIR_ANALYSIS = "analysis"
REQUIRED_PLOT_COLUMNS = ["top", "relhum"]
ROOM_FILE_EXTENSION = ".csv"
PLOT_COLUMN_ALIASES = {
    "top": ["local_de_comf_diag_t_top", "temperatures_top", "top"],
    "relhum": ["iaq_relhum", "relhum"],
}

# ============================================================================
# Komfortzonen
# ============================================================================
# Eckpunkte: [operative Temperatur °C, relative Luftfeuchte %]
COMFORT_HIGH = [[17.8, 72.0], [22.0, 66.5], [23.8, 33.5], [18.4, 40.0]]

COMFORT_NORMAL = [
    [17.0, 85.5],
    [20.3, 80.0],
    [24.7, 60.0],
    [26.8, 29.0],
    [25.9, 20.0],
    [19.9, 20.0],
    [17.0, 34.5],
    [16.0, 74.0],
]


# ============================================================================
# Allgemeine Hilfsfunktionen und Datenzugriff
# ============================================================================
def get_room_data_file(variant_dir, room_name):
    """Liefert den Dateipfad zur aufbereiteten Raum-CSV-Datei."""
    return os.path.join(variant_dir, f"{room_name.replace(' ', '_')}{ROOM_FILE_EXTENSION}")


def annotate_timestamp(fig, timestamp=None):
    """Fügt einen Erstellungszeitstempel unten rechts auf der Figur ein."""
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


def load_room_csv(csv_file, debug=False):
    """Lädt aufbereitete CSV-Datei eines Raumes."""
    try:
        df = pd.read_csv(csv_file)

        # Neue Header aus prepare_data.py auf die erwarteten Plotspalten abbilden.
        for target_column in REQUIRED_PLOT_COLUMNS:
            if target_column in df.columns:
                continue
            for candidate in PLOT_COLUMN_ALIASES.get(target_column, []):
                if candidate in df.columns:
                    df[target_column] = df[candidate]
                    break

        missing_columns = [col for col in REQUIRED_PLOT_COLUMNS if col not in df.columns]
        if missing_columns:
            print(f"    X Fehlende Spalten in {csv_file}: {missing_columns}")
            return None

        # Robuste numerische Konvertierung, damit fehlerhafte Zeilen den Plot nicht abbrechen.
        for column in REQUIRED_PLOT_COLUMNS:
            df[column] = pd.to_numeric(df[column], errors="coerce")
        df = df.dropna(subset=REQUIRED_PLOT_COLUMNS)

        if debug:
            print(f"    + Geladen: {len(df)} Datenpunkte")
        return df
    except Exception as e:
        print(f"    X Fehler beim Lesen {csv_file}: {e}")
        return None


def get_output_prefix(reference_time=None):
    """Erzeugt den Tagespräfix für Ausgabedateien und -ordner."""
    if reference_time is None:
        reference_time = datetime.now()
    return f"{reference_time.strftime('%y%m%d')}_Dimensionierung"


def get_run_id(command_name=None, run_id=None):
    """Gibt eine bestehende Lauf-ID zurück oder erzeugt eine neue mit Befehlsnamen."""
    if run_id:
        return run_id

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    if command_name:
        return f"{timestamp}_{command_name}"
    return timestamp


def ensure_output_run_suffix(run_id):
    """Ergaenzt das Standardsuffix fuer Varianten-Laufordner genau einmal."""
    if run_id.endswith(RUN_FOLDER_SUFFIX):
        return run_id
    return f"{run_id}{RUN_FOLDER_SUFFIX}"


def build_run_output_dir(variant_dir, run_id, output_root=None):
    """Baut den Laufordner im Schema <output_root>/<variant_dir>/<run_id>."""
    # Falls kein eigenes Root übergeben wird, schreiben wir standardmäßig in 2_Output/.
    # Die Variante liegt jetzt direkt unter 2_Output/, der konkrete Lauf darunter.
    # Dadurch wird die Struktur kuerzer: 2_Output/<variante>/<run_id>/...
    base_output_dir = output_root if output_root else OUTPUT_DIR
    return os.path.join(
        base_output_dir,
        get_variant_display_name(variant_dir),
        ensure_output_run_suffix(run_id),
    )


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


def normalize_variant_name(variant_name, suffix):
    """Ergaenzt den erwarteten Datenordner-Suffix, falls er fehlt."""
    if variant_name.endswith(suffix):
        return variant_name
    return f"{variant_name}{suffix}"


def strip_variant_suffix(variant_name):
    """Entfernt bekannte Varianten-Suffixe fuer lesbare Anzeigenamen."""
    for suffix in ("_rohdaten", "_nutzdaten"):
        if variant_name.endswith(suffix):
            return variant_name[: -len(suffix)]
    return variant_name


def get_variant_display_name(variant_name):
    """Gibt den kurzen Anzeigenamen einer Variante oder eines Pfads zurueck."""
    return strip_variant_suffix(Path(variant_name).name)


def get_available_variant_dirs(datenbank_dir, debug=False, selected_variants=None):
    """Findet Nutzdatenordner, optional begrenzt auf ausgewaehlte Varianten."""
    """Liefert alle verfügbaren Nutzdaten-Ordner oder nur die ausgewählten."""
    if not os.path.exists(datenbank_dir):
        return []

    all_dirs = [d for d in os.listdir(datenbank_dir) if os.path.isdir(os.path.join(datenbank_dir, d))]
    all_variants = sorted([d for d in all_dirs if d.endswith("_nutzdaten")])

    if selected_variants is not None:
        normalized = [normalize_variant_name(v, "_nutzdaten") for v in selected_variants]
        variant_dirs = [v for v in normalized if v in all_variants]
    else:
        variant_dirs = all_variants

    if debug:
        print(f"\nGefundene Nutzdaten-Varianten: {[get_variant_display_name(v) for v in all_variants]}")
        if selected_variants is not None:
            print(f"Ausgewählte Varianten: {[get_variant_display_name(v) for v in variant_dirs]}")

    return variant_dirs


def get_latest_variant_dirs(datenbank_dir, debug=False):
    """Waehlt aus Kompatibilitaetsgruenden nur den aktuellsten Nutzdatenordner."""
    """Liefert den aktuellsten Nutzdaten-Ordner als Liste mit einem Eintrag."""
    variant_dirs = get_available_variant_dirs(datenbank_dir, debug=debug)
    if not variant_dirs:
        print(f"X Keine Varianten-Ordner in {datenbank_dir} gefunden")
        return []

    latest_variant_dir = max(variant_dirs, key=lambda d: os.path.getmtime(os.path.join(datenbank_dir, d)))

    if debug:
        print('Hinweis: Nur Ordner mit "_nutzdaten" werden verwendet')
        print(f"Verwendet wird nur der aktuellste Datensatz: {get_variant_display_name(latest_variant_dir)}\n")

    return [latest_variant_dir]


def process_plots(
    datenbank_dir, rooms, run_id=None, output_root=None, variant_dirs=None, debug=False, output_subdir=None
):
    """Erzeugt einzelne Comfort-PNGs fuer die ausgewaehlten Varianten/Raeume."""
    """Erstellt und speichert Raumdiagramme als PNG."""
    if not os.path.exists(datenbank_dir):
        print(f"✗ Verzeichnis mit aufbereiteten Daten nicht gefunden: {datenbank_dir}")
        print("  Führen Sie zuerst 'prepare_data.py' aus!")
        return

    print("=" * 70)
    print("BEHAGLICHKEITSANALYSE - Einzelne Raumdiagramme (PNG)")
    print("=" * 70)

    selected_variant_dirs = (
        get_available_variant_dirs(datenbank_dir, debug=debug, selected_variants=variant_dirs)
        if variant_dirs is not None
        else get_latest_variant_dirs(datenbank_dir, debug=debug)
    )
    if not selected_variant_dirs:
        return

    # output_prefix wird Bestandteil des Dateinamens jedes PNGs.
    # Beispiel: 260328_Dimensionierung_101_lobby.png
    output_prefix = get_output_prefix()

    # run_id trennt verschiedene Ausführungen voneinander.
    # Ohne Übergabe wird eine neue Zeitstempel-ID erzeugt.
    resolved_run_id = get_run_id(command_name="plots", run_id=run_id)

    created_count = 0
    skipped_count = 0
    missing_input_count = 0

    for variant_dir in selected_variant_dirs:
        variant_path = os.path.join(datenbank_dir, variant_dir)
        variant_display_name = get_variant_display_name(variant_dir)

        # Neue, kompaktere Struktur:
        # 2_Output/<variant_dir>/<run_id>/
        run_output_dir = build_run_output_dir(variant_dir, resolved_run_id, output_root=output_root)
        os.makedirs(run_output_dir, exist_ok=True)

        # Variante-spezifische Ablage optional in einem Unterordner.
        # Standard: direkt im Laufordner.
        # Für den Sammelbefehl "all" kann hier z. B. "plots" übergeben werden.
        output_dir = os.path.join(run_output_dir, output_subdir) if output_subdir else run_output_dir
        os.makedirs(output_dir, exist_ok=True)

        if debug:
            print(f"\nVariante: {variant_display_name}")

        print(f"Run-ID: {resolved_run_id}")
        print(f"Output-Basis: {os.path.abspath(run_output_dir)}")

        # Erstelle PNGs für jeden Raum
        for room_name in rooms:
            csv_file = get_room_data_file(variant_path, room_name)

            if debug:
                print(f"  Raum: {room_name}")

            if os.path.exists(csv_file):
                room_data = load_room_csv(csv_file, debug=debug)
                if room_data is not None and not room_data.empty:
                    # Dateiname bleibt bewusst sprechend und stabil:
                    # <tagesprefix>_<raum>.png
                    # So sind Dateien auch ohne Blick in Unterordner eindeutig.
                    png_output = os.path.join(output_dir, f"{output_prefix}_{room_name.replace(' ', '_')}.png")
                    if os.path.exists(png_output):
                        # Bereits vorhandene Dateien werden nicht überschrieben,
                        # damit Wiederholungsläufe idempotent bleiben.
                        skipped_count += 1
                        if debug:
                            print(f"    - SKIP (existiert bereits): {png_output}")
                    else:
                        create_room_plot(room_data, room_name, png_output, debug=debug)
                        created_count += 1
                elif debug:
                    print(f"    X Keine gueltigen Daten nach Bereinigung: {csv_file}")
            else:
                missing_input_count += 1
                if debug:
                    print(f"    X CSV nicht gefunden: {csv_file}")

        print("=" * 70)
        print(f"Variante abgeschlossen: {variant_display_name}")
        print(f"Ablage: {os.path.abspath(output_dir)}")
        print("=" * 70)

    print(
        f"Zusammenfassung: diagramme_erzeugt={created_count}, uebersprungen={skipped_count}, fehlende_inputs={missing_input_count}"
    )


def process_overview(datenbank_dir, rooms, run_id=None, output_root=None, variant_dirs=None, debug=False):
    """Erzeugt PDF-Uebersichten der Comfort-Scatterplots."""
    """Erstellt und speichert Behaglichkeits-Übersichten als PDF."""
    if not os.path.exists(datenbank_dir):
        print(f"X Verzeichnis mit aufbereiteten Daten nicht gefunden: {datenbank_dir}")
        print("  Führen Sie zuerst 'prepare_data.py' aus!")
        return

    print("=" * 70)
    print("BEHAGLICHKEITSANALYSE - PDF-Übersichten")
    print("=" * 70)

    selected_variant_dirs = (
        get_available_variant_dirs(datenbank_dir, debug=debug, selected_variants=variant_dirs)
        if variant_dirs is not None
        else get_latest_variant_dirs(datenbank_dir, debug=debug)
    )
    if not selected_variant_dirs:
        return

    output_prefix = get_output_prefix()
    resolved_run_id = get_run_id(command_name="overview", run_id=run_id)
    created_count = 0
    skipped_count = 0

    for variant_dir in selected_variant_dirs:
        variant_path = os.path.join(datenbank_dir, variant_dir)
        variant_display_name = get_variant_display_name(variant_dir)

        # Neue, kompaktere Struktur:
        # 2_Output/<variant_dir>/<run_id>/
        run_output_dir = build_run_output_dir(variant_dir, resolved_run_id, output_root=output_root)
        os.makedirs(run_output_dir, exist_ok=True)

        # PDF wird direkt im Variantenordner abgelegt.
        output_dir = run_output_dir
        os.makedirs(output_dir, exist_ok=True)

        print(f"Run-ID: {resolved_run_id}")
        print(f"Output-Basis: {os.path.abspath(run_output_dir)}")

        # output_file = os.path.join(output_dir, f'{output_prefix}_{variant_dir}_plots_uebersicht.pdf')
        output_file = os.path.join(output_dir, f"{output_prefix}_plots_uebersicht.pdf")

        if debug:
            print(f"\nVariante: {variant_display_name}")
            print(f"  Output-Verzeichnis: {output_dir}")

        if os.path.exists(output_file):
            skipped_count += 1
            if debug:
                print(f"    - SKIP (existiert bereits): {output_file}")
        else:
            create_overview_pdf(variant_path, rooms, output_file, debug=debug)
            created_count += 1

    print("=" * 70)
    print("Alle PDF-Übersichten gespeichert")
    print(f"Zusammenfassung: erstellt={created_count}, uebersprungen={skipped_count}")
    print("=" * 70)


# ============================================================================
# Komfortzonen-Analyse
# ============================================================================


def count_points_in_zone(room_data, polygon_points):
    """Zählt Messpunkte, die innerhalb eines Polygons liegen."""
    polygon = MplPath(polygon_points)
    measurement_points = room_data[["top", "relhum"]].to_numpy()
    return int(polygon.contains_points(measurement_points).sum())


def build_zone_masks(room_data):
    """Erzeugt Masken für Behaglich, noch Behaglich und außerhalb beider Zonen."""
    measurement_points = room_data[["top", "relhum"]].to_numpy()
    comfort_high_mask = MplPath(COMFORT_HIGH).contains_points(measurement_points)
    comfort_normal_mask = MplPath(COMFORT_NORMAL).contains_points(measurement_points)
    comfort_normal_only_mask = comfort_normal_mask & ~comfort_high_mask
    outside_mask = ~(comfort_high_mask | comfort_normal_mask)
    return comfort_high_mask, comfort_normal_only_mask, outside_mask


def build_analysis_table(results):
    """Baut die Analyse-Tabelle inklusive Prozentanteilen je Kategorie."""
    analysis_table = pd.DataFrame(results)
    if analysis_table.empty:
        return analysis_table

    total_points = analysis_table["messpunkte_gesamt"].replace(0, pd.NA)
    analysis_table["anteil_behaglich_prozent"] = (
        (analysis_table["messpunkte_behaglich"] / total_points * 100).fillna(0.0).round(1)
    )
    analysis_table["anteil_noch_behaglich_prozent"] = (
        (analysis_table["messpunkte_noch_behaglich"] / total_points * 100).fillna(0.0).round(1)
    )
    analysis_table["anteil_ausserhalb_prozent"] = (
        (analysis_table["messpunkte_ausserhalb"] / total_points * 100).fillna(0.0).round(1)
    )
    return analysis_table


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


def process_analysis(
    datenbank_dir,
    rooms,
    run_id=None,
    output_root=None,
    variant_dirs=None,
    debug=False,
    output_individual=True,
    output_overview=True,
    output_excel=True,
):
    """Erzeugt Analyseplots, Analyseuebersichten und Excel-Tabellen."""
    """Erstellt Behaglichkeits-Analyse und Zoneplots pro Raum."""
    if not os.path.exists(datenbank_dir):
        print(f"X Verzeichnis mit aufbereiteten Daten nicht gefunden: {datenbank_dir}")
        return None

    print("=" * 70)
    print("BEHAGLICHKEITSANALYSE - Analyse")
    print("=" * 70)

    selected_variant_dirs = (
        get_available_variant_dirs(datenbank_dir, debug=debug, selected_variants=variant_dirs)
        if variant_dirs is not None
        else get_latest_variant_dirs(datenbank_dir, debug=debug)
    )
    if not selected_variant_dirs:
        return None

    resolved_run_id = get_run_id(command_name="analysis", run_id=run_id)
    output_prefix = get_output_prefix()
    all_results = []

    for variant_dir in selected_variant_dirs:
        variant_path = os.path.join(datenbank_dir, variant_dir)
        variant_display_name = get_variant_display_name(variant_dir)
        run_output_dir = build_run_output_dir(variant_dir, resolved_run_id, output_root=output_root)
        output_dir = os.path.join(run_output_dir, PLOT_SUBDIR_ANALYSIS)
        os.makedirs(output_dir, exist_ok=True)

        print(f"Verwendeter Datensatz: {variant_display_name}")
        print(f"Run-ID: {resolved_run_id}")
        print(f"Plot-Ablage: {os.path.abspath(output_dir)}")

        for room_name in rooms:
            csv_file = get_room_data_file(variant_path, room_name)
            if debug:
                print(f"\nRaum: {room_name}")
            if not os.path.exists(csv_file):
                print(f"  ✗ CSV nicht gefunden: {csv_file}")
                continue
            room_data = load_room_csv(csv_file, debug=debug)
            if room_data is None or room_data.empty:
                continue

            comfort_high_mask, _, outside_mask = build_zone_masks(room_data)
            comfort_high_count = count_points_in_zone(room_data, COMFORT_HIGH)
            comfort_normal_count = count_points_in_zone(room_data, COMFORT_NORMAL)
            outside_count = int(outside_mask.sum())

            all_results.append(
                {
                    "raum": room_name,
                    "messpunkte_gesamt": len(room_data),
                    "messpunkte_behaglich": comfort_high_count,
                    "messpunkte_noch_behaglich": comfort_normal_count,
                    "messpunkte_ausserhalb": outside_count,
                }
            )

            if output_individual:
                plot_file = os.path.join(output_dir, f"{output_prefix}_{room_name.replace(' ', '_')}_analysis.png")
                create_zone_plot(
                    room_data,
                    room_name,
                    plot_file,
                    comfort_high_count,
                    comfort_normal_count,
                    outside_count,
                    debug=debug,
                )

        overview_output_file = os.path.join(run_output_dir, f"{output_prefix}_analyse_uebersicht.pdf")
        if output_overview:
            if debug:
                print("\n  Erstelle Analyse-Übersicht...")
            create_analysis_overview_pdf(variant_path, rooms, overview_output_file, debug=debug)

        if output_excel:
            analysis_table = build_analysis_table(all_results)
            analysis_table_output_file = os.path.join(run_output_dir, f"{output_prefix}_analysis_table.xlsx")
            analysis_table.to_excel(analysis_table_output_file, index=False)
            print(f"    + Analyse-Tabelle erstellt: {analysis_table_output_file}")

    if not all_results:
        return None

    return build_analysis_table(all_results)


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
    """Uebersetzt den Comfort-Unterbefehl in Pipeline-Schritte und Ausgaben."""
    if output_type not in COMFORT_OUTPUT_TYPES:
        raise ValueError(f"Ungültiger output_type: {output_type}. Erwartet: {', '.join(COMFORT_OUTPUT_TYPES)}")
    return COMFORT_OUTPUT_TYPES[output_type]


def run_comfort(args):
    """Fuehrt den Comfort-Befehl entsprechend der CLI-Optionen aus."""
    output_type = getattr(args, "output_type", "plot_analysis_overview")
    settings = get_comfort_output_settings(output_type)

    # Führe die entsprechenden Schritte aus
    if "plots" in settings["steps"]:
        process_plots(
            datenbank_dir=args.datenbank_dir,
            rooms=ROOMS,
            run_id=args.run_id,
            output_root=args.output_root,
            variant_dirs=None,  # oder aus args, falls vorhanden
            debug=args.debug,
        )
    if "overview" in settings["steps"]:
        process_overview(
            datenbank_dir=args.datenbank_dir,
            rooms=ROOMS,
            run_id=args.run_id,
            output_root=args.output_root,
            variant_dirs=None,
            debug=args.debug,
        )
    if "analysis" in settings["steps"]:
        result = process_analysis(
            datenbank_dir=args.datenbank_dir,
            rooms=ROOMS,
            run_id=args.run_id,
            output_root=args.output_root,
            variant_dirs=None,
            debug=args.debug,
            output_individual=settings["analysis_individual"],
            output_overview=settings["analysis_overview"],
            output_excel=True,  # Standardmäßig Excel ausgeben
        )
        if result is not None:
            print(result.to_string(index=False))


def parse_args():
    """Definiert die CLI fuer Comfort-Ausgaben."""
    parser = argparse.ArgumentParser(description="Erstellt einzelne Raumplots oder eine PDF-Übersicht aus Nutzdaten.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--datenbank-dir", default=DATENBANK_DIR, help="Verzeichnis mit aufbereiteten Daten (default: 1_Datenbank)"
    )
    common.add_argument("--run-id", default=None, help="Optionale Lauf-ID, z. B. 2026-03-28_153000")
    common.add_argument(
        "--output-root", default=None, help="Optionales Output-Root; ohne Angabe wird 2_Output verwendet"
    )
    common.add_argument("--debug", dest="debug", action="store_true", help="Aktiviert Debug-Ausgaben")
    common.add_argument("--no-debug", dest="debug", action="store_false", help="Deaktiviert Debug-Ausgaben")

    comfort_parser = subparsers.add_parser(
        "comfort",
        parents=[common],
        help="Erstellt Komfortausgaben: plot, overview, analysis oder Kombinationen",
    )
    comfort_parser.add_argument(
        "--output-type",
        choices=["plot", "plot_overview", "plot_analysis", "plot_analysis_overview"],
        default="plot_analysis_overview",
        help="Wählt das Komfort-Ausgabeprofil aus",
    )
    comfort_parser.set_defaults(debug=True)

    return parser.parse_args()


# ============================================================================
# CLI-Einstiegspunkt
# ============================================================================
if __name__ == "__main__":
    args = parse_args()
    run_comfort(args)
