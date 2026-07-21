"""Lokale, dependency-freie IFC-Lite-Ableitung fuer ``ma_building``.

Der Importer ist bewusst kein vollstaendiger IFC-Parser. Er liest nur
Storeys, Spaces und deren explizite Mengen aus einer IFC-STEP-Datei und
schreibt daraus einen *lokalen Entwurf* samt Lueckenbericht. Quellwerte werden
nicht in versionierte Beispielkonfigurationen kopiert.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from statistics import median
from typing import Iterable

import yaml

from ma_core.compliance import (
    DEFAULT_COMPLIANCE_AUDIT_PATH,
    ComplianceAuditLogger,
    ComplianceDecision,
    ComplianceOperation,
    ComplianceService,
    OperationRequest,
    SourceType,
    inspect_request_metadata,
    safe_open,
)

_ENTITY_PATTERN = re.compile(r"^#(?P<id>\d+)\s*=\s*(?P<type>[A-Z0-9_]+)\((?P<args>.*)\)$", re.DOTALL)
_REFERENCE_PATTERN = re.compile(r"#(\d+)")


@dataclass(frozen=True, slots=True)
class _IfcEntity:
    entity_id: int
    entity_type: str
    arguments: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class IfcLiteImportSummary:
    """Metadaten der lokalen IFC-Ableitung ohne IFC-Rohtext."""

    source_path: str
    source_sha256: str
    ifc_schema: str | None
    building_name: str | None
    storey_count: int
    discovered_space_count: int
    usable_space_count: int
    gap_count: int


def authorize_user_owned_ifc_lite_derivation(
    source_path: str | Path,
    *,
    confirmation_reference: str,
    audit_log_path: str | Path = DEFAULT_COMPLIANCE_AUDIT_PATH,
) -> ComplianceDecision:
    """Dokumentiert die rein lokale Ableitung eines nutzereigenen IFC-Modells."""

    if not confirmation_reference.strip():
        raise ValueError("confirmation_reference darf nicht leer sein.")
    request = OperationRequest(
        source_type=SourceType.USER_OWNED,
        operation=ComplianceOperation.CONVERT,
        purpose="Lokale IFC-Lite-Ableitung eines nutzereigenen Gebaeudemodells",
        file_path=Path(source_path),
        source_origin=f"Nutzereigenes IFC-Modell; Bestaetigung: {confirmation_reference}",
        user_owned=True,
    )
    return ComplianceService(audit_logger=ComplianceAuditLogger(audit_log_path)).evaluate(request)


def derive_ifc_lite_building_candidate(
    source_path: str | Path,
    output_directory: str | Path,
    *,
    compliance_decision: ComplianceDecision | None = None,
) -> IfcLiteImportSummary:
    """Leitet einen lokalen Building-Entwurf und einen Lueckenbericht ab.

    Die Funktion erzeugt keine freigegebene ``BuildingModelSpecification``.
    Nicht sicher aus der IFC ableitbare Angaben bleiben als Luecke erhalten.
    Die IFC-Datei wird nur nach einer ausdruecklichen lokalen Freigabe geoeffnet.
    """

    source = Path(source_path)
    target = Path(output_directory)
    decision = _require_ifc_lite_compliance(compliance_decision, source)
    entities, schema = _read_entities(source, compliance_decision=decision)
    candidate, gaps = _candidate_payload(source, entities, schema)
    target.mkdir(parents=True, exist_ok=True)
    yaml_path = target / "smalloffice_ifc_lite_building_candidate.yaml"
    report_path = target / "smalloffice_ifc_lite_gap_report.json"
    summary = IfcLiteImportSummary(
        source_path=str(source),
        source_sha256=_file_hash(source),
        ifc_schema=schema,
        building_name=candidate["building"]["name"],
        storey_count=len(candidate["storeys"]),
        discovered_space_count=candidate["source_summary"]["discovered_space_count"],
        usable_space_count=len(candidate["spaces"]),
        gap_count=len(gaps),
    )
    with yaml_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(candidate, handle, allow_unicode=True, sort_keys=False)
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump({"summary": asdict(summary), "gaps": gaps}, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return summary


def _require_ifc_lite_compliance(
    decision: ComplianceDecision | None,
    source: Path,
) -> ComplianceDecision:
    """Stoppt die IFC-Ableitung ohne lokale, explizit erlaubte Entscheidung."""

    if decision is None:
        request = OperationRequest(
            source_type=SourceType.UNKNOWN,
            operation=ComplianceOperation.CONVERT,
            purpose="Lokale IFC-Lite-Ableitung fuer ma_building",
            file_path=source,
            source_origin="IFC-Herkunft und Nutzungsrechte noch nicht dokumentiert",
        )
        decision = ComplianceService().evaluate(request)
    else:
        inspect_request_metadata(
            OperationRequest(
                source_type=SourceType.UNKNOWN,
                operation=ComplianceOperation.CONVERT,
                purpose="Metadaten-Preflight innerhalb einer freigegebenen lokalen IFC-Lite-Ableitung",
                file_path=source,
                source_origin="Freigabedetails liegen in der übergebenen lokalen Entscheidung",
            )
        )
    decision.require_allowed()
    return decision


def _candidate_payload(
    source: Path, entities: dict[int, _IfcEntity], schema: str | None
) -> tuple[dict[str, object], list[dict[str, str]]]:
    building = _first_entity(entities, "IFCBUILDING")
    project = _first_entity(entities, "IFCPROJECT")
    storeys = _storeys(entities)
    spaces, space_gaps = _spaces(entities, storeys)
    gaps: list[dict[str, str]] = list(space_gaps)
    if not storeys:
        gaps.append(_gap("building.storeys", "Keine IFCBUILDINGSTOREY-Objekte konnten abgeleitet werden."))
    if not spaces:
        gaps.append(_gap("building.spaces", "Keine Raeume mit eindeutigem Flaechen- und Volumenwert konnten abgeleitet werden."))
    gaps.extend(
        (
            _gap("building.dimensions", "Gebaeudeabmessungen werden nicht aus IFC-Geometrie abgeleitet."),
            _gap("building.north_angle_deg", "Nordrichtung ist im IFC-Lite-Import nicht aufgeloest."),
            _gap("elements", "Bauteile, Konstruktionen und Oeffnungen werden nicht automatisch in das v1-Fachmodell uebernommen."),
            _gap("simple_envelope", "U-Werte und thermische Huelle fehlen und werden nicht aus der IFC angenommen."),
            _gap("zones", "Nutzungen und Raum-Zonen-Zuordnungen sind nicht Bestandteil der IFC-Lite-Ableitung."),
            _gap("technical", "Technische Systeme sind nicht Bestandteil der IFC-Lite-Ableitung."),
        )
    )
    building_name = _label(building.arguments[2]) if building and len(building.arguments) > 2 else None
    project_name = _label(project.arguments[2]) if project and len(project.arguments) > 2 else None
    return (
        {
            "schema_version": "1.0",
            "derivation_status": "draft_with_gaps",
            "source_summary": {
                "source_path": str(source),
                "source_sha256": _file_hash(source),
                "ifc_schema": schema,
                "discovered_space_count": _entity_count(entities, "IFCSPACE"),
                "note": "Lokale IFC-Lite-Ableitung; keine freigegebene BuildingModelSpecification.",
            },
            "project": {
                "project_id": _stable_id("PROJECT-IFC", project.entity_id if project else 0),
                "name": project_name or "SmallOffice IFC-Projekt",
            },
            "building": {
                "building_id": _stable_id("BUILDING-IFC", building.entity_id if building else 0),
                "name": building_name or "SmallOffice IFC-Gebaeude",
                "unit": "m",
                "north_angle_deg": None,
                "length_m": None,
                "width_m": None,
                "height_m": _building_height(storeys),
            },
            "model_version": {
                "version_id": "BUILDING-IFC-LITE-DRAFT-001",
                "source_input_level": "BIL-2",
                "detected_input_level": "BIL-2",
                "confirmed_input_level": None,
                "current_maturity_level": "BIL-2",
                "target_maturity_level": "BIL-3",
            },
            "storeys": storeys,
            "spaces": spaces,
            "elements": [],
            "openings": [],
            "shading_devices": [],
            "assumptions": [
                {
                    "assumption_id": "ASSUMPTION-IFC-LITE-001",
                    "location": "source_summary",
                    "text": "Die Datei wurde lokal und read-only als IFC-Lite-Quelle abgeleitet. Nicht ableitbare Fachwerte bleiben im Lueckenbericht offen.",
                }
            ],
        },
        gaps,
    )


def _storeys(entities: dict[int, _IfcEntity]) -> list[dict[str, object]]:
    values: list[dict[str, object]] = []
    for entity in _entities_of_type(entities, "IFCBUILDINGSTOREY"):
        elevation = _last_number(entity.arguments)
        values.append(
            {
                "storey_id": _stable_id("STOREY-IFC", entity.entity_id),
                "name": _label_at(entity.arguments, 2) or f"IFC-Geschoss {entity.entity_id}",
                "elevation_m": elevation if elevation is not None else 0.0,
                "height_m": None,
                "source_entity_id": entity.entity_id,
            }
        )
    return values


def _spaces(
    entities: dict[int, _IfcEntity], storeys: list[dict[str, object]]
) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    parent_by_child = _aggregate_parent_map(entities)
    quantities_by_object = _quantities_by_object(entities)
    storey_ids_by_entity = {item["source_entity_id"]: item["storey_id"] for item in storeys}
    values: list[dict[str, object]] = []
    gaps: list[dict[str, str]] = []
    for entity in _entities_of_type(entities, "IFCSPACE"):
        quantities = quantities_by_object.get(entity.entity_id, ())
        area = _quantity_value(entities, quantities, "AREA")
        volume = _quantity_value(entities, quantities, "VOLUME")
        storey_entity = _ancestor_of_type(entity.entity_id, parent_by_child, entities, "IFCBUILDINGSTOREY")
        storey_id = storey_ids_by_entity.get(storey_entity)
        if area is None or volume is None or storey_id is None:
            missing = []
            if area is None:
                missing.append("Flaeche")
            if volume is None:
                missing.append("Volumen")
            if storey_id is None:
                missing.append("Geschossbezug")
            gaps.append(_gap(f"IFCSPACE #{entity.entity_id}", f"Nicht uebernommen: {', '.join(missing)} fehlen."))
            continue
        values.append(
            {
                "space_id": _stable_id("SPACE-IFC", entity.entity_id),
                "name": _label_at(entity.arguments, 2) or f"IFC-Raum {entity.entity_id}",
                "storey_id": storey_id,
                "floor_area_m2": area,
                "volume_m3": volume,
                "source_entity_id": entity.entity_id,
            }
        )
    _derive_storey_heights(storeys, values)
    return values, gaps


def _derive_storey_heights(storeys: list[dict[str, object]], spaces: list[dict[str, object]]) -> None:
    for storey in storeys:
        ratios = [
            float(space["volume_m3"]) / float(space["floor_area_m2"])
            for space in spaces
            if space["storey_id"] == storey["storey_id"] and float(space["floor_area_m2"]) > 0
        ]
        storey["height_m"] = round(float(median(ratios)), 4) if ratios else None


def _quantities_by_object(entities: dict[int, _IfcEntity]) -> dict[int, tuple[int, ...]]:
    quantities_by_definition: dict[int, tuple[int, ...]] = {}
    for entity in _entities_of_type(entities, "IFCELEMENTQUANTITY"):
        if len(entity.arguments) > 5:
            quantities_by_definition[entity.entity_id] = _references(entity.arguments[5])
    result: dict[int, tuple[int, ...]] = {}
    for entity in _entities_of_type(entities, "IFCRELDEFINESBYPROPERTIES"):
        if len(entity.arguments) <= 5:
            continue
        definition_refs = _references(entity.arguments[5])
        if not definition_refs:
            continue
        quantities = quantities_by_definition.get(definition_refs[0], ())
        for object_id in _references(entity.arguments[4]):
            result[object_id] = quantities
    return result


def _quantity_value(entities: dict[int, _IfcEntity], quantity_ids: Iterable[int], expected_type: str) -> float | None:
    candidates: list[tuple[int, float]] = []
    for quantity_id in quantity_ids:
        entity = entities.get(quantity_id)
        if entity is None or entity.entity_type != f"IFCQUANTITY{expected_type}":
            continue
        value = _last_number(entity.arguments)
        if value is None or value <= 0:
            continue
        label = (_label_at(entity.arguments, 0) or "").lower().replace(" ", "")
        priority = 0 if label.startswith("net") else 1 if label.startswith("gross") else 2
        candidates.append((priority, value))
    return sorted(candidates, key=lambda item: item[0])[0][1] if candidates else None


def _aggregate_parent_map(entities: dict[int, _IfcEntity]) -> dict[int, int]:
    result: dict[int, int] = {}
    for entity in _entities_of_type(entities, "IFCRELAGGREGATES"):
        if len(entity.arguments) > 5:
            parents = _references(entity.arguments[4])
            if parents:
                result.update({child: parents[0] for child in _references(entity.arguments[5])})
    return result


def _ancestor_of_type(
    entity_id: int, parent_by_child: dict[int, int], entities: dict[int, _IfcEntity], expected_type: str
) -> int | None:
    seen: set[int] = set()
    current = entity_id
    while current not in seen and current in parent_by_child:
        seen.add(current)
        current = parent_by_child[current]
        if entities.get(current) and entities[current].entity_type == expected_type:
            return current
    return None


def _read_entities(
    path: Path,
    *,
    compliance_decision: ComplianceDecision,
) -> tuple[dict[int, _IfcEntity], str | None]:
    with safe_open(path, "r", encoding="utf-8", errors="ignore", decision=compliance_decision) as handle:
        content = handle.read()
    schema_match = re.search(r"FILE_SCHEMA\s*\(\s*\(\s*'([^']+)'", content, re.IGNORECASE)
    entities: dict[int, _IfcEntity] = {}
    for statement in _step_statements(content):
        match = _ENTITY_PATTERN.match(statement.strip())
        if match:
            entity_id = int(match.group("id"))
            entities[entity_id] = _IfcEntity(entity_id, match.group("type"), tuple(_split_arguments(match.group("args"))))
    return entities, schema_match.group(1) if schema_match else None


def _step_statements(content: str) -> Iterable[str]:
    start = 0
    in_string = False
    index = 0
    while index < len(content):
        character = content[index]
        if character == "'":
            if in_string and index + 1 < len(content) and content[index + 1] == "'":
                index += 1
            else:
                in_string = not in_string
        elif character == ";" and not in_string:
            yield content[start:index]
            start = index + 1
        index += 1


def _split_arguments(value: str) -> list[str]:
    result: list[str] = []
    start = 0
    depth = 0
    in_string = False
    index = 0
    while index < len(value):
        character = value[index]
        if character == "'":
            if in_string and index + 1 < len(value) and value[index + 1] == "'":
                index += 1
            else:
                in_string = not in_string
        elif not in_string:
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
            elif character == "," and depth == 0:
                result.append(value[start:index].strip())
                start = index + 1
        index += 1
    result.append(value[start:].strip())
    return result


def _entities_of_type(entities: dict[int, _IfcEntity], entity_type: str) -> Iterable[_IfcEntity]:
    return (entity for entity in entities.values() if entity.entity_type == entity_type)


def _first_entity(entities: dict[int, _IfcEntity], entity_type: str) -> _IfcEntity | None:
    return next(iter(_entities_of_type(entities, entity_type)), None)


def _entity_count(entities: dict[int, _IfcEntity], entity_type: str) -> int:
    return sum(1 for _ in _entities_of_type(entities, entity_type))


def _references(value: str) -> tuple[int, ...]:
    return tuple(int(match) for match in _REFERENCE_PATTERN.findall(value))


def _label_at(arguments: tuple[str, ...], index: int) -> str | None:
    return _label(arguments[index]) if len(arguments) > index else None


def _label(value: str) -> str | None:
    if value.strip() in {"$", "*", ""}:
        return None
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return None


def _last_number(arguments: Iterable[str]) -> float | None:
    for value in reversed(tuple(arguments)):
        try:
            return float(value)
        except ValueError:
            continue
    return None


def _building_height(storeys: list[dict[str, object]]) -> float | None:
    heights = [float(storey["height_m"]) for storey in storeys if storey["height_m"] is not None]
    return round(sum(heights), 4) if heights else None


def _stable_id(prefix: str, entity_id: int) -> str:
    return f"{prefix}-{entity_id:06d}"


def _file_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def _gap(location: str, description: str) -> dict[str, str]:
    return {"location": location, "description": description}
