"""Formatneutrale Herkunfts- und Aenderungsmodelle fuer Eingabedaten."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any
from uuid import uuid4


def utc_now() -> datetime:
    """Erzeugt einen timezone-aware UTC-Zeitpunkt."""
    return datetime.now(timezone.utc)


def _create_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


class InputSourceKind(StrEnum):
    """Unterstuetzte fachliche Herkunftsarten."""

    IMPORT = "import"
    MANUAL = "manual"
    DEMO = "demo"


@dataclass(frozen=True, slots=True)
class InputSource:
    """Beschreibt die nachvollziehbare Herkunft eines Eingabestands."""

    module_key: str
    source_kind: InputSourceKind
    data_format: str
    source_path: Path | None = None
    adapter_key: str | None = None
    is_template: bool = False
    file_size_bytes: int | None = None
    sha256: str | None = None
    source_id: str = field(default_factory=lambda: _create_id("source"))
    loaded_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.module_key.strip():
            raise ValueError("module_key darf nicht leer sein.")
        if not self.data_format.strip():
            raise ValueError("data_format darf nicht leer sein.")
        if not isinstance(self.source_kind, InputSourceKind):
            object.__setattr__(self, "source_kind", InputSourceKind(self.source_kind))
        if self.source_path is not None and not isinstance(self.source_path, Path):
            object.__setattr__(self, "source_path", Path(self.source_path))
        if self.loaded_at.tzinfo is None:
            raise ValueError("loaded_at muss eine Zeitzone enthalten.")


@dataclass(frozen=True, slots=True)
class InputChange:
    """Dokumentiert eine bewusste manuelle Aenderung an Eingabedaten."""

    field_path: str
    old_value: Any
    new_value: Any
    reason: str
    change_id: str = field(default_factory=lambda: _create_id("change"))
    changed_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.field_path.strip():
            raise ValueError("field_path darf nicht leer sein.")
        if not self.reason.strip():
            raise ValueError("reason darf nicht leer sein.")
        if self.changed_at.tzinfo is None:
            raise ValueError("changed_at muss eine Zeitzone enthalten.")


def sha256_file(file_path: str | Path) -> str:
    """Berechnet eine SHA-256-Pruefsumme ohne die Datei zu veraendern."""
    path = Path(file_path)
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_input_source(
    *,
    module_key: str,
    source_kind: InputSourceKind,
    data_format: str,
    source_path: str | Path | None = None,
    adapter_key: str | None = None,
    is_template: bool = False,
) -> InputSource:
    """Erzeugt eine Quelle und erfasst vorhandene Dateimetadaten."""
    path = Path(source_path) if source_path is not None else None
    file_size_bytes: int | None = None
    checksum: str | None = None
    if path is not None:
        if not path.is_file():
            raise FileNotFoundError(f"Eingabedatei nicht gefunden: {path}")
        file_size_bytes = path.stat().st_size
        checksum = sha256_file(path)

    return InputSource(
        module_key=module_key,
        source_kind=source_kind,
        data_format=data_format,
        source_path=path,
        adapter_key=adapter_key,
        is_template=is_template,
        file_size_bytes=file_size_bytes,
        sha256=checksum,
    )
