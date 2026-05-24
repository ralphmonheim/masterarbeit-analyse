"""Erzeugt Excel-Auswertungen aus aufbereiteten Simulationsdaten.

Eingaben:
    Raum-CSV-Dateien aus ``data/database/<Variante>_nutzdaten``.

Ausgaben:
    Excel-Dateien mit zusammengefassten Kennwerten. Im Modus ``compare`` wird
    eine gemeinsame Datei erzeugt, im Modus ``single`` eine Datei pro Variante.

Wichtige Annahmen:
    Die aktuell ausgewerteten Kennwerte sind zentral in ``METRIC_DEFINITIONS``
    definiert. Fehlende Spalten werden nicht als Fehler behandelt, sondern als
    leere Werte in der Ergebnisstruktur gefuehrt.
"""

import argparse
import os

import pandas as pd

from ..core.config import DATENBANK_DIR, ROOMS
from .components.rooms import get_room_data_file
from .components.runtime import build_named_run_output_dir, get_dated_output_prefix, get_run_id
from .components.variants import get_variant_display_name, normalize_variant_name
from .tables.excel_report import prepare_result_dataframe, summarize_room_metrics, write_excel_report


# ============================================================================
# Allgemeine Hilfsfunktionen
# ============================================================================
def parse_comma_separated_list(value):
    """Wandelt eine kommaseparierte CLI-Eingabe in eine Liste um."""
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def get_output_prefix(reference_time=None):
    """Erzeugt den Tagespraefix fuer Excel-Ausgabedateien und -ordner."""
    return get_dated_output_prefix("Dimensionierung", reference_time)


def build_run_output_dir(variant_dir, run_id, output_root=None):
    """Baut den Laufordner im Schema <output_root>/<variant_dir>/<run_id>."""
    return build_named_run_output_dir(str(variant_dir), run_id, output_root=output_root)


def find_variant_dirs(datenbank_dir, selected_variants=None):
    """Findet alle passenden Nutzdaten-Variantenordner."""
    """Findet Varianten in einem Datenbank-Verzeichnis."""
    if not os.path.isdir(datenbank_dir):
        return []

    entries = sorted(os.listdir(datenbank_dir))
    variants = []
    for entry in entries:
        path = os.path.join(datenbank_dir, entry)
        if os.path.isdir(path):
            variants.append((entry, path))

    if selected_variants is not None:
        normalized = {normalize_variant_name(v, "_nutzdaten") for v in selected_variants if v.strip()}
        variants = [(entry, path) for entry, path in variants if entry in normalized]

    return variants


