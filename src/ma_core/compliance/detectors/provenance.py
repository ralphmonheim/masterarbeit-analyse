"""Pruefung der im Request deklarierten Provenienz."""

from ..models import OperationRequest, PreflightRecord
from .base import DetectorFinding


class ProvenanceDetector:
    """Meldet fehlende Herkunft oder Lizenz als blockierende Unsicherheit."""

    def detect(self, _request: OperationRequest, preflight: PreflightRecord) -> tuple[DetectorFinding, ...]:
        findings: list[DetectorFinding] = []
        if not preflight.source_origin_known:
            findings.append(
                DetectorFinding(
                    detector="provenance",
                    code="SOURCE_ORIGIN_UNKNOWN",
                    message="Die Herkunft der Quelle ist nicht dokumentiert.",
                    blocks_processing=True,
                )
            )
        if not preflight.applicable_license_known:
            findings.append(
                DetectorFinding(
                    detector="provenance",
                    code="LICENSE_UNKNOWN",
                    message="Die anwendbare Lizenz ist nicht dokumentiert.",
                )
            )
        return tuple(findings)
