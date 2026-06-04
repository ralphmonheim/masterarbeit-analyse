"""Adapter fuer vorhandene Simulationsergebnisordner aus `ma_analyse`."""

from .adapter import (
    discover_result_folders,
    map_result_folders_to_variants,
    resolve_result_folder,
)
from .export import export_simulation_metrics_to_json
from .metrics import collect_simulation_metrics, read_room_metrics, read_variant_metrics
from .models import (
    RoomMetricResult,
    SimulationResultFolder,
    VariantMetricsResult,
    VariantResultMapping,
)

__all__ = [
    "RoomMetricResult",
    "SimulationResultFolder",
    "VariantMetricsResult",
    "VariantResultMapping",
    "collect_simulation_metrics",
    "discover_result_folders",
    "export_simulation_metrics_to_json",
    "map_result_folders_to_variants",
    "read_room_metrics",
    "read_variant_metrics",
    "resolve_result_folder",
]
