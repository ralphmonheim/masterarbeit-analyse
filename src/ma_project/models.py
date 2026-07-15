"""Neutrale Projekt- und Benennungsmodelle fuer den Demo-Workflow."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, replace
from datetime import UTC, datetime

_PROJECT_ID_PATTERN = re.compile(r"PRJ-[0-9]{6}\Z")
_COUNTRY_CODE_PATTERN = re.compile(r"[A-Z]{2}\Z")


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} darf nicht leer sein.")


def _require_project_text(value: str, field_name: str, *, allow_empty: bool = False) -> None:
    """Validate new P011 text without changing the established P028 helper."""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} muss ein Text sein.")
    if not allow_empty and not value.strip():
        raise ValueError(f"{field_name} darf nicht leer sein.")
    if "\x00" in value:
        raise ValueError(f"{field_name} darf kein Nullzeichen enthalten.")


def _require_project_id(value: str) -> None:
    if not isinstance(value, str) or not _PROJECT_ID_PATTERN.fullmatch(value):
        raise ValueError("project_id muss dem Format PRJ-000001 entsprechen.")


def _require_optional_number(
    value: float | int | None,
    field_name: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} muss eine Zahl sein.")
    if not math.isfinite(float(value)):
        raise ValueError(f"{field_name} muss endlich sein.")
    if minimum is not None and value < minimum:
        raise ValueError(f"{field_name} muss mindestens {minimum} sein.")
    if maximum is not None and value > maximum:
        raise ValueError(f"{field_name} darf hoechstens {maximum} sein.")


def _require_aware_datetime(value: datetime, field_name: str) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} muss ein zeitzonenbewusster datetime-Wert sein.")


@dataclass(frozen=True, slots=True)
class SimulationProgramProfile:
    """Beschreibt ein frei verwaltbares Simulationsprogramm."""

    program_key: str
    display_name: str
    version: str = ""
    note: str = ""

    def __post_init__(self) -> None:
        _require_text(self.program_key, "program_key")
        _require_text(self.display_name, "display_name")


@dataclass(frozen=True, slots=True)
class VariantNamingPart:
    """Ordnet den Optionswerten eines Parameters kurze Namenstokens zu."""

    parameter_key: str
    option_tokens: dict[str, str]

    def __post_init__(self) -> None:
        _require_text(self.parameter_key, "parameter_key")
        if not self.option_tokens:
            raise ValueError("option_tokens darf nicht leer sein.")
        for option_key, token in self.option_tokens.items():
            _require_text(option_key, "option_key")
            _require_text(token, f"Token fuer {option_key}")


@dataclass(frozen=True, slots=True)
class VariantNamingProfile:
    """Neutrales, simulationsprogrammunabhaengiges Benennungsprofil."""

    prefix: str
    index_width: int
    separator: str
    include_index: bool
    parts: tuple[VariantNamingPart, ...]

    def __post_init__(self) -> None:
        _require_text(self.prefix, "prefix")
        _require_text(self.separator, "separator")
        if isinstance(self.index_width, bool) or not isinstance(self.index_width, int) or self.index_width < 1:
            raise ValueError("index_width muss eine positive ganze Zahl sein.")
        if not self.parts:
            raise ValueError("parts darf nicht leer sein.")


@dataclass(frozen=True, slots=True)
class ProjectIdentity:
    """Stable, human-readable master data that identifies one project."""

    project_id: str
    title: str
    short_name: str
    description: str = ""
    project_type: str = ""
    author: str = ""
    organization: str = ""

    def __post_init__(self) -> None:
        _require_project_id(self.project_id)
        _require_project_text(self.title, "title")
        _require_project_text(self.short_name, "short_name")
        for field_name in ("description", "project_type", "author", "organization"):
            _require_project_text(getattr(self, field_name), field_name, allow_empty=True)


@dataclass(frozen=True, slots=True)
class ProjectLocation:
    """General location data without a weather-data or TRY selection."""

    country_code: str
    display_name: str = ""
    postal_code: str = ""
    city: str = ""
    street: str = ""
    house_number: str = ""
    latitude_deg: float | int | None = None
    longitude_deg: float | int | None = None
    elevation_m: float | int | None = None
    timezone: str = ""
    notes: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.country_code, str) or not _COUNTRY_CODE_PATTERN.fullmatch(self.country_code):
            raise ValueError("country_code muss aus genau zwei Grossbuchstaben bestehen.")
        for field_name in (
            "display_name",
            "postal_code",
            "city",
            "street",
            "house_number",
            "timezone",
            "notes",
        ):
            _require_project_text(getattr(self, field_name), field_name, allow_empty=True)
        if not self.display_name.strip() and not self.city.strip():
            raise ValueError("ProjectLocation braucht display_name oder city.")
        if (self.latitude_deg is None) != (self.longitude_deg is None):
            raise ValueError("latitude_deg und longitude_deg muessen zusammen gesetzt werden.")
        _require_optional_number(self.latitude_deg, "latitude_deg", minimum=-90, maximum=90)
        _require_optional_number(self.longitude_deg, "longitude_deg", minimum=-180, maximum=180)
        _require_optional_number(self.elevation_m, "elevation_m")


@dataclass(frozen=True, slots=True)
class ProjectInvestigation:
    """Human-readable investigation frame without variant or run objects."""

    objective: str = ""
    research_question: str = ""
    reference_case_description: str = ""
    scope: str = ""
    exclusions: tuple[str, ...] = ()
    methodology_note: str = ""
    notes: str = ""

    def __post_init__(self) -> None:
        for field_name in (
            "objective",
            "research_question",
            "reference_case_description",
            "scope",
            "methodology_note",
            "notes",
        ):
            _require_project_text(getattr(self, field_name), field_name, allow_empty=True)

        if isinstance(self.exclusions, (str, bytes)) or not isinstance(self.exclusions, (tuple, list)):
            raise ValueError("exclusions muss eine Liste oder ein Tupel aus Texten sein.")
        normalized_exclusions = tuple(self.exclusions)
        for index, exclusion in enumerate(normalized_exclusions):
            _require_project_text(exclusion, f"exclusions[{index}]")
        object.__setattr__(self, "exclusions", normalized_exclusions)


@dataclass(frozen=True, slots=True)
class Project:
    """Immutable project aggregate for the first, persistence-free P011 slice."""

    identity: ProjectIdentity
    created_at: datetime
    updated_at: datetime
    location: ProjectLocation | None = None
    investigation: ProjectInvestigation | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.identity, ProjectIdentity):
            raise ValueError("identity muss ein ProjectIdentity-Objekt sein.")
        _require_aware_datetime(self.created_at, "created_at")
        _require_aware_datetime(self.updated_at, "updated_at")
        if self.updated_at.astimezone(UTC) < self.created_at.astimezone(UTC):
            raise ValueError("updated_at darf nicht vor created_at liegen.")
        if self.location is not None and not isinstance(self.location, ProjectLocation):
            raise ValueError("location muss ein ProjectLocation-Objekt oder None sein.")
        if self.investigation is not None and not isinstance(self.investigation, ProjectInvestigation):
            raise ValueError("investigation muss ein ProjectInvestigation-Objekt oder None sein.")


@dataclass(frozen=True, slots=True)
class ProjectContext:
    """Small read-only payload for the later initialization of another module."""

    project_id: str
    title: str
    short_name: str
    location: ProjectLocation | None = None

    def __post_init__(self) -> None:
        _require_project_id(self.project_id)
        _require_project_text(self.title, "title")
        _require_project_text(self.short_name, "short_name")
        if self.location is not None and not isinstance(self.location, ProjectLocation):
            raise ValueError("location muss ein ProjectLocation-Objekt oder None sein.")


def project_context_from_project(project: Project) -> ProjectContext:
    """Build a small context with an independent immutable location value."""
    if not isinstance(project, Project):
        raise TypeError("project muss ein Project-Objekt sein.")
    location = replace(project.location) if project.location is not None else None
    return ProjectContext(
        project_id=project.identity.project_id,
        title=project.identity.title,
        short_name=project.identity.short_name,
        location=location,
    )
