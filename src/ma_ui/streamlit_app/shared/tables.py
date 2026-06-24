"""Tabellenhelfer fuer Streamlit-Ansichten."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd


def file_rows(paths: list[Path]) -> list[dict[str, object]]:
    """Bereitet Dateipfade fuer eine UI-Tabelle auf."""
    rows: list[dict[str, object]] = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "Datei": path.name,
                "Pfad": str(path),
                "Groesse Byte": path.stat().st_size if exists else None,
                "Vorhanden": exists,
            }
        )
    return rows


def _is_missing(value: object) -> bool:
    """Prueft robuste Missing-Werte fuer einfache UI-Tabellen."""
    if value is None:
        return True
    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def _display_value(value: object) -> str:
    """Wandelt gemischte UI-Werte in Arrow-kompatiblen Text um."""
    if _is_missing(value):
        return ""
    return str(value)


def normalize_table_for_streamlit(data: Iterable[Mapping[str, object]] | pd.DataFrame) -> pd.DataFrame:
    """Bereitet Tabellen fuer `st.dataframe` Arrow-kompatibel auf.

    Streamlit nutzt intern PyArrow. Gemischte Spalten wie Zahlen plus Text
    koennen dort scheitern. Fuer die Anzeige werden nur solche gemischten
    Objektspalten in Text gewandelt; die Fachdaten selbst bleiben unveraendert.
    """
    dataframe = data.copy() if isinstance(data, pd.DataFrame) else pd.DataFrame(list(data))
    for column in dataframe.columns:
        series = dataframe[column]
        if series.dtype != "object":
            continue
        non_missing_values = [value for value in series if not _is_missing(value)]
        value_types = {type(value) for value in non_missing_values}
        if len(value_types) > 1:
            dataframe[column] = series.map(_display_value)
    return dataframe
