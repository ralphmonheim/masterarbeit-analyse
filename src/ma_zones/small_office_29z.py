"""Bearbeitbarer 29Z-Entwurf aus 29 pseudonymisierten Referenzraeumen."""

from __future__ import annotations

from ma_building import load_small_office_5z_endvariant_02_building_spec

from .models import ThermalZone, ZoneAssumption, ZoneModelSpecification

# Der 29Z-Entwurf ist ein eigener Vergleichsstand und darf nicht aus der
# direkten 5Z-Referenz abgeleitet werden. Die Werte bewahren den bisherigen
# pseudonymisierten IFC-Raumzuschnitt, ohne ihn als 5Z-Quellwert zu verwenden.
_REFERENCE_29Z_SPACES = (
    ("001", 65.4, 458.12305), ("002", 6.281, 17.5868), ("003", 43.56, 117.612),
    ("004", 15.12, 40.824), *((f"{index:03d}", 12.18, 32.886) for index in range(5, 13)),
    ("013", 27.447, 74.1069), ("014", 27.1135, 73.20645), ("015", 6.0, 16.2),
    ("016", 5.7, 15.39), ("017", 43.56, 117.612), ("018", 15.12, 40.824),
    *((f"{index:03d}", 12.18, 32.886) for index in range(19, 27)),
    ("027", 13.364031, 36.082883), ("028", 27.447, 74.1069), ("029", 25.849469, 69.793567),
)


def build_small_office_29z_draft() -> ZoneModelSpecification:
    """Erzeugt genau eine thermische Zone je Referenzraum ohne Wertvererbung."""
    building = load_small_office_5z_endvariant_02_building_spec()
    zones = tuple(
        ThermalZone(
            zone_id=f"ZONE-29Z-{space_id}",
            name=f"Space {space_id}",
            usage_profile_id="",
            floor_area_m2=floor_area_m2,
            volume_m3=volume_m3,
            source_space_ids=(f"SPACE-SYNTH-{space_id}",),
            heating_setpoint_c=0.0,
            cooling_setpoint_c=0.0,
            minimum_air_change_rate_1_h=0.0,
        )
        for space_id, floor_area_m2, volume_m3 in _REFERENCE_29Z_SPACES
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
                    "Jeder der 29 pseudonymisierten Referenzraeume bildet eine thermische Zone. "
                    "Es werden keine Profil- oder Lastwerte aus dem 5Z-Modell geerbt."
                ),
            ),
        ),
    )
