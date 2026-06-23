"""Gemeinsame, sichere Dateioperationen fuer kleine Konfigurationen."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

SUPPORTED_CONFIGURATION_SUFFIXES = {".json", ".yaml", ".yml"}


@dataclass(frozen=True, slots=True)
class ConfigurationSource:
    """Beschreibt Herkunft und Schutzstatus einer geladenen Konfiguration."""

    path: Path
    is_template: bool


@dataclass(frozen=True, slots=True)
class ConfigurationSaveResult:
    """Beschreibt das Ergebnis eines kontrollierten Speichervorgangs."""

    path: Path
    created: bool
    overwritten: bool


def load_configuration_file(config_path: str | Path) -> dict[str, Any]:
    """Laedt eine kleine JSON- oder YAML-Konfiguration als Dictionary."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {path}")

    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
    elif path.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        raise ValueError(f"Nicht unterstuetztes Konfigurationsformat: {path.suffix}")

    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Konfigurationsdatei muss ein Objekt enthalten: {path}")
    return data


def validate_configuration_filename(file_name: str, *, default_suffix: str = ".yaml") -> str:
    """Validiert einen einfachen Dateinamen ohne Pfadanteile."""
    normalized = file_name.strip()
    if not normalized:
        raise ValueError("Dateiname darf nicht leer sein.")
    if Path(normalized).name != normalized or "/" in normalized or "\\" in normalized:
        raise ValueError("Dateiname darf keine Pfadangaben enthalten.")

    path = Path(normalized)
    if not path.suffix:
        normalized = f"{normalized}{default_suffix}"
        path = Path(normalized)
    if path.suffix.lower() not in SUPPORTED_CONFIGURATION_SUFFIXES:
        raise ValueError("Unterstuetzte Dateiendungen sind .yaml, .yml und .json.")

    stem = path.stem
    if not stem or not all(character.isalnum() or character in {"-", "_"} for character in stem):
        raise ValueError("Dateiname darf nur Buchstaben, Zahlen, Bindestrich und Unterstrich enthalten.")
    return normalized


def _resolved_child_path(target_dir: str | Path, file_name: str) -> Path:
    root = Path(target_dir).resolve()
    target = (root / validate_configuration_filename(file_name)).resolve()
    if target.parent != root:
        raise ValueError("Zielpfad liegt ausserhalb des erlaubten Konfigurationsordners.")
    return target


def list_configuration_files(target_dir: str | Path) -> tuple[Path, ...]:
    """Listet vorhandene lokale Konfigurationsdateien sortiert auf."""
    root = Path(target_dir)
    if not root.exists():
        return ()
    return tuple(
        sorted(
            path
            for path in root.iterdir()
            if path.is_file() and path.suffix.lower() in SUPPORTED_CONFIGURATION_SUFFIXES
        )
    )


def save_yaml_configuration(
    payload: dict[str, Any],
    *,
    target_dir: str | Path,
    file_name: str,
    source: ConfigurationSource | None = None,
    overwrite_existing: bool = False,
    overwrite_confirmed: bool = False,
) -> ConfigurationSaveResult:
    """Speichert YAML, ohne Vorlagen oder fremde Pfade zu ueberschreiben."""
    target = _resolved_child_path(target_dir, file_name)
    if target.suffix.lower() not in {".yaml", ".yml"}:
        raise ValueError("Dieser Speicheradapter unterstuetzt nur YAML-Dateien.")
    if target.is_symlink():
        raise ValueError("Symbolische Verknuepfungen sind als Speicherziel nicht zulaessig.")
    target_exists = target.exists()

    if overwrite_existing:
        if not overwrite_confirmed:
            raise PermissionError("Ueberschreiben wurde nicht ausdruecklich bestaetigt.")
        if source is None or source.is_template:
            raise PermissionError("Vorlagen und unbekannte Quellen duerfen nicht ueberschrieben werden.")
        if source.path.resolve() != target:
            raise PermissionError("Nur die aktuell geladene eigene Datei darf ueberschrieben werden.")
        if not target_exists:
            raise FileNotFoundError(f"Zu ueberschreibende Datei wurde nicht gefunden: {target}")
    elif target_exists:
        raise FileExistsError(
            f"Datei existiert bereits: {target.name}. Bitte einen anderen neuen Dateinamen auswaehlen."
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return ConfigurationSaveResult(
        path=target,
        created=not target_exists,
        overwritten=target_exists,
    )
