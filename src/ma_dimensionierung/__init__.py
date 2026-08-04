"""Vorbereiteter oeffentlicher Namespace fuer die spaetere P016-Owner-Migration.

Die Fachimplementierung bleibt in diesem Prep-Slice unveraendert im
historischen Modul. Direkte Re-Exports erhalten Objektidentitaet und
Rueckwaertskompatibilitaet, ohne eine zweite Dimensionierungslogik anzulegen.
"""

from ma_analyse.stage_1_dimensioning import (
    DEFAULT_HEATING_OUTDOOR_TEMPERATURE_C,
    DEFAULT_PERSON_SENSIBLE_GAIN_W,
    DimensioningStatus,
    DimensioningStep,
    ReferenceDimensioningResult,
    dimensioning_message_rows,
    dimensioning_step_rows,
    dimensioning_summary_rows,
    run_business_integration_lod1_reference_dimensioning,
    run_lod1_reference_dimensioning,
)

from .gateway import (
    LOD1_GATEWAY_CONTRACT_VERSION,
    LOD1_REFERENCE_METHOD_ID,
    LOD1_REFERENCE_METHOD_VERSION,
    LOD1_RESULT_ROUNDING_RULE,
    DimensioningAssumption,
    Lod1DimensioningRequest,
    Lod1GatewayExecution,
    Lod1GatewayPreparation,
    execute_lod1_reference_dimensioning,
    prepare_lod1_reference_dimensioning_request,
)
from .result_contracts import (
    CALCULATED_LOD1_RESULT_KIND,
    DIMENSIONING_RESULT_CONTRACT_VERSION,
    MANUAL_EXTERNAL_IDA_RESULT_KIND,
    CalculatedLod1ReferenceResult,
    ManualIdaReferenceLoadSet,
    ManualIdaReferenceZoneLoad,
    ManualIdaReviewStatus,
    ManualIdaSourceProvenance,
    calculated_lod1_result_from_execution,
    manual_ida_reference_load_set_from_payload,
)
from .variant_groups import (
    VariantDimensioningAssignment,
    VariantDimensioningRequest,
    build_vver_selected_lod1_requests,
    execute_vver_selected_lod1_requests,
)

__all__ = [
    "DEFAULT_HEATING_OUTDOOR_TEMPERATURE_C",
    "DEFAULT_PERSON_SENSIBLE_GAIN_W",
    "DimensioningStatus",
    "DimensioningAssumption",
    "DIMENSIONING_RESULT_CONTRACT_VERSION",
    "DimensioningStep",
    "ReferenceDimensioningResult",
    "LOD1_GATEWAY_CONTRACT_VERSION",
    "LOD1_REFERENCE_METHOD_ID",
    "LOD1_REFERENCE_METHOD_VERSION",
    "LOD1_RESULT_ROUNDING_RULE",
    "Lod1DimensioningRequest",
    "Lod1GatewayExecution",
    "Lod1GatewayPreparation",
    "CALCULATED_LOD1_RESULT_KIND",
    "MANUAL_EXTERNAL_IDA_RESULT_KIND",
    "CalculatedLod1ReferenceResult",
    "ManualIdaReferenceLoadSet",
    "ManualIdaReferenceZoneLoad",
    "ManualIdaReviewStatus",
    "ManualIdaSourceProvenance",
    "dimensioning_message_rows",
    "dimensioning_step_rows",
    "dimensioning_summary_rows",
    "execute_lod1_reference_dimensioning",
    "calculated_lod1_result_from_execution",
    "manual_ida_reference_load_set_from_payload",
    "prepare_lod1_reference_dimensioning_request",
    "run_business_integration_lod1_reference_dimensioning",
    "run_lod1_reference_dimensioning",
    "VariantDimensioningAssignment",
    "VariantDimensioningRequest",
    "build_vver_selected_lod1_requests",
    "execute_vver_selected_lod1_requests",
]
