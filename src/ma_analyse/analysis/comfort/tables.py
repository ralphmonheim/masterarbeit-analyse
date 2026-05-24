"""Tabellenberechnung fuer Comfort-Zonenanalysen."""

from __future__ import annotations

import pandas as pd


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
