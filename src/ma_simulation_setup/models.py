"""Neutrale Run-Objekte fuer die manuelle Simulationsuebergabe."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ma_analyse.stage_1_dimensioning import OutputRequirementProfile


class SimulationRunStatus(StrEnum):
    """Status eines materialisierten Preprocess-Runs."""

    DRAFT = "draft"
    RELEASED_FOR_SIMULATION = "released_for_simulation"


@dataclass(frozen=True, slots=True)
class SimulationSetupSpecification:
    """Simulatorneutrale Randbedingungen eines vorbereiteten V1-Falls."""

    study_id: str
    study_case_type: str
    weather_key: str
    weather_label: str
    occupancy_schedule_key: str
    occupancy_start_hour: float
    occupancy_end_hour: float
    parent_variant_id: str = ""
    time_zone: str = "Europe/Berlin"
    simulation_period: str = "annual"
    simulation_start: str = ""
    simulation_end: str = ""
    calendar_definition: str = ""
    daylight_saving_time: bool = False
    simulation_timestep_seconds: int = 3600
    weather_source_revision: str = ""
    weather_source_sha256: str = ""
    preparation_only: bool = True

    def __post_init__(self) -> None:
        if not 0 <= self.occupancy_start_hour < self.occupancy_end_hour <= 24:
            raise ValueError("SimulationSetup benoetigt eine gueltige Belegungszeit.")
        if self.simulation_timestep_seconds <= 0:
            raise ValueError("SimulationSetup benoetigt einen positiven Zeitschritt.")


@dataclass(frozen=True, slots=True)
class SimulationRun:
    """Eine RUN/VAR-Zuordnung mit stabilen Quellenreferenzen."""

    run_id: str
    variant_id: str
    parameter_snapshot_id: str
    parameter_snapshot_hash: str
    variant_fingerprint: str
    status: SimulationRunStatus = SimulationRunStatus.DRAFT


@dataclass(frozen=True, slots=True)
class RunManifest:
    """Freigegebenes neutrales Manifest ohne Simulatoradapter."""

    run: SimulationRun
    output_requirements: tuple[OutputRequirementProfile, ...]
    preparation_notes: tuple[str, ...] = ()
    simulation_setup: SimulationSetupSpecification | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "output_requirements", tuple(self.output_requirements))
        object.__setattr__(self, "preparation_notes", tuple(self.preparation_notes))
