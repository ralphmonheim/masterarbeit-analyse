"""Datenmodelle fuer Simulationsergebnis-Adapter."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class SimulationResultFolder:
    """Beschreibt einen vorhandenen aufbereiteten Ergebnisordner."""

    result_key: str
    result_dir: Path
    display_name: str


@dataclass(frozen=True, slots=True)
class VariantResultMapping:
    """Zuordnung einer Variante zu einem vorhandenen Ergebnisordner."""

    variant_key: str
    variant_name: str
    result_dir: Path | None
    result_display_name: str | None
    is_mapped: bool
    notes: list[str]


@dataclass(frozen=True, slots=True)
class RoomMetricResult:
    """Kennwerte eines Raums innerhalb einer Variante."""

    variant_key: str
    variant_name: str
    room_name: str
    source_file: Path
    metrics: dict[str, float | int | None]
    missing_columns: dict[str, list[str]]


@dataclass(frozen=True, slots=True)
class VariantMetricsResult:
    """Kennwerte einer Variante ueber alle gelesenen Raeume."""

    variant_key: str
    variant_name: str
    result_dir: Path
    room_metrics: list[RoomMetricResult]
    summary_metrics: dict[str, float | int | None]
    metadata: dict[str, Any]
