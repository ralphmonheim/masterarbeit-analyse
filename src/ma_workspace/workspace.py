"""Lokale Projekt-Workspaces, Projektdateien und Registry fuer P035."""

from __future__ import annotations

import os
import re
import secrets
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import yaml

from ma_core import load_configuration_file
from ma_project import Project, ProjectSettings, project_from_payload, project_to_payload

PROJECT_FILE_NAME = "project.yaml"
WORKSPACE_SCHEMA_VERSION = "1.0"
REGISTRY_SCHEMA_VERSION = "1.0"
KNOWN_V1_PROJECT_NAMES = ("Masterarbeit-Analyse", "Demo-Project1")
ALLOWED_GALLERY_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
_PROJECT_ID_PATTERN = re.compile(r"PRJ-[0-9]{6}\Z")
_MODULE_KEY_PATTERN = re.compile(r"ma_[a-z0-9_]+\Z")
_WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


def validate_workspace_project_name(name: str) -> str:
    """Gibt einen sicheren Windows-Ordnernamen zurueck."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Projektname darf nicht leer sein.")
    if name != name.strip():
        raise ValueError("Projektname darf nicht mit Leerzeichen beginnen oder enden.")
    if name in {".", ".."} or any(character in name for character in '<>:"/\\|?*\x00'):
        raise ValueError("Projektname darf keine Pfadangaben oder unzulaessigen Windows-Zeichen enthalten.")
    if name.endswith((".", " ")) or any(ord(character) < 32 for character in name):
        raise ValueError("Projektname endet unzulaessig oder enthaelt Steuerzeichen.")
    if name.split(".", maxsplit=1)[0].upper() in _WINDOWS_RESERVED_NAMES:
        raise ValueError("Projektname verwendet einen reservierten Windows-Dateinamen.")
    return name


def create_project_id(existing_ids: tuple[str, ...] | list[str] = ()) -> str:
    """Erzeugt eine P011-kompatible Projekt-ID ohne bekannte Kollision."""
    known_ids = set(existing_ids)
    for _attempt in range(100):
        candidate = f"PRJ-{secrets.randbelow(1_000_000):06d}"
        if candidate not in known_ids:
            return candidate
    raise RuntimeError("Es konnte keine freie Projekt-ID erzeugt werden.")


@dataclass(frozen=True, slots=True)
class WorkspacePaths:
    """Alle von einem lokalen Projekt-Workspace besessenen Pfade."""

    root: Path
    project_file: Path
    assets: Path
    gallery: Path
    config: Path
    output: Path

    @classmethod
    def for_root(cls, root: str | Path) -> WorkspacePaths:
        candidate = Path(root)
        if not candidate.is_absolute():
            raise ValueError("Workspace-Pfad muss absolut sein.")
        normalized_root = candidate.resolve()
        return cls(
            root=normalized_root,
            project_file=normalized_root / PROJECT_FILE_NAME,
            assets=normalized_root / "assets",
            gallery=normalized_root / "assets" / "gallery",
            config=normalized_root / "config",
            output=normalized_root / "output",
        )

    def __post_init__(self) -> None:
        root = self.root.resolve()
        expected_paths = (
            root,
            root / PROJECT_FILE_NAME,
            root / "assets",
            root / "assets" / "gallery",
            root / "config",
            root / "output",
        )
        if (self.root, self.project_file, self.assets, self.gallery, self.config, self.output) != expected_paths:
            raise ValueError("Workspace-Pfade muessen der minimalen Projektstruktur entsprechen.")


@dataclass(frozen=True, slots=True)
class ProjectWorkspace:
    """Validierte Verbindung zwischen P011-Projektdaten und lokalem Ordner."""

    project: Project
    settings: ProjectSettings
    paths: WorkspacePaths

    def __post_init__(self) -> None:
        if not isinstance(self.project, Project):
            raise ValueError("project muss ein Project-Objekt sein.")
        if not isinstance(self.settings, ProjectSettings):
            raise ValueError("settings muss ein ProjectSettings-Objekt sein.")
        if not isinstance(self.paths, WorkspacePaths):
            raise ValueError("paths muss ein WorkspacePaths-Objekt sein.")


@dataclass(frozen=True, slots=True)
class RegistryEntry:
    """Bewusst kleine lokale Referenz auf ein bekanntes Projekt."""

    project_id: str
    name: str
    path: Path

    def __post_init__(self) -> None:
        if not isinstance(self.project_id, str) or not _PROJECT_ID_PATTERN.fullmatch(self.project_id):
            raise ValueError("project_id muss dem Format PRJ-000001 entsprechen.")
        validate_workspace_project_name(self.name)
        raw_path = Path(self.path)
        if not raw_path.is_absolute():
            raise ValueError("Registry-Pfad muss absolut sein.")
        object.__setattr__(self, "path", raw_path.resolve())

    @property
    def available(self) -> bool:
        """Prueft Ordner, Projekt-ID und Projektname gemeinsam."""
        try:
            workspace = load_project_workspace(self.path)
        except (FileNotFoundError, ValueError, OSError):
            return False
        return (
            workspace.project.identity.project_id == self.project_id
            and workspace.project.identity.title == self.name
        )


@dataclass(frozen=True, slots=True)
class KnownProjectSuggestion:
    """Namensvorschlag fuer ein noch nicht zwingend registriertes V1-Projekt."""

    name: str
    path: Path

    def __post_init__(self) -> None:
        validate_workspace_project_name(self.name)
        raw_path = Path(self.path)
        if not raw_path.is_absolute():
            raise ValueError("Vorschlagspfad muss absolut sein.")
        object.__setattr__(self, "path", raw_path.resolve())

    @property
    def available(self) -> bool:
        try:
            workspace = load_project_workspace(self.path)
        except (FileNotFoundError, ValueError, OSError):
            return False
        return workspace.project.identity.title == self.name


class FolderDialogAdapter(Protocol):
    """Injizierbare Grenze fuer einen nativen Ordnerdialog."""

    def choose_folder(self, *, initial_directory: Path | None = None) -> Path | None:
        """Liefert einen Ordner oder ``None`` bei Abbruch."""


def known_v1_project_suggestions(projects_directory: str | Path) -> tuple[KnownProjectSuggestion, ...]:
    parent = Path(projects_directory)
    if not parent.is_absolute():
        raise ValueError("Projektbasis muss absolut sein.")
    parent = parent.resolve()
    return tuple(KnownProjectSuggestion(name=name, path=parent / name) for name in KNOWN_V1_PROJECT_NAMES)


def select_project_parent(
    dialog: FolderDialogAdapter,
    *,
    initial_directory: str | Path | None = None,
) -> Path | None:
    """Waehlt und validiert einen uebergeordneten Zielordner."""
    initial_path = None
    if initial_directory is not None:
        initial_path = Path(initial_directory)
        if not initial_path.is_absolute():
            raise ValueError("initial_directory muss absolut sein.")
        initial_path = initial_path.resolve()
    selected = dialog.choose_folder(initial_directory=initial_path)
    if selected is None:
        return None
    raw_parent = Path(selected)
    if not raw_parent.is_absolute():
        raise ValueError("Der ausgewaehlte Zielordner muss absolut sein.")
    parent = raw_parent.resolve()
    if not parent.is_dir():
        raise ValueError("Der ausgewaehlte Zielordner existiert nicht.")
    if not os.access(parent, os.W_OK):
        raise PermissionError("Der ausgewaehlte Zielordner ist nicht beschreibbar.")
    return parent


def create_project_workspace(
    project: Project,
    parent_directory: str | Path,
    *,
    simulation_program_key: str,
    naming_profile_reference: str | None = None,
    project_name: str | None = None,
) -> ProjectWorkspace:
    """Legt die minimale P035-Struktur ohne Ueberschreiben an."""
    if not isinstance(project, Project):
        raise TypeError("project muss ein Project-Objekt sein.")
    if project_name is not None and project_name != project.identity.title:
        raise ValueError("Projektordner und Projekttitel muessen denselben Namen verwenden.")
    folder_name = validate_workspace_project_name(project.identity.title)
    raw_parent = Path(parent_directory)
    if not raw_parent.is_absolute():
        raise ValueError("Der Zielordner muss absolut sein.")
    parent = raw_parent.resolve()
    if not parent.is_dir():
        raise ValueError("Der Zielordner existiert nicht.")
    if not os.access(parent, os.W_OK):
        raise PermissionError("Der Zielordner ist nicht beschreibbar.")
    settings = ProjectSettings(
        simulation_program_key=simulation_program_key,
        naming_profile_reference=naming_profile_reference,
    )
    paths = WorkspacePaths.for_root(parent / folder_name)
    if paths.root.exists():
        raise FileExistsError("Der Projektordner existiert bereits. Bitte einen anderen Projektnamen verwenden.")

    paths.root.mkdir()
    try:
        paths.gallery.mkdir(parents=True)
        paths.config.mkdir()
        paths.output.mkdir()
        workspace = ProjectWorkspace(project=project, settings=settings, paths=paths)
        _write_project_file(workspace, require_new=True)
    except Exception:
        _rollback_new_workspace(paths)
        raise
    return workspace


def create_project_workspace_from_dialog(
    project: Project,
    dialog: FolderDialogAdapter,
    *,
    simulation_program_key: str,
    naming_profile_reference: str | None = None,
    project_name: str | None = None,
    initial_directory: str | Path | None = None,
) -> ProjectWorkspace | None:
    parent = select_project_parent(dialog, initial_directory=initial_directory)
    if parent is None:
        return None
    return create_project_workspace(
        project,
        parent,
        simulation_program_key=simulation_program_key,
        naming_profile_reference=naming_profile_reference,
        project_name=project_name,
    )


def load_project_workspace(root: str | Path) -> ProjectWorkspace:
    """Laedt und validiert eine P035-Projektdatei ohne Aenderung."""
    paths = WorkspacePaths.for_root(root)
    if not paths.root.is_dir():
        raise FileNotFoundError(f"Projektordner nicht gefunden: {paths.root}")
    if paths.root.is_symlink() or paths.project_file.is_symlink():
        raise ValueError("Symbolische Verknuepfungen sind fuer Projekt-Workspaces nicht zulaessig.")
    if not paths.project_file.is_file():
        raise FileNotFoundError(f"Projektdatei nicht gefunden: {paths.project_file}")
    for required_directory in (paths.gallery, paths.config, paths.output):
        if not required_directory.is_dir():
            raise ValueError(f"Projektstruktur ist unvollstaendig: {required_directory}")
    payload = load_configuration_file(paths.project_file)
    if set(payload) != {"schema_version", "project", "settings"}:
        raise ValueError("project.yaml muss schema_version, project und settings enthalten.")
    if payload["schema_version"] != WORKSPACE_SCHEMA_VERSION:
        raise ValueError("project.yaml hat eine nicht unterstuetzte schema_version.")
    if not isinstance(payload["project"], dict) or not isinstance(payload["settings"], dict):
        raise ValueError("project.yaml muss Projekt- und Einstellungsobjekt enthalten.")
    settings_payload = payload["settings"]
    if set(settings_payload) - {"simulation_program_key", "naming_profile_reference"}:
        raise ValueError("project.yaml enthaelt unbekannte Workspace-Einstellungen.")
    settings = ProjectSettings(
        simulation_program_key=settings_payload.get("simulation_program_key"),
        naming_profile_reference=settings_payload.get("naming_profile_reference"),
    )
    return ProjectWorkspace(
        project=project_from_payload(payload["project"]),
        settings=settings,
        paths=paths,
    )


def save_project_workspace(workspace: ProjectWorkspace) -> None:
    """Speichert Stammdaten und Auswahlreferenzen atomar am selben Ort."""
    existing = load_project_workspace(workspace.paths.root)
    if existing.project.identity.project_id != workspace.project.identity.project_id:
        raise PermissionError("Die Projekt-ID einer bestehenden Projektdatei darf nicht geaendert werden.")
    if workspace.paths.root.name != workspace.project.identity.title:
        raise ValueError(
            "Der Projektname ist in V1 an den Projektordner gebunden und darf nicht direkt geaendert werden."
        )
    _write_project_file(workspace, require_new=False)


def registry_entry_from_workspace(
    workspace: ProjectWorkspace,
) -> RegistryEntry:
    return RegistryEntry(
        project_id=workspace.project.identity.project_id,
        name=workspace.project.identity.title,
        path=workspace.paths.root,
    )


def load_workspace_registry(registry_file: str | Path) -> tuple[RegistryEntry, ...]:
    path = Path(registry_file)
    if not path.exists():
        return ()
    payload = load_configuration_file(path)
    if set(payload) != {"schema_version", "entries"} or payload["schema_version"] != REGISTRY_SCHEMA_VERSION:
        raise ValueError("Registry hat ein ungueltiges Format oder eine ungueltige schema_version.")
    raw_entries = payload["entries"]
    if not isinstance(raw_entries, list):
        raise ValueError("Registry entries muss eine Liste sein.")
    entries = tuple(_registry_entry_from_payload(raw_entry) for raw_entry in raw_entries)
    _validate_unique_registry_entries(entries)
    return entries


def save_workspace_registry(
    entries: tuple[RegistryEntry, ...] | list[RegistryEntry],
    registry_file: str | Path,
) -> None:
    validated_entries = tuple(entries)
    _validate_unique_registry_entries(validated_entries)
    path = Path(registry_file)
    if path.suffix.lower() not in {".yaml", ".yml"}:
        raise ValueError("Die lokale Registry muss als YAML-Datei gespeichert werden.")
    payload = {
        "schema_version": REGISTRY_SCHEMA_VERSION,
        "entries": [_registry_entry_to_payload(entry) for entry in validated_entries],
    }
    _atomic_write_yaml(path, payload, require_new=False)


def upsert_registry_entry(
    registry_file: str | Path,
    entry: RegistryEntry,
) -> tuple[RegistryEntry, ...]:
    entries = list(load_workspace_registry(registry_file))
    for existing in entries:
        if existing.project_id == entry.project_id:
            if existing.path != entry.path:
                raise ValueError("Die Projekt-ID ist bereits mit einem anderen Ordner registriert.")
            entries.remove(existing)
            break
    entries.insert(0, entry)
    save_workspace_registry(entries, registry_file)
    return tuple(entries)


def remove_registry_entry(
    registry_file: str | Path,
    project_id: str,
    *,
    confirmed: bool,
) -> tuple[RegistryEntry, ...]:
    """Entfernt nur die Registry-Referenz nach expliziter Bestaetigung."""
    if not confirmed:
        raise PermissionError("Das Entfernen des Registry-Eintrags wurde nicht bestaetigt.")
    if not isinstance(project_id, str) or not _PROJECT_ID_PATTERN.fullmatch(project_id):
        raise ValueError("project_id muss dem Format PRJ-000001 entsprechen.")
    remaining = tuple(entry for entry in load_workspace_registry(registry_file) if entry.project_id != project_id)
    save_workspace_registry(remaining, registry_file)
    return remaining


def list_gallery_images(workspace: ProjectWorkspace) -> tuple[Path, ...]:
    """Listet nur die fuer die V1-Galerie erlaubten Bilddateien."""
    return tuple(
        sorted(
            (
                path
                for path in workspace.paths.gallery.iterdir()
                if path.is_file() and path.suffix.lower() in ALLOWED_GALLERY_SUFFIXES
            ),
            key=lambda path: path.name.lower(),
        )
    )


def save_gallery_image(
    workspace: ProjectWorkspace,
    file_name: str,
    content: bytes,
) -> Path:
    """Speichert ein lokales Galeriebild ohne vorhandene Datei zu ueberschreiben."""
    target = _gallery_target(workspace, file_name)
    if not isinstance(content, bytes) or not content:
        raise ValueError("Das Galeriebild darf nicht leer sein.")
    if target.exists():
        raise FileExistsError(f"Galeriebild existiert bereits: {target.name}")
    with target.open("xb") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    return target


def remove_gallery_image(
    workspace: ProjectWorkspace,
    file_name: str,
    *,
    confirmed: bool,
) -> None:
    """Entfernt genau ein Galeriebild nach expliziter Bestaetigung."""
    if not confirmed:
        raise PermissionError("Das Entfernen des Galeriebilds wurde nicht bestaetigt.")
    target = _gallery_target(workspace, file_name)
    if not target.is_file() or target.is_symlink():
        raise FileNotFoundError(f"Galeriebild nicht gefunden: {target.name}")
    target.unlink()


def project_module_config_path(workspace: ProjectWorkspace, module_key: str) -> Path:
    if not isinstance(module_key, str) or not _MODULE_KEY_PATTERN.fullmatch(module_key):
        raise ValueError("module_key muss dem Format ma_modul entsprechen.")
    return workspace.paths.config / f"{module_key}.yaml"


def save_project_module_config(
    workspace: ProjectWorkspace,
    module_key: str,
    payload: dict[str, object],
) -> Path:
    """Speichert eine projektbezogene Fachkonfiguration atomar."""
    if not isinstance(payload, dict):
        raise TypeError("payload muss ein Dictionary sein.")
    target = project_module_config_path(workspace, module_key)
    _atomic_write_yaml(target, payload, require_new=False)
    return target


def load_project_module_config(
    workspace: ProjectWorkspace,
    module_key: str,
) -> dict[str, object] | None:
    target = project_module_config_path(workspace, module_key)
    if not target.exists():
        return None
    return load_configuration_file(target)


def _project_file_payload(workspace: ProjectWorkspace) -> dict[str, object]:
    return {
        "schema_version": WORKSPACE_SCHEMA_VERSION,
        "project": project_to_payload(workspace.project),
        "settings": {
            "simulation_program_key": workspace.settings.simulation_program_key,
            "naming_profile_reference": workspace.settings.naming_profile_reference,
        },
    }


def _gallery_target(workspace: ProjectWorkspace, file_name: str) -> Path:
    if not isinstance(file_name, str) or not file_name.strip() or Path(file_name).name != file_name:
        raise ValueError("Galeriedatei braucht einen einfachen Dateinamen.")
    if Path(file_name).suffix.lower() not in ALLOWED_GALLERY_SUFFIXES:
        raise ValueError("Erlaubte Galerieformate sind PNG, JPG/JPEG und WEBP.")
    target = (workspace.paths.gallery / file_name).resolve()
    if target.parent != workspace.paths.gallery.resolve():
        raise ValueError("Galeriedatei liegt ausserhalb des Projektordners.")
    return target


def _write_project_file(workspace: ProjectWorkspace, *, require_new: bool) -> None:
    _atomic_write_yaml(
        workspace.paths.project_file,
        _project_file_payload(workspace),
        require_new=require_new,
    )


def _atomic_write_yaml(path: Path, payload: dict[str, object], *, require_new: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if require_new and path.exists():
        raise FileExistsError(f"Datei existiert bereits: {path}")
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)
            handle.flush()
            os.fsync(handle.fileno())
            temporary_path = Path(handle.name)
        if require_new:
            try:
                os.link(temporary_path, path)
            except FileExistsError:
                raise FileExistsError(f"Datei existiert bereits: {path}") from None
            temporary_path.unlink()
        else:
            os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def _rollback_new_workspace(paths: WorkspacePaths) -> None:
    paths.project_file.unlink(missing_ok=True)
    for directory in (paths.gallery, paths.assets, paths.config, paths.output, paths.root):
        try:
            directory.rmdir()
        except OSError:
            continue


def _validate_unique_registry_entries(entries: tuple[RegistryEntry, ...]) -> None:
    seen_ids: set[str] = set()
    seen_paths: set[Path] = set()
    for entry in entries:
        if not isinstance(entry, RegistryEntry):
            raise TypeError("Registry darf nur RegistryEntry-Objekte enthalten.")
        if entry.project_id in seen_ids:
            raise ValueError(f"Registry enthaelt die Projekt-ID doppelt: {entry.project_id}.")
        if entry.path in seen_paths:
            raise ValueError(f"Registry enthaelt den Projektpfad doppelt: {entry.path}.")
        seen_ids.add(entry.project_id)
        seen_paths.add(entry.path)


def _registry_entry_to_payload(entry: RegistryEntry) -> dict[str, str]:
    return {"project_id": entry.project_id, "name": entry.name, "path": str(entry.path)}


def _registry_entry_from_payload(value: object) -> RegistryEntry:
    if not isinstance(value, dict) or set(value) - {"project_id", "name", "path"}:
        raise ValueError("Registry-Eintrag ist ungueltig.")
    if not {"project_id", "name", "path"} <= set(value):
        raise ValueError("Registry-Eintrag muss project_id, name und path enthalten.")
    return RegistryEntry(
        project_id=value["project_id"],
        name=value["name"],
        path=value["path"],
    )
