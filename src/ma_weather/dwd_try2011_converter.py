"""Konverter fuer DWD TRY 2011 PRN-Dateien aus IDA/ICE."""

from __future__ import annotations

import argparse
import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from ma_core.compliance import (
    DEFAULT_COMPLIANCE_AUDIT_PATH,
    ComplianceAuditLogger,
    ComplianceDecision,
    ComplianceOperation,
    ComplianceService,
    OperationRequest,
    SourceType,
    inspect_request_metadata,
)

DEFAULT_DWD_TRY2011_INPUT_DIR = Path("data/project_inbox/new/weather")
DEFAULT_DWD_TRY2011_IDM_NAME = "DWD TRY Daten 2011.idm"
DEFAULT_DWD_TRY2011_OUTPUT_DIR = Path("data/ma_weather/input")
TARGET_YEAR_HOURS = 8760

PRN_FILE_PATTERN = re.compile(
    r"^TRY(?P<year>20\d{2})_(?P<try_id>\d{2})_(?P<kind>Jahr|Somm|Wint)_DAT\.PRN$",
    re.IGNORECASE,
)
IDM_PARAMETER_PATTERN = re.compile(
    r'\(:PAR\s+:N\s+([A-Z-]+)\s+:V\s+(?:"([^"]*)"|(-?\d+(?:\.\d+)?))\)',
    re.IGNORECASE,
)
CLIMATE_NAME_PATTERN = re.compile(r'\(CLIMATE-DEF\s+:N\s+"([^"]+)"', re.IGNORECASE)

KIND_LABELS = {
    "jahr": "Jahr",
    "somm": "Somm",
    "wint": "Wint",
}
TRY_TYPE_LABELS = {
    "Jahr": "mittleres Jahr",
    "Somm": "extremer Sommer",
    "Wint": "extremer Winter",
}
UMLAUT_REPLACEMENTS = {
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "Ä": "Ae",
    "Ö": "Oe",
    "Ü": "Ue",
    "ß": "ss",
}


@dataclass(frozen=True, slots=True)
class DwdTry2011ClimateDefinition:
    """Metadaten eines CLIMATE-DEF-Eintrags aus der IDM-Uebersicht."""

    name: str
    filename: str
    station: str
    city_name: str
    folder_city_name: str
    try_id: str
    year: int
    kind: str
    latitude_deg: float | None
    longitude_deg: float | None
    elevation_m: float | None
    time_zone_hours: float | None
    wind_height_m: float | None


@dataclass(frozen=True, slots=True)
class DwdTry2011ConvertedFile:
    """Ergebnis einer konvertierten PRN-Datei."""

    source_path: Path
    target_path: Path
    city_name: str
    try_id: str
    year: int
    kind: str
    rows_read: int
    rows_written: int
    rows_dropped: int


@dataclass(frozen=True, slots=True)
class DwdTry2011ConversionSummary:
    """Zusammenfassung eines Konvertierungslaufs."""

    input_dir: Path
    output_dir: Path
    converted_files: tuple[DwdTry2011ConvertedFile, ...]

    @property
    def converted_count(self) -> int:
        return len(self.converted_files)

    @property
    def rows_written(self) -> int:
        return sum(converted.rows_written for converted in self.converted_files)


def convert_dwd_try2011_prn_folder(
    input_dir: str | Path = DEFAULT_DWD_TRY2011_INPUT_DIR,
    *,
    output_dir: str | Path = DEFAULT_DWD_TRY2011_OUTPUT_DIR,
    idm_path: str | Path | None = None,
    overwrite: bool = False,
    compliance_decision: ComplianceDecision | None = None,
) -> DwdTry2011ConversionSummary:
    """Konvertiert alle DWD-TRY-2011-PRN-Dateien in das lokale TRY-DAT-Format."""
    source_dir = Path(input_dir)
    target_root = Path(output_dir)
    overview_path = Path(idm_path) if idm_path is not None else source_dir / DEFAULT_DWD_TRY2011_IDM_NAME
    if not source_dir.exists():
        raise FileNotFoundError(f"Eingabeordner nicht gefunden: {source_dir}")
    if not overview_path.exists():
        raise FileNotFoundError(f"IDM-Uebersichtsdatei nicht gefunden: {overview_path}")

    _require_dwd_try2011_compliance(compliance_decision, overview_path)

    definitions = parse_dwd_try2011_idm(overview_path, compliance_decision=compliance_decision)
    converted_files: list[DwdTry2011ConvertedFile] = []
    for source_path in sorted(source_dir.glob("*.PRN")):
        definition = definitions.get(source_path.name.casefold())
        if definition is None:
            raise ValueError(f"Keine IDM-Zuordnung fuer PRN-Datei gefunden: {source_path.name}")
        converted_files.append(
            convert_dwd_try2011_prn_file(
                source_path,
                definition,
                output_dir=target_root,
                overwrite=overwrite,
                compliance_decision=compliance_decision,
            )
        )

    return DwdTry2011ConversionSummary(
        input_dir=source_dir,
        output_dir=target_root,
        converted_files=tuple(converted_files),
    )


