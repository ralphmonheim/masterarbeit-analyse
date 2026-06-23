"""Append-only Sitzungsprotokoll fuer moduluebergreifende Ereignisse."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import uuid4

from .input_sources import utc_now

DEFAULT_SESSION_LOG_DIR = Path("logs/sessions")


def _timestamped_id(prefix: str) -> str:
    timestamp = utc_now().strftime("%Y%m%dT%H%M%S%fZ")
    return f"{prefix}_{timestamp}_{uuid4().hex[:12]}"


def create_session_id() -> str:
    """Erzeugt eine eindeutige Kennung fuer eine Bedien- oder Prozesssitzung."""
    return _timestamped_id("session")


def create_run_id(run_kind: str = "run") -> str:
    """Erzeugt eine eindeutige Kennung fuer einen einzelnen Lauf."""
    safe_kind = "".join(character if character.isalnum() else "_" for character in run_kind.strip().lower())
    return _timestamped_id(safe_kind or "run")


@dataclass(frozen=True, slots=True)
class SessionLogEvent:
    """Ein strukturierter Eintrag im lokalen Sitzungsprotokoll."""

    session_id: str
    event_type: str
    module_key: str
    run_id: str | None = None
    dataset_key: str | None = None
    severity: str | None = None
    diagnostic_code: str | None = None
    message: str = ""
    location: str | None = None
    source_id: str | None = None
    choice: str | None = None
    release_status: str | None = None
    note: str | None = None
    related_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: _timestamped_id("event"))
    occurred_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.session_id.strip():
            raise ValueError("session_id darf nicht leer sein.")
        if not self.event_type.strip():
            raise ValueError("event_type darf nicht leer sein.")
        if not self.module_key.strip():
            raise ValueError("module_key darf nicht leer sein.")
        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at muss eine Zeitzone enthalten.")


def _json_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


def _validate_session_id(session_id: str) -> None:
    if not session_id or not all(character.isalnum() or character in {"-", "_"} for character in session_id):
        raise ValueError("session_id enthaelt unzulaessige Zeichen.")


def append_session_event(
    event: SessionLogEvent,
    *,
    log_dir: str | Path = DEFAULT_SESSION_LOG_DIR,
) -> Path:
    """Haengt ein Ereignis als einzelne JSON-Zeile an das Sitzungslog an."""
    _validate_session_id(event.session_id)
    root = Path(log_dir)
    root.mkdir(parents=True, exist_ok=True)
    log_path = root / f"{event.session_id}.jsonl"
    payload = _json_value(asdict(event))
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return log_path
