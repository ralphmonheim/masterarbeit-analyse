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

    def __post_init__(self) -> None:
        object.__setattr__(self, "output_requirements", tuple(self.output_requirements))
        object.__setattr__(self, "preparation_notes", tuple(self.preparation_notes))
