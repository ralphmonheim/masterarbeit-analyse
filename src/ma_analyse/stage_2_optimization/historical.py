"""Deskriptiver Vergleich der vorhandenen historischen Optimierungsvarianten."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ma_data_preparation.ida_ice import discover_known_ida_prn, read_prn_as_standardized_series
from ma_data_preparation.services import integrate_time_weighted

BASELINE_VARIANT = "Dimensionierung"


def build_historical_optimization_table(input_root: str | Path) -> pd.DataFrame:
    """Verdichtet ALT-Zeitreihen je Variante und Zone ohne Optimierungsurteil."""

    grouped: dict[tuple[str, str], dict[str, object]] = {}
    for selection in discover_known_ida_prn(input_root):
        if selection.cohort != "ALT" or not selection.zone_id:
            continue
        artifact_kind = selection.path.stem.rsplit(".", 1)[-1].upper()
        if artifact_kind not in {"IAQ", "TEMPERATURES", "ZONE-ENERGY"}:
            continue
        key = (selection.variant_id, selection.zone_id)
        entry = grouped.setdefault(key, {"sources": []})
        entry["sources"].append(str(selection.path))
        for series in read_prn_as_standardized_series(selection):
            _accumulate_summary(entry, series)

    rows = [_summarize_variant_zone(variant, zone, data) for (variant, zone), data in grouped.items()]
    table = pd.DataFrame(rows)
    if table.empty:
        return table
    table = table.sort_values(["Zone", "Variante"], kind="stable").reset_index(drop=True)
    baselines = table[table["Variante"] == BASELINE_VARIANT].set_index("Zone")
    for metric in ("Heizenergie [kWh]", "Max. Heizleistung [W]", "Max. operative Temperatur [°C]"):
        table[f"Delta zu Basis: {metric}"] = [
            _delta(value, baselines, zone, metric)
            for value, zone in zip(table[metric], table["Zone"], strict=True)
        ]
    return table


def export_historical_optimization_table(input_root: str | Path, output_root: str | Path) -> tuple[Path, Path]:
    """Exportiert den ALT-Vergleich als editierbare XLSX- und CSV-Tabelle."""

    table = build_historical_optimization_table(input_root)
    output = Path(output_root)
    output.mkdir(parents=True, exist_ok=True)
    excel_path = output / "Optimierungsvergleich_ALT.xlsx"
    csv_path = output / "Optimierungsvergleich_ALT.csv"
    table.to_excel(excel_path, sheet_name="Variantenvergleich", index=False)
    table.to_csv(csv_path, index=False, encoding="utf-8-sig")
    return excel_path, csv_path


def _summarize_variant_zone(variant: str, zone: str, data: dict[str, object]) -> dict[str, object]:
    return {
        "Variante": variant,
        "Zone": zone,
        "Heizenergie [kWh]": data.get("heating_energy_kwh"),
        "Kühlenergie [kWh]": data.get("cooling_energy_kwh"),
        "Max. Heizleistung [W]": data.get("max_heating_w"),
        "Max. Kühlleistung [W]": data.get("max_cooling_w"),
        "Min. operative Temperatur [°C]": data.get("min_top_c"),
        "Max. operative Temperatur [°C]": data.get("max_top_c"),
        "Max. CO₂ [ppm]": data.get("max_co2_ppm"),
        "PRN-Dateien": len(data["sources"]),
        "Auswertungsstatus": "PARTIAL",
        "Berechnungsgrundlage": "PRN-Ableitung vorlaeufig; IDA-Zeit-/Leistungssemantik offen",
        "Quellenreferenz": "; ".join(data["sources"]),
    }


def _accumulate_summary(entry: dict[str, object], series) -> None:
    """Verdichtet eine Quelldatei sofort und haelt keine Jahresreihen im RAM."""

    if series.metric == "zone_energy.q_heat":
        entry["heating_energy_kwh"] = _safe_integral_kwh(series)
        entry["max_heating_w"] = _maximum(series)
    elif series.metric == "zone_energy.q_cool":
        energy = _safe_integral_kwh(series)
        entry["cooling_energy_kwh"] = abs(energy) if energy is not None else None
        entry["max_cooling_w"] = _maximum_absolute(series)
    elif series.metric == "temperatures.top":
        entry["min_top_c"] = _minimum(series)
        entry["max_top_c"] = _maximum(series)
    elif series.metric == "iaq.xco2vol":
        entry["max_co2_ppm"] = _maximum(series)


def _safe_integral_kwh(series) -> float | None:
    try:
        return integrate_time_weighted(series) / 1000
    except ValueError:
        return None


def _minimum(series) -> float | None:
    return min((record.value for record in series.records), default=None) if series else None


def _maximum(series) -> float | None:
    return max((record.value for record in series.records), default=None) if series else None


def _maximum_absolute(series) -> float | None:
    return max((abs(record.value) for record in series.records), default=None) if series else None


def _delta(value: object, baselines: pd.DataFrame, zone: str, metric: str) -> float | None:
    if not isinstance(value, int | float) or zone not in baselines.index:
        return None
    baseline = baselines.at[zone, metric]
    return float(value - baseline) if isinstance(baseline, int | float) else None
