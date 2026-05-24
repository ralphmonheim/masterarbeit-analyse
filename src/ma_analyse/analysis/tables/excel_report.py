"""Berechnung und Ausgabe der Excel-Kennwerttabellen."""

from __future__ import annotations

import os

import pandas as pd

from .schema import COLUMN_RENAME, METRIC_DEFINITIONS, OUTPUT_COLUMNS, PLOT_SUBDIR_EXCEL


def summarize_room_metrics(df, variant_name, room_name):
    """Berechnet die definierten Kennwerte fuer einen Raum."""
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
