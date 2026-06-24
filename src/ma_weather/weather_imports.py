"""Lokaler Import eigener TRY-Wetterdatensaetze."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ma_core import create_run_id

from .weather_catalog import (
    DATASET_ROLE_SITE_SPECIFIC,
    DATASET_ROLE_TRY_REFERENCE,
    DEFAULT_LOCAL_WEATHER_DATASETS_CONFIG,
    VALID_DATASET_ROLES,
    WeatherCatalog,
    WeatherDataset,
)
from .weather_status import (
    WeatherDatasetStatus,
    create_weather_import_id,
    inspect_weather_dataset_status,
)

DWD_TRY_URL = "https://www.dwd.de/DE/leistungen/testreferenzjahre/testreferenzjahre.html"
LOCAL_WEATHER_INPUT_DIR = Path("data/ma_weather/input/custom")
LOCAL_WEATHER_DATASETS_CONFIG = DEFAULT_LOCAL_WEATHER_DATASETS_CONFIG

VALID_WEATHER_IMPORT_YEAR_TYPES = {
    "reference_year",
    "future_year",
    "summer_extreme",
    "winter_extreme",
}

WEATHER_KEY_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


@dataclass(frozen=True, slots=True)
class WeatherDatasetImportDraft:
    """Metadaten fuer einen lokalen Wetterdatensatz vor dem Speichern."""

    weather_key: str
    display_name: str
    original_filename: str
    location: str
    year_type: str
    climate_scenario: str
    dataset_role: str
    location_id: str
    reference_location_id: str
    selection_priority: int = 100
    file_format: str = "TRY"
    source: str = "Lokaler Import"
    notes: str = "Lokaler Import ueber Streamlit."
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class WeatherDatasetImportResult:
    """Ergebnis eines lokalen Importvorgangs."""

    dataset: WeatherDataset
    status: WeatherDatasetStatus
    catalog_path: Path
    copied_file_path: Path
    import_id: str
    session_id: str
    run_id: str


def suggest_weather_key(
    *,
    location_code: str,
    year: int,
    year_type: str,
) -> str:
    """Schlaegt einen stabilen weather_key fuer einen lokalen Import vor."""
    suffix_by_type = {
        "reference_year": "JAHR",
        "future_year": "JAHR",
        "summer_extreme": "SOMM",
        "winter_extreme": "WINT",
    }
    location_part = _weather_key_part(location_code) or "LOCAL"
    suffix = suffix_by_type.get(year_type, "JAHR")
    return f"TRY_{location_part}_{year}_{suffix}"


def import_local_weather_dataset(
    file_content: bytes,
    *,
    draft: WeatherDatasetImportDraft,
    existing_catalog: WeatherCatalog,
    project_root: str | Path | None = None,
    local_catalog_path: str | Path = LOCAL_WEATHER_DATASETS_CONFIG,
    input_dir: str | Path = LOCAL_WEATHER_INPUT_DIR,
    session_id: str = "",
    run_id: str | None = None,
    import_id: str | None = None,
) -> WeatherDatasetImportResult:
    """Speichert einen lokalen TRY-Datensatz und prueft ihn direkt.

    Die Datei wird in den projektlokalen Datenbereich kopiert. Der YAML-Eintrag
    enthaelt nur einen relativen Pfad, damit der Projektordner verschiebbar
    bleibt.
    """
    root = Path.cwd() if project_root is None else Path(project_root)
    normalized_draft = validate_weather_import_draft(draft)
    if not file_content:
        raise ValueError("Die Importdatei ist leer.")
    if any(dataset.weather_key == normalized_draft.weather_key for dataset in existing_catalog.datasets):
        raise ValueError(f"weather_key ist bereits vorhanden: {normalized_draft.weather_key}")

    import_id = import_id or create_weather_import_id()
    run_id = run_id or create_run_id("weather_import")
    target_file = _target_import_file(
        root=root,
        input_dir=Path(input_dir),
        weather_key=normalized_draft.weather_key,
        original_filename=normalized_draft.original_filename,
    )
    if target_file.exists():
        raise FileExistsError(f"Importdatei existiert bereits: {target_file}")

    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_bytes(file_content)
    relative_file_path = _relative_to_project(target_file, root)
    dataset = _dataset_from_draft(normalized_draft, relative_file_path)
    catalog_path = root / Path(local_catalog_path)
    _append_local_dataset_record(catalog_path, dataset)
    status = inspect_weather_dataset_status(
        dataset,
        project_root=root,
        validate_file=True,
        import_id=import_id,
        session_id=session_id,
        run_id=run_id,
    )
    return WeatherDatasetImportResult(
        dataset=dataset,
        status=status,
        catalog_path=catalog_path,
        copied_file_path=target_file,
        import_id=import_id,
        session_id=session_id,
        run_id=run_id,
    )


def validate_weather_import_draft(draft: WeatherDatasetImportDraft) -> WeatherDatasetImportDraft:
    """Validiert und normalisiert Metadaten fuer einen lokalen TRY-Import."""
    weather_key = draft.weather_key.strip()
    display_name = draft.display_name.strip()
    original_filename = Path(draft.original_filename.strip()).name
    location = draft.location.strip()
    year_type = draft.year_type.strip()
    climate_scenario = draft.climate_scenario.strip()
    dataset_role = draft.dataset_role.strip()
    location_id = draft.location_id.strip()
    reference_location_id = draft.reference_location_id.strip()
    file_format = draft.file_format.strip() or "TRY"
    source = draft.source.strip() or "Lokaler Import"
    notes = draft.notes.strip()

    if not weather_key or not WEATHER_KEY_PATTERN.fullmatch(weather_key):
        raise ValueError("weather_key darf nur Buchstaben, Zahlen, Bindestrich und Unterstrich enthalten.")
    if not display_name:
        raise ValueError("Anzeigename darf nicht leer sein.")
    if not original_filename or Path(original_filename).suffix.lower() != ".dat":
        raise ValueError("Der Import unterstuetzt in diesem Slice nur entpackte .dat-Dateien.")
    if not location:
        raise ValueError("Ort darf nicht leer sein.")
    if year_type not in VALID_WEATHER_IMPORT_YEAR_TYPES:
        raise ValueError(f"Ungueltiger Datensatztyp: {year_type}")
    if not climate_scenario:
        raise ValueError("Szenario darf nicht leer sein.")
    if dataset_role not in VALID_DATASET_ROLES:
        raise ValueError(f"Ungueltige Rolle: {dataset_role}")
    if dataset_role == DATASET_ROLE_SITE_SPECIFIC and not location_id:
        raise ValueError("Standortgenaue Datensaetze brauchen eine Standort-ID.")
    if dataset_role == DATASET_ROLE_TRY_REFERENCE and not reference_location_id:
        raise ValueError("TRY-Referenzdatensaetze brauchen eine Referenzstandort-ID.")
    if draft.selection_priority < 0:
        raise ValueError("Prioritaet muss eine nichtnegative Ganzzahl sein.")

    return WeatherDatasetImportDraft(
        weather_key=weather_key,
        display_name=display_name,
        original_filename=original_filename,
        location=location,
        year_type=year_type,
        climate_scenario=climate_scenario,
        dataset_role=dataset_role,
        location_id=location_id,
        reference_location_id=reference_location_id,
        selection_priority=draft.selection_priority,
        file_format=file_format,
        source=source,
        notes=notes,
        is_active=draft.is_active,
    )


def _weather_key_part(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", value.strip().upper()).strip("_")
    return normalized


def _target_import_file(
    *,
    root: Path,
    input_dir: Path,
    weather_key: str,
    original_filename: str,
) -> Path:
    target_root = root / input_dir / weather_key
    filename = _safe_import_filename(original_filename)
    target = (target_root / filename).resolve()
    if target.parent != target_root.resolve():
        raise ValueError("Zieldatei liegt ausserhalb des Importordners.")
    return target


def _safe_import_filename(filename: str) -> str:
    name = Path(filename).name.strip()
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", Path(name).stem).strip("._-")
    suffix = Path(name).suffix.lower()
    if not stem:
        stem = "weather_import"
    if suffix != ".dat":
        raise ValueError("Der Import unterstuetzt in diesem Slice nur entpackte .dat-Dateien.")
    return f"{stem}{suffix}"


def _relative_to_project(path: Path, root: Path) -> Path:
    try:
        return path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("Importdatei muss innerhalb des Projektordners liegen.") from exc


def _dataset_from_draft(draft: WeatherDatasetImportDraft, relative_file_path: Path) -> WeatherDataset:
    return WeatherDataset(
        weather_key=draft.weather_key,
        display_name=draft.display_name,
        file_path=relative_file_path,
        file_format=draft.file_format,
        source=draft.source,
        location=draft.location,
        year_type=draft.year_type,
        climate_scenario=draft.climate_scenario,
        dataset_role=draft.dataset_role,
        location_id=draft.location_id,
        reference_location_id=draft.reference_location_id,
        selection_priority=draft.selection_priority,
        is_active=draft.is_active,
        notes=draft.notes,
    )


def _append_local_dataset_record(catalog_path: Path, dataset: WeatherDataset) -> None:
    payload = _load_local_catalog_payload(catalog_path)
    records = payload.setdefault("weather_datasets", [])
    if not isinstance(records, list):
        raise ValueError(f"Lokaler Wetterkatalog muss eine Liste enthalten: {catalog_path}")
    if any(isinstance(record, dict) and record.get("weather_key") == dataset.weather_key for record in records):
        raise ValueError(f"weather_key ist im lokalen Wetterkatalog bereits vorhanden: {dataset.weather_key}")
    records.append(_dataset_to_record(dataset))
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def _load_local_catalog_payload(catalog_path: Path) -> dict[str, Any]:
    if not catalog_path.exists():
        return {"weather_datasets": []}
    payload = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    if payload is None:
        return {"weather_datasets": []}
    if not isinstance(payload, dict):
        raise ValueError(f"Lokaler Wetterkatalog muss ein YAML-Objekt sein: {catalog_path}")
    return payload


def _dataset_to_record(dataset: WeatherDataset) -> dict[str, Any]:
    return {
        "weather_key": dataset.weather_key,
        "display_name": dataset.display_name,
        "file_path": dataset.file_path.as_posix(),
        "file_format": dataset.file_format,
        "source": dataset.source,
        "location": dataset.location,
        "year_type": dataset.year_type,
        "climate_scenario": dataset.climate_scenario,
        "dataset_role": dataset.dataset_role,
        "location_id": dataset.location_id,
        "reference_location_id": dataset.reference_location_id,
        "selection_priority": dataset.selection_priority,
        "is_active": dataset.is_active,
        "notes": dataset.notes,
    }