def parse_dwd_try2011_idm(
    idm_path: str | Path,
    *,
    compliance_decision: ComplianceDecision | None = None,
) -> dict[str, DwdTry2011ClimateDefinition]:
    """Liest die IDA/ICE-IDM-Uebersicht und indexiert sie nach PRN-Dateiname."""
    path = Path(idm_path)
    _require_dwd_try2011_compliance(compliance_decision, path)
    definitions: dict[str, DwdTry2011ClimateDefinition] = {}
    for line in _read_text(path).splitlines():
        if "CLIMATE-DEF" not in line or "FILENAME" not in line:
            continue
        definition = _parse_climate_definition_line(line)
        definitions[definition.filename.casefold()] = definition
    if not definitions:
        raise ValueError(f"Keine CLIMATE-DEF-Eintraege in IDM-Datei gefunden: {path}")
    return definitions


def convert_dwd_try2011_prn_file(
    source_path: str | Path,
    definition: DwdTry2011ClimateDefinition,
    *,
    output_dir: str | Path = DEFAULT_DWD_TRY2011_OUTPUT_DIR,
    overwrite: bool = False,
    compliance_decision: ComplianceDecision | None = None,
) -> DwdTry2011ConvertedFile:
    """Konvertiert eine einzelne PRN-Datei in eine bestehende ma_weather-TRY-DAT-Datei."""
    source = Path(source_path)
    _require_dwd_try2011_compliance(compliance_decision, source)
    records = list(_read_prn_records(source))
    if len(records) < TARGET_YEAR_HOURS:
        raise ValueError(f"PRN-Datei hat weniger als {TARGET_YEAR_HOURS} Datenzeilen: {source}")

    target_dir = Path(output_dir) / f"TRY_{definition.try_id}_{definition.folder_city_name}"
    target_path = target_dir / f"TRY{definition.year}_{definition.try_id}_{definition.kind}.dat"
    if target_path.exists() and not overwrite:
        raise FileExistsError(f"Zieldatei existiert bereits: {target_path}")

    target_dir.mkdir(parents=True, exist_ok=True)
    _write_try_dat_file(target_path, records[:TARGET_YEAR_HOURS], definition)
    return DwdTry2011ConvertedFile(
        source_path=source,
        target_path=target_path,
        city_name=definition.city_name,
        try_id=definition.try_id,
        year=definition.year,
        kind=definition.kind,
        rows_read=len(records),
        rows_written=TARGET_YEAR_HOURS,
        rows_dropped=max(0, len(records) - TARGET_YEAR_HOURS),
    )


def authorize_dwd_try2011_local_conversion(
    idm_path: str | Path,
    *,
    confirmation_reference: str,
    permission_reference: str,
    audit_log_path: str | Path = DEFAULT_COMPLIANCE_AUDIT_PATH,
) -> ComplianceDecision:
    """Erzeugt die dokumentierte Gelb-Freigabe fuer den lokalen TRY-2011-Konverter."""
    request = OperationRequest(
        source_type=SourceType.DWD_REGISTERED_DATA,
        operation=ComplianceOperation.CONVERT,
        purpose="Lokale Konvertierung des DWD-TRY-2011-Pakets fuer ma_weather",
        file_path=Path(idm_path),
        source_origin="DWD TRY 2011, bezogen als registriertes oder bestelltes IDA-ICE-Paket",
        declared_license="Produktspezifische DWD-Bezugsrechte; Referenz erforderlich",
        official_source=True,
        attribution_present=True,
        third_party_rights_cleared=False,
    )
    service = ComplianceService(audit_logger=ComplianceAuditLogger(audit_log_path))
    decision = service.evaluate(request)
    return service.approve_yellow(
        request,
        decision,
        confirmation_reference=confirmation_reference,
        permission_reference=permission_reference,
    )


