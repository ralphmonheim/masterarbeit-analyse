"""Wetterdaten-Seite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

import re
from pathlib import Path

import streamlit as st

from ma_ui.shared import normalize_table_for_streamlit
from ma_weather import (
    WeatherAnalysisResult,
    WeatherDataset,
    WeatherMetrics,
    WeatherPlotResult,
    import_weather_catalog,
    run_weather_analysis,
)

WEATHER_RESULT_SESSION_KEY = "ma_ui_weather_analysis_result"
WEATHER_KEY_WIDGET_KEY = "ma_ui_weather_key"


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


def weather_dataset_label(dataset: WeatherDataset) -> str:
    """Baut eine kompakte Auswahlbeschriftung fuer Wetterdatensaetze."""
    return f"{dataset.weather_key} - {dataset.location} ({dataset.display_name})"


def weather_start_year(dataset: WeatherDataset) -> int:
    """Leitet das Startjahr fuer den Wetter-Zeitindex aus Katalogdaten ab."""
    candidates = (
        dataset.weather_key,
        dataset.file_path.name,
        dataset.display_name,
        dataset.climate_scenario,
    )
    for candidate in candidates:
        match = re.search(r"(19|20)\d{2}", candidate)
        if match:
            return int(match.group(0))
    return 2015


def weather_metric_rows(metrics: WeatherMetrics) -> list[dict[str, object]]:
    """Bereitet Wetterkennwerte fuer Streamlit auf."""
    labels = {
        "mean_temperature_c": "Mittlere Temperatur [Grad C]",
        "min_temperature_c": "Minimale Temperatur [Grad C]",
        "max_temperature_c": "Maximale Temperatur [Grad C]",
        "mean_relative_humidity_pct": "Mittlere relative Feuchte [%]",
        "mean_wind_speed_m_s": "Mittlere Windgeschwindigkeit [m/s]",
        "max_wind_speed_m_s": "Maximale Windgeschwindigkeit [m/s]",
        "global_radiation_kwh_m2a": "Globalstrahlung [kWh/m2a]",
        "hours_above_25c": "Stunden ueber 25 Grad C",
        "hours_above_30c": "Stunden ueber 30 Grad C",
        "heating_degree_hours_kh": "Heizgradstunden [Kh]",
        "cooling_degree_hours_kh": "Kuehlgradstunden [Kh]",
    }
    rows: list[dict[str, object]] = []
    for key, value in metrics.as_dict().items():
        display_value = round(value, 2) if isinstance(value, float) else value
        rows.append({"Kennwert": labels.get(key, key), "Wert": display_value})
    return rows


def weather_plot_rows(plot_results: tuple[WeatherPlotResult, ...]) -> list[dict[str, object]]:
    """Bereitet die erzeugten Wetterdiagramme fuer eine Dateitabelle auf."""
    rows: list[dict[str, object]] = []
    for plot_result in plot_results:
        path = plot_result.path
        rows.append(
            {
                "plot_key": plot_result.plot_key,
                "Status": plot_result.status,
                "Datei": path.name if path else "",
                "Pfad": str(path) if path else "",
                "Vorhanden": bool(path and path.exists()),
                "Hinweise": "; ".join(plot_result.warnings),
            }
        )
    return rows


def weather_analysis_file_rows(result: WeatherAnalysisResult) -> list[dict[str, object]]:
    """Listet die zentralen Dateien eines Wetteranalyse-Laufs."""
    files = (
        ("Aufbereitete Wetterdaten", result.processed_data_path),
        ("Markdown-Bericht", result.report_path),
    )
    return [
        {
            "Typ": label,
            "Datei": path.name,
            "Pfad": str(path),
            "Vorhanden": path.exists(),
        }
        for label, path in files
    ]


def created_weather_plot_paths(plot_results: tuple[WeatherPlotResult, ...]) -> list[Path]:
    """Gibt vorhandene PNG-Pfade fuer die direkte Diagrammvorschau zurueck."""
    return [
        plot_result.path
        for plot_result in plot_results
        if plot_result.status == "created" and plot_result.path is not None and plot_result.path.exists()
    ]


def _render_weather_analysis_result(result: WeatherAnalysisResult) -> None:
    st.subheader("Analyseergebnis")
    status = result.validation_report.status
    if status == "ok":
        st.success(f"Validierung ok: {result.import_result.row_count} Stundenwerte.")
    elif status == "warning":
        st.warning(f"Validierung mit Hinweisen: {result.import_result.row_count} Stundenwerte.")
    else:
        st.error(f"Validierung mit Fehlern: {result.import_result.row_count} Stundenwerte.")

    if result.validation_report.warnings:
        st.warning("\n".join(result.validation_report.warnings))
    if result.validation_report.errors:
        st.error("\n".join(result.validation_report.errors))

    st.markdown("**Kennwerte**")
    st.dataframe(normalize_table_for_streamlit(weather_metric_rows(result.metrics)), hide_index=True, width="stretch")

    image_paths = created_weather_plot_paths(result.plot_results)
    if image_paths:
        st.markdown("**Diagramme**")
        for image_path in image_paths:
            st.image(str(image_path), caption=image_path.name, width="stretch")

    st.markdown("**Ausgabedateien**")
    st.dataframe(
        normalize_table_for_streamlit(weather_analysis_file_rows(result)),
        hide_index=True,
        width="stretch",
    )
    st.dataframe(normalize_table_for_streamlit(weather_plot_rows(result.plot_results)), hide_index=True, width="stretch")


def render() -> None:
    """Zeigt Wetterkatalog, Auswahl und lokale Wetteranalyse."""
    st.title("Wetterdaten")
    st.caption("Lokale TRY-Datensaetze analysieren und Diagramme anzeigen")

    try:
        catalog = import_weather_catalog()
    except Exception as exc:  # noqa: BLE001 - UI zeigt Servicefehler als Status an.
        st.error(f"Wetterkatalog konnte nicht geladen werden: {exc}")
        return

    active_datasets = catalog.active_datasets()
    active_count = len(active_datasets)
    st.metric("Aktive Wetterdatensaetze", active_count)
    st.dataframe(normalize_table_for_streamlit(weather_dataset_rows(catalog.datasets)), hide_index=True, width="stretch")

    if not active_datasets:
        st.info("Im Wetterkatalog ist aktuell kein aktiver Wetterdatensatz vorhanden.")
        return

    datasets_by_key = {dataset.weather_key: dataset for dataset in active_datasets}
    selected_key = st.selectbox(
        "Wetterdatensatz",
        options=tuple(datasets_by_key),
        format_func=lambda key: weather_dataset_label(datasets_by_key[key]),
        key=WEATHER_KEY_WIDGET_KEY,
    )
    selected_dataset = datasets_by_key[selected_key]
    selected_path = selected_dataset.resolved_file_path()
    selected_start_year = weather_start_year(selected_dataset)

    st.caption(f"Datei: {selected_path}")
    st.caption(f"Startjahr fuer Zeitindex: {selected_start_year}")
    file_exists = selected_path.exists()
    if not file_exists:
        st.warning("Die lokale TRY-Datei wurde nicht gefunden. Die Analyse kann erst nach dem Ablegen der Datei starten.")

    if st.button("Wetteranalyse starten", type="primary", disabled=not file_exists):
        with st.spinner(f"Wetteranalyse fuer {selected_dataset.weather_key} laeuft..."):
            try:
                result = run_weather_analysis(
                    selected_dataset.weather_key,
                    start_year=selected_start_year,
                    print_summary=False,
                )
            except Exception as exc:  # noqa: BLE001 - UI zeigt Servicefehler als Status an.
                st.session_state.pop(WEATHER_RESULT_SESSION_KEY, None)
                st.error(f"Wetteranalyse fehlgeschlagen: {exc}")
            else:
                st.session_state[WEATHER_RESULT_SESSION_KEY] = result

    result = st.session_state.get(WEATHER_RESULT_SESSION_KEY)
    if isinstance(result, WeatherAnalysisResult):
        if result.dataset.weather_key == selected_dataset.weather_key:
            _render_weather_analysis_result(result)
        else:
            st.info(
                "Es liegt ein Analyseergebnis fuer einen anderen Wetterdatensatz vor. "
                "Starte die Analyse fuer die aktuelle Auswahl neu."
            )
