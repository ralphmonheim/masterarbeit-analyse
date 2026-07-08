"""Einfache Fachmodelle fuer ma_technical Lite."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

VALID_SYSTEM_TYPES = frozenset({"heating", "cooling", "ventilation"})


class TechnicalInputDetailLevel(StrEnum):
    """Umfang der Eingabedaten fuer ma_technical."""

    LOD_1 = "LOD-1"
    LOD_2 = "LOD-2"
    LOD_3 = "LOD-3"


@dataclass(frozen=True, slots=True)
class ReferenceTechnicalSystem:
    """Ein einfaches Referenzsystem fuer die LoD-1-Eingabekette."""

    system_id: str
    name: str
    system_type: str
    served_zone_ids: tuple[str, ...]
    design_power_w_m2: float | None = None
    supply_temperature_c: float | None = None
    return_temperature_c: float | None = None
    performance_factor: float | None = None
    air_change_rate_1_h: float | None = None
    heat_recovery_efficiency_percent: float | None = None
    control_strategy: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "served_zone_ids", tuple(self.served_zone_ids))
        object.__setattr__(self, "system_type", str(self.system_type).strip())


@dataclass(frozen=True, slots=True)
class TechnicalAssumption:
    """Dokumentierte Annahme fuer technische Systeme."""

    assumption_id: str
    text: str
    location: str | None = None


@dataclass(frozen=True, slots=True)
class TechnicalSystemSpecification:
    """Versionierte Spezifikation der technischen Referenzannahmen."""

    schema_version: str
    technical_model_id: str
    project_id: str
    building_id: str
    source_zone_model_id: str
    input_detail_level: TechnicalInputDetailLevel | str
    systems: tuple[ReferenceTechnicalSystem, ...]
    assumptions: tuple[TechnicalAssumption, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "systems", tuple(self.systems))
        object.__setattr__(self, "assumptions", tuple(self.assumptions))
        if not isinstance(self.input_detail_level, TechnicalInputDetailLevel):
            value_text = str(self.input_detail_level).strip()
            try:
                object.__setattr__(self, "input_detail_level", TechnicalInputDetailLevel(value_text))
            except ValueError:
                object.__setattr__(self, "input_detail_level", value_text)

    @property
    def system_ids(self) -> set[str]:
        return {system.system_id for system in self.systems}

    def object_id_locations(self) -> tuple[tuple[str, str], ...]:
        """Liefert Objekt-IDs mit Fundstelle fuer die Validierung."""
        rows: list[tuple[str, str]] = [(self.technical_model_id, "technical_model_id")]
        rows.extend((system.system_id, f"systems.{index}.system_id") for index, system in enumerate(self.systems))
        rows.extend(
            (assumption.assumption_id, f"assumptions.{index}.assumption_id")
            for index, assumption in enumerate(self.assumptions)
        )
        return tuple(rows)


def _sequence(data: Mapping[str, Any], key: str) -> tuple[Mapping[str, Any], ...]:
    value = data.get(key, ())
    if value is None:
        return ()
    if not isinstance(value, list | tuple):
        raise ValueError(f"{key} muss eine Liste sein.")
    if not all(isinstance(item, Mapping) for item in value):
        raise ValueError(f"{key} darf nur Mapping-Eintraege enthalten.")
    return tuple(value)


def _optional_float(data: Mapping[str, Any], key: str) -> float | None:
    value = data.get(key)
    if value is None:
        return None
    return float(value)


def technical_specification_from_dict(data: Mapping[str, Any]) -> TechnicalSystemSpecification:
    """Wandelt YAML-/JSON-kompatible Daten in die ma_technical-Fachmodelle um."""
    return TechnicalSystemSpecification(
        schema_version=str(data.get("schema_version", "")).strip(),
        technical_model_id=str(data.get("technical_model_id", "")).strip(),
        project_id=str(data.get("project_id", "")).strip(),
        building_id=str(data.get("building_id", "")).strip(),
        source_zone_model_id=str(data.get("source_zone_model_id", "")).strip(),
        input_detail_level=str(data.get("input_detail_level", TechnicalInputDetailLevel.LOD_1.value)).strip(),
        systems=tuple(
            ReferenceTechnicalSystem(
                system_id=str(item.get("system_id", "")).strip(),
                name=str(item.get("name", "")).strip(),
                system_type=str(item.get("system_type", "")).strip(),
                served_zone_ids=tuple(str(zone_id).strip() for zone_id in item.get("served_zone_ids", ())),
                design_power_w_m2=_optional_float(item, "design_power_w_m2"),
                supply_temperature_c=_optional_float(item, "supply_temperature_c"),
                return_temperature_c=_optional_float(item, "return_temperature_c"),
                performance_factor=_optional_float(item, "performance_factor"),
                air_change_rate_1_h=_optional_float(item, "air_change_rate_1_h"),
                heat_recovery_efficiency_percent=_optional_float(item, "heat_recovery_efficiency_percent"),
                control_strategy=str(item.get("control_strategy", "")).strip(),
            )
            for item in _sequence(data, "systems")
        ),
        assumptions=tuple(
            TechnicalAssumption(
                assumption_id=str(item.get("assumption_id", "")).strip(),
                text=str(item.get("text", "")).strip(),
                location=str(item["location"]).strip() if item.get("location") else None,
            )
            for item in _sequence(data, "assumptions")
        ),
    )


def technical_specification_from_any(data: Any) -> TechnicalSystemSpecification:
    """Robuster Einstieg fuer Loader und Tests."""
    if not isinstance(data, Mapping):
        raise ValueError("Technikspezifikation muss ein Mapping sein.")
    return technical_specification_from_dict(data)
