"""Neutrale Projekt- und Benennungsmodelle fuer den Demo-Workflow."""

from __future__ import annotations

from dataclasses import dataclass


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} darf nicht leer sein.")


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
