"""Importer fuer Quellenkataloge aus YAML oder JSON."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..importing.io import load_config_file
from .models import Source, SourceCatalogImportResult

SOURCE_REQUIRED_FIELDS = (
    "source_key",
    "source_type",
    "title",
    "url",
    "citation",
    "accessed_at",
    "data_quality",
)


def _missing_fields(raw_item: dict[str, Any], required_fields: tuple[str, ...]) -> list[str]:
    return [field for field in required_fields if field not in raw_item]


def import_sources(config_path: str | Path) -> SourceCatalogImportResult:
    """Laedt Quellen aus YAML oder JSON."""
    path = Path(config_path)
    data = load_config_file(path)
    raw_sources = data.get("sources")
    if not isinstance(raw_sources, list):
        return SourceCatalogImportResult([], ["Konfiguration muss eine Liste 'sources' enthalten."], path)

    sources: list[Source] = []
    errors: list[str] = []
    seen_keys: set[str] = set()

    for index, raw_item in enumerate(raw_sources, start=1):
        item_label = f"sources[{index}]"
        if not isinstance(raw_item, dict):
            errors.append(f"{item_label} muss ein Objekt sein.")
            continue

        missing = _missing_fields(raw_item, SOURCE_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{item_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue

        source_key = str(raw_item["source_key"]).strip()
        if source_key in seen_keys:
            errors.append(f"Doppelter source_key '{source_key}'.")
            continue
        seen_keys.add(source_key)

        try:
            sources.append(Source(**{field: raw_item[field] for field in SOURCE_REQUIRED_FIELDS}))
        except ValueError as exc:
            errors.append(f"{item_label}: {exc}")

    return SourceCatalogImportResult(sources=sources, errors=errors, source_path=path)
