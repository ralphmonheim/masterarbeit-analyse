"""Nachweisbares Quellenmapping fuer die SmallOffice-5Z-Referenz.

Die Fachkonfiguration bleibt eine bewusst kleine, von IDA exportierbare V1-
Eingabe. Dieses Modul bewahrt dagegen die Herkunft, Details und Konflikte der
ausgelesenen Quellen. Es ersetzt weder IDM/IDC- noch IFC-Importer.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable

from .ifc_lite_import import _read_entities


@dataclass(frozen=True, slots=True)
class MappingSource:
    source_id: str
    source_kind: str
    sha256: str
    priority: int


@dataclass(frozen=True, slots=True)
class ZoneEnvelopeTotal:
    zone_id: str
    source_zone_name: str
    floor_area_m2: float
    volume_m3: float
    opaque_wall_area_m2: float
    window_area_m2: float
    door_area_m2: float
    roof_area_m2: float = 0.0
    uppermost_ceiling_area_m2: float = 0.0


@dataclass(frozen=True, slots=True)
class EnvelopeDetail:
    component_id: str
    zone_id: str
    component_kind: str
    area_m2: float
    orientation_deg: float | None
    source_label: str
    mapping_status: str
    viewer_global_id: str | None = None
    ifc_entity_type: str | None = None


@dataclass(frozen=True, slots=True)
class ReferenceMapping:
    sources: tuple[MappingSource, ...]
    totals: tuple[ZoneEnvelopeTotal, ...]
    details: tuple[EnvelopeDetail, ...]
    conflicts: tuple[str, ...]


_ZONE_TOTALS = (
    ("SPACE-5Z-LOBBY", "Lobby", 65.4, 458.1, 34.49, 72.22, 0.0, 77.95284375, 0.0),
    ("SPACE-5Z-EG-WEST", "EG West", 162.6, 438.9, 79.58, 41.51, 3.78, 0.0, 0.0),
    ("SPACE-5Z-EG-OST", "EG Ost", 67.96, 183.5, 59.72, 11.56, 1.89, 0.0, 0.0),
    ("SPACE-5Z-OG-WEST", "OG West", 162.6, 438.9, 85.94, 41.51, 3.78, 0.0, 162.552),
    ("SPACE-5Z-OG-OST", "OG Ost", 67.96, 183.5, 64.30, 10.71, 1.89, 0.0, 67.964),
)


def build_small_office_5z_b1_mapping(*, idm_path: str | Path | None = None, input_excel_path: str | Path | None = None) -> ReferenceMapping:
    """Erstellt B1 aus den fünf festgelegten 5Z-Referenzwerten.

    Die quantitativen Zonalsummen entsprechen der direkten 5Z-IDA-Eingabe.
    IDM-Details werden nur zusaetzlich gelesen und bei Abweichung als Konflikt
    gekennzeichnet; sie werden niemals auf die Summen skaliert.
    """
    totals = tuple(ZoneEnvelopeTotal(*row) for row in _ZONE_TOTALS)
    sources: list[MappingSource] = []
    details: list[EnvelopeDetail] = []
    conflicts: list[str] = []
    if input_excel_path:
        sources.append(_source("5z_input_excel", "ida_5z_input_excel", Path(input_excel_path), 1))
    if idm_path:
        path = Path(idm_path)
        sources.append(_source("5z_idm", "ida_5z_idm", path, 2))
        details, conflicts = _read_idm_surface_details(path, totals)
    return ReferenceMapping(tuple(sources), totals, tuple(details), tuple(conflicts))


def enrich_b2_from_viewer_and_ifc(
    mapping: ReferenceMapping,
    *,
    viewer_excel_path: str | Path,
    ifc_path: str | Path,
) -> ReferenceMapping:
    """Ergaenzt nur sichere B2-Links per explizitem IFC-GlobalId.

    Namens- oder Flaechenheuristiken sind absichtlich ausgeschlossen. Ohne
    vorliegenden GlobalId bleibt ein Detail ``unresolved`` statt geraten.
    """
    viewer = _viewer_global_ids(Path(viewer_excel_path))
    entities, _ = _read_entities(Path(ifc_path))
    entity_by_global_id = {
        _ifc_global_id(entity.arguments): entity.entity_type
        for entity in entities.values()
        if _ifc_global_id(entity.arguments)
    }
    enriched: list[EnvelopeDetail] = []
    unresolved = 0
    for detail in mapping.details:
        global_id = detail.viewer_global_id
        entity_type = entity_by_global_id.get(global_id) if global_id else None
        if global_id and global_id in viewer and entity_type:
            enriched.append(replace(detail, ifc_entity_type=entity_type, mapping_status="verified_b2"))
        else:
            unresolved += 1
            enriched.append(detail)
    sources = mapping.sources + (
        _source("ifc_viewer_excel", "ifc_viewer_excel", Path(viewer_excel_path), 3),
        _source("ifc_step", "ifc_step", Path(ifc_path), 3),
    )
    conflicts = mapping.conflicts + ((f"B2: {unresolved} IDM-Details ohne expliziten GlobalId-Link bleiben unaufgeloest.",) if unresolved else ())
    return ReferenceMapping(sources, mapping.totals, tuple(enriched), conflicts)


def _read_idm_surface_details(path: Path, totals: tuple[ZoneEnvelopeTotal, ...]) -> tuple[list[EnvelopeDetail], list[str]]:
    if not path.is_file():
        return [], [f"B1: IDM-Quelle fehlt: {path.name}"]
    content = path.read_text(encoding="utf-8", errors="ignore")
    details: list[EnvelopeDetail] = []
    conflicts: list[str] = []
    for total in totals:
        section = _report_section(content, total.source_zone_name)
        areas: list[float] = []
        for index, match in enumerate(re.finditer(
            r'\(NAME\s+"(?P<name>[^"]+)"\s+TYPE\s+"(?P<type>[^"]+)"\s+AREA\s+(?P<area>[-+0-9.eE]+).*?AZIM\s+(?P<azim>[-+0-9.eE]+)',
            section,
            re.S,
        ), start=1):
            type_text = match.group("type").lower()
            if "wand" not in type_text and "wall" not in type_text:
                continue
            area = float(match.group("area"))
            areas.append(area)
            details.append(EnvelopeDetail(
                f"B1-{total.zone_id}-AW-{index:02d}", total.zone_id, "wall_segment", area,
                float(match.group("azim")), match.group("name"), "detail_only",
            ))
        if areas and abs(sum(areas) - total.opaque_wall_area_m2) > 0.01:
            conflicts.append(f"B1: {total.source_zone_name}: IDM-Wandsegmente {sum(areas):.3f} m2 weichen von IDA-5Z-Summe {total.opaque_wall_area_m2:.3f} m2 ab.")
    return details, conflicts


def _report_section(content: str, zone_name: str) -> str:
    match = re.search(
        rf'\(\(REPORT-OBJECT\s+:N\s+"{re.escape(zone_name)}"\s+:T\s+ZONE-INDATA-REPORT\)(.*?)(?=\(\(REPORT-OBJECT|\Z)',
        content,
        re.S | re.I,
    )
    return match.group(0) if match else ""


def _number(block: str, key: str) -> float | None:
    match = re.search(rf"\b{key}\s*=\s*([-+0-9.eE]+)", block, re.I)
    return float(match.group(1)) if match else None


def _text(block: str, key: str) -> str | None:
    match = re.search(rf"\b{key}\s*=\s*['\"]([^'\"]+)", block, re.I)
    return match.group(1).strip() if match else None


def _source(source_id: str, source_kind: str, path: Path, priority: int) -> MappingSource:
    digest = hashlib.sha256(path.read_bytes()).hexdigest().upper() if path.is_file() else "MISSING"
    return MappingSource(source_id, source_kind, digest, priority)


def _viewer_global_ids(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    # Der Viewer-Export ist eine XLSX. Ohne neue Abhaengigkeit darf er nur
    # ueber optionale openpyxl-Installation gelesen werden.
    try:
        import openpyxl  # type: ignore[import-not-found]
    except ImportError:
        return set()
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet = workbook.active
    rows = sheet.iter_rows(values_only=True)
    headers = next(rows, ())
    index = next((index for index, value in enumerate(headers) if str(value).strip().lower().endswith("globalid")), None)
    if index is None:
        return set()
    return {str(row[index]).strip() for row in rows if len(row) > index and row[index]}


def _ifc_global_id(arguments: Iterable[str]) -> str | None:
    values = tuple(arguments)
    if not values:
        return None
    match = re.fullmatch(r"'([^']+)'", values[0].strip())
    return match.group(1) if match else None
