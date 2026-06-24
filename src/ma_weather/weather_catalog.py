"""Katalog fuer lokale Wetterdatensaetze."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_WEATHER_DATASETS_CONFIG = Path("config/ma_weather/datasets/example_weather_datasets.yaml")
DEFAULT_LOCAL_WEATHER_DATASETS_CONFIG = Path("data/ma_weather/config/datasets/weather_datasets_local.yaml")

DATASET_ROLE_TRY_REFERENCE = "try_reference"
DATASET_ROLE_SITE_SPECIFIC = "site_specific"
VALID_DATASET_ROLES = (DATASET_ROLE_TRY_REFERENCE, DATASET_ROLE_SITE_SPECIFIC)
DATASET_ROLE_ORDER = {
    DATASET_ROLE_TRY_REFERENCE: 0,
    DATASET_ROLE_SITE_SPECIFIC: 1,
    "": 2,
}

REQUIRED_TEXT_FIELDS = (
    "weather_key",
    "display_name",
    "file_path",
    "file_format",
    "source",
    "location",
    "year_type",
)


@dataclass(frozen=True, slots=True)
class WeatherDataset:
    """Beschreibt einen lokalen Wetterdatensatz ohne den Dateiinhalt zu speichern."""

    weather_key: str
    display_name: str
    file_path: Path
    file_format: str
    source: str
    location: str
    year_type: str
    climate_scenario: str = ""
    dataset_role: str = ""
    location_id: str = ""
    reference_location_id: str = ""
    selection_priority: int = 100
    is_active: bool = True
    notes: str = ""

    def resolved_file_path(self, base_dir: str | Path | None = None) -> Path:
        """Gibt den absoluten Dateipfad zurueck, ohne die Datei vorauszusetzen."""
        if self.file_path.is_absolute():
            return self.file_path
        base_path = Path.cwd() if base_dir is None else Path(base_dir)
        return base_path / self.file_path


@dataclass(frozen=True, slots=True)
class WeatherCatalog:
    """Sammlung registrierter Wetterdatensaetze."""

    datasets: list[WeatherDataset]

    def active_datasets(self) -> list[WeatherDataset]:
        """Gibt nur aktive Datensaetze zurueck."""
        return [dataset for dataset in self.datasets if dataset.is_active]

    def datasets_for_location(
        self,
        *,
        location_id: str,
        reference_location_id: str,
    ) -> list[WeatherDataset]:
        """Gibt eindeutig zugeordnete Datensaetze fuer eine Stadt sortiert zurueck.

        TRY-Referenzdatensaetze werden zuerst gelistet. Standortgenaue
        Datensaetze folgen danach. Datensaetze ohne klare neue Zuordnung werden
        hier bewusst nicht als Ersatz zurueckgegeben.
        """
        matching_datasets = [
            dataset
            for dataset in self.active_datasets()
            if _dataset_matches_location(
                dataset,
                location_id=location_id,
                reference_location_id=reference_location_id,
            )
        ]
        return sorted(
            matching_datasets,
            key=lambda dataset: (
                DATASET_ROLE_ORDER.get(dataset.dataset_role, 99),
                dataset.selection_priority,
                dataset.display_name,
            ),
        )

    def get(self, weather_key: str) -> WeatherDataset:
        """Findet einen Datensatz ueber seinen technischen weather_key."""
        for dataset in self.datasets:
            if dataset.weather_key == weather_key:
                return dataset
        raise KeyError(f"Wetterdatensatz nicht gefunden: {weather_key}")


def import_weather_catalog(
    config_path: str | Path = DEFAULT_WEATHER_DATASETS_CONFIG,
    *,
    local_config_path: str | Path | None = DEFAULT_LOCAL_WEATHER_DATASETS_CONFIG,
    include_local: bool | None = None,
    require_existing_files: bool = False,
) -> WeatherCatalog:
    """Laedt den Wetterkatalog aus einer oder zwei YAML-Dateien.

    Reale TRY-Dateien duerfen lokal fehlen, solange `require_existing_files`
    nicht gesetzt ist. Dadurch kann das Repo nur die Struktur versionieren.
    Bei Nutzung des Standardkatalogs wird ein vorhandener lokaler Importkatalog
    aus `data/ma_weather/config` automatisch ergaenzt.
    """
    path = Path(config_path)
    if include_local is None:
        include_local = path == DEFAULT_WEATHER_DATASETS_CONFIG
    config_paths = [path]
    if include_local and local_config_path is not None:
        local_path = Path(local_config_path)
        if local_path.exists():
            config_paths.append(local_path)

    datasets: list[WeatherDataset] = []
    errors: list[str] = []
    seen_keys: set[str] = set()

    for config_file in config_paths:
        raw_config = _load_yaml_object(config_file)
        raw_datasets = raw_config.get("weather_datasets", [])
        if not isinstance(raw_datasets, list):
            errors.append(f"{config_file}: weather_datasets muss eine Liste sein.")
            continue

        for index, raw_dataset in enumerate(raw_datasets, start=1):
            if not isinstance(raw_dataset, dict):
                errors.append(f"{config_file}: weather_datasets[{index}] muss ein Objekt sein.")
                continue

            dataset_errors = _validate_dataset_record(raw_dataset, index, source_path=config_file)
            weather_key = str(raw_dataset.get("weather_key", "")).strip()
            if weather_key and weather_key in seen_keys:
                dataset_errors.append(f"{config_file}: weather_datasets[{index}].weather_key ist doppelt: {weather_key}")
            seen_keys.add(weather_key)

            if dataset_errors:
                errors.extend(dataset_errors)
                continue

            dataset = _build_weather_dataset(raw_dataset)
            if require_existing_files and not dataset.resolved_file_path().exists():
                errors.append(f"Datei fuer {dataset.weather_key} nicht gefunden: {dataset.file_path}")
                continue
            datasets.append(dataset)

    if errors:
        raise ValueError("; ".join(errors))

    return WeatherCatalog(datasets=datasets)


def _load_yaml_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Wetterkatalog nicht gefunden: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Wetterkatalog muss ein YAML-Objekt enthalten: {path}")
    return data


def _validate_dataset_record(
    raw_dataset: dict[str, Any],
    index: int,
    *,
    source_path: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    prefix = f"{source_path}: " if source_path is not None else ""
    for field_name in REQUIRED_TEXT_FIELDS:
        value = raw_dataset.get(field_name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{prefix}weather_datasets[{index}].{field_name} fehlt oder ist leer.")

    is_active = raw_dataset.get("is_active", True)
    if not isinstance(is_active, bool):
        errors.append(f"{prefix}weather_datasets[{index}].is_active muss true oder false sein.")

    dataset_role = str(raw_dataset.get("dataset_role", "")).strip()
    location_id = str(raw_dataset.get("location_id", "")).strip()
    reference_location_id = str(raw_dataset.get("reference_location_id", "")).strip()
    if dataset_role and dataset_role not in VALID_DATASET_ROLES:
        errors.append(
            f"{prefix}weather_datasets[{index}].dataset_role ist ungueltig: {dataset_role}. "
            f"Erlaubt sind {', '.join(VALID_DATASET_ROLES)}."
        )
    if not dataset_role and (location_id or reference_location_id):
        errors.append(f"{prefix}weather_datasets[{index}].dataset_role fehlt fuer die Standortzuordnung.")
    if dataset_role == DATASET_ROLE_TRY_REFERENCE and not reference_location_id:
        errors.append(f"{prefix}weather_datasets[{index}].reference_location_id fehlt fuer TRY-Referenzdatensatz.")
    if dataset_role == DATASET_ROLE_SITE_SPECIFIC and not location_id:
        errors.append(f"{prefix}weather_datasets[{index}].location_id fehlt fuer standortgenauen Datensatz.")

    selection_priority = raw_dataset.get("selection_priority", 100)
    if not isinstance(selection_priority, int) or selection_priority < 0:
        errors.append(f"{prefix}weather_datasets[{index}].selection_priority muss eine nichtnegative Ganzzahl sein.")
    return errors


def _build_weather_dataset(raw_dataset: dict[str, Any]) -> WeatherDataset:
    return WeatherDataset(
        weather_key=str(raw_dataset["weather_key"]).strip(),
        display_name=str(raw_dataset["display_name"]).strip(),
        file_path=Path(str(raw_dataset["file_path"]).strip()),
        file_format=str(raw_dataset["file_format"]).strip(),
        source=str(raw_dataset["source"]).strip(),
        location=str(raw_dataset["location"]).strip(),
        year_type=str(raw_dataset["year_type"]).strip(),
        climate_scenario=str(raw_dataset.get("climate_scenario", "")).strip(),
        dataset_role=str(raw_dataset.get("dataset_role", "")).strip(),
        location_id=str(raw_dataset.get("location_id", "")).strip(),
        reference_location_id=str(raw_dataset.get("reference_location_id", "")).strip(),
        selection_priority=int(raw_dataset.get("selection_priority", 100)),
        is_active=bool(raw_dataset.get("is_active", True)),
        notes=str(raw_dataset.get("notes", "")).strip(),
    )


def _dataset_matches_location(
    dataset: WeatherDataset,
    *,
    location_id: str,
    reference_location_id: str,
) -> bool:
    if dataset.dataset_role == DATASET_ROLE_TRY_REFERENCE:
        return dataset.reference_location_id == reference_location_id
    if dataset.dataset_role == DATASET_ROLE_SITE_SPECIFIC:
        return dataset.location_id == location_id
    return False