def _require_dwd_try2011_compliance(
    decision: ComplianceDecision | None,
    path: Path,
) -> None:
    if decision is None:
        request = OperationRequest(
            source_type=SourceType.DWD_REGISTERED_DATA,
            operation=ComplianceOperation.CONVERT,
            purpose="Lokale Konvertierung des DWD-TRY-2011-Pakets fuer ma_weather",
            file_path=path,
            source_origin="DWD TRY 2011, Bezugsrechte noch nicht dokumentiert",
            declared_license="Produktspezifische DWD-Bezugsrechte noch zu belegen",
            official_source=True,
            attribution_present=True,
            third_party_rights_cleared=False,
        )
        ComplianceService().evaluate(request).require_allowed()
        return
    preflight_request = OperationRequest(
        source_type=SourceType.DWD_REGISTERED_DATA,
        operation=ComplianceOperation.CONVERT,
        purpose="Metadaten-Preflight innerhalb der freigegebenen lokalen TRY-2011-Konvertierung",
        file_path=path,
        source_origin="DWD TRY 2011, freigegebener lokaler Konvertierungslauf",
        declared_license="Produktspezifische DWD-Bezugsrechte referenziert",
        official_source=True,
        attribution_present=True,
        third_party_rights_cleared=False,
    )
    inspect_request_metadata(preflight_request)
    decision.require_allowed()


def _parse_climate_definition_line(line: str) -> DwdTry2011ClimateDefinition:
    name_match = CLIMATE_NAME_PATTERN.search(line)
    params = {key.upper(): text_value or number_value for key, text_value, number_value in IDM_PARAMETER_PATTERN.findall(line)}
    filename = str(params.get("FILENAME", "")).strip()
    filename_match = PRN_FILE_PATTERN.fullmatch(filename)
    if name_match is None or filename_match is None:
        raise ValueError(f"Ungueltiger CLIMATE-DEF-Eintrag: {line[:160]}")

    year = int(filename_match.group("year"))
    kind = KIND_LABELS[filename_match.group("kind").casefold()]
    station = str(params.get("STATION", "")).strip()
    city_name = _ascii_city_name(_city_name_from_station(station, year) or name_match.group(1).split("_", maxsplit=1)[0])
    return DwdTry2011ClimateDefinition(
        name=name_match.group(1),
        filename=filename,
        station=station,
        city_name=city_name,
        folder_city_name=_safe_path_part(city_name),
        try_id=filename_match.group("try_id"),
        year=year,
        kind=kind,
        latitude_deg=_float_or_none(params.get("LATITUDE")),
        longitude_deg=_float_or_none(params.get("LONGITUDE")),
        elevation_m=_float_or_none(params.get("ELEVATION")),
        time_zone_hours=_float_or_none(params.get("TIME_ZONE")),
        wind_height_m=_float_or_none(params.get("WIND-HEIGHT")),
    )


def _read_prn_records(path: Path) -> list[dict[str, float]]:
    columns: list[str] | None = None
    records: list[dict[str, float]] = []
    for raw_line in _read_text(path).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            columns = line.lstrip("#").split()
            continue
        if columns is None:
            raise ValueError(f"PRN-Kopfzeile fehlt: {path}")
        values = line.split()
        if len(values) != len(columns):
            raise ValueError(f"PRN-Zeile hat unerwartete Spaltenzahl in {path}: {line}")
        records.append({column: float(value) for column, value in zip(columns, values, strict=True)})
    _validate_prn_columns(path, columns)
    return records


def _write_try_dat_file(
    target_path: Path,
    records: list[dict[str, float]],
    definition: DwdTry2011ClimateDefinition,
) -> None:
    pressure_hpa = _pressure_from_elevation(definition.elevation_m)
    try_coordinates = _try_coordinates_from_definition(definition)
    start = datetime(definition.year, 1, 1)
    with target_path.open("w", encoding="latin-1", newline="\n") as file:
        for line in _try_header_lines(definition, try_coordinates):
            file.write(f"{line}\n")
        for index, record in enumerate(records):
            timestamp = start + timedelta(hours=index)
            file.write(_format_try_data_line(record, timestamp, pressure_hpa, definition, try_coordinates))
            file.write("\n")


