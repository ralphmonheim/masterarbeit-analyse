"""Erzeugt Comfort- und Behaglichkeitsdiagramme aus Raumdaten.

Eingaben:
    Aufbereitete Raum-CSV-Dateien aus ``data/ma_analyse/database/<Variante>_nutzdaten``.

Ausgaben:
    Einzelraum-PNGs, PDF-Uebersichten und Analyseausgaben mit Komfortzonen.

Wichtige Annahmen:
    Comfort-Plots benoetigen operative Temperatur ``top`` und relative
    Luftfeuchte ``relhum``. Falls die Spalten aus ``prepare`` anders
    benannt sind, werden sie ueber ``PLOT_COLUMN_ALIASES`` zugeordnet.
"""

import argparse
import os

from ...core.config import DATENBANK_DIR, ROOMS
from ..components.rooms import get_room_data_file
from ..components.runtime import build_variant_run_output_dir, get_dated_output_prefix, get_run_id
from ..components.variants import get_variant_display_name, normalize_variant_name
from .analysis_plots import create_analysis_overview_pdf, create_zone_plot
from .data import load_room_csv
from .plots import create_overview_pdf, create_room_plot
from .tables import build_analysis_table
from .zones import COMFORT_HIGH, COMFORT_NORMAL, build_zone_masks, count_points_in_zone

# ============================================================================
# Konfiguration
# ============================================================================
# Zentrales Ausgabe-Root für alle erzeugten Bilddateien.
# Darunter wird automatisch pro Skriptlauf ein eigener Unterordner angelegt,
# damit alte Ergebnisse nicht überschrieben werden.
# Variantenbezogene Laufordner im Output enden konsistent auf "_output".
# Unterordner für Behaglichkeits-Analyse-Plots innerhalb des Laufordners.
PLOT_SUBDIR_ANALYSIS = "analysis"


# ============================================================================
# Allgemeine Hilfsfunktionen und Datenzugriff
# ============================================================================
def get_output_prefix(reference_time=None):
    """Erzeugt den Tagespraefix fuer Comfort-Ausgabedateien und -ordner."""
    return get_dated_output_prefix("Dimensionierung", reference_time)


def build_run_output_dir(variant_dir, run_id, output_root=None):
    """Baut den Laufordner im Schema <output_root>/<variante>/<run_id>_output."""
    return build_variant_run_output_dir(variant_dir, run_id, output_root=output_root)


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
        print("  Führen Sie zuerst 'python -m ma_analyse prepare' aus!")
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
        # data/ma_analyse/output/<variant_dir>/<run_id>/
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
        print("  Führen Sie zuerst 'python -m ma_analyse prepare' aus!")
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
        # data/ma_analyse/output/<variant_dir>/<run_id>/
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
        "--datenbank-dir", default=DATENBANK_DIR, help="Verzeichnis mit aufbereiteten Daten (default: data/ma_analyse/database)"
    )
    common.add_argument("--run-id", default=None, help="Optionale Lauf-ID, z. B. 2026-03-28_153000")
    common.add_argument(
        "--output-root", default=None, help="Optionales Output-Root; ohne Angabe wird data/ma_analyse/output verwendet"
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
