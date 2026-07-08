"""Vorschau auf eine spaetere zentrale Parameterliste."""

from __future__ import annotations

from ma_building import BuildingModelSpecification, load_business_integration_lod1_building_spec, validate_building_spec
from ma_technical import (
    TechnicalSystemSpecification,
    load_business_integration_lod1_technical_spec,
    validate_technical_spec,
)
from ma_zones import ZoneModelSpecification, load_business_integration_lod1_zone_spec, validate_zone_spec

from .models import ParameterPreviewRow


def build_lod1_parameter_preview_rows(
    building_spec: BuildingModelSpecification,
    zone_spec: ZoneModelSpecification,
    technical_spec: TechnicalSystemSpecification,
) -> tuple[ParameterPreviewRow, ...]:
    """Erzeugt eine einfache, nicht-produktive Vorschau der LoD-1-Eingabekette."""
    rows: list[ParameterPreviewRow] = []
    rows.extend(_building_rows(building_spec))
    rows.extend(_zone_rows(zone_spec))
    rows.extend(_technical_rows(technical_spec, zone_spec=zone_spec))
    return tuple(rows)


def build_business_integration_lod1_parameter_preview_rows() -> tuple[ParameterPreviewRow, ...]:
    """Laedt die BusinessIntegration-Demos und erzeugt die LoD-1-Parameter-Vorschau."""
    building_spec = load_business_integration_lod1_building_spec()
    zone_spec = load_business_integration_lod1_zone_spec()
    technical_spec = load_business_integration_lod1_technical_spec()

    # Die Statuszeilen machen sichtbar, ob die Vorschau aus freigegebenen
    # Eingaben stammt. Die eigentliche Freigabe bleibt in den Fachmodulen.
    status_rows = (
        _status_row("ma_building", "building_validation_status", validate_building_spec(building_spec).release_status.value),
        _status_row(
            "ma_zones",
            "zone_validation_status",
            validate_zone_spec(zone_spec, building_spec=building_spec).release_status.value,
        ),
        _status_row(
            "ma_technical",
            "technical_validation_status",
            validate_technical_spec(technical_spec, zone_spec=zone_spec).release_status.value,
        ),
    )
    return (*status_rows, *build_lod1_parameter_preview_rows(building_spec, zone_spec, technical_spec))


def parameter_preview_table_rows(rows: tuple[ParameterPreviewRow, ...]) -> list[dict[str, object]]:
    """Bereitet Vorschauzeilen fuer UI-Tabellen und Tests auf."""
    return [
        {
            "Modul": row.module_key,
            "Parameter": row.parameter_key,
            "Bezeichnung": row.label,
            "Wert": row.value,
            "Einheit": row.unit,
            "Quelle": row.source,
            "Status": row.status,
        }
        for row in rows
    ]


def _status_row(module_key: str, parameter_key: str, value: str) -> ParameterPreviewRow:
    return ParameterPreviewRow(
        module_key=module_key,
        parameter_key=parameter_key,
        label="Freigabestatus",
        value=value,
        unit="",
        source="Fachvalidierung",
        status=value,
    )


def _building_rows(spec: BuildingModelSpecification) -> tuple[ParameterPreviewRow, ...]:
    source = spec.model_version.version_id
    rows = [
        ParameterPreviewRow("ma_building", "building_length_m", "Gebaeudelaenge", spec.building.length_m, "m", source),
        ParameterPreviewRow("ma_building", "building_width_m", "Gebaeudebreite", spec.building.width_m, "m", source),
        ParameterPreviewRow("ma_building", "building_height_m", "Gebaeudehoehe", spec.building.height_m, "m", source),
    ]
    if spec.simple_envelope is None:
        return tuple(rows)

    envelope = spec.simple_envelope
    rows.extend(
        [
            ParameterPreviewRow(
                "ma_building",
                "external_wall_u_value_w_m2k",
                "U-Wert Aussenwand",
                envelope.external_wall_u_value_w_m2k,
                "W/m2K",
                source,
            ),
            ParameterPreviewRow(
                "ma_building",
                "window_u_value_w_m2k",
                "U-Wert Fenster",
                envelope.window_u_value_w_m2k,
                "W/m2K",
                source,
            ),
            ParameterPreviewRow(
                "ma_building",
                "window_area_ratio_percent",
                "Fensterflaechenanteil",
                envelope.window_area_ratio_percent,
                "%",
                source,
            ),
            ParameterPreviewRow(
                "ma_building",
                "floor_area_m2",
                "Einfache Grundflaeche",
                envelope.floor_area_m2 or spec.building.length_m * spec.building.width_m,
                "m2",
                source,
            ),
        ]
    )
    return tuple(rows)


