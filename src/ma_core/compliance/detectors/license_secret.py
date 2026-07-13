"""Detektor fuer bereits deklarierte Lizenz- oder Zugangsdaten."""

from ..models import OperationRequest, PreflightRecord
from .base import DetectorFinding


class LicenseSecretDetector:
    """Stoppt anhand des Request-Merkmals, ohne einen geheimen Wert zu loggen."""

    def detect(self, request: OperationRequest, _preflight: PreflightRecord) -> tuple[DetectorFinding, ...]:
        if not request.contains_license_or_access_data:
            return ()
        return (
            DetectorFinding(
                detector="license_secret",
                code="LICENSE_OR_ACCESS_DATA",
                message="Lizenz- oder Zugangsdaten wurden erkannt.",
                blocks_processing=True,
            ),
        )
