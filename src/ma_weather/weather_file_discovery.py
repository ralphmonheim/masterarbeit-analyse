"""Erkennung lokal abgelegter TRY-Dateien ohne automatische Registrierung."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import yaml

from ma_validation import ReleaseStatus

from .weather_catalog import (
    DATASET_ROLE_SITE_SPECIFIC,
    DATASET_ROLE_TRY_REFERENCE,
    DEFAULT_LOCAL_WEATHER_DATASETS_CONFIG,
    DEFAULT_WEATHER_DATASETS_CONFIG,
    VALID_DATASET_ROLES,
    WeatherCatalog,
    WeatherDataset,
    import_weather_catalog,
)
from .weather_imports import _append_local_dataset_record, suggest_weather_key
from .weather_location_resolution import WeatherLocationResolutionStatus, resolve_weather_file_location
from .weather_locations import (
    WeatherLocation,
    WeatherLocationCatalog,
    import_weather_location_catalog,
)
from .weather_status import WeatherDatasetStatus, inspect_weather_dataset_status

DEFAULT_TRY_FILE_LOCATION_CONFIG = Path("config/ma_weather/try_locations/example_try_file_locations.yaml")
DEFAULT_WEATHER_INPUT_DIR = Path("data/ma_weather/input")

TRY_FILE_PATTERN = re.compile(
    r"^TRY(?P<year>20\d{2})_(?P<try_id>\d+)_(?P<kind>Jahr|Somm|Wint)\.dat$",
    re.IGNORECASE,
)
TRY_FOLDER_PATTERN = re.compile(r"^TRY_(?P<try_id>\d+)(?:_[A-Za-z0-9_-]+)?$", re.IGNORECASE)
CUSTOM_INPUT_PART = "custom"

DATASET_TYPE_BY_KIND = {
    "jahr": "Jahr",
    "somm": "Sommer",
    "wint": "Winter",
}
YEAR_TYPE_BY_KIND = {
    "somm": "summer_extreme",
    "wint": "winter_extreme",
}
WEATHER_KEY_SUFFIX_BY_KIND = {
    "jahr": "JAHR",
    "somm": "SOMM",
    "wint": "WINT",
}
WEATHER_KEY_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
HEADER_FIELDS = {
    "Standort": "file_location_name",
    "Ort": "file_location_name",
    "Stadt": "file_location_name",
    "Gemeinde": "file_location_name",
    "Rechtswert": "rechtswert_m",
    "Hochwert": "hochwert_m",
    "Hoehenlage": "hoehenlage_m",
    "Art des TRY": "try_type",
    "Bezugszeitraum": "reference_period",
}
LOCATION_RESOLUTION_SOURCE_FILE_REFERENCE = "file_reference"
LOCATION_RESOLUTION_SOURCE_TRY_COORDINATES = "try_coordinates"
LOCATION_RESOLUTION_SOURCE_MANUAL = "manual"
LOCATION_RESOLUTION_STATUS_CONFIRMED = "confirmed"
LOCATION_RESOLUTION_STATUS_SUGGESTED = "suggested"
LOCATION_RESOLUTION_STATUS_MISSING = "missing"
LOCATION_RESOLUTION_STATUS_CONFLICT = "conflict"
LOCATION_RESOLUTION_STATUS_BLOCKED = "blocked"
MAPPING_STATUS_CONFIRMED = "confirmed"
MAPPING_STATUS_CANDIDATE = "candidate"
MAPPING_STATUS_OPEN = "open"
MAPPING_STATUSES = {
    MAPPING_STATUS_CONFIRMED,
    MAPPING_STATUS_CANDIDATE,
    MAPPING_STATUS_OPEN,
}


class WeatherDiscoveryStatus(StrEnum):
    """Status eines gefundenen, noch nicht katalogisierten TRY-Dateientwurfs."""

    READY = "vollstaendig"
    OPEN = "offen"


@dataclass(frozen=True, slots=True)
class WeatherTryLocationMapping:
    """Versionierte Zuordnung eines TRY-Ordners zu einem Wetterstandort."""

    try_folder_key: str
    location_id: str
    mapping_status: str = MAPPING_STATUS_CONFIRMED
    mapping_source: str = ""
    confidence: str = ""
    notes: str = ""

    @property
    def is_confirmed(self) -> bool:
        """Nur bestaetigte Zuordnungen duerfen automatisch vorbelegen."""
        return self.mapping_status == MAPPING_STATUS_CONFIRMED


@dataclass(frozen=True, slots=True)
class WeatherLocationMappingSuggestion:
    """Vorsichtiger Standortvorschlag aus TRY-Koordinaten."""

    location_id: str
    location_name: str
    region_id: str
    reference_location_id: str
    distance_m: float
    height_difference_m: float | None
    confidence: str
    reason: str
    source: str


@dataclass(frozen=True, slots=True)
class _WeatherLocationCoordinateReference:
    location_id: str
    location_name: str
    region_id: str
    reference_location_id: str
    rechtswert_m: float
    hochwert_m: float
    hoehenlage_m: float | None
    source: str


@dataclass(frozen=True, slots=True)
class WeatherFileDiscovery:
    """Datensatzentwurf aus einer lokal gefundenen TRY-Datei."""

    weather_key: str
    display_name: str
    file_path: Path
    try_folder_key: str
    try_id: str
    year: int | None
    dataset_type: str
    year_type: str
    climate_scenario: str
    dataset_role: str
    location_id: str
    reference_location_id: str
    location_name: str
    selection_priority: int
    metadata: dict[str, str]
    missing_fields: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()
    status: WeatherDiscoveryStatus = WeatherDiscoveryStatus.READY

    @property
    def is_complete(self) -> bool:
        """Gibt an, ob der Entwurf ohne Nacharbeit registriert werden kann."""
        return self.status is WeatherDiscoveryStatus.READY and not self.missing_fields


@dataclass(frozen=True, slots=True)
class WeatherStagedInputFile:
    """Rein lokal abgelegte TRY-Datei ohne Katalogregistrierung."""

    file_path: Path
    try_folder_key: str
    try_id: str
    original_filename: str


@dataclass(frozen=True, slots=True)
class WeatherDiscoveryValidationResult:
    """Validierung eines Datensatzentwurfs vor der Katalogregistrierung."""

    discovery: WeatherFileDiscovery
    dataset_status: WeatherDatasetStatus
    can_register: bool
    warnings_released: bool = False
    messages: tuple[str, ...] = ()


def stage_weather_input_file(
    file_content: bytes,
    *,
    original_filename: str,
    input_dir: str | Path = DEFAULT_WEATHER_INPUT_DIR,
    project_root: str | Path | None = None,
) -> WeatherStagedInputFile:
    """Legt eine hochgeladene TRY-Datei lokal ab, ohne sie zu katalogisieren."""
    root = Path.cwd() if project_root is None else Path(project_root)
    filename = Path(original_filename.strip()).name
    if not file_content:
        raise ValueError("Die TRY-Datei ist leer.")
    if Path(filename).suffix.lower() != ".dat":
        raise ValueError("Es koennen nur entpackte TRY-.dat-Dateien abgelegt werden.")

    filename_match = TRY_FILE_PATTERN.fullmatch(filename)
    if filename_match is None:
        raise ValueError("Dateiname entspricht nicht dem erwarteten TRY-Muster, z. B. TRY2015_494997084777_Jahr.dat.")

    try_id = filename_match.group("try_id")
    try_folder_key = f"TRY_{try_id}"
    target_dir = (root / Path(input_dir) / try_folder_key).resolve()
    target_file = (target_dir / filename).resolve()
    if target_file.parent != target_dir:
        raise ValueError("Zieldatei liegt ausserhalb des Wetterdatenordners.")
    if target_file.exists():
        raise FileExistsError(f"TRY-Datei existiert bereits: {_relative_to_project(target_file, root)}")

    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_bytes(file_content)
    return WeatherStagedInputFile(
        file_path=_relative_to_project(target_file, root),
        try_folder_key=try_folder_key,
        try_id=try_id,
        original_filename=filename,
    )


def discover_weather_input_files(
    input_dir: str | Path = DEFAULT_WEATHER_INPUT_DIR,
    *,
    existing_catalog: WeatherCatalog | None = None,
    location_catalog: WeatherLocationCatalog | None = None,
    mapping_path: str | Path = DEFAULT_TRY_FILE_LOCATION_CONFIG,
    project_root: str | Path | None = None,
) -> list[WeatherFileDiscovery]:
    """Findet noch nicht katalogisierte TRY-Dateien im lokalen Eingabeordner."""
    root = Path.cwd() if project_root is None else Path(project_root)
    scan_root = root / Path(input_dir)
    if not scan_root.exists():
        return []

    catalog = existing_catalog or import_weather_catalog(DEFAULT_WEATHER_DATASETS_CONFIG)
    locations = location_catalog or import_weather_location_catalog()
    mapping = _load_try_location_mapping(root / Path(mapping_path))
    coordinate_references = _coordinate_references_from_input_files(scan_root, root, locations, mapping)
    existing_paths = {_normalize_relative_path(dataset.file_path) for dataset in catalog.datasets}

    discoveries: list[WeatherFileDiscovery] = []
    for file_path in sorted(scan_root.rglob("TRY*.dat")):
        relative_path = _relative_to_project(file_path, root)
        if CUSTOM_INPUT_PART in relative_path.parts:
            continue
        if _normalize_relative_path(relative_path) in existing_paths:
            continue
        discoveries.append(
            _build_file_discovery(
                file_path=file_path,
                relative_path=relative_path,
                existing_catalog=catalog,
                location_catalog=locations,
                try_location_mapping=mapping,
                coordinate_references=coordinate_references,
                project_root=root,
            )
        )
    return discoveries


def weather_discovery_rows(discoveries: list[WeatherFileDiscovery]) -> list[dict[str, object]]:
    """Bereitet gefundene TRY-Dateien fuer die UI-Tabelle auf."""
    rows: list[dict[str, object]] = []
    for discovery in discoveries:
        rows.append(
            {
                "Status": discovery.status.value,
                "weather_key": discovery.weather_key,
                "Name": discovery.display_name,
                "TRY-Ordner": discovery.try_folder_key,
                "TRY-ID": discovery.try_id,
                "Ort": discovery.location_name,
                "Standort-ID": discovery.location_id,
                "Referenzstandort-ID": discovery.reference_location_id,
                "Rolle": _dataset_role_label(discovery.dataset_role),
                "Jahr": discovery.year if discovery.year is not None else "",
                "Datensatztyp": discovery.dataset_type,
                "Jahrtyp": discovery.year_type,
                "Szenario": discovery.climate_scenario,
                "Prioritaet": discovery.selection_priority,
                "Datei": discovery.file_path.as_posix(),
                "Rechtswert": discovery.metadata.get("rechtswert_m", ""),
                "Hochwert": discovery.metadata.get("hochwert_m", ""),
                "Hoehenlage": discovery.metadata.get("hoehenlage_m", ""),
                "Art des TRY": discovery.metadata.get("try_type", ""),
                "Bezugszeitraum": discovery.metadata.get("reference_period", ""),
                "Offene Punkte": ", ".join(discovery.missing_fields),
                "Hinweise": "; ".join(discovery.messages),
            }
        )
    return rows


def update_weather_file_discovery(
    discovery: WeatherFileDiscovery,
    *,
    location_catalog: WeatherLocationCatalog,
    location_id: str,
    dataset_type: str,
    climate_scenario: str,
    dataset_role: str,
    year: int | None,
    weather_key: str,
    display_name: str,
) -> WeatherFileDiscovery:
    """Uebernimmt bewusst angepasste Entwurfswerte aus der UI."""
    location = _location_or_none(location_catalog, location_id) if location_id else None
    metadata = dict(discovery.metadata)
    kind = _kind_for_dataset_type(dataset_type)
    year_value = int(year) if year is not None else None
    year_type = _year_type_for_dataset_type(dataset_type, climate_scenario)
    dataset_role_value = dataset_role
    if location is not None and dataset_role_value not in VALID_DATASET_ROLES:
        dataset_role_value = DATASET_ROLE_TRY_REFERENCE if location.is_reference_location else DATASET_ROLE_SITE_SPECIFIC
    reference_location_id = ""
    if location is not None:
        reference_location_id = (
            location.location_id
            if dataset_role_value == DATASET_ROLE_TRY_REFERENCE
            else location.reference_location_id
        )
    weather_key_value = weather_key.strip()
    display_name_value = display_name.strip()
    if location is not None and year_value is not None and kind:
        if not weather_key_value:
            weather_key_value = _weather_key_for_discovery(location, year_value, kind)
        if not display_name_value:
            display_name_value = _display_name_for_discovery(location, year_value, dataset_type)
    missing_fields = _missing_adjusted_fields(
        weather_key=weather_key_value,
        display_name=display_name_value,
        location_id=location.location_id if location is not None else "",
        dataset_type=dataset_type,
        climate_scenario=climate_scenario,
        dataset_role=dataset_role_value,
        year=year_value,
        year_type=year_type,
    )
    messages = list(discovery.messages)
    if location_id and location is None:
        messages.append(f"Standort-ID ist nicht im Standortkatalog vorhanden: {location_id}")
    if location is not None and dataset_role_value == DATASET_ROLE_TRY_REFERENCE and not location.is_reference_location:
        messages.append("TRY-Referenzdatensatz ist auf einen nicht als Referenzstandort markierten Standort gesetzt.")
    if location is not None:
        metadata.update(
            _location_resolution_metadata(
                source=LOCATION_RESOLUTION_SOURCE_MANUAL,
                status=LOCATION_RESOLUTION_STATUS_CONFIRMED,
                detail="Standort wurde in der Pruefansicht bewusst gesetzt.",
            )
        )
    status = WeatherDiscoveryStatus.OPEN if missing_fields else WeatherDiscoveryStatus.READY
    return WeatherFileDiscovery(
        weather_key=weather_key_value,
        display_name=display_name_value,
        file_path=discovery.file_path,
        try_folder_key=discovery.try_folder_key,
        try_id=discovery.try_id,
        year=year_value,
        dataset_type=dataset_type,
        year_type=year_type,
        climate_scenario=climate_scenario,
        dataset_role=dataset_role_value,
        location_id=location.location_id if location is not None else "",
        reference_location_id=reference_location_id,
        location_name=location.location_name if location is not None else "",
        selection_priority=_selection_priority(kind, year_value),
        metadata=metadata,
        missing_fields=tuple(missing_fields),
        messages=tuple(dict.fromkeys(messages)),
        status=status,
    )


def validate_weather_file_discovery(
    discovery: WeatherFileDiscovery,
    *,
    existing_catalog: WeatherCatalog | None = None,
    project_root: str | Path | None = None,
    warnings_released: bool = False,
) -> WeatherDiscoveryValidationResult:
    """Prueft einen Entwurf technisch, bevor er registriert werden darf."""
    root = Path.cwd() if project_root is None else Path(project_root)
    catalog = existing_catalog or import_weather_catalog()
    messages = list(discovery.messages)
    duplicate_key = any(dataset.weather_key == discovery.weather_key for dataset in catalog.datasets)
    if duplicate_key:
        messages.append(f"weather_key ist bereits vorhanden: {discovery.weather_key}")
    location_resolution_blocking = _location_resolution_blocks_registration(discovery)
    if location_resolution_blocking:
        status_text = discovery.metadata.get("location_resolution_status", "unbekannt")
        messages.append(f"Standortaufloesung blockiert die Registrierung: {status_text}")

    dataset = _dataset_from_discovery(discovery)
    status = inspect_weather_dataset_status(dataset, project_root=root, validate_file=True)
    can_register = (
        discovery.is_complete
        and not duplicate_key
        and not location_resolution_blocking
        and (
            status.release_status is ReleaseStatus.RELEASED
            or (status.release_status is ReleaseStatus.CONFIRMATION_REQUIRED and warnings_released)
        )
        and status.error_count == 0
    )
    return WeatherDiscoveryValidationResult(
        discovery=discovery,
        dataset_status=status,
        can_register=can_register,
        warnings_released=warnings_released,
        messages=tuple(dict.fromkeys(messages + list(status.messages))),
    )


def register_discovered_weather_dataset(
    discovery: WeatherFileDiscovery,
    *,
    existing_catalog: WeatherCatalog | None = None,
    local_catalog_path: str | Path = DEFAULT_LOCAL_WEATHER_DATASETS_CONFIG,
    project_root: str | Path | None = None,
    is_active: bool = True,
) -> WeatherDataset:
    """Uebernimmt einen vollstaendigen Entwurf in den lokalen Wetterkatalog."""
    if not discovery.is_complete:
        missing = ", ".join(discovery.missing_fields) or "offene Entwurfsdaten"
        raise ValueError(f"Entwurf ist unvollstaendig: {missing}")
    if discovery.year is None:
        raise ValueError("Entwurf enthaelt kein Bezugsjahr.")

    catalog = existing_catalog or import_weather_catalog()
    if any(dataset.weather_key == discovery.weather_key for dataset in catalog.datasets):
        raise ValueError(f"weather_key ist bereits vorhanden: {discovery.weather_key}")

    root = Path.cwd() if project_root is None else Path(project_root)
    dataset = WeatherDataset(
        weather_key=discovery.weather_key,
        display_name=discovery.display_name,
        file_path=discovery.file_path,
        file_format="TRY",
        source="DWD TRY",
        location=discovery.location_name,
        year_type=discovery.year_type,
        climate_scenario=discovery.climate_scenario,
        dataset_role=discovery.dataset_role,
        location_id=discovery.location_id,
        reference_location_id=discovery.reference_location_id,
        selection_priority=discovery.selection_priority,
        is_active=is_active,
        notes="Aus lokalem TRY-Dateiscan registriert; Datei bleibt unversioniert.",
        **_dataset_location_resolution_kwargs(discovery.metadata),
    )
    _append_local_dataset_record(root / Path(local_catalog_path), dataset)
    return dataset


def _dataset_from_discovery(discovery: WeatherFileDiscovery) -> WeatherDataset:
    return WeatherDataset(
        weather_key=discovery.weather_key,
        display_name=discovery.display_name,
        file_path=discovery.file_path,
        file_format="TRY",
        source="DWD TRY",
        location=discovery.location_name,
        year_type=discovery.year_type,
        climate_scenario=discovery.climate_scenario,
        dataset_role=discovery.dataset_role,
        location_id=discovery.location_id,
        reference_location_id=discovery.reference_location_id,
        selection_priority=discovery.selection_priority,
        is_active=False,
        notes="Entwurf aus lokalem TRY-Dateiscan.",
        **_dataset_location_resolution_kwargs(discovery.metadata),
    )


def _dataset_location_resolution_kwargs(metadata: dict[str, str]) -> dict[str, object]:
    method = metadata.get("municipality_match_method") or metadata.get("location_resolution_method", "")
    return {
        "source_easting": _metadata_number(metadata.get("source_easting", metadata.get("rechtswert_m", ""))),
        "source_northing": _metadata_number(metadata.get("source_northing", metadata.get("hochwert_m", ""))),
        "source_crs_epsg": _metadata_int(metadata.get("source_crs_epsg", "")),
        "resolved_latitude": _metadata_number(metadata.get("resolved_latitude", "")),
        "resolved_longitude": _metadata_number(metadata.get("resolved_longitude", "")),
        "elevation_m": _metadata_number(metadata.get("elevation_m", metadata.get("hoehenlage_m", ""))),
        "detected_municipality_name": metadata.get("detected_municipality_name", ""),
        "detected_municipality_code": metadata.get("detected_municipality_code", ""),
        "detected_federal_state": metadata.get("detected_federal_state", ""),
        "detected_postal_code": metadata.get("detected_postal_code", ""),
        "location_resolution_source": metadata.get("location_resolution_source", ""),
        "location_resolution_status": metadata.get("location_resolution_status", ""),
        "location_resolution_method": method,
        "geodata_source_id": metadata.get("geodata_source_id", ""),
    }


def _build_file_discovery(
    *,
    file_path: Path,
    relative_path: Path,
    existing_catalog: WeatherCatalog,
    location_catalog: WeatherLocationCatalog,
    try_location_mapping: dict[str, WeatherTryLocationMapping],
    coordinate_references: list[_WeatherLocationCoordinateReference],
    project_root: Path,
) -> WeatherFileDiscovery:
    filename_match = TRY_FILE_PATTERN.fullmatch(file_path.name)
    folder_key, folder_try_id = _try_folder_key(relative_path.parent.name)
    try_id = folder_try_id
    year: int | None = None
    kind = ""
    missing_fields: list[str] = []
    messages: list[str] = []

    if filename_match is None:
        missing_fields.extend(["year", "dataset_type"])
        messages.append("Dateiname entspricht nicht dem erwarteten TRY-Muster.")
    else:
        year = int(filename_match.group("year"))
        kind = filename_match.group("kind").casefold()
        try_id = filename_match.group("try_id")
        if folder_try_id and folder_try_id != try_id:
            missing_fields.append("try_id")
            messages.append("TRY-ID im Ordner und Dateinamen stimmt nicht ueberein.")

    if not folder_key:
        missing_fields.append("try_folder_key")
        messages.append("TRY-Ordnerkennung konnte nicht abgeleitet werden.")
        folder_key = f"TRY_{try_id}" if try_id else ""

    metadata = _read_try_header_metadata(file_path)
    location_resolution = resolve_weather_file_location(metadata, project_root=project_root)
    location_resolution_is_blocking = False
    if location_resolution.status is not WeatherLocationResolutionStatus.NOT_CONFIGURED:
        metadata.update(_geodata_location_resolution_metadata(location_resolution.to_metadata()))
        messages.extend(location_resolution.messages)
        location_resolution_is_blocking = location_resolution.is_blocking
    mapping_entry = try_location_mapping.get(folder_key)
    metadata.update(_mapping_metadata(mapping_entry))
    file_location = _location_from_file_reference(metadata, location_catalog)
    mapping_location_id = mapping_entry.location_id if mapping_entry is not None and mapping_entry.is_confirmed else ""
    geodata_location = _location_from_geodata_resolution(metadata, location_catalog)
    if location_resolution_is_blocking and file_location is None and not mapping_location_id:
        missing_fields.append("location_resolution")
    location_id = file_location.location_id if file_location is not None else mapping_location_id
    if not location_id and geodata_location is not None:
        location_id = geodata_location.location_id
    location = _location_or_none(location_catalog, location_id) if location_id else None
    if file_location is not None and mapping_location_id and file_location.location_id != mapping_location_id:
        location_id = ""
        location = None
        missing_fields.extend(["location_id", "location_resolution"])
        messages.append(
            "Standortkonflikt zwischen Dateiverweis "
            f"{file_location.location_id} und bestaetigter TRY-Ordner-Zuordnung {mapping_location_id}."
        )
        metadata.update(
            _location_resolution_metadata(
                source=LOCATION_RESOLUTION_SOURCE_FILE_REFERENCE,
                status=LOCATION_RESOLUTION_STATUS_CONFLICT,
                detail="Dateiverweis und bestaetigte TRY-Ordner-Zuordnung widersprechen sich.",
            )
        )
    elif location is not None:
        if file_location is not None:
            detail = "Standort wurde aus einem Dateiverweis gelesen."
            source = LOCATION_RESOLUTION_SOURCE_FILE_REFERENCE
        elif mapping_location_id:
            detail = "Standort wurde aus bestaetigter TRY-Ordner-Zuordnung gelesen."
            source = LOCATION_RESOLUTION_SOURCE_FILE_REFERENCE
        else:
            detail = "Standort wurde per lokaler Gemeinde-Geodatenquelle aus TRY-Koordinaten erkannt."
            source = LOCATION_RESOLUTION_SOURCE_TRY_COORDINATES
        metadata.update(
            _location_resolution_metadata(
                source=source,
                status=LOCATION_RESOLUTION_STATUS_CONFIRMED,
                detail=detail,
            )
        )
        if metadata.get("geodata_location_resolution_blocking") == "true":
            metadata["geodata_location_resolution_blocking"] = "false"
            metadata["geodata_location_resolution_override"] = source
    elif mapping_entry is not None and not mapping_entry.is_confirmed:
        missing_fields.append("location_id")
        messages.append(f"Standortzuordnung fuer {folder_key or relative_path.parent.name} ist noch nicht bestaetigt.")
        metadata.update(
            _location_resolution_metadata(
                source=LOCATION_RESOLUTION_SOURCE_FILE_REFERENCE,
                status=LOCATION_RESOLUTION_STATUS_SUGGESTED,
                detail="TRY-Ordner-Zuordnung ist vorhanden, aber noch nicht bestaetigt.",
            )
        )
    elif not location_id:
        missing_fields.append("location_id")
        detected_municipality_name = metadata.get("detected_municipality_name", "").strip()
        if detected_municipality_name:
            messages.append(
                "Gemeinde aus lokalen Geodaten erkannt, aber nicht im Standortkatalog vorhanden: "
                f"{detected_municipality_name}."
            )
        else:
            messages.append(f"Keine Standortzuordnung fuer {folder_key or relative_path.parent.name} gefunden.")
        metadata.update(
            _location_resolution_metadata(
                source="",
                status=LOCATION_RESOLUTION_STATUS_MISSING,
                detail="Keine eindeutige Standortquelle gefunden.",
            )
        )
    elif location is None:
        missing_fields.append("location_id")
        messages.append(f"Standort-ID aus Zuordnungstabelle ist nicht im Standortkatalog vorhanden: {location_id}")
        metadata.update(
            _location_resolution_metadata(
                source=LOCATION_RESOLUTION_SOURCE_FILE_REFERENCE,
                status=LOCATION_RESOLUTION_STATUS_BLOCKED,
                detail="Standort-ID aus expliziter Zuordnung ist nicht im Standortkatalog vorhanden.",
            )
        )

    dataset_type = DATASET_TYPE_BY_KIND.get(kind, "")
    year_type = _year_type_for_kind(kind, year)
    climate_scenario = _climate_scenario_for_year(year)
    selection_priority = _selection_priority(kind, year)
    weather_key = _weather_key_for_discovery(location, year, kind)
    display_name = _display_name_for_discovery(location, year, dataset_type)
    dataset_role = ""
    reference_location_id = ""
    location_name = ""

    if location is not None:
        location_name = location.location_name
        reference_location_id = location.reference_location_id
        dataset_role = DATASET_ROLE_TRY_REFERENCE if location.is_reference_location else DATASET_ROLE_SITE_SPECIFIC
    elif metadata.get("location_resolution_status") not in {
        LOCATION_RESOLUTION_STATUS_CONFLICT,
        LOCATION_RESOLUTION_STATUS_BLOCKED,
    }:
        suggestion = _suggest_location_from_metadata(
            metadata,
            location_catalog=location_catalog,
            coordinate_references=coordinate_references,
        )
        if suggestion is not None:
            metadata.update(_suggestion_metadata(suggestion))
            metadata.update(
                _location_resolution_metadata(
                    source=LOCATION_RESOLUTION_SOURCE_TRY_COORDINATES,
                    status=LOCATION_RESOLUTION_STATUS_SUGGESTED,
                    detail="Standortvorschlag wurde aus TRY-Koordinaten abgeleitet.",
                )
            )
            messages.append(
                "Standortvorschlag aus TRY-Koordinaten: "
                f"{suggestion.location_name} ({suggestion.distance_m:.0f} m Abstand). "
                "Bitte bewusst uebernehmen."
            )
    if not weather_key:
        missing_fields.append("weather_key")
    elif any(dataset.weather_key == weather_key for dataset in existing_catalog.datasets):
        missing_fields.append("weather_key")
        messages.append(f"weather_key ist bereits katalogisiert: {weather_key}")
    if not year_type:
        missing_fields.append("year_type")
    if not climate_scenario:
        missing_fields.append("climate_scenario")

    deduplicated_missing = tuple(dict.fromkeys(missing_fields))
    status = WeatherDiscoveryStatus.OPEN if deduplicated_missing else WeatherDiscoveryStatus.READY
    return WeatherFileDiscovery(
        weather_key=weather_key,
        display_name=display_name,
        file_path=relative_path,
        try_folder_key=folder_key,
        try_id=try_id,
        year=year,
        dataset_type=dataset_type,
        year_type=year_type,
        climate_scenario=climate_scenario,
        dataset_role=dataset_role,
        location_id=location_id if location is not None else "",
        reference_location_id=reference_location_id,
        location_name=location_name,
        selection_priority=selection_priority,
        metadata=metadata,
        missing_fields=deduplicated_missing,
        messages=tuple(messages),
        status=status,
    )


def _load_try_location_mapping(path: Path) -> dict[str, WeatherTryLocationMapping]:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ValueError(f"TRY-Standortzuordnung muss ein YAML-Objekt sein: {path}")
    raw_locations = payload.get("try_file_locations", [])
    if not isinstance(raw_locations, list):
        raise ValueError(f"try_file_locations muss eine Liste sein: {path}")

    mapping: dict[str, WeatherTryLocationMapping] = {}
    for index, raw_location in enumerate(raw_locations, start=1):
        if not isinstance(raw_location, dict):
            raise ValueError(f"try_file_locations[{index}] muss ein Objekt sein.")
        try_folder_key = str(raw_location.get("try_folder_key", "")).strip()
        location_id = str(raw_location.get("location_id", "")).strip()
        mapping_status = str(raw_location.get("mapping_status", MAPPING_STATUS_CONFIRMED)).strip() or MAPPING_STATUS_CONFIRMED
        if not try_folder_key or not location_id:
            raise ValueError(f"try_file_locations[{index}] braucht try_folder_key und location_id.")
        if mapping_status not in MAPPING_STATUSES:
            raise ValueError(
                f"try_file_locations[{index}].mapping_status ist ungueltig: {mapping_status}."
            )
        if try_folder_key in mapping:
            raise ValueError(f"TRY-Ordnerkennung ist doppelt: {try_folder_key}")
        mapping[try_folder_key] = WeatherTryLocationMapping(
            try_folder_key=try_folder_key,
            location_id=location_id,
            mapping_status=mapping_status,
            mapping_source=str(raw_location.get("mapping_source", "")).strip(),
            confidence=str(raw_location.get("confidence", "")).strip(),
            notes=str(raw_location.get("notes", "")).strip(),
        )
    return mapping


def suggest_weather_location_mapping(
    discovery: WeatherFileDiscovery,
    *,
    location_catalog: WeatherLocationCatalog,
    reference_discoveries: list[WeatherFileDiscovery],
) -> WeatherLocationMappingSuggestion | None:
    """Erzeugt einen vorsichtigen Standortvorschlag aus TRY-Koordinaten."""
    coordinate_references = [
        _coordinate_reference_from_discovery(reference, location_catalog=location_catalog)
        for reference in reference_discoveries
        if reference.location_id
    ]
    return _suggest_location_from_metadata(
        discovery.metadata,
        location_catalog=location_catalog,
        coordinate_references=[
            reference for reference in coordinate_references if reference is not None
        ],
    )


def _coordinate_references_from_input_files(
    scan_root: Path,
    root: Path,
    location_catalog: WeatherLocationCatalog,
    mapping: dict[str, WeatherTryLocationMapping],
) -> list[_WeatherLocationCoordinateReference]:
    references: list[_WeatherLocationCoordinateReference] = []
    seen: set[tuple[str, float, float]] = set()
    for file_path in sorted(scan_root.rglob("TRY*.dat")):
        relative_path = _relative_to_project(file_path, root)
        if CUSTOM_INPUT_PART in relative_path.parts:
            continue
        folder_key, _ = _try_folder_key(relative_path.parent.name)
        mapping_entry = mapping.get(folder_key)
        if mapping_entry is None or not mapping_entry.is_confirmed:
            continue
        location = _location_or_none(location_catalog, mapping_entry.location_id)
        if location is None:
            continue
        metadata = _read_try_header_metadata(file_path)
        reference = _coordinate_reference_from_metadata(
            metadata,
            location=location,
            source=relative_path.as_posix(),
        )
        if reference is None:
            continue
        identity = (reference.location_id, reference.rechtswert_m, reference.hochwert_m)
        if identity in seen:
            continue
        seen.add(identity)
        references.append(reference)
    return references


def _coordinate_reference_from_discovery(
    discovery: WeatherFileDiscovery,
    *,
    location_catalog: WeatherLocationCatalog,
) -> _WeatherLocationCoordinateReference | None:
    location = _location_or_none(location_catalog, discovery.location_id)
    if location is None:
        return None
    return _coordinate_reference_from_metadata(
        discovery.metadata,
        location=location,
        source=discovery.file_path.as_posix(),
    )


def _coordinate_reference_from_metadata(
    metadata: dict[str, str],
    *,
    location: WeatherLocation,
    source: str,
) -> _WeatherLocationCoordinateReference | None:
    rechtswert = _metadata_number(metadata.get("rechtswert_m", ""))
    hochwert = _metadata_number(metadata.get("hochwert_m", ""))
    if rechtswert is None or hochwert is None:
        return None
    return _WeatherLocationCoordinateReference(
        location_id=location.location_id,
        location_name=location.location_name,
        region_id=location.region_id,
        reference_location_id=location.reference_location_id,
        rechtswert_m=rechtswert,
        hochwert_m=hochwert,
        hoehenlage_m=_metadata_number(metadata.get("hoehenlage_m", "")),
        source=source,
    )


def _suggest_location_from_metadata(
    metadata: dict[str, str],
    *,
    location_catalog: WeatherLocationCatalog,
    coordinate_references: list[_WeatherLocationCoordinateReference],
) -> WeatherLocationMappingSuggestion | None:
    rechtswert = _metadata_number(metadata.get("rechtswert_m", ""))
    hochwert = _metadata_number(metadata.get("hochwert_m", ""))
    if rechtswert is None or hochwert is None or not coordinate_references:
        return None

    target_height = _metadata_number(metadata.get("hoehenlage_m", ""))
    nearest = min(
        coordinate_references,
        key=lambda reference: math.hypot(reference.rechtswert_m - rechtswert, reference.hochwert_m - hochwert),
    )
    distance = math.hypot(nearest.rechtswert_m - rechtswert, nearest.hochwert_m - hochwert)
    height_difference = None
    if target_height is not None and nearest.hoehenlage_m is not None:
        height_difference = abs(nearest.hoehenlage_m - target_height)
    reference_location = location_catalog.reference_location_for_city(nearest.location_id)
    confidence = _mapping_confidence(distance)
    return WeatherLocationMappingSuggestion(
        location_id=nearest.location_id,
        location_name=nearest.location_name,
        region_id=nearest.region_id,
        reference_location_id=reference_location.location_id,
        distance_m=distance,
        height_difference_m=height_difference,
        confidence=confidence,
        reason=(
            "Naechster bestaetigter TRY-Standort anhand Rechtswert/Hochwert"
            if height_difference is None
            else "Naechster bestaetigter TRY-Standort anhand Rechtswert/Hochwert; Hoehenlage als Zusatzhinweis"
        ),
        source=nearest.source,
    )


def _mapping_metadata(mapping_entry: WeatherTryLocationMapping | None) -> dict[str, str]:
    if mapping_entry is None:
        return {}
    return {
        "mapping_location_id": mapping_entry.location_id,
        "mapping_status": mapping_entry.mapping_status,
        "mapping_source": mapping_entry.mapping_source,
        "mapping_confidence": mapping_entry.confidence,
        "mapping_notes": mapping_entry.notes,
    }


def _location_resolution_metadata(*, source: str, status: str, detail: str) -> dict[str, str]:
    return {
        "location_resolution_source": source,
        "location_resolution_status": status,
        "location_resolution_detail": detail,
    }


def _geodata_location_resolution_metadata(metadata: dict[str, str]) -> dict[str, str]:
    """Bewahrt technische Geodatenstatus getrennt vom fachlichen Standortstatus auf."""
    converted = dict(metadata)
    if "location_resolution_status" in converted:
        converted["geodata_location_resolution_status"] = converted.pop("location_resolution_status")
    if "location_resolution_blocking" in converted:
        converted["geodata_location_resolution_blocking"] = converted.pop("location_resolution_blocking")
    if "location_resolution_messages" in converted:
        converted["geodata_location_resolution_messages"] = converted.pop("location_resolution_messages")
    return converted


def _location_from_file_reference(
    metadata: dict[str, str],
    location_catalog: WeatherLocationCatalog,
) -> WeatherLocation | None:
    location_name = metadata.get("file_location_name", "").strip()
    if not location_name:
        return None
    try:
        return location_catalog.get_location_by_name(location_name)
    except KeyError:
        return None


def _location_from_geodata_resolution(
    metadata: dict[str, str],
    location_catalog: WeatherLocationCatalog,
) -> WeatherLocation | None:
    """Uebernimmt nur eindeutige Gemeinde-Geodaten, keine unsicheren Naechstvorschlaege."""
    if metadata.get("geodata_location_resolution_blocking") == "true":
        return None
    if metadata.get("geodata_location_resolution_status") not in {
        WeatherLocationResolutionStatus.MATCHED.value,
        WeatherLocationResolutionStatus.MATCHED_WITH_WARNING.value,
    }:
        return None
    municipality_name = metadata.get("detected_municipality_name", "").strip()
    if not municipality_name:
        return None
    try:
        return location_catalog.get_location_by_name(municipality_name)
    except KeyError:
        return None


def _location_resolution_blocks_registration(discovery: WeatherFileDiscovery) -> bool:
    geodata_blocks = discovery.metadata.get("geodata_location_resolution_blocking") == "true"
    status = discovery.metadata.get("location_resolution_status", "")
    if status in {
        LOCATION_RESOLUTION_STATUS_CONFLICT,
        LOCATION_RESOLUTION_STATUS_BLOCKED,
        LOCATION_RESOLUTION_STATUS_SUGGESTED,
    }:
        return True
    return geodata_blocks or (bool(status) and status != LOCATION_RESOLUTION_STATUS_CONFIRMED)


def _suggestion_metadata(suggestion: WeatherLocationMappingSuggestion) -> dict[str, str]:
    metadata = {
        "suggested_location_id": suggestion.location_id,
        "suggested_location_name": suggestion.location_name,
        "suggested_region_id": suggestion.region_id,
        "suggested_reference_location_id": suggestion.reference_location_id,
        "suggested_distance_m": f"{suggestion.distance_m:.0f}",
        "suggested_confidence": suggestion.confidence,
        "suggested_reason": suggestion.reason,
        "suggested_source": suggestion.source,
    }
    if suggestion.height_difference_m is not None:
        metadata["suggested_height_difference_m"] = f"{suggestion.height_difference_m:.0f}"
    return metadata


def _metadata_number(value: str) -> float | None:
    match = re.search(r"-?\d+(?:[,.]\d+)?", str(value))
    if match is None:
        return None
    return float(match.group(0).replace(",", "."))


def _metadata_int(value: str) -> int | None:
    number = _metadata_number(value)
    if number is None:
        return None
    return int(number)


def _mapping_confidence(distance_m: float) -> str:
    if distance_m <= 1000:
        return "hoch"
    if distance_m <= 10000:
        return "mittel"
    return "niedrig"


def _read_try_header_metadata(path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    try:
        with path.open("r", encoding="latin-1") as file:
            for raw_line in file:
                line = raw_line.strip()
                if line.startswith("***"):
                    break
                if ":" not in line:
                    continue
                label, value = [part.strip() for part in line.split(":", maxsplit=1)]
                key = HEADER_FIELDS.get(label)
                if key:
                    metadata[key] = value
    except OSError as exc:
        metadata["read_error"] = str(exc)
    return metadata


def _try_folder_key(folder_name: str) -> tuple[str, str]:
    match = TRY_FOLDER_PATTERN.fullmatch(folder_name)
    if match is None:
        return "", ""
    try_id = match.group("try_id")
    return f"TRY_{try_id}", try_id


def _location_or_none(catalog: WeatherLocationCatalog, location_id: str) -> WeatherLocation | None:
    try:
        return catalog.get_location(location_id)
    except KeyError:
        return None


def _year_type_for_kind(kind: str, year: int | None) -> str:
    if kind == "jahr":
        return "future_year" if year in {2035, 2045} else "reference_year"
    return YEAR_TYPE_BY_KIND.get(kind, "")


def _kind_for_dataset_type(dataset_type: str) -> str:
    normalized = dataset_type.strip().casefold()
    if normalized == "jahr":
        return "jahr"
    if normalized == "sommer":
        return "somm"
    if normalized == "winter":
        return "wint"
    return ""


def _year_type_for_dataset_type(dataset_type: str, climate_scenario: str) -> str:
    kind = _kind_for_dataset_type(dataset_type)
    if kind == "jahr":
        if climate_scenario in {"future_2035", "future_2045"}:
            return "future_year"
        if climate_scenario in {"present", "present_2010"}:
            return "reference_year"
        return ""
    return YEAR_TYPE_BY_KIND.get(kind, "")


def _climate_scenario_for_year(year: int | None) -> str:
    if year == 2010:
        return "present_2010"
    if year == 2015:
        return "present"
    if year == 2035:
        return "future_2035"
    if year == 2045:
        return "future_2045"
    return ""


def _selection_priority(kind: str, year: int | None) -> int:
    base = 20 if year in {2035, 2045} else 10
    return base + {"jahr": 0, "somm": 1, "wint": 2}.get(kind, 9)


def _weather_key_for_discovery(location: WeatherLocation | None, year: int | None, kind: str) -> str:
    if location is None or year is None:
        return ""
    suffix = WEATHER_KEY_SUFFIX_BY_KIND.get(kind)
    if not suffix:
        return ""
    location_code = location.legacy_code or location.location_name
    return suggest_weather_key(location_code=location_code, year=year, year_type=_year_type_for_kind(kind, year))


def _missing_adjusted_fields(
    *,
    weather_key: str,
    display_name: str,
    location_id: str,
    dataset_type: str,
    climate_scenario: str,
    dataset_role: str,
    year: int | None,
    year_type: str,
) -> list[str]:
    missing_fields: list[str] = []
    if not weather_key.strip() or not WEATHER_KEY_PATTERN.fullmatch(weather_key.strip()):
        missing_fields.append("weather_key")
    if not display_name.strip():
        missing_fields.append("display_name")
    if not location_id.strip():
        missing_fields.append("location_id")
    if dataset_type not in set(DATASET_TYPE_BY_KIND.values()):
        missing_fields.append("dataset_type")
    if not climate_scenario:
        missing_fields.append("climate_scenario")
    if dataset_role not in VALID_DATASET_ROLES:
        missing_fields.append("dataset_role")
    if year is None or year < 1900 or year > 2100:
        missing_fields.append("year")
    if not year_type:
        missing_fields.append("year_type")
    return missing_fields


def _display_name_for_discovery(location: WeatherLocation | None, year: int | None, dataset_type: str) -> str:
    if location is None or year is None or not dataset_type:
        return ""
    return f"TRY {location.location_name} {year} {dataset_type}"


def _relative_to_project(path: Path, root: Path) -> Path:
    try:
        return path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("TRY-Datei muss innerhalb des Projektordners liegen.") from exc


def _normalize_relative_path(path: Path) -> str:
    return path.as_posix().replace("\\", "/")


def _dataset_role_label(dataset_role: str) -> str:
    if dataset_role == DATASET_ROLE_TRY_REFERENCE:
        return "TRY-Referenzdatensatz"
    if dataset_role == DATASET_ROLE_SITE_SPECIFIC:
        return "Standortgenauer Datensatz"
    return ""
