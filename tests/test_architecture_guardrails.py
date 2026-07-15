"""Guardrails for P032's incremental architecture migration."""

from __future__ import annotations

import ast
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / "src"
TEMPORARY_DEBT_PAIRS = {
    ("ma_technical", "ma_zones"),
}
EXPECTED_TEMPORARY_DEBT_IMPORTS = Counter(
    {
        ("ma_technical/validation.py", "ma_zones"): 1,
    }
)
EXPECTED_RUNTIME_CYCLES: set[frozenset[str]] = set()
PROTECTED_CATALOG_SENTINELS = (
    "data/catalogs/materials/future-material-catalog.yaml",
    "data/catalogs/materials/unreviewed/nested-catalog.yaml",
    "data/catalogs/products/future-product-catalog.yaml",
    "data/catalogs/sources/future-source-catalog.yaml",
)
CATALOG_STRUCTURE_SENTINELS = (
    "data/catalogs/materials/.gitkeep",
    "data/catalogs/products/.gitkeep",
    "data/catalogs/sources/.gitkeep",
)


def _tracked_python_source_files() -> tuple[Path, ...]:
    """Return only versioned source files from the positive scan allowlist."""
    result = subprocess.run(
        ["git", "ls-files", "--", "src"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(REPO_ROOT / path for path in result.stdout.splitlines() if path.endswith(".py"))


def _is_type_checking_guard(condition: ast.expr) -> bool:
    return isinstance(condition, ast.Name) and condition.id == "TYPE_CHECKING"


class _RuntimeModuleImportCollector(ast.NodeVisitor):
    """Collect absolute imports that are active at runtime, not typing-only imports."""

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


def _imported_module_names(source_file: Path) -> tuple[str, ...]:
    syntax_tree = ast.parse(source_file.read_text(encoding="utf-8"))
    collector = _RuntimeModuleImportCollector()
    collector.visit(syntax_tree)
    return tuple(module for module in collector.module_names if module.startswith("ma_"))


def _cross_package_imports() -> list[tuple[str, str, str, str]]:
    imports: list[tuple[str, str, str, str]] = []
    for source_file in _tracked_python_source_files():
        relative_path = source_file.relative_to(SOURCE_ROOT).as_posix()
        source_package = relative_path.split("/", maxsplit=1)[0]
        for target_module in _imported_module_names(source_file):
            target_package = target_module.split(".", maxsplit=1)[0]
            if source_package != target_package:
                imports.append((source_package, target_package, target_module, relative_path))
    return imports


def _is_ignored(relative_path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "-q", "--", relative_path],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode in {0, 1}, result.stderr
    return result.returncode == 0


def test_foundation_packages_remain_domain_neutral() -> None:
    imports_by_source: defaultdict[str, set[str]] = defaultdict(set)
    for source_package, target_package, _, _ in _cross_package_imports():
        imports_by_source[source_package].add(target_package)

    assert not imports_by_source["ma_core"]
    assert imports_by_source["ma_validation"] <= {"ma_core"}


def test_domain_packages_do_not_depend_on_the_ui() -> None:
    domain_to_ui_imports = [
        (source_package, relative_path)
        for source_package, target_package, _, relative_path in _cross_package_imports()
        if target_package == "ma_ui" and source_package != "ma_ui"
    ]

    assert not domain_to_ui_imports


def test_current_migration_debts_are_limited_to_documented_imports() -> None:
    temporary_debt_imports = Counter(
        (relative_path, target_module)
        for source_package, target_package, target_module, relative_path in _cross_package_imports()
        if (source_package, target_package) in TEMPORARY_DEBT_PAIRS
    )

    assert temporary_debt_imports == EXPECTED_TEMPORARY_DEBT_IMPORTS


def test_parameter_catalog_owner_has_no_runtime_dependency_on_variants() -> None:
    """Keep W2a's one-way compatibility boundary effective before staging."""
    parameter_source_files = sorted((SOURCE_ROOT / "ma_parameters").rglob("*.py"))
    variant_imports = [
        (source_file.relative_to(SOURCE_ROOT).as_posix(), target_module)
        for source_file in parameter_source_files
        for target_module in _imported_module_names(source_file)
        if target_module == "ma_variants" or target_module.startswith("ma_variants.")
    ]

    assert not variant_imports


def _reachable_packages(adjacency: dict[str, set[str]], start: str) -> set[str]:
    reachable: set[str] = set()
    pending = [start]
    while pending:
        package = pending.pop()
        if package in reachable:
            continue
        reachable.add(package)
        pending.extend(adjacency[package] - reachable)
    return reachable


def _runtime_cycles() -> set[frozenset[str]]:
    adjacency: defaultdict[str, set[str]] = defaultdict(set)
    for source_package, target_package, _, _ in _cross_package_imports():
        adjacency[source_package].add(target_package)
        adjacency.setdefault(target_package, set())

    reverse_adjacency: defaultdict[str, set[str]] = defaultdict(set)
    for source_package, target_packages in adjacency.items():
        for target_package in target_packages:
            reverse_adjacency[target_package].add(source_package)
        reverse_adjacency.setdefault(source_package, set())

    remaining = set(adjacency)
    cycles: set[frozenset[str]] = set()
    while remaining:
        package = next(iter(remaining))
        component = frozenset(_reachable_packages(adjacency, package) & _reachable_packages(reverse_adjacency, package))
        remaining -= component
        if len(component) > 1:
            cycles.add(component)
    return cycles


def test_runtime_cycles_are_eliminated_for_the_current_tracked_source_set() -> None:
    assert _runtime_cycles() == EXPECTED_RUNTIME_CYCLES


def test_root_and_data_readmes_use_current_paths() -> None:
    root_readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    data_readme = (REPO_ROOT / "data" / "README.md").read_text(encoding="utf-8")

    assert "src/ma_analyse/gui/" not in root_readme
    assert "src/ma_ui/tkinter_app/" in root_readme
    assert "data/ma_analyse/input/" not in data_readme
    assert "data/ma_analyse/ida_imports/" in data_readme


def test_sensitive_catalog_subpaths_are_ignored_without_hiding_structure() -> None:
    assert all(_is_ignored(path) for path in PROTECTED_CATALOG_SENTINELS)
    assert not any(_is_ignored(path) for path in CATALOG_STRUCTURE_SENTINELS)
