"""Bereitet Rohdaten-PRN-Dateien fuer die Analysepipeline auf.

Eingaben:
    Variantenordner unter ``data/input`` mit Raumunterordnern und den erwarteten
    PRN-Dateien je Raum.

Ausgaben:
    Zusammengefuehrte Raumtabellen unter ``data/database/<Variante>_nutzdaten``.
    Je nach Exportformat werden CSV-, Excel- oder beide Dateitypen erzeugt.

Wichtige Annahmen:
    Pro Raum werden die in ``PRN_FILES`` definierten Quelldateien erwartet. Die
    Zeitspalte heisst ``time`` und dient als gemeinsame Merge-Achse.
"""

import os
from pathlib import Path

import pandas as pd

from ..core.config import (
    DATENBANK_DIR,
    EXPORT_FORMATS,
    INPUT_DIR,
    PRN_FILES,
    RELHUM_COLUMN,
    RELHUM_FILE,
    ROOM_FILE_EXTENSIONS,
    ROOMS,
    TARGET_HOURS,
    TIME_COLUMN,
)


# ============================================================================
# Einzeldateien lesen und normalisieren
# ============================================================================
def load_prn_file(file_path, debug=False):
    """Lädt eine PRN-Datei mit Header und übernimmt alle Spalten."""
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            header_line = handle.readline().strip()
            if header_line.startswith("#"):
                header_line = header_line[1:].strip()

            column_names = [col.lower() for col in header_line.split()]

            if debug:
                print(f"    Spalten ({Path(file_path).name}): {column_names}")

            data = pd.read_csv(handle, sep=r"\s+", names=column_names, header=None)

        return data
    except Exception as exc:
        print(f"    X Fehler beim Lesen {file_path}: {exc}")
        return None


def to_numeric_by_column(dataframe):
    """Konvertiert alle Spalten robust in numerische Werte."""
    converted = dataframe.copy()
    for column in converted.columns:
        converted[column] = pd.to_numeric(converted[column], errors="coerce")
    return converted


def build_source_prefix(filename):
    """Erzeugt ein stabiles Präfix pro Quelldatei für Spaltennamen."""
    stem = Path(filename).stem.lower()
    return stem.replace("-", "_")


def prepare_file_dataframe(file_path, source_filename, debug=False):
    """Bereitet eine einzelne PRN-Datei auf und behält alle Spalten bei."""
    data = load_prn_file(file_path, debug=debug)
    if data is None or data.empty:
        if debug:
            print(f"    X Datei leer oder nicht lesbar: {source_filename}")
        return None

    if TIME_COLUMN not in data.columns:
        if debug:
            print(f"    X Spalte '{TIME_COLUMN}' fehlt in {source_filename}")
        return None

    data = to_numeric_by_column(data)
    data = data.dropna(subset=[TIME_COLUMN])

    if data.empty:
        if debug:
            print(f"    X Keine gueltigen Zeitwerte in {source_filename}")
        return None

    # Vorgabe beibehalten: relative Feuchte aus IAQ in Prozent umrechnen.
    if source_filename == RELHUM_FILE and RELHUM_COLUMN in data.columns:
        data[RELHUM_COLUMN] = data[RELHUM_COLUMN] * 100

    # Wieder auf Stunden aggregieren wie zuvor.
    data["hour"] = data[TIME_COLUMN].floordiv(1).astype(int)
    value_columns = [column for column in data.columns if column != TIME_COLUMN]
    data = data.groupby("hour", as_index=False)[value_columns].mean(numeric_only=True)
    data = data.rename(columns={"hour": TIME_COLUMN})
    data = data.sort_values(by=TIME_COLUMN).reset_index(drop=True)

    # Auf genau 8760 Stunden begrenzen (z. B. falls 0..8760 vorhanden ist).
    if len(data) > TARGET_HOURS:
        data = data.head(TARGET_HOURS)

    prefix = build_source_prefix(source_filename)
    rename_map = {column: f"{prefix}_{column}" for column in data.columns if column != TIME_COLUMN}
    data = data.rename(columns=rename_map)

    return data


