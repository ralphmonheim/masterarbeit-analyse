"""Fachliche Validierung fuer ParameterSnapshot v1."""

from __future__ import annotations

import math
from collections import defaultdict

from ma_validation import (
    DiagnosticMessage,
    DiagnosticSeverity,
    ReleaseStatus,
    ValidationResult,
    build_validation_result,
)

from .models import (
    BASELINE_SNAPSHOT_SCHEMA_VERSION,
    INPUT_PACKAGE_SCHEMA_VERSION,
    BaselineParameterSnapshot,
    FreshnessStatus,
    ParameterInputPackage,
    ParameterSnapshot,
)

REQUIRED_LOD1_PARAMETER_KEYS = frozenset(
    {
        "building_length_m",
        "building_width_m",
        "building_height_m",
        "external_wall_u_value_w_m2k",
        "window_u_value_w_m2k",
        "window_area_ratio_percent",
        "floor_area_m2",
        "zone_count",
        "zone_floor_area_m2",
        "zone_volume_m3",
        "technical_system_count",
    }
)
REQUIRED_SOURCE_MODULES = frozenset({"ma_building", "ma_zones", "ma_technical"})
REQUIRED_INPUT_PACKAGE_SOURCE_MODULES = frozenset({"ma_building", "ma_zones", "ma_technical"})
REQUIRED_WEATHER_PARAMETER_KEYS = frozenset({"weather.weather_key", "weather.location", "weather.year_type"})
ALLOWED_BASELINE_RELEASE_STATUSES = frozenset(
    {"draft", "validation_required", "review_required", "released", "blocked", "archived"}
)


def validate_parameter_snapshot(snapshot: ParameterSnapshot) -> ValidationResult:
    """Prueft einen ParameterSnapshot und erzeugt ein gemeinsames ValidationResult."""
    messages: list[DiagnosticMessage] = []
    messages.extend(_validate_header(snapshot))
    messages.extend(_validate_object_ids(snapshot))
    messages.extend(_validate_sources(snapshot))
    messages.extend(_validate_values(snapshot))
    messages.extend(_validate_lod1_required_values(snapshot))
    return build_validation_result(tuple(messages))


def validate_baseline_parameter_snapshot(snapshot: BaselineParameterSnapshot) -> ValidationResult:
    """Prueft den BaselineParameterSnapshot v2 fuer die kontrollierte Weitergabe."""
    messages: list[DiagnosticMessage] = []
    messages.extend(_validate_baseline_header(snapshot))
    messages.extend(_validate_baseline_object_ids(snapshot))
    messages.extend(_validate_baseline_sources(snapshot))
    messages.extend(_validate_baseline_reference_versions(snapshot))
    messages.extend(_validate_baseline_values(snapshot))
    messages.extend(_validate_baseline_scoped_keys(snapshot))
    return build_validation_result(tuple(messages))


def validate_parameter_input_package(input_package: ParameterInputPackage) -> ValidationResult:
    """Prueft das P015-S3a-Eingangspaket vor Baseline- und Folgerechnung."""
    messages: list[DiagnosticMessage] = []
    messages.extend(_validate_input_package_header(input_package))
    messages.extend(_validate_input_package_object_ids(input_package))
    messages.extend(_validate_input_package_sources(input_package))
    messages.extend(_validate_input_package_values(input_package))
    messages.extend(_validate_input_package_lod1_required_values(input_package))
    return build_validation_result(tuple(messages))


def _message(
    severity: DiagnosticSeverity,
    code: str,
    message: str,
    location: str,
) -> DiagnosticMessage:
    return DiagnosticMessage(severity=severity, code=code, message=message, location=location)


def _validate_header(snapshot: ParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    required_values = {
        "schema_version": snapshot.schema_version,
        "snapshot_id": snapshot.snapshot_id,
        "snapshot_version": snapshot.snapshot_version,
        "project_id": snapshot.project_id,
        "building_id": snapshot.building_id,
        "input_detail_level": snapshot.input_detail_level,
    }
    for location, value in required_values.items():
        if not str(value).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_SNAPSHOT_REQUIRED_FIELD_MISSING",
                    "Pflichtfeld des ParameterSnapshot fehlt.",
                    location,
                )
            )
    return messages


