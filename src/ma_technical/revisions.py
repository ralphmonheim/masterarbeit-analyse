"""Unveraenderliche, freigegebene YAML-Revisionen fuer Technikmodelle v2."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from ma_core import utc_now
from ma_validation import ReleaseStatus

from .specification import TechnicalModelSpecification
from .validation import validate_technical_model


@dataclass(frozen=True, slots=True)
class TechnicalModelRevision:
    """Freigegebener, hashbarer Technikstand ohne bearbeitbaren Draft."""

    technical_model_id: str
    revision_id: str
    content_hash: str
    release_status: ReleaseStatus
    specification_payload: dict[str, object]
    released_at: datetime


def release_technical_model(
    specification: TechnicalModelSpecification,
    *,
    revision_id: str,
    target_dir: str | Path,
) -> TechnicalModelRevision:
    """Validiert und speichert einen neuen freigegebenen Technikstand."""
    result = validate_technical_model(specification)
    if result.release_status is not ReleaseStatus.RELEASED:
        raise ValueError("Nur ein fehlerfreies v2-Technikmodell darf freigegeben werden.")
    payload = _to_payload(specification)
    content_hash = _content_hash(payload)
    revision = TechnicalModelRevision(
        technical_model_id=specification.technical_model_id,
        revision_id=revision_id,
        content_hash=content_hash,
        release_status=ReleaseStatus.RELEASED,
        specification_payload=payload,
        released_at=utc_now(),
    )
    path = Path(target_dir) / f"{revision_id}.yaml"
    if path.exists():
        raise FileExistsError(f"Technikrevision existiert bereits: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(_revision_payload(revision), sort_keys=False), encoding="utf-8")
    return revision


def load_technical_model_revision(path: str | Path) -> TechnicalModelRevision:
    """Laedt eine Revision und blockiert manipulierte YAML-Nutzlasten."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    payload = data.get("specification")
    if not isinstance(payload, dict):
        raise ValueError("Technikrevision enthaelt keine Spezifikationsnutzlast.")
    content_hash = str(data.get("content_hash", ""))
    if content_hash != _content_hash(payload):
        raise ValueError("Content-Hash der Technikrevision stimmt nicht mit der Nutzlast ueberein.")
    return TechnicalModelRevision(
        technical_model_id=str(data.get("technical_model_id", "")),
        revision_id=str(data.get("revision_id", "")),
        content_hash=content_hash,
        release_status=ReleaseStatus(str(data.get("release_status", ""))),
        specification_payload=payload,
        released_at=datetime.fromisoformat(str(data.get("released_at", ""))),
    )


def _revision_payload(revision: TechnicalModelRevision) -> dict[str, object]:
    return {
        "technical_model_id": revision.technical_model_id,
        "revision_id": revision.revision_id,
        "content_hash": revision.content_hash,
        "release_status": revision.release_status.value,
        "released_at": revision.released_at.isoformat(),
        "specification": revision.specification_payload,
    }


def _content_hash(payload: dict[str, object]) -> str:
    canonical_payload = _without_timestamps(payload)
    return hashlib.sha256(json.dumps(canonical_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _to_payload(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value):
        return {field.name: _to_payload(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, tuple):
        return [_to_payload(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_payload(item) for key, item in value.items()}
    return value


def _without_timestamps(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_timestamps(item)
            for key, item in value.items()
            if not key.endswith("_at")
        }
    if isinstance(value, list):
        return [_without_timestamps(item) for item in value]
    return value
