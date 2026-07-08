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

from .models import ParameterSnapshot

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


def validate_parameter_snapshot(snapshot: ParameterSnapshot) -> ValidationResult:
    """Prueft einen ParameterSnapshot und erzeugt ein gemeinsames ValidationResult."""
    messages: list[DiagnosticMessage] = []
    messages.extend(_validate_header(snapshot))
    messages.extend(_validate_object_ids(snapshot))
    messages.extend(_validate_sources(snapshot))
    messages.extend(_validate_values(snapshot))
    messages.extend(_validate_lod1_required_values(snapshot))
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
