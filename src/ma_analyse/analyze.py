"""Erzeugt Excel-Auswertungen aus aufbereiteten Simulationsdaten.

Eingaben:
    Raum-CSV-Dateien aus ``1_Datenbank/<Variante>_nutzdaten``.

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
from datetime import datetime
from pathlib import Path

import pandas as pd

from .config import DATENBANK_DIR, OUTPUT_DIR, ROOM_FILE_EXTENSION, ROOMS

PLOT_SUBDIR_EXCEL = "excel"

# Metriken, die derzeit standardmäßig aus den Raum-CSV-Dateien extrahiert werden.
# Spaltennamen können später ergänzt oder angepasst werden.
# Die Ausgabe wird als breite Tabelle erzeugt, damit die Struktur nachträglich leichter geändert werden kann.
METRIC_DEFINITIONS = {
    "max_q_heat": ("zone_energy_q_heat", "max"),
    "min_q_heat": ("zone_energy_q_heat", "min"),
    "max_q_cool": ("zone_energy_q_cool", "max"),
    "min_q_cool": ("zone_energy_q_cool", "min"),
    "max_q_occ": ("zone_energy_q_occ", "max"),
    "max_q_loss": ("zone_energy_q_loss", "max"),
    "max_q_equip": ("zone_energy_q_equip", "max"),
    "max_co2": ("iaq_xco2vol", "max"),
    "mean_co2": ("iaq_xco2vol", "mean"),
    "max_tair": ("temperatures_tairmean", "max"),
    "min_tair": ("temperatures_tairmean", "min"),
    "max_top": ("temperatures_top", "max"),
    "min_top": ("temperatures_top", "min"),
    "mean_top": ("temperatures_top", "mean"),
    "max_relhum": ("iaq_relhum", "max"),
    "min_relhum": ("iaq_relhum", "min"),
    "mean_relhum": ("iaq_relhum", "mean"),
    "max_air_age": ("iaq_air_age", "max"),
}
OUTPUT_COLUMNS = [
    "Zone",
    "Group",
    "Zone multiplier, M",
    "Min temp., \u00b0C",
    "Max temp., \u00b0C",
    "Min op temp., \u00b0C",
    "Max op temp., \u00b0C",
    "Room unit heat, kWh",
    "Room unit heat, kWh/m2",
    "Max heat supplied, W/m2",
    "Room unit heat, W/m2",
    "Max heat removed, W/m2",
    "Room unit cool, kWh",
    "Room unit cool, kWh/m2",
    "Room unit cool, W/m2",
    "Dryvent cool, W/m2",
    "Max sup airflow, L/s m2",
    "Max rtn airflow, L/s",
    "Max solar gain, W/m2",
    "Min rel hum, %",
    "Max rel hum, %",
    "Max CO2 ppm (vol)",
    "Max PPD, %",
    "Max age of air, h",
    "In use, h",
    "h of T_op>25, h",
    "h of T_op>27, h",
    "Occ. hours, h PDH, h",
    "Unmet hours (cooling)",
    "Unmet hours (heating)",
    "DIN 4108-2 over-temperature degree hours, h Deg-C",
]
COLUMN_RENAME = {
    "room": "Zone",
    "variant": "Group",
    "row_count": "In use, h",
    "min_tair": "Min temp., \u00b0C",
    "max_tair": "Max temp., \u00b0C",
    "min_top": "Min op temp., \u00b0C",
    "max_top": "Max op temp., \u00b0C",
    "max_q_heat": "Max heat supplied, W/m2",
    "max_q_cool": "Max heat removed, W/m2",
    "min_relhum": "Min rel hum, %",
    "max_relhum": "Max rel hum, %",
    "max_co2": "Max CO2 ppm (vol)",
    "max_air_age": "Max age of air, h",
}


# ============================================================================
# Allgemeine Hilfsfunktionen
# ============================================================================
def parse_comma_separated_list(value):
    """Wandelt eine kommaseparierte CLI-Eingabe in eine Liste um."""
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


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


def build_run_output_dir(variant_dir, run_id, output_root=None):
    """Baut den Laufordner im Schema <output_root>/<variant_dir>/<run_id>."""
    base_output_dir = output_root if output_root else OUTPUT_DIR
    return os.path.join(base_output_dir, variant_dir, run_id)


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


def get_room_data_file(variant_dir, room_name):
    """Liefert den erwarteten CSV-Pfad fuer einen Raum."""
    """Liefert den Dateipfad zur aufbereiteten Raum-CSV-Datei."""
    return os.path.join(variant_dir, f"{room_name.replace(' ', '_')}{ROOM_FILE_EXTENSION}")


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


def summarize_room_metrics(df, variant_name, room_name):
    """Berechnet die definierten Kennwerte fuer einen Raum."""
    """Berechnet die definierten Metriken für einen Raum und gibt eine breite Zeile zurück."""
    if df is None or df.empty:
        return None

    row = {
        "variant": variant_name,
        "room": room_name,
        "row_count": len(df),
    }

    for metric_name, (column_name, agg_func) in METRIC_DEFINITIONS.items():
        if column_name not in df.columns:
            row[metric_name] = None
            continue

        series = df[column_name].dropna()
        if series.empty:
            row[metric_name] = None
            continue

        if agg_func == "max":
            value = series.max()
        elif agg_func == "min":
            value = series.min()
        elif agg_func == "mean":
            value = series.mean()
        elif agg_func == "median":
            value = series.median()
        else:
            value = None

        row[metric_name] = value

    return row


def prepare_result_dataframe(rows):
    """Bringt Ergebniszeilen in die gewuenschte Excel-Spaltenreihenfolge."""
    result_df = pd.DataFrame(rows)
    result_df = result_df.sort_values(["variant", "room"])
    result_df = result_df.rename(columns=COLUMN_RENAME)
    return result_df.reindex(columns=OUTPUT_COLUMNS)


def write_excel_report(result_df, output_dir, filename):
    """Schreibt eine Ergebnis-Tabelle als Excel-Datei."""
    output_excel_dir = os.path.join(output_dir, PLOT_SUBDIR_EXCEL)
    os.makedirs(output_excel_dir, exist_ok=True)

    output_file = os.path.join(output_excel_dir, filename)
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        result_df.to_excel(writer, sheet_name="metrics", index=False)
    return output_file


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
                f"{datetime.now().strftime('%y%m%d')}_{variant_display_name}_analysis.xlsx",
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
        help="Verzeichnis mit aufbereiteten Raum-CSV-Dateien (default: 1_Datenbank)",
    )
    parser.add_argument(
        "--output-root", default=None, help="Wurzelverzeichnis für die Excel-Ausgabe (default: 2_Output)"
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