def _validate_baseline_header(snapshot: BaselineParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    required_values = {
        "schema_version": snapshot.schema_version,
        "snapshot_id": snapshot.snapshot_id,
        "snapshot_version": snapshot.snapshot_version,
        "project_id": snapshot.project_id,
        "building_id": snapshot.building_id,
        "building_detail_mode": snapshot.building_detail_mode.value,
        "content_hash": snapshot.content_hash,
        "release_status": snapshot.release_status,
        "freshness_status": snapshot.freshness_status.value,
    }
    for location, value in required_values.items():
        if not str(value).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BASELINE_REQUIRED_FIELD_MISSING",
                    "Pflichtfeld des BaselineParameterSnapshot fehlt.",
                    location,
                )
            )

    if snapshot.schema_version != BASELINE_SNAPSHOT_SCHEMA_VERSION:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BASELINE_SCHEMA_VERSION_UNSUPPORTED",
                "BaselineParameterSnapshot nutzt eine nicht unterstuetzte Schema-Version.",
                "schema_version",
            )
        )
    if snapshot.release_status not in ALLOWED_BASELINE_RELEASE_STATUSES:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BASELINE_RELEASE_STATUS_UNKNOWN",
                f"Unbekannter Baseline-Freigabestatus: {snapshot.release_status}",
                "release_status",
            )
        )
    elif snapshot.release_status == "blocked":
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BASELINE_RELEASE_STATUS_BLOCKED",
                "Blockierte Baseline-Snapshots duerfen nicht weitergegeben werden.",
                "release_status",
            )
        )
    elif snapshot.release_status != "released":
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "BASELINE_RELEASE_STATUS_NOT_RELEASED",
                "Baseline-Snapshot ist noch nicht freigegeben.",
                "release_status",
            )
        )

    if snapshot.freshness_status is not FreshnessStatus.CURRENT:
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "BASELINE_FRESHNESS_NOT_CURRENT",
                "Baseline-Snapshot ist nicht als aktuell markiert.",
                "freshness_status",
            )
        )
    return messages


def _validate_input_package_header(input_package: ParameterInputPackage) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    required_values = {
        "schema_version": input_package.schema_version,
        "package_id": input_package.package_id,
        "package_version": input_package.package_version,
        "project_id": input_package.project_id,
        "building_id": input_package.building_id,
        "input_detail_level": input_package.input_detail_level,
        "source_snapshot_id": input_package.source_snapshot_id,
        "source_snapshot_version": input_package.source_snapshot_version,
    }
    for location, value in required_values.items():
        if not str(value).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_REQUIRED_FIELD_MISSING",
                    "Pflichtfeld des Parameter-Eingangspakets fehlt.",
                    location,
                )
            )

    if input_package.schema_version != INPUT_PACKAGE_SCHEMA_VERSION:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_INPUT_SCHEMA_VERSION_UNSUPPORTED",
                "Parameter-Eingangspaket nutzt eine nicht unterstuetzte Schema-Version.",
                "schema_version",
            )
        )
    return messages


def _validate_object_ids(snapshot: ParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    locations_by_id: dict[str, list[str]] = defaultdict(list)
    for object_id, location in snapshot.object_id_locations():
        if not object_id:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_OBJECT_ID_MISSING",
                    "Eine Snapshot-ID, Quellen-ID oder Parameter-ID ist leer.",
                    location,
                )
            )
            continue
        locations_by_id[object_id].append(location)

    for object_id, locations in locations_by_id.items():
        if len(locations) > 1:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_OBJECT_ID_DUPLICATE",
                    f"ID ist mehrfach vergeben: {object_id}",
                    ", ".join(locations),
                )
            )
    return messages


