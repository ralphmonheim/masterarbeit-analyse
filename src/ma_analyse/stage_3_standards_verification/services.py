"""Wertfreie Readiness-Prüfung für später freizugebende Normnachweise."""

from __future__ import annotations

from collections.abc import Mapping
from math import isfinite

from ma_analyse.stage_2_optimization.models import CheckResult, MetricValue
from ma_parameters.usage_profile_catalog import DIN_USAGE_PROFILE_METADATA

from .models import (
    ProfileValidation,
    StandardEvaluationProfile,
    StandardRequirement,
    StandardVerificationResult,
    VerificationReadinessItem,
    readiness_item_row,
)

_OPERATORS = {"<", "<=", "==", ">=", ">"}


class StandardVerificationEngine:
    """Wertet ein extern konfiguriertes Profil aus und verändert keine Varianten."""

    def verify(
        self, profile: StandardEvaluationProfile, metrics: Mapping[str, MetricValue]
    ) -> StandardVerificationResult:
        validation = validate_profile(profile)
        if not validation.is_valid:
            return StandardVerificationResult("INVALID", profile.profile_id, validation, ())

        checks = tuple(_evaluate_requirement(requirement, metrics) for requirement in profile.requirements)
        status = _verification_status(checks, profile.requirements)
        return StandardVerificationResult(status, profile.profile_id, validation, checks)


def verify_standard_profile(
    profile: StandardEvaluationProfile, metrics: Mapping[str, MetricValue]
) -> StandardVerificationResult:
    """Praktische Funktion für die reine, UI-neutrale Profilprüfung."""

    return StandardVerificationEngine().verify(profile, metrics)


def validate_profile(profile: StandardEvaluationProfile) -> ProfileValidation:
    """Prüft nur die Konfiguration, nicht die fachliche Gültigkeit eines Regelwerks."""

    errors: list[str] = []
    if not profile.profile_id.strip():
        errors.append("Profil-ID fehlt.")
    if not profile.standard_reference.strip():
        errors.append("Regelwerksreferenz fehlt.")
    if not profile.edition.strip():
        errors.append("Ausgabe fehlt.")
    if not profile.requirements:
        errors.append("Mindestens eine Anforderung ist erforderlich.")

    requirement_ids: set[str] = set()
    for requirement in profile.requirements:
        if not requirement.requirement_id.strip():
            errors.append("Anforderungs-ID fehlt.")
        elif requirement.requirement_id in requirement_ids:
            errors.append(f"Anforderungs-ID ist nicht eindeutig: {requirement.requirement_id}")
        requirement_ids.add(requirement.requirement_id)
        if not requirement.metric_id.strip():
            errors.append(f"Kennwert-ID fehlt: {requirement.requirement_id}")
        if requirement.operator not in _OPERATORS:
            errors.append(f"Ungültiger Operator: {requirement.requirement_id}")
        if not requirement.unit:
            errors.append(f"Einheit fehlt: {requirement.requirement_id}")
        if not isfinite(requirement.limit):
            errors.append(f"Grenzwert ist nicht endlich: {requirement.requirement_id}")

    return ProfileValidation(is_valid=not errors, errors=tuple(errors))


def _evaluate_requirement(
    requirement: StandardRequirement, metrics: Mapping[str, MetricValue]
) -> CheckResult:
    metric = metrics.get(requirement.metric_id)
    if metric is None:
        return CheckResult(requirement.requirement_id, "NOT_EVALUABLE", "Kennwert fehlt.", limit=requirement.limit,
                           operator=requirement.operator)
    if not _units_match(metric.unit, requirement.unit):
        return CheckResult(
            requirement.requirement_id,
            "NOT_EVALUABLE",
            "Einheit fehlt oder ist nicht kompatibel.",
            metric,
            requirement.limit,
            requirement.operator,
        )
    if not isfinite(metric.value):
        return CheckResult(
            requirement.requirement_id,
            "NOT_EVALUABLE",
            "Kennwert ist nicht endlich.",
            metric,
            requirement.limit,
            requirement.operator,
        )

    passed = _compare(metric.value, requirement.operator, requirement.limit)
    return CheckResult(
        requirement.requirement_id,
        "PASS" if passed else "FAIL",
        "Anforderung erfüllt." if passed else "Anforderung nicht erfüllt.",
        metric,
        requirement.limit,
        requirement.operator,
    )


