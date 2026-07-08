"""Builder und Tabellenhelfer fuer ParameterSnapshot v1."""

from __future__ import annotations

from ma_building import BuildingModelSpecification, load_business_integration_lod1_building_spec, validate_building_spec
from ma_technical import (
    TechnicalSystemSpecification,
    load_business_integration_lod1_technical_spec,
    validate_technical_spec,
)
from ma_zones import ZoneModelSpecification, load_business_integration_lod1_zone_spec, validate_zone_spec

from .models import ParameterSnapshot, ParameterSourceReference, ParameterValue
from .previews import build_lod1_parameter_preview_rows

BUSINESS_INTEGRATION_LOD1_SNAPSHOT_ID = "PARAM-BI-LOD1-SNAPSHOT-0001"
BUSINESS_INTEGRATION_LOD1_SNAPSHOT_VERSION = "PARAM-BI-LOD1-V1"


def build_business_integration_lod1_parameter_snapshot() -> ParameterSnapshot:
    """Laedt die BusinessIntegration-Demos und baut einen Snapshot v1."""
    building_spec = load_business_integration_lod1_building_spec()
    zone_spec = load_business_integration_lod1_zone_spec()
    technical_spec = load_business_integration_lod1_technical_spec()
    return build_lod1_parameter_snapshot(
        building_spec,
        zone_spec,
        technical_spec,
        snapshot_id=BUSINESS_INTEGRATION_LOD1_SNAPSHOT_ID,
        snapshot_version=BUSINESS_INTEGRATION_LOD1_SNAPSHOT_VERSION,
    )


def build_lod1_parameter_snapshot(
    building_spec: BuildingModelSpecification,
    zone_spec: ZoneModelSpecification,
    technical_spec: TechnicalSystemSpecification,
    *,
    snapshot_id: str,
    snapshot_version: str,
) -> ParameterSnapshot:
    """Erzeugt einen ParameterSnapshot aus der validierten LoD-1-Eingabekette."""
    source_references = _source_references(building_spec, zone_spec, technical_spec)
    values = tuple(
        ParameterValue(
            parameter_key=row.parameter_key,
            label=row.label,
            value=row.value,
            unit=row.unit if row.unit else "dimensionless",
            source_reference_id=_source_reference_id(row.module_key, row.source),
            status="released",
        )
        for row in build_lod1_parameter_preview_rows(building_spec, zone_spec, technical_spec)
    )
    return ParameterSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        project_id=building_spec.project.project_id,
        building_id=building_spec.building.building_id,
        input_detail_level=str(building_spec.input_detail_level.value),
        values=values,
        source_references=source_references,
        description="BusinessIntegration-LoD-1 ParameterSnapshot aus Building, Zones und Technical.",
    )


def parameter_snapshot_summary_rows(snapshot: ParameterSnapshot) -> list[dict[str, object]]:
    """Bereitet Snapshot-Kopfdaten fuer die UI auf."""
    return [
        {"Kennwert": "Snapshot", "Wert": snapshot.snapshot_id},
        {"Kennwert": "Version", "Wert": snapshot.snapshot_version},
        {"Kennwert": "Schema", "Wert": snapshot.schema_version},
        {"Kennwert": "Projekt", "Wert": snapshot.project_id},
        {"Kennwert": "Gebaeude", "Wert": snapshot.building_id},
        {"Kennwert": "Eingabe-LoD", "Wert": snapshot.input_detail_level},
        {"Kennwert": "Parameterwerte", "Wert": len(snapshot.values)},
        {"Kennwert": "Quellen", "Wert": len(snapshot.source_references)},
    ]


def parameter_snapshot_value_rows(snapshot: ParameterSnapshot) -> list[dict[str, object]]:
    """Bereitet Parameterwerte fuer UI-Tabellen und Tests auf."""
    source_by_id = {source.source_reference_id: source for source in snapshot.source_references}
    rows: list[dict[str, object]] = []
    for value in snapshot.values:
        source = source_by_id.get(value.source_reference_id)
        rows.append(
            {
                "Parameter": value.parameter_key,
                "Bezeichnung": value.label,
                "Wert": value.value,
                "Einheit": value.unit,
                "Quelle": value.source_reference_id,
                "Modul": source.module_key if source else "",
                "Status": value.status,
            }
        )
    return rows


def parameter_snapshot_source_rows(snapshot: ParameterSnapshot) -> list[dict[str, object]]:
    """Bereitet Quellenreferenzen fuer UI-Tabellen und Tests auf."""
    return [
        {
            "Quelle": source.source_reference_id,
            "Modul": source.module_key,
            "Datensatz": source.dataset_key,
            "Version": source.version_id,
            "Validierung": source.validation_status,
            "Label": source.label,
        }
        for source in snapshot.source_references
    ]


def _source_references(
    building_spec: BuildingModelSpecification,
    zone_spec: ZoneModelSpecification,
    technical_spec: TechnicalSystemSpecification,
) -> tuple[ParameterSourceReference, ...]:
    building_status = validate_building_spec(building_spec).release_status.value
    zone_status = validate_zone_spec(zone_spec, building_spec=building_spec).release_status.value
    technical_status = validate_technical_spec(technical_spec, zone_spec=zone_spec).release_status.value
    return (
        ParameterSourceReference(
            source_reference_id=_source_reference_id("ma_building", building_spec.model_version.version_id),
            module_key="ma_building",
            dataset_key=building_spec.building.building_id,
            version_id=building_spec.model_version.version_id,
            validation_status=building_status,
            label=building_spec.building.name,
        ),
        ParameterSourceReference(
            source_reference_id=_source_reference_id("ma_zones", zone_spec.zone_model_id),
            module_key="ma_zones",
            dataset_key=zone_spec.zone_model_id,
            version_id=zone_spec.zone_model_id,
            validation_status=zone_status,
            label="BusinessIntegration LoD-1 Zonenmodell",
        ),
        ParameterSourceReference(
            source_reference_id=_source_reference_id("ma_technical", technical_spec.technical_model_id),
            module_key="ma_technical",
            dataset_key=technical_spec.technical_model_id,
            version_id=technical_spec.technical_model_id,
            validation_status=technical_status,
            label="BusinessIntegration LoD-1 Technikmodell",
        ),
    )


def _source_reference_id(module_key: str, version_id: str) -> str:
    return f"{module_key}:{version_id}"
