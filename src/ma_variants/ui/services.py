"""Testbare Hilfsfunktionen fuer die lokale UI."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from ..importing.catalog import import_catalog
from ..option_catalog import OptionSet, OptionValue
from ..parameter_catalog import Parameter
from ..reporting import VariantExportResult, export_variant_overview
from ..selection import select_variants_by_key
from ..variant_manager import (
    Variant,
    VariantValue,
    calculate_theoretical_variant_count,
    generate_variants,
)

GeneratedVariant = tuple[Variant, list[VariantValue]]

DEFAULT_PARAMETER_CONFIG = Path("config/parameters/example_parameters.yaml")
DEFAULT_OPTION_CONFIG = Path("config/options/example_options.yaml")
DEFAULT_EXPORT_DIR = Path("data/exports")


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


def load_variant_ui_data(
    parameter_config: str | Path = DEFAULT_PARAMETER_CONFIG,
    option_config: str | Path = DEFAULT_OPTION_CONFIG,
) -> VariantUiData:
    """Laedt Katalogdaten, berechnet Variantenanzahl und erzeugt Beispielvarianten."""
    catalog = import_catalog(parameter_config, option_config, report_path=None)
    theoretical_variant_count = calculate_theoretical_variant_count(
        catalog.parameters,
        catalog.option_values,
    )
    generated_variants = generate_variants(catalog.parameters, catalog.option_values)
    return VariantUiData(
        parameters=catalog.parameters,
        option_sets=catalog.option_sets,
        option_values=catalog.option_values,
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
