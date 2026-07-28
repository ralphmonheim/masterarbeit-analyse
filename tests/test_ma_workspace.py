"""Focused P035 tests for local, dependency-free project workspaces."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ma_project import Project, ProjectIdentity, ProjectLocation
from ma_workspace import (
    KnownProjectSuggestion,
    RegistryEntry,
    create_project_workspace,
    create_project_workspace_from_dialog,
    known_v1_project_suggestions,
    list_gallery_images,
    load_project_module_config,
    load_project_workspace,
    load_workspace_registry,
    remove_gallery_image,
    remove_registry_entry,
    save_gallery_image,
    save_project_module_config,
    save_workspace_registry,
    upsert_registry_entry,
    validate_workspace_project_name,
)


def _project(project_id: str = "PRJ-000042") -> Project:
    timestamp = datetime(2026, 7, 27, 10, 0, tzinfo=UTC)
    return Project(
        identity=ProjectIdentity(project_id, "Testprojekt", "Test"),
        created_at=timestamp,
        updated_at=timestamp,
        location=ProjectLocation(country_code="DE", city="Beispielstadt"),
    )


class _Dialog:
    def __init__(self, result: Path | None) -> None:
        self.result = result

    def choose_folder(self, *, initial_directory: Path | None = None) -> Path | None:
        return self.result


@pytest.mark.parametrize("name", ["", " ../unsafe", "A/B", r"A\\B", "CON", "project."])
def test_workspace_project_name_rejects_paths_and_windows_unsafe_names(name: str):
    with pytest.raises(ValueError):
        validate_workspace_project_name(name)


def test_create_workspace_writes_only_minimal_structure_and_round_trips(tmp_path: Path):
    tmp_path = tmp_path.resolve()
    workspace = create_project_workspace(
        _project(),
        tmp_path,
        simulation_program_key="ida_ice",
        naming_profile_reference="small_office_v1",
    )

    assert workspace.paths.project_file.is_file()
    assert workspace.paths.gallery.is_dir()
    assert workspace.paths.config.is_dir()
    assert workspace.paths.output.is_dir()
    assert load_project_workspace(workspace.paths.root) == workspace
    with pytest.raises(FrozenInstanceError):
        workspace.paths.root = tmp_path


def test_existing_target_folder_is_never_overwritten(tmp_path: Path):
    tmp_path = tmp_path.resolve()
    (tmp_path / "Testprojekt").mkdir()

    with pytest.raises(FileExistsError, match="existiert bereits"):
        create_project_workspace(_project(), tmp_path, simulation_program_key="ida_ice")


def test_dialog_cancel_does_not_create_a_project_file(tmp_path: Path):
    tmp_path = tmp_path.resolve()
    workspace = create_project_workspace_from_dialog(
        _project(),
        _Dialog(None),
        simulation_program_key="ida_ice",
    )

    assert workspace is None
    assert list(tmp_path.iterdir()) == []


def test_registry_rejects_duplicate_id_and_keeps_missing_project_visible(tmp_path: Path):
    tmp_path = tmp_path.resolve()
    registry_file = tmp_path / "registry.yaml"
    missing = RegistryEntry("PRJ-000010", "Fehlendes Projekt", tmp_path / "missing")
    duplicate = RegistryEntry("PRJ-000010", "Anderer Name", tmp_path / "other")
    available_workspace = create_project_workspace(
        _project("PRJ-000011"),
        tmp_path,
        simulation_program_key="ida_ice",
    )
    available = RegistryEntry("PRJ-000011", "Testprojekt", available_workspace.paths.root)

    with pytest.raises(ValueError, match="doppelt"):
        save_workspace_registry([missing, duplicate, available], registry_file)

    save_workspace_registry([missing, available], registry_file)
    entries = load_workspace_registry(registry_file)

    assert entries == (missing, available)
    assert entries[0].available is False
    assert entries[1].available is True


def test_removing_registry_entry_never_deletes_project_folder(tmp_path: Path):
    tmp_path = tmp_path.resolve()
    workspace = create_project_workspace(_project(), tmp_path, simulation_program_key="ida_ice")
    registry_file = tmp_path / "registry.yaml"
    entry = RegistryEntry("PRJ-000042", "Testprojekt", workspace.paths.root)
    save_workspace_registry([entry], registry_file)

    with pytest.raises(PermissionError, match="bestaetigt"):
        remove_registry_entry(registry_file, "PRJ-000042", confirmed=False)
    assert remove_registry_entry(registry_file, "PRJ-000042", confirmed=True) == ()
    assert workspace.paths.root.is_dir()


def test_known_v1_projects_are_visible_as_unavailable_when_not_yet_created(tmp_path: Path):
    tmp_path = tmp_path.resolve()
    entries = known_v1_project_suggestions(tmp_path)

    assert [entry.name for entry in entries] == ["Masterarbeit-Analyse", "Demo-Project1"]
    assert all(isinstance(entry, KnownProjectSuggestion) for entry in entries)
    assert all(entry.available is False for entry in entries)


def test_registry_availability_checks_project_identity_not_only_project_file(tmp_path: Path):
    tmp_path = tmp_path.resolve()
    workspace = create_project_workspace(_project(), tmp_path, simulation_program_key="ida_ice")

    wrong_id = RegistryEntry("PRJ-000099", "Testprojekt", workspace.paths.root)
    wrong_name = RegistryEntry("PRJ-000042", "Anderer Name", workspace.paths.root)

    assert wrong_id.available is False
    assert wrong_name.available is False


def test_upsert_rejects_same_id_for_different_folder(tmp_path: Path):
    tmp_path = tmp_path.resolve()
    registry_file = tmp_path / "registry.yaml"
    first = RegistryEntry("PRJ-000042", "Testprojekt", tmp_path / "first")
    second = RegistryEntry("PRJ-000042", "Testprojekt", tmp_path / "second")
    upsert_registry_entry(registry_file, first)

    with pytest.raises(ValueError, match="anderen Ordner"):
        upsert_registry_entry(registry_file, second)


def test_registry_entry_rejects_relative_path():
    with pytest.raises(ValueError, match="absolut"):
        RegistryEntry("PRJ-000042", "Testprojekt", Path("relative/project"))


def test_gallery_accepts_images_and_requires_confirmation_for_removal(tmp_path: Path):
    workspace = create_project_workspace(
        _project(),
        tmp_path.resolve(),
        simulation_program_key="ida_ice",
    )

    image_path = save_gallery_image(workspace, "ansicht.PNG", b"synthetic-image")

    assert list_gallery_images(workspace) == (image_path,)
    with pytest.raises(PermissionError, match="bestaetigt"):
        remove_gallery_image(workspace, image_path.name, confirmed=False)
    remove_gallery_image(workspace, image_path.name, confirmed=True)
    assert list_gallery_images(workspace) == ()


@pytest.mark.parametrize("file_name", ["../bild.png", "bild.gif", "bild"])
def test_gallery_rejects_unsafe_or_unsupported_names(tmp_path: Path, file_name: str):
    workspace = create_project_workspace(
        _project(),
        tmp_path.resolve(),
        simulation_program_key="ida_ice",
    )

    with pytest.raises(ValueError):
        save_gallery_image(workspace, file_name, b"synthetic-image")


def test_project_module_config_round_trips_inside_workspace(tmp_path: Path):
    workspace = create_project_workspace(
        _project(),
        tmp_path.resolve(),
        simulation_program_key="ida_ice",
    )

    target = save_project_module_config(
        workspace,
        "ma_parameters",
        {"schema_version": "1.0", "status": "draft"},
    )

    assert target == workspace.paths.config / "ma_parameters.yaml"
    assert load_project_module_config(workspace, "ma_parameters") == {
        "schema_version": "1.0",
        "status": "draft",
    }
