"""Projektbezogene Orchestrierung fuer die direkte P014-Freigabeansicht."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ma_building import (
    BuildingModelSpecification,
    load_named_building_specification,
    validate_building_spec,
)
from ma_technical import (
    BUSINESS_INTEGRATION_LOD1_TECHNICAL_SPEC_PATH,
    SMALL_OFFICE_5Z_ENDVARIANT_02_TECHNICAL_SPEC_PATH,
    SMALL_OFFICE_LOD1_TECHNICAL_SPEC_PATH,
    ObjectReference,
    ReleasedTechnicalHandover,
    TechnicalModelRevision,
    TechnicalSystemSpecification,
    build_released_technical_handover,
    load_business_integration_lod1_technical_spec,
    load_small_office_5z_endvariant_02_technical_spec,
    load_small_office_lod1_technical_spec,
    load_technical_model_revision,
    technical_revisions_directory,
)
from ma_validation import ReleaseStatus
from ma_workspace import (
    ProjectWorkspace,
    load_project_module_config,
    save_project_module_config,
)

LEGACY_TECHNICAL_SOURCE_OPTIONS = (
    (
        "small_office_5z_endvariant_02",
        "SmallOffice Endvariante 02 (Legacy-Uebergang)",
        SMALL_OFFICE_5Z_ENDVARIANT_02_TECHNICAL_SPEC_PATH,
        load_small_office_5z_endvariant_02_technical_spec,
    ),
    (
        "business_integration_lod1",
        "BusinessIntegration LoD-1 (Legacy-Demo)",
        BUSINESS_INTEGRATION_LOD1_TECHNICAL_SPEC_PATH,
        load_business_integration_lod1_technical_spec,
    ),
    (
        "synthetic_small_office_lod1",
        "Synthetisches SmallOffice LoD-1 (Legacy-Demo)",
        SMALL_OFFICE_LOD1_TECHNICAL_SPEC_PATH,
        load_small_office_lod1_technical_spec,
    ),
)


@dataclass(frozen=True, slots=True)
class SelectedBuildingContext:
    """Explizit uebernommener Building-Stand des aktiven Workspaces."""

    selection_key: str
    specification: BuildingModelSpecification
    reference: ObjectReference


class StaleActiveTechnicalRevisionError(ValueError):
    """Kennzeichnet einen gueltigen Technikstand fuer eine alte Building-Version."""

    def __init__(self, technical_model_id: str) -> None:
        self.technical_model_id = technical_model_id
        super().__init__("Die aktive Technikrevision gehoert zu einem frueheren Building-Stand.")


def legacy_technical_source_rows() -> list[dict[str, str]]:
    """Liefert die freigegebenen Legacy-Quelloptionen ohne verstecktes Titelrouting."""
    return [
        {"Schluessel": key, "Name": label, "Quelle": source_path.relative_to(source_path.parents[3]).as_posix()}
        for key, label, source_path, _loader in LEGACY_TECHNICAL_SOURCE_OPTIONS
    ]


def load_legacy_technical_source(selection_key: str) -> tuple[TechnicalSystemSpecification, Path]:
    """Laedt genau die bewusst ausgewaehlte, versionierte Legacy-Quelle."""
    for key, _label, source_path, loader in LEGACY_TECHNICAL_SOURCE_OPTIONS:
        if key == selection_key:
            return loader(), source_path
    raise ValueError(f"Unbekannte Legacy-Technikquelle: {selection_key}")


def resolve_selected_building_context(workspace: ProjectWorkspace) -> SelectedBuildingContext:
    """Prueft die explizite P012-Auswahl gegen Workspace und versionierte Quelle."""
    payload = load_project_module_config(workspace, "ma_building")
    if not isinstance(payload, dict):
        raise ValueError("Bitte zuerst in Gebaeude eine Gebaeudespezifikation uebernehmen.")
    workspace_project_id = workspace.project.identity.project_id
    if payload.get("project_id") != workspace_project_id:
        raise ValueError("Die Gebaeudekonfiguration gehoert nicht zum aktiven Projekt.")
    selection = payload.get("building_specification")
    if not isinstance(selection, dict):
        raise ValueError("Die Gebaeudekonfiguration enthaelt keinen uebernommenen Building-Stand.")
    selection_key = _required_text(selection.get("selection_key"), "building_specification.selection_key")
    building_id = _required_text(selection.get("building_id"), "building_specification.building_id")
    model_version = _required_text(selection.get("model_version"), "building_specification.model_version")
    specification = load_named_building_specification(selection_key)
    if validate_building_spec(specification).release_status is not ReleaseStatus.RELEASED:
        raise ValueError("Der uebernommene Building-Stand ist nicht strukturfreigegeben.")
    if specification.building.building_id != building_id:
        raise ValueError("Building-ID der Projektkonfiguration stimmt nicht mit der Quelle ueberein.")
    if specification.model_version.version_id != model_version:
        raise ValueError("Building-Version der Projektkonfiguration stimmt nicht mit der Quelle ueberein.")
    return SelectedBuildingContext(
        selection_key=selection_key,
        specification=specification,
        reference=ObjectReference(
            object_id=building_id,
            revision_id=model_version,
            object_type="BuildingModelSpecification",
        ),
    )


def store_active_technical_revision(
    workspace: ProjectWorkspace,
    *,
    revision_path: Path,
) -> tuple[TechnicalModelRevision, ReleasedTechnicalHandover]:
    """Laedt, prueft und referenziert genau die gespeicherte Revision."""
    resolved_revision_path = _workspace_revision_path(workspace, revision_path)
    revision = load_technical_model_revision(resolved_revision_path)
    handover = build_released_technical_handover(revision)
    if handover.project_id != workspace.project.identity.project_id:
        raise ValueError("Der Technik-Handover gehoert nicht zum aktiven Projekt.")
    if handover.building_reference is None:
        raise ValueError("Der Technik-Handover enthaelt keine Building-Referenz.")
    if not handover.release_evidence_hash:
        raise ValueError("Die projektaktive Technikrevision braucht einen hashgesicherten Freigabenachweis.")
    if not handover.has_consistent_service_interface_references() or not handover.has_consistent_handover_content():
        raise ValueError("Der Technik-Handover ist nicht hashkonsistent.")
    workspace_root = workspace.paths.root.resolve()
    _require_canonical_revision_path(workspace, resolved_revision_path, handover)

    payload = _technical_project_payload(workspace)
    active_by_building = payload.setdefault("active_v2_revisions_by_building", {})
    if not isinstance(active_by_building, dict):
        raise ValueError("Aktive v2-Technikrevisionen haben ein ungueltiges Format.")
    building_id = handover.building_reference.object_id
    active_by_building[building_id] = {
        "technical_model_id": handover.technical_model_id,
        "revision_id": handover.revision_id,
        "content_hash": handover.content_hash,
        "release_evidence_hash": handover.release_evidence_hash,
        "handover_content_hash": handover.handover_content_hash,
        "building_revision_id": handover.building_reference.revision_id,
        "relative_revision_path": resolved_revision_path.relative_to(workspace_root).as_posix(),
    }
    save_project_module_config(workspace, "ma_technical", payload)
    return revision, handover


def load_active_technical_revision(
    workspace: ProjectWorkspace,
    building_reference: ObjectReference,
) -> tuple[TechnicalModelRevision, ReleasedTechnicalHandover, Path] | None:
    """Laedt und prueft den aktiven, projektlokalen Technik-Handover eines Buildings."""
    building_id = building_reference.object_id
    payload = load_project_module_config(workspace, "ma_technical")
    if not isinstance(payload, dict):
        return None
    if payload.get("project_id") != workspace.project.identity.project_id:
        raise ValueError("Die Technikkonfiguration gehoert nicht zum aktiven Projekt.")
    active_by_building = payload.get("active_v2_revisions_by_building", {})
    if not isinstance(active_by_building, dict):
        raise ValueError("Aktive v2-Technikrevisionen haben ein ungueltiges Format.")
    reference = active_by_building.get(building_id)
    if reference is None:
        return None
    if not isinstance(reference, dict):
        raise ValueError("Die aktive Technikrevision hat ein ungueltiges Referenzformat.")
    relative_path = Path(_required_text(reference.get("relative_revision_path"), "relative_revision_path"))
    if relative_path.is_absolute():
        raise ValueError("Die aktive Technikrevision muss workspace-relativ referenziert sein.")
    workspace_root = workspace.paths.root.resolve()
    revision_path = (workspace_root / relative_path).resolve()
    revision_path = _workspace_revision_path(workspace, revision_path)
    revision = load_technical_model_revision(revision_path)
    handover = build_released_technical_handover(revision)
    _require_canonical_revision_path(workspace, revision_path, handover)
    expected_values = {
        "technical_model_id": handover.technical_model_id,
        "revision_id": handover.revision_id,
        "content_hash": handover.content_hash,
        "release_evidence_hash": handover.release_evidence_hash,
        "handover_content_hash": handover.handover_content_hash,
        "building_revision_id": handover.building_reference.revision_id if handover.building_reference else "",
    }
    for key, expected in expected_values.items():
        if reference.get(key) != expected:
            raise ValueError(f"Aktive Technikreferenz stimmt bei {key} nicht mit der Revision ueberein.")
    if handover.project_id != workspace.project.identity.project_id:
        raise ValueError("Die aktive Technikrevision gehoert nicht zum aktuellen Projekt.")
    if handover.building_reference != building_reference:
        raise StaleActiveTechnicalRevisionError(handover.technical_model_id)
    return revision, handover, revision_path


def _technical_project_payload(workspace: ProjectWorkspace) -> dict[str, object]:
    payload = load_project_module_config(workspace, "ma_technical")
    if not isinstance(payload, dict):
        payload = {}
    payload.setdefault("schema_version", "1.0")
    payload.setdefault("project_id", workspace.project.identity.project_id)
    if payload.get("project_id") != workspace.project.identity.project_id:
        raise ValueError("Die Technikkonfiguration gehoert nicht zum aktiven Projekt.")
    return payload


def _required_text(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location} darf nicht leer sein.")
    return value.strip()


def _workspace_revision_path(workspace: ProjectWorkspace, revision_path: Path) -> Path:
    resolved_path = revision_path.resolve()
    revision_root = (workspace.paths.config / "ma_technical" / "revisions").resolve()
    if not resolved_path.is_relative_to(revision_root):
        raise ValueError("Die Technikrevision liegt ausserhalb des kanonischen Workspace-Revisionspfads.")
    return resolved_path


def _require_canonical_revision_path(
    workspace: ProjectWorkspace,
    revision_path: Path,
    handover: ReleasedTechnicalHandover,
) -> None:
    if handover.building_reference is None:
        raise ValueError("Der Technik-Handover enthaelt keine Building-Referenz.")
    expected_path = (
        technical_revisions_directory(
            workspace.paths.root,
            building_id=handover.building_reference.object_id,
            technical_model_id=handover.technical_model_id,
        )
        / f"{handover.revision_id}.yaml"
    ).resolve()
    if revision_path != expected_path:
        raise ValueError("Die Technikrevision liegt nicht am kanonischen Pfad ihrer IDs.")
