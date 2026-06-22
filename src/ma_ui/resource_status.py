"""UI-neutrale Ressourcenuebersicht fuer geplante Modulansichten."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ma_analyse.core.config import PROJECT_ROOT
from ma_workflow import resolve_step_key

IGNORED_FILE_NAMES = {".gitkeep"}
IGNORED_DIR_NAMES = {"__pycache__"}


@dataclass(frozen=True, slots=True)
class ResourceSpec:
    """Beschreibt eine Projektressource, die in der UI geprueft werden kann."""

    label: str
    relative_path: str
    note: str


@dataclass(frozen=True, slots=True)
class ResourceStatus:
    """Beschreibt den aktuellen lokalen Zustand einer Projektressource."""

    label: str
    relative_path: str
    exists: bool
    file_count: int
    directory_count: int
    status: str
    note: str


RESOURCE_SPECS_BY_STEP: dict[str, tuple[ResourceSpec, ...]] = {
    "parameters": (
        ResourceSpec(
            "Parameterkatalog",
            "config/ma_variants/parameters/example_parameters.yaml",
            "Aktuelle Parameterlogik liegt noch in ma_variants.",
        ),
        ResourceSpec(
            "Optionskatalog",
            "config/ma_variants/options/example_options.yaml",
            "Optionen werden aktuell vom Variantenmodul importiert.",
        ),
        ResourceSpec(
            "Namensregeln",
            "config/ma_variants/naming/example_naming_rules.yaml",
            "Relevante Vorarbeit fuer spaetere ma_parameters-Extraktion.",
        ),
    ),
    "building": (
        ResourceSpec(
            "IDA-Rohdaten und Zonen",
            "data/ma_analyse/ida_imports",
            "Der Ordner enthaelt aktuell die lokalen IDA-Importdaten.",
        ),
        ResourceSpec(
            "Aufbereitete Analyse-Datenbank",
            "data/ma_analyse/database",
            "Wird von ma_analyse nach Prepare-Schritten befuellt.",
        ),
    ),
    "simulation_setup": (
        ResourceSpec(
            "Systemtemplates",
            "config/ma_variants/systems/example_system_templates.yaml",
            "Vorarbeit fuer technische Systementscheidungen.",
        ),
        ResourceSpec(
            "IDA-Exportkonfiguration",
            "config/ma_variants/export/example_ida_export.yaml",
            "Vorhandene Konfiguration fuer spaetere Simulationsuebergabe.",
        ),
    ),
    "export_simulation": (
        ResourceSpec(
            "IDA-Exportkonfiguration",
            "config/ma_variants/export/example_ida_export.yaml",
            "Vorhandene IDA-ICE-Konfiguration fuer den allgemeinen Exportadapter.",
        ),
        ResourceSpec(
            "IDA-Exportordner",
            "data/ma_variants/ida_exports",
            "Bestehende Zielstruktur fuer exportierte Simulationspakete.",
        ),
    ),
    "import_simulation": (
        ResourceSpec(
            "IDA-Importdaten",
            "data/ma_analyse/ida_imports",
            "Aktueller Rohdatenordner des IDA-ICE-Importadapters.",
        ),
        ResourceSpec(
            "Analyse-Datenbankordner",
            "data/ma_analyse/database",
            "Ziel fuer aufbereitete CSV-/Excel-Daten.",
        ),
        ResourceSpec(
            "Analyseberichte",
            "data/ma_analyse/reports",
            "Berichtsordner fuer spaetere Import-/Pruefberichte.",
        ),
    ),
    "feedback": (
        ResourceSpec(
            "Planstatus",
            "docs/project/plans/PLAN_STATUS.md",
            "Aktive Aufgaben- und Plansteuerung.",
        ),
        ResourceSpec(
            "Offene Nutzerentscheidungen",
            "docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md",
            "Entscheidungsliste fuer Rueckfragen vor groesseren Umbauten.",
        ),
        ResourceSpec(
            "Analyseberichte",
            "data/ma_analyse/reports",
            "Moegliche Quelle fuer spaetere Rueckfuehrung von Auffaelligkeiten.",
        ),
    ),
}


def _count_directory(path: Path) -> tuple[int, int]:
    """Zaehlt relevante Dateien und Unterordner robust und ohne Fachlogik."""
    file_count = 0
    directory_count = 0
    try:
        children = tuple(path.iterdir())
    except OSError:
        return 0, 0

    for child in children:
        if child.is_dir():
            if child.name in IGNORED_DIR_NAMES:
                continue
            directory_count += 1
            nested_files, nested_dirs = _count_directory(child)
            file_count += nested_files
            directory_count += nested_dirs
        elif child.is_file() and child.name not in IGNORED_FILE_NAMES:
            file_count += 1
    return file_count, directory_count


def resource_status(spec: ResourceSpec, *, project_root: Path = PROJECT_ROOT) -> ResourceStatus:
    """Prueft eine einzelne Ressource relativ zum Projekt-Root."""
    path = project_root / spec.relative_path
    if not path.exists():
        return ResourceStatus(
            label=spec.label,
            relative_path=spec.relative_path,
            exists=False,
            file_count=0,
            directory_count=0,
            status="fehlt",
            note=spec.note,
        )

    if path.is_file():
        return ResourceStatus(
            label=spec.label,
            relative_path=spec.relative_path,
            exists=True,
            file_count=1,
            directory_count=0,
            status="vorhanden",
            note=spec.note,
        )

    file_count, directory_count = _count_directory(path)
    return ResourceStatus(
        label=spec.label,
        relative_path=spec.relative_path,
        exists=True,
        file_count=file_count,
        directory_count=directory_count,
        status="vorhanden" if file_count else "Struktur vorhanden",
        note=spec.note,
    )


def resource_statuses_for_step(step_key: str, *, project_root: Path = PROJECT_ROOT) -> tuple[ResourceStatus, ...]:
    """Gibt Ressourcenstatuswerte fuer einen Workflow-Schritt zurueck."""
    specs = RESOURCE_SPECS_BY_STEP.get(resolve_step_key(step_key), ())
    return tuple(resource_status(spec, project_root=project_root) for spec in specs)


def resource_status_rows(step_key: str, *, project_root: Path = PROJECT_ROOT) -> list[dict[str, str | int]]:
    """Bereitet Ressourcenstatuswerte fuer eine Streamlit-Tabelle auf."""
    return [
        {
            "Bereich": status.label,
            "Pfad": status.relative_path,
            "Status": status.status,
            "Dateien": status.file_count,
            "Ordner": status.directory_count,
            "Hinweis": status.note,
        }
        for status in resource_statuses_for_step(step_key, project_root=project_root)
    ]
