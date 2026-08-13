"""Einheitlicher Tabellenvertrag fuer die fachliche Masterarbeitsauswertung."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

import pandas as pd


@dataclass(frozen=True)
class ThesisColumn:
    key: str
    label: str
    unit: str | None = None

    @property
    def output_name(self) -> str:
        return f"{self.label} [{self.unit}]" if self.unit else self.label


ZONE_COLUMNS = (
    ThesisColumn("zone", "Zone"),
    ThesisColumn("group", "Gruppe"),
    ThesisColumn("zone_multiplier", "Zonenmultiplikator"),
    ThesisColumn("area_m2", "Netto-Raumfläche", "m²"),
    ThesisColumn("min_air_temperature_c", "Min. Lufttemperatur", "°C"),
    ThesisColumn("max_air_temperature_c", "Max. Lufttemperatur", "°C"),
    ThesisColumn("min_operative_temperature_c", "Min. operative Temperatur", "°C"),
    ThesisColumn("max_operative_temperature_c", "Max. operative Temperatur", "°C"),
    ThesisColumn("heating_energy_kwh", "Raumheizung", "kWh"),
    ThesisColumn("heating_energy_kwh_m2", "Raumheizung spezifisch", "kWh/m²"),
    ThesisColumn("max_heat_supplied_w", "Max. Wärmeabgabe absolut", "W"),
    ThesisColumn("max_heat_supplied_w_m2", "Max. Wärmeabgabe", "W/m²"),
    ThesisColumn("local_heating_w", "Lokale Heizung absolut", "W"),
    ThesisColumn("local_heating_w_m2", "Lokale Heizung", "W/m²"),
    ThesisColumn("max_heat_removed_w_m2", "Max. Wärmeentzug", "W/m²"),
    ThesisColumn("cooling_energy_kwh", "Raumkühlung", "kWh"),
    ThesisColumn("cooling_energy_kwh_m2", "Raumkühlung spezifisch", "kWh/m²"),
    ThesisColumn("max_heat_removed_w", "Max. Wärmeentzug absolut", "W"),
    ThesisColumn("local_cooling_w_m2", "Lokale Kühlung", "W/m²"),
    ThesisColumn("local_cooling_w", "Lokale Kühlung absolut", "W"),
    ThesisColumn("ventilation_cooling_w_m2", "Lüftungskühlung", "W/m²"),
    ThesisColumn("ventilation_cooling_w", "Lüftungskühlung absolut", "W"),
    ThesisColumn("max_supply_airflow_l_s_m2", "Max. Zuluftvolumenstrom", "L/(s·m²)"),
    ThesisColumn("max_exhaust_airflow_l_s_m2", "Max. Abluftvolumenstrom", "L/(s·m²)"),
    ThesisColumn("max_solar_gain_w_m2", "Max. solarer Eintrag", "W/m²"),
    ThesisColumn("min_relative_humidity_pct", "Min. relative Feuchte", "%"),
    ThesisColumn("max_relative_humidity_pct", "Max. relative Feuchte", "%"),
    ThesisColumn("max_co2_ppm", "Max. CO₂", "ppm"),
    ThesisColumn("max_ppd_pct", "Max. PPD", "%"),
    ThesisColumn("max_air_age_h", "Max. Luftalter", "h"),
    ThesisColumn("in_use_hours_h", "Nutzungsstunden", "h"),
    ThesisColumn("operative_temperature_above_25_h", "Nutzungsstunden T_op > 25 °C", "h"),
    ThesisColumn("operative_temperature_above_27_h", "Nutzungsstunden T_op > 27 °C", "h"),
    ThesisColumn("person_hours_h", "Personenstunden", "Pers·h"),
    ThesisColumn("ppd_weighted_person_hours_h", "PPD-gewichtete Personenstunden", "Pers·h"),
    ThesisColumn("unmet_cooling_hours_h", "Unerfüllte Stunden Kühlung", "h"),
    ThesisColumn("unmet_heating_hours_h", "Unerfüllte Stunden Heizung", "h"),
    ThesisColumn("overtemperature_degree_hours_kh", "Übertemperaturgradstunden", "Kh"),
    ThesisColumn("data_coverage_pct", "Datenabdeckung", "%"),
    ThesisColumn("evaluation_status", "Auswertungsstatus"),
    ThesisColumn("calculation_basis", "Berechnungsgrundlage"),
    ThesisColumn("source_reference", "Quellenreferenz"),
)


@dataclass(frozen=True)
class ZoneMetricRecord:
    """Wertemenge einer Zone; fehlende Kennwerte bleiben bewusst leer."""

    zone: str
    group: str
    values: Mapping[str, Any] = field(default_factory=dict)


def build_zone_metrics_table(records: list[ZoneMetricRecord]) -> pd.DataFrame:
    """Erzeugt eine stabile Tabelle mit allen vereinbarten Spalten."""

    rows: list[dict[str, Any]] = []
    for record in records:
        source = {"zone": record.zone, "group": record.group, **dict(record.values)}
        rows.append({column.output_name: source.get(column.key) for column in ZONE_COLUMNS})
    return pd.DataFrame(rows, columns=[column.output_name for column in ZONE_COLUMNS])


def zone_metric_keys() -> tuple[str, ...]:
    return tuple(column.key for column in ZONE_COLUMNS)
