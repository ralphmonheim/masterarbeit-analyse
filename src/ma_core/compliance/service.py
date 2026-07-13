"""Deterministische Schutzregeln fuer die freigegebenen Projektoperationen."""

from __future__ import annotations

from collections.abc import Callable

from .audit import ComplianceAuditLogger
from .enums import ComplianceLevel, ComplianceOperation, ProcessingEnvironment, SourceType
from .models import ComplianceDecision, OperationRequest, PreflightRecord
from .preflight import inspect_request_metadata


class ComplianceService:
    """Bewertet Operationen konservativ und protokolliert nur Metadaten."""

    def __init__(self, *, audit_logger: ComplianceAuditLogger | None = None) -> None:
        self._audit_logger = audit_logger

    def evaluate(self, request: OperationRequest) -> ComplianceDecision:
        """Fuehrt Metadaten-Preflight und regelbasierte Entscheidung aus."""
        preflight = inspect_request_metadata(request)
        decision = self._evaluate_rules(request, preflight)
        if self._audit_logger is not None:
            self._audit_logger.append(request, preflight, decision)
        return decision

    def approve_yellow(
        self,
        request: OperationRequest,
        decision: ComplianceDecision,
        *,
        confirmation_reference: str,
        permission_reference: str | None = None,
        university_approval_reference: str | None = None,
    ) -> ComplianceDecision:
        """Dokumentiert die vollstaendige Freigabe einer gelben Entscheidung."""
        if decision.request_id != request.request_id:
            raise ValueError("Entscheidung und Anfrage gehoeren nicht zusammen.")
        approved = decision.with_approval(
            confirmation_reference=confirmation_reference,
            permission_reference=permission_reference,
            university_approval_reference=university_approval_reference,
        )
        if self._audit_logger is not None:
            self._audit_logger.append(request, inspect_request_metadata(request), approved)
        return approved

    def _evaluate_rules(self, request: OperationRequest, preflight: PreflightRecord) -> ComplianceDecision:
        rules: tuple[Callable[[OperationRequest, PreflightRecord], ComplianceDecision | None], ...] = (
            _license_secret_rule,
            _missing_file_rule,
            _unknown_origin_rule,
            _unknown_license_rule,
            _forbidden_technical_operation_rule,
            _equa_ida_rule,
            _din_nautos_rule,
            _dwd_rule,
            _user_owned_rule,
        )
        for rule in rules:
            decision = rule(request, preflight)
            if decision is not None:
                return decision
        return _decision(
            request,
            ComplianceLevel.UNKNOWN,
            reason="Fuer diese Kombination aus Quelle und Operation ist keine belastbare Freigaberegel vorhanden.",
            rules=("SHARED-UNKNOWN-002",),
            excluded=(request.operation.value,),
            alternative="Herkunft, Lizenz und minimalen Verarbeitungsumfang dokumentieren und erneut pruefen.",
        )


def _missing_file_rule(
    request: OperationRequest,
    preflight: PreflightRecord,
) -> ComplianceDecision | None:
    if request.file_path is None or preflight.file_exists is not False:
        return None
    return _decision(
        request,
        ComplianceLevel.UNKNOWN,
        reason="Die angegebene Quelldatei existiert nicht und kann nicht vorgeprueft werden.",
        rules=("SHARED-FILE-MISSING-001",),
        excluded=(request.operation.value,),
        alternative="Vorhandene Quelldatei auswaehlen und den Preflight erneut ausfuehren.",
    )


def _decision(
    request: OperationRequest,
    level: ComplianceLevel,
    *,
    reason: str,
    rules: tuple[str, ...],
    allowed: tuple[str, ...] = (),
    excluded: tuple[str, ...] = (),
    alternative: str | None = None,
    written_permission: bool = False,
    university_approval: bool = False,
) -> ComplianceDecision:
    is_green = level is ComplianceLevel.GREEN
    is_yellow = level is ComplianceLevel.YELLOW
    return ComplianceDecision(
        request_id=request.request_id,
        classification=level,
        processing_allowed=is_green,
        warning_required=not is_green,
        reason=reason,
        applicable_rules=rules,
        allowed_scope=allowed,
        excluded_scope=excluded,
        safe_alternative=alternative,
        confirmation_required=is_yellow,
        written_permission_required=written_permission,
        university_approval_required=university_approval,
    )


