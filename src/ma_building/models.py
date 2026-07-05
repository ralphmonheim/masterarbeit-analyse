"""Einfache Fachmodelle fuer die erste ma_building-Version."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

VALID_CONSTRUCTION_CODES = frozenset({"AW", "IW", "BP", "GD", "DA", "FA", "FI", "TA", "TI"})


class BuildingMaturityLevel(StrEnum):
    """Informationsstand des Gebaeudemodells."""

    BIL_0 = "BIL-0"
    BIL_1 = "BIL-1"
    BIL_2 = "BIL-2"
    BIL_3 = "BIL-3"
    BIL_4 = "BIL-4"
    BIL_5 = "BIL-5"


class BuildingInputDetailLevel(StrEnum):
    """Umfang der Eingabedaten fuer ma_building."""

    LOD_1 = "LOD-1"
    LOD_2 = "LOD-2"
    LOD_3 = "LOD-3"


@dataclass(frozen=True, slots=True)
class ProjectInfo:
    """Projektbezogene Kopfdaten der Gebaeudespezifikation."""

    project_id: str
    name: str


@dataclass(frozen=True, slots=True)
class BuildingInfo:
    """Basisdaten fuer ein einzelnes Gebaeude."""

    building_id: str
    name: str
    unit: str
    north_angle_deg: float
    length_m: float
    width_m: float
    height_m: float


@dataclass(frozen=True, slots=True)
class BuildingModelVersion:
    """Version und Reifegrad eines Gebaeudemodellstands."""

    version_id: str
    source_input_level: BuildingMaturityLevel | str
    detected_input_level: BuildingMaturityLevel | str
    confirmed_input_level: BuildingMaturityLevel | str
    current_maturity_level: BuildingMaturityLevel | str
    target_maturity_level: BuildingMaturityLevel | str

    def __post_init__(self) -> None:
        for field_name in (
            "source_input_level",
            "detected_input_level",
            "confirmed_input_level",
            "current_maturity_level",
            "target_maturity_level",
        ):
            value = getattr(self, field_name)
            if isinstance(value, BuildingMaturityLevel):
                continue
            value_text = str(value).strip()
            if not value_text:
                object.__setattr__(self, field_name, "")
                continue
            try:
                object.__setattr__(self, field_name, BuildingMaturityLevel(value_text))
            except ValueError:
                object.__setattr__(self, field_name, value_text)


@dataclass(frozen=True, slots=True)
class SimpleEnvelopeInput:
    """LoD-1-Huellparameter fuer einfache Dimensionierung und erste Analysen."""

    external_wall_u_value_w_m2k: float
    window_u_value_w_m2k: float
    window_area_ratio_percent: float
    roof_u_value_w_m2k: float | None = None
    floor_u_value_w_m2k: float | None = None
    external_wall_area_m2: float | None = None
    window_area_m2: float | None = None
    roof_area_m2: float | None = None
    floor_area_m2: float | None = None


@dataclass(frozen=True, slots=True)
class Storey:
    """Ein Geschoss im Gebaeudemodell."""

    storey_id: str
    name: str
    elevation_m: float
    height_m: float


@dataclass(frozen=True, slots=True)
class Space:
    """Ein geometrischer Raum mit Bezug auf ein Geschoss."""

    space_id: str
    name: str
    storey_id: str
    floor_area_m2: float
    volume_m3: float


@dataclass(frozen=True, slots=True)
class PhysicalElement:
    """Ein physisches Bauteil wie Wand, Bodenplatte, Decke oder Dach."""

    element_id: str
    element_type: str
    construction_code: str
    storey_id: str
    area_m2: float
    orientation_deg: float | None = None
    adjacent_space_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "adjacent_space_ids", tuple(self.adjacent_space_ids))


@dataclass(frozen=True, slots=True)
class Opening:
    """Fenster oder Tuer mit Host-Beziehung zum Bauteil."""

    opening_id: str
    opening_type: str
    host_element_id: str
    construction_code: str
    area_m2: float


@dataclass(frozen=True, slots=True)
class ShadingDevice:
    """Einfaches Sonnenschutzobjekt fuer eine Oeffnung."""

    shading_id: str
    opening_id: str
    shading_type: str
    description: str = ""


@dataclass(frozen=True, slots=True)
class Assumption:
    """Dokumentierte Annahme oder offener Punkt."""

    assumption_id: str
    text: str
    location: str | None = None


@dataclass(frozen=True, slots=True)
class BuildingModelSpecification:
    """Programmneutrale Gebaeudespezifikation fuer v1."""

    schema_version: str
    project: ProjectInfo
    building: BuildingInfo
    model_version: BuildingModelVersion
    storeys: tuple[Storey, ...]
    spaces: tuple[Space, ...]
    elements: tuple[PhysicalElement, ...]
    openings: tuple[Opening, ...] = ()
    shading_devices: tuple[ShadingDevice, ...] = ()
    assumptions: tuple[Assumption, ...] = ()
    input_detail_level: BuildingInputDetailLevel | str = BuildingInputDetailLevel.LOD_2
    simple_envelope: SimpleEnvelopeInput | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "storeys", tuple(self.storeys))
        object.__setattr__(self, "spaces", tuple(self.spaces))
        object.__setattr__(self, "elements", tuple(self.elements))
        object.__setattr__(self, "openings", tuple(self.openings))
        object.__setattr__(self, "shading_devices", tuple(self.shading_devices))
        object.__setattr__(self, "assumptions", tuple(self.assumptions))
        if not isinstance(self.input_detail_level, BuildingInputDetailLevel):
            value_text = str(self.input_detail_level).strip()
            try:
                object.__setattr__(self, "input_detail_level", BuildingInputDetailLevel(value_text))
            except ValueError:
                object.__setattr__(self, "input_detail_level", value_text)

    @property
    def storey_ids(self) -> set[str]:
        return {storey.storey_id for storey in self.storeys}

    @property
    def space_ids(self) -> set[str]:
        return {space.space_id for space in self.spaces}

    @property
    def element_ids(self) -> set[str]:
        return {element.element_id for element in self.elements}

    def object_id_locations(self) -> tuple[tuple[str, str], ...]:
        """Liefert Objekt-IDs mit Fundstelle fuer die Validierung."""
        rows: list[tuple[str, str]] = [
            (self.building.building_id, "building.building_id"),
        ]
        rows.extend((storey.storey_id, f"storeys.{index}.storey_id") for index, storey in enumerate(self.storeys))
        rows.extend((space.space_id, f"spaces.{index}.space_id") for index, space in enumerate(self.spaces))
        rows.extend((element.element_id, f"elements.{index}.element_id") for index, element in enumerate(self.elements))
        rows.extend((opening.opening_id, f"openings.{index}.opening_id") for index, opening in enumerate(self.openings))
        rows.extend(
            (shading.shading_id, f"shading_devices.{index}.shading_id")
            for index, shading in enumerate(self.shading_devices)
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


def _optional_float(data: Mapping[str, Any], key: str) -> float | None:
    value = data.get(key)
    if value is None:
        return None
    return float(value)


def _simple_envelope_from_dict(data: Any) -> SimpleEnvelopeInput | None:
    if data is None:
        return None
    if not isinstance(data, Mapping):
        raise ValueError("simple_envelope fehlt oder ist keine Mapping-Struktur.")
    return SimpleEnvelopeInput(
        external_wall_u_value_w_m2k=float(data.get("external_wall_u_value_w_m2k", 0.0)),
        window_u_value_w_m2k=float(data.get("window_u_value_w_m2k", 0.0)),
        window_area_ratio_percent=float(data.get("window_area_ratio_percent", -1.0)),
        roof_u_value_w_m2k=_optional_float(data, "roof_u_value_w_m2k"),
        floor_u_value_w_m2k=_optional_float(data, "floor_u_value_w_m2k"),
        external_wall_area_m2=_optional_float(data, "external_wall_area_m2"),
        window_area_m2=_optional_float(data, "window_area_m2"),
        roof_area_m2=_optional_float(data, "roof_area_m2"),
        floor_area_m2=_optional_float(data, "floor_area_m2"),
    )


def building_specification_from_dict(data: Mapping[str, Any]) -> BuildingModelSpecification:
    """Wandelt YAML-/JSON-kompatible Daten in die v1-Fachmodelle um."""
    project_data = _mapping(data, "project")
    building_data = _mapping(data, "building")
    version_data = _mapping(data, "model_version")

    return BuildingModelSpecification(
        schema_version=str(data.get("schema_version", "")).strip(),
        project=ProjectInfo(
            project_id=str(project_data.get("project_id", "")).strip(),
            name=str(project_data.get("name", "")).strip(),
        ),
        building=BuildingInfo(
            building_id=str(building_data.get("building_id", "")).strip(),
            name=str(building_data.get("name", "")).strip(),
            unit=str(building_data.get("unit", "")).strip(),
            north_angle_deg=float(building_data.get("north_angle_deg", 0.0)),
            length_m=float(building_data.get("length_m", 0.0)),
            width_m=float(building_data.get("width_m", 0.0)),
            height_m=float(building_data.get("height_m", 0.0)),
        ),
        model_version=BuildingModelVersion(
            version_id=str(version_data.get("version_id", "")).strip(),
            source_input_level=str(version_data.get("source_input_level", "")).strip(),
            detected_input_level=str(version_data.get("detected_input_level", "")).strip(),
            confirmed_input_level=str(version_data.get("confirmed_input_level", "")).strip(),
            current_maturity_level=str(version_data.get("current_maturity_level", "")).strip(),
            target_maturity_level=str(version_data.get("target_maturity_level", "")).strip(),
        ),
        storeys=tuple(
            Storey(
                storey_id=str(item.get("storey_id", "")).strip(),
                name=str(item.get("name", "")).strip(),
                elevation_m=float(item.get("elevation_m", 0.0)),
                height_m=float(item.get("height_m", 0.0)),
            )
            for item in _sequence(data, "storeys")
        ),
        spaces=tuple(
            Space(
                space_id=str(item.get("space_id", "")).strip(),
                name=str(item.get("name", "")).strip(),
                storey_id=str(item.get("storey_id", "")).strip(),
                floor_area_m2=float(item.get("floor_area_m2", 0.0)),
                volume_m3=float(item.get("volume_m3", 0.0)),
            )
            for item in _sequence(data, "spaces")
        ),
        elements=tuple(
            PhysicalElement(
                element_id=str(item.get("element_id", "")).strip(),
                element_type=str(item.get("element_type", "")).strip(),
                construction_code=str(item.get("construction_code", "")).strip(),
                storey_id=str(item.get("storey_id", "")).strip(),
                area_m2=float(item.get("area_m2", 0.0)),
                orientation_deg=(float(item["orientation_deg"]) if item.get("orientation_deg") is not None else None),
                adjacent_space_ids=tuple(str(space_id).strip() for space_id in item.get("adjacent_space_ids", ())),
            )
            for item in _sequence(data, "elements")
        ),
        openings=tuple(
            Opening(
                opening_id=str(item.get("opening_id", "")).strip(),
                opening_type=str(item.get("opening_type", "")).strip(),
                host_element_id=str(item.get("host_element_id", "")).strip(),
                construction_code=str(item.get("construction_code", "")).strip(),
                area_m2=float(item.get("area_m2", 0.0)),
            )
            for item in _sequence(data, "openings")
        ),
        shading_devices=tuple(
            ShadingDevice(
                shading_id=str(item.get("shading_id", "")).strip(),
                opening_id=str(item.get("opening_id", "")).strip(),
                shading_type=str(item.get("shading_type", "")).strip(),
                description=str(item.get("description", "")).strip(),
            )
            for item in _sequence(data, "shading_devices")
        ),
        assumptions=tuple(
            Assumption(
                assumption_id=str(item.get("assumption_id", "")).strip(),
                text=str(item.get("text", "")).strip(),
                location=str(item["location"]).strip() if item.get("location") else None,
            )
            for item in _sequence(data, "assumptions")
        ),
        input_detail_level=str(data.get("input_detail_level", BuildingInputDetailLevel.LOD_2.value)).strip(),
        simple_envelope=_simple_envelope_from_dict(data.get("simple_envelope")),
    )
