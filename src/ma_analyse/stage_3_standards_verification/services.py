"""Wertfreie Readiness-Prüfung für später freizugebende Normnachweise."""

from __future__ import annotations

from ma_parameters.usage_profile_catalog import DIN_USAGE_PROFILE_METADATA

from .models import VerificationReadinessItem, readiness_item_row


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
