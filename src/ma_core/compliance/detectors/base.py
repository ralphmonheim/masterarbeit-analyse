"""Gemeinsamer Vertrag fuer metadatenbasierte Detektoren."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..models import OperationRequest, PreflightRecord


@dataclass(frozen=True, slots=True)
class DetectorFinding:
    """Ein technischer Fund ohne geschuetzten Dateiinhalt."""

    detector: str
    code: str
    message: str
    blocks_processing: bool = False


class ComplianceDetector(Protocol):
    """Minimale Schnittstelle fuer weitere Projektdetektoren."""

    def detect(self, request: OperationRequest, preflight: PreflightRecord) -> tuple[DetectorFinding, ...]: ...
