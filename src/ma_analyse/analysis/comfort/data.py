"""Datenladen und Spaltennormalisierung fuer Comfort-Auswertungen."""

from __future__ import annotations

import pandas as pd

REQUIRED_PLOT_COLUMNS = ["top", "relhum"]
PLOT_COLUMN_ALIASES = {
    "top": ["local_de_comf_diag_t_top", "temperatures_top", "top"],
    "relhum": ["iaq_relhum", "relhum"],
}


def load_room_csv(csv_file, debug=False):
    """Laedt aufbereitete CSV-Datei eines Raumes und normalisiert Plotspalten."""
    try:
        df = pd.read_csv(csv_file)

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

        for column in REQUIRED_PLOT_COLUMNS:
            df[column] = pd.to_numeric(df[column], errors="coerce")
        df = df.dropna(subset=REQUIRED_PLOT_COLUMNS)

        if debug:
            print(f"    + Geladen: {len(df)} Datenpunkte")
        return df
    except Exception as exc:
        print(f"    X Fehler beim Lesen {csv_file}: {exc}")
        return None
