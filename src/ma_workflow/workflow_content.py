"""Lesender Adapter fuer die fachlichen Workflow-Steckbriefe.

Die technischen Stammdaten bleiben im Workflow-Katalog. Dieser Adapter stellt
nur die erklärenden Markdown-Inhalte für die nutzungsorientierte UI bereit.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .catalog import list_module_definitions, resolve_module_key

WORKFLOW_DOCUMENTATION_ROOT = Path(__file__).resolve().parents[2] / "docs" / "project" / "workflow"
WORKFLOW_MODULE_DOCUMENTATION_ROOT = WORKFLOW_DOCUMENTATION_ROOT / "modules"


@dataclass(frozen=True, slots=True)
class WorkflowModuleGuide:
    """Ein aus Markdown geladener, nutzungsorientierter Modulsteckbrief."""

    module_key: str
    path: Path
    markdown: str


def workflow_module_documentation_path(module_key: str) -> Path:
    """Gibt den stabilen Markdown-Pfad eines katalogisierten Moduls zurück."""

    canonical_key = resolve_module_key(module_key)
    filename = canonical_key.replace(".", "__") + ".md"
    return WORKFLOW_MODULE_DOCUMENTATION_ROOT / filename


def load_workflow_module_guide(module_key: str) -> WorkflowModuleGuide:
    """Lädt einen Modulsteckbrief und prüft seine zugehörige Modul-ID."""

    canonical_key = resolve_module_key(module_key)
    path = workflow_module_documentation_path(canonical_key)
    markdown = path.read_text(encoding="utf-8")
    marker = f"Modul-ID: `{canonical_key}`"
    if marker not in markdown:
        raise ValueError(f"Workflow-Steckbrief ohne passende Modul-ID: {path}")
    return WorkflowModuleGuide(module_key=canonical_key, path=path, markdown=markdown)


def workflow_module_summary(module_key: str) -> str:
    """Liest die kurze Ablaufrolle für eine Workflowkarte aus dem Steckbrief."""

    markdown = load_workflow_module_guide(module_key).markdown
    role_marker = "## Rolle im Ablauf\n"
    if role_marker not in markdown:
        raise ValueError(f"Workflow-Steckbrief ohne Ablaufrolle: {module_key}")
    role_section = markdown.split(role_marker, maxsplit=1)[1].split("\n## ", maxsplit=1)[0].strip()
    return role_section.split("\n\n", maxsplit=1)[0]


def missing_workflow_module_guides() -> tuple[str, ...]:
    """Nennt katalogisierte Module, deren fachlicher Steckbrief fehlt."""

    return tuple(
        module.module_key
        for module in list_module_definitions()
        if not workflow_module_documentation_path(module.module_key).is_file()
    )
