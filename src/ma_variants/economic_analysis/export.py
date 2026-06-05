"""Datei-Exporte fuer generische Wirtschaftlichkeitsergebnisse."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .models import VariantCostResult

DEFAULT_JSON_EXPORT_PATH = Path("data/ma_variants/exports/variant_cost_results.json")
DEFAULT_CSV_EXPORT_PATH = Path("data/ma_variants/exports/variant_cost_results.csv")


def _timestamp(exported_at: str | None) -> str:
    return exported_at or datetime.now(timezone.utc).isoformat()


def export_variant_cost_results_json(
    results: list[VariantCostResult],
    output_path: str | Path = DEFAULT_JSON_EXPORT_PATH,
    exported_at: str | None = None,
) -> Path:
    """Exportiert Wirtschaftlichkeitsergebnisse als JSON."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "exported_at": _timestamp(exported_at),
        "result_count": len(results),
        "results": [asdict(result) for result in results],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def export_variant_cost_results_csv(
    results: list[VariantCostResult],
    output_path: str | Path = DEFAULT_CSV_EXPORT_PATH,
) -> Path:
    """Exportiert Wirtschaftlichkeitsergebnisse als CSV."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "variant_key",
        "variant_name",
        "scenario_key",
        "selected_system_types",
        "investment_cost_eur",
        "maintenance_cost_eur_per_year",
        "maintenance_cost_total_eur",
        "energy_cost_eur_per_year",
        "energy_cost_total_eur",
        "replacement_cost_eur",
        "total_cost_eur",
        "observation_period_years",
        "heating_energy_kwh_per_year",
        "cooling_energy_kwh_per_year",
        "uses_simulation_results",
        "uses_example_energy_values",
        "assumption_notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            row = asdict(result)
            row["selected_system_types"] = ";".join(result.selected_system_types)
            row["assumption_notes"] = ";".join(result.assumption_notes)
            writer.writerow(row)
    return path
