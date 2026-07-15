"""Tests for P011-S1a's pure project-model contracts."""

from __future__ import annotations

import ast
import json
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from ma_project import (
    Project,
    ProjectContext,
    ProjectIdentity,
    ProjectInvestigation,
    ProjectLocation,
    project_context_from_project,
    project_from_payload,
    project_to_payload,
)

CREATED_AT = datetime(2026, 7, 15, 9, 30, tzinfo=UTC)
UPDATED_AT = datetime(2026, 7, 15, 10, 45, tzinfo=UTC)


def _project() -> Project:
    """Build a fully synthetic, fixed-time project fixture."""
    return Project(
        identity=ProjectIdentity(
            project_id="PRJ-000042",
            title="Synthetische Referenzuntersuchung",
            short_name="Referenz",
            description="Ausschliesslich Testdaten ohne reale Projektinhalte.",
            project_type="Masterarbeit",
            author="Testautor",
            organization="Testorganisation",
        ),
        created_at=CREATED_AT,
        updated_at=UPDATED_AT,
        location=ProjectLocation(
            country_code="DE",
            display_name="Synthetischer Standort",
            postal_code="00000",
            city="Beispielstadt",
            street="Testallee",
            house_number="0",
            latitude_deg=0.0,
            longitude_deg=0.0,
            elevation_m=0.0,
            timezone="Etc/UTC",
            notes="Keine Wetterdaten oder TRY-Referenz.",
        ),
        investigation=ProjectInvestigation(
            objective="Nachvollziehbaren Testfall beschreiben.",
            research_question="Bleibt der Projektvertrag rein und reproduzierbar?",
            reference_case_description="Synthetischer Referenzfall.",
            scope="Nur Projektstammdaten.",
            exclusions=("Keine Assets", "Keine Fachmodelle"),
            methodology_note="Reine Modellvalidierung.",
            notes="Keine reale Untersuchung.",
        ),
    )


def test_project_context_exposes_minimal_reading_contract():
    project = _project()

    context = project_context_from_project(project)

    assert context == ProjectContext(
        project_id="PRJ-000042",
        title="Synthetische Referenzuntersuchung",
        short_name="Referenz",
        location=project.location,
    )
    assert context.location == project.location


@pytest.mark.parametrize(
    ("project_id", "title", "short_name"),
    (
        ("PRJ-42", "Titel", "Kurz"),
        ("prj-000042", "Titel", "Kurz"),
        ("PRJ-ABCDEF", "Titel", "Kurz"),
        ("PRJ-１２３４５６", "Titel", "Kurz"),
        ("PRJ-000042", "", "Kurz"),
        ("PRJ-000042", "Titel", ""),
    ),
)
def test_project_identity_rejects_invalid_ids_and_required_text(
    project_id: str,
    title: str,
    short_name: str,
):
    with pytest.raises(ValueError):
        ProjectIdentity(project_id=project_id, title=title, short_name=short_name)


@pytest.mark.parametrize(
    "location_kwargs",
    (
        {"country_code": ""},
        {"country_code": "Germany", "display_name": "Synthetisch"},
        {"country_code": "DE"},
        {"country_code": "DE", "display_name": "Synthetisch", "latitude_deg": 90.1},
        {"country_code": "DE", "display_name": "Synthetisch", "latitude_deg": -90.1},
        {"country_code": "DE", "display_name": "Synthetisch", "longitude_deg": 180.1},
        {"country_code": "DE", "display_name": "Synthetisch", "longitude_deg": -180.1},
        {"country_code": "DE", "display_name": "Synthetisch", "latitude_deg": 48.5},
        {"country_code": "DE", "display_name": "Synthetisch", "longitude_deg": 13.4},
    ),
)
def test_project_location_requires_valid_country_name_or_city_and_coordinate_pair(location_kwargs: dict):
    with pytest.raises(ValueError):
        ProjectLocation(**location_kwargs)