def _zone_rows(spec: ZoneModelSpecification) -> tuple[ParameterPreviewRow, ...]:
    source = spec.zone_model_id
    total_floor_area = sum(zone.floor_area_m2 for zone in spec.zones)
    total_volume = sum(zone.volume_m3 for zone in spec.zones)
    rows: list[ParameterPreviewRow] = [
        ParameterPreviewRow("ma_zones", "zone_count", "Anzahl thermische Zonen", len(spec.zones), "Stk", source),
        ParameterPreviewRow("ma_zones", "zone_floor_area_m2", "Zonenflaeche gesamt", total_floor_area, "m2", source),
        ParameterPreviewRow("ma_zones", "zone_volume_m3", "Zonenvolumen gesamt", total_volume, "m3", source),
    ]
    for zone in spec.zones:
        rows.extend(
            [
                ParameterPreviewRow(
                    "ma_zones",
                    f"{zone.zone_id}.heating_setpoint_c",
                    f"Heiz-Sollwert {zone.name}",
                    zone.heating_setpoint_c,
                    "Grad C",
                    source,
                ),
                ParameterPreviewRow(
                    "ma_zones",
                    f"{zone.zone_id}.cooling_setpoint_c",
                    f"Kuehl-Sollwert {zone.name}",
                    zone.cooling_setpoint_c,
                    "Grad C",
                    source,
                ),
                ParameterPreviewRow(
                    "ma_zones",
                    f"{zone.zone_id}.minimum_air_change_rate_1_h",
                    f"Mindestluftwechsel {zone.name}",
                    zone.minimum_air_change_rate_1_h,
                    "1/h",
                    source,
                ),
            ]
        )
    for profile in spec.usage_profiles:
        rows.extend(
            [
                ParameterPreviewRow(
                    "ma_zones",
                    f"{profile.profile_id}.occupancy_density_m2_per_person",
                    f"Belegungsdichte {profile.name}",
                    profile.occupancy_density_m2_per_person,
                    "m2/Person",
                    source,
                ),
                ParameterPreviewRow(
                    "ma_zones",
                    f"{profile.profile_id}.lighting_power_w_m2",
                    f"Beleuchtungsleistung {profile.name}",
                    profile.lighting_power_w_m2,
                    "W/m2",
                    source,
                ),
                ParameterPreviewRow(
                    "ma_zones",
                    f"{profile.profile_id}.equipment_power_w_m2",
                    f"Geraeteleistung {profile.name}",
                    profile.equipment_power_w_m2,
                    "W/m2",
                    source,
                ),
            ]
        )
    return tuple(rows)


def _technical_rows(
    spec: TechnicalSystemSpecification,
    *,
    zone_spec: ZoneModelSpecification,
) -> tuple[ParameterPreviewRow, ...]:
    source = spec.technical_model_id
    floor_area_by_zone = {zone.zone_id: zone.floor_area_m2 for zone in zone_spec.zones}
    rows: list[ParameterPreviewRow] = [
        ParameterPreviewRow("ma_technical", "technical_system_count", "Anzahl technischer Systeme", len(spec.systems), "Stk", source)
    ]
    for system in spec.systems:
        served_area = sum(floor_area_by_zone.get(zone_id, 0.0) for zone_id in system.served_zone_ids)
        if system.design_power_w_m2 is not None:
            rows.append(
                ParameterPreviewRow(
                    "ma_technical",
                    f"{system.system_id}.design_power_w_m2",
                    f"Spezifische Leistung {system.name}",
                    system.design_power_w_m2,
                    "W/m2",
                    source,
                )
            )
            rows.append(
                ParameterPreviewRow(
                    "ma_technical",
                    f"{system.system_id}.estimated_design_power_w",
                    f"Geschaetzte Leistung {system.name}",
                    round(system.design_power_w_m2 * served_area, 2),
                    "W",
                    source,
                )
            )
        if system.air_change_rate_1_h is not None:
            rows.append(
                ParameterPreviewRow(
                    "ma_technical",
                    f"{system.system_id}.air_change_rate_1_h",
                    f"Luftwechsel {system.name}",
                    system.air_change_rate_1_h,
                    "1/h",
                    source,
                )
            )
        if system.performance_factor is not None:
            rows.append(
                ParameterPreviewRow(
                    "ma_technical",
                    f"{system.system_id}.performance_factor",
                    f"Leistungszahl/Wirkungsgrad {system.name}",
                    system.performance_factor,
                    "",
                    source,
                )
            )
    return tuple(rows)
