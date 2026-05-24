"""Uebernimmt Namensaenderungen aus naming.md in Paketmodulen und Doku."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, replace
from pathlib import Path

from ..core.config import COMMAND_DOC, NAMING_DOC, PACKAGE_DIR, SETTINGS_DIR

SCRIPT_DIR = PACKAGE_DIR
DEFAULT_MAPPING_DOC = NAMING_DOC
LEGACY_MAPPING_DOC = NAMING_DOC
EXCLUDED_TARGETS = {DEFAULT_MAPPING_DOC.name, LEGACY_MAPPING_DOC.name, Path(__file__).name}
TARGET_SUFFIXES = {".py", ".md"}


@dataclass(frozen=True)
class MappingEntry:
    category: str
    current_name: str
    new_name: str
    usage: str
    hint: str
    entry_id: str
    mode: str
    line_number: int


@dataclass(frozen=True)
class MappingRunSummary:
    mapping_doc: Path
    entries: list[MappingEntry]
    changed_files: int
    total_replacements: int
    target_file_count: int
    actionable_count: int
    dry_run: bool


def collect_target_files() -> list[Path]:
    target_dirs = [SCRIPT_DIR, SETTINGS_DIR]
    candidates = []
    for target_dir in target_dirs:
        if not target_dir.exists():
            continue
        candidates.extend(
            path
            for path in target_dir.rglob("*")
            if path.is_file() and path.suffix in TARGET_SUFFIXES and path.name not in EXCLUDED_TARGETS
        )
    if COMMAND_DOC.exists() and COMMAND_DOC.name not in EXCLUDED_TARGETS:
        candidates.append(COMMAND_DOC)
    return sorted(set(candidates))


def parse_hint_metadata(hint: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for raw_part in hint.split(";"):
        part = raw_part.strip()
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        metadata[key.strip().upper()] = value.strip()
    return metadata


def is_separator_row(cells: list[str]) -> bool:
    return all(set(cell) <= {"-", ":"} for cell in cells)


def parse_mapping_document(mapping_doc: Path) -> list[MappingEntry]:
    lines = mapping_doc.read_text(encoding="utf-8").splitlines()
    entries: list[MappingEntry] = []

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue

        cells = [cell.strip() for cell in stripped.split("|")[1:-1]]
        if len(cells) != 5:
            continue
        if cells[0] == "Kategorie" or is_separator_row(cells):
            continue

        category, current_name, new_name, usage, hint = cells
        metadata = parse_hint_metadata(hint)
        entry_id = metadata.get("ID", "")
        mode = metadata.get("MODE", "literal").lower()

        if not entry_id:
            raise ValueError(f"Fehlende ID in Namensmapping.md, Zeile {line_number}: {line}")
        if mode not in {"literal", "quoted"}:
            raise ValueError(f"Unbekannter MODE '{mode}' in Namensmapping.md, Zeile {line_number}: {line}")

        entries.append(
            MappingEntry(
                category=category,
                current_name=current_name,
                new_name=new_name,
                usage=usage,
                hint=hint,
                entry_id=entry_id,
                mode=mode,
                line_number=line_number,
            )
        )

    return entries


def load_mapping_entries(mapping_doc: str | Path | None = None) -> tuple[Path, list[MappingEntry]]:
    resolved_doc = resolve_mapping_document(str(mapping_doc) if mapping_doc else None)
    if not resolved_doc.exists():
        raise FileNotFoundError(f"Mapping-Dokument nicht gefunden: {resolved_doc}")
    return resolved_doc, parse_mapping_document(resolved_doc)


def update_mapping_entries(
    entries: list[MappingEntry],
    updates: dict[str, str],
) -> list[MappingEntry]:
    updated_entries: list[MappingEntry] = []
    for entry in entries:
        new_name = updates.get(entry.entry_id, entry.new_name)
        updated_entries.append(replace(entry, new_name=new_name.strip()))
    return updated_entries


def format_mapping_row(entry: MappingEntry) -> str:
    return f"| {entry.category} | {entry.current_name} | {entry.new_name} | {entry.usage} | {entry.hint} |"


def write_mapping_entries(mapping_doc: Path, entries: list[MappingEntry]) -> None:
    lines = mapping_doc.read_text(encoding="utf-8").splitlines()
    entries_by_line = {entry.line_number: entry for entry in entries}

    for index, _line in enumerate(lines, start=1):
        entry = entries_by_line.get(index)
        if entry is None:
            continue
        lines[index - 1] = format_mapping_row(entry)

    mapping_doc.write_text("\n".join(lines) + "\n", encoding="utf-8")


def resolve_mapping_document(cli_value: str | None) -> Path:
    """Liefert das aktuelle Mapping-Dokument und faellt auf den Legacy-Namen zurueck."""
    if cli_value:
        return Path(cli_value).resolve()
    if DEFAULT_MAPPING_DOC.exists():
        return DEFAULT_MAPPING_DOC.resolve()
    if LEGACY_MAPPING_DOC.exists():
        return LEGACY_MAPPING_DOC.resolve()
    return DEFAULT_MAPPING_DOC.resolve()


def replace_quoted_token(content: str, current_name: str, new_name: str) -> tuple[str, int]:
    pattern = re.compile(r"(?P<quote>['\"])%s(?P=quote)" % re.escape(current_name))

    def _replacement(match: re.Match[str]) -> str:
        quote = match.group("quote")
        return f"{quote}{new_name}{quote}"

    return pattern.subn(_replacement, content)


def apply_entry_to_content(content: str, entry: MappingEntry, is_python_file: bool) -> tuple[str, int]:
    if entry.mode == "quoted" and is_python_file:
        return replace_quoted_token(content, entry.current_name, entry.new_name)

    return content.replace(entry.current_name, entry.new_name), content.count(entry.current_name)


def apply_mappings(entries: list[MappingEntry], target_files: list[Path], dry_run: bool) -> tuple[int, int]:
    changed_files = 0
    total_replacements = 0

    actionable_entries = [entry for entry in entries if entry.new_name and entry.new_name != entry.current_name]
    actionable_entries.sort(key=lambda entry: len(entry.current_name), reverse=True)

    for target_file in target_files:
        original_content = target_file.read_text(encoding="utf-8")
        updated_content = original_content
        file_replacements = 0
        is_python_file = target_file.suffix == ".py"

        for entry in actionable_entries:
            updated_content, replacements = apply_entry_to_content(
                updated_content,
                entry,
                is_python_file=is_python_file,
            )
            file_replacements += replacements

        if updated_content == original_content:
            continue

        changed_files += 1
        total_replacements += file_replacements
        if not dry_run:
            target_file.write_text(updated_content, encoding="utf-8")

    return changed_files, total_replacements


def build_run_summary(
    mapping_doc: Path,
    entries: list[MappingEntry],
    changed_files: int,
    total_replacements: int,
    target_file_count: int,
    dry_run: bool,
) -> MappingRunSummary:
    actionable_count = sum(1 for entry in entries if entry.new_name and entry.new_name != entry.current_name)
    return MappingRunSummary(
        mapping_doc=mapping_doc,
        entries=entries,
        changed_files=changed_files,
        total_replacements=total_replacements,
        target_file_count=target_file_count,
        actionable_count=actionable_count,
        dry_run=dry_run,
    )


def run_mapping(
    mapping_doc: str | Path | None = None,
    dry_run: bool = False,
    entries: list[MappingEntry] | None = None,
) -> MappingRunSummary:
    resolved_doc, parsed_entries = load_mapping_entries(mapping_doc)
    effective_entries = entries if entries is not None else parsed_entries
    if entries is not None and not dry_run:
        write_mapping_entries(resolved_doc, effective_entries)

    target_files = collect_target_files()
    changed_files, total_replacements = apply_mappings(
        effective_entries,
        target_files,
        dry_run=dry_run,
    )
    return build_run_summary(
        resolved_doc,
        effective_entries,
        changed_files,
        total_replacements,
        len(target_files),
        dry_run,
    )


def format_run_summary(summary: MappingRunSummary) -> str:
    mode_text = "DRY-RUN" if summary.dry_run else "ANWENDEN"
    lines = [
        "=" * 70,
        f"NAMENSMAPPING - {mode_text}",
        "=" * 70,
        f"Mapping-Dokument: {summary.mapping_doc}",
        f"Ausgewertete Eintraege: {len(summary.entries)}",
        f"Aktive Umbenennungen: {summary.actionable_count}",
        f"Gepruefte Dateien: {summary.target_file_count}",
        f"Geaenderte Dateien: {summary.changed_files}",
        f"Ersetzte Vorkommen: {summary.total_replacements}",
    ]
    if summary.actionable_count == 0:
        lines.append("Hinweis: Es sind noch keine neuen Namen im Mapping-Dokument eingetragen.")
    lines.append("=" * 70)
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Liest das Namensmapping-Dokument und uebernimmt definierte Namensaenderungen."
    )
    parser.add_argument(
        "--mapping-doc",
        default=None,
        help="Pfad zum Markdown-Dokument mit Namensmapping",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Zeigt nur an, wie viele Dateien betroffen waeren, ohne zu schreiben",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    summary = run_mapping(mapping_doc=args.mapping_doc, dry_run=args.dry_run)
    print(format_run_summary(summary))


if __name__ == "__main__":
    main()