def _try_header_lines(
    definition: DwdTry2011ClimateDefinition,
    try_coordinates: tuple[float, float] | None,
) -> list[str]:
    lines = [
        "Konvertiert aus DWD TRY 2011 IDA/ICE PRN",
        f"Standort          : {definition.city_name}",
        f"Ort               : {definition.city_name}",
    ]
    if try_coordinates is not None:
        easting, northing = try_coordinates
        lines.extend(
            [
                f"Rechtswert        : {round(easting)} Meter",
                f"Hochwert          : {round(northing)} Meter",
            ]
        )
    lines.extend(
        [
            f"Hoehenlage        : {_format_number(definition.elevation_m)} Meter ueber NN",
            f"Art des TRY       : {TRY_TYPE_LABELS[definition.kind]}",
            f"Bezugszeitraum    : DWD TRY 2011, Datensatzjahr {definition.year}",
            "Datenbasis        : DWD TRY 2011 IDA/ICE PRN",
            f"Originaldatei     : {definition.filename}",
            "Umrechnung        : WindX/WindY zu WR/WG; IDirNorm vereinfacht auf horizontale Direktstrahlung projiziert.",
            "Hinweis           : IDA-PRN-Dateien enthalten 8785 Stuetzstellen; exportiert werden die ersten 8760 Jahresstunden.",
            "",
            "     RW      HW MM DD HH     t    p  WR   WG N    x  RF    B    D   A    E IL",
            "*** ",
        ]
    )
    return lines


def _format_try_data_line(
    record: dict[str, float],
    timestamp: datetime,
    pressure_hpa: float,
    definition: DwdTry2011ClimateDefinition,
    try_coordinates: tuple[float, float] | None,
) -> str:
    easting, northing = try_coordinates if try_coordinates is not None else (0.0, 0.0)
    temperature_c = record["TAir"]
    relative_humidity_pct = _clamp(record["RelHum"], 0.0, 100.0)
    wind_x = record["WindX"]
    wind_y = record["WindY"]
    wind_speed_m_s = math.hypot(wind_x, wind_y)
    wind_direction_deg = _wind_direction_from_components(wind_x, wind_y)
    cloud_cover_octas = round(_clamp(record["SkyCover"], 0.0, 100.0) / 12.5)
    water_content_g_kg = _humidity_ratio_g_kg(temperature_c, relative_humidity_pct, pressure_hpa)
    direct_horizontal = _direct_horizontal_from_normal(record["IDirNorm"], timestamp, definition)
    diffuse_horizontal = max(0.0, record["IDiffHor"])
    return (
        f"{round(easting):7d} {round(northing):7d} "
        f"{timestamp.month:2d} {timestamp.day:2d} {timestamp.hour + 1:2d} "
        f"{temperature_c:5.1f} {round(pressure_hpa):4d} "
        f"{round(wind_direction_deg):3d} {wind_speed_m_s:4.1f} "
        f"{cloud_cover_octas:1d} {water_content_g_kg:4.1f} {round(relative_humidity_pct):3d} "
        f"{round(direct_horizontal):4d} {round(diffuse_horizontal):4d} "
        f"{0:3d} {0:4d} {1:2d}"
    )


def _validate_prn_columns(path: Path, columns: list[str] | None) -> None:
    required = {"Time", "TAir", "RelHum", "WindX", "WindY", "IDirNorm", "IDiffHor", "SkyCover"}
    if columns is None:
        raise ValueError(f"PRN-Datei enthaelt keine Kopfzeile: {path}")
    missing = sorted(required.difference(columns))
    if missing:
        raise ValueError(f"PRN-Datei enthaelt nicht alle benoetigten Spalten {missing}: {path}")


def _direct_horizontal_from_normal(
    direct_normal_w_m2: float,
    timestamp: datetime,
    definition: DwdTry2011ClimateDefinition,
) -> float:
    if direct_normal_w_m2 <= 0:
        return 0.0
    latitude = definition.latitude_deg
    longitude = definition.longitude_deg
    if latitude is None or longitude is None:
        return 0.0
    sun_height_factor = _solar_cos_zenith(
        timestamp,
        latitude_deg=latitude,
        longitude_deg_east=abs(longitude),
        timezone_hours=abs(definition.time_zone_hours or 1.0),
    )
    return max(0.0, direct_normal_w_m2 * sun_height_factor)


def _try_coordinates_from_definition(definition: DwdTry2011ClimateDefinition) -> tuple[float, float] | None:
    if definition.latitude_deg is None or definition.longitude_deg is None:
        return None
    try:
        from pyproj import Transformer
    except ImportError:
        return None

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3034", always_xy=True)
    # Die IDA-Uebersicht fuehrt deutsche Ost-Laengengrade mit negativem Vorzeichen.
    easting, northing = transformer.transform(abs(definition.longitude_deg), definition.latitude_deg)
    return float(easting), float(northing)