def _license_secret_rule(
    request: OperationRequest,
    _preflight: PreflightRecord,
) -> ComplianceDecision | None:
    if not request.contains_license_or_access_data:
        return None
    return _decision(
        request,
        ComplianceLevel.RED,
        reason="Lizenz-, Aktivierungs- oder Zugangsdaten duerfen nicht verarbeitet werden.",
        rules=("SHARED-SECRET-001",),
        excluded=("read", "store", "upload", "log"),
        alternative="Zugangsdaten entfernen und nur eine bereinigte Arbeitskopie neu pruefen.",
    )


def _unknown_origin_rule(
    request: OperationRequest,
    preflight: PreflightRecord,
) -> ComplianceDecision | None:
    if request.source_type is SourceType.UNKNOWN or not preflight.source_origin_known:
        return _decision(
            request,
            ComplianceLevel.UNKNOWN,
            reason="Die Herkunft der Quelle ist nicht dokumentiert.",
            rules=("SHARED-UNKNOWN-001",),
            excluded=(request.operation.value,),
            alternative="Nur Metadaten erfassen und die Quelle vor jeder Inhaltsverarbeitung klaeren.",
        )
    return None


def _unknown_license_rule(
    request: OperationRequest,
    preflight: PreflightRecord,
) -> ComplianceDecision | None:
    license_optional_sources = {
        SourceType.USER_OWNED,
        SourceType.DIN_METADATA,
        SourceType.DIN_PARAPHRASE,
    }
    if preflight.applicable_license_known or request.source_type in license_optional_sources:
        return None
    return _decision(
        request,
        ComplianceLevel.UNKNOWN,
        reason="Die anwendbare Lizenz oder Bezugsberechtigung ist nicht dokumentiert.",
        rules=("SHARED-UNKNOWN-LICENSE-001",),
        excluded=(request.operation.value,),
        alternative="Lizenz, Vertrag oder eigene Rechte dokumentieren und erneut pruefen.",
    )


def _forbidden_technical_operation_rule(
    request: OperationRequest,
    _preflight: PreflightRecord,
) -> ComplianceDecision | None:
    if request.operation in {
        ComplianceOperation.REVERSE_ENGINEER,
        ComplianceOperation.BINARY_ANALYSIS,
    }:
        return _decision(
            request,
            ComplianceLevel.RED,
            reason="Reverse Engineering und Binaeranalyse liegen ausserhalb des freigegebenen Projektumfangs.",
            rules=("SHARED-TECHNICAL-STOP-001",),
            excluded=(request.operation.value,),
            alternative="Offizielle Schnittstellen und eigene, neutral beschriebene Daten verwenden.",
        )
    return None