def test_project_location_accepts_city_without_display_name():
    location = ProjectLocation(country_code="DE", city="Synthetische Stadt")

    assert location.display_name == ""
    assert location.city == "Synthetische Stadt"


@pytest.mark.parametrize(
    ("created_at", "updated_at"),
    (
        (datetime(2026, 7, 15, 9, 30), UPDATED_AT),
        (CREATED_AT, datetime(2026, 7, 15, 10, 45)),
        (UPDATED_AT, CREATED_AT),
    ),
)
def test_project_rejects_naive_or_reverse_timestamps(created_at: datetime, updated_at: datetime):
    with pytest.raises(ValueError):
        Project(
            identity=ProjectIdentity("PRJ-000042", "Synthetisch", "Test"),
            created_at=created_at,
            updated_at=updated_at,
        )


def test_project_rejects_reverse_timestamp_across_dst_fold():
    berlin = ZoneInfo("Europe/Berlin")
    created_at = datetime(2026, 10, 25, 2, 15, tzinfo=berlin, fold=1)
    updated_at = datetime(2026, 10, 25, 2, 45, tzinfo=berlin, fold=0)

    with pytest.raises(ValueError):
        Project(
            identity=ProjectIdentity("PRJ-000042", "Synthetisch", "Test"),
            created_at=created_at,
            updated_at=updated_at,
        )


def test_project_models_are_immutable():
    project = _project()

    with pytest.raises(FrozenInstanceError):
        project.updated_at = CREATED_AT
    with pytest.raises(FrozenInstanceError):
        project.identity.title = "Geaendert"
    with pytest.raises(FrozenInstanceError):
        project.location.city = "Andere Stadt"
    with pytest.raises(FrozenInstanceError):
        project.investigation.scope = "Andere Abgrenzung"


def test_project_payload_is_json_compatible_stable_and_round_trips():
    project = _project()

    payload = project_to_payload(project)

    assert payload == project_to_payload(project)
    assert json.loads(json.dumps(payload, sort_keys=True)) == payload
    assert payload["investigation"]["exclusions"] == ["Keine Assets", "Keine Fachmodelle"]
    assert project_from_payload(payload) == project


@pytest.mark.parametrize(
    "payload",
    (
        {},
        {"identity": "kein Objekt"},
        {
            "identity": {
                "project_id": "PRJ-000042",
                "title": "Synthetisch",
                "short_name": "Test",
            },
            "created_at": "2026-07-15T09:30:00",
            "updated_at": "2026-07-15T10:45:00+00:00",
        },
    ),
)
def test_project_from_payload_rejects_malformed_or_naive_data(payload: dict):
    with pytest.raises(ValueError):
        project_from_payload(payload)


def _is_type_checking_guard(condition: ast.expr) -> bool:
    return isinstance(condition, ast.Name) and condition.id == "TYPE_CHECKING"


class _RuntimeDomainImportCollector(ast.NodeVisitor):
    """Collect only absolute domain imports that execute at runtime."""

    def __init__(self) -> None:
        self.module_names: list[str] = []

    def visit_If(self, node: ast.If) -> None:  # noqa: N802
        if _is_type_checking_guard(node.test):
            for statement in node.orelse:
                self.visit(statement)
            return
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        self.module_names.extend(alias.name for alias in node.names)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        if node.level == 0 and node.module:
            self.module_names.append(node.module)


def test_project_package_has_no_runtime_domain_imports_except_ma_core():
    source_root = Path(__file__).resolve().parents[1] / "src" / "ma_project"
    imported_domain_packages: set[str] = set()

    for source_file in source_root.rglob("*.py"):
        syntax_tree = ast.parse(source_file.read_text(encoding="utf-8"))
        collector = _RuntimeDomainImportCollector()
        collector.visit(syntax_tree)
        imported_domain_packages.update(
            module_name.split(".", maxsplit=1)[0]
            for module_name in collector.module_names
            if module_name.startswith("ma_")
        )

    assert imported_domain_packages <= {"ma_core"}