def _solar_cos_zenith(
    timestamp: datetime,
    *,
    latitude_deg: float,
    longitude_deg_east: float,
    timezone_hours: float,
) -> float:
    """Vereinfachte NOAA-Formel fuer den Stundenmittelpunkt."""
    day_of_year = timestamp.timetuple().tm_yday
    hour_decimal = timestamp.hour + 0.5
    gamma = 2.0 * math.pi / 365.0 * (day_of_year - 1 + (hour_decimal - 12.0) / 24.0)
    equation_of_time = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2.0 * gamma)
        - 0.040849 * math.sin(2.0 * gamma)
    )
    declination = (
        0.006918
        - 0.399912 * math.cos(gamma)
        + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2.0 * gamma)
        + 0.000907 * math.sin(2.0 * gamma)
        - 0.002697 * math.cos(3.0 * gamma)
        + 0.00148 * math.sin(3.0 * gamma)
    )
    true_solar_time = hour_decimal * 60.0 + equation_of_time + 4.0 * longitude_deg_east - 60.0 * timezone_hours
    hour_angle = math.radians(true_solar_time / 4.0 - 180.0)
    latitude = math.radians(latitude_deg)
    cos_zenith = math.sin(latitude) * math.sin(declination) + math.cos(latitude) * math.cos(declination) * math.cos(hour_angle)
    return _clamp(cos_zenith, 0.0, 1.0)


def _wind_direction_from_components(wind_x: float, wind_y: float) -> float:
    if math.hypot(wind_x, wind_y) < 0.05:
        return 0.0
    return (math.degrees(math.atan2(-wind_x, -wind_y)) + 360.0) % 360.0


def _pressure_from_elevation(elevation_m: float | None) -> float:
    if elevation_m is None:
        return 1013.25
    return 1013.25 * (1.0 - 2.25577e-5 * elevation_m) ** 5.25588


def _humidity_ratio_g_kg(temperature_c: float, relative_humidity_pct: float, pressure_hpa: float) -> float:
    saturation_pressure_hpa = 6.112 * math.exp((17.67 * temperature_c) / (temperature_c + 243.5))
    vapor_pressure_hpa = _clamp(relative_humidity_pct, 0.0, 100.0) / 100.0 * saturation_pressure_hpa
    if pressure_hpa <= vapor_pressure_hpa:
        return 0.0
    return 621.98 * vapor_pressure_hpa / (pressure_hpa - vapor_pressure_hpa)


def _city_name_from_station(station: str, year: int) -> str:
    marker = f" {year} "
    if marker in station:
        return station.split(marker, maxsplit=1)[0].strip()
    return station.strip()


def _ascii_city_name(value: str) -> str:
    result = value
    for source, replacement in UMLAUT_REPLACEMENTS.items():
        result = result.replace(source, replacement)
    normalized = unicodedata.normalize("NFKD", result).encode("ascii", errors="ignore").decode("ascii")
    return normalized.strip()


def _safe_path_part(value: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^A-Za-z0-9]+", "_", value)).strip("_")


def _read_text(path: Path) -> str:
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def _float_or_none(value: object) -> float | None:
    if value in (None, ""):
        return None
    return float(str(value))


def _format_number(value: float | None) -> str:
    if value is None:
        return "nicht verfuegbar"
    return f"{value:.0f}"


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DWD TRY 2011 PRN-Dateien in ma_weather-DAT-Dateien konvertieren.")
    parser.add_argument("--input-dir", default=str(DEFAULT_DWD_TRY2011_INPUT_DIR))
    parser.add_argument("--output-dir", default=str(DEFAULT_DWD_TRY2011_OUTPUT_DIR))
    parser.add_argument("--idm-path", default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--compliance-confirmation",
        required=True,
        help="Referenz auf die dokumentierte Nutzerbestaetigung fuer die lokale Verarbeitung.",
    )
    parser.add_argument(
        "--permission-reference",
        required=True,
        help="Referenz auf Angebot, Lizenz oder schriftliche DWD-Nutzungsfreigabe.",
    )
    args = parser.parse_args(argv)

    overview_path = Path(args.idm_path) if args.idm_path else Path(args.input_dir) / DEFAULT_DWD_TRY2011_IDM_NAME
    compliance_decision = authorize_dwd_try2011_local_conversion(
        overview_path,
        confirmation_reference=args.compliance_confirmation,
        permission_reference=args.permission_reference,
    )
    summary = convert_dwd_try2011_prn_folder(
        args.input_dir,
        output_dir=args.output_dir,
        idm_path=args.idm_path,
        overwrite=args.overwrite,
        compliance_decision=compliance_decision,
    )
    print(f"Konvertierte Dateien: {summary.converted_count}")
    print(f"Geschriebene Datenzeilen: {summary.rows_written}")
    if summary.converted_files:
        print(f"Erste Zieldatei: {summary.converted_files[0].target_path}")
        print(f"Letzte Zieldatei: {summary.converted_files[-1].target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
