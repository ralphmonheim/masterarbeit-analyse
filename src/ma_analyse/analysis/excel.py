"""Erzeugt Excel-Auswertungen aus aufbereiteten Simulationsdaten.

Eingaben:
    Raum-CSV-Dateien aus ``data/ma_analyse/database/<Variante>_nutzdaten``.

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
from ..stage_3_standards_verification import build_verification_readiness_rows
from .components.rooms import get_room_data_file
from .components.runtime import build_named_run_output_dir, get_dated_output_prefix, get_run_id
from .components.variants import get_variant_display_name, normalize_variant_name
from .tables.excel_report import (
    AnalysisTableBundle,
    build_calculation_boundary_rows,
    build_data_inventory_row,
    prepare_legacy_result_dataframe,
    prepare_result_dataframe,
    summarize_room_metrics,
    write_excel_report,
)


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
    power_display_mode="both",
    power_source_unit="unverified",
    reference_areas_m2=None,
):
    """Erstellt die Excel-Auswertung fuer die gewaehlten Varianten und Raeume."""
    """Erstellt eine Excel-Zusammenfassung für alle Varianten und Räume."""
    resolved_run_id = get_run_id(command_name="excel-analysis", run_id=run_id)
    output_prefix = get_output_prefix()

    if variant_mode == "single":
        output_files = []
        variants = _resolved_variant_dirs(datenbank_dir, selected_variants)
        for variant_name, _variant_path in variants:
            bundle = build_analysis_table_bundle(
                datenbank_dir,
                selected_variants=[variant_name],
                rooms=rooms,
                power_display_mode=power_display_mode,
                power_source_unit=power_source_unit,
                reference_areas_m2=reference_areas_m2,
                debug=debug,
            )
            variant_display_name = get_variant_display_name(variant_name)
            run_output_dir = build_run_output_dir(variant_name, resolved_run_id, output_root=output_root)
            output_file = write_excel_report(
                bundle.summary,
                run_output_dir,
                f"{get_dated_output_prefix(variant_display_name)}_analysis.xlsx",
                legacy_result_df=bundle.legacy_summary,
                detail_tables=bundle.detail_tables(),
            )
            output_files.append(output_file)
            if debug:
                print(f"Excel-Bericht erzeugt: {output_file}")
        return output_files

    bundle = build_analysis_table_bundle(
        datenbank_dir,
        selected_variants=selected_variants,
        rooms=rooms,
        power_display_mode=power_display_mode,
        power_source_unit=power_source_unit,
        reference_areas_m2=reference_areas_m2,
        debug=debug,
    )
    run_output_dir = build_run_output_dir("analyze_simulation", resolved_run_id, output_root=output_root)
    output_file = write_excel_report(
        bundle.summary,
        run_output_dir,
        f"{output_prefix}_analysis.xlsx",
        legacy_result_df=bundle.legacy_summary,
        detail_tables=bundle.detail_tables(),
    )

    if debug:
        print(f"Excel-Bericht erzeugt: {output_file}")

    return output_file


def build_analysis_table_bundle(
    datenbank_dir,
    *,
    selected_variants=None,
    rooms=None,
    power_display_mode="both",
    power_source_unit="unverified",
    reference_areas_m2=None,
    debug=False,
) -> AnalysisTableBundle:
    """Berechnet denselben Tabellenstand für Service, UI und Excel."""

    rooms = ROOMS if rooms is None else rooms
    reference_areas_m2 = reference_areas_m2 or {}
    summary_rows: list[dict[str, object]] = []
    inventory_rows: list[dict[str, object]] = []

    for variant_name, variant_path in _resolved_variant_dirs(datenbank_dir, selected_variants):
        variant_display_name = get_variant_display_name(variant_name)
        if debug:
            print(f"Verarbeite Variante: {variant_display_name}")

        for room_name in rooms:
            csv_file = get_room_data_file(variant_path, room_name)
            if not os.path.exists(csv_file):
                if debug:
                    print(f"  Raumdatei fehlt: {csv_file}")
                continue
            df_room = load_room_csv(csv_file)
            if df_room is None or df_room.empty:
                continue
            area_m2 = reference_areas_m2.get(room_name)
            room_summary = summarize_room_metrics(
                df_room,
                variant_display_name,
                room_name,
                reference_area_m2=area_m2,
                power_display_mode=power_display_mode,
                power_source_unit=power_source_unit,
            )
            if room_summary is not None:
                summary_rows.append(room_summary)
            inventory_rows.append(
                build_data_inventory_row(
                    df_room,
                    variant_name=variant_display_name,
                    room_name=room_name,
                    source_file=csv_file,
                    reference_area_m2=area_m2,
                    power_source_unit=power_source_unit,
                )
            )

    if not summary_rows:
        raise ValueError("Keine Raumdaten gefunden. Bitte prüfen Sie das Datenbank-Verzeichnis.")

    return AnalysisTableBundle(
        summary=prepare_result_dataframe(summary_rows, power_display_mode),
        legacy_summary=prepare_legacy_result_dataframe(summary_rows),
        data_inventory=pd.DataFrame(inventory_rows),
        calculation_boundaries=pd.DataFrame(
            build_calculation_boundary_rows(inventory_rows, power_display_mode=power_display_mode)
        ),
        verification_readiness=pd.DataFrame(build_verification_readiness_rows()),
    )


def _resolved_variant_dirs(datenbank_dir, selected_variants=None):
    variants = find_variant_dirs(datenbank_dir, selected_variants=selected_variants)
    if variants:
        return variants
    if os.path.isdir(datenbank_dir):
        return [(get_variant_display_name(datenbank_dir), datenbank_dir)]
    raise FileNotFoundError(f"Datenbank-Verzeichnis nicht gefunden: {datenbank_dir}")


def main():
    """CLI-Einstiegspunkt fuer ``analyze_data``."""
    parser = argparse.ArgumentParser(description="Analysiert Simulationsergebnisse und erzeugt eine Excel-Ausgabe.")
    parser.add_argument(
        "--datenbank-dir",
        default=DATENBANK_DIR,
        help="Verzeichnis mit aufbereiteten Raum-CSV-Dateien (default: data/ma_analyse/database)",
    )
    parser.add_argument(
        "--output-root", default=None, help="Wurzelverzeichnis für die Excel-Ausgabe (default: data/ma_analyse/output)"
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
