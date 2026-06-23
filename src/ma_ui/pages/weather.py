"""Wetterdaten-Seite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

import re
from pathlib import Path
from typing import MutableMapping

import streamlit as st

from ma_core import create_session_id
from ma_ui.shared import normalize_table_for_streamlit
from ma_validation import (
    ReleaseChoice,
    ReleaseDecision,
    ReleaseStatus,
)
from ma_weather import (
    WeatherAnalysisResult,
    WeatherDataset,
    WeatherLocation,
    WeatherLocationCatalog,
    WeatherMetrics,
    WeatherPlotResult,
    WeatherRegion,
    import_weather_catalog,
    import_weather_location_catalog,
    record_weather_release_decision,
    run_weather_analysis,
)
from ma_weather.weather_catalog import DATASET_ROLE_SITE_SPECIFIC, DATASET_ROLE_TRY_REFERENCE

WEATHER_RESULT_SESSION_KEY = "ma_ui_weather_analysis_result"
WEATHER_KEY_WIDGET_KEY = "ma_ui_weather_key"
WEATHER_LOCATION_WIDGET_KEY = "ma_ui_weather_location"
WEATHER_SESSION_ID_SESSION_KEY = "ma_ui_weather_session_id"
WEATHER_RELEASE_DECISION_SESSION_KEY = "ma_ui_weather_release_decision"
WEATHER_RELEASE_NOTE_WIDGET_KEY = "ma_ui_weather_release_note"
WEATHER_MAP_IMAGE_PATH = Path("src/ma_ui/assets/weather/klimaregionen_deutschland.png")


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
                "Rolle": weather_dataset_role_label(dataset),
                "Standort-ID": dataset.location_id,
                "Referenzstandort-ID": dataset.reference_location_id,
                "Prioritaet": dataset.selection_priority,
                "Aktiv": dataset.is_active,
                "Datei": str(dataset.file_path),
                "Datei vorhanden": resolved_path.exists(),
                "Hinweise": dataset.notes,
            }
        )
    return rows


def weather_dataset_role_label(dataset: WeatherDataset) -> str:
    """Gibt die fachliche Rolle eines Wetterdatensatzes lesbar aus."""
    if dataset.dataset_role == DATASET_ROLE_TRY_REFERENCE:
        return "TRY-Referenzdatensatz"
    if dataset.dataset_role == DATASET_ROLE_SITE_SPECIFIC:
        return "Standortgenauer Datensatz"
    return "Nicht zugeordnet"


def weather_dataset_label(dataset: WeatherDataset) -> str:
    """Baut eine kompakte Auswahlbeschriftung fuer Wetterdatensaetze."""
    role_label = weather_dataset_role_label(dataset)
    prefix = "Empfohlen: " if dataset.dataset_role == DATASET_ROLE_TRY_REFERENCE else ""
    return f"{prefix}{dataset.weather_key} - {dataset.location} ({role_label})"


def weather_location_label(location: WeatherLocation) -> str:
    """Baut eine kompakte Auswahlbeschriftung fuer Staedte."""
    if location.legacy_code:
        return f"{location.location_name} ({location.legacy_code})"
    return location.location_name


def weather_location_rows(catalog: WeatherLocationCatalog) -> list[dict[str, object]]:
    """Bereitet Standortdaten fuer Streamlit-Tabellen oder Tests auf."""
    rows: list[dict[str, object]] = []
    for location in catalog.active_locations():
        region = catalog.region_for_location(location.location_id)
        reference_location = catalog.reference_location_for_city(location.location_id)
        rows.append(
            {
                "Standort-ID": location.location_id,
                "Stadt": location.location_name,
                "Legacy-Code": location.legacy_code,
                "Klimaregion": region.region_code,
                "TRY-Referenzstandort": reference_location.location_name,
                "Referenzstandort": location.is_reference_location,
            }
        )
    return rows


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


def get_weather_session_id(session_state: MutableMapping[str, object]) -> str:
    """Verwendet eine stabile Sitzungs-ID fuer alle Wetterlaeufe der UI-Sitzung."""
    current = session_state.get(WEATHER_SESSION_ID_SESSION_KEY)
    if isinstance(current, str) and current:
        return current
    session_id = create_session_id()
    session_state[WEATHER_SESSION_ID_SESSION_KEY] = session_id
    return session_id


def _try_reference_datasets(datasets: list[WeatherDataset]) -> list[WeatherDataset]:
    return [dataset for dataset in datasets if dataset.dataset_role == DATASET_ROLE_TRY_REFERENCE]


def _site_specific_datasets(datasets: list[WeatherDataset]) -> list[WeatherDataset]:
    return [dataset for dataset in datasets if dataset.dataset_role == DATASET_ROLE_SITE_SPECIFIC]


def _render_weather_map() -> None:
    st.markdown("**Klimaregionen**")
    if WEATHER_MAP_IMAGE_PATH.exists():
        st.image(str(WEATHER_MAP_IMAGE_PATH), caption="TRY-Klimaregionen Deutschland", width="stretch")
    else:
        st.info(
            "Die Klimaregionenkarte ist noch nicht hinterlegt. "
            f"Erwarteter Pfad: `{WEATHER_MAP_IMAGE_PATH}`"
        )


def _render_location_context(
    location_catalog: WeatherLocationCatalog,
    selected_location: WeatherLocation,
) -> tuple[WeatherRegion, WeatherLocation]:
    region = location_catalog.region_for_location(selected_location.location_id)
    reference_location = location_catalog.reference_location_for_city(selected_location.location_id)
    st.markdown(f"**Klimaregion:** {region.region_code} - {region.region_name or 'ohne Bezeichnung'}")
    st.markdown(f"**TRY-Referenzstandort:** {reference_location.location_name}")
    return region, reference_location


def _render_weather_selection(
    catalog: object,
    location_catalog: WeatherLocationCatalog | None,
) -> WeatherDataset | None:
    """Rendert die Standort- und Datensatzauswahl und gibt den Datensatz zurueck."""
    active_datasets = catalog.active_datasets()
    left_column, right_column = st.columns([1, 2])
    with left_column:
        _render_weather_map()

    with right_column:
        if location_catalog is None:
            st.warning("Der Standortkatalog konnte nicht geladen werden. Es werden alle aktiven Datensaetze angezeigt.")
            selectable_datasets = active_datasets
        else:
            active_locations = location_catalog.active_locations()
            if not active_locations:
                st.info("Im Standortkatalog ist aktuell kein aktiver Standort vorhanden.")
                return None
            locations_by_id = {location.location_id: location for location in active_locations}
            selected_location_id = st.selectbox(
                "Stadt",
                options=tuple(locations_by_id),
                format_func=lambda location_id: weather_location_label(locations_by_id[location_id]),
                key=WEATHER_LOCATION_WIDGET_KEY,
            )
            selected_location = locations_by_id[selected_location_id]
            _, reference_location = _render_location_context(location_catalog, selected_location)
            selectable_datasets = catalog.datasets_for_location(
                location_id=selected_location.location_id,
                reference_location_id=reference_location.location_id,
            )
            if not _try_reference_datasets(selectable_datasets):
                st.info(
                    "Fuer diesen TRY-Referenzstandort ist noch kein aktiver "
                    "TRY-Referenzdatensatz katalogisiert."
                )
            if _site_specific_datasets(selectable_datasets):
                st.caption("Standortgenaue Datensaetze werden zusaetzlich zur Referenz angezeigt.")

        if not selectable_datasets:
            st.warning("Fuer die aktuelle Auswahl ist kein eindeutig zugeordneter aktiver Wetterdatensatz vorhanden.")
            return None

        datasets_by_key = {dataset.weather_key: dataset for dataset in selectable_datasets}
        selected_key = st.selectbox(
            "Wetterdatensatz",
            options=tuple(datasets_by_key),
            format_func=lambda key: weather_dataset_label(datasets_by_key[key]),
            key=WEATHER_KEY_WIDGET_KEY,
        )
        return datasets_by_key[selected_key]


def weather_source_rows(result: WeatherAnalysisResult) -> list[dict[str, object]]:
    """Bereitet die technische und fachliche Quellenherkunft auf."""
    source = result.import_result.source
    return [
        {
            "Quellen-ID": source.source_id,
            "Quellenart": source.source_kind.value,
            "Format": source.data_format,
            "Datei": str(source.source_path or ""),
            "Adapter": source.adapter_key or "",
            "Geladen": source.loaded_at.isoformat(),
            "Vorlage": source.is_template,
            "Dateigroesse Byte": source.file_size_bytes,
            "SHA-256": source.sha256 or "",
        }
    ]


def weather_diagnostic_rows(result: WeatherAnalysisResult) -> list[dict[str, object]]:
    """Bereitet alle strukturierten Import- und Validierungsmeldungen auf."""
    return [
        {
            "Diagnose-ID": message.diagnostic_id,
            "Schweregrad": message.severity.value,
            "Code": message.code,
            "Problem": message.message,
            "Fundstelle": message.location or "",
        }
        for message in result.validation_report.validation_result.messages
    ]


def release_decision_matches_result(
    decision: object,
    result: WeatherAnalysisResult,
) -> bool:
    """Verhindert, dass eine alte Freigabe auf einen neuen Lauf uebertragen wird."""
    return (
        isinstance(decision, ReleaseDecision)
        and decision.session_id == result.session_id
        and decision.run_id == result.run_id
        and decision.dataset_key == result.dataset.weather_key
    )


def _render_release_status(result: WeatherAnalysisResult) -> None:
    validation_result = result.validation_report.validation_result
    stored_decision = st.session_state.get(WEATHER_RELEASE_DECISION_SESSION_KEY)
    decision = (
        stored_decision
        if release_decision_matches_result(stored_decision, result)
        else result.release_decision
    )

    st.markdown("**Freigabe**")
    if isinstance(decision, ReleaseDecision):
        if decision.resulting_status is ReleaseStatus.RELEASED:
            st.success(f"Freigegeben ({decision.choice.value}), Entscheidung {decision.decision_id}")
        else:
            st.error(f"Nicht freigegeben ({decision.choice.value}), Entscheidung {decision.decision_id}")
        if decision.note:
            st.caption(f"Notiz: {decision.note}")
        return

    if validation_result.release_status is ReleaseStatus.BLOCKED:
        st.error("Der Datenstand ist durch Fehler blockiert und kann nicht freigegeben werden.")
        return
    if validation_result.release_status is ReleaseStatus.RELEASED:
        st.success("Der Datenstand wurde ohne Warnungen automatisch freigegeben.")
        return

    st.warning("Warnungen muessen bewusst bestaetigt oder blockiert werden.")
    note = st.text_area(
        "Optionale Notiz zur Entscheidung",
        key=WEATHER_RELEASE_NOTE_WIDGET_KEY,
    )
    blocked_column, released_column = st.columns(2)
    with blocked_column:
        keep_blocked = st.button(
            "Nicht freigeben",
            key=f"weather_keep_blocked_{result.run_id}",
            width="stretch",
        )
    with released_column:
        release_with_warnings = st.button(
            "Warnungen bestaetigen und freigeben",
            key=f"weather_release_warnings_{result.run_id}",
            type="primary",
            width="stretch",
        )

    selected_choice: ReleaseChoice | None = None
    if keep_blocked:
        selected_choice = ReleaseChoice.KEEP_BLOCKED
    elif release_with_warnings:
        selected_choice = ReleaseChoice.RELEASE_WITH_WARNINGS
    if selected_choice is not None:
        try:
            decision = record_weather_release_decision(
                result,
                choice=selected_choice,
                note=note,
            )
        except (OSError, ValueError) as exc:
            st.error(f"Freigabeentscheidung konnte nicht gespeichert werden: {exc}")
        else:
            st.session_state[WEATHER_RELEASE_DECISION_SESSION_KEY] = decision
            st.rerun()


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

    st.markdown("**Quelle**")
    st.dataframe(
        normalize_table_for_streamlit(weather_source_rows(result)),
        hide_index=True,
        width="stretch",
    )
    diagnostic_rows = weather_diagnostic_rows(result)
    if diagnostic_rows:
        st.markdown("**Diagnosen**")
        st.dataframe(
            normalize_table_for_streamlit(diagnostic_rows),
            hide_index=True,
            width="stretch",
        )
    _render_release_status(result)

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
    st.caption(f"Sitzungslog: {result.session_log_path}")


def render() -> None:
    """Zeigt Wetterkatalog, Auswahl und lokale Wetteranalyse."""
    st.title("Wetterdaten")
    st.caption("Lokale TRY-Datensaetze analysieren und Diagramme anzeigen")

    try:
        catalog = import_weather_catalog()
    except Exception as exc:  # noqa: BLE001 - UI zeigt Servicefehler als Status an.
        st.error(f"Wetterkatalog konnte nicht geladen werden: {exc}")
        return

    try:
        location_catalog: WeatherLocationCatalog | None = import_weather_location_catalog()
    except Exception as exc:  # noqa: BLE001 - UI zeigt Servicefehler als Status an.
        location_catalog = None
        st.warning(f"Standortkatalog konnte nicht geladen werden: {exc}")

    active_datasets = catalog.active_datasets()
    active_count = len(active_datasets)

    st.subheader("Standort und Wetterauswahl")

    if not active_datasets:
        st.info("Im Wetterkatalog ist aktuell kein aktiver Wetterdatensatz vorhanden.")
        st.subheader("Wetterdatensaetze")
        st.metric("Aktive Wetterdatensaetze", active_count)
        st.dataframe(
            normalize_table_for_streamlit(weather_dataset_rows(catalog.datasets)),
            hide_index=True,
            width="stretch",
        )
        return

    selected_dataset = _render_weather_selection(catalog, location_catalog)
    if selected_dataset is None:
        st.subheader("Wetterdatensaetze")
        st.metric("Aktive Wetterdatensaetze", active_count)
        st.dataframe(
            normalize_table_for_streamlit(weather_dataset_rows(catalog.datasets)),
            hide_index=True,
            width="stretch",
        )
        return

    selected_path = selected_dataset.resolved_file_path()
    selected_start_year = weather_start_year(selected_dataset)

    st.subheader("Analyse")
    st.caption(f"Datei: {selected_path}")
    st.caption(f"Startjahr fuer Zeitindex: {selected_start_year}")
    file_exists = selected_path.exists()
    if not file_exists:
        st.warning("Die lokale TRY-Datei wurde nicht gefunden. Die Analyse kann erst nach dem Ablegen der Datei starten.")

    if st.button("Wetteranalyse starten", type="primary", disabled=not file_exists):
        st.session_state.pop(WEATHER_RELEASE_DECISION_SESSION_KEY, None)
        st.session_state.pop(WEATHER_RELEASE_NOTE_WIDGET_KEY, None)
        with st.spinner(f"Wetteranalyse fuer {selected_dataset.weather_key} laeuft..."):
            try:
                result = run_weather_analysis(
                    selected_dataset.weather_key,
                    start_year=selected_start_year,
                    session_id=get_weather_session_id(st.session_state),
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

    st.subheader("Wetterdatensaetze")
    st.metric("Aktive Wetterdatensaetze", active_count)
    st.dataframe(
        normalize_table_for_streamlit(weather_dataset_rows(catalog.datasets)),
        hide_index=True,
        width="stretch",
    )
