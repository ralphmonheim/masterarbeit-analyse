"""Builder und Tabellenhelfer fuer ParameterSnapshot und Baseline-Snapshot."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace

from ma_building import BuildingModelSpecification, load_business_integration_lod1_building_spec, validate_building_spec
from ma_technical import (
    ReleasedTechnicalHandover,
    TechnicalSystemSpecification,
    load_business_integration_lod1_technical_spec,
    validate_technical_spec,
)
from ma_validation import (
    DiagnosticMessage,
    DiagnosticSeverity,
    ReleaseStatus,
    ValidationResult,
    build_validation_result,
)
from ma_weather.weather_catalog import WeatherCatalog, WeatherDataset, import_weather_catalog
from ma_weather.weather_selection import (
    WeatherActivationRecord,
    WeatherSelectionState,
    load_weather_selection_state,
    project_default_weather_dataset,
)
from ma_weather.weather_status import WeatherDatasetStatus
from ma_zones import (
    ReleasedZoneHandover,
    ZoneModelSpecification,
    load_business_integration_lod1_zone_spec,
    validate_zone_spec,
)

from .models import (
    BaselineParameterSnapshot,
    BaselineParameterValue,
    BuildingDetailMode,
    FreshnessStatus,
    ParameterClass,
    ParameterInputPackage,
    ParameterReferenceVersion,
    ParameterScope,
    ParameterScopeType,
    ParameterSnapshot,
    ParameterSourceReference,
    ParameterValue,
    ParameterVariability,
)
from .previews import build_lod1_parameter_preview_rows

BUSINESS_INTEGRATION_LOD1_SNAPSHOT_ID = "PARAM-BI-LOD1-SNAPSHOT-0001"
BUSINESS_INTEGRATION_LOD1_SNAPSHOT_VERSION = "PARAM-BI-LOD1-V1"
BUSINESS_INTEGRATION_LOD1_INPUT_PACKAGE_ID = "PARAM-BI-LOD1-INPUT-PACKAGE-0001"
BUSINESS_INTEGRATION_LOD1_INPUT_PACKAGE_VERSION = "PARAM-BI-LOD1-INPUT-PACKAGE-V1"
BUSINESS_INTEGRATION_LOD1_BASELINE_SNAPSHOT_ID = "PARAM-BI-LOD1-BASELINE-0001"
BUSINESS_INTEGRATION_LOD1_BASELINE_SNAPSHOT_VERSION = "PARAM-BI-LOD1-BASELINE-V2"


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


def build_business_integration_lod1_baseline_parameter_snapshot() -> BaselineParameterSnapshot:
    """Baut den ersten Baseline-Snapshot v2 aus dem vorhandenen LoD-1-Snapshot."""
    source_snapshot = build_business_integration_lod1_parameter_snapshot()
    return build_baseline_parameter_snapshot_from_parameter_snapshot(
        source_snapshot,
        snapshot_id=BUSINESS_INTEGRATION_LOD1_BASELINE_SNAPSHOT_ID,
        snapshot_version=BUSINESS_INTEGRATION_LOD1_BASELINE_SNAPSHOT_VERSION,
    )


def build_business_integration_lod1_parameter_input_package(
    *,
    weather_catalog: WeatherCatalog | None = None,
    weather_selection_state: WeatherSelectionState | None = None,
    weather_statuses_by_key: dict[str, WeatherDatasetStatus] | None = None,
    require_weather: bool = True,
) -> ParameterInputPackage:
    """Baut das P015-S3a-Eingangspaket aus Snapshot v1 und Wetterauswahl."""
    source_snapshot = build_business_integration_lod1_parameter_snapshot()
    catalog = import_weather_catalog() if weather_catalog is None else weather_catalog
    selection_state = load_weather_selection_state() if weather_selection_state is None else weather_selection_state
    return build_lod1_parameter_input_package_from_selection(
        source_snapshot,
        catalog,
        selection_state,
        weather_statuses_by_key=weather_statuses_by_key,
        package_id=BUSINESS_INTEGRATION_LOD1_INPUT_PACKAGE_ID,
        package_version=BUSINESS_INTEGRATION_LOD1_INPUT_PACKAGE_VERSION,
        require_weather=require_weather,
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


def build_lod1_parameter_input_package_from_selection(
    source_snapshot: ParameterSnapshot,
    weather_catalog: WeatherCatalog,
    weather_selection_state: WeatherSelectionState,
    *,
    weather_statuses_by_key: dict[str, WeatherDatasetStatus] | None = None,
    package_id: str,
    package_version: str,
    require_weather: bool = True,
) -> ParameterInputPackage:
    """Uebernimmt nur den bewusst aktivierten Projekt-Default aus ma_weather."""
    weather_dataset = project_default_weather_dataset(weather_catalog, weather_selection_state)
    weather_activation = (
        weather_selection_state.activation_for(weather_dataset.weather_key)
        if weather_dataset is not None
        else None
    )
    weather_status = (
        weather_statuses_by_key.get(weather_dataset.weather_key)
        if weather_dataset is not None and weather_statuses_by_key is not None
        else None
    )
    return build_lod1_parameter_input_package(
        source_snapshot,
        package_id=package_id,
        package_version=package_version,
        weather_dataset=weather_dataset,
        weather_status=weather_status,
        weather_activation=weather_activation,
        weather_is_activated=weather_activation is not None,
        require_weather=require_weather,
    )


def build_lod1_parameter_input_package(
    source_snapshot: ParameterSnapshot,
    *,
    package_id: str,
    package_version: str,
    weather_dataset: WeatherDataset | None = None,
    weather_status: WeatherDatasetStatus | None = None,
    weather_activation: WeatherActivationRecord | None = None,
    weather_is_activated: bool = False,
    require_weather: bool = True,
) -> ParameterInputPackage:
    """Erzeugt ein Eingangspaket ohne den bestehenden Snapshot-v1-Vertrag zu veraendern."""
    source_references = [_baseline_source_reference(source) for source in source_snapshot.source_references]
    values = list(source_snapshot.values)
    weather_activated = False

    if weather_dataset is not None:
        weather_source = _weather_source_reference(
            weather_dataset,
            weather_status=weather_status,
            weather_activation=weather_activation,
        )
        source_references.append(weather_source)
        values.extend(_weather_parameter_values(weather_dataset, weather_source, weather_status=weather_status))
        weather_activated = weather_is_activated

    return ParameterInputPackage(
        package_id=package_id,
        package_version=package_version,
        project_id=source_snapshot.project_id,
        building_id=source_snapshot.building_id,
        input_detail_level=source_snapshot.input_detail_level,
        values=tuple(values),
        source_references=tuple(source_references),
        source_snapshot_id=source_snapshot.snapshot_id,
        source_snapshot_version=source_snapshot.snapshot_version,
        requires_weather=require_weather,
        weather_activated=weather_activated,
        description="P015-S3a Eingangspaket aus LoD-1-Snapshot und aktiviertem Wetter-Default.",
    )


def build_baseline_parameter_snapshot_from_parameter_snapshot(
    source_snapshot: ParameterSnapshot,
    *,
    snapshot_id: str,
    snapshot_version: str,
    building_detail_mode: BuildingDetailMode | str = BuildingDetailMode.SIMPLIFIED,
) -> BaselineParameterSnapshot:
    """Hebt einen validierten ParameterSnapshot v1 in den Baseline-v2-Vertrag."""
    source_references = tuple(_baseline_source_reference(source) for source in source_snapshot.source_references)
    parameter_values = tuple(
        _baseline_parameter_value(source_snapshot, value, source_reference_id=value.source_reference_id)
        for value in source_snapshot.values
    )
    reference_versions = tuple(
        ParameterReferenceVersion(
            reference_id=source.reference_id,
            reference_version=source.reference_version,
            content_hash=source.content_hash,
            source_reference_id=source.source_reference_id,
            label=source.label,
        )
        for source in source_references
    )
    content_hash = _stable_hash(
        {
            "snapshot_id": snapshot_id,
            "source_snapshot_id": source_snapshot.snapshot_id,
            "values": [_baseline_value_hash_payload(value) for value in parameter_values],
            "sources": [_source_hash_payload(source) for source in source_references],
        }
    )
    return BaselineParameterSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        project_id=source_snapshot.project_id,
        building_id=source_snapshot.building_id,
        building_detail_mode=building_detail_mode,
        parameter_values=parameter_values,
        source_references=source_references,
        reference_versions=reference_versions,
        source_snapshot_id=source_snapshot.snapshot_id,
        source_snapshot_version=source_snapshot.snapshot_version,
        content_hash=content_hash,
        release_status="released",
        freshness_status=FreshnessStatus.CURRENT,
        description="BaselineParameterSnapshot v2 aus dem BusinessIntegration-LoD-1 ParameterSnapshot.",
    )


def build_baseline_parameter_snapshot_from_input_package(
    input_package: ParameterInputPackage,
    *,
    snapshot_id: str,
    snapshot_version: str,
    building_detail_mode: BuildingDetailMode | str = BuildingDetailMode.SIMPLIFIED,
) -> BaselineParameterSnapshot:
    """Leitet einen Baseline-v2-Stand aus dem P015-S3a-Eingangspaket ab."""
    source_references = tuple(_baseline_source_reference(source) for source in input_package.source_references)
    checkpoint_references = tuple(
        _baseline_source_reference(reference) for reference in input_package.checkpoint_references
    )
    parameter_values = tuple(
        _baseline_parameter_value(input_package, value, source_reference_id=value.source_reference_id)
        for value in input_package.values
    )
    reference_versions = tuple(
        ParameterReferenceVersion(
            reference_id=source.reference_id,
            reference_version=source.reference_version,
            content_hash=source.content_hash,
            source_reference_id=source.source_reference_id,
            label=source.label,
        )
        for source in source_references
    )
    content_hash_payload: dict[str, object] = {
        "snapshot_id": snapshot_id,
        "source_package_id": input_package.package_id,
        "values": [_baseline_value_hash_payload(value) for value in parameter_values],
        "sources": [_source_hash_payload(source) for source in source_references],
    }
    if input_package.requires_released_checkpoints or checkpoint_references:
        content_hash_payload["released_checkpoints"] = {
            "required": input_package.requires_released_checkpoints,
            "references": [_checkpoint_hash_payload(reference) for reference in checkpoint_references],
        }
    content_hash = _stable_hash(content_hash_payload)
    return BaselineParameterSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=snapshot_version,
        project_id=input_package.project_id,
        building_id=input_package.building_id,
        building_detail_mode=building_detail_mode,
        parameter_values=parameter_values,
        source_references=source_references,
        reference_versions=reference_versions,
        source_snapshot_id=input_package.package_id,
        source_snapshot_version=input_package.package_version,
        checkpoint_references=checkpoint_references,
        requires_released_checkpoints=input_package.requires_released_checkpoints,
        content_hash=content_hash,
        release_status=_baseline_release_status_from_input_package(input_package),
        freshness_status=FreshnessStatus.CURRENT,
        description="BaselineParameterSnapshot v2 aus dem P015-S3a-Eingangspaket.",
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


def parameter_input_package_summary_rows(input_package: ParameterInputPackage) -> list[dict[str, object]]:
    """Bereitet Kopfdaten des P015-S3a-Eingangspakets fuer UI und Tests auf."""
    return [
        {"Kennwert": "Eingangspaket", "Wert": input_package.package_id},
        {"Kennwert": "Version", "Wert": input_package.package_version},
        {"Kennwert": "Schema", "Wert": input_package.schema_version},
        {"Kennwert": "Projekt", "Wert": input_package.project_id},
        {"Kennwert": "Gebaeude", "Wert": input_package.building_id},
        {"Kennwert": "Eingabe-LoD", "Wert": input_package.input_detail_level},
        {"Kennwert": "Parameterwerte", "Wert": len(input_package.values)},
        {"Kennwert": "Quellen", "Wert": len(input_package.source_references)},
        {"Kennwert": "Wetter erforderlich", "Wert": input_package.requires_weather},
        {"Kennwert": "Wetter aktiviert", "Wert": input_package.weather_activated},
        {"Kennwert": "Quell-Snapshot", "Wert": input_package.source_snapshot_id},
    ]


def baseline_parameter_snapshot_summary_rows(snapshot: BaselineParameterSnapshot) -> list[dict[str, object]]:
    """Bereitet Baseline-v2-Kopfdaten fuer UI-Tabellen und Tests auf."""
    return [
        {"Kennwert": "Baseline", "Wert": snapshot.snapshot_id},
        {"Kennwert": "Version", "Wert": snapshot.snapshot_version},
        {"Kennwert": "Schema", "Wert": snapshot.schema_version},
        {"Kennwert": "Projekt", "Wert": snapshot.project_id},
        {"Kennwert": "Gebaeude", "Wert": snapshot.building_id},
        {"Kennwert": "Detailmodus", "Wert": snapshot.building_detail_mode.value},
        {"Kennwert": "Parameterwerte", "Wert": len(snapshot.parameter_values)},
        {"Kennwert": "Quellen", "Wert": len(snapshot.source_references)},
        {"Kennwert": "Referenzversionen", "Wert": len(snapshot.reference_versions)},
        {"Kennwert": "Freigabestatus", "Wert": snapshot.release_status},
        {"Kennwert": "Aktualitaet", "Wert": snapshot.freshness_status.value},
        {"Kennwert": "Content-Hash", "Wert": snapshot.content_hash},
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


def parameter_input_package_value_rows(input_package: ParameterInputPackage) -> list[dict[str, object]]:
    """Bereitet Eingangspaket-Werte fuer UI-Tabellen und Tests auf."""
    source_by_id = {source.source_reference_id: source for source in input_package.source_references}
    rows: list[dict[str, object]] = []
    for value in input_package.values:
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


def baseline_parameter_snapshot_value_rows(snapshot: BaselineParameterSnapshot) -> list[dict[str, object]]:
    """Bereitet Baseline-v2-Werte mit Scope und Klassifikation auf."""
    source_by_id = {source.source_reference_id: source for source in snapshot.source_references}
    rows: list[dict[str, object]] = []
    for value in snapshot.parameter_values:
        source = source_by_id.get(value.source_reference_id)
        rows.append(
            {
                "Value-ID": value.parameter_value_id,
                "Parameter": value.parameter_key,
                "Bezeichnung": value.label,
                "Scope": value.scope.scope_type.value,
                "Scope-ID": value.scope.scope_id,
                "Scope-Label": value.scope.label,
                "Klasse": value.parameter_class.value,
                "Variierbarkeit": value.variability.value,
                "Wert": value.value,
                "Einheit": value.unit,
                "Quelle": value.source_reference_id,
                "Modul": source.module_key if source else "",
                "Status": value.status,
                "Content-Hash": value.content_hash,
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


def parameter_input_package_source_rows(input_package: ParameterInputPackage) -> list[dict[str, object]]:
    """Bereitet Quellenreferenzen des Eingangspakets auf."""
    return [
        {
            "Quelle": source.source_reference_id,
            "Modul": source.module_key,
            "Datensatz": source.dataset_key,
            "Version": source.version_id,
            "Validierung": source.validation_status,
            "Referenz-ID": source.reference_id,
            "Referenzversion": source.reference_version,
            "Aktualitaet": source.freshness_status,
            "Content-Hash": source.content_hash,
            "Label": source.label,
        }
        for source in input_package.source_references
    ]


def baseline_parameter_snapshot_source_rows(snapshot: BaselineParameterSnapshot) -> list[dict[str, object]]:
    """Bereitet erweiterte Baseline-v2-Quellenreferenzen auf."""
    return [
        {
            "Quelle": source.source_reference_id,
            "Modul": source.module_key,
            "Datensatz": source.dataset_key,
            "Version": source.version_id,
            "Validierung": source.validation_status,
            "Referenz-ID": source.reference_id,
            "Referenzversion": source.reference_version,
            "Aktualitaet": source.freshness_status,
            "Content-Hash": source.content_hash,
            "Label": source.label,
        }
        for source in snapshot.source_references
    ]


def baseline_parameter_snapshot_reference_rows(snapshot: BaselineParameterSnapshot) -> list[dict[str, object]]:
    """Bereitet die versionierten Fachobjektreferenzen des Baseline-Snapshots auf."""
    return [
        {
            "Referenz-ID": reference.reference_id,
            "Version": reference.reference_version,
            "Quelle": reference.source_reference_id,
            "Content-Hash": reference.content_hash,
            "Label": reference.label,
        }
        for reference in snapshot.reference_versions
    ]


def attach_released_checkpoints_to_parameter_input_package(
    input_package: ParameterInputPackage,
    *,
    zone_handover: ReleasedZoneHandover,
    technical_handover: ReleasedTechnicalHandover,
) -> ParameterInputPackage:
    """Ergaenzt ein Paket um das zusammengehoerige P013-/P014-Checkpoint-Paar.

    Die bestehenden Parameterwerte und ``source_references`` bleiben bewusst
    unveraendert. Nur dieser explizite Factory-Pfad prueft die Beziehung der
    beiden urspruenglichen Handover; normale ``ParameterSourceReference``-
    Objekte enthalten diese Triple-Beziehung nicht.
    """
    if not isinstance(input_package, ParameterInputPackage):
        raise TypeError("input_package muss ein ParameterInputPackage sein.")
    if input_package.checkpoint_references or input_package.requires_released_checkpoints:
        raise ValueError("Das Eingangspaket enthaelt bereits einen Released-Checkpoint.")

    validation = validate_released_checkpoint_handover_pair(
        input_package,
        zone_handover=zone_handover,
        technical_handover=technical_handover,
    )
    if validation.release_status is not ReleaseStatus.RELEASED:
        raise ValueError("Das P013-/P014-Checkpoint-Paar ist nicht freigegeben oder nicht zusammengehoerig.")

    return replace(
        input_package,
        checkpoint_references=(
            parameter_checkpoint_reference_from_released_zone_handover(zone_handover),
            parameter_checkpoint_reference_from_released_technical_handover(technical_handover),
        ),
        requires_released_checkpoints=True,
    )


def validate_released_checkpoint_handover_pair(
    input_package: ParameterInputPackage,
    *,
    zone_handover: ReleasedZoneHandover,
    technical_handover: ReleasedTechnicalHandover,
) -> ValidationResult:
    """Prueft den noch nicht verlustfrei darstellbaren P013-/P014-Zusammenhang.

    Die benoetigten technischen Parent-Felder liegen nur auf den beiden
    Handover-Objekten vor. Nach der Umwandlung in die getrennten
    ``checkpoint_references`` prueft der allgemeine Paketvalidator lediglich
    Freigabe, Aktualitaet und die Form des Paares.
    """
    if not isinstance(input_package, ParameterInputPackage):
        raise TypeError("input_package muss ein ParameterInputPackage sein.")

    messages: list[DiagnosticMessage] = []
    if not isinstance(zone_handover, ReleasedZoneHandover):
        messages.append(
            _checkpoint_message(
                "PARAMETER_CHECKPOINT_ZONE_HANDOVER_INVALID",
                "P013-Checkpoint muss ein ReleasedZoneHandover sein.",
                "zone_handover",
            )
        )
    if not isinstance(technical_handover, ReleasedTechnicalHandover):
        messages.append(
            _checkpoint_message(
                "PARAMETER_CHECKPOINT_TECHNICAL_HANDOVER_INVALID",
                "P014-Checkpoint muss ein ReleasedTechnicalHandover sein.",
                "technical_handover",
            )
        )
    if messages:
        return build_validation_result(tuple(messages))

    _append_missing_checkpoint_fields(
        messages,
        zone_handover,
        field_names=(
            "zone_handover_id",
            "revision_id",
            "zone_model_id",
            "project_id",
            "building_id",
            "building_revision_id",
            "technical_model_id",
            "technical_revision_id",
            "technical_content_hash",
            "content_hash",
        ),
        location_prefix="zone_handover",
    )
    _append_missing_checkpoint_fields(
        messages,
        technical_handover,
        field_names=("technical_model_id", "revision_id", "content_hash"),
        location_prefix="technical_handover",
    )
    if _handover_release_status(zone_handover.release_status) != ReleaseStatus.RELEASED.value:
        messages.append(
            _checkpoint_message(
                "PARAMETER_CHECKPOINT_ZONE_HANDOVER_NOT_RELEASED",
                "P013-Checkpoint ist nicht freigegeben.",
                "zone_handover.release_status",
            )
        )
    if _handover_release_status(technical_handover.release_status) != ReleaseStatus.RELEASED.value:
        messages.append(
            _checkpoint_message(
                "PARAMETER_CHECKPOINT_TECHNICAL_HANDOVER_NOT_RELEASED",
                "P014-Checkpoint ist nicht freigegeben.",
                "technical_handover.release_status",
            )
        )
    if zone_handover.project_id != input_package.project_id:
        messages.append(
            _checkpoint_message(
                "PARAMETER_CHECKPOINT_PROJECT_MISMATCH",
                "P013-Checkpoint und Eingangspaket gehoeren nicht zum selben Projekt.",
                "zone_handover.project_id",
            )
        )
    if zone_handover.building_id != input_package.building_id:
        messages.append(
            _checkpoint_message(
                "PARAMETER_CHECKPOINT_BUILDING_MISMATCH",
                "P013-Checkpoint und Eingangspaket gehoeren nicht zum selben Gebaeude.",
                "zone_handover.building_id",
            )
        )

    zone_technical_triple = (
        zone_handover.technical_model_id,
        zone_handover.technical_revision_id,
        zone_handover.technical_content_hash,
    )
    technical_triple = (
        technical_handover.technical_model_id,
        technical_handover.revision_id,
        technical_handover.content_hash,
    )
    if zone_technical_triple != technical_triple:
        messages.append(
            _checkpoint_message(
                "PARAMETER_CHECKPOINT_TECHNICAL_TRIPLE_MISMATCH",
                "P013- und P014-Checkpoint referenzieren nicht dieselbe Technikrevision.",
                "zone_handover.technical_revision_id",
            )
        )
    return build_validation_result(tuple(messages))


def parameter_checkpoint_reference_from_released_zone_handover(
    handover: ReleasedZoneHandover,
    *,
    label: str = "Freigegebener P013-Zonencheckpoint",
) -> ParameterSourceReference:
    """Erzeugt eine getrennte, payloadfreie P013-Checkpoint-Referenz."""
    if not isinstance(handover, ReleasedZoneHandover):
        raise TypeError("handover muss ein ReleasedZoneHandover sein.")
    required_values = (
        handover.zone_handover_id,
        handover.revision_id,
        handover.zone_model_id,
        handover.project_id,
        handover.building_id,
        handover.building_revision_id,
        handover.technical_model_id,
        handover.technical_revision_id,
        handover.technical_content_hash,
        handover.content_hash,
    )
    release_status = _handover_release_status(handover.release_status)
    if release_status != ReleaseStatus.RELEASED.value or not all(str(value).strip() for value in required_values):
        raise ValueError("Checkpoint-Referenzen duerfen nur vollstaendige, freigegebene Zonen-Handover uebernehmen.")
    return ParameterSourceReference(
        source_reference_id=f"checkpoint:{handover.zone_handover_id}",
        module_key="ma_zones",
        dataset_key=handover.zone_model_id,
        version_id=handover.revision_id,
        validation_status=release_status,
        label=label,
        reference_id=handover.zone_handover_id,
        reference_version=handover.revision_id,
        content_hash=handover.content_hash,
        freshness_status=FreshnessStatus.CURRENT.value,
    )


def parameter_checkpoint_reference_from_released_technical_handover(
    handover: ReleasedTechnicalHandover,
    *,
    label: str = "Freigegebener P014-v2-Technikcheckpoint",
) -> ParameterSourceReference:
    """Erzeugt eine getrennte, payloadfreie P014-Checkpoint-Referenz."""
    if not isinstance(handover, ReleasedTechnicalHandover):
        raise TypeError("handover muss ein ReleasedTechnicalHandover sein.")
    return parameter_source_reference_from_released_technical_handover(
        handover,
        source_reference_id=(f"checkpoint:ma_technical:{handover.technical_model_id}:{handover.revision_id}"),
        label=label,
    )


def parameter_source_reference_from_released_technical_handover(
    handover: ReleasedTechnicalHandover,
    *,
    source_reference_id: str | None = None,
    label: str = "Freigegebene P014-v2-Technikrevision",
) -> ParameterSourceReference:
    """Uebernimmt nur freigegebene P014-Referenzmetadaten als Parameterquelle.

    Die Funktion ist bewusst kein v1-zu-v2-Konverter fuer Parameterwerte.
    Sie stellt lediglich die nachweisbare Quellenreferenz fuer einen folgenden
    P015-S3b-Eingangspaket-Slice bereit.
    """
    release_status = getattr(handover.release_status, "value", str(handover.release_status))
    required_values = (
        handover.technical_model_id,
        handover.revision_id,
        handover.content_hash,
    )
    if release_status != "released" or not all(str(value).strip() for value in required_values):
        raise ValueError("Parameterquellen duerfen nur vollstaendige, freigegebene Technik-Handover uebernehmen.")

    return ParameterSourceReference(
        source_reference_id=source_reference_id or _source_reference_id("ma_technical", handover.technical_model_id),
        module_key="ma_technical",
        dataset_key=handover.technical_model_id,
        version_id=handover.revision_id,
        validation_status=release_status,
        label=label,
        reference_id=handover.technical_model_id,
        reference_version=handover.revision_id,
        content_hash=handover.content_hash,
        freshness_status=FreshnessStatus.CURRENT.value,
    )


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
            reference_id=building_spec.building.building_id,
            reference_version=building_spec.model_version.version_id,
            content_hash=_stable_hash(
                {
                    "module_key": "ma_building",
                    "dataset_key": building_spec.building.building_id,
                    "version_id": building_spec.model_version.version_id,
                }
            ),
        ),
        ParameterSourceReference(
            source_reference_id=_source_reference_id("ma_zones", zone_spec.zone_model_id),
            module_key="ma_zones",
            dataset_key=zone_spec.zone_model_id,
            version_id=zone_spec.zone_model_id,
            validation_status=zone_status,
            label="BusinessIntegration LoD-1 Zonenmodell",
            reference_id=zone_spec.zone_model_id,
            reference_version=zone_spec.zone_model_id,
            content_hash=_stable_hash(
                {
                    "module_key": "ma_zones",
                    "dataset_key": zone_spec.zone_model_id,
                    "version_id": zone_spec.zone_model_id,
                }
            ),
        ),
        ParameterSourceReference(
            source_reference_id=_source_reference_id("ma_technical", technical_spec.technical_model_id),
            module_key="ma_technical",
            dataset_key=technical_spec.technical_model_id,
            version_id=technical_spec.technical_model_id,
            validation_status=technical_status,
            label="BusinessIntegration LoD-1 Technikmodell",
            reference_id=technical_spec.technical_model_id,
            reference_version=technical_spec.technical_model_id,
            content_hash=_stable_hash(
                {
                    "module_key": "ma_technical",
                    "dataset_key": technical_spec.technical_model_id,
                    "version_id": technical_spec.technical_model_id,
                }
            ),
        ),
    )


def _source_reference_id(module_key: str, version_id: str) -> str:
    return f"{module_key}:{version_id}"


def _baseline_source_reference(source: ParameterSourceReference) -> ParameterSourceReference:
    reference_id = source.reference_id or source.dataset_key
    reference_version = source.reference_version or source.version_id
    content_hash = source.content_hash or _stable_hash(_source_hash_payload(source))
    return ParameterSourceReference(
        source_reference_id=source.source_reference_id,
        module_key=source.module_key,
        dataset_key=source.dataset_key,
        version_id=source.version_id,
        validation_status=source.validation_status,
        label=source.label,
        reference_id=reference_id,
        reference_version=reference_version,
        content_hash=content_hash,
        freshness_status=source.freshness_status or FreshnessStatus.CURRENT.value,
    )


def _checkpoint_message(code: str, message: str, location: str) -> DiagnosticMessage:
    return DiagnosticMessage(DiagnosticSeverity.ERROR, code, message, location)


def _append_missing_checkpoint_fields(
    messages: list[DiagnosticMessage],
    handover: object,
    *,
    field_names: tuple[str, ...],
    location_prefix: str,
) -> None:
    for field_name in field_names:
        if not str(getattr(handover, field_name, "")).strip():
            messages.append(
                _checkpoint_message(
                    "PARAMETER_CHECKPOINT_HANDOVER_FIELD_MISSING",
                    "Released-Checkpoint enthaelt ein unvollstaendiges Referenzfeld.",
                    f"{location_prefix}.{field_name}",
                )
            )


def _handover_release_status(release_status: object) -> str:
    return str(getattr(release_status, "value", release_status)).strip()


def _weather_source_reference(
    dataset: WeatherDataset,
    *,
    weather_status: WeatherDatasetStatus | None,
    weather_activation: WeatherActivationRecord | None,
) -> ParameterSourceReference:
    validation_status = weather_status.release_status.value if weather_status and weather_status.release_status else "unknown"
    version_id = (
        weather_status.import_id
        if weather_status and weather_status.import_id
        else weather_activation.import_id
        if weather_activation and weather_activation.import_id
        else dataset.weather_key
    )
    reference_version = version_id
    content_hash = _stable_hash(
        {
            "module_key": "ma_weather",
            "weather_key": dataset.weather_key,
            "file_path": dataset.file_path.as_posix(),
            "source": dataset.source,
            "location": dataset.location,
            "year_type": dataset.year_type,
            "climate_scenario": dataset.climate_scenario,
            "dataset_role": dataset.dataset_role,
            "file_size_bytes": weather_status.file_size_bytes if weather_status else None,
            "modified_ns": weather_status.modified_ns if weather_status else None,
            "import_id": weather_status.import_id if weather_status else "",
            "source_id": weather_status.source_id if weather_status else "",
        }
    )
    return ParameterSourceReference(
        source_reference_id=_source_reference_id("ma_weather", dataset.weather_key),
        module_key="ma_weather",
        dataset_key=dataset.weather_key,
        version_id=version_id,
        validation_status=validation_status,
        label=dataset.display_name,
        reference_id=dataset.weather_key,
        reference_version=reference_version,
        content_hash=content_hash,
        freshness_status=FreshnessStatus.CURRENT.value,
    )


def _baseline_release_status_from_input_package(input_package: ParameterInputPackage) -> str:
    if input_package.requires_weather and (
        "ma_weather" not in input_package.source_modules
        or not input_package.weather_activated
    ):
        return "blocked"
    if any(source.validation_status != "released" for source in input_package.source_references):
        return "blocked"
    if not _released_checkpoint_references_are_valid(
        input_package.checkpoint_references,
        requires_released_checkpoints=input_package.requires_released_checkpoints,
    ):
        return "blocked"
    return "released"


def _released_checkpoint_references_are_valid(
    checkpoint_references: tuple[ParameterSourceReference, ...],
    *,
    requires_released_checkpoints: bool,
) -> bool:
    """Spiegelt die Freigabekriterien fuer die Baseline-Statusableitung."""
    if not checkpoint_references:
        return not requires_released_checkpoints

    required_fields = (
        "source_reference_id",
        "module_key",
        "dataset_key",
        "version_id",
        "validation_status",
        "reference_id",
        "reference_version",
        "content_hash",
        "freshness_status",
    )
    if any(
        not all(str(getattr(reference, field_name)).strip() for field_name in required_fields)
        or reference.validation_status != ReleaseStatus.RELEASED.value
        or reference.freshness_status != FreshnessStatus.CURRENT.value
        for reference in checkpoint_references
    ):
        return False
    if not requires_released_checkpoints:
        return True
    return (
        len(checkpoint_references) == 2
        and {reference.module_key for reference in checkpoint_references} == {"ma_zones", "ma_technical"}
        and len({reference.source_reference_id for reference in checkpoint_references}) == 2
    )


def _weather_parameter_values(
    dataset: WeatherDataset,
    source_reference: ParameterSourceReference,
    *,
    weather_status: WeatherDatasetStatus | None,
) -> tuple[ParameterValue, ...]:
    rows: list[tuple[str, str, object]] = [
        ("weather.weather_key", "Wetterdatensatz", dataset.weather_key),
        ("weather.display_name", "Wetterdatensatz-Anzeige", dataset.display_name),
        ("weather.location", "Wetterstandort", dataset.location),
        ("weather.year_type", "Wetterjahrtyp", dataset.year_type),
        ("weather.source", "Wetterquelle", dataset.source),
        ("weather.file_path", "Wetterdatei", dataset.file_path.as_posix()),
    ]
    optional_rows = (
        ("weather.dataset_role", "Wetterdatensatzrolle", dataset.dataset_role),
        ("weather.climate_scenario", "Klimaszenario", dataset.climate_scenario),
        ("weather.location_id", "Wetter-Orts-ID", dataset.location_id),
        ("weather.reference_location_id", "TRY-Referenzstandort", dataset.reference_location_id),
        ("weather.import_id", "Wetterimport-ID", weather_status.import_id if weather_status else ""),
        ("weather.source_id", "Wetterquellen-ID", weather_status.source_id if weather_status else ""),
    )
    rows.extend((key, label, value) for key, label, value in optional_rows if str(value).strip())
    return tuple(
        ParameterValue(
            parameter_key=key,
            label=label,
            value=value,
            unit="dimensionless",
            source_reference_id=source_reference.source_reference_id,
            status="released",
        )
        for key, label, value in rows
    )


def _baseline_parameter_value(
    snapshot: ParameterSnapshot | ParameterInputPackage,
    value: ParameterValue,
    *,
    source_reference_id: str,
) -> BaselineParameterValue:
    scope = _scope_for_parameter_value(snapshot, value)
    payload = {
        "parameter_key": value.parameter_key,
        "value": value.value,
        "unit": value.unit,
        "scope_type": scope.scope_type.value,
        "scope_id": scope.scope_id,
        "source_reference_id": value.source_reference_id,
    }
    return BaselineParameterValue(
        parameter_value_id=f"PV-{_stable_hash(payload)[:16]}",
        parameter_key=value.parameter_key,
        label=value.label,
        value=value.value,
        unit=value.unit,
        scope=scope,
        parameter_class=_parameter_class_for_value(value),
        variability=_variability_for_value(value),
        source_reference_id=source_reference_id,
        reference_id=scope.scope_id,
        reference_version=value.source_reference_id,
        content_hash=_stable_hash(payload),
        status=value.status,
    )


def _scope_for_parameter_value(snapshot: ParameterSnapshot | ParameterInputPackage, value: ParameterValue) -> ParameterScope:
    key = value.parameter_key
    if "." in key:
        object_id, field_key = key.split(".", maxsplit=1)
        if object_id == "weather":
            return ParameterScope(ParameterScopeType.PROJECT, snapshot.project_id, "Wetterdatensatz")
        if object_id.startswith("ZONE-"):
            return ParameterScope(ParameterScopeType.ZONE, object_id, "Thermische Zone")
        if object_id.startswith("TECH-"):
            return ParameterScope(ParameterScopeType.TECHNICAL_SYSTEM, object_id, "Technisches System")
        if object_id.startswith("USE-"):
            return ParameterScope(ParameterScopeType.ZONE_GROUP, object_id, "Nutzungsprofil")
        return ParameterScope(ParameterScopeType.BUILDING, snapshot.building_id, field_key)

    if key.startswith("zone_"):
        return ParameterScope(ParameterScopeType.ZONE_GROUP, "all_zones", "Alle thermischen Zonen")
    return ParameterScope(ParameterScopeType.BUILDING, snapshot.building_id, "Gebaeude")


def _parameter_class_for_value(value: ParameterValue) -> ParameterClass:
    key = value.parameter_key
    if key.startswith("weather."):
        return ParameterClass.PRIMARY_REFERENCE
    derived_keys = {
        "floor_area_m2",
        "zone_count",
        "zone_floor_area_m2",
        "zone_volume_m3",
        "technical_system_count",
    }
    if key in derived_keys or key.endswith(".estimated_design_power_w"):
        return ParameterClass.PRIMARY_DERIVED
    return ParameterClass.PRIMARY_DIRECT


def _variability_for_value(value: ParameterValue) -> ParameterVariability:
    key = value.parameter_key
    if key.startswith("weather."):
        return ParameterVariability.REFERENCE_VARIABLE
    direct_variable_keys = {
        "external_wall_u_value_w_m2k",
        "window_u_value_w_m2k",
        "window_area_ratio_percent",
    }
    direct_variable_suffixes = (
        ".heating_setpoint_c",
        ".cooling_setpoint_c",
        ".minimum_air_change_rate_1_h",
        ".occupancy_density_m2_per_person",
        ".lighting_power_w_m2",
        ".equipment_power_w_m2",
        ".design_power_w_m2",
        ".air_change_rate_1_h",
        ".performance_factor",
    )
    if key in direct_variable_keys or key.endswith(direct_variable_suffixes):
        return ParameterVariability.DIRECT_VARIABLE
    if key in {"building_length_m", "building_width_m", "building_height_m"}:
        return ParameterVariability.STRUCTURAL_VARIABLE
    return ParameterVariability.NOT_VARIABLE


def _stable_hash(payload: object) -> str:
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _baseline_value_hash_payload(value: BaselineParameterValue) -> dict[str, object]:
    return {
        "parameter_value_id": value.parameter_value_id,
        "parameter_key": value.parameter_key,
        "value": value.value,
        "unit": value.unit,
        "scope_type": value.scope.scope_type.value,
        "scope_id": value.scope.scope_id,
        "parameter_class": value.parameter_class.value,
        "variability": value.variability.value,
        "source_reference_id": value.source_reference_id,
    }


def _source_hash_payload(source: ParameterSourceReference) -> dict[str, object]:
    return {
        "source_reference_id": source.source_reference_id,
        "module_key": source.module_key,
        "dataset_key": source.dataset_key,
        "version_id": source.version_id,
        "validation_status": source.validation_status,
        "reference_id": source.reference_id,
        "reference_version": source.reference_version,
    }


def _checkpoint_hash_payload(reference: ParameterSourceReference) -> dict[str, object]:
    """Liefert die vollstaendige, hashrelevante Referenz eines Checkpoints."""
    return {
        **_source_hash_payload(reference),
        "content_hash": reference.content_hash,
        "freshness_status": reference.freshness_status,
    }
