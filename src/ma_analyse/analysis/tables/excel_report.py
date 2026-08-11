"""Berechnung und Ausgabe nachvollziehbarer Analyse-Tabellen."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from math import isfinite
from pathlib import Path

import pandas as pd

from .schema import (
    LEGACY_COLUMN_RENAME,
    LEGACY_OUTPUT_COLUMNS,
    METRIC_DEFINITIONS,
    PLOT_SUBDIR_EXCEL,
    POWER_DISPLAY_MODES,
    POWER_METRIC_KEYS,
    POWER_SOURCE_UNITS,
    V2_COLUMN_RENAME,
    output_columns,
)


@dataclass(frozen=True)
class AnalysisTableBundle:
    """Gemeinsamer Tabellenvertrag für Service, UI und Excel."""

    summary: pd.DataFrame
    legacy_summary: pd.DataFrame
    data_inventory: pd.DataFrame
    calculation_boundaries: pd.DataFrame
    verification_readiness: pd.DataFrame = field(default_factory=pd.DataFrame)

    def detail_tables(self) -> dict[str, pd.DataFrame]:
        return {
            "Dateninventar": self.data_inventory,
            "Berechnungsgrenzen": self.calculation_boundaries,
            "Nachweisbereitschaft": self.verification_readiness,
        }


def summarize_room_metrics(
    df,
    variant_name,
    room_name,
    *,
    reference_area_m2: float | None = None,
    power_display_mode: str = "both",
    power_source_unit: str = "unverified",
):
    """Berechnet neutrale Kennwerte für einen Raum."""

    if df is None or df.empty:
        return None
    _validate_power_display_mode(power_display_mode)
    _validate_power_source_unit(power_source_unit)

    area_m2 = _valid_reference_area(reference_area_m2)
    source_unit_label = _power_source_unit_label(power_source_unit)
    power_coverage_status = _power_coverage_status(df)
    specific_status = _derived_power_status(
        power_coverage_status,
        source_unit=power_source_unit,
        area_m2=area_m2,
        target="specific",
    )
    row = {
        "variant": variant_name,
        "room": room_name,
        "evaluation_hours": _evaluation_hours(df),
        "reference_area_m2": area_m2,
        "specific_power_status": specific_status,
        "power_source_unit_label": source_unit_label,
        "power_unit_status": "nicht bestätigt" if power_source_unit == "unverified" else "für Lauf angegeben",
    }

    for metric_name, (column_name, agg_func) in METRIC_DEFINITIONS.items():
        value = _aggregate_metric(df, column_name, agg_func)
        if metric_name in POWER_METRIC_KEYS:
            row[f"raw_{metric_name}"] = value
            absolute_value, specific_value = _derive_power_values(
                value,
                source_unit=power_source_unit,
                area_m2=area_m2,
            )
            row[metric_name] = absolute_value
            row[f"{metric_name}_per_m2"] = specific_value
        else:
            row[metric_name] = value

    return row


def build_data_inventory_row(
    df: pd.DataFrame,
    *,
    variant_name: str,
    room_name: str,
    source_file: str | Path,
    reference_area_m2: float | None,
    power_source_unit: str,
) -> dict[str, object]:
    """Beschreibt die tatsächlich geladene Raumtabelle ohne Fachannahmen."""

    required_columns = {column_name for column_name, _aggregation in METRIC_DEFINITIONS.values()}
    available = sorted(required_columns.intersection(df.columns))
    missing = sorted(required_columns.difference(df.columns))
    power_columns = {METRIC_DEFINITIONS[key][0] for key in POWER_METRIC_KEYS}
    available_power_columns = [
        column_name
        for column_name in sorted(power_columns.intersection(df.columns))
        if not pd.to_numeric(df[column_name], errors="coerce").dropna().empty
    ]
    power_status = _coverage_status(len(available_power_columns), len(power_columns))
    area_m2 = _valid_reference_area(reference_area_m2)
    absolute_status = _derived_power_status(
        power_status,
        source_unit=power_source_unit,
        area_m2=area_m2,
        target="absolute",
    )
    specific_status = _derived_power_status(
        power_status,
        source_unit=power_source_unit,
        area_m2=area_m2,
        target="specific",
    )
    return {
        "Variante": variant_name,
        "Raum": room_name,
        "Quelldatei": Path(source_file).name,
        "Datensätze": len(df),
        "Auswertungsstunden [h]": _evaluation_hours(df),
        "Spalten": len(df.columns),
        "Fehlwerte": int(df.isna().sum().sum()),
        "Verfügbare Kennwertspalten": ", ".join(available) or "keine",
        "Fehlende Kennwertspalten": ", ".join(missing) or "keine",
        "Bezugsfläche [m²]": area_m2,
        "Flächenstatus": "auswertbar" if area_m2 is not None else "nicht auswertbar",
        "Flächenherkunft": "Laufparameter; automatische/manuelle Herkunft noch nicht differenziert",
        "Rohleistungsstatus": power_status,
        "Quelleneinheit Leistung": _power_source_unit_label(power_source_unit),
        "Einheitenstatus": "nicht bestätigt" if power_source_unit == "unverified" else "für Lauf angegeben",
        "Einheitenbasis": "manuelle Laufangabe; kein versionierter Importvertrag",
        "Absolutstatus": absolute_status,
        "Spezifischstatus": specific_status,
        "Kennwertstatus Leistung": _power_metric_status_text(df, power_source_unit),
    }


def build_calculation_boundary_rows(
    inventory_rows: list[dict[str, object]],
    *,
    power_display_mode: str,
) -> list[dict[str, str]]:
    """Macht bekannte Berechnungsgrenzen als Ergebnisbestandteil sichtbar."""

    specific_requested = power_display_mode in {"specific", "both"}
    total_count = len(inventory_rows)
    missing_area_count = sum(row.get("Flächenstatus") != "auswertbar" for row in inventory_rows)
    absolute_status = _combine_statuses([str(row.get("Absolutstatus")) for row in inventory_rows])
    specific_status = _combine_statuses([str(row.get("Spezifischstatus")) for row in inventory_rows])
    time_status = _combine_statuses(
        [
            "auswertbar" if row.get("Auswertungsstunden [h]") is not None else "nicht auswertbar"
            for row in inventory_rows
        ]
    )
    area_reason = (
        "Quelleneinheit, Leistungsreihen und die für die Ableitung nötige Bezugsbasis sind angegeben."
        if specific_status == "auswertbar"
        else f"Für {missing_area_count} von {total_count} Raum-/Variantenkombinationen fehlt eine belastbare Bezugsfläche; zusätzlich gelten Einheiten- und Datenstatus aus dem Inventar."
    )

    return [
        {
            "Prüfpunkt": "Absolute Leistung",
            "Status": absolute_status,
            "Regel": "W wird nur aus vorhandenen numerischen Reihen und einer für den Lauf angegebenen Quelleneinheit abgeleitet.",
        },
        {
            "Prüfpunkt": "Spezifische Leistung",
            "Status": specific_status if specific_requested else "nicht angefordert",
            "Regel": area_reason,
        },
        {
            "Prüfpunkt": "Auswertungsstunden",
            "Status": time_status,
            "Regel": "Stunden werden aus der stündlich aufbereiteten time-Achse bestimmt.",
        },
        {
            "Prüfpunkt": "Nutzungsstunden",
            "Status": "nicht auswertbar",
            "Regel": "Eine Zeilenanzahl ist kein Belegungsprofil; Nutzungsstunden benötigen ein freigegebenes Profil.",
        },
        {
            "Prüfpunkt": "Übertemperatur-Gradstunden nach Regelwerk",
            "Status": "nicht auswertbar",
            "Regel": "Methode, Ausgabe, Kriterien und fachlicher Referenztest sind noch nicht freigegeben.",
        },
    ]


def prepare_result_dataframe(rows, power_display_mode: str = "both"):
    """Bringt Ergebniszeilen in die gewählte, einheitlich beschriftete Form."""

    _validate_power_display_mode(power_display_mode)
    include_absolute_fallback = power_display_mode == "specific" and any(
        row.get("specific_power_status") == "nicht auswertbar: Bezugsfläche fehlt" for row in rows
    )
    if not rows:
        return pd.DataFrame(columns=output_columns(power_display_mode))
    result_df = pd.DataFrame(rows).sort_values(["variant", "room"])
    result_df = result_df.rename(columns=V2_COLUMN_RENAME)
    return result_df.reindex(
        columns=output_columns(power_display_mode, include_absolute_fallback=include_absolute_fallback)
    )


def prepare_legacy_result_dataframe(rows):
    """Erzeugt das historische ``metrics``-Schema ohne unbelegte Ersatzwerte."""

    if not rows:
        return pd.DataFrame(columns=LEGACY_OUTPUT_COLUMNS)
    result_df = pd.DataFrame(rows).sort_values(["variant", "room"])
    result_df = result_df.rename(columns=LEGACY_COLUMN_RENAME)
    return result_df.reindex(columns=LEGACY_OUTPUT_COLUMNS)


def write_excel_report(
    result_df,
    output_dir,
    filename,
    *,
    legacy_result_df: pd.DataFrame | None = None,
    detail_tables: dict[str, pd.DataFrame] | None = None,
):
    """Schreibt Kennwerte und vorhandene Prüftabellen in eine Arbeitsmappe."""

    output_excel_dir = os.path.join(output_dir, PLOT_SUBDIR_EXCEL)
    os.makedirs(output_excel_dir, exist_ok=True)

    output_file = os.path.join(output_excel_dir, filename)
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        (legacy_result_df if legacy_result_df is not None else result_df).to_excel(
            writer,
            sheet_name="metrics",
            index=False,
        )
        result_df.to_excel(writer, sheet_name="metrics_v2", index=False)
        for table_name, table in (detail_tables or {}).items():
            table.to_excel(writer, sheet_name=_excel_sheet_name(table_name), index=False)
    return output_file


def _aggregate_metric(df: pd.DataFrame, column_name: str, agg_func: str):
    if column_name not in df.columns:
        return None
    series = pd.to_numeric(df[column_name], errors="coerce").dropna()
    if series.empty:
        return None
    aggregations = {
        "max": series.max,
        "min": series.min,
        "mean": series.mean,
        "median": series.median,
        "abs_max": lambda: series.abs().max(),
    }
    aggregation = aggregations.get(agg_func)
    return aggregation() if aggregation is not None else None


def _valid_reference_area(value: object) -> float | None:
    try:
        area_m2 = float(value)
    except TypeError, ValueError:
        return None
    return area_m2 if isfinite(area_m2) and area_m2 > 0 else None


def _coverage_status(available_count: int, total_count: int) -> str:
    if available_count <= 0 or total_count <= 0:
        return "nicht auswertbar"
    if available_count < total_count:
        return "teilweise auswertbar"
    return "auswertbar"


def _power_coverage_status(df: pd.DataFrame) -> str:
    power_columns = {METRIC_DEFINITIONS[key][0] for key in POWER_METRIC_KEYS}
    available_count = sum(
        column_name in df.columns and not pd.to_numeric(df[column_name], errors="coerce").dropna().empty
        for column_name in power_columns
    )
    return _coverage_status(available_count, len(power_columns))


def _derive_power_values(
    value: float | None,
    *,
    source_unit: str,
    area_m2: float | None,
) -> tuple[float | None, float | None]:
    if value is None or source_unit == "unverified":
        return None, None
    if source_unit == "w":
        return value, value / area_m2 if area_m2 is not None else None
    return (value * area_m2 if area_m2 is not None else None), value


def _derived_power_status(
    coverage_status: str,
    *,
    source_unit: str,
    area_m2: float | None,
    target: str,
) -> str:
    if source_unit == "unverified":
        return "nicht auswertbar: Quelleneinheit nicht bestätigt"
    area_required = (source_unit == "w" and target == "specific") or (
        source_unit == "w_per_m2" and target == "absolute"
    )
    if area_required and area_m2 is None:
        return "nicht auswertbar: Bezugsfläche fehlt"
    return coverage_status


def _power_source_unit_label(source_unit: str) -> str:
    return {"unverified": "nicht bestätigt", "w": "W", "w_per_m2": "W/m²"}[source_unit]


def _power_metric_status_text(df: pd.DataFrame, source_unit: str) -> str:
    unit_status = "Einheit nicht bestätigt" if source_unit == "unverified" else "Quelleneinheit angegeben"
    statuses = []
    for metric_key in POWER_METRIC_KEYS:
        column_name = METRIC_DEFINITIONS[metric_key][0]
        available = column_name in df.columns and not pd.to_numeric(df[column_name], errors="coerce").dropna().empty
        statuses.append(f"{metric_key}={'vorhanden' if available else 'fehlt'}")
    return f"{unit_status}; " + ", ".join(sorted(statuses))


def _combine_statuses(statuses: list[str]) -> str:
    normalized = [
        "nicht auswertbar"
        if status.startswith("nicht auswertbar")
        else "teilweise auswertbar"
        if status.startswith("teilweise auswertbar")
        else status
        for status in statuses
    ]
    if not normalized or all(status == "nicht auswertbar" for status in normalized):
        return "nicht auswertbar"
    if all(status == "auswertbar" for status in normalized):
        return "auswertbar"
    return "teilweise auswertbar"


def _evaluation_hours(df: pd.DataFrame) -> int | None:
    """Bestimmt Stunden nur für die belegte stündliche prepared-time-Achse."""

    if "time" not in df.columns:
        return None
    time_values = pd.to_numeric(df["time"], errors="coerce").dropna().drop_duplicates().sort_values()
    if time_values.empty:
        return None
    if len(time_values) == 1:
        return 1
    differences = time_values.diff().dropna()
    if not differences.eq(1).all():
        return None
    return int(len(time_values))


def _validate_power_display_mode(power_display_mode: str) -> None:
    if power_display_mode not in POWER_DISPLAY_MODES:
        raise ValueError("power_display_mode muss absolute, specific oder both sein.")


def _validate_power_source_unit(power_source_unit: str) -> None:
    if power_source_unit not in POWER_SOURCE_UNITS:
        raise ValueError("power_source_unit muss unverified, w oder w_per_m2 sein.")


def _excel_sheet_name(table_name: str) -> str:
    names = {
        "Dateninventar": "data_inventory",
        "Berechnungsgrenzen": "calculation_limits",
        "Nachweisbereitschaft": "verification_readiness",
    }
    return names.get(table_name, table_name[:31])
