"""Referenzen, Herkunft und Wertmetadaten fuer ma_technical v2."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import TypeVar

from ma_core import InputSource, utc_now

EnumT = TypeVar("EnumT", bound=StrEnum)


def coerce_enum(value: EnumT | str, enum_type: type[EnumT]) -> EnumT | str:
    """Konvertiert bekannte Stringwerte in ein StrEnum, ohne unbekannte Werte zu verlieren."""
    if isinstance(value, enum_type):
        return value
    value_text = str(value).strip()
    try:
        return enum_type(value_text)
    except ValueError:
        return value_text


def tuple_of_strings(values: Iterable[object] | None) -> tuple[str, ...]:
    """Normalisiert optionale Listen auf ein unveraenderliches String-Tuple."""
    if values is None:
        return ()
    return tuple(str(value).strip() for value in values if str(value).strip())


@dataclass(frozen=True, slots=True)
class ObjectReference:
    """Formatneutrale Referenz auf ein Objekt oder eine Revision."""

    object_id: str
    revision_id: str = ""
    content_hash: str = ""
    object_type: str = ""


@dataclass(frozen=True, slots=True)
class SourceMetadata:
    """Nachvollziehbare Herkunft eines manuellen oder importierten Technikstands."""

    source_type: str = "manual"
    source_reference: str = ""
    source_version: str = ""
    imported_or_entered_at: datetime = field(default_factory=utc_now)
    notes: str = ""
    input_source: InputSource | None = None

    def __post_init__(self) -> None:
        if self.imported_or_entered_at.tzinfo is None:
            raise ValueError("imported_or_entered_at muss eine Zeitzone enthalten.")


@dataclass(frozen=True, slots=True)
class TechnicalValueMetadata:
    """Metadaten fuer einzelne technische Werte."""

    source: SourceMetadata | None = None
    confirmation_status: str = "unconfirmed"
    variability: str = "fixed"
    assumption_reference: str = ""
    decision_reference: str = ""


@dataclass(frozen=True, slots=True)
class TechnicalAssumption:
    """Dokumentierte Annahme fuer technische Systeme."""

    assumption_id: str
    text: str
    location: str | None = None
