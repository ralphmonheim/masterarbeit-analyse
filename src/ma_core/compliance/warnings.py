"""Knappe Warntexte fuer UI, CLI und Protokolle."""

from .models import ComplianceDecision


def format_compliance_warning(decision: ComplianceDecision) -> str:
    """Formatiert eine Entscheidung ohne geschuetzte Quelldaten."""
    parts = [f"Compliance-{decision.classification.value.upper()}: {decision.reason}"]
    if decision.confirmation_required:
        parts.append("Eine dokumentierte Nutzerbestaetigung ist erforderlich.")
    if decision.written_permission_required:
        parts.append("Eine schriftliche Rechtefreigabe ist erforderlich.")
    if decision.university_approval_required:
        parts.append("Eine dokumentierte Hochschulfreigabe ist erforderlich.")
    if decision.safe_alternative:
        parts.append(f"Sichere Alternative: {decision.safe_alternative}")
    return " ".join(parts)
