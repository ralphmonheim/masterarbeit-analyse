"""Neutrale Run-Objekte fuer die manuelle Simulationsuebergabe."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ma_analyse import OutputRequirementProfile


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


@dataclass(frozen=True, slots=True)
class RunVariantReference:
    """Direkte Zuordnung einer finalen VAR zu einem gemeinsamen RUN."""

    variant_id: str
    variant_fingerprint: str


@dataclass(frozen=True, slots=True)
class SimulationRunV1:
    """P018-Zielvertrag: eine finale Selection, ein Setup, mehrere VAR."""

    run_id: str
    selection_id: str
    selection_fingerprint: str
    parameter_snapshot_id: str
    parameter_snapshot_hash: str
    variants: tuple[RunVariantReference, ...]
    status: SimulationRunStatus = SimulationRunStatus.DRAFT

    def __post_init__(self) -> None:
        object.__setattr__(self, "variants", tuple(self.variants))
        if not self.run_id or not self.selection_id or not self.selection_fingerprint or not self.variants:
            raise ValueError("RUN braucht ID, finale Selection und mindestens eine VAR-Referenz.")
        if len({item.variant_id for item in self.variants}) != len(self.variants):
            raise ValueError("Eine VAR darf innerhalb eines RUN nur einmal vorkommen.")


@dataclass(frozen=True, slots=True)
class RunManifestV1:
    """Neutrales Mehrvarianten-Manifest ohne SimulationCase-Ebene."""

    run: SimulationRunV1
    simulation_setup: SimulationSetupSpecification
    output_requirements: tuple[OutputRequirementProfile, ...]
    preparation_notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "output_requirements", tuple(self.output_requirements))
        object.__setattr__(self, "preparation_notes", tuple(self.preparation_notes))
        if not self.output_requirements:
            raise ValueError("Ein RUN braucht mindestens eine ausgewaehlte Ausgabeanforderung.")
