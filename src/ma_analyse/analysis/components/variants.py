"""Datenbezogene Helfer fuer Varianten- und Ordnernamen."""

from __future__ import annotations

from pathlib import Path

RAW_VARIANT_SUFFIX = "_rohdaten"
PROCESSED_VARIANT_SUFFIX = "_nutzdaten"
KNOWN_VARIANT_SUFFIXES = (RAW_VARIANT_SUFFIX, PROCESSED_VARIANT_SUFFIX)


def normalize_variant_name(variant_name: str, suffix: str) -> str:
    """Ergaenzt einen erwarteten Varianten-Suffix, falls er fehlt."""
    if variant_name.endswith(suffix):
        return variant_name
    return f"{variant_name}{suffix}"


def strip_variant_suffix(variant_name: str) -> str:
    """Entfernt bekannte Varianten-Suffixe fuer Vergleich und Anzeige."""
    for suffix in KNOWN_VARIANT_SUFFIXES:
        if variant_name.endswith(suffix):
            return variant_name[: -len(suffix)]
    return variant_name


def get_variant_display_name(variant_name: str | Path) -> str:
    """Gibt den kurzen Anzeigenamen einer Variante oder eines Pfads zurueck."""
    return strip_variant_suffix(Path(variant_name).name)


def build_nutzdaten_folder_name(variant_name: str | Path) -> str:
    """Leitet aus einem Rohdaten-Variantennamen den Nutzdatenordner ab."""
    raw_name = Path(variant_name).name
    if raw_name.endswith(RAW_VARIANT_SUFFIX):
        return f"{raw_name[: -len(RAW_VARIANT_SUFFIX)]}{PROCESSED_VARIANT_SUFFIX}"
    return normalize_variant_name(raw_name, PROCESSED_VARIANT_SUFFIX)


def normalize_selected_variants(selected_variants: list[str] | tuple[str, ...] | None, suffix: str) -> set[str] | None:
    """Normalisiert eine optionale Variantenliste auf einen erwarteten Suffix."""
    if selected_variants is None:
        return None
    return {normalize_variant_name(variant.strip(), suffix) for variant in selected_variants if variant.strip()}


def normalize_selected_variant_stems(selected_variants: list[str] | tuple[str, ...] | None) -> set[str] | None:
    """Normalisiert eine optionale Variantenliste auf suffixfreie Vergleichsnamen."""
    if selected_variants is None:
        return None
    return {strip_variant_suffix(variant.strip()) for variant in selected_variants if variant.strip()}
