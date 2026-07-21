"""Contract tests for the repository-local Codex operating system."""

import subprocess
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_AGENTS = {
    "compliance_auditor",
    "implementation_engineer",
    "professor",
    "project_explorer",
    "quality_auditor",
}
READ_ONLY_AGENTS = {
    "compliance_auditor",
    "professor",
    "project_explorer",
    "quality_auditor",
}
EXPECTED_SKILLS = {
    "project-governance-workflow",
    "repo-release-workflow",
}
EXPECTED_SKILL_TRIGGERS = {
    "project-governance-workflow": (
        "aktualisieren",
        "tagesstart",
        "Guten Morgen, es ist ein neuer Tag.",
        "projektlage",
        "chat-stats",
        "chat-handover",
        "update planung",
        "plan aufnehmen",
        "projektinput aufnehmen",
        "entscheidung festhalten",
        "council analyse",
        "council review",
        "council compliance",
        "council umsetzen",
        "ohne council",
        "nur Tera",
        "mit Sol-Review",
    ),
    "repo-release-workflow": (
        "aktualisieren und tagesende direkt",
        "aktualisieren und direkt update repo",
        "update repo",
        "direkt update repo",
        "release check",
        "tagesende",
        "Gute Nacht.",
        "tagesende direkt",
        "Gute Nacht direkt.",
        "wochenabschluss",
        "Eine schoene Woche.",
    ),
}
CANONICAL_WORKFLOW_TRIGGERS = {trigger for triggers in EXPECTED_SKILL_TRIGGERS.values() for trigger in triggers} | {
    "aktualisiere tests"
}
ALLOWED_TRACKED_PROTECTED_PATHS = {
    "data/common/normen/README.md",
    "data/common/normen/current/.gitkeep",
    "data/common/normen/rounds/.gitkeep",
    "data/common/normen/rounds/round1_v0_1/.gitkeep",
    "data/common/normen/rounds/round1_v0_1/extracted/.gitkeep",
    "data/common/normen/rounds/round1_v0_1/incoming/.gitkeep",
    "data/common/normen/rounds/round1_v0_1/review/.gitkeep",
    "data/common/normen/templates/.gitkeep",
    "data/catalogs/documents/materials/.gitkeep",
    "data/catalogs/documents/products/.gitkeep",
    "data/catalogs/materials/.gitkeep",
    "data/catalogs/products/.gitkeep",
    "data/catalogs/sources/.gitkeep",
    "data/ma_analyse/ida_imports/.gitkeep",
    "data/ma_variants/ida_exports/.gitkeep",
}


def _load_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as file_handle:
        return tomllib.load(file_handle)


def _tracked_files() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return {line.strip().replace("\\", "/") for line in result.stdout.splitlines()}


