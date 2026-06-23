"""Testbare Hilfsfunktionen fuer die lokale UI."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

from ma_project import VariantNamingProfile

from ..importing.catalog import import_catalog
from ..naming import NamingRulePart, NamingRules, apply_variant_names, load_naming_rules
from ..option_catalog import OptionSet, OptionValue
from ..parameter_catalog import Parameter
from ..reporting import VariantExportResult, export_variant_overview
from ..selection import filter_variants_by_options, random_select_variants, select_variants_by_key
from ..variant_manager import (
    Variant,
    VariantValue,
    calculate_theoretical_variant_count,
    generate_variants,
)

GeneratedVariant = tuple[Variant, list[VariantValue]]

DEFAULT_PARAMETER_CONFIG = Path("config/ma_variants/parameters/example_parameters.yaml")
DEFAULT_OPTION_CONFIG = Path("config/ma_variants/options/example_options.yaml")
DEFAULT_EXPORT_DIR = Path("data/ma_variants/exports")
DEFAULT_NAMING_CONFIG = Path("config/ma_variants/naming/example_naming_rules.yaml")


@dataclass(frozen=True, slots=True)
class SelectionMethodInfo:
    """Beschreibt eine in der UI angezeigte Auswahlmethode."""

    method_key: str
    label: str
    is_implemented: bool
    notes: str


@dataclass(frozen=True, slots=True)
class VariantUiData:
    """Gebündelte Daten fuer die lokale Variantenoberflaeche."""

    parameters: list[Parameter]
    option_sets: list[OptionSet]
    option_values: list[OptionValue]
    theoretical_variant_count: int
    generated_variants: list[GeneratedVariant]


@dataclass(frozen=True, slots=True)
class ResultFileInfo:
    """Metadaten einer erzeugten Ergebnisdatei."""

    file_name: str
    path: Path
    size_bytes: int
    modified_at: str


SELECTION_METHODS: tuple[SelectionMethodInfo, ...] = (
    SelectionMethodInfo(
        method_key="manual",
        label="Manuell nach variant_key",
        is_implemented=True,
        notes="Waehlt Varianten ueber ihre technischen variant_key Werte aus.",
    ),
    SelectionMethodInfo(
        method_key="random",
        label="Vollstaendig zufaellig",
        is_implemented=True,
        notes="Waehlt reproduzierbar eine zufaellige Teilmenge mit festem random_seed aus.",
    ),
    SelectionMethodInfo(
        method_key="filter",
        label="Auswahl bestimmter Parameter",
        is_implemented=True,
        notes="Filtert Varianten ueber parameter_key und erlaubte option_key Werte.",
    ),
    SelectionMethodInfo(
        method_key="monte_carlo",
        label="Monte Carlo",
        is_implemented=False,
        notes="Nur vorbereitet. Es gibt noch keine Monte-Carlo-Logik.",
    ),
    SelectionMethodInfo(
        method_key="structured_coverage",
        label="Strukturierte Abdeckung",
        is_implemented=False,
        notes="Nur vorbereitet. Es gibt noch keine Abdeckungslogik.",
    ),
    SelectionMethodInfo(
        method_key="sensitivity",
        label="Sensitivitaetsvarianten",
        is_implemented=False,
        notes="Nur vorbereitet. Es gibt noch keine Sensitivitaetsanalyse.",
    ),
    SelectionMethodInfo(
        method_key="rule_based",
        label="Regelbasierte Auswahl",
        is_implemented=False,
        notes="Nur vorbereitet. Es gibt noch keine komplexe Regellogik.",
    ),
)


def load_variant_ui_data(
    parameter_config: str | Path = DEFAULT_PARAMETER_CONFIG,
    option_config: str | Path = DEFAULT_OPTION_CONFIG,
) -> VariantUiData:
    """Laedt Katalogdaten, berechnet Variantenanzahl und erzeugt Beispielvarianten."""
    catalog = import_catalog(parameter_config, option_config, report_path=None)
    return build_variant_ui_data(
        catalog.parameters,
        catalog.option_sets,
        catalog.option_values,
    )


def build_variant_ui_data(
    parameters: list[Parameter],
    option_sets: list[OptionSet],
    option_values: list[OptionValue],
) -> VariantUiData:
    """Erzeugt den Variantenraum aus bereits validierten Katalogobjekten."""
    theoretical_variant_count = calculate_theoretical_variant_count(
        parameters,
        option_values,
    )
    generated_variants = generate_variants(parameters, option_values)
    return VariantUiData(
        parameters=parameters,
        option_sets=option_sets,
        option_values=option_values,
        theoretical_variant_count=theoretical_variant_count,
        generated_variants=generated_variants,
    )


def parameter_rows(parameters: list[Parameter]) -> list[dict[str, object]]:
    """Bereitet Parameter fuer eine UI-Tabelle auf."""
    return [asdict(parameter) for parameter in parameters]


def option_value_rows(
    option_sets: list[OptionSet],
    option_values: list[OptionValue],
) -> list[dict[str, object]]:
    """Bereitet Optionsgruppen und Optionswerte fuer eine UI-Tabelle auf."""
    option_set_by_key = {option_set.option_set_key: option_set for option_set in option_sets}
    rows: list[dict[str, object]] = []
    for option_value in option_values:
        option_set = option_set_by_key.get(option_value.option_set_key)
        rows.append(
            {
                "option_set_key": option_value.option_set_key,
                "option_set_name": option_set.display_name if option_set is not None else "",
                "option_key": option_value.option_key,
                "label": option_value.label,
                "value": option_value.value,
                "unit": option_value.unit,
                "is_active": option_value.is_active,
            }
        )
    return rows


def variant_rows(generated_variants: list[GeneratedVariant]) -> list[dict[str, object]]:
    """Bereitet Varianten fuer eine UI-Auswahlliste auf."""
    return [
        {
            "variant_key": variant.variant_key,
            "variant_name": variant.variant_name,
            "status": variant.status,
            "values": ", ".join(
                f"{variant_value.parameter_key}={variant_value.option_key}" for variant_value in variant_values
            ),
        }
        for variant, variant_values in generated_variants
    ]


def select_variants_for_export(
    generated_variants: list[GeneratedVariant],
    selected_variant_keys: list[str],
) -> list[GeneratedVariant]:
    """Waehlt Varianten ueber die bestehende Auswahlfunktion aus."""
    return select_variants_by_key(generated_variants, selected_variant_keys)


def selection_method_rows() -> list[dict[str, object]]:
    """Bereitet Auswahlmethoden fuer eine UI-Tabelle auf."""
    return [asdict(method) for method in SELECTION_METHODS]


def selection_method_by_label(label: str) -> SelectionMethodInfo:
    """Findet eine Auswahlmethode ueber ihre sichtbare UI-Beschriftung."""
    for method in SELECTION_METHODS:
        if method.label == label:
            return method
    raise ValueError(f"Unbekannte Auswahlmethode: {label}")


def select_variants_by_method(
    generated_variants: list[GeneratedVariant],
    method_key: str,
    *,
    selected_variant_keys: list[str] | None = None,
    random_count: int = 0,
    random_seed: int = 42,
    filter_criteria: dict[str, str | list[str]] | None = None,
) -> list[GeneratedVariant]:
    """Fuehrt die in der UI waehlbaren einfachen Auswahlmethoden aus."""
    if method_key == "manual":
        return select_variants_by_key(generated_variants, selected_variant_keys or [])
    if method_key == "random":
        return random_select_variants(generated_variants, random_count, random_seed)
    if method_key == "filter":
        return filter_variants_by_options(generated_variants, filter_criteria or {})

    raise NotImplementedError(f"Auswahlmethode '{method_key}' ist vorbereitet, aber noch nicht implementiert.")


def apply_naming_to_ui_data(
    ui_data: VariantUiData,
    naming_config: str | Path = DEFAULT_NAMING_CONFIG,
) -> VariantUiData:
    """Wendet die bestehenden Namensregeln auf alle erzeugten Varianten an."""
    naming_rules = load_naming_rules(naming_config)
    named_variants = apply_variant_names(ui_data.generated_variants, naming_rules)
    return replace(ui_data, generated_variants=named_variants)


def apply_naming_profile_to_ui_data(
    ui_data: VariantUiData,
    profile: VariantNamingProfile,
) -> VariantUiData:
    """Wendet ein formatneutrales Projekt-Benennungsprofil auf Varianten an."""
    naming_rules = NamingRules(
        prefix=profile.prefix,
        index_width=profile.index_width,
        separator=profile.separator,
        include_index=profile.include_index,
        parts=[
            NamingRulePart(
                parameter_key=part.parameter_key,
                option_tokens=dict(part.option_tokens),
            )
            for part in profile.parts
        ],
    )
    named_variants = apply_variant_names(ui_data.generated_variants, naming_rules)
    return replace(ui_data, generated_variants=named_variants)


def run_variant_export(
    ui_data: VariantUiData,
    selected_variants: list[GeneratedVariant],
    output_dir: str | Path = DEFAULT_EXPORT_DIR,
) -> VariantExportResult:
    """Startet den bestehenden Basisexport fuer ausgewaehlte Varianten."""
    return export_variant_overview(
        all_variants=ui_data.generated_variants,
        selected_variants=selected_variants,
        parameters=ui_data.parameters,
        option_sets=ui_data.option_sets,
        option_values=ui_data.option_values,
        output_dir=output_dir,
    )


def list_result_files(output_dir: str | Path = DEFAULT_EXPORT_DIR) -> list[ResultFileInfo]:
    """Listet vorhandene Ergebnisdateien fuer die UI."""
    export_dir = Path(output_dir)
    if not export_dir.exists():
        return []

    result_files: list[ResultFileInfo] = []
    for path in sorted(item for item in export_dir.iterdir() if item.is_file()):
        stat = path.stat()
        modified_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).replace(microsecond=0).isoformat()
        result_files.append(
            ResultFileInfo(
                file_name=path.name,
                path=path,
                size_bytes=stat.st_size,
                modified_at=modified_at,
            )
        )
    return result_files
