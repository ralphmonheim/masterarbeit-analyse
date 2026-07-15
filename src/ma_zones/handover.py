"""Payloadfreier Referenzcheckpoint fuer freigegebene Zonenstaende.

Der Handover transportiert bewusst keine Zonen-, Nutzungsprofil- oder
Raumzuordnungsnutzlast. Sein Content-Hash bindet diese Informationen trotzdem
vollstaendig und kanonisch, damit nachgelagerte Module einen konkreten,
reproduzierbaren P013-/P014-Stand referenzieren koennen.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any

from ma_building import BuildingModelSpecification, validate_building_spec
from ma_validation import ReleaseStatus

from .models import ZoneModelSpecification
from .thermal_building import ThermalBuildingModel, validate_thermal_building_model
from .validation import validate_zone_spec

if TYPE_CHECKING:
    from ma_technical import ReleasedTechnicalHandover


@dataclass(frozen=True, slots=True)
class ReleasedZoneHandover:
    """Kleiner, unveraenderlicher Checkpoint eines freigegebenen Zonenstands.

    ``revision_id`` wird deterministisch als ``ZONE-HANDOVER-<16 hex>`` aus
    dem kanonischen Content-Hash abgeleitet. Der DTO enthaelt absichtlich weder
    Zonen- oder Nutzungsprofilnutzlast noch Raum-Zonen-Zuordnungen.
    """

    zone_handover_id: str
    revision_id: str
    zone_model_id: str
    project_id: str
    building_id: str
    building_revision_id: str
    technical_model_id: str
    technical_revision_id: str
    technical_content_hash: str
    content_hash: str
    release_status: ReleaseStatus

    def __post_init__(self) -> None:
        if not isinstance(self.release_status, ReleaseStatus):
            object.__setattr__(self, "release_status", ReleaseStatus(self.release_status))


def build_released_zone_handover(
    building_spec: BuildingModelSpecification,
    zone_spec: ZoneModelSpecification,
    thermal_building_model: ThermalBuildingModel,
    technical_handover: ReleasedTechnicalHandover,
) -> ReleasedZoneHandover:
    """Erzeugt einen referenz-only Handover aus konsistenten Freigabestaenden.

    Building-, Zonen- und ThermalBuilding-Stand muessen jeweils ohne offene
    Validierungsbefunde freigegeben sein. Zudem muss das technische Triple des
    P014-Handovers exakt mit dem im ThermalBuildingModel gespeicherten Triple
    uebereinstimmen.
    """
    _require_types(building_spec, zone_spec, thermal_building_model)
    _require_released_validation_states(building_spec, zone_spec, thermal_building_model)

    technical_model_id, technical_revision_id, technical_content_hash = _released_technical_reference(
        technical_handover
    )
    _require_matching_technical_reference(
        thermal_building_model,
        technical_model_id=technical_model_id,
        technical_revision_id=technical_revision_id,
        technical_content_hash=technical_content_hash,
    )

    content_hash = _content_hash(
        _canonical_handover_payload(
            building_spec,
            zone_spec,
            thermal_building_model,
            technical_model_id=technical_model_id,
            technical_revision_id=technical_revision_id,
            technical_content_hash=technical_content_hash,
        )
    )
    revision_id = f"ZONE-HANDOVER-{content_hash[:16]}"
    return ReleasedZoneHandover(
        zone_handover_id=f"ma_zones:{zone_spec.zone_model_id}:{revision_id}",
        revision_id=revision_id,
        zone_model_id=zone_spec.zone_model_id,
        project_id=building_spec.project.project_id,
        building_id=building_spec.building.building_id,
        building_revision_id=building_spec.model_version.version_id,
        technical_model_id=technical_model_id,
        technical_revision_id=technical_revision_id,
        technical_content_hash=technical_content_hash,
        content_hash=content_hash,
        release_status=ReleaseStatus.RELEASED,
    )


def _require_types(
    building_spec: BuildingModelSpecification,
    zone_spec: ZoneModelSpecification,
    thermal_building_model: ThermalBuildingModel,
) -> None:
    if not isinstance(building_spec, BuildingModelSpecification):
        raise TypeError("building_spec muss eine BuildingModelSpecification sein.")
    if not isinstance(zone_spec, ZoneModelSpecification):
        raise TypeError("zone_spec muss eine ZoneModelSpecification sein.")
    if not isinstance(thermal_building_model, ThermalBuildingModel):
        raise TypeError("thermal_building_model muss ein ThermalBuildingModel sein.")


def _require_released_validation_states(
    building_spec: BuildingModelSpecification,
    zone_spec: ZoneModelSpecification,
    thermal_building_model: ThermalBuildingModel,
) -> None:
    if validate_building_spec(building_spec).release_status is not ReleaseStatus.RELEASED:
        raise ValueError("Building-Spezifikation ist nicht freigegeben.")
    if validate_zone_spec(zone_spec, building_spec=building_spec).release_status is not ReleaseStatus.RELEASED:
        raise ValueError("Zonenspezifikation ist nicht freigegeben oder nicht zum Building-Stand passend.")
    if (
        validate_thermal_building_model(
            thermal_building_model,
            building_spec=building_spec,
            zone_spec=zone_spec,
        ).release_status
        is not ReleaseStatus.RELEASED
    ):
        raise ValueError("ThermalBuildingModel ist nicht freigegeben oder nicht zum Zonenstand passend.")


def _released_technical_reference(
    technical_handover: ReleasedTechnicalHandover,
) -> tuple[str, str, str]:
    """Liest nur das freigegebene P014-Referenztriple ohne Payloadzugriff."""
    # Der lokale Import vermeidet einen Importzyklus, wenn ma_zones zuerst
    # geladen wird. Beim Builder-Aufruf ist ma_technical bereits vollstaendig
    # initialisiert und der P014-v2-Gatewaytyp muss zwingend vorliegen.
    from ma_technical import ReleasedTechnicalHandover

    if not isinstance(technical_handover, ReleasedTechnicalHandover):
        raise TypeError("technical_handover muss ein ReleasedTechnicalHandover sein.")

    technical_model_id = _required_text(
        getattr(technical_handover, "technical_model_id", None),
        "technical_handover.technical_model_id",
    )
    technical_revision_id = _required_text(
        getattr(technical_handover, "revision_id", None),
        "technical_handover.revision_id",
    )
    technical_content_hash = _required_text(
        getattr(technical_handover, "content_hash", None),
        "technical_handover.content_hash",
    )
    release_status = _release_status(
        getattr(technical_handover, "release_status", None),
        "technical_handover.release_status",
    )
    if release_status is not ReleaseStatus.RELEASED:
        raise ValueError("P014-Technik-Handover ist nicht freigegeben.")
    return technical_model_id, technical_revision_id, technical_content_hash


def _require_matching_technical_reference(
    thermal_building_model: ThermalBuildingModel,
    *,
    technical_model_id: str,
    technical_revision_id: str,
    technical_content_hash: str,
) -> None:
    model_triple = (
        _required_text(thermal_building_model.technical_model_id, "thermal_building_model.technical_model_id"),
        _required_text(thermal_building_model.technical_revision_id, "thermal_building_model.technical_revision_id"),
        _required_text(thermal_building_model.technical_content_hash, "thermal_building_model.technical_content_hash"),
    )
    handover_triple = (technical_model_id, technical_revision_id, technical_content_hash)
    if model_triple != handover_triple:
        raise ValueError("ThermalBuildingModel und P014-Handover haben unterschiedliche Technikreferenzen.")


def _canonical_handover_payload(
    building_spec: BuildingModelSpecification,
    zone_spec: ZoneModelSpecification,
    thermal_building_model: ThermalBuildingModel,
    *,
    technical_model_id: str,
    technical_revision_id: str,
    technical_content_hash: str,
) -> dict[str, object]:
    return {
        "building_reference": {
            "building_id": building_spec.building.building_id,
            "building_revision_id": building_spec.model_version.version_id,
        },
        "zone_specification": _canonical_zone_specification(zone_spec),
        "room_zone_assignments": [
            [space_id, zone_id] for space_id, zone_id in sorted(thermal_building_model.room_zone_assignments)
        ],
        "technical_reference": {
            "technical_model_id": technical_model_id,
            "technical_revision_id": technical_revision_id,
            "technical_content_hash": technical_content_hash,
        },
    }


def _canonical_zone_specification(spec: ZoneModelSpecification) -> dict[str, object]:
    return {
        "schema_version": spec.schema_version,
        "zone_model_id": spec.zone_model_id,
        "project_id": spec.project_id,
        "building_id": spec.building_id,
        "source_building_version_id": spec.source_building_version_id,
        "input_detail_level": _enum_value(spec.input_detail_level),
        "zones": _sorted_payloads(
            {
                "zone_id": zone.zone_id,
                "name": zone.name,
                "usage_profile_id": zone.usage_profile_id,
                "floor_area_m2": zone.floor_area_m2,
                "volume_m3": zone.volume_m3,
                "source_space_ids": sorted(zone.source_space_ids),
                "heating_setpoint_c": zone.heating_setpoint_c,
                "cooling_setpoint_c": zone.cooling_setpoint_c,
                "minimum_air_change_rate_1_h": zone.minimum_air_change_rate_1_h,
            }
            for zone in spec.zones
        ),
        "usage_profiles": _sorted_payloads(
            {
                "profile_id": profile.profile_id,
                "name": profile.name,
                "operation_start_hour": profile.operation_start_hour,
                "operation_end_hour": profile.operation_end_hour,
                "operation_days_per_week": profile.operation_days_per_week,
                "occupancy_density_m2_per_person": profile.occupancy_density_m2_per_person,
                "lighting_power_w_m2": profile.lighting_power_w_m2,
                "equipment_power_w_m2": profile.equipment_power_w_m2,
            }
            for profile in spec.usage_profiles
        ),
        "assumptions": _sorted_payloads(
            {
                "assumption_id": assumption.assumption_id,
                "text": assumption.text,
                "location": assumption.location,
            }
            for assumption in spec.assumptions
        ),
    }


def _sorted_payloads(payloads: Any) -> list[dict[str, object]]:
    return sorted(payloads, key=_canonical_json)


def _content_hash(payload: dict[str, object]) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _canonical_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _enum_value(value: object) -> object:
    return value.value if isinstance(value, Enum) else value


def _required_text(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location} darf nicht leer sein.")
    return value.strip()


def _release_status(value: object, location: str) -> ReleaseStatus:
    try:
        return ReleaseStatus(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{location} ist kein gueltiger Freigabestatus.") from error
