"""Bearbeitbarer 29Z-Entwurf aus den 29 IFC-Raeumen des SmallOffice."""

from __future__ import annotations

from ma_building import load_small_office_5z_endvariant_02_building_spec

from .models import ThermalZone, ZoneAssumption, ZoneModelSpecification


def build_small_office_29z_draft() -> ZoneModelSpecification:
    """Erzeugt genau eine thermische Zone je IFC-Raum, ohne 5Z-Wertvererbung."""
    building = load_small_office_5z_endvariant_02_building_spec()
    zones = tuple(
        ThermalZone(
            zone_id=f"ZONE-29Z-{space.space_id.removeprefix('ROOM-IFC-')}",
            name=space.name,
            usage_profile_id="",
            floor_area_m2=space.floor_area_m2,
            volume_m3=space.volume_m3,
            source_space_ids=(space.space_id,),
            heating_setpoint_c=0.0,
            cooling_setpoint_c=0.0,
            minimum_air_change_rate_1_h=0.0,
        )
        for space in building.spaces
    )
    return ZoneModelSpecification(
        schema_version="1.0",
        zone_model_id="ZONEVAR-SMALLOFFICE-29Z-DRAFT-001",
        project_id="PROJECT-SMALL-OFFICE-V1",
        building_id=building.building.building_id,
        source_building_version_id=building.model_version.version_id,
        input_detail_level=building.input_detail_level.value,
        zones=zones,
        usage_profiles=(),
        assumptions=(
            ZoneAssumption(
                assumption_id="SMALLOFFICE-29Z-DRAFT-001",
                location="zones",
                text=(
                    "Jeder der 29 IFC-Raeume bildet eine thermische Zone. "
                    "Es werden keine Profil- oder Lastwerte aus dem 5Z-Modell geerbt."
                ),
            ),
        ),
    )