def _validate_input_package_object_ids(input_package: ParameterInputPackage) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    locations_by_id: dict[str, list[str]] = defaultdict(list)
    for object_id, location in input_package.object_id_locations():
        if not object_id:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_OBJECT_ID_MISSING",
                    "Eine Paket-ID, Quellen-ID oder Parameter-ID ist leer.",
                    location,
                )
            )
            continue
        locations_by_id[object_id].append(location)

    for object_id, locations in locations_by_id.items():
        if len(locations) > 1:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_OBJECT_ID_DUPLICATE",
                    f"ID ist mehrfach vergeben: {object_id}",
                    ", ".join(locations),
                )
            )
    return messages


def _validate_baseline_object_ids(snapshot: BaselineParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    locations_by_id: dict[str, list[str]] = defaultdict(list)
    for object_id, location in snapshot.object_id_locations():
        if not object_id:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BASELINE_OBJECT_ID_MISSING",
                    "Eine Baseline-ID, Quellen-ID, Referenz-ID oder Parameterwert-ID ist leer.",
                    location,
                )
            )
            continue
        locations_by_id[object_id].append(location)

    for object_id, locations in locations_by_id.items():
        if len(locations) > 1:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BASELINE_OBJECT_ID_DUPLICATE",
                    f"ID ist mehrfach vergeben: {object_id}",
                    ", ".join(locations),
                )
            )
    return messages


def _validate_sources(snapshot: ParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not snapshot.source_references:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_SOURCES_MISSING",
                "ParameterSnapshot benoetigt mindestens eine Quellenreferenz.",
                "source_references",
            )
        )
        return messages

    modules = {source.module_key for source in snapshot.source_references}
    missing_modules = sorted(REQUIRED_SOURCE_MODULES - modules)
    if missing_modules:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_REQUIRED_SOURCE_MISSING",
                f"Erforderliche Quellenmodule fehlen: {', '.join(missing_modules)}",
                "source_references",
            )
        )

    for index, source in enumerate(snapshot.source_references):
        for field_name in ("source_reference_id", "module_key", "dataset_key", "version_id", "validation_status"):
            if not str(getattr(source, field_name)).strip():
                messages.append(
                    _message(
                        DiagnosticSeverity.ERROR,
                        "PARAMETER_SOURCE_FIELD_MISSING",
                        "Quellenreferenzen benoetigen ID, Modul, Datensatz, Version und Validierungsstatus.",
                        f"source_references.{index}.{field_name}",
                    )
                )
        if source.validation_status != ReleaseStatus.RELEASED.value:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_SOURCE_NOT_RELEASED",
                    "ParameterSnapshot darf nur freigegebene Fachquellen uebernehmen.",
                    f"source_references.{index}.validation_status",
                )
            )
    return messages


def _validate_input_package_sources(input_package: ParameterInputPackage) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not input_package.source_references:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_INPUT_SOURCES_MISSING",
                "Parameter-Eingangspaket benoetigt mindestens eine Quellenreferenz.",
                "source_references",
            )
        )
        return messages

    modules = input_package.source_modules
    missing_modules = sorted(REQUIRED_INPUT_PACKAGE_SOURCE_MODULES - modules)
    if missing_modules:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_INPUT_REQUIRED_SOURCE_MISSING",
                f"Erforderliche Quellenmodule fehlen: {', '.join(missing_modules)}",
                "source_references",
            )
        )

    has_weather_source = "ma_weather" in modules
    if input_package.requires_weather and not has_weather_source:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_INPUT_WEATHER_SOURCE_MISSING",
                "Eingangspaket benoetigt einen aktivierten Wetterdatensatz als Quelle.",
                "source_references",
            )
        )
    if has_weather_source and not input_package.weather_activated:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_INPUT_WEATHER_NOT_ACTIVATED",
                "Wetterquelle darf erst nach bewusster Projekt-Default-Aktivierung uebergeben werden.",
                "weather_activated",
            )
        )

    for index, source in enumerate(input_package.source_references):
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
        for field_name in required_fields:
            if not str(getattr(source, field_name)).strip():
                messages.append(
                    _message(
                        DiagnosticSeverity.ERROR,
                        "PARAMETER_INPUT_SOURCE_FIELD_MISSING",
                        "Eingangspaket-Quellen benoetigen ID, Modul, Version, Referenz und Hash.",
                        f"source_references.{index}.{field_name}",
                    )
                )
        if source.validation_status != ReleaseStatus.RELEASED.value:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_SOURCE_NOT_RELEASED",
                    "Eingangspakete duerfen nur freigegebene Fachquellen uebernehmen.",
                    f"source_references.{index}.validation_status",
                )
            )
        if source.freshness_status != FreshnessStatus.CURRENT.value:
            messages.append(
                _message(
                    DiagnosticSeverity.WARNING,
                    "PARAMETER_INPUT_SOURCE_NOT_CURRENT",
                    "Quellenreferenz ist nicht als aktuell markiert.",
                    f"source_references.{index}.freshness_status",
                )
            )
    return messages


