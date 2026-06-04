"""Datenmodelle fuer Quellenkataloge."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..validation import require_non_empty


@dataclass(frozen=True, slots=True)
class Source:
    """Beschreibt eine Quelle fuer Katalogdaten."""

    source_key: str
    source_type: str
    title: str
    url: str
    citation: str
    accessed_at: str
    data_quality: str

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.source_key, "source_key", model_name)
        require_non_empty(self.source_type, "source_type", model_name)
        require_non_empty(self.title, "title", model_name)
        require_non_empty(self.url, "url", model_name)
        require_non_empty(self.citation, "citation", model_name)
        require_non_empty(self.accessed_at, "accessed_at", model_name)
        require_non_empty(self.data_quality, "data_quality", model_name)


@dataclass(frozen=True, slots=True)
class SourceCatalogImportResult:
    """Ergebnis eines Quellenkatalogimports."""

    sources: list[Source]
    errors: list[str]
    source_path: Path | None = None
