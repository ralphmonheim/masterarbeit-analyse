"""Konservative Quellenklassifikation ohne Inhaltsanalyse."""

from ..enums import SourceType
from ..models import OperationRequest, PreflightRecord
from .base import DetectorFinding


class ProtectedContentDetector:
    """Markiert Quellenarten mit vertraglichen oder urheberrechtlichen Grenzen."""

    PROTECTED_SOURCES = {
        SourceType.IDA_IDM,
        SourceType.EQUA_LIBRARY,
        SourceType.EQUA_PARAMETER,
        SourceType.DIN_CONTENT,
        SourceType.NAUTOS_CONTENT,
        SourceType.DWD_REGISTERED_DATA,
        SourceType.DWD_THIRD_PARTY,
    }

    def detect(self, request: OperationRequest, _preflight: PreflightRecord) -> tuple[DetectorFinding, ...]:
        if request.source_type not in self.PROTECTED_SOURCES:
            return ()
        return (
            DetectorFinding(
                detector="protected_content",
                code="PROTECTED_SOURCE",
                message="Die deklarierte Quellenart erfordert eine zweckgebundene Compliance-Entscheidung.",
            ),
        )