def _equa_ida_rule(
    request: OperationRequest,
    _preflight: PreflightRecord,
) -> ComplianceDecision | None:
    equa_sources = {SourceType.IDA_RESULT, SourceType.IDA_IDM, SourceType.EQUA_LIBRARY, SourceType.EQUA_PARAMETER}
    if request.source_type not in equa_sources:
        return None

    if request.operation in {ComplianceOperation.EXECUTE_SIMULATION, ComplianceOperation.BATCH_SIMULATION}:
        return _decision(
            request,
            ComplianceLevel.RED,
            reason="IDA ICE darf ohne ausdrueckliche EQUA-Freigabe nicht automatisiert gestartet oder ausgefuehrt werden.",
            rules=("EQUA-EULA-3E-AUTOMATION-STOP",),
            excluded=(request.operation.value,),
            alternative="Run-Manifest erzeugen und Simulation manuell in IDA ICE starten.",
        )

    if request.source_type is SourceType.EQUA_LIBRARY:
        return _decision(
            request,
            ComplianceLevel.RED,
            reason="Vollstaendige EQUA-Bibliotheken duerfen nicht repliziert, extrahiert oder indexiert werden.",
            rules=("EQUA-EULA-3A-5A-LIBRARY-STOP",),
            excluded=(request.operation.value, "complete_library"),
            alternative="Nur benoetigte Einzelparameter manuell dokumentieren und ihre Herkunft belegen.",
        )

    if request.source_type is SourceType.IDA_RESULT and request.user_owned:
        return _decision(
            request,
            ComplianceLevel.GREEN,
            reason="Eigene exportierte Simulationsergebnisse duerfen lokal ausgewertet werden.",
            rules=("EQUA-OWN-RESULTS-001",),
            allowed=(request.operation.value, "local_analysis", "own_results"),
            excluded=("embedded_third_party_content", "license_data"),
        )

    if request.source_type is SourceType.IDA_IDM:
        external = request.operation is ComplianceOperation.UPLOAD_EXTERNAL or request.environment in {
            ProcessingEnvironment.CLOUD,
            ProcessingEnvironment.EXTERNAL_AI,
        }
        return _decision(
            request,
            ComplianceLevel.YELLOW,
            reason=(
                "Eine vollstaendige IDM-Datei enthaelt potenziell EQUA- und Projektdaten; externe Verarbeitung ist nicht pauschal freigegeben."
                if external
                else "Das lokale Lesen einer IDM-Datei bleibt auf den dokumentierten Minimalumfang begrenzt."
            ),
            rules=(("EQUA-IDM-EXTERNAL-002",) if external else ("EQUA-IDM-LOCAL-001",)),
            allowed=(("metadata_only",) if external else ("local_parse", "documented_fields_only")),
            excluded=("complete_content_upload", "library_replication", "model_modification"),
            alternative="Nur benoetigte eigene Metadaten in eine bereinigte Zwischendatei uebertragen.",
            written_permission=external,
        )

    if request.source_type is SourceType.EQUA_PARAMETER:
        return _decision(
            request,
            ComplianceLevel.YELLOW,
            reason="Einzelne EQUA-Parameter duerfen nur zweckgebunden und ohne Bibliotheksrekonstruktion verglichen werden.",
            rules=("EQUA-PARAMETER-LIMIT-001",),
            allowed=("individual_parameter", request.operation.value),
            excluded=("systematic_library_extraction", "redistribution"),
            alternative="Eigene neutrale Parameterbeschreibung mit Quellenverweis verwenden.",
        )
    return None


def _din_nautos_rule(
    request: OperationRequest,
    _preflight: PreflightRecord,
) -> ComplianceDecision | None:
    din_sources = {
        SourceType.DIN_METADATA,
        SourceType.DIN_PARAPHRASE,
        SourceType.DIN_SHORT_QUOTE,
        SourceType.DIN_CONTENT,
        SourceType.NAUTOS_CONTENT,
    }
    if request.source_type not in din_sources:
        return None

    if request.source_type in {SourceType.DIN_METADATA, SourceType.DIN_PARAPHRASE}:
        return _decision(
            request,
            ComplianceLevel.GREEN,
            reason="Bibliografische Metadaten und eigene Paraphrasen enthalten keinen systematischen Normvolltext.",
            rules=("DIN-METADATA-PARAPHRASE-001",),
            allowed=(request.operation.value, request.source_type.value),
            excluded=("norm_fulltext", "reconstructed_standard"),
        )

    if request.source_type is SourceType.DIN_SHORT_QUOTE:
        return _decision(
            request,
            ComplianceLevel.YELLOW,
            reason="Ein kurzes Normzitat erfordert Zweck-, Umfangs- und Quellenpruefung.",
            rules=("DIN-SHORT-QUOTE-001",),
            allowed=("short_necessary_quote",),
            excluded=("systematic_excerpts", "substantial_reconstruction"),
            alternative="In eigenen Worten paraphrasieren und die Normstelle bibliografisch belegen.",
        )

    if request.operation in {
        ComplianceOperation.OCR,
        ComplianceOperation.RAG,
        ComplianceOperation.INDEX,
        ComplianceOperation.EXTRACT,
        ComplianceOperation.UPLOAD_EXTERNAL,
    }:
        return _decision(
            request,
            ComplianceLevel.RED,
            reason="Maschinenlesbare Normextraktion, OCR, RAG oder externe KI-Verarbeitung ist ohne gesonderte Rechte nicht erlaubt.",
            rules=("DIN-AGB-5-4-5-6-AI-STOP",),
            excluded=(request.operation.value, "norm_fulltext"),
            alternative="Norm lokal manuell auswerten und nur eigene Paraphrasen oder Berechnungslogik dokumentieren.",
        )

    return _decision(
        request,
        ComplianceLevel.YELLOW,
        reason="Die Nutzung geschuetzter DIN- oder Nautos-Inhalte ist vertraglich und institutionell zu klaeren.",
        rules=("DIN-NAUTOS-REVIEW-001",),
        allowed=("manual_review",),
        excluded=("automated_processing", "repository_storage"),
        alternative="Nur bibliografische Metadaten und eigene Notizen verwenden.",
        written_permission=True,
        university_approval=True,
    )


