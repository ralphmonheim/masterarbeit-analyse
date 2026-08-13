"""Aufbau der einheitlichen Zonenkennwerttabelle aus freigegebenen IDA-Daten."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from ma_data_preparation.ida_ice import discover_known_ida_prn, read_prn_as_standardized_series
from ma_data_preparation.services import integrate_time_weighted
from ma_data_preparation.zone_metadata import ZoneMetadata, read_zone_metadata
from ma_import_simulation.adapters.ida_ice import extract_zone_report_rows

from .tables.master_thesis import ZoneMetricRecord, build_zone_metrics_table

MODEL_WORKBOOKS = {
    "5Z": "Dimensionierung_5Z_Eingabe_Allgemein.xlsx",
    "29Z": "Dimensionierung_29Z_Eingabe_Allgemein.xlsx",
}


@dataclass(frozen=True, slots=True)
class ModelTableResult:
    cohort: str
    zone_table: pd.DataFrame
    inventory_table: pd.DataFrame
    excel_path: Path | None = None
    csv_path: Path | None = None


def build_model_zone_tables(input_root: str | Path, cohort: str) -> ModelTableResult:
    """Berechnet datenkompatible Zonenwerte fuer 5Z oder 29Z."""

    if cohort not in MODEL_WORKBOOKS:
        raise ValueError("cohort muss 5Z oder 29Z sein.")
    root = Path(input_root)
    metadata_path = root / MODEL_WORKBOOKS[cohort]
    zones = read_zone_metadata(metadata_path)
    selections = tuple(
        selection
        for selection in discover_known_ida_prn(root)
        if selection.cohort == cohort and selection.result_kind == "energy" and selection.zone_id
    )
    by_zone: dict[str, list] = {}
    for selection in selections:
        by_zone.setdefault(_zone_key(selection.zone_id), []).append(selection)

    report_rows = _report_values(root, cohort)
    records: list[ZoneMetricRecord] = []
    inventory: list[dict[str, object]] = []
    for zone in zones:
        zone_key = _zone_key(zone.zone)
        values, sources, metric_count = _zone_values(
            zone, by_zone.get(zone_key, []), report_rows.get(zone_key, {})
        )
        records.append(ZoneMetricRecord(zone.zone, zone.group, values))
        inventory.append(
            {
                "Modell": cohort,
                "Zone": zone.zone,
                "PRN-Dateien": len(by_zone.get(zone_key, [])),
                "Ermittelte Kennwerte": metric_count,
                "Status": values["evaluation_status"],
                "Quellen": "; ".join(sources),
            }
        )
    return ModelTableResult(cohort, build_zone_metrics_table(records), pd.DataFrame(inventory))


def export_model_zone_tables(
    input_root: str | Path, output_root: str | Path, cohort: str
) -> ModelTableResult:
    """Schreibt die Zonenkennwerte als XLSX und CSV fuer die Masterarbeit."""

    result = build_model_zone_tables(input_root, cohort)
    output = Path(output_root)
    output.mkdir(parents=True, exist_ok=True)
    excel_path = output / f"Zonenkennwerte_{cohort}.xlsx"
    csv_path = output / f"Zonenkennwerte_{cohort}.csv"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        result.zone_table.to_excel(writer, sheet_name="Zonenkennwerte", index=False)
        result.inventory_table.to_excel(writer, sheet_name="Dateninventar", index=False)
    result.zone_table.to_csv(csv_path, index=False, encoding="utf-8-sig")
    return ModelTableResult(cohort, result.zone_table, result.inventory_table, excel_path, csv_path)


def _zone_values(
    zone: ZoneMetadata, selections: list, report: dict[str, object]
) -> tuple[dict[str, object], list[str], int]:
    series_by_metric = {}
    sources: list[str] = []
    for selection in selections:
        sources.append(str(selection.path))
        for series in read_prn_as_standardized_series(selection):
            series_by_metric[series.metric] = series
    report_sources = report.get("_source_references", [])
    if isinstance(report_sources, list):
        sources.extend(str(source) for source in report_sources)

    values: dict[str, object] = {
        "zone_multiplier": zone.multiplier,
        "area_m2": zone.area_m2,
        "max_supply_airflow_l_s_m2": zone.max_supply_airflow_l_s_m2,
        "max_exhaust_airflow_l_s_m2": zone.max_exhaust_airflow_l_s_m2,
    }
    _add_extreme(values, series_by_metric, "temperatures.tairmean", "min_air_temperature_c", min)
    _add_extreme(values, series_by_metric, "temperatures.tairmean", "max_air_temperature_c", max)
    _add_extreme(values, series_by_metric, "temperatures.top", "min_operative_temperature_c", min)
    _add_extreme(values, series_by_metric, "temperatures.top", "max_operative_temperature_c", max)
    _add_extreme(values, series_by_metric, "iaq.relhum", "min_relative_humidity_pct", min)
    _add_extreme(values, series_by_metric, "iaq.relhum", "max_relative_humidity_pct", max)
    _add_extreme(values, series_by_metric, "iaq.xco2vol", "max_co2_ppm", max)
    _add_extreme(values, series_by_metric, "iaq.air_age", "max_air_age_h", max)

    area = zone.area_m2 if zone.area_m2 and zone.area_m2 > 0 else None
    heating = series_by_metric.get("zone_energy.q_heat")
    cooling = series_by_metric.get("zone_energy.q_cool")
    if heating is not None:
        energy = _safe_integral_kwh(heating)
        values["heating_energy_kwh"] = energy
        values["heating_energy_kwh_m2"] = energy / area if energy is not None and area else None
        values["max_heat_supplied_w"] = max(record.value for record in heating.records)
        values["max_heat_supplied_w_m2"] = values["max_heat_supplied_w"] / area if area else None
    if cooling is not None:
        signed_energy = _safe_integral_kwh(cooling)
        energy = abs(signed_energy) if signed_energy is not None else None
        values["cooling_energy_kwh"] = energy
        values["cooling_energy_kwh_m2"] = energy / area if energy is not None and area else None
        values["max_heat_removed_w"] = max(abs(record.value) for record in cooling.records)
        values["max_heat_removed_w_m2"] = values["max_heat_removed_w"] / area if area else None

    _merge_report_values(values, report, area)
    populated = sum(value is not None for value in values.values())
    expected_artifacts = {"heat_balance", "iaq", "local_de_comf_diag_t", "temperatures", "zone_energy"}
    present_artifacts = {selection.path.stem.rsplit(".", 1)[-1].lower().replace("-", "_") for selection in selections}
    values["data_coverage_pct"] = round(100.0 * len(expected_artifacts & present_artifacts) / len(expected_artifacts), 1)
    # Die IDA-PRN-Zeit- und Leistungssemantik ist noch nicht unabhaengig
    # bestaetigt. Quantitative Ableitungen bleiben deshalb vorlaeufig.
    values["evaluation_status"] = "PARTIAL"
    values["calculation_basis"] = "PRN-Ableitung vorlaeufig; IDA-Zeit-/Leistungssemantik offen"
    values["source_reference"] = "; ".join(dict.fromkeys(sources))
    return values, list(dict.fromkeys(sources)), populated


def _add_extreme(values: dict[str, object], series_by_metric: dict, metric: str, key: str, operation) -> None:
    series = series_by_metric.get(metric)
    if series is not None and series.records:
        values[key] = operation(record.value for record in series.records)


def _safe_integral_kwh(series) -> float | None:
    try:
        return integrate_time_weighted(series) / 1000.0
    except ValueError:
        return None


def _merge_report_values(values: dict[str, object], report: dict[str, object], area: float | None) -> None:
    mappings = {
        "lokale_heizung_w": ("local_heating_w", "local_heating_w_m2"),
        "lokale_kuhlung_w": ("local_cooling_w", "local_cooling_w_m2"),
        "vent_kuhlung_w": ("ventilation_cooling_w", "ventilation_cooling_w_m2"),
        "warmeabgabe_w": ("max_heat_supplied_w", "max_heat_supplied_w_m2"),
        "entzogene_warme_w": ("max_heat_removed_w", "max_heat_removed_w_m2"),
    }
    for source, (absolute_target, specific_target) in mappings.items():
        raw = report.get(source)
        if isinstance(raw, int | float):
            values[absolute_target] = float(raw)
            values[specific_target] = float(raw) / area if area else None


def _report_values(root: Path, cohort: str) -> dict[str, dict[str, object]]:
    if cohort != "5Z":
        return {}
    report_root = root / "Masterthesis_Dimensionierung_5Z" / "Berichte"
    combined: dict[str, dict[str, object]] = {}
    for name in ("heating", "cooling", "summer_peak"):
        path = report_root / f"Masterthesis_Dimensionierung_5Z_{name}.html"
        if not path.is_file():
            continue
        for row in extract_zone_report_rows(path):
            zone = row.get("zone")
            if isinstance(zone, str):
                target = combined.setdefault(_zone_key(zone), {"_source_references": []})
                target.update(row)
                target["_source_references"].append(str(path))
    return combined


def _zone_key(value: object) -> str:
    """Normalisiert Zonennamen ohne die Bezeichnung in Ausgaben zu veraendern."""

    return str(value).strip().casefold()
