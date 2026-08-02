"""Deterministische, einwegige Legacy-v1-zu-v2-Ueberfuehrung.

Der Adapter bildet nur zentrale Systemrollen ab. Direkte Zonenbezuge und
zahlenbasierte Legacykennwerte sind keine v2-Dimensionierungseingaben; sie
bleiben deshalb als sichtbare Annahmen erhalten.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

from ma_core import InputSource, InputSourceKind

from .enums import (
    CapacityMode,
    ComponentAvailability,
    TechnicalMedium,
    TechnicalRepresentationMode,
    TechnicalServiceType,
)
from .equipment import PhysicalEquipment
from .metadata import ObjectReference, SourceMetadata, TechnicalAssumption
from .models import ReferenceTechnicalSystem, TechnicalSystemSpecification
from .specification import TechnicalModelSchemaVersion, TechnicalModelSpecification
from .topology import TechnicalServiceInterface

LEGACY_V1_TO_V2_MAPPING_VERSION = "legacy-v1-to-v2-1"
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
_REPO_RELATIVE_PATH_PATTERN = re.compile(r"[^\\/]+")
_ADAPTER_TIMESTAMP = datetime(1970, 1, 1, tzinfo=UTC)


def adapt_legacy_v1_to_v2(
    legacy_specification: TechnicalSystemSpecification,
    *,
    technical_model_id: str,
    project_id: str,
    building_reference: ObjectReference,
    legacy_source_reference: str,
    legacy_source_sha256: str,
    mapping_version: str = LEGACY_V1_TO_V2_MAPPING_VERSION,
) -> TechnicalModelSpecification:
    """Erstellt einen reproduzierbaren, projektgebundenen v2-Entwurf.

    ``legacy_source_reference`` ist bewusst ein repo-relativer Nachweis, zum
    Beispiel ``config/ma_technical/examples/example.yaml``. Der SHA-256-Wert
    muss vom aufrufenden Loader aus genau dieser Quelle stammen.
    """
    if not isinstance(legacy_specification, TechnicalSystemSpecification):
        raise TypeError("legacy_specification muss eine TechnicalSystemSpecification sein.")
    _required_text(technical_model_id, "technical_model_id")
    _required_text(project_id, "project_id")
    if not isinstance(building_reference, ObjectReference):
        raise TypeError("building_reference muss eine ObjectReference sein.")
    _required_text(building_reference.object_id, "building_reference.object_id")
    _required_text(building_reference.revision_id, "building_reference.revision_id")
    source_path = _repo_relative_path(legacy_source_reference)
    source_sha256 = _sha256(legacy_source_sha256)
    _required_text(mapping_version, "mapping_version")

    equipment_register = tuple(
        _equipment_from_legacy(system, technical_model_id, index)
        for index, system in enumerate(legacy_specification.systems, start=1)
    )
    service_interfaces = tuple(
        _service_interface_from_legacy(system, technical_model_id, index)
        for index, system in enumerate(legacy_specification.systems, start=1)
    )
    assumptions = _legacy_assumptions(
        legacy_specification,
        technical_model_id=technical_model_id,
        mapping_version=mapping_version,
        source_sha256=source_sha256,
    )
    return TechnicalModelSpecification(
        schema_version=TechnicalModelSchemaVersion.V2.value,
        technical_model_id=technical_model_id,
        project_id=project_id,
        building_reference=building_reference,
        declared_detail_level=legacy_specification.input_detail_level,
        equipment_register=equipment_register,
        service_interfaces=service_interfaces,
        assumptions=assumptions,
        source_metadata=SourceMetadata(
            source_type="legacy_v1_adapter",
            source_reference=source_path.as_posix(),
            source_version=f"sha256:{source_sha256}; mapping:{mapping_version}",
            imported_or_entered_at=_ADAPTER_TIMESTAMP,
            notes=(
                f"Legacy-Modell {legacy_specification.technical_model_id}; "
                "served_zone_ids wurden nicht in v2 uebernommen."
            ),
            input_source=InputSource(
                module_key="ma_technical",
                source_kind=InputSourceKind.DEMO,
                data_format="yaml",
                source_path=source_path,
                adapter_key=mapping_version,
                is_template=True,
                sha256=source_sha256,
                source_id=f"legacy-v1-{source_sha256[:16]}",
                loaded_at=_ADAPTER_TIMESTAMP,
            ),
        ),
    )


def _equipment_from_legacy(
    system: ReferenceTechnicalSystem,
    technical_model_id: str,
    index: int,
) -> PhysicalEquipment:
    return PhysicalEquipment(
        equipment_id=f"{technical_model_id}-EQUIPMENT-{index:03d}",
        equipment_type=f"legacy_{system.system_type}_system",
        availability=ComponentAvailability.PLANNED,
        representation_mode=TechnicalRepresentationMode.ASSUMED,
        input_detail_level="LOD-1",
        supported_services=(system.system_type,),
    )


def _service_interface_from_legacy(
    system: ReferenceTechnicalSystem,
    technical_model_id: str,
    index: int,
) -> TechnicalServiceInterface:
    service_type, medium = _service_type_and_medium(system.system_type)
    equipment_id = f"{technical_model_id}-EQUIPMENT-{index:03d}"
    return TechnicalServiceInterface(
        interface_id=f"{technical_model_id}-SERVICE-{service_type.value.upper()}-{index:03d}",
        service_type=service_type,
        source_system_reference=ObjectReference(equipment_id, object_type="PhysicalEquipment"),
        medium=medium,
        capacity_mode=CapacityMode.ASSUMED,
        compatible_terminal_types=(),
        availability=ComponentAvailability.PLANNED,
    )


def _service_type_and_medium(system_type: str) -> tuple[TechnicalServiceType, TechnicalMedium]:
    if system_type == "heating":
        return TechnicalServiceType.HEATING, TechnicalMedium.WATER
    if system_type == "cooling":
        return TechnicalServiceType.COOLING, TechnicalMedium.WATER
    if system_type == "ventilation":
        return TechnicalServiceType.SUPPLY_AIR, TechnicalMedium.AIR
    raise ValueError(f"Legacy-Systemtyp kann nicht nach v2 ueberfuehrt werden: {system_type}")


def _legacy_assumptions(
    specification: TechnicalSystemSpecification,
    *,
    technical_model_id: str,
    mapping_version: str,
    source_sha256: str,
) -> tuple[TechnicalAssumption, ...]:
    assumptions = [
        TechnicalAssumption(
            assumption_id=f"{technical_model_id}-ASSUMPTION-001",
            text=(
                f"Einwegmigration aus Legacy-Modell {specification.technical_model_id}; "
                f"Mapping {mapping_version}; Quellen-SHA-256 {source_sha256}."
            ),
            location="legacy_v1_adapter",
        )
    ]
    for system_index, system in enumerate(specification.systems, start=1):
        base_number = len(assumptions) + 1
        assumptions.append(
            TechnicalAssumption(
                assumption_id=f"{technical_model_id}-ASSUMPTION-{base_number:03d}",
                text=(
                    f"Legacy-System {system.system_id}: {len(system.served_zone_ids)} direkte "
                    "served_zone_ids wurden verworfen; die Zonenbelegung wird nicht nach v2 migriert."
                ),
                location=f"legacy.systems.{system_index - 1}.served_zone_ids",
            )
        )
        if system.system_type == "ventilation":
            number = len(assumptions) + 1
            assumptions.append(
                TechnicalAssumption(
                    assumption_id=f"{technical_model_id}-ASSUMPTION-{number:03d}",
                    text=(
                        f"Legacy-System {system.system_id}: Die Zu-/Abluftanlage wird im aktuellen Mapping "
                        "nur als supply_air-Serviceinterface projiziert; ein extract_air-Interface wird nicht "
                        "erzeugt und muss vor einer entsprechenden Fachzuordnung getrennt ergaenzt werden."
                    ),
                    location=f"legacy.systems.{system_index - 1}.system_type",
                )
            )
        for label, value in _legacy_value_rows(system):
            number = len(assumptions) + 1
            assumptions.append(
                TechnicalAssumption(
                    assumption_id=f"{technical_model_id}-ASSUMPTION-{number:03d}",
                    text=(
                        f"Legacy-System {system.system_id}: {label}={value!s} bleibt nur "
                        "Herkunftsangabe und wird nicht als v2-Kapazitaet oder Dimensionierung verwendet."
                    ),
                    location=f"legacy.systems.{system_index - 1}",
                )
            )
    return tuple(assumptions)


def _legacy_value_rows(system: ReferenceTechnicalSystem) -> tuple[tuple[str, object], ...]:
    values = (
        ("design_power_w_m2", system.design_power_w_m2),
        ("supply_temperature_c", system.supply_temperature_c),
        ("return_temperature_c", system.return_temperature_c),
        ("performance_factor", system.performance_factor),
        ("air_change_rate_1_h", system.air_change_rate_1_h),
        ("heat_recovery_efficiency_percent", system.heat_recovery_efficiency_percent),
        ("control_strategy", system.control_strategy),
    )
    return tuple((label, value) for label, value in values if value not in (None, ""))


def _repo_relative_path(value: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("legacy_source_reference darf nicht leer sein.")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not _REPO_RELATIVE_PATH_PATTERN.search(value):
        raise ValueError("legacy_source_reference muss ein repo-relativer Pfad sein.")
    return path


def _sha256(value: str) -> str:
    if not isinstance(value, str) or not _SHA256_PATTERN.fullmatch(value):
        raise ValueError("legacy_source_sha256 muss ein SHA-256-Hexwert sein.")
    return value


def _required_text(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} darf nicht leer sein.")
    return value.strip()
