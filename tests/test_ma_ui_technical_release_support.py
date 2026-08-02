"""Vertragstests fuer die projektbezogene P014-UI-Orchestrierung."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from ma_project import Project, ProjectIdentity, ProjectLocation
from ma_technical import ObjectReference, build_released_technical_handover, load_synthetic_v2_reference_technical_spec
from ma_technical.revisions import release_technical_model
from ma_ui.streamlit_app.module_views import technical_view
from ma_ui.streamlit_app.module_views.technical_release_support import (
    StaleActiveTechnicalRevisionError,
    legacy_technical_source_rows,
    load_active_technical_revision,
    load_legacy_technical_source,
    resolve_selected_building_context,
    store_active_technical_revision,
)
from ma_workspace import create_project_workspace, save_project_module_config


def _workspace(tmp_path):
    timestamp = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)
    project = Project(
        identity=ProjectIdentity("PRJ-000001", "Testprojekt", "TP"),
        created_at=timestamp,
        updated_at=timestamp,
        location=ProjectLocation(country_code="DE", city="Teststadt"),
    )
    return create_project_workspace(project, tmp_path.resolve(), simulation_program_key="ida_ice")


def _save_building_selection(workspace):
    save_project_module_config(
        workspace,
        "ma_building",
        {
            "schema_version": "1.0",
            "project_id": workspace.project.identity.project_id,
            "building_specification": {
                "selection_key": "business_integration_lod1",
                "building_id": "BUILDING-BI-LOD1-0001",
                "model_version": "BUILDING-BI-LOD1-V2",
            },
        },
    )


def test_selected_building_context_requires_an_explicit_project_selection(tmp_path):
    workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="zuerst in Gebaeude"):
        resolve_selected_building_context(workspace)

    _save_building_selection(workspace)
    context = resolve_selected_building_context(workspace)

    assert context.selection_key == "business_integration_lod1"
    assert context.reference.object_id == "BUILDING-BI-LOD1-0001"
    assert context.reference.revision_id == "BUILDING-BI-LOD1-V2"
    assert context.reference.content_hash == ""


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("project_id", "PRJ-999999", "nicht zum aktiven Projekt"),
        ("building_id", "BUILDING-WRONG", "Building-ID"),
        ("model_version", "BUILDING-WRONG-V1", "Building-Version"),
    ),
)
def test_selected_building_context_blocks_mismatched_project_and_building(tmp_path, field, value, message):
    workspace = _workspace(tmp_path)
    _save_building_selection(workspace)
    payload = {
        "schema_version": "1.0",
        "project_id": workspace.project.identity.project_id,
        "building_specification": {
            "selection_key": "business_integration_lod1",
            "building_id": "BUILDING-BI-LOD1-0001",
            "model_version": "BUILDING-BI-LOD1-V2",
        },
    }
    if field == "project_id":
        payload[field] = value
    else:
        payload["building_specification"][field] = value
    save_project_module_config(workspace, "ma_building", payload)

    with pytest.raises(ValueError, match=message):
        resolve_selected_building_context(workspace)


def test_legacy_sources_are_explicit_repo_relative_choices():
    rows = legacy_technical_source_rows()
    specification, source_path = load_legacy_technical_source("business_integration_lod1")

    assert {row["Schluessel"] for row in rows} >= {
        "business_integration_lod1",
        "small_office_5z_endvariant_02",
    }
    assert all(not row["Quelle"].startswith(("/", "C:")) for row in rows)
    assert specification.technical_model_id == "TECH-BI-LOD1-MODEL-0001"
    assert source_path.is_file()


def test_direct_view_prepares_without_writing_and_releases_only_on_explicit_action(tmp_path, monkeypatch):
    workspace = _workspace(tmp_path)
    _save_building_selection(workspace)
    building_context = resolve_selected_building_context(workspace)
    before = {
        path.relative_to(workspace.paths.root): path.read_bytes()
        for path in workspace.paths.root.rglob("*")
        if path.is_file()
    }

    draft = technical_view.prepare_project_technical_draft(
        workspace,
        building_context,
        selection_key="business_integration_lod1",
        technical_model_id="TECH-000001",
    )

    after_prepare = {
        path.relative_to(workspace.paths.root): path.read_bytes()
        for path in workspace.paths.root.rglob("*")
        if path.is_file()
    }
    assert after_prepare == before

    class FakeStreamlit:
        session_state: dict[str, object] = {}

        @staticmethod
        def success(*_args, **_kwargs):
            return None

        @staticmethod
        def error(*_args, **_kwargs):
            return None

        @staticmethod
        def dataframe(*_args, **_kwargs):
            return None

    monkeypatch.setattr(technical_view, "st", FakeStreamlit())
    technical_view._release_project_technical_draft(
        workspace,
        building_context,
        draft,
        warnings_confirmed=True,
    )

    active = load_active_technical_revision(workspace, building_context.reference)
    assert active is not None
    revision, handover, revision_path = active
    assert revision.revision_id == "TECH-000001-REV-000001"
    assert handover.content_hash == revision.content_hash
    assert revision_path.is_file()
    assert all("served_zone_ids" not in item for item in revision.specification_payload["service_interfaces"])


def test_active_revision_reference_round_trips_only_inside_workspace(tmp_path):
    workspace = _workspace(tmp_path)
    _save_building_selection(workspace)
    building_context = resolve_selected_building_context(workspace)
    specification = replace(
        load_synthetic_v2_reference_technical_spec(),
        technical_model_id="TECH-000001",
        project_id=workspace.project.identity.project_id,
        building_reference=ObjectReference(
            object_id=building_context.reference.object_id,
            revision_id=building_context.reference.revision_id,
            object_type="BuildingModelSpecification",
        ),
    )
    target_directory = (
        workspace.paths.config
        / "ma_technical"
        / "revisions"
        / building_context.reference.object_id
        / specification.technical_model_id
    )
    revision = release_technical_model(
        specification,
        revision_id="TECH-000001-REV-000001",
        target_dir=target_directory,
    )
    revision_path = target_directory / "TECH-000001-REV-000001.yaml"
    handover = build_released_technical_handover(revision)

    stored_revision, stored_handover = store_active_technical_revision(
        workspace,
        revision_path=revision_path,
    )
    reloaded = load_active_technical_revision(workspace, building_context.reference)

    assert reloaded is not None
    assert stored_revision == revision
    assert stored_handover.handover_content_hash == handover.handover_content_hash
    reloaded_revision, reloaded_handover, reloaded_path = reloaded
    assert reloaded_revision.content_hash == revision.content_hash
    assert reloaded_handover.handover_content_hash == handover.handover_content_hash
    assert reloaded_path == revision_path.resolve()

    changed_building_reference = ObjectReference(
        object_id=building_context.reference.object_id,
        revision_id="BUILDING-BI-LOD1-V3",
        object_type="BuildingModelSpecification",
    )
    with pytest.raises(StaleActiveTechnicalRevisionError):
        load_active_technical_revision(workspace, changed_building_reference)


def test_active_revision_reference_blocks_path_escape(tmp_path):
    workspace = _workspace(tmp_path)
    save_project_module_config(
        workspace,
        "ma_technical",
        {
            "schema_version": "1.0",
            "project_id": workspace.project.identity.project_id,
            "active_v2_revisions_by_building": {
                "BUILDING-BI-LOD1-0001": {
                    "relative_revision_path": "../../outside.yaml",
                }
            },
        },
    )

    with pytest.raises(ValueError, match="ausserhalb"):
        load_active_technical_revision(
            workspace,
            ObjectReference(
                object_id="BUILDING-BI-LOD1-0001",
                revision_id="BUILDING-BI-LOD1-V2",
                object_type="BuildingModelSpecification",
            ),
        )


def test_active_revision_store_rejects_noncanonical_paths_before_loading(tmp_path):
    workspace = _workspace(tmp_path)
    outside_path = workspace.paths.root.parent / "outside-revision.yaml"

    with pytest.raises(ValueError, match="kanonischen Workspace-Revisionspfads"):
        store_active_technical_revision(workspace, revision_path=outside_path)


def test_active_revision_store_rejects_a_wrong_internal_revision_path(tmp_path):
    workspace = _workspace(tmp_path)
    _save_building_selection(workspace)
    building_context = resolve_selected_building_context(workspace)
    specification = replace(
        load_synthetic_v2_reference_technical_spec(),
        technical_model_id="TECH-000001",
        project_id=workspace.project.identity.project_id,
        building_reference=building_context.reference,
    )
    wrong_directory = workspace.paths.config / "ma_technical" / "revisions" / "wrong"
    release_technical_model(
        specification,
        revision_id="TECH-000001-REV-000001",
        target_dir=wrong_directory,
    )

    with pytest.raises(ValueError, match="kanonischen Pfad ihrer IDs"):
        store_active_technical_revision(
            workspace,
            revision_path=wrong_directory / "TECH-000001-REV-000001.yaml",
        )
