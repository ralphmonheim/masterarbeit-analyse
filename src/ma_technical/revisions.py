"""Unveraenderliche, freigegebene YAML-Revisionen fuer Technikmodelle v2."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from ma_core import utc_now
from ma_validation import DiagnosticSeverity, ReleaseStatus

from .specification import TechnicalModelSpecification
from .validation import validate_technical_model

_REVISION_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}\Z")


@dataclass(frozen=True, slots=True)
class ConfirmedTechnicalWarning:
    """Deterministischer Nachweis einer bewusst bestaetigten Warnung."""

    code: str
    location: str


@dataclass(frozen=True, slots=True)
class TechnicalModelRevision:
    """Freigegebener, hashbarer Technikstand ohne bearbeitbaren Draft."""

    technical_model_id: str
    revision_id: str
    content_hash: str
    release_status: ReleaseStatus
    specification_payload: dict[str, object]
    released_at: datetime
    warnings_confirmed: bool = False
    confirmed_warnings: tuple[ConfirmedTechnicalWarning, ...] = ()
    release_evidence_hash: str = ""


def release_technical_model(
    specification: TechnicalModelSpecification,
    *,
    revision_id: str,
    target_dir: str | Path,
    warnings_confirmed: bool = False,
) -> TechnicalModelRevision:
    """Validiert und speichert einen neuen freigegebenen Technikstand."""
    result = validate_technical_model(specification)
    if result.release_status is ReleaseStatus.BLOCKED:
        raise ValueError("Ein fehlerhaftes v2-Technikmodell darf nicht freigegeben werden.")
    if result.release_status is ReleaseStatus.CONFIRMATION_REQUIRED and not warnings_confirmed:
        raise ValueError("Warnungen der v2-Technikstruktur muessen ausdruecklich bestaetigt werden.")
    payload = _to_payload(specification)
    content_hash = _content_hash(payload)
    released_at = utc_now()
    warnings_confirmed_on_release = result.release_status is ReleaseStatus.CONFIRMATION_REQUIRED
    confirmed_warnings = _confirmed_warnings(result.messages) if warnings_confirmed_on_release else ()
    revision = TechnicalModelRevision(
        technical_model_id=specification.technical_model_id,
        revision_id=revision_id,
        content_hash=content_hash,
        release_status=ReleaseStatus.RELEASED,
        specification_payload=payload,
        released_at=released_at,
        warnings_confirmed=warnings_confirmed_on_release,
        confirmed_warnings=confirmed_warnings,
        release_evidence_hash=_release_evidence_hash(
            technical_model_id=specification.technical_model_id,
            revision_id=revision_id,
            content_hash=content_hash,
            warnings_confirmed=warnings_confirmed_on_release,
            confirmed_warnings=confirmed_warnings,
        ),
    )
    path = _revision_path(target_dir, revision_id)
    _write_new_revision(path, _revision_payload(revision))
    return revision


def load_technical_model_revision(path: str | Path) -> TechnicalModelRevision:
    """Laedt eine Revision und blockiert manipulierte YAML-Nutzlasten."""
    revision_path = Path(path)
    loaded_data = yaml.safe_load(revision_path.read_text(encoding="utf-8"))
    if loaded_data is None:
        data: dict[str, object] = {}
    elif isinstance(loaded_data, dict):
        data = loaded_data
    else:
        raise ValueError("Technikrevision muss ein YAML-Mapping als Wurzel enthalten.")
    payload = data.get("specification")
    if not isinstance(payload, dict):
        raise ValueError("Technikrevision enthaelt keine Spezifikationsnutzlast.")
    content_hash = str(data.get("content_hash", ""))
    if content_hash != _content_hash(payload):
        raise ValueError("Content-Hash der Technikrevision stimmt nicht mit der Nutzlast ueberein.")
    revision_id = str(data.get("revision_id", ""))
    if revision_path.suffix.lower() != ".yaml" or revision_path.stem != revision_id:
        raise ValueError("Dateiname und gespeicherte revision_id der Technikrevision muessen uebereinstimmen.")
    technical_model_id = str(data.get("technical_model_id", ""))
    release_status = ReleaseStatus(str(data.get("release_status", "")))
    warnings_confirmed = data.get("warnings_confirmed", False)
    if type(warnings_confirmed) is not bool:
        raise ValueError("warnings_confirmed der Technikrevision muss boolesch sein.")
    confirmed_warnings = _load_confirmed_warnings(data.get("confirmed_warnings", ()))
    release_evidence_hash = str(data.get("release_evidence_hash", ""))
    if release_evidence_hash:
        expected_evidence_hash = _release_evidence_hash(
            technical_model_id=technical_model_id,
            revision_id=revision_id,
            content_hash=content_hash,
            warnings_confirmed=warnings_confirmed,
            confirmed_warnings=confirmed_warnings,
        )
        if release_evidence_hash != expected_evidence_hash:
            raise ValueError("Freigabenachweis der Technikrevision ist nicht hashkonsistent.")
        _validate_confirmed_warnings(payload, warnings_confirmed, confirmed_warnings)
    elif warnings_confirmed or confirmed_warnings:
        raise ValueError("Bestaetigte Warnungen benoetigen einen hashgesicherten Freigabenachweis.")
    else:
        _validate_legacy_revision_without_evidence(payload)
    return TechnicalModelRevision(
        technical_model_id=technical_model_id,
        revision_id=revision_id,
        content_hash=content_hash,
        release_status=release_status,
        specification_payload=payload,
        released_at=datetime.fromisoformat(str(data.get("released_at", ""))),
        warnings_confirmed=warnings_confirmed,
        confirmed_warnings=confirmed_warnings,
        release_evidence_hash=release_evidence_hash,
    )


def technical_model_content_hash(specification: TechnicalModelSpecification) -> str:
    """Berechnet den spaeteren Revisionshash eines Entwurfs ohne Dateischreibzugriff."""
    if not isinstance(specification, TechnicalModelSpecification):
        raise TypeError("specification muss eine TechnicalModelSpecification sein.")
    return _content_hash(_to_payload(specification))


def _revision_payload(revision: TechnicalModelRevision) -> dict[str, object]:
    return {
        "technical_model_id": revision.technical_model_id,
        "revision_id": revision.revision_id,
        "content_hash": revision.content_hash,
        "release_status": revision.release_status.value,
        "released_at": revision.released_at.isoformat(),
        "warnings_confirmed": revision.warnings_confirmed,
        "confirmed_warnings": [
            {"code": warning.code, "location": warning.location}
            for warning in revision.confirmed_warnings
        ],
        "release_evidence_hash": revision.release_evidence_hash,
        "specification": revision.specification_payload,
    }


def _confirmed_warnings(messages) -> tuple[ConfirmedTechnicalWarning, ...]:
    return tuple(
        ConfirmedTechnicalWarning(code=message.code, location=message.location)
        for message in messages
        if message.severity is DiagnosticSeverity.WARNING
    )


def _load_confirmed_warnings(value: object) -> tuple[ConfirmedTechnicalWarning, ...]:
    if not isinstance(value, list | tuple):
        raise ValueError("confirmed_warnings der Technikrevision muss eine Liste sein.")
    result: list[ConfirmedTechnicalWarning] = []
    for item in value:
        if not isinstance(item, dict) or set(item) != {"code", "location"}:
            raise ValueError("confirmed_warnings enthaelt einen ungueltigen Eintrag.")
        code = item["code"]
        location = item["location"]
        if not isinstance(code, str) or not code.strip() or not isinstance(location, str):
            raise ValueError("confirmed_warnings benoetigt Code und Fundstelle als Text.")
        result.append(ConfirmedTechnicalWarning(code=code.strip(), location=location.strip()))
    return tuple(result)


def _validate_confirmed_warnings(
    payload: dict[str, object],
    warnings_confirmed: bool,
    confirmed_warnings: tuple[ConfirmedTechnicalWarning, ...],
) -> None:
    from .v2_loader import technical_model_specification_from_dict

    result = validate_technical_model(technical_model_specification_from_dict(payload))
    current_warnings = _confirmed_warnings(result.messages)
    if result.release_status is ReleaseStatus.BLOCKED:
        raise ValueError("Die gespeicherte Technikrevision ist nach erneuter Validierung blockiert.")
    if warnings_confirmed != bool(current_warnings) or confirmed_warnings != current_warnings:
        raise ValueError("Bestaetigte Warnungen stimmen nicht mit der gespeicherten Spezifikation ueberein.")


def _validate_legacy_revision_without_evidence(payload: dict[str, object]) -> None:
    from .v2_loader import technical_model_specification_from_dict

    result = validate_technical_model(technical_model_specification_from_dict(payload))
    if result.release_status is ReleaseStatus.BLOCKED:
        raise ValueError("Die gespeicherte Technikrevision ist nach erneuter Validierung blockiert.")
    if result.release_status is ReleaseStatus.CONFIRMATION_REQUIRED:
        raise ValueError("Eine warnungsbehaftete Technikrevision benoetigt einen Freigabenachweis.")


def _release_evidence_hash(
    *,
    technical_model_id: str,
    revision_id: str,
    content_hash: str,
    warnings_confirmed: bool,
    confirmed_warnings: tuple[ConfirmedTechnicalWarning, ...],
) -> str:
    return _content_hash(
        {
            "technical_model_id": technical_model_id,
            "revision_id": revision_id,
            "content_hash": content_hash,
            "warnings_confirmed": warnings_confirmed,
            "confirmed_warnings": [
                {"code": warning.code, "location": warning.location}
                for warning in confirmed_warnings
            ],
        }
    )


def _revision_path(target_dir: str | Path, revision_id: str) -> Path:
    """Baut einen einzelnen, sicheren YAML-Dateinamen fuer eine Revision."""
    if not isinstance(revision_id, str) or not _REVISION_ID_PATTERN.fullmatch(revision_id):
        raise ValueError("revision_id darf nur Buchstaben, Ziffern, Bindestriche und Unterstriche enthalten.")
    return Path(target_dir) / f"{revision_id}.yaml"


def _write_new_revision(path: Path, payload: dict[str, object]) -> None:
    """Schreibt eine Revision atomar neu; bestehende Dateien bleiben unveraendert."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)
            handle.flush()
            os.fsync(handle.fileno())
            temporary_path = Path(handle.name)
        try:
            os.link(temporary_path, path)
        except FileExistsError:
            raise FileExistsError(f"Technikrevision existiert bereits: {path}") from None
        temporary_path.unlink()
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def _content_hash(payload: dict[str, object]) -> str:
    canonical_payload = _without_timestamps(payload)
    return hashlib.sha256(
        json.dumps(canonical_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _to_payload(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return value.as_posix()
    if is_dataclass(value):
        return {field.name: _to_payload(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, tuple):
        return [_to_payload(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_payload(item) for key, item in value.items()}
    return value


def _without_timestamps(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _without_timestamps(item) for key, item in value.items() if not key.endswith("_at")}
    if isinstance(value, list):
        return [_without_timestamps(item) for item in value]
    return value
