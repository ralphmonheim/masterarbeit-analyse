"""Getrennte Ergebnisvertraege fuer P016-Referenzdimensionierung.

Die LoD-1-Naeherung und manuell aus einem externen IDA-Lauf uebernommene
Zonenlasten sind fachlich nicht austauschbar. Dieses Modul modelliert beide
Ergebnisarten deshalb mit getrennten, versionierten Datenklassen. Es ersetzt
noch keine historische Persistenz oder UI-Validierung; die Adapter machen
deren bestehende Ergebnisse lediglich explizit und pruefbar.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Final, Mapping, Sequence

from ma_analyse.stage_1_dimensioning import DimensioningStatus

from .gateway import (
    LOD1_RESULT_ROUNDING_RULE,
    DimensioningAssumption,
    Lod1GatewayExecution,
)

DIMENSIONING_RESULT_CONTRACT_VERSION: Final = "1.0"
CALCULATED_LOD1_RESULT_KIND: Final = "calculated_lod1_reference"
MANUAL_EXTERNAL_IDA_RESULT_KIND: Final = "manual_external_ida_reference"
_SHA256_PATTERN: Final = re.compile(r"[0-9a-fA-F]{64}\Z")


class ManualIdaReviewStatus(StrEnum):
    """Pruefstatus einer manuell aus IDA uebernommenen Referenzlast."""

    UNREVIEWED = "unreviewed"
    REVIEWED = "reviewed"


@dataclass(frozen=True, slots=True)
class CalculatedLod1ReferenceResult:
    """Nachvollziehbares Ergebnis der berechneten LoD-1-Naeherung."""

    result_kind: str
    contract_version: str
    result_id: str
    source_snapshot_id: str
    source_snapshot_version: str
    status: DimensioningStatus
    method_id: str
    method_version: str
    assumptions: tuple[DimensioningAssumption, ...]
    rounding_rule: str
    input_fingerprint: str
    result_fingerprint: str
    heating_transmission_load_w: float | None
    heating_ventilation_load_w: float | None
    heating_total_load_w: float | None
    cooling_internal_load_w: float | None
    ventilation_volume_flow_m3_h: float | None

    def __post_init__(self) -> None:
        if self.result_kind != CALCULATED_LOD1_RESULT_KIND:
            raise ValueError("Der Ergebnisvertrag ist nur fuer berechnete LoD-1-Referenzen gueltig.")
        if self.contract_version != DIMENSIONING_RESULT_CONTRACT_VERSION:
            raise ValueError("Die Ergebnisvertragsversion ist nicht unterstuetzt.")
        if not self.result_id.strip() or not self.source_snapshot_id.strip() or not self.source_snapshot_version.strip():
            raise ValueError("Berechnete LoD-1-Ergebnisse brauchen eine vollstaendige Snapshot-Provenienz.")
        if not self.method_id.strip() or not self.method_version.strip():
            raise ValueError("Berechnete LoD-1-Ergebnisse brauchen Methoden-ID und -Version.")
        if self.rounding_rule != LOD1_RESULT_ROUNDING_RULE:
            raise ValueError("Berechnete LoD-1-Ergebnisse brauchen die vereinbarte Rundungsregel.")
        _require_sha256("input_fingerprint", self.input_fingerprint)
        _require_sha256("result_fingerprint", self.result_fingerprint)
        object.__setattr__(self, "assumptions", tuple(self.assumptions))
        _validate_optional_loads(self)


@dataclass(frozen=True, slots=True)
class ManualIdaReferenceZoneLoad:
    """Eine manuell uebernommene zonale Heiz- und Kuehllast in Watt."""

    zone_id: str
    zone_name: str
    heating_load_w: float
    cooling_load_w: float

    def __post_init__(self) -> None:
        if not self.zone_id.strip() or not self.zone_name.strip():
            raise ValueError("Manuelle IDA-Lasten brauchen Zonen-ID und Zonenname.")
        _require_non_negative_finite("heating_load_w", self.heating_load_w)
        _require_non_negative_finite("cooling_load_w", self.cooling_load_w)


@dataclass(frozen=True, slots=True)
class ManualIdaSourceProvenance:
    """Provenienz des extern ausgefuehrten IDA-Laufs ohne Quelldateizugriff."""

    ida_version: str
    model_id: str
    run_id: str
    source_file_name: str
    source_file_sha256: str
    heating_load_definition: str
    cooling_load_definition: str
    maximum_definition: str
    design_conditions: str
    responsible: str
    review_status: ManualIdaReviewStatus | str
    reviewer: str = ""
    reviewed_at: str = ""
    review_note: str = ""
    source_classification: str = "externally_simulated_result"

    def __post_init__(self) -> None:
        for field_name in (
            "ida_version",
            "model_id",
            "run_id",
            "source_file_name",
            "heating_load_definition",
            "cooling_load_definition",
            "maximum_definition",
            "design_conditions",
            "responsible",
            "source_classification",
        ):
            if not getattr(self, field_name).strip():
                raise ValueError(f"Manuelle IDA-Provenienz benoetigt '{field_name}'.")
        _require_sha256("source_file_sha256", self.source_file_sha256)
        if not isinstance(self.review_status, ManualIdaReviewStatus):
            object.__setattr__(self, "review_status", ManualIdaReviewStatus(self.review_status))
        if self.review_status is ManualIdaReviewStatus.REVIEWED:
            for field_name in ("reviewer", "reviewed_at", "review_note"):
                if not getattr(self, field_name).strip():
                    raise ValueError(f"Gepruefte IDA-Provenienz benoetigt '{field_name}'.")


@dataclass(frozen=True, slots=True)
class ManualIdaReferenceLoadSet:
    """Manuell uebernommene externe IDA-Referenzlasten, getrennt von LoD-1."""

    result_kind: str
    contract_version: str
    result_id: str
    project_id: str
    zone_model_id: str
    zone_model_hash: str
    reference_parameter_fingerprint: str
    result_fingerprint: str
    unit: str
    zone_loads: tuple[ManualIdaReferenceZoneLoad, ...]
    source: ManualIdaSourceProvenance
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.result_kind != MANUAL_EXTERNAL_IDA_RESULT_KIND:
            raise ValueError("Der Ergebnisvertrag ist nur fuer manuelle externe IDA-Referenzen gueltig.")
        if self.contract_version != DIMENSIONING_RESULT_CONTRACT_VERSION:
            raise ValueError("Die Ergebnisvertragsversion ist nicht unterstuetzt.")
        if self.unit != "W":
            raise ValueError("Manuelle IDA-Referenzlasten werden ausschliesslich in W gefuehrt.")
        for field_name in ("result_id", "project_id", "zone_model_id"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"Manuelle IDA-Referenzen benoetigen '{field_name}'.")
        _require_sha256("zone_model_hash", self.zone_model_hash)
        _require_sha256("reference_parameter_fingerprint", self.reference_parameter_fingerprint)
        _require_sha256("result_fingerprint", self.result_fingerprint)
        object.__setattr__(self, "zone_loads", tuple(self.zone_loads))
        object.__setattr__(self, "warnings", tuple(self.warnings))
        if not self.zone_loads:
            raise ValueError("Manuelle IDA-Referenzen brauchen mindestens eine Zonelast.")
        zone_ids = [row.zone_id for row in self.zone_loads]
        if len(zone_ids) != len(set(zone_ids)):
            raise ValueError("Manuelle IDA-Referenzen duerfen keine doppelte Zonen-ID enthalten.")


def calculated_lod1_result_from_execution(execution: Lod1GatewayExecution) -> CalculatedLod1ReferenceResult:
    """Adaptierte LoD-1-Ausfuehrung in den neuen, getrennten Ergebnisvertrag."""
    result = execution.result
    return CalculatedLod1ReferenceResult(
        result_kind=CALCULATED_LOD1_RESULT_KIND,
        contract_version=DIMENSIONING_RESULT_CONTRACT_VERSION,
        result_id=result.result_id,
        source_snapshot_id=result.source_snapshot_id,
        source_snapshot_version=result.source_snapshot_version,
        status=result.status,
        method_id=execution.request.method_id,
        method_version=execution.request.method_version,
        assumptions=execution.request.assumptions,
        rounding_rule=execution.request.rounding_rule,
        input_fingerprint=execution.request.input_fingerprint,
        result_fingerprint=_fingerprint(_calculated_result_payload(execution)),
        heating_transmission_load_w=result.heating_transmission_load_w,
        heating_ventilation_load_w=result.heating_ventilation_load_w,
        heating_total_load_w=result.heating_total_load_w,
        cooling_internal_load_w=result.cooling_internal_load_w,
        ventilation_volume_flow_m3_h=result.ventilation_volume_flow_m3_h,
    )


def manual_ida_reference_load_set_from_payload(payload: Mapping[str, object]) -> ManualIdaReferenceLoadSet:
    """Prueft und adaptiert den bestehenden manuellen UI-Payload ohne ihn zu aendern."""
    if payload.get("source_type") != "manual_ida_result":
        raise ValueError("Der Payload ist keine manuell uebernommene IDA-Referenzlast.")
    zone_loads_raw = _require_list(payload, "zone_loads")
    zone_loads = tuple(_manual_zone_load_from_payload(row) for row in zone_loads_raw)
    source = _manual_source_from_payload(_require_mapping(payload, "ida_source"))
    project_id = _require_text(payload, "project_id")
    zone_model_id = _require_text(payload, "zone_model_id")
    zone_model_hash = _require_text(payload, "zone_model_hash")
    reference_parameter_fingerprint = _require_text(payload, "reference_parameter_fingerprint")
    warnings = tuple(str(warning) for warning in payload.get("warnings", ()) if str(warning).strip())
    result_fingerprint = _fingerprint(
        {
            "result_kind": MANUAL_EXTERNAL_IDA_RESULT_KIND,
            "contract_version": DIMENSIONING_RESULT_CONTRACT_VERSION,
            "project_id": project_id,
            "zone_model_id": zone_model_id,
            "zone_model_hash": zone_model_hash,
            "reference_parameter_fingerprint": reference_parameter_fingerprint,
            "unit": _require_text(payload, "unit"),
            "zone_loads": [asdict(row) for row in zone_loads],
            "source": _provenance_payload(source),
            "warnings": list(warnings),
        }
    )
    return ManualIdaReferenceLoadSet(
        result_kind=MANUAL_EXTERNAL_IDA_RESULT_KIND,
        contract_version=DIMENSIONING_RESULT_CONTRACT_VERSION,
        result_id=f"manual-ida-{result_fingerprint[:16]}",
        project_id=project_id,
        zone_model_id=zone_model_id,
        zone_model_hash=zone_model_hash,
        reference_parameter_fingerprint=reference_parameter_fingerprint,
        result_fingerprint=result_fingerprint,
        unit=_require_text(payload, "unit"),
        zone_loads=zone_loads,
        source=source,
        warnings=warnings,
    )


def validate_manual_ida_editor_rows(
    expected_zones: Sequence[tuple[str, str]],
    editor_rows: Sequence[Mapping[str, object]],
) -> tuple[list[dict[str, object]], tuple[str, ...]]:
    """Validiert die UI-neutralen drei Spalten der manuellen IDA-Eingabe.

    Die Reihenfolge der erwarteten Zonen ist absichtlich Teil des Vertrags:
    Die gesperrte Namensspalte verhindert, dass Lasten versehentlich einer
    anderen Zone zugeordnet werden.
    """
    if len(editor_rows) != len(expected_zones):
        raise ValueError("Jede Zone des aktiven Modells muss genau einmal enthalten sein.")
    values: list[dict[str, object]] = []
    warnings: list[str] = []
    for (zone_id, zone_name), row in zip(expected_zones, editor_rows, strict=True):
        if str(row.get("Zone", "")).strip() != zone_name:
            raise ValueError(
                "Die Zonenspalte wurde sortiert oder veraendert. "
                "Bitte die Tabelle auf den Modellstand zuruecksetzen."
            )
        heating_value = _editor_load_value(row.get("Heizlast [W]"), zone_name, "Heiz")
        cooling_value = _editor_load_value(row.get("Kuehllast [W]"), zone_name, "Kühl")
        if heating_value == 0 or cooling_value == 0:
            warnings.append(f"Zone '{zone_name}' enthält 0 W und muss fachlich geprüft werden.")
        values.append(
            {
                "zone_id": zone_id,
                "zone_name": zone_name,
                "heating_load_w": heating_value,
                "cooling_load_w": cooling_value,
            }
        )
    return values, tuple(warnings)


def validate_manual_ida_source_metadata(
    metadata: Mapping[str, object],
) -> ManualIdaSourceProvenance:
    """Validiert die manuell erfasste IDA-Provenienz ohne Quelldateizugriff."""
    required = (
        "ida_version", "model_id", "run_id", "source_file_name",
        "cooling_load_definition", "maximum_definition", "design_conditions", "responsible",
    )
    missing = [field for field in required if not str(metadata.get(field, "")).strip()]
    if missing:
        raise ValueError(f"IDA-Quellmetadaten fehlen: {', '.join(missing)}.")
    source_hash = str(metadata.get("source_file_sha256", "")).strip()
    if not _SHA256_PATTERN.fullmatch(source_hash):
        raise ValueError("Die IDA-Quelldatei braucht eine gueltige SHA-256-Pruefsumme.")
    if str(metadata.get("review_status", "")).strip() == ManualIdaReviewStatus.REVIEWED:
        review_fields = ("reviewer", "reviewed_at", "review_note")
        missing_review = [field for field in review_fields if not str(metadata.get(field, "")).strip()]
        if missing_review:
            raise ValueError("Gepruefte IDA-Daten brauchen Reviewer, Pruefdatum und Pruefhinweis.")
        try:
            datetime.fromisoformat(str(metadata["reviewed_at"]))
        except ValueError as exc:
            raise ValueError("Das IDA-Pruefdatum muss ISO-8601 entsprechen.") from exc
    return _manual_source_from_payload(metadata)


def build_manual_ida_legacy_payload(
    *,
    project_id: str,
    zone_model_id: str,
    zone_model_hash: str,
    parameter_fingerprint: str,
    reference_parameter_fingerprint: str,
    zone_loads: Sequence[Mapping[str, object]],
    source_metadata: Mapping[str, object],
    warnings: Sequence[str],
    updated_at: str | None = None,
) -> dict[str, object]:
    """Erzeugt den unveraenderten historischen Workspace-Payload nach Owner-Pruefung."""
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "source_type": "manual_ida_result",
        "project_id": project_id,
        "zone_model_id": zone_model_id,
        "zone_model_hash": zone_model_hash,
        "updated_at": updated_at or datetime.now(UTC).isoformat(),
        "unit": "W",
        "zone_loads": [dict(row) for row in zone_loads],
        "parameter_fingerprint": parameter_fingerprint,
        "reference_parameter_fingerprint": reference_parameter_fingerprint,
        "ida_source": dict(source_metadata),
        "warnings": list(warnings),
    }
    manual_ida_reference_load_set_from_payload(payload)
    return payload


def _calculated_result_payload(execution: Lod1GatewayExecution) -> dict[str, object]:
    result = execution.result
    return {
        "result_kind": CALCULATED_LOD1_RESULT_KIND,
        "contract_version": DIMENSIONING_RESULT_CONTRACT_VERSION,
        "method_id": execution.request.method_id,
        "method_version": execution.request.method_version,
        "rounding_rule": execution.request.rounding_rule,
        "input_fingerprint": execution.request.input_fingerprint,
        "legacy_gateway_result_fingerprint": execution.result_fingerprint,
        "result_id": result.result_id,
        "source_snapshot_id": result.source_snapshot_id,
        "source_snapshot_version": result.source_snapshot_version,
        "status": result.status.value,
        "loads": {
            "heating_transmission_load_w": result.heating_transmission_load_w,
            "heating_ventilation_load_w": result.heating_ventilation_load_w,
            "heating_total_load_w": result.heating_total_load_w,
            "cooling_internal_load_w": result.cooling_internal_load_w,
            "ventilation_volume_flow_m3_h": result.ventilation_volume_flow_m3_h,
        },
        "assumptions": [asdict(assumption) for assumption in execution.request.assumptions],
    }


def _manual_zone_load_from_payload(value: object) -> ManualIdaReferenceZoneLoad:
    row = _as_mapping(value, "zone_loads-Eintrag")
    return ManualIdaReferenceZoneLoad(
        zone_id=_require_text(row, "zone_id"),
        zone_name=_require_text(row, "zone_name"),
        heating_load_w=_require_number(row, "heating_load_w"),
        cooling_load_w=_require_number(row, "cooling_load_w"),
    )


def _editor_load_value(value: object, zone_name: str, _load_label: str) -> float:
    if value is None:
        raise ValueError(f"Für Zone '{zone_name}' fehlen Heiz- oder Kühllast.")
    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Lastwerte der Zone '{zone_name}' müssen Zahlen sein.") from exc
    if not math.isfinite(numeric_value):
        raise ValueError(f"Lastwerte der Zone '{zone_name}' müssen endlich sein.")
    if numeric_value < 0:
        raise ValueError(f"Lastwerte der Zone '{zone_name}' dürfen nicht negativ sein.")
    return numeric_value


def _manual_source_from_payload(value: Mapping[str, object]) -> ManualIdaSourceProvenance:
    return ManualIdaSourceProvenance(
        ida_version=_require_text(value, "ida_version"),
        model_id=_require_text(value, "model_id"),
        run_id=_require_text(value, "run_id"),
        source_file_name=_require_text(value, "source_file_name"),
        source_file_sha256=_require_text(value, "source_file_sha256"),
        heating_load_definition=_require_text(value, "heating_load_definition"),
        cooling_load_definition=_require_text(value, "cooling_load_definition"),
        maximum_definition=_require_text(value, "maximum_definition"),
        design_conditions=_require_text(value, "design_conditions"),
        responsible=_require_text(value, "responsible"),
        review_status=_require_text(value, "review_status"),
        reviewer=str(value.get("reviewer", "")).strip(),
        reviewed_at=str(value.get("reviewed_at", "")).strip(),
        review_note=str(value.get("review_note", "")).strip(),
        source_classification=_require_text(value, "source_classification"),
    )


def _provenance_payload(source: ManualIdaSourceProvenance) -> dict[str, str]:
    return {
        field_name: str(getattr(source, field_name))
        for field_name in (
            "ida_version", "model_id", "run_id", "source_file_name", "source_file_sha256",
            "heating_load_definition", "cooling_load_definition", "maximum_definition",
            "design_conditions", "responsible", "review_status", "reviewer", "reviewed_at",
            "review_note", "source_classification",
        )
    }


def _validate_optional_loads(result: CalculatedLod1ReferenceResult) -> None:
    for field_name in (
        "heating_transmission_load_w",
        "heating_ventilation_load_w",
        "heating_total_load_w",
        "cooling_internal_load_w",
        "ventilation_volume_flow_m3_h",
    ):
        value = getattr(result, field_name)
        if value is not None:
            _require_non_negative_finite(field_name, value)


def _require_non_negative_finite(field_name: str, value: object) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)) or float(value) < 0:
        raise ValueError(f"'{field_name}' muss eine endliche, nichtnegative Zahl sein.")


def _require_sha256(field_name: str, value: str) -> None:
    if not _SHA256_PATTERN.fullmatch(value):
        raise ValueError(f"'{field_name}' muss ein SHA-256-Hash sein.")


def _require_text(payload: Mapping[str, object], field_name: str) -> str:
    value = payload.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Manuelle IDA-Referenz benoetigt '{field_name}'.")
    return value.strip()


def _require_number(payload: Mapping[str, object], field_name: str) -> float:
    value = payload.get(field_name)
    if isinstance(value, bool):
        raise ValueError(f"Manuelle IDA-Referenz benoetigt eine Zahl fuer '{field_name}'.")
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Manuelle IDA-Referenz benoetigt eine Zahl fuer '{field_name}'.") from exc


def _require_mapping(payload: Mapping[str, object], field_name: str) -> Mapping[str, object]:
    return _as_mapping(payload.get(field_name), field_name)


def _as_mapping(value: object, field_name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"Manuelle IDA-Referenz benoetigt ein Objekt fuer '{field_name}'.")
    return value


def _require_list(payload: Mapping[str, object], field_name: str) -> list[object]:
    value = payload.get(field_name)
    if not isinstance(value, list):
        raise ValueError(f"Manuelle IDA-Referenz benoetigt eine Liste fuer '{field_name}'.")
    return value


def _fingerprint(payload: object) -> str:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
