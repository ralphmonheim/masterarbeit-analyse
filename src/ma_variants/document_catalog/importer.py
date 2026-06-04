"""Importer fuer Dokumentreferenzen aus YAML oder JSON."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..importing.io import load_config_file
from .models import Document, DocumentCatalogImportResult

DOCUMENT_REQUIRED_FIELDS = (
    "document_key",
    "document_type",
    "title",
    "document_path",
    "related_key",
    "source",
    "data_quality",
)


def _missing_fields(raw_item: dict[str, Any], required_fields: tuple[str, ...]) -> list[str]:
    return [field for field in required_fields if field not in raw_item]


def import_documents(config_path: str | Path) -> DocumentCatalogImportResult:
    """Laedt Dokumentreferenzen aus YAML oder JSON."""
    path = Path(config_path)
    data = load_config_file(path)
    raw_documents = data.get("documents")
    if not isinstance(raw_documents, list):
        return DocumentCatalogImportResult([], ["Konfiguration muss eine Liste 'documents' enthalten."], path)

    documents: list[Document] = []
    errors: list[str] = []
    seen_keys: set[str] = set()

    for index, raw_item in enumerate(raw_documents, start=1):
        item_label = f"documents[{index}]"
        if not isinstance(raw_item, dict):
            errors.append(f"{item_label} muss ein Objekt sein.")
            continue

        missing = _missing_fields(raw_item, DOCUMENT_REQUIRED_FIELDS)
        if missing:
            errors.append(f"{item_label} fehlt Pflichtfeld(er): {', '.join(missing)}.")
            continue

        document_key = str(raw_item["document_key"]).strip()
        if document_key in seen_keys:
            errors.append(f"Doppelter document_key '{document_key}'.")
            continue
        seen_keys.add(document_key)

        try:
            documents.append(Document(**{field: raw_item[field] for field in DOCUMENT_REQUIRED_FIELDS}))
        except ValueError as exc:
            errors.append(f"{item_label}: {exc}")

    return DocumentCatalogImportResult(documents=documents, errors=errors, source_path=path)
