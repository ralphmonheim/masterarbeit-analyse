"""Standort- und Klimaregionskatalog fuer ma_weather."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_WEATHER_LOCATIONS_CONFIG = Path("config/ma_weather/locations/example_weather_locations.yaml")

REQUIRED_REGION_TEXT_FIELDS = (
    "region_id",
    "region_code",
    "reference_location_id",
    "reference_location_name",
)

REQUIRED_LOCATION_TEXT_FIELDS = (
    "location_id",
    "location_name",
    "region_id",
    "reference_location_id",
)

UMLAUT_REPLACEMENTS = {
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
    "Ä": "ae",
    "Ö": "oe",
    "Ü": "ue",
}


@dataclass(frozen=True, slots=True)
class WeatherRegion:
    """Beschreibt eine TRY-Klimaregion mit ihrem Referenzstandort."""

    region_id: str
    region_number: int
    region_code: str
    reference_location_id: str
    reference_location_name: str
    region_name: str = ""
    active: bool = True


@dataclass(frozen=True, slots=True)
class WeatherLocation:
    """Beschreibt eine Stadt oder einen TRY-Referenzstandort."""

    location_id: str
    location_name: str
    normalized_name: str
    region_id: str
    reference_location_id: str
    legacy_code: str = ""
    is_reference_location: bool = False
    active: bool = True


@dataclass(frozen=True, slots=True)
class WeatherLocationCatalog:
    """Sammlung der Klimaregionen und Standorte."""

    regions: list[WeatherRegion]
    locations: list[WeatherLocation]

    def active_locations(self) -> list[WeatherLocation]:
        """Gibt aktive Standorte alphabetisch sortiert zurueck."""
        return sorted(
            (location for location in self.locations if location.active),
            key=lambda location: normalize_location_name(location.location_name),
        )

    def active_regions(self) -> list[WeatherRegion]:
        """Gibt aktive Klimaregionen nach Regionsnummer sortiert zurueck."""
        return sorted(
            (region for region in self.regions if region.active),
            key=lambda region: region.region_number,
        )

    def get_location(self, location_id: str) -> WeatherLocation:
        """Findet einen Standort ueber seine stabile ID."""
        for location in self.locations:
            if location.location_id == location_id:
                return location
        raise KeyError(f"Wetterstandort nicht gefunden: {location_id}")

    def get_location_by_name(self, location_name: str) -> WeatherLocation:
        """Findet einen Standort ueber den Anzeigenamen."""
        normalized = normalize_location_name(location_name)
        for location in self.locations:
            if location.normalized_name == normalized:
                return location
        raise KeyError(f"Wetterstandort nicht gefunden: {location_name}")

    def get_region(self, region_id: str) -> WeatherRegion:
        """Findet eine Klimaregion ueber ihre stabile ID."""
        for region in self.regions:
            if region.region_id == region_id:
                return region
        raise KeyError(f"Klimaregion nicht gefunden: {region_id}")

    def region_for_location(self, location_id: str) -> WeatherRegion:
        """Leitet die Klimaregion fuer einen Standort ab."""
        location = self.get_location(location_id)
        return self.get_region(location.region_id)

    def reference_location_for_city(self, location_id: str) -> WeatherLocation:
        """Leitet den TRY-Referenzstandort fuer eine Stadt ab."""
        location = self.get_location(location_id)
        return self.get_location(location.reference_location_id)


def normalize_location_name(value: str) -> str:
    """Normalisiert Standortnamen fuer Suche und Vergleich."""
    normalized = value.strip()
    for source, replacement in UMLAUT_REPLACEMENTS.items():
        normalized = normalized.replace(source, replacement)
    return " ".join(normalized.casefold().split())


def import_weather_location_catalog(
    config_path: str | Path = DEFAULT_WEATHER_LOCATIONS_CONFIG,
) -> WeatherLocationCatalog:
    """Laedt den Standort- und Klimaregionskatalog aus YAML."""
    path = Path(config_path)
    raw_config = _load_yaml_object(path)
    raw_regions = raw_config.get("weather_regions", [])
    raw_locations = raw_config.get("weather_locations", [])
    if not isinstance(raw_regions, list):
        raise ValueError("weather_regions muss eine Liste sein.")
    if not isinstance(raw_locations, list):
        raise ValueError("weather_locations muss eine Liste sein.")

    regions: list[WeatherRegion] = []
    locations: list[WeatherLocation] = []
    errors: list[str] = []
    seen_region_ids: set[str] = set()
    seen_location_ids: set[str] = set()

    for index, raw_region in enumerate(raw_regions, start=1):
        if not isinstance(raw_region, dict):
            errors.append(f"weather_regions[{index}] muss ein Objekt sein.")
            continue
        region_errors = _validate_region_record(raw_region, index)
        region_id = str(raw_region.get("region_id", "")).strip()
        if region_id and region_id in seen_region_ids:
            region_errors.append(f"weather_regions[{index}].region_id ist doppelt: {region_id}")
        seen_region_ids.add(region_id)
        if region_errors:
            errors.extend(region_errors)
            continue
        regions.append(_build_region(raw_region))

    for index, raw_location in enumerate(raw_locations, start=1):
        if not isinstance(raw_location, dict):
            errors.append(f"weather_locations[{index}] muss ein Objekt sein.")
            continue
        location_errors = _validate_location_record(raw_location, index)
        location_id = str(raw_location.get("location_id", "")).strip()
        if location_id and location_id in seen_location_ids:
            location_errors.append(f"weather_locations[{index}].location_id ist doppelt: {location_id}")
        seen_location_ids.add(location_id)
        if location_errors:
            errors.extend(location_errors)
            continue
        locations.append(_build_location(raw_location))

    if not errors:
        errors.extend(_validate_catalog_links(regions, locations))
    if errors:
        raise ValueError("; ".join(errors))

    return WeatherLocationCatalog(regions=regions, locations=locations)


def _load_yaml_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Wetterstandortkatalog nicht gefunden: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Wetterstandortkatalog muss ein YAML-Objekt enthalten: {path}")
    return data


def _validate_region_record(raw_region: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    for field_name in REQUIRED_REGION_TEXT_FIELDS:
        value = raw_region.get(field_name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"weather_regions[{index}].{field_name} fehlt oder ist leer.")

    region_number = raw_region.get("region_number")
    if not isinstance(region_number, int) or region_number < 1:
        errors.append(f"weather_regions[{index}].region_number muss eine positive Zahl sein.")

    active = raw_region.get("active", True)
    if not isinstance(active, bool):
        errors.append(f"weather_regions[{index}].active muss true oder false sein.")
    return errors


def _validate_location_record(raw_location: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    for field_name in REQUIRED_LOCATION_TEXT_FIELDS:
        value = raw_location.get(field_name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"weather_locations[{index}].{field_name} fehlt oder ist leer.")

    for field_name in ("is_reference_location", "active"):
        value = raw_location.get(field_name, False if field_name == "is_reference_location" else True)
        if not isinstance(value, bool):
            errors.append(f"weather_locations[{index}].{field_name} muss true oder false sein.")
    return errors


def _build_region(raw_region: dict[str, Any]) -> WeatherRegion:
    return WeatherRegion(
        region_id=str(raw_region["region_id"]).strip(),
        region_number=int(raw_region["region_number"]),
        region_code=str(raw_region["region_code"]).strip(),
        reference_location_id=str(raw_region["reference_location_id"]).strip(),
        reference_location_name=str(raw_region["reference_location_name"]).strip(),
        region_name=str(raw_region.get("region_name", "")).strip(),
        active=bool(raw_region.get("active", True)),
    )


def _build_location(raw_location: dict[str, Any]) -> WeatherLocation:
    location_name = str(raw_location["location_name"]).strip()
    normalized_name = str(raw_location.get("normalized_name") or normalize_location_name(location_name)).strip()
    return WeatherLocation(
        location_id=str(raw_location["location_id"]).strip(),
        location_name=location_name,
        normalized_name=normalize_location_name(normalized_name),
        legacy_code=str(raw_location.get("legacy_code", "")).strip(),
        region_id=str(raw_location["region_id"]).strip(),
        reference_location_id=str(raw_location["reference_location_id"]).strip(),
        is_reference_location=bool(raw_location.get("is_reference_location", False)),
        active=bool(raw_location.get("active", True)),
    )


def _validate_catalog_links(
    regions: list[WeatherRegion],
    locations: list[WeatherLocation],
) -> list[str]:
    errors: list[str] = []
    regions_by_id = {region.region_id: region for region in regions}
    locations_by_id = {location.location_id: location for location in locations}

    for region in regions:
        reference_location = locations_by_id.get(region.reference_location_id)
        if reference_location is None:
            errors.append(f"{region.region_id} verweist auf unbekannten Referenzstandort {region.reference_location_id}.")
        elif not reference_location.is_reference_location:
            errors.append(f"{region.reference_location_id} ist nicht als Referenzstandort gekennzeichnet.")

    for location in locations:
        if location.region_id not in regions_by_id:
            errors.append(f"{location.location_id} verweist auf unbekannte Klimaregion {location.region_id}.")
        reference_location = locations_by_id.get(location.reference_location_id)
        if reference_location is None:
            errors.append(f"{location.location_id} verweist auf unbekannten Referenzstandort {location.reference_location_id}.")
        elif not reference_location.is_reference_location:
            errors.append(f"{location.reference_location_id} ist nicht als Referenzstandort gekennzeichnet.")
    return errors
