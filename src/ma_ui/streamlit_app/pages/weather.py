"""Wetterdaten-Seite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

from pathlib import Path
from typing import MutableMapping

import streamlit as st

from ma_core import create_session_id
from ma_ui.streamlit_app.shared import normalize_table_for_streamlit
from ma_validation import (
    ReleaseChoice,
    ReleaseDecision,
    ReleaseStatus,
)
from ma_weather import (
    ALL_WEATHER_PLOTS,
    DWD_TRY_URL,
    WEATHER_PLOT_CHOICES,
    WEATHER_PLOT_SPECS,
    WeatherAnalysisResult,
    WeatherDataset,
    WeatherDatasetStatus,
    WeatherDiscoveryValidationResult,
    WeatherEvent,
    WeatherFileDiscovery,
    WeatherLocation,
    WeatherLocationCatalog,
    WeatherMetrics,
    WeatherPlotResult,
    WeatherRegion,
    WeatherSelectionState,
    activate_weather_dataset,
    discover_weather_input_files,
    import_weather_catalog,
    import_weather_location_catalog,
    infer_weather_start_year,
    inspect_weather_catalog_statuses,
    inspect_weather_dataset_status,
    load_weather_selection_state,
    plot_template_weather,
    record_weather_release_decision,
    register_discovered_weather_dataset,
    save_weather_selection_state,
    set_project_default_weather_dataset,
    stage_weather_input_file,
    stale_weather_status,
    update_weather_file_discovery,
    validate_weather_file_discovery,
    weather_status_file_changed,
    weather_status_from_analysis_result,
    weather_statuses_by_key,
)
from ma_weather import (
    weather_event_rows as build_weather_event_rows,
)
from ma_weather.weather_catalog import DATASET_ROLE_SITE_SPECIFIC, DATASET_ROLE_TRY_REFERENCE

WEATHER_RESULT_SESSION_KEY = "ma_ui_weather_analysis_result"
WEATHER_KEY_WIDGET_KEY = "ma_ui_weather_key"
WEATHER_PLOT_WIDGET_KEY = "ma_ui_weather_plot_template"
WEATHER_LOCATION_WIDGET_KEY = "ma_ui_weather_location"
WEATHER_REGION_WIDGET_KEY = "ma_ui_weather_region"
WEATHER_SELECTION_MODE_WIDGET_KEY = "ma_ui_weather_selection_mode"
WEATHER_DATASET_TYPE_WIDGET_KEY = "ma_ui_weather_dataset_type"
WEATHER_SESSION_ID_SESSION_KEY = "ma_ui_weather_session_id"
WEATHER_RELEASE_DECISION_SESSION_KEY = "ma_ui_weather_release_decision"
WEATHER_RELEASE_NOTE_WIDGET_KEY = "ma_ui_weather_release_note"
WEATHER_STATUS_SESSION_KEY = "ma_ui_weather_dataset_statuses"
WEATHER_SELECTION_STATE_SESSION_KEY = "ma_ui_weather_selection_state"
WEATHER_IMPORT_MESSAGE_SESSION_KEY = "ma_ui_weather_import_message"
WEATHER_DATASET_ACTION_SESSION_KEY = "ma_ui_weather_dataset_action"
WEATHER_DISCOVERY_SESSION_KEY = "ma_ui_weather_discoveries"
WEATHER_DISCOVERY_MESSAGE_SESSION_KEY = "ma_ui_weather_discovery_message"
WEATHER_DISCOVERY_VALIDATION_SESSION_KEY = "ma_ui_weather_discovery_validation"
WEATHER_ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "weather"
WEATHER_MAP_IMAGE_PATH = WEATHER_ASSET_DIR / "klimaregionen_deutschland.png"
WEATHER_MAP_IMAGE_CANDIDATES = (
    WEATHER_MAP_IMAGE_PATH,
    WEATHER_ASSET_DIR / "klimaregionen_deutschland.jpg",
    WEATHER_ASSET_DIR / "klimaregionen_deutschland.jpeg",
    Path(__file__).resolve().parents[1] / "assets" / "weather" / "klimaregionen_deutschland.png",
    Path(__file__).resolve().parents[1] / "assets" / "weather" / "klimaregionen_deutschland.jpg",
    Path(__file__).resolve().parents[1] / "assets" / "weather" / "klimaregionen_deutschland.jpeg",
)
LOCAL_IMPORT_SOURCE_LABEL = "Lokaler Import"
LOCAL_IMPORT_PATH_PREFIX = "data/ma_weather/input/custom/"

WEATHER_YEAR_TYPE_LABELS = {
    "reference_year": "Jahr",
    "future_year": "Jahr",
    "summer_extreme": "Sommer",
    "winter_extreme": "Winter",
}
WEATHER_SELECTION_MODE_CITY = "Stadt"
WEATHER_SELECTION_MODE_REGION = "Klimaregion"
WEATHER_SELECTION_MODE_OPTIONS = (WEATHER_SELECTION_MODE_CITY, WEATHER_SELECTION_MODE_REGION)
WEATHER_DATASET_TYPE_FILTER_OPTIONS = ("Jahr", "Sommer", "Winter")
GENERATED_DISCOVERY_FIELDS = {
    "dataset_role",
    "display_name",
    "weather_key",
}
DISCOVERY_FIELD_LABELS = {
    "climate_scenario": "Szenario",
    "dataset_type": "Datensatztyp",
    "location_id": "Stadt",
    "location_resolution": "Standortaufloesung",
    "try_folder_key": "TRY-Ordner",
    "try_id": "TRY-ID",
    "year": "Bezugsjahr",
    "year_type": "Jahrtyp",
}

WEATHER_IMPORT_TYPE_OPTIONS = {
    "Jahr": "reference_year",
    "Sommer": "summer_extreme",
    "Winter": "winter_extreme",
}

WEATHER_IMPORT_SCENARIO_OPTIONS = {
    "Gegenwart": "present",
    "Zukunft 2045": "future_2045",
}

WEATHER_IMPORT_ROLE_OPTIONS = {
    "Standortgenauer Datensatz": DATASET_ROLE_SITE_SPECIFIC,
    "TRY-Referenzdatensatz": DATASET_ROLE_TRY_REFERENCE,
}

WEATHER_DATASET_ACTION_IMPORT = "Import"
WEATHER_DATASET_ACTION_SCAN = "Scannen"
WEATHER_DATASET_ACTION_VALIDATE_LEGACY = "Validieren"
WEATHER_DATASET_ACTION_VALIDATE = "Pruefen"
WEATHER_DATASET_ACTIONS = (
    WEATHER_DATASET_ACTION_IMPORT,
    WEATHER_DATASET_ACTION_SCAN,
    WEATHER_DATASET_ACTION_VALIDATE,
)
WEATHER_VALIDATION_VIEW_OPEN = "Gefundene lokale TRY-Dateien"
WEATHER_VALIDATION_VIEW_KEYS = "Parameter pruefen"
WEATHER_VALIDATION_VIEWS = (
    WEATHER_VALIDATION_VIEW_OPEN,
    WEATHER_VALIDATION_VIEW_KEYS,
)
WEATHER_DISCOVERY_OVERVIEW_COLUMNS = (
    "Datei",
    "Status",
    "Ort / Vorschlag",
    "Jahr",
    "Typ",
    "Szenario",
    "Offene Punkte",
)
WEATHER_DATASET_DEFAULT_COLUMNS = (
    "Name",
    "Ort",
    "Quelle",
    "Jahrtyp",
    "Datensatztyp",
    "Szenario",
)
WEATHER_PLOT_OPTIONS = (ALL_WEATHER_PLOTS, *WEATHER_PLOT_CHOICES)
WEATHER_PLOT_LABELS = {
    ALL_WEATHER_PLOTS: "Alle Wetterdiagramme",
    **{spec.plot_key: spec.label for spec in WEATHER_PLOT_SPECS},
}


def weather_plot_label(plot_key: str) -> str:
    """Gibt einen lesbaren Namen fuer einen Wetterdiagramm-Schluessel zurueck."""
    return WEATHER_PLOT_LABELS.get(plot_key, plot_key)


def normalize_weather_plot_key(plot_key: object) -> str:
    """Normalisiert alte Session-State-Werte auf einen bekannten Diagramm-Schluessel."""
    return str(plot_key) if plot_key in WEATHER_PLOT_OPTIONS else ALL_WEATHER_PLOTS


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
                "Standortquelle": dataset.location_resolution_source,
                "Standortaufloesung": dataset.location_resolution_status,
                "Gemeinde": dataset.detected_municipality_name,
                "AGS": dataset.detected_municipality_code,
                "Bundesland": dataset.detected_federal_state,
                "PLZ": dataset.detected_postal_code,
                "Geodatenquelle": dataset.geodata_source_id,
                "Hinweise": dataset.notes,
            }
        )
    return rows


def _weather_dataset_default_table(rows: list[dict[str, object]]):
    """Reduziert die aktive Datensatztabelle auf die fachliche Standardansicht."""
    table = normalize_table_for_streamlit(rows)
    visible_columns = [column for column in WEATHER_DATASET_DEFAULT_COLUMNS if column in table.columns]
    return table.loc[:, visible_columns]


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


def _datasets_for_weather_dataset_type(
    datasets: list[WeatherDataset],
    dataset_type: str,
) -> list[WeatherDataset]:
    """Filtert Datensaetze fuer die kompakte Auswahl nach Jahr, Sommer oder Winter."""
    return [
        dataset
        for dataset in datasets
        if weather_dataset_type_label(dataset) == dataset_type
    ]


def weather_dataset_label(
    dataset: WeatherDataset,
    status: WeatherDatasetStatus | None = None,
    selection_state: WeatherSelectionState | None = None,
) -> str:
    """Baut eine kompakte Auswahlbeschriftung fuer Wetterdatensaetze."""
    _ = status, selection_state
    return dataset.display_name


def weather_location_label(location: WeatherLocation) -> str:
    """Baut eine kompakte Auswahlbeschriftung fuer Staedte."""
    if location.legacy_code:
        return f"{location.location_name} ({location.legacy_code})"
    return location.location_name


def weather_region_label(region: WeatherRegion) -> str:
    """Baut eine kompakte Auswahlbeschriftung fuer Klimaregionen."""
    return _weather_region_display_code(region)


def _weather_region_display_code(region: WeatherRegion) -> str:
    """Kuerzt TRY12 in der Auswahlansicht zu 12."""
    region_code = region.region_code.strip()
    if region_code.upper().startswith("TRY") and region_code[3:].isdigit():
        return region_code[3:]
    return region_code


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
        ("Run-Ordner", result.run_output_dir),
        ("Aufbereitete Wetterdaten", result.processed_data_path),
        ("Markdown-Bericht", result.report_path),
        ("Run-Manifest", result.manifest_path),
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


def _dataset_needs_startup_validation(dataset: WeatherDataset) -> bool:
    """Validiert lokale UI-Imports direkt, damit offene Datensaetze nicht regulaer wirken."""
    normalized_path = dataset.file_path.as_posix().replace("\\", "/")
    return dataset.source == LOCAL_IMPORT_SOURCE_LABEL or normalized_path.startswith(LOCAL_IMPORT_PATH_PREFIX)


def _is_dataset_regularly_selectable(
    dataset: WeatherDataset,
    status_by_key: dict[str, WeatherDatasetStatus],
) -> bool:
    status = status_by_key.get(dataset.weather_key)
    return status is None or status.is_regularly_selectable


def _regularly_selectable_datasets(
    datasets: list[WeatherDataset],
    status_by_key: dict[str, WeatherDatasetStatus],
) -> list[WeatherDataset]:
    return [dataset for dataset in datasets if _is_dataset_regularly_selectable(dataset, status_by_key)]


def _base_statuses(catalog: object) -> list[WeatherDatasetStatus]:
    return [
        inspect_weather_dataset_status(
            dataset,
            validate_file=_dataset_needs_startup_validation(dataset),
        )
        for dataset in catalog.datasets
    ]


def _stored_statuses() -> list[WeatherDatasetStatus]:
    statuses = st.session_state.get(WEATHER_STATUS_SESSION_KEY)
    if isinstance(statuses, list) and all(isinstance(status, WeatherDatasetStatus) for status in statuses):
        return statuses
    return []


def _render_weather_import_message() -> None:
    message = st.session_state.pop(WEATHER_IMPORT_MESSAGE_SESSION_KEY, None)
    if not isinstance(message, tuple) or len(message) != 2:
        return
    message_type, text = message
    if message_type == "error":
        st.error(str(text))
    elif message_type == "warning":
        st.warning(str(text))
    else:
        st.success(str(text))


def _store_weather_discovery_message(message_type: str, text: str) -> None:
    st.session_state[WEATHER_DISCOVERY_MESSAGE_SESSION_KEY] = (message_type, text)


def _render_weather_discovery_message() -> None:
    message = st.session_state.pop(WEATHER_DISCOVERY_MESSAGE_SESSION_KEY, None)
    if not isinstance(message, tuple) or len(message) != 2:
        return
    message_type, text = message
    if message_type == "error":
        st.error(str(text))
    elif message_type == "warning":
        st.warning(str(text))
    else:
        st.success(str(text))


def _stored_weather_discoveries() -> list[WeatherFileDiscovery]:
    discoveries = st.session_state.get(WEATHER_DISCOVERY_SESSION_KEY)
    if isinstance(discoveries, list) and all(isinstance(item, WeatherFileDiscovery) for item in discoveries):
        return discoveries
    return []


def _stored_weather_discovery_validation() -> WeatherDiscoveryValidationResult | None:
    result = st.session_state.get(WEATHER_DISCOVERY_VALIDATION_SESSION_KEY)
    if isinstance(result, WeatherDiscoveryValidationResult):
        return result
    return None


def _set_weather_dataset_action(action: str) -> None:
    if action == WEATHER_DATASET_ACTION_VALIDATE_LEGACY:
        action = WEATHER_DATASET_ACTION_VALIDATE
    if action in WEATHER_DATASET_ACTIONS:
        st.session_state[WEATHER_DATASET_ACTION_SESSION_KEY] = action


def _active_weather_dataset_action() -> str:
    action = st.session_state.get(WEATHER_DATASET_ACTION_SESSION_KEY)
    if action == WEATHER_DATASET_ACTION_VALIDATE_LEGACY:
        st.session_state[WEATHER_DATASET_ACTION_SESSION_KEY] = WEATHER_DATASET_ACTION_VALIDATE
        return WEATHER_DATASET_ACTION_VALIDATE
    if isinstance(action, str) and action in WEATHER_DATASET_ACTIONS:
        return action
    return ""


def _toggle_weather_dataset_action(action: str) -> None:
    """Oeffnet oder schliesst eine Datensatz-Arbeitsansicht."""
    if action == WEATHER_DATASET_ACTION_VALIDATE_LEGACY:
        action = WEATHER_DATASET_ACTION_VALIDATE
    if action not in WEATHER_DATASET_ACTIONS:
        return
    if _active_weather_dataset_action() == action:
        st.session_state.pop(WEATHER_DATASET_ACTION_SESSION_KEY, None)
        return
    _set_weather_dataset_action(action)


def _option_index_or_none(options: tuple[str, ...], value: str) -> int | None:
    return options.index(value) if value in options else None


def _option_label_for_value(options: dict[str, str], value: str) -> str:
    for label, option_value in options.items():
        if option_value == value:
            return label
    return ""


def _editor_rows_as_records(edited_rows: object) -> list[dict[str, object]]:
    if hasattr(edited_rows, "to_dict"):
        records = edited_rows.to_dict("records")
        return [dict(record) for record in records]
    if isinstance(edited_rows, list):
        return [dict(record) for record in edited_rows if isinstance(record, MutableMapping)]
    return []


def _key_parameter_value(rows: list[dict[str, object]], field_name: str) -> str:
    for row in rows:
        if str(row.get("Feld", "")).strip() == field_name:
            return str(row.get("Wert", row.get("Zielwert", ""))).strip()
    return ""


def _location_editor_value(location_id: str, locations_by_id: dict[str, WeatherLocation]) -> str:
    location = locations_by_id.get(location_id)
    if location is None:
        return ""
    return f"{location.location_id} - {location.location_name}"


def _location_id_from_editor_value(value: str, locations_by_id: dict[str, WeatherLocation]) -> str:
    normalized_value = value.strip().casefold()
    if not normalized_value:
        return ""
    possible_id = value.split("-", maxsplit=1)[0].strip()
    for location_id, location in locations_by_id.items():
        candidates = {
            location_id.casefold(),
            location.location_name.casefold(),
            weather_location_label(location).casefold(),
            f"{location.location_id} - {location.location_name}".casefold(),
        }
        if normalized_value in candidates or possible_id.casefold() == location_id.casefold():
            return location_id
    raise ValueError(f"Stadt konnte nicht zugeordnet werden: {value}")


def _dataset_type_from_editor_value(value: str) -> str:
    normalized_value = value.strip().casefold()
    if not normalized_value:
        return ""
    for label in WEATHER_IMPORT_TYPE_OPTIONS:
        if normalized_value == label.casefold():
            return label
    raise ValueError(f"Datensatztyp ist ungueltig: {value}")


def _option_value_from_editor_value(value: str, options: dict[str, str], field_name: str) -> str:
    normalized_value = value.strip().casefold()
    if not normalized_value:
        return ""
    for label, option_value in options.items():
        if normalized_value in {label.casefold(), option_value.casefold()}:
            return option_value
    raise ValueError(f"{field_name} ist ungueltig: {value}")


def _year_from_editor_value(value: str) -> int | None:
    if not value.strip():
        return None
    try:
        return int(value.strip())
    except ValueError as exc:
        raise ValueError("Bezugsjahr muss als ganze Jahreszahl eingetragen werden.") from exc


def _updated_discovery_from_key_parameter_rows(
    discovery: WeatherFileDiscovery,
    *,
    edited_rows: object,
    location_catalog: WeatherLocationCatalog,
    locations_by_id: dict[str, WeatherLocation],
) -> WeatherFileDiscovery:
    rows = _editor_rows_as_records(edited_rows)
    location_id = _location_id_from_editor_value(_key_parameter_value(rows, "Stadt"), locations_by_id)
    dataset_type = _dataset_type_from_editor_value(_key_parameter_value(rows, "Datensatztyp"))
    climate_scenario = _option_value_from_editor_value(
        _key_parameter_value(rows, "Szenario"),
        WEATHER_IMPORT_SCENARIO_OPTIONS,
        "Szenario",
    )
    year = _year_from_editor_value(_key_parameter_value(rows, "Bezugsjahr"))
    return update_weather_file_discovery(
        discovery,
        location_catalog=location_catalog,
        location_id=location_id,
        dataset_type=dataset_type,
        climate_scenario=climate_scenario,
        dataset_role="",
        year=year,
        weather_key="",
        display_name="",
    )


def _apply_location_suggestion_to_discovery(
    discovery: WeatherFileDiscovery,
    *,
    location_catalog: WeatherLocationCatalog,
) -> WeatherFileDiscovery:
    suggested_location_id = discovery.metadata.get("suggested_location_id", "")
    location = location_catalog.get_location(suggested_location_id)
    dataset_role = DATASET_ROLE_TRY_REFERENCE if location.is_reference_location else DATASET_ROLE_SITE_SPECIFIC
    return update_weather_file_discovery(
        discovery,
        location_catalog=location_catalog,
        location_id=location.location_id,
        dataset_type=discovery.dataset_type,
        climate_scenario=discovery.climate_scenario,
        dataset_role=dataset_role,
        year=discovery.year,
        weather_key=discovery.weather_key,
        display_name=discovery.display_name,
    )


def _replace_stored_weather_discovery(updated_discovery: WeatherFileDiscovery) -> None:
    discoveries = [
        discovery
        for discovery in _stored_weather_discoveries()
        if discovery.file_path != updated_discovery.file_path
    ]
    discoveries.append(updated_discovery)
    discoveries.sort(key=lambda discovery: discovery.file_path.as_posix())
    st.session_state[WEATHER_DISCOVERY_SESSION_KEY] = discoveries


def _remove_stored_weather_discovery(registered_discovery: WeatherFileDiscovery) -> None:
    st.session_state[WEATHER_DISCOVERY_SESSION_KEY] = [
        discovery
        for discovery in _stored_weather_discoveries()
        if discovery.file_path != registered_discovery.file_path
    ]
    stored_validation = _stored_weather_discovery_validation()
    if stored_validation and stored_validation.discovery.file_path == registered_discovery.file_path:
        st.session_state.pop(WEATHER_DISCOVERY_VALIDATION_SESSION_KEY, None)


def _current_status_map(
    catalog: object,
    result: object,
) -> dict[str, WeatherDatasetStatus]:
    status_map = weather_statuses_by_key(_base_statuses(catalog))
    for stored_status in _stored_statuses():
        current_status = status_map.get(stored_status.weather_key)
        if current_status is None:
            status_map[stored_status.weather_key] = stored_status
        elif weather_status_file_changed(stored_status, current_status):
            status_map[stored_status.weather_key] = stale_weather_status(current_status, stored_status)
        else:
            status_map[stored_status.weather_key] = stored_status
    if isinstance(result, WeatherAnalysisResult):
        stored_decision = st.session_state.get(WEATHER_RELEASE_DECISION_SESSION_KEY)
        decision = stored_decision if release_decision_matches_result(stored_decision, result) else None
        status_map[result.dataset.weather_key] = weather_status_from_analysis_result(result, decision=decision)
    return status_map


def _refresh_weather_catalog_state(*, validate_files: bool = True) -> None:
    """Laedt den Wetterkatalog neu und speichert aktuelle Datensatzstatus in der Sitzung."""
    refreshed_catalog = import_weather_catalog()
    st.session_state[WEATHER_STATUS_SESSION_KEY] = inspect_weather_catalog_statuses(
        refreshed_catalog,
        validate_files=validate_files,
    )
    st.session_state.pop(WEATHER_DISCOVERY_VALIDATION_SESSION_KEY, None)


def _run_weather_catalog_validation(catalog: object) -> None:
    """Prueft katalogisierte Wetterdateien und merkt den Status in der UI-Sitzung."""
    with st.spinner("Katalogisierte Wetterdateien werden geprueft..."):
        st.session_state[WEATHER_STATUS_SESSION_KEY] = inspect_weather_catalog_statuses(catalog, validate_files=True)
        st.session_state.pop(WEATHER_DISCOVERY_VALIDATION_SESSION_KEY, None)
    st.rerun()


def _run_weather_input_discovery(
    catalog: object,
    location_catalog: WeatherLocationCatalog | None,
) -> None:
    """Sucht neue TRY-Dateien und speichert Entwuerfe in der UI-Sitzung."""
    if location_catalog is None:
        _store_weather_discovery_message("error", "Standortkatalog ist fuer den lokalen TRY-Dateiscan erforderlich.")
        return
    try:
        with st.spinner("Lokale TRY-Dateien werden gesucht..."):
            discoveries = discover_weather_input_files(
                existing_catalog=catalog,
                location_catalog=location_catalog,
            )
    except (OSError, ValueError) as exc:
        _store_weather_discovery_message("error", f"Lokaler TRY-Dateiscan fehlgeschlagen: {exc}")
        return

    st.session_state[WEATHER_DISCOVERY_SESSION_KEY] = discoveries
    ready_count = sum(1 for discovery in discoveries if discovery.is_complete)
    open_count = len(discoveries) - ready_count
    if discoveries:
        _store_weather_discovery_message(
            "success" if open_count == 0 else "warning",
            f"Lokaler TRY-Dateiscan abgeschlossen: {ready_count} vollstaendig, {open_count} offen.",
        )
    else:
        _store_weather_discovery_message("success", "Keine neuen lokalen TRY-Dateien gefunden.")


def _render_weather_dataset_actions(
    catalog: object,
    location_catalog: WeatherLocationCatalog | None,
) -> None:
    """Zeigt die Datensatzaktionen gemeinsam im Wetterdatensatzbereich."""
    import_column, scan_column, validation_column = st.columns(3)
    with import_column:
        show_import = st.button(
            WEATHER_DATASET_ACTION_IMPORT,
            key="ma_ui_weather_import_toggle",
            width="stretch",
        )
    with scan_column:
        show_scan = st.button(
            WEATHER_DATASET_ACTION_SCAN,
            key="ma_ui_weather_discover_input_files",
            width="stretch",
        )
    with validation_column:
        show_validation = st.button(
            WEATHER_DATASET_ACTION_VALIDATE,
            key="ma_ui_weather_validate_catalog",
            width="stretch",
        )

    if show_import:
        _toggle_weather_dataset_action(WEATHER_DATASET_ACTION_IMPORT)
    if show_scan:
        _toggle_weather_dataset_action(WEATHER_DATASET_ACTION_SCAN)
    if show_validation:
        _toggle_weather_dataset_action(WEATHER_DATASET_ACTION_VALIDATE)

    if st.button(
        "Datensatzbestand pruefen",
        key="ma_ui_weather_check_dataset_inventory",
        width="stretch",
    ):
        _run_weather_catalog_validation(catalog)

    _render_weather_import_message()
    _render_weather_discovery_message()


def _render_weather_import_panel() -> None:
    if _active_weather_dataset_action() != WEATHER_DATASET_ACTION_IMPORT:
        return

    st.markdown("**Import**")
    st.link_button("TRY-Daten beim DWD oeffnen", DWD_TRY_URL)
    st.caption("Der Import legt die Datei nur lokal ab. Metadaten werden anschliessend ueber Scannen und Pruefen erzeugt.")
    with st.form("ma_ui_weather_stage_form"):
        uploaded_file = st.file_uploader("TRY-Datei (.dat)", type=("dat",), key="ma_ui_weather_import_file")
        submitted = st.form_submit_button("Datei lokal ablegen", type="primary", width="stretch")

    if not submitted:
        return
    if uploaded_file is None:
        st.error("Bitte zuerst eine entpackte TRY-.dat-Datei auswaehlen.")
        return
    try:
        staged_file = stage_weather_input_file(
            uploaded_file.getvalue(),
            original_filename=uploaded_file.name,
        )
    except (OSError, ValueError) as exc:
        st.error(f"TRY-Datei konnte nicht abgelegt werden: {exc}")
        return

    st.session_state[WEATHER_IMPORT_MESSAGE_SESSION_KEY] = (
        "success",
        f"TRY-Datei abgelegt: {staged_file.file_path.as_posix()}. Danach Scannen ausfuehren.",
    )
    _set_weather_dataset_action(WEATHER_DATASET_ACTION_SCAN)
    st.rerun()


def _discovery_location_overview_value(discovery: WeatherFileDiscovery) -> str:
    """Zeigt nur bestaetigte Standorte als Ort in der Entwurfsuebersicht."""
    if discovery.location_id and discovery.location_name:
        return discovery.location_name
    return "offen"


def _weather_discovery_overview_rows(discoveries: list[WeatherFileDiscovery]) -> list[dict[str, object]]:
    """Reduzierte Uebersicht fuer lokale TRY-Dateientwuerfe."""
    rows: list[dict[str, object]] = []
    for discovery in discoveries:
        rows.append(
            {
                "Datei": discovery.file_path.name,
                "Status": discovery.status.value,
                "Ort / Vorschlag": _discovery_location_overview_value(discovery),
                "Jahr": discovery.year if discovery.year is not None else "",
                "Typ": discovery.dataset_type,
                "Szenario": discovery.climate_scenario,
                "Offene Punkte": _visible_discovery_missing_fields(discovery),
            }
        )
    return rows


def _visible_discovery_missing_fields(discovery: WeatherFileDiscovery) -> str:
    """Zeigt nur fachlich relevante offene Entwurfspunkte in der UI."""
    visible_fields = [
        DISCOVERY_FIELD_LABELS.get(field_name, field_name)
        for field_name in discovery.missing_fields
        if field_name not in GENERATED_DISCOVERY_FIELDS
    ]
    return ", ".join(dict.fromkeys(visible_fields))


def _render_weather_discoveries(*, show_validation_hint: bool = False) -> None:
    """Zeigt gescannte lokale TRY-Dateien als Entwurfstabelle."""
    discoveries = _stored_weather_discoveries()
    if not discoveries:
        return

    st.markdown("**Gefundene lokale TRY-Dateien**")
    ready_discoveries = [discovery for discovery in discoveries if discovery.is_complete]
    open_discoveries = [discovery for discovery in discoveries if not discovery.is_complete]
    st.caption(
        f"{len(ready_discoveries)} vollstaendige Entwuerfe, "
        f"{len(open_discoveries)} offene Entwuerfe."
    )
    st.dataframe(
        normalize_table_for_streamlit(_weather_discovery_overview_rows(discoveries)),
        hide_index=True,
        width="stretch",
    )
    if show_validation_hint and ready_discoveries:
        st.info("Vollstaendige Entwuerfe werden im Schritt Pruefen geprueft und registriert.")


def _render_weather_scan_panel(
    catalog: object,
    location_catalog: WeatherLocationCatalog | None,
) -> None:
    if _active_weather_dataset_action() != WEATHER_DATASET_ACTION_SCAN:
        return

    st.markdown("**Scannen**")
    st.caption("Sucht neue TRY-Dateien unter `data/ma_weather/input/TRY_*` und erzeugt Datensatzentwuerfe.")
    if st.button("Lokale TRY-Dateien jetzt scannen", key="ma_ui_weather_rescan_input_files"):
        _run_weather_input_discovery(catalog, location_catalog)
    _render_weather_discoveries(show_validation_hint=True)


def _render_weather_validation_panel(
    catalog: object,
    location_catalog: WeatherLocationCatalog | None,
    status_by_key: dict[str, WeatherDatasetStatus],
) -> None:
    if _active_weather_dataset_action() != WEATHER_DATASET_ACTION_VALIDATE:
        return

    st.markdown("**Pruefen**")
    st.caption("Prueft lokale Datensatzentwuerfe vor der bewussten Registrierung.")

    discoveries = _stored_weather_discoveries()
    validation_view = st.radio(
        "Pruefansicht",
        options=WEATHER_VALIDATION_VIEWS,
        horizontal=True,
        key="ma_ui_weather_validation_view",
    )
    if validation_view == WEATHER_VALIDATION_VIEW_OPEN:
        if not discoveries:
            st.info("Keine Entwuerfe in der Sitzung. Bitte zuerst den Schritt Scannen ausfuehren.")
            return
        _render_weather_discoveries()
        return

    if not discoveries:
        st.info("Keine Entwuerfe in der Sitzung. Bitte zuerst den Schritt Scannen ausfuehren.")
        return
    if location_catalog is None:
        st.warning("Der Standortkatalog ist fuer die Entwurfsvalidierung erforderlich.")
        return

    discoveries_by_path = {discovery.file_path.as_posix(): discovery for discovery in discoveries}
    selected_path = st.selectbox(
        "Entwurf",
        options=tuple(discoveries_by_path),
        format_func=lambda path: f"{discoveries_by_path[path].weather_key or 'ohne weather_key'} - {path}",
        key="ma_ui_weather_validation_discovery",
    )
    selected_discovery = discoveries_by_path[selected_path]
    active_locations = location_catalog.active_locations()
    if not active_locations:
        st.info("Im Standortkatalog ist aktuell kein aktiver Standort vorhanden.")
        return
    locations_by_id = {location.location_id: location for location in active_locations}
    if selected_discovery.metadata.get("suggested_location_id") and not selected_discovery.location_id:
        suggestion_label = selected_discovery.metadata.get("suggested_location_name", "")
        if st.button(
            f"Koordinatenvorschlag uebernehmen: {suggestion_label}",
            key=f"ma_ui_weather_apply_mapping_suggestion_{selected_path}",
        ):
            try:
                updated_discovery = _apply_location_suggestion_to_discovery(
                    selected_discovery,
                    location_catalog=location_catalog,
                )
            except (KeyError, ValueError) as exc:
                st.error(f"Standortvorschlag konnte nicht uebernommen werden: {exc}")
                return
            _replace_stored_weather_discovery(updated_discovery)
            st.session_state.pop(WEATHER_DISCOVERY_VALIDATION_SESSION_KEY, None)
            _store_weather_discovery_message("success", "Standortvorschlag wurde in den Entwurf uebernommen.")
            st.rerun()

    st.markdown("**Parameter pruefen**")
    edited_rows = st.data_editor(
        normalize_table_for_streamlit(weather_discovery_key_parameter_rows(selected_discovery, locations_by_id)),
        hide_index=True,
        width="stretch",
        disabled=("Feld",),
        key=f"ma_ui_weather_key_parameter_editor_{selected_path}",
    )
    apply_submitted = st.button(
        "Aenderungen uebernehmen",
        key=f"ma_ui_weather_apply_discovery_changes_{selected_path}",
        width="stretch",
    )
    release_warnings = st.checkbox(
        "Warnungen fuer diesen Entwurf bewusst freigeben",
        key=f"ma_ui_weather_validate_release_warnings_{selected_path}",
    )
    validate_submitted = st.button(
        "Entwurf pruefen",
        key=f"ma_ui_weather_validate_discovery_button_{selected_path}",
        width="stretch",
    )

    validation_result = _stored_weather_discovery_validation()
    if apply_submitted:
        try:
            updated_discovery = _updated_discovery_from_key_parameter_rows(
                selected_discovery,
                edited_rows=edited_rows,
                location_catalog=location_catalog,
                locations_by_id=locations_by_id,
            )
        except ValueError as exc:
            st.error(str(exc))
            return
        _replace_stored_weather_discovery(updated_discovery)
        st.session_state.pop(WEATHER_DISCOVERY_VALIDATION_SESSION_KEY, None)
        _store_weather_discovery_message("success", "Aenderungen wurden in den Entwurf uebernommen.")
        st.rerun()

    if validate_submitted:
        try:
            validation_result = validate_weather_file_discovery(
                selected_discovery,
                existing_catalog=import_weather_catalog(),
                warnings_released=release_warnings,
            )
        except (OSError, ValueError) as exc:
            st.error(f"Entwurf konnte nicht validiert werden: {exc}")
            return
        st.session_state[WEATHER_DISCOVERY_VALIDATION_SESSION_KEY] = validation_result

    if validation_result is None or validation_result.discovery.file_path != selected_discovery.file_path:
        return

    _render_weather_discovery_validation_result(validation_result)
    if not validation_result.can_register:
        return

    if st.button(
        "Geprueften Entwurf registrieren",
        key=f"ma_ui_weather_register_validated_discovery_{selected_path}",
        type="primary",
    ):
        try:
            register_discovered_weather_dataset(
                validation_result.discovery,
                existing_catalog=import_weather_catalog(),
                is_active=True,
            )
        except (OSError, ValueError) as exc:
            _store_weather_discovery_message("error", f"Entwurf konnte nicht registriert werden: {exc}")
            return
        _remove_stored_weather_discovery(validation_result.discovery)
        with st.spinner("Datensatzbestand wird aktualisiert..."):
            _refresh_weather_catalog_state(validate_files=True)
        _store_weather_discovery_message(
            "success",
            f"Entwurf wurde aktiv registriert: {validation_result.discovery.weather_key}",
        )
        st.rerun()


def _render_weather_discovery_validation_result(result: WeatherDiscoveryValidationResult) -> None:
    status = result.dataset_status
    if status.error_count:
        st.error(f"Entwurf blockiert: {status.error_count} Fehler.")
    elif status.warning_count and not result.warnings_released:
        st.warning("Entwurf hat Warnungen und braucht eine bewusste Freigabe.")
    elif result.can_register:
        st.success("Entwurf ist validiert und kann registriert werden.")
    else:
        st.info("Entwurf ist geprueft, aber noch nicht registrierbar.")
    st.dataframe(
        normalize_table_for_streamlit(weather_status_rows([status])),
        hide_index=True,
        width="stretch",
    )
    if result.messages:
        st.caption("; ".join(result.messages))


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
        st.image(str(image_path), caption="Klimaregionen Deutschland", width="stretch")
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
    st.markdown(f"**Klimaregion:** {_weather_region_display_code(region)}")
    st.markdown(f"**Referenzstandort:** {reference_location.location_name}")
    return region, reference_location


def _render_region_context(
    location_catalog: WeatherLocationCatalog,
    selected_region: WeatherRegion,
) -> WeatherLocation:
    """Zeigt den Kontext einer direkt gewaehlten Klimaregion an."""
    reference_location = location_catalog.get_location(selected_region.reference_location_id)
    st.markdown(f"**Klimaregion:** {_weather_region_display_code(selected_region)}")
    st.markdown(f"**Referenzstandort:** {reference_location.location_name}")
    return reference_location


def _render_unselected_weather_context(selection_mode: str) -> tuple[None, bool]:
    """Haelt die Auswahlbereiche sichtbar, solange Standort oder Klimaregion fehlen."""
    if selection_mode == WEATHER_SELECTION_MODE_REGION:
        missing_message = "Bitte zuerst eine Klimaregion auswaehlen."
        missing_dataset_placeholder = "Noch keine Klimaregion ausgewaehlt"
    else:
        missing_message = "Bitte zuerst eine Stadt auswaehlen."
        missing_dataset_placeholder = "Noch keine Stadt ausgewaehlt"
    st.markdown("**Klimaregion:** -")
    st.markdown("**Referenzstandort:** -")
    st.info(missing_message)
    st.segmented_control(
        "Datensatztyp",
        options=WEATHER_DATASET_TYPE_FILTER_OPTIONS,
        selection_mode="single",
        default=WEATHER_DATASET_TYPE_FILTER_OPTIONS[0],
        required=True,
        disabled=True,
        key=f"{WEATHER_DATASET_TYPE_WIDGET_KEY}_placeholder",
        width="stretch",
    )
    st.selectbox(
        "Wetterdatensatz",
        options=(missing_dataset_placeholder,),
        disabled=True,
        key=f"{WEATHER_KEY_WIDGET_KEY}_placeholder",
    )
    st.selectbox(
        "Wetterdiagramm",
        options=(weather_plot_label(ALL_WEATHER_PLOTS),),
        disabled=True,
        key=f"{WEATHER_PLOT_WIDGET_KEY}_placeholder",
    )
    st.button("Wetteranalyse starten", type="primary", disabled=True)
    return None, False


def _render_weather_selection(
    catalog: object,
    location_catalog: WeatherLocationCatalog | None,
    status_by_key: dict[str, WeatherDatasetStatus],
    selection_state: WeatherSelectionState,
) -> tuple[WeatherDataset | None, bool]:
    """Rendert die Standort- und Datensatzauswahl und gibt den Datensatz zurueck."""
    selectable_active_datasets = _regularly_selectable_datasets(catalog.active_datasets(), status_by_key)
    left_column, right_column = st.columns([1, 2])
    with left_column:
        _render_weather_map()

    with right_column:
        if location_catalog is None:
            st.warning("Der Standortkatalog konnte nicht geladen werden. Es werden alle aktiven Datensaetze angezeigt.")
            selectable_datasets = selectable_active_datasets
        else:
            selection_mode = st.segmented_control(
                "Auswahl",
                options=WEATHER_SELECTION_MODE_OPTIONS,
                selection_mode="single",
                default=WEATHER_SELECTION_MODE_CITY,
                required=True,
                key=WEATHER_SELECTION_MODE_WIDGET_KEY,
                width="stretch",
            )
            selection_mode = selection_mode or WEATHER_SELECTION_MODE_CITY
            active_locations = location_catalog.active_locations()
            if selection_mode == WEATHER_SELECTION_MODE_REGION:
                active_regions = location_catalog.active_regions()
                if not active_regions:
                    st.info("Im Standortkatalog ist aktuell keine aktive Klimaregion vorhanden.")
                    return None, False
                regions_by_id = {region.region_id: region for region in active_regions}
                selected_region_id = st.selectbox(
                    "Klimaregion",
                    options=tuple(regions_by_id),
                    format_func=lambda region_id: weather_region_label(regions_by_id[region_id]),
                    index=None,
                    placeholder="Klimaregion auswaehlen",
                    key=WEATHER_REGION_WIDGET_KEY,
                )
                if selected_region_id is None:
                    return _render_unselected_weather_context(WEATHER_SELECTION_MODE_REGION)
                selected_region = regions_by_id[selected_region_id]
                reference_location = _render_region_context(location_catalog, selected_region)
                selectable_datasets = _regularly_selectable_datasets(
                    catalog.datasets_for_reference_location(reference_location_id=reference_location.location_id),
                    status_by_key,
                )
                selection_help_text = (
                    "Bei Klimaregionsauswahl werden nur Referenzdatensaetze der gewaehlten Klimaregion angeboten."
                )
            else:
                if not active_locations:
                    st.info("Im Standortkatalog ist aktuell kein aktiver Standort vorhanden.")
                    return None, False
                locations_by_id = {location.location_id: location for location in active_locations}
                selected_location_id = st.selectbox(
                    "Stadt",
                    options=tuple(locations_by_id),
                    format_func=lambda location_id: weather_location_label(locations_by_id[location_id]),
                    index=None,
                    placeholder="Stadt auswaehlen",
                    key=WEATHER_LOCATION_WIDGET_KEY,
                )
                if selected_location_id is None:
                    return _render_unselected_weather_context(WEATHER_SELECTION_MODE_CITY)
                selected_location = locations_by_id[selected_location_id]
                _, reference_location = _render_location_context(location_catalog, selected_location)
                selectable_datasets = _regularly_selectable_datasets(
                    catalog.datasets_for_location(
                        location_id=selected_location.location_id,
                        reference_location_id=reference_location.location_id,
                    ),
                    status_by_key,
                )
                selection_help_text = (
                    "Bei Stadtauswahl werden standortgenaue Datensaetze bevorzugt; "
                    "der Referenzdatensatz der Klimaregion bleibt als Vergleich verfuegbar."
                )

        selected_dataset_type = st.segmented_control(
            "Datensatztyp",
            options=WEATHER_DATASET_TYPE_FILTER_OPTIONS,
            selection_mode="single",
            default=WEATHER_DATASET_TYPE_FILTER_OPTIONS[0],
            required=True,
            key=WEATHER_DATASET_TYPE_WIDGET_KEY,
            width="stretch",
        )
        selected_dataset_type = selected_dataset_type or WEATHER_DATASET_TYPE_FILTER_OPTIONS[0]
        selectable_datasets = _datasets_for_weather_dataset_type(selectable_datasets, selected_dataset_type)
        if location_catalog is not None:
            st.caption(selection_help_text)
        if location_catalog is not None and not _try_reference_datasets(selectable_datasets):
            st.info("Fuer diesen Referenzstandort ist noch kein aktiver Referenzdatensatz katalogisiert.")

        if not selectable_datasets:
            st.warning("Fuer die aktuelle Auswahl ist kein eindeutig zugeordneter aktiver Wetterdatensatz vorhanden.")
            return None, False

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
        selected_dataset = datasets_by_key[selected_key]
        st.session_state[WEATHER_PLOT_WIDGET_KEY] = normalize_weather_plot_key(
            st.session_state.get(WEATHER_PLOT_WIDGET_KEY)
        )
        st.selectbox(
            "Wetterdiagramm",
            options=WEATHER_PLOT_OPTIONS,
            format_func=weather_plot_label,
            key=WEATHER_PLOT_WIDGET_KEY,
        )
        selected_path = selected_dataset.resolved_file_path()
        file_exists = selected_path.exists()
        start_analysis = st.button("Wetteranalyse starten", type="primary", disabled=not file_exists)
        if not file_exists:
            st.warning(
                "Die lokale TRY-Datei wurde nicht gefunden. "
                "Die Analyse kann erst nach dem Ablegen der Datei starten."
            )
        return selected_dataset, start_analysis


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
                "Typ": "Katalogdatensatz",
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


def weather_open_discovery_rows(discoveries: list[WeatherFileDiscovery]) -> list[dict[str, object]]:
    """Bereitet unregistrierte Scan-Entwuerfe fuer die offene Uebersicht auf."""
    rows: list[dict[str, object]] = []
    for discovery in discoveries:
        rows.append(
            {
                "Typ": "Scan-Entwurf",
                "weather_key": discovery.weather_key,
                "Name": discovery.display_name,
                "Status": discovery.status.value,
                "Datei vorhanden": (Path.cwd() / discovery.file_path).exists(),
                "Pruefstatus": "discovery",
                "Freigabestatus": "",
                "Import-ID": "",
                "Session-ID": "",
                "Run-ID": "",
                "Quellen-ID": "",
                "Stundenwerte": "",
                "Warnungen": 0,
                "Fehler": len(discovery.missing_fields),
                "Datei": discovery.file_path.as_posix(),
                "Offene Punkte": _visible_discovery_missing_fields(discovery),
                "Hinweise": "; ".join(discovery.messages),
            }
        )
    return rows


def weather_discovery_file_value_rows(discovery: WeatherFileDiscovery) -> list[dict[str, object]]:
    """Zeigt die aus Datei, Pfad und TRY-Kopf gelesenen Entwurfswerte."""
    metadata = discovery.metadata
    values = [
        ("Dateiname", discovery.file_path.name, "Dateipfad"),
        ("Relativer Pfad", discovery.file_path.as_posix(), "Dateipfad"),
        ("TRY-Ordner", discovery.try_folder_key, "Dateipfad"),
        ("TRY-ID", discovery.try_id, "Dateipfad"),
        ("Bezugsjahr", discovery.year if discovery.year is not None else "", "Dateiname"),
        ("Datensatztyp", discovery.dataset_type, "Dateiname"),
        ("Jahrtyp", discovery.year_type, "Dateiname"),
        ("Szenario", discovery.climate_scenario, "Dateiname"),
        ("Rechtswert", metadata.get("rechtswert_m", ""), "TRY-Kopf"),
        ("Hochwert", metadata.get("hochwert_m", ""), "TRY-Kopf"),
        ("Hoehenlage", metadata.get("hoehenlage_m", ""), "TRY-Kopf"),
        ("Art des TRY", metadata.get("try_type", ""), "TRY-Kopf"),
        ("Bezugszeitraum", metadata.get("reference_period", ""), "TRY-Kopf"),
        ("Mapping-Status", metadata.get("mapping_status", ""), "Mapping"),
        ("Mapping-Standort-ID", metadata.get("mapping_location_id", ""), "Mapping"),
        ("Mapping-Quelle", metadata.get("mapping_source", ""), "Mapping"),
        ("Mapping-Vertrauen", metadata.get("mapping_confidence", ""), "Mapping"),
        ("Mapping-Hinweis", metadata.get("mapping_notes", ""), "Mapping"),
        ("Standortvorschlag", metadata.get("suggested_location_name", ""), "Koordinatenvorschlag"),
        ("Vorschlag Standort-ID", metadata.get("suggested_location_id", ""), "Koordinatenvorschlag"),
        ("Vorschlag Klimaregion", metadata.get("suggested_region_id", ""), "Koordinatenvorschlag"),
        (
            "Vorschlag Referenzstandort-ID",
            metadata.get("suggested_reference_location_id", ""),
            "Koordinatenvorschlag",
        ),
        ("Vorschlag Abstand m", metadata.get("suggested_distance_m", ""), "Koordinatenvorschlag"),
        (
            "Vorschlag Hoehenabweichung m",
            metadata.get("suggested_height_difference_m", ""),
            "Koordinatenvorschlag",
        ),
        ("Vorschlag Vertrauen", metadata.get("suggested_confidence", ""), "Koordinatenvorschlag"),
        ("Vorschlag Begruendung", metadata.get("suggested_reason", ""), "Koordinatenvorschlag"),
    ]
    return [
        {"Feld": field, "Gelesener Wert": value, "Quelle": source}
        for field, value, source in values
        if value not in ("", None)
    ]


def weather_discovery_key_parameter_rows(
    discovery: WeatherFileDiscovery,
    locations_by_id: dict[str, WeatherLocation],
) -> list[dict[str, object]]:
    """Zeigt nur die vom Nutzer fachlich zu pruefenden Parameter."""
    scenario_label = _option_label_for_value(WEATHER_IMPORT_SCENARIO_OPTIONS, discovery.climate_scenario)
    key_parameters = [
        ("Stadt", _location_editor_value(discovery.location_id, locations_by_id)),
        ("Bezugsjahr", discovery.year if discovery.year is not None else ""),
        ("Datensatztyp", discovery.dataset_type),
        ("Szenario", scenario_label or discovery.climate_scenario),
    ]
    return [{"Feld": field, "Wert": value} for field, value in key_parameters]


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


def _render_open_weather_datasets(
    status_by_key: dict[str, WeatherDatasetStatus],
    *,
    discoveries: list[WeatherFileDiscovery] | None = None,
) -> None:
    open_statuses = [status for status in status_by_key.values() if status.is_open]
    open_discoveries = list(discoveries or [])
    rows = weather_status_rows(open_statuses) + weather_open_discovery_rows(open_discoveries)
    st.markdown("**Offene Wetterdatensaetze**")
    st.metric("Offene Wetterdatensaetze", len(rows))
    if not rows:
        st.success("Keine offenen, fehlenden oder blockierten Wetterdatensaetze im aktuellen Status.")
        return
    st.dataframe(
        normalize_table_for_streamlit(rows),
        hide_index=True,
        width="stretch",
    )


def _render_active_weather_datasets(
    datasets: list[WeatherDataset],
    *,
    status_by_key: dict[str, WeatherDatasetStatus],
    selection_state: WeatherSelectionState,
) -> None:
    """Zeigt die regulaer aktiven Wetterdatensaetze."""
    st.markdown("**Aktive Wetterdatensaetze**")
    st.metric("Aktive Wetterdatensaetze", len(datasets))
    rows = weather_dataset_rows(
        datasets,
        status_by_key=status_by_key,
        selection_state=selection_state,
    )
    st.dataframe(
        _weather_dataset_default_table(rows),
        hide_index=True,
        width="stretch",
    )


def _render_weather_dataset_section(
    catalog: object,
    status_by_key: dict[str, WeatherDatasetStatus],
    selection_state: WeatherSelectionState,
    location_catalog: WeatherLocationCatalog | None,
) -> None:
    active_datasets = _regularly_selectable_datasets(catalog.active_datasets(), status_by_key)
    st.subheader("Wetterdatensaetze")
    st.caption(
        "Bei Stadtauswahl werden standortgenaue Datensaetze bevorzugt; "
        "bei Klimaregionsauswahl werden nur Referenzdatensaetze angeboten."
    )
    _render_weather_dataset_actions(catalog, location_catalog)

    active_action = _active_weather_dataset_action()
    if active_action == WEATHER_DATASET_ACTION_IMPORT:
        _render_weather_import_panel()
        return
    if active_action == WEATHER_DATASET_ACTION_SCAN:
        _render_weather_scan_panel(catalog, location_catalog)
        return
    if active_action == WEATHER_DATASET_ACTION_VALIDATE:
        _render_weather_validation_panel(catalog, location_catalog, status_by_key)
        return

    active_column, open_column = st.columns(2)
    with active_column:
        _render_active_weather_datasets(
            active_datasets,
            status_by_key=status_by_key,
            selection_state=selection_state,
        )
    with open_column:
        _render_open_weather_datasets(status_by_key, discoveries=_stored_weather_discoveries())


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
    selection_state = get_weather_selection_state(st.session_state)
    result = st.session_state.get(WEATHER_RESULT_SESSION_KEY)
    status_by_key = _current_status_map(catalog, result)

    st.subheader("Standort und Wetterauswahl")

    if not active_datasets:
        st.info("Im Wetterkatalog ist aktuell kein aktiver Wetterdatensatz vorhanden.")
        _render_weather_dataset_section(catalog, status_by_key, selection_state, location_catalog)
        return

    selected_dataset, start_analysis = _render_weather_selection(catalog, location_catalog, status_by_key, selection_state)
    if selected_dataset is None:
        _render_weather_dataset_section(catalog, status_by_key, selection_state, location_catalog)
        return

    selected_start_year = weather_start_year(selected_dataset)
    selected_weather_plot = normalize_weather_plot_key(st.session_state.get(WEATHER_PLOT_WIDGET_KEY))

    if start_analysis:
        st.session_state.pop(WEATHER_RELEASE_DECISION_SESSION_KEY, None)
        st.session_state.pop(WEATHER_RELEASE_NOTE_WIDGET_KEY, None)
        with st.spinner(f"Wetteranalyse fuer {selected_dataset.weather_key} laeuft..."):
            try:
                result = plot_template_weather(
                    selected_dataset.weather_key,
                    start_year=selected_start_year,
                    session_id=get_weather_session_id(st.session_state),
                    plot_key=selected_weather_plot,
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

    _render_weather_dataset_section(
        catalog,
        status_by_key,
        get_weather_selection_state(st.session_state),
        location_catalog,
    )