def _tracked_markdown_files() -> set[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--", "*.md"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return {REPO_ROOT / line.strip() for line in result.stdout.splitlines() if line.strip()}


def _skill_frontmatter(skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    opening, separator, remainder = text.partition("\n---\n")
    assert separator, f"Missing YAML frontmatter terminator in {skill_file}"
    assert opening.startswith("---\n")
    frontmatter: dict[str, str] = {}
    for line in opening.removeprefix("---\n").splitlines():
        key, value = line.split(":", maxsplit=1)
        frontmatter[key.strip()] = value.strip()
    assert remainder.strip()
    return frontmatter


def test_project_codex_runtime_is_bounded() -> None:
    config = _load_toml(REPO_ROOT / ".codex" / "config.toml")

    assert config["approval_policy"] == "on-request"
    assert config["sandbox_mode"] == "workspace-write"
    assert config["sandbox_workspace_write"] == {"network_access": False}
    assert config["agents"] == {"max_threads": 3, "max_depth": 1}
    assert "mcp_servers" not in config
    assert "hooks" not in config


def test_project_agents_have_explicit_roles_and_sandboxes() -> None:
    agent_files = sorted((REPO_ROOT / ".codex" / "agents").glob("*.toml"))
    agents = {_load_toml(path)["name"]: _load_toml(path) for path in agent_files}

    assert set(agents) == EXPECTED_AGENTS
    for name, agent in agents.items():
        assert agent["description"]
        assert agent["developer_instructions"]
        assert agent["nickname_candidates"]
        assert "mcp_servers" not in agent
        if name in READ_ONLY_AGENTS:
            assert agent["sandbox_mode"] == "read-only"

    implementation_agent = agents["implementation_engineer"]
    assert implementation_agent["sandbox_mode"] == "workspace-write"
    assert "Nutzerfreigabe" in implementation_agent["developer_instructions"]


def test_council_majority_delegation_keeps_special_gates_separate() -> None:
    agent_rules = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "### Delegierte Council-Mehrheitsfreigabe" in agent_rules
    assert "mindestens drei der fuenf definierten Council-Rollen" in agent_rules
    assert "geschuetzte oder reale Daten" in agent_rules
    assert "Commits, Pushes, Tags oder Veroeffentlichungen" in agent_rules


def test_repo_skills_are_thin_valid_routers() -> None:
    skills_root = REPO_ROOT / ".agents" / "skills"
    skill_dirs = {path.name for path in skills_root.iterdir() if path.is_dir()}

    assert skill_dirs == EXPECTED_SKILLS
    assert (skills_root / "README.md").is_file()
    for skill_name in EXPECTED_SKILLS:
        skill_file = skills_root / skill_name / "SKILL.md"
        metadata = _skill_frontmatter(skill_file)
        text = skill_file.read_text(encoding="utf-8")
        interface = (skills_root / skill_name / "agents" / "openai.yaml").read_text(encoding="utf-8")

        assert metadata["name"] == skill_name
        assert metadata["description"]
        assert "TODO" not in text
        assert "docs/project/UPDATE_ROUTINES.md" in text
        assert f"${skill_name}" in interface
        for trigger in EXPECTED_SKILL_TRIGGERS[skill_name]:
            assert f"`{trigger}`" in metadata["description"]


def test_workflow_sources_have_unambiguous_ownership() -> None:
    routines = (REPO_ROOT / "docs/project/UPDATE_ROUTINES.md").read_text(encoding="utf-8")
    commands = (REPO_ROOT / "docs/common/commands_common.md").read_text(encoding="utf-8")
    implementation_notes = (REPO_ROOT / "docs/project/plans/IMPLEMENTATION_NOTES.md").read_text(encoding="utf-8")
    norms_readme = (REPO_ROOT / "data/common/normen/README.md").read_text(encoding="utf-8")
    github_professor = (REPO_ROOT / ".github/agents/Professor.md").read_text(encoding="utf-8")

    assert "einzige Ablaufwahrheit" in routines
    assert "Triggerindex" in commands
    assert "aktualisieren und tagesende direkt" in routines
    assert "aktualisieren und direkt update repo" in routines
    for trigger in CANONICAL_WORKFLOW_TRIGGERS:
        assert f"`{trigger}`" in routines
        assert f"`{trigger}`" in commands
    assert "keine Oberflaeche automatisch starten" in implementation_notes
    assert "bei freiem Port `8501` automatisch starten" not in implementation_notes
    assert "ChatGPT-Auswertungen und automatische Extraktionen" not in norms_readme
    assert "OCR, automatische Extraktion" in norms_readme
    assert "GitHub-spezifische Adapter" in github_professor
    assert ".codex/agents/professor.toml" in github_professor


def test_protected_working_data_is_not_part_of_tracked_scan_scope() -> None:
    tracked = _tracked_files()
    protected_prefixes = (
        "config/ma_database/catalogs/",
        "data/catalogs/",
        "data/common/normen/",
        "data/ma_analyse/ida_imports/",
        "data/ma_variants/ida_exports/",
    )
    protected_tracked = {path for path in tracked if path.startswith(protected_prefixes)}

    assert protected_tracked == ALLOWED_TRACKED_PROTECTED_PATHS


def test_p031_is_the_only_project_os_audit_container() -> None:
    p031 = REPO_ROOT / "docs/project/plans/inbox/260715_Plan_P031_Codex_Project_Operating_System.md"
    text = p031.read_text(encoding="utf-8")

    assert "erteilt keine technische, fachliche, rechtliche" in text
    assert "## Repository Audit" in text
    assert "## Conflict Register" in text
    assert "## Tool Capability Audit" in text
    assert "## Master-System Backlog" in text

    audit_headings = {
        "## Repository Audit",
        "## Conflict Register",
        "## Tool Capability Audit",
        "## Master-System Backlog",
    }
    markdown_files = _tracked_markdown_files() | {p031}
    audit_containers = []
    for markdown_file in markdown_files:
        if not markdown_file.is_file():
            continue
        candidate = markdown_file.read_text(encoding="utf-8")
        if sum(heading in candidate for heading in audit_headings) >= 2:
            audit_containers.append(markdown_file.relative_to(REPO_ROOT).as_posix())

    expected_p031 = p031.relative_to(REPO_ROOT).as_posix()
    assert sorted(audit_containers) == [expected_p031]

    plan_index = (REPO_ROOT / "docs/project/plans/PLAN_INDEX.md").read_text(encoding="utf-8")
    project_os_rows = [
        line for line in plan_index.splitlines() if line.startswith("| ") and "Codex Project Operating System" in line
    ]
    p031_rows = [line for line in plan_index.splitlines() if line.startswith("| P031 |")]
    assert len(p031_rows) == 1
    assert len(project_os_rows) == 1
    assert project_os_rows == p031_rows
    assert "inbox/260715_Plan_P031_Codex_Project_Operating_System.md" in p031_rows[0]

    plan_status = (REPO_ROOT / "docs/project/plans/PLAN_STATUS.md").read_text(encoding="utf-8")
    ownership_marker = "P031 ordnet das repo-lokale Codex Project Operating System"
    assert plan_status.count(ownership_marker) == 1

    parallel_truths = (
        REPO_ROOT / "AGENT_SYSTEM_OPERATIONS.md",
        REPO_ROOT / "docs/handover/AGENT_SYSTEM_HANDOVER.md",
        REPO_ROOT / "docs/agents/AGENT_TEAM.md",
        REPO_ROOT / "docs/architecture/SOURCE_OF_TRUTH.md",
        REPO_ROOT / "docs/architecture/OBSIDIAN_STRATEGY.md",
        REPO_ROOT / "docs/graphify/FIRST_GRAPH_EVALUATION.md",
        REPO_ROOT / "docs/project/MASTER_SYSTEM_BACKLOG.md",
    )
    assert not any(path.exists() for path in parallel_truths)