def _verification_status(checks: tuple[CheckResult, ...], requirements: tuple[StandardRequirement, ...]) -> str:
    mandatory_statuses = {
        check.status for check, requirement in zip(checks, requirements, strict=True) if requirement.mandatory
    }
    if "FAIL" in mandatory_statuses:
        return "FAIL"
    if "NOT_EVALUABLE" in mandatory_statuses:
        return "NOT_EVALUABLE"
    return "PASS"


def _units_match(metric_unit: str | None, requirement_unit: str | None) -> bool:
    if not metric_unit or not requirement_unit:
        return False
    return metric_unit.strip().casefold() == requirement_unit.strip().casefold()


def _compare(value: float, operator: str, limit: float) -> bool:
    return {
        "<": value < limit,
        "<=": value <= limit,
        "==": value == limit,
        ">=": value >= limit,
        ">": value > limit,
    }[operator]


def build_verification_readiness_items() -> tuple[VerificationReadinessItem, ...]:
    """Liefert belegte Kandidaten, ohne Normwerte oder Rechenregeln zu erfinden."""

    profile_edition = _single_profile_edition()
    return (
        VerificationReadinessItem(
            criterion_id="din18599_usage_profiles",
            criterion="Nutzungsprofil-Vertrag",
            standard_reference="DIN/TS 18599-10",
            edition=profile_edition,
            required_inputs=("Profil-ID", "Tabellenreferenz", "manuell geprüfte Profilwerte"),
            method_status="schema_ready_values_not_released",
            metadata_basis="versioned_user_supplied_metadata_only",
            rights_status="norm_content_not_released",
            content_access_status="machine_content_access_blocked",
            test_status="contract_tests_pending",
            stage3_status="NOT_EVALUABLE",
            reason=(
                f"{len(DIN_USAGE_PROFILE_METADATA)} Profilidentitäten sind vorhanden; "
                "geschützte Profilwerte sind nicht freigegeben."
            ),
            next_gate="Werte, Fundstelle, Rechte und fachlichen Test manuell bestätigen.",
        ),
        VerificationReadinessItem(
            criterion_id="din4108_2_overtemperature_degree_hours",
            criterion="Übertemperatur-Gradstunden",
            standard_reference="DIN 4108-2",
            edition="nicht fachlich bestätigt",
            required_inputs=(
                "operative Temperatur",
                "Zeitstempel und Zeitschritt",
                "Nutzungszeit",
                "fachlich geprüfte Methode und Kriterien",
            ),
            method_status="data_field_candidate_rule_not_defined",
            metadata_basis="legacy_field_name_and_filename_metadata_only",
            rights_status="norm_content_not_released",
            content_access_status="machine_content_access_blocked",
            test_status="no_verified_method_test",
            stage3_status="NOT_EVALUABLE",
            reason="Das Legacy-Excel-Feld besitzt weder Berechnung noch freigegebenes Kriterium.",
            next_gate=(
                "Dokument, Ausgabe, Fundstelle, Verarbeitungsrecht, Methode, Geltungsbereich, "
                "Kriterien und Referenztest bestätigen."
            ),
        ),
    )


def build_verification_readiness_rows() -> list[dict[str, str]]:
    """Bereitet alle Readiness-Kandidaten als neutrale Tabelle auf."""

    return [readiness_item_row(item) for item in build_verification_readiness_items()]


def _single_profile_edition() -> str:
    editions = {profile.edition for profile in DIN_USAGE_PROFILE_METADATA}
    return next(iter(editions)) if len(editions) == 1 else "uneinheitliche Metadaten"