def _dwd_rule(
    request: OperationRequest,
    _preflight: PreflightRecord,
) -> ComplianceDecision | None:
    dwd_sources = {SourceType.DWD_OPEN_DATA, SourceType.DWD_REGISTERED_DATA, SourceType.DWD_THIRD_PARTY}
    if request.source_type not in dwd_sources:
        return None

    if request.attribution_present is False:
        return _decision(
            request,
            ComplianceLevel.RED,
            reason="Die erforderliche DWD-Quellenangabe fehlt.",
            rules=("DWD-ATTRIBUTION-STOP-001",),
            excluded=(request.operation.value, "publication", "redistribution"),
            alternative="DWD-Urhebervermerk, Datensatz, Lizenz und Aenderungshinweis ergaenzen.",
        )

    if request.source_type is SourceType.DWD_OPEN_DATA:
        license_text = (request.declared_license or "").lower().replace(" ", "-")
        cc_by = "cc-by-4.0" in license_text or "creativecommons.org/licenses/by/4.0" in license_text
        if request.official_source and cc_by and request.attribution_present and request.third_party_rights_cleared:
            return _decision(
                request,
                ComplianceLevel.GREEN,
                reason="Offizielle DWD-OpenData-Quelle, CC BY 4.0, Attribution und Drittrechte sind dokumentiert.",
                rules=("DWD-OPENDATA-CC-BY-001",),
                allowed=(request.operation.value, "documented_dataset"),
                excluded=("endorsement_claim", "third_party_content", "real_data_repository_storage"),
            )
        return _decision(
            request,
            ComplianceLevel.YELLOW,
            reason="Die OpenData-Freigabe ist fuer diesen Datensatz noch nicht vollstaendig belegt.",
            rules=("DWD-OPENDATA-EVIDENCE-002",),
            allowed=("metadata_only",),
            excluded=(request.operation.value, "redistribution"),
            alternative="Offizielle Datensatz-URL, CC-BY-Hinweis, Attribution und Drittrechte dokumentieren.",
            written_permission=request.third_party_rights_cleared is not True,
        )

    if request.source_type is SourceType.DWD_REGISTERED_DATA:
        return _decision(
            request,
            ComplianceLevel.YELLOW,
            reason="Fuer registrierte oder bestellte DWD-Daten gelten die produktspezifischen Bezugsrechte.",
            rules=("DWD-AGB-OFFER-SCOPE-001",),
            allowed=("local_processing_after_review",),
            excluded=("external_processing", "redistribution", "repository_storage"),
            alternative="Angebot oder Datensatzlizenz pruefen; bis dahin nur Metadaten bearbeiten.",
            written_permission=True,
        )

    return _decision(
        request,
        ComplianceLevel.YELLOW,
        reason="DWD-nahe Inhalte mit unklaren Drittrechten sind nicht pauschal freigegeben.",
        rules=("DWD-THIRD-PARTY-001",),
        allowed=("metadata_only",),
        excluded=(request.operation.value, "publication", "redistribution"),
        alternative="Drittanbieter und anwendbare Lizenz einzeln klaeren.",
        written_permission=True,
    )


def _user_owned_rule(
    request: OperationRequest,
    _preflight: PreflightRecord,
) -> ComplianceDecision | None:
    if request.source_type is SourceType.USER_OWNED and request.user_owned:
        return _decision(
            request,
            ComplianceLevel.GREEN,
            reason="Die Quelle ist als eigener Inhalt dokumentiert und keine Schutzgrenze ist betroffen.",
            rules=("SHARED-USER-OWNED-001",),
            allowed=(request.operation.value,),
            excluded=("embedded_third_party_content", "license_data"),
        )
    return None
