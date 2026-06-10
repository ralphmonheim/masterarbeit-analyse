"""Wetterdaten-Seite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

import streamlit as st

from ma_weather import WeatherDataset, import_weather_catalog


def weather_dataset_rows(datasets: list[WeatherDataset]) -> list[dict[str, object]]:
    """Bereitet Wetterdatensaetze fuer eine UI-Tabelle auf."""
    rows: list[dict[str, object]] = []
    for dataset in datasets:
        resolved_path = dataset.resolved_file_path()
        rows.append(
            {
                "weather_key": dataset.weather_key,
                "Name": dataset.display_name,
                "Ort": dataset.location,
                "Format": dataset.file_format,
                "Quelle": dataset.source,
                "Jahrtyp": dataset.year_type,
                "Szenario": dataset.climate_scenario,
                "Aktiv": dataset.is_active,
                "Datei": str(dataset.file_path),
                "Datei vorhanden": resolved_path.exists(),
                "Hinweise": dataset.notes,
            }
        )
    return rows


def render() -> None:
    """Zeigt den vorbereiteten Wetterkatalog ohne TRY-Dateiimport."""
    st.title("Wetterdaten")
    st.caption("Lokale TRY-Datensaetze und Wetterkatalog")

    try:
        catalog = import_weather_catalog()
    except Exception as exc:  # noqa: BLE001 - UI zeigt Servicefehler als Status an.
        st.error(f"Wetterkatalog konnte nicht geladen werden: {exc}")
        return

    active_count = len(catalog.active_datasets())
    st.metric("Aktive Wetterdatensaetze", active_count)
    st.dataframe(weather_dataset_rows(catalog.datasets), hide_index=True, use_container_width=True)