def merge_room_prn_tables(room_dir, room_name, debug=False):
    """Fuehrt alle verfuegbaren PRN-Tabellen eines Raums ueber ``time`` zusammen."""
    """Mergt die 5 PRN-Dateien eines Raums über time (outer join)."""
    room_tables = []

    for source_filename in PRN_FILES:
        source_path = os.path.join(room_dir, source_filename)
        if not os.path.exists(source_path):
            if debug:
                print(f"    - Datei fehlt: {source_filename}")
            continue

        prepared = prepare_file_dataframe(source_path, source_filename, debug=debug)
        if prepared is not None and not prepared.empty:
            room_tables.append(prepared)

    if not room_tables:
        return None

    merged = room_tables[0]
    for table in room_tables[1:]:
        merged = pd.merge(merged, table, on=TIME_COLUMN, how="outer")

    merged.insert(0, "room", room_name)
    ordered_columns = ["room", TIME_COLUMN] + [
        column for column in merged.columns if column not in {"room", TIME_COLUMN}
    ]
    merged = merged[ordered_columns]
    merged = merged.sort_values(by=TIME_COLUMN).reset_index(drop=True)
    return merged


def build_room_output_file(output_dir, room_name, file_format):
    """Erzeugt den Zielpfad fuer eine Raumtabelle im gewaehlten Exportformat."""
    """Erzeugt den Dateipfad für eine aufbereitete Raumdatei im Ziel-Format."""
    return os.path.join(
        output_dir,
        f"{room_name.replace(' ', '_')}{ROOM_FILE_EXTENSIONS[file_format]}",
    )


def save_room_table(room_table, output_dir, room_name, export_format, debug=False):
    """Speichert eine Raumtabelle als CSV, Excel oder in beiden Formaten."""
    """Speichert eine Raumtabelle als CSV, XLSX oder beides."""
    if export_format not in EXPORT_FORMATS:
        raise ValueError(f"Ungueltiges Exportformat: {export_format}")

    if export_format in {"csv", "both"}:
        csv_file = build_room_output_file(output_dir, room_name, "csv")
        room_table.to_csv(csv_file, index=False)
        if debug:
            print(f"    + Raum-CSV gespeichert: {csv_file}")

    if export_format in {"excel", "both"}:
        excel_file = build_room_output_file(output_dir, room_name, "excel")
        room_table.to_excel(excel_file, index=False, engine="openpyxl")
        if debug:
            print(f"    + Raum-XLSX gespeichert: {excel_file}")


def build_nutzdaten_folder_name(variant_name):
    """Leitet aus einem Rohdaten-Variantennamen den Nutzdatenordner ab."""
    """Leitet den Nutzdaten-Ordnernamen aus der Varianten-Nomenklatur ab."""
    if variant_name.endswith("_rohdaten"):
        return f"{variant_name[: -len('_rohdaten')]}_nutzdaten"
    return f"{variant_name}_nutzdaten"


def prepare_variant_data(variant_dir, rooms, datenbank_dir, debug=False, export_format="csv"):
    """Bereitet alle ausgewaehlten Raeume einer Variante auf."""
    """Erstellt je Variante Raumdateien aus 5 PRN-Dateien."""
    variant_name = Path(variant_dir).name
    nutzdaten_folder = build_nutzdaten_folder_name(variant_name)
    nutzdaten_output_dir = os.path.join(datenbank_dir, nutzdaten_folder)
    os.makedirs(nutzdaten_output_dir, exist_ok=True)

    if debug:
        print(f"\nVariante: {variant_name}")
        print(f"  Zielordner: {nutzdaten_output_dir}")

    processed_rooms = 0
    total_room_rows = 0

    for room_name in sorted(rooms):
        room_dir = os.path.join(variant_dir, room_name)

        if debug:
            print(f"  Raum: {room_name}")

        if not os.path.exists(room_dir):
            if debug:
                print("    X Verzeichnis nicht gefunden")
            continue

        room_table = merge_room_prn_tables(room_dir, room_name, debug=debug)
        if room_table is None or room_table.empty:
            if debug:
                print("    X Keine verwertbaren PRN-Daten")
            continue

        save_room_table(
            room_table,
            nutzdaten_output_dir,
            room_name,
            export_format=export_format,
            debug=debug,
        )

        processed_rooms += 1
        total_room_rows += len(room_table)

        if debug:
            print(f"    + Datenzeilen: {len(room_table)}")

    if processed_rooms == 0:
        return {"variant_name": variant_name, "processed_rooms": 0, "rows": 0}

    return {"variant_name": variant_name, "processed_rooms": processed_rooms, "rows": total_room_rows}


