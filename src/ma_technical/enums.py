"""Gemeinsame Enums fuer ma_technical v1/v2."""

from __future__ import annotations

from enum import StrEnum


class TechnicalInputDetailLevel(StrEnum):
    """Umfang der Eingabedaten fuer ma_technical."""

    LOD_1 = "LOD-1"
    LOD_2 = "LOD-2"
    LOD_3 = "LOD-3"


class ComponentAvailability(StrEnum):
    """Einbau- und Nutzungsstatus einer technischen Komponente."""

    NOT_INSTALLED = "not_installed"
    PLANNED = "planned"
    INSTALLED = "installed"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"


class TechnicalRepresentationMode(StrEnum):
    """Beschreibt, wie belastbar eine technische Angabe modelliert ist."""

    IDEALIZED = "idealized"
    ASSUMED = "assumed"
    SPECIFIED = "specified"
    PRODUCT_BASED = "product_based"


class CapacityMode(StrEnum):
    """Art der technischen Leistungsangabe."""

    IDEAL_UNLIMITED = "ideal_unlimited"
    ASSUMED = "assumed"
    SPECIFIED = "specified"
    DIMENSIONING_RESULT = "dimensioning_result"
    PRODUCT_BASED = "product_based"


class HeatingConfigurationMode(StrEnum):
    """Kardinalitaet der Heizfunktionen im neutralen Plant-Modell."""

    NO_HEATING = "no_heating"
    BASE_HEATING_ONLY = "base_heating_only"
    TOP_UP_HEATING_ONLY = "top_up_heating_only"
    BASE_AND_TOP_UP_HEATING = "base_and_top_up_heating"


class HeatingFunctionalRole(StrEnum):
    """Fachliche Rolle einer Heizfunktion unabhaengig vom spaeteren Adapter-Slot."""

    SOLE_SUPPLY = "sole_supply"
    BASE_LOAD = "base_load"
    TOP_UP_LOAD = "top_up_load"
    BACKUP = "backup"
    DOMESTIC_HOT_WATER_SUPPORT = "domestic_hot_water_support"
    CUSTOM = "custom"


class HeatingDispatchStrategy(StrEnum):
    """Betriebsstrategie bei mehreren Heizfunktionen."""

    BASE_FIRST = "base_first"
    PARALLEL = "parallel"
    ALTERNATING = "alternating"
    PARTIALLY_PARALLEL = "partially_parallel"
    OUTDOOR_TEMPERATURE_BASED = "outdoor_temperature_based"
    CUSTOM = "custom"


class PerformanceMetricType(StrEnum):
    """Typ einer Leistungskennzahl."""

    THERMAL_EFFICIENCY = "thermal_efficiency"
    ELECTRICAL_EFFICIENCY = "electrical_efficiency"
    HEATING_COP = "heating_cop"
    COOLING_COP = "cooling_cop"
    EER = "eer"
    FUEL_UTILIZATION_FACTOR = "fuel_utilization_factor"
    GENERIC_PERFORMANCE_FACTOR = "generic_performance_factor"


class TechnicalServiceType(StrEnum):
    """Servicearten, die ma_technical an ma_zones bereitstellt."""

    HEATING = "heating"
    COOLING = "cooling"
    SUPPLY_AIR = "supply_air"
    EXTRACT_AIR = "extract_air"
    DOMESTIC_HOT_WATER = "domestic_hot_water"


class TechnicalMedium(StrEnum):
    """Medien fuer Topologie und Serviceinterfaces."""

    WATER = "water"
    AIR = "air"
    REFRIGERANT = "refrigerant"
    BRINE = "brine"
    ELECTRICITY = "electricity"
    DOMESTIC_HOT_WATER = "domestic_hot_water"
    UNKNOWN = "unknown"