def _validate_baseline_sources(snapshot: BaselineParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not snapshot.source_references:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BASELINE_SOURCES_MISSING",
                "BaselineParameterSnapshot benoetigt mindestens eine Quellenreferenz.",
                "source_references",
            )
        )
        return messages

    modules = {source.module_key for source in snapshot.source_references}
    missing_modules = sorted(REQUIRED_SOURCE_MODULES - modules)
    if missing_modules:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BASELINE_REQUIRED_SOURCE_MISSING",
                f"Erforderliche Quellenmodule fehlen: {', '.join(missing_modules)}",
                "source_references",
            )
        )

    for index, source in enumerate(snapshot.source_references):
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
        for field_name in required_fields:
            if not str(getattr(source, field_name)).strip():
                messages.append(
                    _message(
                        DiagnosticSeverity.ERROR,
                        "BASELINE_SOURCE_FIELD_MISSING",
                        "Baseline-Quellenreferenzen benoetigen ID, Modul, Version, Referenz und Hash.",
                        f"source_references.{index}.{field_name}",
                    )
                )
        if source.validation_status != ReleaseStatus.RELEASED.value:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BASELINE_SOURCE_NOT_RELEASED",
                    "Baseline-Snapshots duerfen nur freigegebene Fachquellen uebernehmen.",
                    f"source_references.{index}.validation_status",
                )
            )
        if source.freshness_status != FreshnessStatus.CURRENT.value:
            messages.append(
                _message(
                    DiagnosticSeverity.WARNING,
                    "BASELINE_SOURCE_NOT_CURRENT",
                    "Quellenreferenz ist nicht als aktuell markiert.",
                    f"source_references.{index}.freshness_status",
                )
            )
    return messages


def _validate_baseline_reference_versions(snapshot: BaselineParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not snapshot.reference_versions:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BASELINE_REFERENCE_VERSIONS_MISSING",
                "BaselineParameterSnapshot benoetigt versionierte Fachobjektreferenzen.",
                "reference_versions",
            )
        )
        return messages

    for index, reference in enumerate(snapshot.reference_versions):
        for field_name in ("reference_id", "reference_version", "content_hash", "source_reference_id"):
            if not str(getattr(reference, field_name)).strip():
                messages.append(
                    _message(
                        DiagnosticSeverity.ERROR,
                        "BASELINE_REFERENCE_FIELD_MISSING",
                        "Referenzversionen benoetigen ID, Version, Hash und Quellenbezug.",
                        f"reference_versions.{index}.{field_name}",
                    )
                )
        if reference.source_reference_id not in snapshot.source_reference_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BASELINE_REFERENCE_SOURCE_UNKNOWN",
                    f"Referenzversion verweist auf unbekannte Quelle: {reference.source_reference_id}",
                    f"reference_versions.{index}.source_reference_id",
                )
            )
    return messages


