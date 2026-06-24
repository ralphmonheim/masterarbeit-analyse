"""Lokaler Aktivierungs- und Projekt-Default-Status fuer Wetterdatensaetze."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ma_core import utc_now
from ma_validation import ReleaseStatus

from .weather_catalog import WeatherCatalog, WeatherDataset

DEFAULT_WEATHER_SELECTION_STATE_PATH = Path("data/ma_weather/database/weather_selection_state.yaml")


@dataclass(frozen=True, slots=True)
class WeatherActivationRecord:
    """Nachweis einer bewussten Aktivierung eines Wetterdatensatzes."""

    weather_key: str
    import_id: str = ""
    activated_at: str = ""


@dataclass(frozen=True, slots=True)
class WeatherSelectionState:
    """Lokaler Status fuer aktivierte Datensaetze und Projekt-Default."""

    activations: tuple[WeatherActivationRecord, ...] = ()
    project_default_weather_key: str | None = None

    def is_activated(self, weather_key: str) -> bool:
        return any(record.weather_key == weather_key for record in self.activations)

    def activation_for(self, weather_key: str) -> WeatherActivationRecord | None:
        for record in self.activations:
            if record.weather_key == weather_key:
                return record
        return None


def load_weather_selection_state(
    state_path: str | Path = DEFAULT_WEATHER_SELECTION_STATE_PATH,
) -> WeatherSelectionState:
    """Laedt den lokalen Wetter-Auswahlstatus; fehlende Datei bedeutet leerer Status."""
    path = Path(state_path)
    if not path.exists():
        return WeatherSelectionState()
    raw_data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw_data, dict):
        raise ValueError(f"Wetter-Auswahlstatus muss ein YAML-Objekt enthalten: {path}")

    raw_activations = raw_data.get("activations", [])
    if not isinstance(raw_activations, list):
        raise ValueError("activations muss eine Liste sein.")

    activations = tuple(_activation_from_raw(item) for item in raw_activations)
    default_key = raw_data.get("project_default_weather_key")
    if default_key is not None:
        default_key = str(default_key).strip() or None
    return WeatherSelectionState(
        activations=activations,
        project_default_weather_key=default_key,
    )


def save_weather_selection_state(
    state: WeatherSelectionState,
    state_path: str | Path = DEFAULT_WEATHER_SELECTION_STATE_PATH,
) -> Path:
    """Speichert Aktivierungen und Projekt-Default als lokale YAML-Datei."""
    path = Path(state_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "activations": [
            {
                "weather_key": record.weather_key,
                "import_id": record.import_id,
                "activated_at": record.activated_at,
            }
            for record in state.activations
        ],
        "project_default_weather_key": state.project_default_weather_key,
    }
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def activate_weather_dataset(
    state: WeatherSelectionState,
    weather_key: str,
    *,
    release_status: ReleaseStatus,
    import_id: str = "",
) -> WeatherSelectionState:
    """Aktiviert einen freigegebenen Wetterdatensatz bewusst."""
    if release_status is not ReleaseStatus.RELEASED:
        raise ValueError("Nur freigegebene Wetterdatensaetze duerfen aktiviert werden.")
    normalized_key = weather_key.strip()
    if not normalized_key:
        raise ValueError("weather_key darf nicht leer sein.")

    activation = WeatherActivationRecord(
        weather_key=normalized_key,
        import_id=import_id.strip(),
        activated_at=utc_now().isoformat(),
    )
    remaining = tuple(record for record in state.activations if record.weather_key != normalized_key)
    return WeatherSelectionState(
        activations=(*remaining, activation),
        project_default_weather_key=state.project_default_weather_key,
    )


def set_project_default_weather_dataset(
    state: WeatherSelectionState,
    weather_key: str,
) -> WeatherSelectionState:
    """Setzt den Projekt-Default nur fuer bewusst aktivierte Datensaetze."""
    normalized_key = weather_key.strip()
    if not state.is_activated(normalized_key):
        raise ValueError("Projekt-Default ist nur fuer aktivierte Wetterdatensaetze erlaubt.")
    return WeatherSelectionState(
        activations=state.activations,
        project_default_weather_key=normalized_key,
    )


def project_default_weather_dataset(
    catalog: WeatherCatalog,
    state: WeatherSelectionState,
) -> WeatherDataset | None:
    """Gibt den aktivierten Projekt-Default fuer spaetere ma_parameters-Uebergabe zurueck."""
    default_key = state.project_default_weather_key
    if not default_key or not state.is_activated(default_key):
        return None
    return catalog.get(default_key)


def _activation_from_raw(raw_item: Any) -> WeatherActivationRecord:
    if not isinstance(raw_item, dict):
        raise ValueError("Ein Aktivierungseintrag muss ein Objekt sein.")
    weather_key = str(raw_item.get("weather_key", "")).strip()
    if not weather_key:
        raise ValueError("Aktivierungseintrag ohne weather_key.")
    return WeatherActivationRecord(
        weather_key=weather_key,
        import_id=str(raw_item.get("import_id", "")).strip(),
        activated_at=str(raw_item.get("activated_at", "")).strip(),
    )
