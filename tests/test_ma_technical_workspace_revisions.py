from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from ma_project import Project, ProjectIdentity, ProjectLocation
from ma_technical import load_synthetic_v2_reference_technical_spec
from ma_technical.metadata import ObjectReference
from ma_technical.revisions import load_technical_model_revision
from ma_technical.workspace_revisions import (
    next_technical_model_id,
    next_technical_revision_id,
    release_workspace_technical_model,
    technical_revisions_directory,
)
from ma_workspace import create_project_workspace, save_project_module_config


def _workspace(tmp_path):
    timestamp = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)
    project = Project(
        identity=ProjectIdentity("PRJ-000001", "Technical-Testprojekt", "TTP"),
        created_at=timestamp,
        updated_at=timestamp,
        location=ProjectLocation(country_code="DE", city="Teststadt"),
    )
    workspace = create_project_workspace(project, tmp_path.resolve(), simulation_program_key="ida_ice")
    _select_building(workspace, "BUILDING-000001", "BUILDING-V1")
    return workspace


def _select_building(workspace, building_id: str, revision_id: str) -> ObjectReference:
    save_project_module_config(
        workspace,
        "ma_building",
        {
            "schema_version": "1.0",
            "project_id": workspace.project.identity.project_id,
            "building_specification": {
                "selection_key": "synthetic_test",
                "building_id": building_id,
                "model_version": revision_id,
            },
        },
    )
    return ObjectReference(
        object_id=building_id,
        revision_id=revision_id,
        object_type="BuildingModelSpecification",
    )


def _bound_specification(*, building_id: str = "BUILDING-000001", revision_id: str = "BUILDING-V1"):
    return replace(
        load_synthetic_v2_reference_technical_spec(),
        technical_model_id="TECH-000001",
        project_id="PRJ-000001",
        building_reference=ObjectReference(
            object_id=building_id,
            revision_id=revision_id,
            object_type="BuildingModelSpecification",
        ),
    )


def test_workspace_revision_release_uses_the_ud115_directory_and_sequential_ids(tmp_path):
    workspace = _workspace(tmp_path)
    specification = _bound_specification()

    first = release_workspace_technical_model(
        specification,
        workspace_root=workspace.paths.root,
        building_reference=specification.building_reference,
    )
    second = release_workspace_technical_model(
        specification,
        workspace_root=workspace.paths.root,
        building_reference=specification.building_reference,
    )

    directory = workspace.paths.config / "ma_technical" / "revisions" / "BUILDING-000001" / "TECH-000001"
    assert first.revision_id == "TECH-000001-REV-000001"
    assert second.revision_id == "TECH-000001-REV-000002"
    assert first.content_hash == second.content_hash
    assert (directory / f"{first.revision_id}.yaml").is_file()
    assert (directory / f"{second.revision_id}.yaml").is_file()


def test_next_model_id_is_project_local_across_buildings(tmp_path):
    workspace = _workspace(tmp_path)
    first = _bound_specification(building_id="BUILDING-000001")
    second = replace(first, technical_model_id="TECH-000002", building_reference=ObjectReference(
        object_id="BUILDING-000002", revision_id="BUILDING-V1", object_type="BuildingModelSpecification"
    ))
    release_workspace_technical_model(
        first, workspace_root=workspace.paths.root, building_reference=first.building_reference
    )
    _select_building(workspace, "BUILDING-000002", "BUILDING-V1")
    release_workspace_technical_model(
        second, workspace_root=workspace.paths.root, building_reference=second.building_reference
    )

    assert next_technical_model_id(workspace.paths.root) == "TECH-000003"
    assert next_technical_revision_id(
        workspace.paths.root,
        building_id="BUILDING-000001",
        technical_model_id="TECH-000001",
    ) == "TECH-000001-REV-000002"


@pytest.mark.parametrize("building_id", ("../outside", "BUILDING/OTHER", ""))
def test_workspace_revision_path_rejects_unsafe_building_ids(tmp_path, building_id):
    workspace = _workspace(tmp_path)

    with pytest.raises(ValueError):
        technical_revisions_directory(
            workspace.paths.root,
            building_id=building_id,
            technical_model_id="TECH-000001",
        )


def test_workspace_revision_release_rejects_mismatched_or_incomplete_building_reference(tmp_path):
    workspace = _workspace(tmp_path)
    mismatched = _bound_specification(building_id="BUILDING-OTHER")
    incomplete = replace(
        _bound_specification(),
        building_reference=ObjectReference(
            object_id="BUILDING-000001", revision_id="", object_type="BuildingModelSpecification"
        ),
    )

    with pytest.raises(ValueError, match="uebereinstimmen"):
        release_workspace_technical_model(
            mismatched,
            workspace_root=workspace.paths.root,
            building_reference=_bound_specification().building_reference,
        )
    with pytest.raises(ValueError, match="Building-Referenz"):
        release_workspace_technical_model(
            incomplete,
            workspace_root=workspace.paths.root,
            building_reference=incomplete.building_reference,
        )


def test_workspace_revision_release_rejects_a_foreign_project_binding(tmp_path):
    workspace = _workspace(tmp_path)
    foreign_specification = replace(_bound_specification(), project_id="PRJ-OTHER")

    with pytest.raises(ValueError, match="Workspace-Projekt"):
        release_workspace_technical_model(
            foreign_specification,
            workspace_root=workspace.paths.root,
            building_reference=foreign_specification.building_reference,
        )


def test_revision_loader_rejects_a_filename_that_does_not_match_the_stored_id(tmp_path):
    workspace = _workspace(tmp_path)
    revision = release_workspace_technical_model(
        _bound_specification(),
        workspace_root=workspace.paths.root,
        building_reference=_bound_specification().building_reference,
    )
    original = (
        workspace.paths.config
        / "ma_technical"
        / "revisions"
        / "BUILDING-000001"
        / "TECH-000001"
        / f"{revision.revision_id}.yaml"
    )
    mismatched = original.with_name("TECH-000001-REV-999999.yaml")
    original.rename(mismatched)

    with pytest.raises(ValueError, match="Dateiname"):
        load_technical_model_revision(mismatched)


@pytest.mark.parametrize("yaml_text", ("- list-root\n", "scalar-root\n"))
def test_revision_loader_rejects_non_mapping_yaml_roots(tmp_path, yaml_text):
    revision_path = tmp_path / "TECH-000001-REV-000001.yaml"
    revision_path.write_text(yaml_text, encoding="utf-8")

    with pytest.raises(ValueError, match="YAML-Mapping"):
        load_technical_model_revision(revision_path)