def _validate_values(snapshot: ParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not snapshot.values:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_VALUES_MISSING",
                "ParameterSnapshot benoetigt mindestens einen Parameterwert.",
                "values",
            )
        )
        return messages

    for index, value in enumerate(snapshot.values):
        if not str(value.parameter_key).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_KEY_MISSING",
                    "Parameterwerte benoetigen einen Schluessel.",
                    f"values.{index}.parameter_key",
                )
            )
        if not str(value.label).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_LABEL_MISSING",
                    "Parameterwerte benoetigen eine lesbare Bezeichnung.",
                    f"values.{index}.label",
                )
            )
        if not str(value.unit).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_UNIT_MISSING",
                    "Parameterwerte benoetigen eine Einheit oder 'dimensionless'.",
                    f"values.{index}.unit",
                )
            )
        if value.source_reference_id not in snapshot.source_reference_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_SOURCE_UNKNOWN",
                    f"Parameterwert verweist auf unbekannte Quelle: {value.source_reference_id}",
                    f"values.{index}.source_reference_id",
                )
            )
        if value.value is None or str(value.value).strip() == "":
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_VALUE_MISSING",
                    "Parameterwerte duerfen nicht leer sein.",
                    f"values.{index}.value",
                )
            )
        if isinstance(value.value, int | float) and not isinstance(value.value, bool) and not math.isfinite(value.value):
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_VALUE_INVALID",
                    "Numerische Parameterwerte muessen endlich sein.",
                    f"values.{index}.value",
                )
            )
    return messages


def _validate_input_package_values(input_package: ParameterInputPackage) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not input_package.values:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_INPUT_VALUES_MISSING",
                "Parameter-Eingangspaket benoetigt mindestens einen Parameterwert.",
                "values",
            )
        )
        return messages

    for index, value in enumerate(input_package.values):
        if not str(value.parameter_key).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_KEY_MISSING",
                    "Eingangspaket-Werte benoetigen einen Schluessel.",
                    f"values.{index}.parameter_key",
                )
            )
        if not str(value.label).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_LABEL_MISSING",
                    "Eingangspaket-Werte benoetigen eine lesbare Bezeichnung.",
                    f"values.{index}.label",
                )
            )
        if not str(value.unit).strip():
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_UNIT_MISSING",
                    "Eingangspaket-Werte benoetigen eine Einheit oder 'dimensionless'.",
                    f"values.{index}.unit",
                )
            )
        if value.source_reference_id not in input_package.source_reference_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_VALUE_SOURCE_UNKNOWN",
                    f"Eingangspaket-Wert verweist auf unbekannte Quelle: {value.source_reference_id}",
                    f"values.{index}.source_reference_id",
                )
            )
        if value.value is None or str(value.value).strip() == "":
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_VALUE_MISSING",
                    "Eingangspaket-Werte duerfen nicht leer sein.",
                    f"values.{index}.value",
                )
            )
        if isinstance(value.value, int | float) and not isinstance(value.value, bool) and not math.isfinite(value.value):
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_VALUE_INVALID",
                    "Numerische Eingangspaket-Werte muessen endlich sein.",
                    f"values.{index}.value",
                )
            )
    return messages


