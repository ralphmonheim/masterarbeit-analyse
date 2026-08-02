"""Technische Systeme, Komponenten, Verteilung, Uebergabe und Regelung."""

from .ahu import AirHandlingUnit, FanConfiguration, HeatRecoveryConfiguration
from .demo_loader import (
    load_business_integration_lod1_technical_spec,
    load_small_office_5z_endvariant_02_technical_spec,
    load_small_office_lod1_technical_spec,
    load_technical_spec,
)
from .distribution import CoolingDistribution, HeatingCurve, HeatingCurvePoint, HeatingDistribution, PumpConfiguration
from .domestic_hot_water import DomesticHotWaterGeneration, ElectricReheater, ThermalStorage
from .electrical import ElectricalSystem
from .enums import (
    CapacityMode,
    ComponentAvailability,
    HeatingConfigurationMode,
    HeatingDispatchStrategy,
    HeatingFunctionalRole,
    PerformanceMetricType,
    TechnicalInputDetailLevel,
    TechnicalMedium,
    TechnicalRepresentationMode,
    TechnicalServiceType,
)
from .equipment import PhysicalEquipment
from .excel_catalogs import (
    TechnicalExcelCatalog,
    load_technical_excel_catalog,
    technical_catalog_record_status,
)
from .handover import (
    ReleasedTechnicalHandover,
    ReleasedTechnicalServiceInterfaceReference,
    build_released_technical_handover,
)
from .legacy_v2_adapter import LEGACY_V1_TO_V2_MAPPING_VERSION, adapt_legacy_v1_to_v2
from .metadata import ObjectReference, SourceMetadata, TechnicalValueMetadata
from .models import (
    VALID_SYSTEM_TYPES,
    ReferenceTechnicalSystem,
    TechnicalAssumption,
    TechnicalSystemSpecification,
    technical_specification_from_any,
    technical_specification_from_dict,
)
from .paths import (
    BUSINESS_INTEGRATION_LOD1_TECHNICAL_SPEC_PATH,
    SMALL_OFFICE_5Z_ENDVARIANT_02_TECHNICAL_SPEC_PATH,
    SMALL_OFFICE_LOD1_TECHNICAL_SPEC_PATH,
    SYNTHETIC_V2_REFERENCE_TECHNICAL_SPEC_PATH,
    TECHNICAL_CONFIG_DIR,
)
from .plant import (
    CapacityDefinition,
    CoolingGeneration,
    HeatingDispatchConfiguration,
    HeatingFunction,
    HeatingGeneration,
    PerformanceDefinition,
    TechnicalPlant,
)
from .revisions import (
    ConfirmedTechnicalWarning,
    TechnicalModelRevision,
    load_technical_model_revision,
    release_technical_model,
    technical_model_content_hash,
)
from .schedules import TechnicalSchedule, TechnicalScheduleRegistry
from .specification import TechnicalModelSchemaVersion, TechnicalModelSpecification
from .topology import TechnicalConnection, TechnicalPort, TechnicalServiceInterface, TechnicalTopology
from .v2_loader import (
    load_synthetic_v2_reference_technical_spec,
    load_technical_model_specification,
    technical_model_specification_from_dict,
)
from .validation import validate_technical_model, validate_technical_spec
from .workspace_revisions import (
    next_technical_model_id,
    next_technical_revision_id,
    release_workspace_technical_model,
    technical_revisions_directory,
)

__all__ = [
    "AirHandlingUnit",
    "BUSINESS_INTEGRATION_LOD1_TECHNICAL_SPEC_PATH",
    "SMALL_OFFICE_5Z_ENDVARIANT_02_TECHNICAL_SPEC_PATH",
    "SMALL_OFFICE_LOD1_TECHNICAL_SPEC_PATH",
    "SYNTHETIC_V2_REFERENCE_TECHNICAL_SPEC_PATH",
    "CapacityDefinition",
    "CapacityMode",
    "ComponentAvailability",
    "ConfirmedTechnicalWarning",
    "CoolingDistribution",
    "CoolingGeneration",
    "DomesticHotWaterGeneration",
    "ElectricReheater",
    "ElectricalSystem",
    "FanConfiguration",
    "HeatingConfigurationMode",
    "HeatingCurve",
    "HeatingCurvePoint",
    "HeatingDispatchConfiguration",
    "HeatingDispatchStrategy",
    "HeatingDistribution",
    "HeatingFunction",
    "HeatingFunctionalRole",
    "HeatingGeneration",
    "HeatRecoveryConfiguration",
    "LEGACY_V1_TO_V2_MAPPING_VERSION",
    "ObjectReference",
    "PerformanceDefinition",
    "PerformanceMetricType",
    "PhysicalEquipment",
    "PumpConfiguration",
    "ReleasedTechnicalHandover",
    "ReleasedTechnicalServiceInterfaceReference",
    "SourceMetadata",
    "TECHNICAL_CONFIG_DIR",
    "TechnicalConnection",
    "TechnicalMedium",
    "TechnicalModelSchemaVersion",
    "TechnicalModelSpecification",
    "TechnicalModelRevision",
    "TechnicalPlant",
    "TechnicalPort",
    "TechnicalRepresentationMode",
    "TechnicalSchedule",
    "TechnicalScheduleRegistry",
    "TechnicalServiceInterface",
    "TechnicalServiceType",
    "TechnicalTopology",
    "TechnicalValueMetadata",
    "ThermalStorage",
    "VALID_SYSTEM_TYPES",
    "ReferenceTechnicalSystem",
    "TechnicalAssumption",
    "TechnicalInputDetailLevel",
    "TechnicalSystemSpecification",
    "load_business_integration_lod1_technical_spec",
    "load_small_office_5z_endvariant_02_technical_spec",
    "load_synthetic_v2_reference_technical_spec",
    "load_technical_model_specification",
    "adapt_legacy_v1_to_v2",
    "build_released_technical_handover",
    "load_technical_model_revision",
    "release_technical_model",
    "release_workspace_technical_model",
    "load_technical_spec",
    "load_small_office_lod1_technical_spec",
    "technical_specification_from_any",
    "technical_specification_from_dict",
    "technical_model_specification_from_dict",
    "technical_model_content_hash",
    "technical_revisions_directory",
    "next_technical_model_id",
    "next_technical_revision_id",
    "validate_technical_spec",
    "TechnicalExcelCatalog",
    "load_technical_excel_catalog",
    "technical_catalog_record_status",
    "validate_technical_model",
]
