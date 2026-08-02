"""Zonen, Nutzungen, Sollwerte, Lasten und Profile."""

from .demo_loader import (
    load_business_integration_lod1_zone_spec,
    load_small_office_5z_endvariant_02_zone_spec,
    load_small_office_lod1_zone_spec,
    load_zone_spec,
)
from .handover import ReleasedZoneHandover, build_released_zone_handover
from .models import (
    ThermalZone,
    UsageProfile,
    ZoneAssumption,
    ZoneInputDetailLevel,
    ZoneModelSpecification,
    ZoneTechnicalServiceAssignment,
    zone_specification_from_any,
    zone_specification_from_dict,
    zone_specification_to_dict,
)
from .paths import (
    BUSINESS_INTEGRATION_LOD1_ZONE_SPEC_PATH,
    SMALL_OFFICE_5Z_ENDVARIANT_02_ZONE_SPEC_PATH,
    SMALL_OFFICE_LOD1_ZONE_SPEC_PATH,
    ZONES_CONFIG_DIR,
)
from .small_office_29z import build_small_office_29z_draft
from .thermal_building import ThermalBuildingModel, build_thermal_building_model, validate_thermal_building_model
from .validation import (
    validate_technical_zone_integration,
    validate_zone_spec,
    validate_zone_technical_assignments,
)

__all__ = [
    "BUSINESS_INTEGRATION_LOD1_ZONE_SPEC_PATH",
    "SMALL_OFFICE_5Z_ENDVARIANT_02_ZONE_SPEC_PATH",
    "SMALL_OFFICE_LOD1_ZONE_SPEC_PATH",
    "ZONES_CONFIG_DIR",
    "ThermalZone",
    "ThermalBuildingModel",
    "ReleasedZoneHandover",
    "UsageProfile",
    "ZoneAssumption",
    "ZoneInputDetailLevel",
    "ZoneModelSpecification",
    "ZoneTechnicalServiceAssignment",
    "load_business_integration_lod1_zone_spec",
    "load_small_office_5z_endvariant_02_zone_spec",
    "load_zone_spec",
    "load_small_office_lod1_zone_spec",
    "validate_zone_spec",
    "validate_technical_zone_integration",
    "validate_zone_technical_assignments",
    "build_thermal_building_model",
    "build_released_zone_handover",
    "build_small_office_29z_draft",
    "validate_thermal_building_model",
    "zone_specification_from_any",
    "zone_specification_from_dict",
    "zone_specification_to_dict",
]
