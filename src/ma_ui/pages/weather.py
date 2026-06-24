"""Wetterdaten-Seite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

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
    WeatherDatasetStatus,
    WeatherEvent,
    WeatherLocation,
    WeatherLocationCatalog,
    WeatherMetrics,
    WeatherPlotResult,
    WeatherRegion,
    WeatherSelectionState,
    activate_weather_dataset,
    import_weather_catalog,
    import_weather_location_catalog,
    infer_weather_start_year,
    inspect_weather_catalog_statuses,
    load_weather_selection_state,
    record_weather_release_decision,
    run_weather_analysis,
    save_weather_selection_state,
    set_project_default_weather_dataset,
    weather_status_from_analysis_result,
    weather_statuses_by_key,
)
from ma_weather import (
    weather_event_rows as build_weather_event_rows,
)
from ma_weather.weather_catalog import DATASET_ROLE_SITE_SPECIFIC, DATASET_ROLE_TRY_REFERENCE

WEATHER_RESULT_SESSION_KEY = "ma_ui_weather_analysis_result"
WEATHER_KEY_WIDGET_KEY = "ma_ui_weather_key"
WEATHER_LOCATION_WIDGET_KEY = "ma_ui_weather_location"
WEATHER_SESSION_ID_SESSION_KEY = "ma_ui_weather_session_id"
WEATHER_RELEASE_DECISION_SESSION_KEY = "ma_ui_weather_release_decision"
WEATHER_RELEASE_NOTE_WIDGET_KEY = "ma_ui_weather_release_note"
WEATHER_STATUS_SESSION_KEY = "ma_ui_weather_dataset_statuses"
WEATHER_SELECTION_STATE_SESSION_KEY = "ma_ui_weather_selection_state"
WEATHER_ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "weather"
WEATHER_MAP_IMAGE_PATH = WEATHER_ASSET_DIR / "klimaregionen_deutschland.png"
WEATHER_MAP_IMAGE_CANDIDATES = (
    WEATHER_MAP_IMAGE_PATH,
    WEATHER_ASSET_DIR / "klimaregionen_deutschland.jpg",
    WEATHER_ASSET_DIR / "klimaregionen_deutschland.jpeg",
)

WEATHER_YEAR_TYPE_LABELS = {
    "reference_year": "Jahr",
    "future_year": "Jahr",
    "summer_extreme": "Sommer",
    "winter_extreme": "Winter",
}


def weather_dataset_rows(
    datasets: list[WeatherDataset],
    *,
    status_by_key: dict[str, WeatherDatasetStatus] | None = None,
    selection_state: WeatherSelectionState | None = None,
) -> list[dict[str, object]]:
    """Bereitet Wetterdatensaetze fuer eine UI-Tabelle auf."""
    rows: list[dict[str, object]] = []
    for dataset in datasets:
        resolved_path = dataset.resolved_file_path()
        status = status_by_key.get(dataset.weather_key) if status_by_key else None
        rows.append(
            {
                "weather_key": dataset.weather_key,
                "Name": dataset.display_name,
                "Ort": dataset.location,
                "Format": dataset.file_format,
                "Quelle": dataset.source,
                "Jahrtyp": dataset.year_type,
                "Datensatztyp": weather_dataset_type_label(dataset),
                "Szenario": dataset.climate_scenario,
                "Rolle": weather_dataset_role_label(dataset),
                "Standort-ID": dataset.location_id,
                "Referenzstandort-ID": dataset.reference_location_id,
                "Prioritaet": dataset.selection_priority,
                "Aktiv": dataset.is_active,
                "Aktiviert": bool(selection_state and selection_state.is_activated(dataset.weather_key)),
                "Projekt-Default": bool(
                    selection_state
                    and selection_state.project_default_weather_key == dataset.weather_key
                ),
                "Datensatzstatus": status.status_label if status else "Nicht geprueft",
                "Freigabestatus": status.release_status.value if status and status.release_status else "",
                "Import-ID": status.import_id if status else "",
                "Warnungen": status.warning_count if status else 0,
                "Fehler": status.error_count if status else 0,
                "Stundenwerte": status.row_count if status and status.row_count is not None else "",
                "Datei": str(dataset.file_path),
                "Datei vorhanden": status.file_exists if status else resolved_path.exists(),
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


def weather_dataset_type_label(dataset: WeatherDataset) -> str:
    """Gibt Jahr, Sommer oder Winter fuer Wetterdatensaetze aus."""
    return WEATHER_YEAR_TYPE_LABELS.get(dataset.year_type, dataset.year_type or "Unbekannt")


def weather_dataset_label(
    dataset: WeatherDataset,
    status: WeatherDatasetStatus | None = None,
    selection_state: WeatherSelectionState | None = None,
) -> str:
    """Baut eine kompakte Auswahlbeschriftung fuer Wetterdatensaetze."""
    role_label = weather_dataset_role_label(dataset)
    type_label = weather_dataset_type_label(dataset)
    prefix = "Empfohlen: " if dataset.dataset_role == DATASET_ROLE_TRY_REFERENCE else ""
    state_suffix = ""
    if selection_state and selection_state.project_default_weather_key == dataset.weather_key:
        state_suffix = " | Projekt-Default"
    elif selection_state and selection_state.is_activated(dataset.weather_key):
        state_suffix = " | aktiviert"
    status_suffix = f" | {status.status_label}" if status else ""
    return f"{prefix}{dataset.weather_key} - {dataset.location} [{type_label}] ({role_label}{status_suffix}{state_suffix})"


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
    return infer_weather_start_year(dataset)


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


def get_weather_selection_state(session_state: MutableMapping[str, object]) -> WeatherSelectionState:
    """Laedt den lokalen Wetter-Auswahlstatus einmal pro UI-Sitzung."""
    current = session_state.get(WEATHER_SELECTION_STATE_SESSION_KEY)
    if isinstance(current, WeatherSelectionState):
        return current
    state = load_weather_selection_state()
    session_state[WEATHER_SELECTION_STATE_SESSION_KEY] = state
    return state


def _store_weather_selection_state(state: WeatherSelectionState) -> None:
    save_weather_selection_state(state)
    st.session_state[WEATHER_SELECTION_STATE_SESSION_KEY] = state


def _base_statuses(catalog: object) -> list[WeatherDatasetStatus]:
    return inspect_weather_catalog_statuses(catalog, validate_files=False)


def _stored_statuses() -> list[WeatherDatasetStatus]:
    statuses = st.session_state.get(WEATHER_STATUS_SESSION_KEY)
    if isinstance(statuses, list) and all(isinstance(status, WeatherDatasetStatus) for status in statuses):
        return statuses
    return []


def _current_status_map(
    catalog: object,
    result: object,
) -> dict[str, WeatherDatasetStatus]:
    status_map = weather_statuses_by_key(_base_statuses(catalog))
    status_map.update(weather_statuses_by_key(_stored_statuses()))
    if isinstance(result, WeatherAnalysisResult):
        stored_decision = st.session_state.get(WEATHER_RELEASE_DECISION_SESSION_KEY)
        decision = stored_decision if release_decision_matches_result(stored_decision, result) else None
        status_map[result.dataset.weather_key] = weather_status_from_analysis_result(result, decision=decision)
    return status_map


def _try_reference_datasets(datasets: list[WeatherDataset]) -> list[WeatherDataset]:
    return [dataset for dataset in datasets if dataset.dataset_role == DATASET_ROLE_TRY_REFERENCE]


def _site_specific_datasets(datasets: list[WeatherDataset]) -> list[WeatherDataset]:
    return [dataset for dataset in datasets if dataset.dataset_role == DATASET_ROLE_SITE_SPECIFIC]


def _weather_map_image_path() -> Path:
    """Findet die hinterlegte Klimaregionenkarte im UI-Assetbereich."""
    for image_path in WEATHER_MAP_IMAGE_CANDIDATES:
        if image_path.exists():
            return image_path
    return WEATHER_MAP_IMAGE_PATH


def _display_path(path: Path) -> str:
    """Gibt Pfade fuer UI-Hinweise bevorzugt relativ zum Projektverzeichnis aus."""
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def _render_weather_map() -> None:
    st.markdown("**Klimaregionen**")
    image_path = _weather_map_image_path()
    if image_path.exists():
        st.image(str(image_path), caption="TRY-Klimaregionen Deutschland", width="stretch")
    else:
        st.info(
            "Die Klimaregionenkarte ist noch nicht hinterlegt. "
            f"Erwarteter Pfad: `{_display_path(WEATHER_MAP_IMAGE_PATH)}`"
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
    status_by_key: dict[str, WeatherDatasetStatus],
    selection_state: WeatherSelectionState,
) -> WeatherDataset | None:
    """Rendert die Standort- und Datensatzauswahl und gibt den Datensatz zurueck."""
    selectable_active_datasets = [
        dataset
        for dataset in catalog.active_datasets()
        if status_by_key.get(dataset.weather_key) is None
        or status_by_key[dataset.weather_key].is_regularly_selectable
    ]
    left_column, right_column = st.columns([1, 2])
    with left_column:
        _render_weather_map()

    with right_column:
        if location_catalog is None:
            st.warning("Der Standortkatalog konnte nicht geladen werden. Es werden alle aktiven Datensaetze angezeigt.")
            selectable_datasets = selectable_active_datasets
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
            selectable_datasets = [
                dataset
                for dataset in catalog.datasets_for_location(
                    location_id=selected_location.location_id,
                    reference_location_id=reference_location.location_id,
                )
                if status_by_key.get(dataset.weather_key) is None
                or status_by_key[dataset.weather_key].is_regularly_selectable
            ]
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
            format_func=lambda key: weather_dataset_label(
                datasets_by_key[key],
                status_by_key.get(key),
                selection_state,
            ),
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


def weather_status_rows(statuses: list[WeatherDatasetStatus]) -> list[dict[str, object]]:
    """Bereitet Datensatzstatus fuer die offene Wetterdatensatz-Tabelle vor."""
    rows: list[dict[str, object]] = []
    for status in statuses:
        rows.append(
            {
                "weather_key": status.weather_key,
                "Name": status.display_name,
                "Status": status.status_label,
                "Datei vorhanden": status.file_exists,
                "Pruefstatus": status.import_status.value,
                "Freigabestatus": status.release_status.value if status.release_status else "",
                "Import-ID": status.import_id,
                "Session-ID": status.session_id,
                "Run-ID": status.run_id,
                "Quellen-ID": status.source_id,
                "Stundenwerte": status.row_count if status.row_count is not None else "",
                "Warnungen": status.warning_count,
                "Fehler": status.error_count,
                "Datei": str(status.file_path),
                "Hinweise": "; ".join(status.messages),
            }
        )
    return rows


def weather_event_rows(events: tuple[WeatherEvent, ...] | list[WeatherEvent]) -> list[dict[str, object]]:
    """Bereitet kritische Wetterereignisse fuer Streamlit auf."""
    return build_weather_event_rows(events)


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


def _effective_release_status(result: WeatherAnalysisResult) -> ReleaseStatus:
    stored_decision = st.session_state.get(WEATHER_RELEASE_DECISION_SESSION_KEY)
    if release_decision_matches_result(stored_decision, result):
        return stored_decision.resulting_status
    if result.release_decision is not None:
        return result.release_decision.resulting_status
    return result.validation_report.validation_result.release_status


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


def _render_activation_controls(
    result: WeatherAnalysisResult,
    selection_state: WeatherSelectionState,
) -> None:
    st.markdown("**Aktivierung und Projekt-Default**")
    release_status = _effective_release_status(result)
    weather_key = result.dataset.weather_key
    activation = selection_state.activation_for(weather_key)

    if activation is not None:
        st.success(f"Datensatz ist aktiviert. Import-ID: {activation.import_id or 'ohne Import-ID'}")
    elif release_status is ReleaseStatus.RELEASED:
        if st.button("Datensatz aktivieren", key=f"weather_activate_{result.import_id}"):
            try:
                new_state = activate_weather_dataset(
                    selection_state,
                    weather_key,
                    release_status=release_status,
                    import_id=result.import_id,
                )
                _store_weather_selection_state(new_state)
            except (OSError, ValueError) as exc:
                st.error(f"Datensatz konnte nicht aktiviert werden: {exc}")
            else:
                st.rerun()
    elif release_status is ReleaseStatus.CONFIRMATION_REQUIRED:
        st.info("Aktivierung ist erst nach bewusster Freigabe der Warnungen moeglich.")
    else:
        st.warning("Dieser Datensatz ist blockiert und kann nicht aktiviert werden.")

    selection_state = get_weather_selection_state(st.session_state)
    if selection_state.is_activated(weather_key):
        if selection_state.project_default_weather_key == weather_key:
            st.success("Dieser Datensatz ist aktuell der Projekt-Default.")
        elif st.button("Als Projekt-Default setzen", key=f"weather_default_{weather_key}"):
            try:
                new_state = set_project_default_weather_dataset(selection_state, weather_key)
                _store_weather_selection_state(new_state)
            except (OSError, ValueError) as exc:
                st.error(f"Projekt-Default konnte nicht gesetzt werden: {exc}")
            else:
                st.rerun()
    else:
        st.caption("Projekt-Default ist erst nach Aktivierung moeglich.")


def _render_open_weather_datasets(status_by_key: dict[str, WeatherDatasetStatus]) -> None:
    open_statuses = [status for status in status_by_key.values() if status.is_open]
    st.subheader("Offene Wetterdatensaetze")
    if not open_statuses:
        st.success("Keine offenen, fehlenden oder blockierten Wetterdatensaetze im aktuellen Status.")
        return
    st.dataframe(
        normalize_table_for_streamlit(weather_status_rows(open_statuses)),
        hide_index=True,
        width="stretch",
    )


def _render_critical_weather_events(result: WeatherAnalysisResult) -> None:
    st.markdown("**Kritische Wetterereignisse**")
    if not result.critical_events:
        st.info("Fuer diesen Datensatz wurden keine kritischen Wetterereignisse erkannt.")
        return
    rows = weather_event_rows(result.critical_events)
    st.dataframe(
        normalize_table_for_streamlit(rows),
        hide_index=True,
        width="stretch",
    )
    events_by_id = {event.event_id: event for event in result.critical_events}
    selected_event_id = st.selectbox(
        "Ereignis fuer spaetere P021-Nutzung vormerken",
        options=tuple(events_by_id),
        format_func=lambda event_id: f"{events_by_id[event_id].event_type} ({events_by_id[event_id].start_time:%Y-%m-%d})",
        key=f"weather_event_selection_{result.run_id}",
    )
    selected_event = events_by_id[selected_event_id]
    st.caption(
        "Vorgemerkt fuer spaetere P021-Anbindung: "
        f"{selected_event.event_id}. Es erfolgt in diesem Slice keine automatische Uebergabe."
    )


def _render_weather_analysis_result(
    result: WeatherAnalysisResult,
    selection_state: WeatherSelectionState,
) -> None:
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
    _render_activation_controls(result, selection_state)

    st.markdown("**Kennwerte**")
    st.dataframe(normalize_table_for_streamlit(weather_metric_rows(result.metrics)), hide_index=True, width="stretch")
    _render_critical_weather_events(result)

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
    selection_state = get_weather_selection_state(st.session_state)
    result = st.session_state.get(WEATHER_RESULT_SESSION_KEY)
    status_by_key = _current_status_map(catalog, result)

    st.subheader("Standort und Wetterauswahl")
    if st.button("Bestand und Validierung pruefen", width="stretch"):
        with st.spinner("Katalogisierte Wetterdateien werden geprueft..."):
            st.session_state[WEATHER_STATUS_SESSION_KEY] = inspect_weather_catalog_statuses(
                catalog,
                validate_files=True,
            )
        st.rerun()

    if not active_datasets:
        st.info("Im Wetterkatalog ist aktuell kein aktiver Wetterdatensatz vorhanden.")
        st.subheader("Wetterdatensaetze")
        st.metric("Aktive Wetterdatensaetze", active_count)
        st.dataframe(
            normalize_table_for_streamlit(
                weather_dataset_rows(
                    catalog.datasets,
                    status_by_key=status_by_key,
                    selection_state=selection_state,
                )
            ),
            hide_index=True,
            width="stretch",
        )
        return

    selected_dataset = _render_weather_selection(catalog, location_catalog, status_by_key, selection_state)
    if selected_dataset is None:
        st.subheader("Wetterdatensaetze")
        st.metric("Aktive Wetterdatensaetze", active_count)
        st.dataframe(
            normalize_table_for_streamlit(
                weather_dataset_rows(
                    catalog.datasets,
                    status_by_key=status_by_key,
                    selection_state=selection_state,
                )
            ),
            hide_index=True,
            width="stretch",
        )
        _render_open_weather_datasets(status_by_key)
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
                status_by_key[result.dataset.weather_key] = weather_status_from_analysis_result(result)

    result = st.session_state.get(WEATHER_RESULT_SESSION_KEY)
    if isinstance(result, WeatherAnalysisResult):
        if result.dataset.weather_key == selected_dataset.weather_key:
            _render_weather_analysis_result(result, selection_state)
            status_by_key = _current_status_map(catalog, result)
        else:
            st.info(
                "Es liegt ein Analyseergebnis fuer einen anderen Wetterdatensatz vor. "
                "Starte die Analyse fuer die aktuelle Auswahl neu."
            )

    st.subheader("Wetterdatensaetze")
    st.metric("Aktive Wetterdatensaetze", active_count)
    st.dataframe(
        normalize_table_for_streamlit(
            weather_dataset_rows(
                catalog.datasets,
                status_by_key=status_by_key,
                selection_state=get_weather_selection_state(st.session_state),
            )
        ),
        hide_index=True,
        width="stretch",
    )
    _render_open_weather_datasets(status_by_key)
