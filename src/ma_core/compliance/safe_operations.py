"""Kleine Schutzwrapper fuer Datei-, Parser- und externe Operationen."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

from .models import ComplianceDecision

ResultT = TypeVar("ResultT")


def safe_open(
    path: str | Path,
    mode: str,
    *,
    decision: ComplianceDecision,
    **open_kwargs: Any,
):
    """Oeffnet eine Datei erst nach technischer Compliance-Freigabe."""
    decision.require_allowed()
    return Path(path).open(mode, **open_kwargs)


def safe_parse(
    parser: Callable[..., ResultT],
    *args: Any,
    decision: ComplianceDecision,
    **kwargs: Any,
) -> ResultT:
    """Fuehrt einen Parser nur im freigegebenen Umfang aus."""
    decision.require_allowed()
    return parser(*args, **kwargs)


def safe_convert(
    converter: Callable[..., ResultT],
    *args: Any,
    decision: ComplianceDecision,
    **kwargs: Any,
) -> ResultT:
    """Fuehrt eine Konvertierung nur im freigegebenen Umfang aus."""
    decision.require_allowed()
    return converter(*args, **kwargs)


def safe_upload(
    uploader: Callable[..., ResultT],
    *args: Any,
    decision: ComplianceDecision,
    **kwargs: Any,
) -> ResultT:
    """Erzwingt die Freigabe vor jeder externen Uebertragung."""
    decision.require_allowed()
    return uploader(*args, **kwargs)


def safe_index(
    indexer: Callable[..., ResultT],
    *args: Any,
    decision: ComplianceDecision,
    **kwargs: Any,
) -> ResultT:
    """Erzwingt die Freigabe vor Index-, Embedding- oder RAG-Schritten."""
    decision.require_allowed()
    return indexer(*args, **kwargs)


def safe_execute_simulation(
    executor: Callable[..., ResultT],
    *args: Any,
    decision: ComplianceDecision,
    **kwargs: Any,
) -> ResultT:
    """Erzwingt die Freigabe vor einem Simulationsstart."""
    decision.require_allowed()
    return executor(*args, **kwargs)