def _validate_baseline_values(snapshot: BaselineParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if not snapshot.parameter_values:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "BASELINE_VALUES_MISSING",
                "BaselineParameterSnapshot benoetigt mindestens einen Parameterwert.",
                "parameter_values",
            )
        )
        return messages

    for index, value in enumerate(snapshot.parameter_values):
        required_values = {
            "parameter_value_id": value.parameter_value_id,
            "parameter_key": value.parameter_key,
            "label": value.label,
            "unit": value.unit,
            "scope.scope_id": value.scope.scope_id,
            "source_reference_id": value.source_reference_id,
            "content_hash": value.content_hash,
            "status": value.status,
        }
        for field_name, field_value in required_values.items():
            if not str(field_value).strip():
                messages.append(
                    _message(
                        DiagnosticSeverity.ERROR,
                        "BASELINE_VALUE_FIELD_MISSING",
                        "Baseline-Parameterwerte benoetigen ID, Key, Scope, Quelle, Einheit und Hash.",
                        f"parameter_values.{index}.{field_name}",
                    )
                )
        if value.source_reference_id not in snapshot.source_reference_ids:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BASELINE_VALUE_SOURCE_UNKNOWN",
                    f"Baseline-Wert verweist auf unbekannte Quelle: {value.source_reference_id}",
                    f"parameter_values.{index}.source_reference_id",
                )
            )
        if value.value is None or str(value.value).strip() == "":
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BASELINE_VALUE_MISSING",
                    "Baseline-Parameterwerte duerfen nicht leer sein.",
                    f"parameter_values.{index}.value",
                )
            )
        if isinstance(value.value, int | float) and not isinstance(value.value, bool) and not math.isfinite(value.value):
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BASELINE_VALUE_INVALID",
                    "Numerische Baseline-Parameterwerte muessen endlich sein.",
                    f"parameter_values.{index}.value",
                )
            )
    return messages


def _validate_input_package_lod1_required_values(input_package: ParameterInputPackage) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if input_package.input_detail_level != "LOD-1":
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "PARAMETER_INPUT_DETAIL_LEVEL_UNEXPECTED",
                "Parameter-Eingangspaket ist fuer die BusinessIntegration-LoD-1-Kette ausgelegt.",
                "input_detail_level",
            )
        )
        return messages

    missing_keys = sorted(REQUIRED_LOD1_PARAMETER_KEYS - input_package.parameter_keys)
    if missing_keys:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_INPUT_REQUIRED_KEY_MISSING",
                f"Erforderliche LoD-1-Parameter fehlen: {', '.join(missing_keys)}",
                "values",
            )
        )

    if input_package.requires_weather:
        missing_weather_keys = sorted(REQUIRED_WEATHER_PARAMETER_KEYS - input_package.parameter_keys)
        if missing_weather_keys:
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "PARAMETER_INPUT_WEATHER_KEY_MISSING",
                    f"Erforderliche Wetter-Parameter fehlen: {', '.join(missing_weather_keys)}",
                    "values",
                )
            )
    return messages


def _validate_baseline_scoped_keys(snapshot: BaselineParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    locations_by_key: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for index, value in enumerate(snapshot.parameter_values):
        scoped_key = (value.parameter_key, value.scope.scope_type.value, value.scope.scope_id)
        locations_by_key[scoped_key].append(f"parameter_values.{index}")

    for scoped_key, locations in locations_by_key.items():
        if len(locations) > 1:
            parameter_key, scope_type, scope_id = scoped_key
            messages.append(
                _message(
                    DiagnosticSeverity.ERROR,
                    "BASELINE_SCOPED_PARAMETER_DUPLICATE",
                    f"Parameter ist im gleichen Scope mehrfach vorhanden: {parameter_key} / {scope_type} / {scope_id}",
                    ", ".join(locations),
                )
            )
    return messages


def _validate_lod1_required_values(snapshot: ParameterSnapshot) -> list[DiagnosticMessage]:
    messages: list[DiagnosticMessage] = []
    if snapshot.input_detail_level != "LOD-1":
        messages.append(
            _message(
                DiagnosticSeverity.WARNING,
                "PARAMETER_INPUT_DETAIL_LEVEL_UNEXPECTED",
                "ParameterSnapshot v1 ist fuer die BusinessIntegration-LoD-1-Kette ausgelegt.",
                "input_detail_level",
            )
        )
        return messages

    missing_keys = sorted(REQUIRED_LOD1_PARAMETER_KEYS - snapshot.parameter_keys)
    if missing_keys:
        messages.append(
            _message(
                DiagnosticSeverity.ERROR,
                "PARAMETER_REQUIRED_KEY_MISSING",
                f"Erforderliche LoD-1-Parameter fehlen: {', '.join(missing_keys)}",
                "values",
            )
        )
    return messages