def normalize_variant_name(variant_name, suffix):
    """Ergaenzt einen erwarteten Varianten-Suffix, falls er fehlt."""
    """Normalisiert einen Variablennamen auf das gewünschte Suffix."""
    if variant_name.endswith(suffix):
        return variant_name
    return f"{variant_name}{suffix}"


def strip_variant_suffix(variant_name):
    """Entfernt bekannte Varianten-Suffixe fuer Vergleich und Anzeige."""
    """Entfernt bekannte Varianten-Suffixe fuer einen stabilen Vergleich."""
    for suffix in ("_rohdaten", "_nutzdaten"):
        if variant_name.endswith(suffix):
            return variant_name[: -len(suffix)]
    return variant_name


def is_input_variant_dir(variant_path, rooms=None):
    """Prueft, ob ein Ordner wie ein Rohdaten-Variantenordner aussieht."""
    """Erkennt einen Input-Variantenordner ueber vorhandene Raum-Unterordner."""
    if not os.path.isdir(variant_path):
        return False

    room_candidates = rooms if rooms is not None else ROOMS
    return any(os.path.isdir(os.path.join(variant_path, room_name)) for room_name in room_candidates)


def discover_variant_dirs(input_root, rooms=None, debug=False, selected_variants=None):
    """Findet passende Variantenordner im Input-Root."""
    """Findet Variantenordner unter data/input, auch ohne Suffix _rohdaten."""
    if not os.path.exists(input_root):
        return []

    all_variants = [
        entry
        for entry in sorted(os.listdir(input_root))
        if is_input_variant_dir(os.path.join(input_root, entry), rooms=rooms)
    ]

    if selected_variants is not None:
        normalized = {strip_variant_suffix(v.strip()) for v in selected_variants if v.strip()}
        variants = [entry for entry in all_variants if strip_variant_suffix(entry) in normalized]
    else:
        variants = all_variants

    if debug:
        print(f"Gefundene Varianten: {all_variants}")
        if selected_variants is not None:
            print(f"Ausgewählte Varianten: {variants}")

    return [os.path.join(input_root, v) for v in variants]


def process_all_variants(
    input_root,
    rooms,
    datenbank_dir,
    debug=False,
    selected_variants=None,
    export_format="csv",
):
    """Fuehrt die Datenaufbereitung fuer alle ausgewaehlten Varianten aus."""
    """Verarbeitet alle Varianten unter Input und erzeugt Raumdateien."""
    os.makedirs(datenbank_dir, exist_ok=True)

    print("=" * 70)
    print(f"BEHAGLICHKEITSANALYSE - Datenaufbereitung ({export_format.upper()})")
    print("=" * 70)

    variant_dirs = discover_variant_dirs(
        input_root,
        rooms=rooms,
        debug=debug,
        selected_variants=selected_variants,
    )
    if not variant_dirs:
        if selected_variants:
            print(f"X Keine der ausgewaehlten Varianten in {input_root} gefunden: {selected_variants}")
        else:
            print(f"X Keine verarbeitbaren Variantenordner in {input_root} gefunden")
        return

    total_rooms = 0
    total_rows = 0

    for variant_dir in variant_dirs:
        result = prepare_variant_data(
            variant_dir,
            rooms,
            datenbank_dir,
            debug=debug,
            export_format=export_format,
        )
        total_rooms += result["processed_rooms"]
        total_rows += result["rows"]

    print("=" * 70)
    print(f"Verarbeitete Räume insgesamt: {total_rooms}")
    print(f"Zeilen in Raum-Dateien insgesamt: {total_rows}")
    print(f"Ablageort: {os.path.abspath(datenbank_dir)}")
    print("=" * 70)


# ============================================================================
# CLI-Einstiegspunkt
# ============================================================================
if __name__ == "__main__":
    DEBUG = True
    process_all_variants(INPUT_DIR, ROOMS, DATENBANK_DIR, debug=DEBUG)
