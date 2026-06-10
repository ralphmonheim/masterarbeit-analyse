"""Neutraler Projektzustand fuer UI-Adapter."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ProjectState:
    """Haelt zentrale Projektauswahlen ohne direkte Streamlit-Abhaengigkeit."""

    project_folder: Path | None = None
    result_folder: Path | None = None
    weather_file: Path | None = None
    selected_variants: list[str] = field(default_factory=list)
    selected_rooms: list[str] = field(default_factory=list)
    simulation_start: str | None = None
    simulation_end: str | None = None
    timestep: str | None = None
    active_scenario: str | None = None