def load_room_csv(csv_file):
    """Laedt eine Raum-CSV und gibt bei Fehlern eine leere Tabelle zurueck."""
    """Lädt eine Raum-CSV-Datei und konvertiert numerische Spalten."""
    try:
        df = pd.read_csv(csv_file)
    except Exception as exc:
        print(f"X Fehler beim Lesen der Datei {csv_file}: {exc}")
        return None

    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def build_excel_report(
    datenbank_dir,
    output_root=None,
    debug=False,
    run_id=None,
    selected_variants=None,
    rooms=None,
    variant_mode="compare",
):
    """Erstellt die Excel-Auswertung fuer die gewaehlten Varianten und Raeume."""
    """Erstellt eine Excel-Zusammenfassung für alle Varianten und Räume."""
    if rooms is None:
        rooms = ROOMS

    variants = find_variant_dirs(datenbank_dir, selected_variants=selected_variants)
    if not variants:
        # Wenn keine Unterordner vorhanden sind, verwende das Verzeichnis selbst als Variante.
        if os.path.isdir(datenbank_dir):
            variants = [(get_variant_display_name(datenbank_dir), datenbank_dir)]
        else:
            raise FileNotFoundError(f"Datenbank-Verzeichnis nicht gefunden: {datenbank_dir}")

    rows_by_variant = {}
    for variant_name, variant_path in variants:
        variant_display_name = get_variant_display_name(variant_name)
        if debug:
            print(f"Verarbeite Variante: {variant_display_name}")

        variant_rows = []
        for room_name in rooms:
            csv_file = get_room_data_file(variant_path, room_name)
            if not os.path.exists(csv_file):
                if debug:
                    print(f"  Raumdatei fehlt: {csv_file}")
                continue

            df_room = load_room_csv(csv_file)
            room_summary = summarize_room_metrics(df_room, variant_display_name, room_name)
            if room_summary is not None:
                variant_rows.append(room_summary)

        if variant_rows:
            rows_by_variant[variant_name] = variant_rows

    all_rows = [row for variant_rows in rows_by_variant.values() for row in variant_rows]

    if not all_rows:
        raise ValueError("Keine Raumdaten gefunden. Bitte prüfen Sie das Datenbank-Verzeichnis.")

    resolved_run_id = get_run_id(command_name="excel-analysis", run_id=run_id)
    output_prefix = get_output_prefix()

    if variant_mode == "single":
        output_files = []
        for variant_name, variant_rows in rows_by_variant.items():
            result_df = prepare_result_dataframe(variant_rows)
            variant_display_name = get_variant_display_name(variant_name)
            run_output_dir = build_run_output_dir(variant_name, resolved_run_id, output_root=output_root)
            output_file = write_excel_report(
                result_df,
                run_output_dir,
                f"{get_dated_output_prefix(variant_display_name)}_analysis.xlsx",
            )
            output_files.append(output_file)
            if debug:
                print(f"Excel-Bericht erzeugt: {output_file}")
        return output_files

    result_df = prepare_result_dataframe(all_rows)
    run_output_dir = build_run_output_dir("analyze_simulation", resolved_run_id, output_root=output_root)
    output_file = write_excel_report(result_df, run_output_dir, f"{output_prefix}_analysis.xlsx")

    if debug:
        print(f"Excel-Bericht erzeugt: {output_file}")

    return output_file


def main():
    """CLI-Einstiegspunkt fuer ``analyze_data``."""
    parser = argparse.ArgumentParser(description="Analysiert Simulationsergebnisse und erzeugt eine Excel-Ausgabe.")
    parser.add_argument(
        "--datenbank-dir",
        default=DATENBANK_DIR,
        help="Verzeichnis mit aufbereiteten Raum-CSV-Dateien (default: data/database)",
    )
    parser.add_argument(
        "--output-root", default=None, help="Wurzelverzeichnis für die Excel-Ausgabe (default: data/output)"
    )
    parser.add_argument("--run-id", default=None, help="Optionale Lauf-ID für die Ausgabestruktur")
    parser.add_argument(
        "--variants",
        type=parse_comma_separated_list,
        default=None,
        help="Komma-getrennte Liste von Varianten ohne Suffix, z. B. 101 lobby,109 office",
    )
    parser.add_argument(
        "--rooms", type=parse_comma_separated_list, default=None, help="Komma-getrennte Liste von Räumen"
    )
    parser.add_argument(
        "--variant-mode",
        choices=["single", "compare"],
        default=None,
        help="Ausgabemodus: compare erzeugt eine gemeinsame Excel, single eine Excel pro Variante",
    )
    parser.add_argument(
        "--series-layout",
        choices=["separate", "combined"],
        default=None,
        help="Excel-Ausgabe: separate erzeugt eine Excel pro Variante, combined eine gemeinsame Excel",
    )
    parser.add_argument("--debug", action="store_true", help="Aktiviert Debug-Ausgaben")
    args = parser.parse_args()
    if args.series_layout == "separate":
        variant_mode = "single"
    elif args.series_layout == "combined":
        variant_mode = "compare"
    else:
        variant_mode = args.variant_mode or "single"

    output_file = build_excel_report(
        args.datenbank_dir,
        output_root=args.output_root,
        debug=args.debug,
        run_id=args.run_id,
        selected_variants=args.variants,
        rooms=args.rooms,
        variant_mode=variant_mode,
    )
    if isinstance(output_file, list):
        for file_path in output_file:
            print(f"Excel-Ausgabe erstellt: {file_path}")
    else:
        print(f"Excel-Ausgabe erstellt: {output_file}")


if __name__ == "__main__":
    main()
