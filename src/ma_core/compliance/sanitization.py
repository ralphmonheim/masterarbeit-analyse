"""Erkennung und Maskierung typischer vertraulicher Textmerkmale."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SensitiveFinding:
    """Fund ohne Speicherung des eigentlichen Geheimnisses."""

    category: str
    start: int
    end: int


SENSITIVE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
    ("windows_user_path", re.compile(r"\b[A-Z]:\\Users\\[^\\\s]+", re.IGNORECASE)),
    (
        "license_or_api_key",
        re.compile(
            r"\b(?:license|licence|serial|activation|api[_ -]?key|token)\s*[:=]\s*[A-Z0-9_./+-]{8,}\b",
            re.IGNORECASE,
        ),
    ),
)


def find_sensitive_markers(text: str) -> tuple[SensitiveFinding, ...]:
    """Meldet Kategorien und Positionen, aber keine gefundenen Werte."""
    findings: list[SensitiveFinding] = []
    for category, pattern in SENSITIVE_PATTERNS:
        findings.extend(
            SensitiveFinding(category=category, start=match.start(), end=match.end())
            for match in pattern.finditer(text)
        )
    return tuple(sorted(findings, key=lambda finding: (finding.start, finding.end)))


def sanitize_text(text: str) -> str:
    """Ersetzt sensible Werte durch stabile Kategorien."""
    sanitized = text
    for category, pattern in SENSITIVE_PATTERNS:
        sanitized = pattern.sub(f"[REDACTED_{category.upper()}]", sanitized)
    return sanitized
