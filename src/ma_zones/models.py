"""Einfache Fachmodelle fuer ma_zones LoD-1."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class ZoneInputDetailLevel(StrEnum):
    """Umfang der Eingabedaten fuer ma_zones."""

    LOD_1 = "LOD-1"
    LOD_2 = "LOD-2"
    LOD_3 = "LOD-3"


@dataclass(frozen=True, slots=True)
class UsageProfile:
    """Nutzungsprofil mit einfachen LoD-1-Last- und Betriebsannahmen."""

    profile_id: str
    name: str
    operation_start_hour: float
    operation_end_hour: float
    operation_days_per_week: int
    occupancy_density_m2_per_person: float
    lighting_power_w_m2: float
    equipment_power_w_m2: float


@dataclass(frozen=True, slots=True)
class ThermalZone:
    """Bestaetigte thermische Zone."""

    zone_id: str
    name: str
    usage_profile_id: str
    floor_area_m2: float
    volume_m3: float
    source_space_ids: tuple[str, ...] = ()
    heating_setpoint_c: float = 20.0
    cooling_setpoint_c: float = 26.0
    minimum_air_change_rate_1_h: float = 0.5

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_space_ids", tuple(self.source_space_ids))


@dataclass(frozen=True, slots=True)
class ZoneAssumption:
    """Dokumentierte Annahme fuer das Zonenmodell."""

    assumption_id: str
    text: str
    location: str | None = None


@dataclass(frozen=True, slots=True)
class ZoneModelSpecification:
    """Versionierte Zonenspezifikation fuer die BusinessIntegration-Kette."""

    schema_version: str
    zone_model_id: str
    project_id: str
    building_id: str
    source_building_version_id: str
    input_detail_level: ZoneInputDetailLevel | str
    zones: tuple[ThermalZone, ...]
    usage_profiles: tuple[UsageProfile, ...]
    assumptions: tuple[ZoneAssumption, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "zones", tuple(self.zones))
        object.__setattr__(self, "usage_profiles", tuple(self.usage_profiles))
        object.__setattr__(self, "assumptions", tuple(self.assumptions))
        if not isinstance(self.input_detail_level, ZoneInputDetailLevel):
            value_text = str(self.input_detail_level).strip()
            try:
                object.__setattr__(self, "input_detail_level", ZoneInputDetailLevel(value_text))
            except ValueError:
                object.__setattr__(self, "input_detail_level", value_text)

    @property
    def zone_ids(self) -> set[str]:
        return {zone.zone_id for zone in self.zones}

    @property
    def usage_profile_ids(self) -> set[str]:
        return {profile.profile_id for profile in self.usage_profiles}

    def object_id_locations(self) -> tuple[tuple[str, str], ...]:
        """Liefert Objekt-IDs mit Fundstelle fuer die Validierung."""
        rows: list[tuple[str, str]] = [(self.zone_model_id, "zone_model_id")]
        rows.extend((zone.zone_id, f"zones.{index}.zone_id") for index, zone in enumerate(self.zones))
        rows.extend(
            (profile.profile_id, f"usage_profiles.{index}.profile_id")
            for index, profile in enumerate(self.usage_profiles)
        )
        rows.extend(
            (assumption.assumption_id, f"assumptions.{index}.assumption_id")
            for index, assumption in enumerate(self.assumptions)
        )
        return tuple(rows)


def _mapping(data: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = data.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"{key} fehlt oder ist keine Mapping-Struktur.")
    return value


def _sequence(data: Mapping[str, Any], key: str) -> tuple[Mapping[str, Any], ...]:
    value = data.get(key, ())
    if value is None:
        return ()
    if not isinstance(value, list | tuple):
        raise ValueError(f"{key} muss eine Liste sein.")
    if not all(isinstance(item, Mapping) for item in value):
        raise ValueError(f"{key} darf nur Mapping-Eintraege enthalten.")
    return tuple(value)


def zone_specification_from_dict(data: Mapping[str, Any]) -> ZoneModelSpecification:
    """Wandelt YAML-/JSON-kompatible Daten in die ma_zones-Fachmodelle um."""
    return ZoneModelSpecification(
        schema_version=str(data.get("schema_version", "")).strip(),
        zone_model_id=str(data.get("zone_model_id", "")).strip(),
        project_id=str(data.get("project_id", "")).strip(),
        building_id=str(data.get("building_id", "")).strip(),
        source_building_version_id=str(data.get("source_building_version_id", "")).strip(),
        input_detail_level=str(data.get("input_detail_level", ZoneInputDetailLevel.LOD_1.value)).strip(),
        usage_profiles=tuple(
            UsageProfile(
                profile_id=str(item.get("profile_id", "")).strip(),
                name=str(item.get("name", "")).strip(),
                operation_start_hour=float(item.get("operation_start_hour", 0.0)),
                operation_end_hour=float(item.get("operation_end_hour", 0.0)),
                operation_days_per_week=int(item.get("operation_days_per_week", 0)),
                occupancy_density_m2_per_person=float(item.get("occupancy_density_m2_per_person", 0.0)),
                lighting_power_w_m2=float(item.get("lighting_power_w_m2", 0.0)),
                equipment_power_w_m2=float(item.get("equipment_power_w_m2", 0.0)),
            )
            for item in _sequence(data, "usage_profiles")
        ),
        zones=tuple(
            ThermalZone(
                zone_id=str(item.get("zone_id", "")).strip(),
                name=str(item.get("name", "")).strip(),
                usage_profile_id=str(item.get("usage_profile_id", "")).strip(),
                floor_area_m2=float(item.get("floor_area_m2", 0.0)),
                volume_m3=float(item.get("volume_m3", 0.0)),
                source_space_ids=tuple(str(space_id).strip() for space_id in item.get("source_space_ids", ())),
                heating_setpoint_c=float(item.get("heating_setpoint_c", 20.0)),
                cooling_setpoint_c=float(item.get("cooling_setpoint_c", 26.0)),
                minimum_air_change_rate_1_h=float(item.get("minimum_air_change_rate_1_h", 0.5)),
            )
            for item in _sequence(data, "zones")
        ),
        assumptions=tuple(
            ZoneAssumption(
                assumption_id=str(item.get("assumption_id", "")).strip(),
                text=str(item.get("text", "")).strip(),
                location=str(item["location"]).strip() if item.get("location") else None,
            )
            for item in _sequence(data, "assumptions")
        ),
    )


def zone_specification_to_dict(spec: ZoneModelSpecification) -> dict[str, Any]:
    """Erzeugt eine einfache, UI-taugliche Mapping-Darstellung."""
    return {
        "schema_version": spec.schema_version,
        "zone_model_id": spec.zone_model_id,
        "project_id": spec.project_id,
        "building_id": spec.building_id,
        "source_building_version_id": spec.source_building_version_id,
        "input_detail_level": spec.input_detail_level.value
        if isinstance(spec.input_detail_level, ZoneInputDetailLevel)
        else str(spec.input_detail_level),
        "zones": [asdict(zone) for zone in spec.zones],
        "usage_profiles": [asdict(profile) for profile in spec.usage_profiles],
        "assumptions": [asdict(assumption) for assumption in spec.assumptions],
    }


def _ensure_mapping(data: Any) -> Mapping[str, Any]:
    if not isinstance(data, Mapping):
        raise ValueError("Zonenspezifikation muss ein Mapping sein.")
    return data


def zone_specification_from_any(data: Any) -> ZoneModelSpecification:
    """Robuster Einstieg fuer Loader und Tests."""
    return zone_specification_from_dict(_ensure_mapping(data))
