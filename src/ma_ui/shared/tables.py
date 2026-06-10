"""Tabellenhelfer fuer Streamlit-Ansichten."""

from __future__ import annotations

from pathlib import Path


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
