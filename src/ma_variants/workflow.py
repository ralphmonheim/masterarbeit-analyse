"""Kompakte P017-Kette fuer verifizierte Varianten.

Die Funktionen halten die fuenf fachlichen Schritte sichtbar getrennt:
VSP (Raum), VVER (Pruefung), VCAT (Index), VSEL (Auswahl) und VGEN
(vollstaendige Varianten). Dadurch muss die UI keine eigene Fachlogik tragen.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from ma_parameters import BaselineParameterSnapshot, ParameterVariationSpecification, VariationDimension

from .preprocess import PreprocessVariant, VariationValue, build_baseline_variant, build_explicit_variant

MAX_CATALOG_VARIANTS = 500


@dataclass(frozen=True, slots=True)
class VariantRule:
    """Fachliche Randbedingung fuer einen Variantenraum."""

    rule_id: str
    owner_module: str
    scope_type: str
    scope_id: str
    title: str
    short_description: str
    details: str
    rule_type: str
    parameter_keys: tuple[str, ...]
    dimension_key: str = ""
    severity: str = "block"


@dataclass(frozen=True, slots=True)
class VariantCandidate:
    """Kompakter Kandidat vor der vollstaendigen Variantenmaterialisierung."""

    candidate_id: str
    selected_options: tuple[tuple[str, str], ...]
    resolved_values: tuple[VariationValue, ...]


@dataclass(frozen=True, slots=True)
class VariantVerification:
    """Pruefergebnis eines Kandidaten inklusive Ausschlussgrund."""

    candidate: VariantCandidate
    is_valid: bool
    messages: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class VariantCatalog:
    """Verifizierter, begrenzter Variantenindex (VCAT)."""

    catalog_id: str
    baseline_snapshot_id: str
    candidates: tuple[VariantCandidate, ...]
    rejected_count: int


@dataclass(frozen=True, slots=True)
class VariantSelection:
    """Ausgewählte Kandidat-IDs eines einzelnen Katalogs."""

    catalog_id: str
    candidate_ids: tuple[str, ...]
    method: str


@dataclass(frozen=True, slots=True)
class VariantWorkflowResult:
    """Darstellbarer Status aller P017-Schritte."""

    specification: ParameterVariationSpecification
    rules: tuple[VariantRule, ...]
    candidates: tuple[VariantCandidate, ...]
    verifications: tuple[VariantVerification, ...]
    catalog: VariantCatalog


def default_zone_rules(specification: ParameterVariationSpecification) -> tuple[VariantRule, ...]:
    """Liefert die erste Regel aus der gemeinsam festgelegten Referenz."""
    rules: list[VariantRule] = []
    for dimension in specification.unlocked_dimensions:
        if dimension.value_mode == "coupled_option" and len(dimension.target_parameter_keys) == 2:
            rules.append(
                VariantRule(
                    rule_id=f"RULE-{dimension.dimension_key.upper()}",
                    owner_module="zones",
                    scope_type="zone",
                    scope_id=dimension.scope_id,
                    title="Heiz- und Kuehlsollwertfaktor gemeinsam fuehren",
                    short_description="Beide Sollwertfaktoren der Buerzone muessen identisch sein.",
                    details=(
                        "Diese Randbedingung wird als gekoppelte Variationsdimension umgesetzt. "
                        "Eine Option setzt denselben Faktor fuer Heiz- und Kuehlsollwert; "
                        "unabhaengige Kombinationen werden nicht erzeugt."
                    ),
                    rule_type="coupled_dimension",
                    parameter_keys=dimension.target_parameter_keys,
                    dimension_key=dimension.dimension_key,
                )
            )
    return tuple(rules)


def build_variant_workflow(
    baseline: BaselineParameterSnapshot,
    specification: ParameterVariationSpecification,
    rules: tuple[VariantRule, ...] | None = None,
) -> VariantWorkflowResult:
    """Fuehrt VSP, VVER und VCAT fuer die aktuelle Referenz aus."""
    if specification.baseline_snapshot_id != baseline.snapshot_id:
        raise ValueError("Die Variationsspezifikation referenziert nicht die aktuelle Baseline.")
    if specification.baseline_content_hash != baseline.content_hash:
        raise ValueError("Die Variationsspezifikation ist gegenueber der Baseline veraltet.")

    effective_rules = rules if rules is not None else default_zone_rules(specification)
    candidates = build_variant_space(baseline, specification)
    verifications = tuple(verify_candidate(candidate, effective_rules) for candidate in candidates)
    valid_candidates = tuple(item.candidate for item in verifications if item.is_valid)
    if len(valid_candidates) > MAX_CATALOG_VARIANTS:
        raise ValueError(f"Der Variantenkatalog darf hoechstens {MAX_CATALOG_VARIANTS} Eintraege enthalten.")
    catalog = VariantCatalog(
        catalog_id=f"VCAT-{specification.specification_id}",
        baseline_snapshot_id=baseline.snapshot_id,
        candidates=valid_candidates,
        rejected_count=len(candidates) - len(valid_candidates),
    )
    return VariantWorkflowResult(specification, effective_rules, candidates, verifications, catalog)


def build_variant_space(
    baseline: BaselineParameterSnapshot,
    specification: ParameterVariationSpecification,
) -> tuple[VariantCandidate, ...]:
    """Erzeugt den VSP nur aus nicht gesperrten Variationsdimensionen."""
    dimensions = specification.unlocked_dimensions
    if not dimensions:
        return ()
    baseline_values = {value.parameter_key: value for value in baseline.parameter_values}
    candidates: list[VariantCandidate] = []
    for index, selected_options in enumerate(product(*(dimension.options for dimension in dimensions)), start=1):
        option_pairs = tuple(
            (dimension.dimension_key, option.option_key) for dimension, option in zip(dimensions, selected_options, strict=True)
        )
        values: list[VariationValue] = []
        for dimension, option in zip(dimensions, selected_options, strict=True):
            values.extend(_resolve_dimension_values(dimension, option.value, baseline_values))
        candidates.append(
            VariantCandidate(
                candidate_id=f"VAR-{index:04d}",
                selected_options=option_pairs,
                resolved_values=tuple(values),
            )
        )
    return tuple(candidates)


def verify_candidate(candidate: VariantCandidate, rules: tuple[VariantRule, ...]) -> VariantVerification:
    """Prueft VVER-Regeln und dokumentiert jede Ablehnung."""
    values_by_key = {value.parameter_key: value.value for value in candidate.resolved_values}
    messages: list[str] = []
    for rule in rules:
        if rule.rule_type == "coupled_dimension":
            selected_dimension_keys = {dimension_key for dimension_key, _ in candidate.selected_options}
            if rule.dimension_key not in selected_dimension_keys:
                messages.append(f"{rule.rule_id}: gekoppelte Dimension fehlt.")
            continue
        if rule.rule_type != "equal_values":
            messages.append(f"{rule.rule_id}: unbekannter Regeltyp '{rule.rule_type}'.")
            continue
        compared = [values_by_key.get(key) for key in rule.parameter_keys]
        if None in compared or len(set(compared)) != 1:
            messages.append(f"{rule.rule_id}: {rule.short_description}")
    return VariantVerification(candidate, not messages, tuple(messages))


def select_catalog_candidates(
    catalog: VariantCatalog,
    candidate_ids: tuple[str, ...],
    *,
    method: str = "manual",
) -> VariantSelection:
    """Erzeugt VSEL ausschliesslich aus IDs des vorliegenden Katalogs."""
    known_ids = {candidate.candidate_id for candidate in catalog.candidates}
    unknown_ids = set(candidate_ids) - known_ids
    if unknown_ids:
        raise ValueError(f"Auswahl enthält unbekannte Varianten: {', '.join(sorted(unknown_ids))}.")
    return VariantSelection(catalog.catalog_id, tuple(candidate_ids), method)


def generate_selected_variants(
    baseline: BaselineParameterSnapshot,
    catalog: VariantCatalog,
    selection: VariantSelection,
) -> tuple[PreprocessVariant, ...]:
    """Materialisiert VGEN erst fuer die in VSEL ausgewaehlten Kandidaten."""
    if selection.catalog_id != catalog.catalog_id:
        raise ValueError("Die Auswahl gehoert nicht zum angegebenen Variantenkatalog.")
    candidate_by_id = {candidate.candidate_id: candidate for candidate in catalog.candidates}
    variants: list[PreprocessVariant] = []
    for candidate_id in selection.candidate_ids:
        candidate = candidate_by_id[candidate_id]
        if not candidate.resolved_values:
            variants.append(build_baseline_variant(baseline))
            continue
        variants.append(
            build_explicit_variant(
                baseline,
                variant_id=candidate.candidate_id,
                label=f"Variante {candidate.candidate_id}",
                values=candidate.resolved_values,
            )
        )
    return tuple(variants)


def catalog_rows(catalog: VariantCatalog) -> list[dict[str, object]]:
    """UI-Tabelle fuer VCAT."""
    return [
        {
            "VAR-ID": candidate.candidate_id,
            "Optionen": ", ".join(f"{dimension}={option}" for dimension, option in candidate.selected_options),
            "Aufgeloeste Werte": ", ".join(f"{value.parameter_key}={value.value:g} {value.unit}" for value in candidate.resolved_values),
        }
        for candidate in catalog.candidates
    ]


def rule_rows(rules: tuple[VariantRule, ...]) -> list[dict[str, object]]:
    """Kompakte Regelübersicht mit Herkunft und Geltung."""
    return [
        {
            "Regel": rule.title,
            "Quellmodul": rule.owner_module,
            "Geltung": f"{rule.scope_type}: {rule.scope_id}",
            "Beschreibung": rule.short_description,
            "Schwere": rule.severity,
        }
        for rule in rules
    ]


def _resolve_dimension_values(
    dimension: VariationDimension,
    option_value: object,
    baseline_values: dict[str, object],
) -> list[VariationValue]:
    values: list[VariationValue] = []
    for parameter_key in dimension.target_parameter_keys:
        baseline_value = baseline_values[parameter_key]
        if dimension.value_mode == "coupled_option":
            value = float(baseline_value.value) * float(option_value)
            values.append(VariationValue(parameter_key, value, baseline_value.unit))
        else:
            values.append(VariationValue(parameter_key, option_value, baseline_value.unit))
    return values
