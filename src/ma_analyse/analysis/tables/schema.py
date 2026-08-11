"""Schema und Kennwertdefinitionen für Excel- und UI-Auswertungen."""

from __future__ import annotations

PLOT_SUBDIR_EXCEL = "excel"

POWER_DISPLAY_MODES = {"absolute", "specific", "both"}
POWER_SOURCE_UNITS = {"unverified", "w", "w_per_m2"}

METRIC_DEFINITIONS = {
    "max_q_heat": ("zone_energy_q_heat", "max"),
    "min_q_heat": ("zone_energy_q_heat", "min"),
    "max_q_cool": ("zone_energy_q_cool", "max"),
    "min_q_cool": ("zone_energy_q_cool", "min"),
    "peak_abs_q_cool": ("zone_energy_q_cool", "abs_max"),
    "max_q_occ": ("zone_energy_q_occ", "max"),
    "max_q_loss": ("zone_energy_q_loss", "max"),
    "max_q_equip": ("zone_energy_q_equip", "max"),
    "max_co2": ("iaq_xco2vol", "max"),
    "mean_co2": ("iaq_xco2vol", "mean"),
    "max_tair": ("temperatures_tairmean", "max"),
    "min_tair": ("temperatures_tairmean", "min"),
    "max_top": ("temperatures_top", "max"),
    "min_top": ("temperatures_top", "min"),
    "mean_top": ("temperatures_top", "mean"),
    "max_relhum": ("iaq_relhum", "max"),
    "min_relhum": ("iaq_relhum", "min"),
    "mean_relhum": ("iaq_relhum", "mean"),
    "max_air_age": ("iaq_air_age", "max"),
}

POWER_METRIC_KEYS = {
    "max_q_heat",
    "min_q_heat",
    "max_q_cool",
    "min_q_cool",
    "peak_abs_q_cool",
    "max_q_occ",
    "max_q_loss",
    "max_q_equip",
}

METRIC_LABELS = {
    "max_q_heat": "Max. Heizleistung",
    "min_q_heat": "Min. Heizleistung",
    "max_q_cool": "Algebraisches Maximum Raumkühlwert",
    "min_q_cool": "Algebraisches Minimum Raumkühlwert",
    "peak_abs_q_cool": "Max. Betrag Raumkühlwert",
    "max_q_occ": "Max. Personenlast",
    "max_q_loss": "Max. Wärmeverlust",
    "max_q_equip": "Max. Gerätelast",
    "max_co2": "Max. CO₂-Konzentration",
    "mean_co2": "Mittlere CO₂-Konzentration",
    "max_tair": "Max. Raumlufttemperatur",
    "min_tair": "Min. Raumlufttemperatur",
    "max_top": "Max. operative Temperatur",
    "min_top": "Min. operative Temperatur",
    "mean_top": "Mittlere operative Temperatur",
    "max_relhum": "Max. relative Feuchte",
    "min_relhum": "Min. relative Feuchte",
    "mean_relhum": "Mittlere relative Feuchte",
    "max_air_age": "Max. Luftalter",
}

METRIC_UNITS = {
    "max_co2": "ppm",
    "mean_co2": "ppm",
    "max_tair": "°C",
    "min_tair": "°C",
    "max_top": "°C",
    "min_top": "°C",
    "mean_top": "°C",
    "max_relhum": "%",
    "min_relhum": "%",
    "mean_relhum": "%",
    "max_air_age": "h",
}

BASE_OUTPUT_COLUMNS = [
    "Variante",
    "Raum",
    "Auswertungsstunden [h]",
    "Bezugsfläche [m²]",
    "Spezifische Leistung",
    "Quelleneinheit Leistung",
    "Einheitenstatus",
]


def metric_output_column(metric_key: str, *, specific: bool = False) -> str:
    """Liefert eine eindeutige Spaltenbezeichnung samt belastbarer Einheit."""

    label = METRIC_LABELS[metric_key]
    if metric_key in POWER_METRIC_KEYS:
        return f"{label} [{'W/m²' if specific else 'W'}]"
    return f"{label} [{METRIC_UNITS[metric_key]}]"


