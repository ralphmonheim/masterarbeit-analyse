"""Offline-Standortaufloesung fuer ortsgenaue TRY-Dateien."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import yaml

DEFAULT_WEATHER_GEODATA_CONFIG = Path("config/ma_weather/geodata/example_weather_geodata_sources.yaml")
TRY_SOURCE_CRS_EPSG = 3034
WGS84_EPSG = 4326


class WeatherLocationResolutionStatus(StrEnum):
    """Status der offline berechneten Standortaufloesung."""

    NOT_CONFIGURED = "not_configured"
    MATCHED = "matched"
    MATCHED_WITH_WARNING = "matched_with_warning"
    INVALID_COORDINATES = "invalid_coordinates"
    DEPENDENCY_MISSING = "dependency_missing"
    GEODATA_MISSING = "geodata_missing"
    MUNICIPALITY_NOT_FOUND = "municipality_not_found"
    MULTIPLE_MUNICIPALITY_MATCHES = "multiple_municipality_matches"


@dataclass(frozen=True, slots=True)
class WeatherGeodataSource:
    """Beschreibt eine lokale GeoJSON-Quelle fuer Standortauflösung."""

    source_id: str
    kind: str
    path: Path
    crs_epsg: int = WGS84_EPSG
    name_field: str = ""
    code_field: str = ""
    state_field: str = ""
    postal_code_field: str = ""
    version: str = ""
    license: str = ""


@dataclass(frozen=True, slots=True)
class WeatherLocationResolution:
    """Ergebnis der Standortaufloesung fuer TRY-Koordinaten."""

    status: WeatherLocationResolutionStatus
    source_easting: float | None = None
    source_northing: float | None = None
    source_crs_epsg: int = TRY_SOURCE_CRS_EPSG
    longitude: float | None = None
    latitude: float | None = None
    elevation_m: float | None = None
    municipality_name: str = ""
    municipality_code: str = ""
    federal_state: str = ""
    postal_code: str = ""
    municipality_match_method: str = ""
    postal_code_match_method: str = ""
    geodata_source_id: str = ""
    messages: tuple[str, ...] = ()
    is_blocking: bool = False

    def to_metadata(self) -> dict[str, str]:
        """Serialisiert das Ergebnis fuer Datensatzentwuerfe und Kataloge."""
        metadata: dict[str, str] = {
            "location_resolution_status": self.status.value,
            "location_resolution_blocking": "true" if self.is_blocking else "false",
            "source_crs_epsg": str(self.source_crs_epsg),
        }
        optional_values: dict[str, object | None] = {
            "source_easting": self.source_easting,
            "source_northing": self.source_northing,
            "resolved_longitude": self.longitude,
            "resolved_latitude": self.latitude,
            "elevation_m": self.elevation_m,
            "detected_municipality_name": self.municipality_name,
            "detected_municipality_code": self.municipality_code,
            "detected_federal_state": self.federal_state,
            "detected_postal_code": self.postal_code,
            "municipality_match_method": self.municipality_match_method,
            "postal_code_match_method": self.postal_code_match_method,
            "geodata_source_id": self.geodata_source_id,
            "location_resolution_messages": "; ".join(self.messages),
        }
        for key, value in optional_values.items():
            if value not in (None, ""):
                metadata[key] = f"{value}"
        return metadata


def transform_try_coordinates(
    easting: float,
    northing: float,
    *,
    source_epsg: int = TRY_SOURCE_CRS_EPSG,
    target_epsg: int = WGS84_EPSG,
) -> tuple[float, float]:
    """Transformiert TRY-Koordinaten mit `always_xy=True`."""
    try:
        from pyproj import Transformer
    except ImportError as exc:  # pragma: no cover - abhaengig von lokaler venv
        raise RuntimeError("pyproj ist fuer die EPSG:3034-Transformation erforderlich.") from exc

    transformer = Transformer.from_crs(
        f"EPSG:{source_epsg}",
        f"EPSG:{target_epsg}",
        always_xy=True,
    )
    x_value, y_value = transformer.transform(easting, northing)
    return float(x_value), float(y_value)


def resolve_weather_file_location(
    metadata: dict[str, str],
    *,
    geodata_config_path: str | Path = DEFAULT_WEATHER_GEODATA_CONFIG,
    project_root: str | Path | None = None,
) -> WeatherLocationResolution:
    """Bestimmt Gemeinde und optional PLZ aus TRY-Headerkoordinaten."""
    root = Path.cwd() if project_root is None else Path(project_root)
    config = _load_geodata_config(root / Path(geodata_config_path), root=root)
    if not config["enabled"]:
        return WeatherLocationResolution(status=WeatherLocationResolutionStatus.NOT_CONFIGURED)

    easting = _metadata_number(metadata.get("rechtswert_m", ""))
    northing = _metadata_number(metadata.get("hochwert_m", ""))
    elevation = _metadata_number(metadata.get("hoehenlage_m", ""))
    if easting is None or northing is None:
        return WeatherLocationResolution(
            status=WeatherLocationResolutionStatus.INVALID_COORDINATES,
            elevation_m=elevation,
            messages=("Rechtswert oder Hochwert fehlt im TRY-Kopf.",),
            is_blocking=True,
        )

    municipality_sources = [source for source in config["sources"] if source.kind == "municipality"]
    postal_sources = [source for source in config["sources"] if source.kind == "postal_code"]
    if not municipality_sources:
        return WeatherLocationResolution(
            status=WeatherLocationResolutionStatus.GEODATA_MISSING,
            source_easting=easting,
            source_northing=northing,
            elevation_m=elevation,
            messages=("Keine Gemeinde-Geodatenquelle konfiguriert.",),
            is_blocking=True,
        )

    try:
        longitude, latitude = transform_try_coordinates(easting, northing)
    except RuntimeError as exc:
        return WeatherLocationResolution(
            status=WeatherLocationResolutionStatus.DEPENDENCY_MISSING,
            source_easting=easting,
            source_northing=northing,
            elevation_m=elevation,
            messages=(str(exc),),
            is_blocking=True,
        )

    try:
        municipality_result = _resolve_feature(
            easting=easting,
            northing=northing,
            source=municipality_sources[0],
            root=root,
        )
    except (OSError, ValueError, RuntimeError) as exc:
        return WeatherLocationResolution(
            status=WeatherLocationResolutionStatus.GEODATA_MISSING,
            source_easting=easting,
            source_northing=northing,
            longitude=longitude,
            latitude=latitude,
            elevation_m=elevation,
            messages=(str(exc),),
            is_blocking=True,
        )

    if municipality_result["status"] == "multiple":
        return WeatherLocationResolution(
            status=WeatherLocationResolutionStatus.MULTIPLE_MUNICIPALITY_MATCHES,
            source_easting=easting,
            source_northing=northing,
            longitude=longitude,
            latitude=latitude,
            elevation_m=elevation,
            messages=("Mehrere Gemeindegeometrien treffen auf die TRY-Koordinate zu.",),
            is_blocking=True,
        )
    if municipality_result["status"] == "missing":
        return WeatherLocationResolution(
            status=WeatherLocationResolutionStatus.MUNICIPALITY_NOT_FOUND,
            source_easting=easting,
            source_northing=northing,
            longitude=longitude,
            latitude=latitude,
            elevation_m=elevation,
            messages=("Keine Gemeindegeometrie fuer die TRY-Koordinate gefunden.",),
            is_blocking=True,
        )

    municipality_properties = municipality_result["properties"]
    postal_code = ""
    postal_method = ""
    messages: list[str] = []
    status = WeatherLocationResolutionStatus.MATCHED
    if postal_sources:
        try:
            postal_result = _resolve_feature(
                easting=easting,
                northing=northing,
                source=postal_sources[0],
                root=root,
            )
            if postal_result["status"] == "matched":
                postal_code = str(postal_result["properties"].get(postal_sources[0].postal_code_field, "")).strip()
                postal_method = "point_in_polygon"
            elif postal_result["status"] == "multiple":
                status = WeatherLocationResolutionStatus.MATCHED_WITH_WARNING
                messages.append("Mehrere PLZ-Geometrien treffen auf die TRY-Koordinate zu.")
            else:
                status = WeatherLocationResolutionStatus.MATCHED_WITH_WARNING
                messages.append("Keine PLZ-Geometrie fuer die TRY-Koordinate gefunden.")
        except (OSError, ValueError, RuntimeError) as exc:
            status = WeatherLocationResolutionStatus.MATCHED_WITH_WARNING
            messages.append(f"PLZ-Aufloesung nicht verfuegbar: {exc}")

    municipality_source = municipality_sources[0]
    return WeatherLocationResolution(
        status=status,
        source_easting=easting,
        source_northing=northing,
        longitude=longitude,
        latitude=latitude,
        elevation_m=elevation,
        municipality_name=str(municipality_properties.get(municipality_source.name_field, "")).strip(),
        municipality_code=str(municipality_properties.get(municipality_source.code_field, "")).strip(),
        federal_state=str(municipality_properties.get(municipality_source.state_field, "")).strip(),
        postal_code=postal_code,
        municipality_match_method="point_in_polygon",
        postal_code_match_method=postal_method,
        geodata_source_id=municipality_source.source_id,
        messages=tuple(messages),
        is_blocking=False,
    )


def _load_geodata_config(path: Path, *, root: Path) -> dict[str, object]:
    if not path.exists():
        return {"enabled": False, "sources": []}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if payload is None:
        return {"enabled": False, "sources": []}
    if not isinstance(payload, dict):
        raise ValueError(f"Geodaten-Konfiguration muss ein YAML-Objekt sein: {path}")

    raw_sources = payload.get("geodata_sources", [])
    if not isinstance(raw_sources, list):
        raise ValueError("geodata_sources muss eine Liste sein.")
    sources = [_build_geodata_source(raw_source, root=root) for raw_source in raw_sources]
    return {"enabled": bool(payload.get("enabled", False)), "sources": sources}


def _build_geodata_source(raw_source: object, *, root: Path) -> WeatherGeodataSource:
    if not isinstance(raw_source, dict):
        raise ValueError("Geodatenquelle muss ein YAML-Objekt sein.")
    source_path = Path(str(raw_source.get("path", "")).strip())
    if not source_path.is_absolute():
        source_path = root / source_path
    return WeatherGeodataSource(
        source_id=str(raw_source.get("source_id", "")).strip(),
        kind=str(raw_source.get("kind", "")).strip(),
        path=source_path,
        crs_epsg=int(raw_source.get("crs_epsg", WGS84_EPSG)),
        name_field=str(raw_source.get("name_field", "")).strip(),
        code_field=str(raw_source.get("code_field", "")).strip(),
        state_field=str(raw_source.get("state_field", "")).strip(),
        postal_code_field=str(raw_source.get("postal_code_field", "")).strip(),
        version=str(raw_source.get("version", "")).strip(),
        license=str(raw_source.get("license", "")).strip(),
    )


def _resolve_feature(
    *,
    easting: float,
    northing: float,
    source: WeatherGeodataSource,
    root: Path,
) -> dict[str, object]:
    try:
        from shapely.geometry import Point, shape
    except ImportError as exc:  # pragma: no cover - abhaengig von lokaler venv
        raise RuntimeError("shapely ist fuer die Punkt-in-Polygon-Pruefung erforderlich.") from exc

    if not source.path.exists():
        raise FileNotFoundError(f"Geodatenquelle nicht gefunden: {source.path.relative_to(root)}")
    point_x, point_y = transform_try_coordinates(easting, northing, target_epsg=source.crs_epsg)
    point = Point(point_x, point_y)
    payload = json.loads(source.path.read_text(encoding="utf-8"))
    features = payload.get("features", [])
    if not isinstance(features, list):
        raise ValueError(f"GeoJSON-Quelle enthaelt keine Feature-Liste: {source.path}")

    matches: list[dict[str, object]] = []
    for feature in features:
        if not isinstance(feature, dict):
            continue
        geometry = feature.get("geometry")
        properties = feature.get("properties", {})
        if not isinstance(properties, dict) or geometry is None:
            continue
        if shape(geometry).covers(point):
            matches.append(properties)

    if len(matches) == 1:
        return {"status": "matched", "properties": matches[0]}
    if len(matches) > 1:
        return {"status": "multiple", "properties": {}}
    return {"status": "missing", "properties": {}}


def _metadata_number(value: str) -> float | None:
    match = re.search(r"-?\d+(?:[,.]\d+)?", str(value))
    if match is None:
        return None
    return float(match.group(0).replace(",", "."))
