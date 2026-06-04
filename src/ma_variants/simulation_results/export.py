"""JSON-Export fuer eingelesene Simulationskennwerte."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import VariantMetricsResult


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json_default(value: Any) -> str:
    if isinstance(value, Path):
        return value.as_posix()
    raise TypeError(f"Nicht JSON-serialisierbarer Wert: {value!r}")


def export_simulation_metrics_to_json(
    metric_results: list[VariantMetricsResult],
    output_path: str | Path = Path("data/exports/simulation_metrics.json"),
    exported_at: str | None = None,
) -> Path:
    """Schreibt eingelesene Simulationskennwerte als JSON."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "exported_at": exported_at or _utc_timestamp(),
        "variant_count": len(metric_results),
        "variants": [asdict(metric_result) for metric_result in metric_results],
    }
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=_json_default),
        encoding="utf-8",
    )
    return path
