"""Projektlokale, append-only Revisionen fuer ``ma_technical``.

Dieses Modul kennt nur die P035-Ordnergrenze. Die fachliche YAML-Revision
bleibt in :mod:`ma_technical.revisions` implementiert und kann deshalb auch
weiterhin mit temporaeren Testordnern verwendet werden.
"""

from __future__ import annotations

import re
from pathlib import Path

from ma_workspace import load_project_module_config, load_project_workspace

from .metadata import ObjectReference
from .revisions import TechnicalModelRevision, release_technical_model
from .specification import TechnicalModelSpecification

_BUILDING_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}\Z")
_TECHNICAL_MODEL_ID_PATTERN = re.compile(r"TECH-([0-9]{6})\Z")
_TECHNICAL_REVISION_ID_PATTERN = re.compile(r"(TECH-[0-9]{6})-REV-([0-9]{6})\Z")


def technical_revisions_directory(
    workspace_root: str | Path,
    *,
    building_id: str,
    technical_model_id: str,
) -> Path:
    """Liefert den ausschliesslich von einem Building/Technikmodell besessenen Pfad."""
    root = _workspace_root(workspace_root)
    _require_building_id(building_id)
    _require_technical_model_id(technical_model_id)
    target = (root / "config" / "ma_technical" / "revisions" / building_id / technical_model_id).resolve()
    config_root = (root / "config").resolve()
    if not target.is_relative_to(config_root):
        raise ValueError("Der Technikrevisionspfad liegt ausserhalb der Workspace-Konfiguration.")
    return target


def next_technical_model_id(workspace_root: str | Path) -> str:
    """Vergibt die naechste projektlokale, systemseitige Technikmodell-ID."""
    root = _workspace_root(workspace_root)
    revisions_root = root / "config" / "ma_technical" / "revisions"
    highest_sequence = 0
    if revisions_root.is_dir():
        for building_directory in revisions_root.iterdir():
            if not building_directory.is_dir() or building_directory.is_symlink():
                continue
            for model_directory in building_directory.iterdir():
                if not model_directory.is_dir() or model_directory.is_symlink():
                    continue
                match = _TECHNICAL_MODEL_ID_PATTERN.fullmatch(model_directory.name)
                if match:
                    highest_sequence = max(highest_sequence, int(match.group(1)))
    if highest_sequence >= 999_999:
        raise RuntimeError("Die projektlokale TECH-ID-Sequenz ist ausgeschoepft.")
    return f"TECH-{highest_sequence + 1:06d}"


def next_technical_revision_id(
    workspace_root: str | Path,
    *,
    building_id: str,
    technical_model_id: str,
) -> str:
    """Vergibt die naechste Revision eines bestehenden projektlokalen Technikmodells."""
    directory = technical_revisions_directory(
        workspace_root,
        building_id=building_id,
        technical_model_id=technical_model_id,
    )
    highest_sequence = 0
    if directory.is_dir():
        for revision_file in directory.glob("*.yaml"):
            if not revision_file.is_file() or revision_file.is_symlink():
                continue
            match = _TECHNICAL_REVISION_ID_PATTERN.fullmatch(revision_file.stem)
            if match and match.group(1) == technical_model_id:
                highest_sequence = max(highest_sequence, int(match.group(2)))
    if highest_sequence >= 999_999:
        raise RuntimeError("Die Revisionsequenz dieses Technikmodells ist ausgeschoepft.")
    return f"{technical_model_id}-REV-{highest_sequence + 1:06d}"


def release_workspace_technical_model(
    specification: TechnicalModelSpecification,
    *,
    workspace_root: str | Path,
    building_reference: ObjectReference,
    warnings_confirmed: bool = False,
) -> TechnicalModelRevision:
    """Gibt einen korrekt gebundenen Entwurf als neue Workspace-Revision frei.

    Der Aufrufer prueft die fachliche Auswahl des Buildings. Diese Grenze
    prueft deren unveraenderliche IDs nochmals, bevor eine Datei entsteht.
    """
    root = _workspace_root(workspace_root)
    workspace = load_project_workspace(root)
    project_id = workspace.project.identity.project_id
    if specification.project_id != project_id:
        raise ValueError("project_id muss mit dem aktiven Workspace-Projekt uebereinstimmen.")
    if not isinstance(building_reference, ObjectReference):
        raise TypeError("building_reference muss eine ObjectReference sein.")
    _require_selected_building_reference(workspace, building_reference)
    if specification.building_reference != building_reference:
        raise ValueError("building_reference muss mit dem aktiven Workspace-Building uebereinstimmen.")
    building_id = building_reference.object_id
    _require_building_id(building_id)
    _require_technical_model_id(specification.technical_model_id)
    if specification.building_reference.object_id != building_id:
        raise ValueError("building_id muss mit der building_reference des Technikmodells uebereinstimmen.")
    if not specification.building_reference.revision_id:
        raise ValueError("Die building_reference des Technikmodells braucht eine model_version.")
    target_dir = technical_revisions_directory(
        workspace_root,
        building_id=building_id,
        technical_model_id=specification.technical_model_id,
    )
    revision_id = next_technical_revision_id(
        workspace_root,
        building_id=building_id,
        technical_model_id=specification.technical_model_id,
    )
    return release_technical_model(
        specification,
        revision_id=revision_id,
        target_dir=target_dir,
        warnings_confirmed=warnings_confirmed,
    )


def _require_selected_building_reference(workspace, building_reference: ObjectReference) -> None:
    payload = load_project_module_config(workspace, "ma_building")
    if not isinstance(payload, dict) or payload.get("project_id") != workspace.project.identity.project_id:
        raise ValueError("Der aktive Workspace enthaelt keinen passenden ma_building-Projektstand.")
    selection = payload.get("building_specification")
    if not isinstance(selection, dict):
        raise ValueError("Der aktive Workspace enthaelt keinen ausgewaehlten Building-Stand.")
    selected_reference = ObjectReference(
        object_id=str(selection.get("building_id", "")).strip(),
        revision_id=str(selection.get("model_version", "")).strip(),
        content_hash=str(selection.get("content_hash", "")).strip(),
        object_type="BuildingModelSpecification",
    )
    if selected_reference != building_reference:
        raise ValueError("Building-Referenz stimmt nicht mit dem aktiven ma_building-Stand ueberein.")


def _workspace_root(workspace_root: str | Path) -> Path:
    root = Path(workspace_root)
    if not root.is_absolute():
        raise ValueError("workspace_root muss absolut sein.")
    resolved_root = root.resolve()
    if not resolved_root.is_dir():
        raise FileNotFoundError(f"Workspace-Ordner nicht gefunden: {resolved_root}")
    return resolved_root


def _require_building_id(building_id: str) -> None:
    if not isinstance(building_id, str) or not _BUILDING_ID_PATTERN.fullmatch(building_id):
        raise ValueError("building_id darf nur Buchstaben, Ziffern, Bindestriche und Unterstriche enthalten.")


def _require_technical_model_id(technical_model_id: str) -> None:
    if not isinstance(technical_model_id, str) or not _TECHNICAL_MODEL_ID_PATTERN.fullmatch(technical_model_id):
        raise ValueError("technical_model_id muss dem Format TECH-000001 entsprechen.")
