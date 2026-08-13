"""Strukturierte Sicht auf vorhandene IDA-HTML-Berichtstabellen."""

from __future__ import annotations

import re
from pathlib import Path

from .results import parse_html_report


def extract_zone_report_rows(path: str | Path) -> tuple[dict[str, object], ...]:
    """Liefert die Berichtstabelle, deren erste Spalte `Zone` heißt."""

    _, tables = parse_html_report(path)
    for table in tables:
        if not table or not table[0] or _key(table[0][0]) != "zone":
            continue
        headers = tuple(_key(value) for value in table[0])
        return tuple(
            {header: _value(value) for header, value in zip(headers, row, strict=False)}
            for row in table[1:]
            if row and str(row[0]).strip()
        )
    return ()


def _key(value: str) -> str:
    normalized = value.casefold().replace("²", "2").replace("ä", "a").replace("ö", "o").replace("ü", "u")
    normalized = normalized.replace("ß", "ss").replace("\xad", "")
    return re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")


def _value(value: str) -> object:
    normalized = str(value).strip()
    if not normalized or normalized.casefold() == "nil":
        return None
    numeric = normalized.replace(" ", "").replace(",", ".")
    try:
        return float(numeric)
    except ValueError:
        return normalized
