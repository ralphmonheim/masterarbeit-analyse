"""Datenmodelle fuer Dokumentreferenzen."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..validation import require_non_empty


@dataclass(frozen=True, slots=True)
class Document:
    """Referenziert ein Dokument ueber einen Dateipfad."""

    document_key: str
    document_type: str
    title: str
    document_path: str
    related_key: str
    source: str
    data_quality: str

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.document_key, "document_key", model_name)
        require_non_empty(self.document_type, "document_type", model_name)
        require_non_empty(self.title, "title", model_name)
        require_non_empty(self.document_path, "document_path", model_name)
        require_non_empty(self.related_key, "related_key", model_name)
        require_non_empty(self.source, "source", model_name)
        require_non_empty(self.data_quality, "data_quality", model_name)


@dataclass(frozen=True, slots=True)
class DocumentCatalogImportResult:
    """Ergebnis eines Dokumentkatalogimports."""

    documents: list[Document]
    errors: list[str]
    source_path: Path | None = None