def raw_metric_output_column(metric_key: str) -> str:
    """Kennzeichnet Aggregationen aus Leistungsreihen ohne Einheitenbehauptung."""

    return f"Einheitenoffener Aggregationskennwert: {METRIC_LABELS[metric_key]} [Quelleneinheit]"


def output_columns(power_display_mode: str = "both", *, include_absolute_fallback: bool = False) -> list[str]:
    """Baut die Ausgabespalten für absolute, spezifische oder beide Werte."""

    columns = BASE_OUTPUT_COLUMNS.copy()
    for metric_key in METRIC_DEFINITIONS:
        if metric_key not in POWER_METRIC_KEYS:
            columns.append(metric_output_column(metric_key))
            continue
        columns.append(raw_metric_output_column(metric_key))
        if power_display_mode in {"absolute", "both"} or include_absolute_fallback:
            columns.append(metric_output_column(metric_key))
        if power_display_mode in {"specific", "both"}:
            columns.append(metric_output_column(metric_key, specific=True))
    return columns


V2_OUTPUT_COLUMNS = output_columns("both")
V2_COLUMN_RENAME = {
    "variant": "Variante",
    "room": "Raum",
    "evaluation_hours": "Auswertungsstunden [h]",
    "reference_area_m2": "Bezugsfläche [m²]",
    "specific_power_status": "Spezifische Leistung",
    "power_source_unit_label": "Quelleneinheit Leistung",
    "power_unit_status": "Einheitenstatus",
    **{
        metric_key: metric_output_column(metric_key)
        for metric_key in METRIC_DEFINITIONS
        if metric_key not in POWER_METRIC_KEYS
    },
    **{metric_key: metric_output_column(metric_key) for metric_key in POWER_METRIC_KEYS},
    **{f"{metric_key}_per_m2": metric_output_column(metric_key, specific=True) for metric_key in POWER_METRIC_KEYS},
    **{f"raw_{metric_key}": raw_metric_output_column(metric_key) for metric_key in POWER_METRIC_KEYS},
}

# Das historische ``metrics``-Blatt bleibt als Adapter erhalten. Nicht belegte
# Felder werden bewusst leer gelassen; insbesondere sind Zeilenzahl und
# Nutzungsstunden nicht gleichzusetzen.
LEGACY_OUTPUT_COLUMNS = [
    "Zone",
    "Group",
    "Zone multiplier, M",
    "Min temp., °C",
    "Max temp., °C",
    "Min op temp., °C",
    "Max op temp., °C",
    "Room unit heat, kWh",
    "Room unit heat, kWh/m2",
    "Max heat supplied, W/m2",
    "Room unit heat, W/m2",
    "Max heat removed, W/m2",
    "Room unit cool, kWh",
    "Room unit cool, kWh/m2",
    "Room unit cool, W/m2",
    "Dryvent cool, W/m2",
    "Max sup airflow, L/s m2",
    "Max rtn airflow, L/s",
    "Max solar gain, W/m2",
    "Min rel hum, %",
    "Max rel hum, %",
    "Max CO2 ppm (vol)",
    "Max PPD, %",
    "Max age of air, h",
    "In use, h",
    "h of T_op>25, h",
    "h of T_op>27, h",
    "Occ. hours, h PDH, h",
    "Unmet hours (cooling)",
    "Unmet hours (heating)",
    "DIN 4108-2 over-temperature degree hours, h Deg-C",
]

LEGACY_COLUMN_RENAME = {
    "room": "Zone",
    "variant": "Group",
    "min_tair": "Min temp., °C",
    "max_tair": "Max temp., °C",
    "min_top": "Min op temp., °C",
    "max_top": "Max op temp., °C",
    "max_q_heat_per_m2": "Max heat supplied, W/m2",
    "peak_abs_q_cool_per_m2": "Max heat removed, W/m2",
    "min_relhum": "Min rel hum, %",
    "max_relhum": "Max rel hum, %",
    "max_co2": "Max CO2 ppm (vol)",
    "max_air_age": "Max age of air, h",
}

# Historische Python-Importe behalten den bisherigen Vertrag. Neue Verbraucher
# verwenden explizit die V2-Namen oder ``output_columns``.
OUTPUT_COLUMNS = LEGACY_OUTPUT_COLUMNS
COLUMN_RENAME = LEGACY_COLUMN_RENAME
