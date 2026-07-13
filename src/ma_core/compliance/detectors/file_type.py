"""Dateitypdetektor fuer bekannte geschuetzte oder neutrale Formate."""

from ..models import OperationRequest, PreflightRecord
from .base import DetectorFinding


class FileTypeDetector:
    """Ordnet nur anhand der Endung ein; die Datei wird nicht geoeffnet."""

    PROTECTED_SUFFIXES = {".idm", ".nmf", ".pdf"}

    def detect(self, _request: OperationRequest, preflight: PreflightRecord) -> tuple[DetectorFinding, ...]:
        if preflight.file_suffix not in self.PROTECTED_SUFFIXES:
            return ()
        return (
            DetectorFinding(
                detector="file_type",
                code="PROTECTED_SUFFIX",
                message=f"Dateityp {preflight.file_suffix} erfordert eine dokumentierte Schutzpruefung.",
            ),
        )
