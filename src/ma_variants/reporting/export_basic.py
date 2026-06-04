"""Kontrollierbare Basisexporte fuer Variantenuebersichten."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..option_catalog import OptionSet, OptionValue
from ..parameter_catalog import Parameter
from ..variant_manager import Variant, VariantValue

GeneratedVariant = tuple[Variant, list[VariantValue]]


@dataclass(frozen=True, slots=True)
class VariantExportReport:
    """Zusammenfassung eines Basisexports fuer Pruefung und Dokumentation."""

    total_variant_count: int
    selected_variant_count: int
    used_parameters: list[dict[str, str]]
    used_option_sets: list[dict[str, str]]
    exported_at: str
    missing_data_notes: list[str]


@dataclass(frozen=True, slots=True)
class VariantExportResult:
    """Dateipfade und Berichtsdaten eines vollstaendigen Basisexports."""

    json_path: Path
    csv_path: Path
    report_path: Path
    report: VariantExportReport


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _unique_in_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _variant_to_dict(variant: Variant, variant_values: list[VariantValue]) -> dict[str, Any]:
    return {
        **asdict(variant),
        "values": [asdict(variant_value) for variant_value in variant_values],
    }


def _selected_parameter_keys(selected_variants: list[GeneratedVariant]) -> list[str]:
    return _unique_in_order(
        [
            variant_value.parameter_key
            for _variant, variant_values in selected_variants
            for variant_value in variant_values
        ]
    )


def build_variant_export_report(
    all_variants: list[GeneratedVariant],
    selected_variants: list[GeneratedVariant],
    parameters: list[Parameter],
    option_sets: list[OptionSet],
    option_values: list[OptionValue] | None = None,
    exported_at: str | None = None,
) -> VariantExportReport:
    """Erstellt einen pruefbaren Bericht fuer einen Variantenexport."""
    parameter_by_key = {parameter.parameter_key: parameter for parameter in parameters}
    option_set_by_key = {option_set.option_set_key: option_set for option_set in option_sets}
    option_value_keys = (
        {option_value.option_key for option_value in option_values}
        if option_values is not None
        else None
    )

    selected_parameter_keys = _selected_parameter_keys(selected_variants)
    used_parameters: list[dict[str, str]] = []
    used_option_set_keys: list[str] = []
    missing_data_notes: list[str] = []

    for parameter_key in selected_parameter_keys:
        parameter = parameter_by_key.get(parameter_key)
        if parameter is None:
            missing_data_notes.append(
                "Parameter "
                f"'{parameter_key}' ist in ausgewaehlten Varianten enthalten, "
                "aber nicht im Parameterkatalog vorhanden."
            )
            used_parameters.append(
                {
                    "parameter_key": parameter_key,
                    "display_name": "",
                    "option_set_key": "",
                }
            )
            continue

        used_parameters.append(
            {
                "parameter_key": parameter.parameter_key,
                "display_name": parameter.display_name,
                "option_set_key": parameter.option_set_key,
            }
        )
        used_option_set_keys.append(parameter.option_set_key)

        if parameter.option_set_key not in option_set_by_key:
            missing_data_notes.append(
                "Optionsgruppe "
                f"'{parameter.option_set_key}' fuer Parameter "
                f"'{parameter.parameter_key}' fehlt im Optionskatalog."
            )

    if option_value_keys is not None:
        selected_option_keys = _unique_in_order(
            [
                variant_value.option_key
                for _variant, variant_values in selected_variants
                for variant_value in variant_values
            ]
        )
        for option_key in selected_option_keys:
            if option_key not in option_value_keys:
                missing_data_notes.append(
                    "Optionswert "
                    f"'{option_key}' ist in ausgewaehlten Varianten enthalten, "
                    "aber nicht im Optionskatalog vorhanden."
                )

    used_option_sets = [
        {
            "option_set_key": option_set_key,
            "display_name": option_set_by_key[option_set_key].display_name
            if option_set_key in option_set_by_key
            else "",
        }
        for option_set_key in _unique_in_order(used_option_set_keys)
    ]

    return VariantExportReport(
        total_variant_count=len(all_variants),
        selected_variant_count=len(selected_variants),
        used_parameters=used_parameters,
        used_option_sets=used_option_sets,
        exported_at=exported_at or _utc_timestamp(),
        missing_data_notes=missing_data_notes,
    )


def export_selected_variants_json(
    selected_variants: list[GeneratedVariant],
    output_path: str | Path,
) -> Path:
    """Exportiert ausgewaehlte Varianten als strukturierte JSON-Datei."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "variant_count": len(selected_variants),
        "variants": [
            _variant_to_dict(variant, variant_values)
            for variant, variant_values in selected_variants
        ],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def export_selected_variants_csv(
    selected_variants: list[GeneratedVariant],
    output_path: str | Path,
) -> Path:
    """Exportiert ausgewaehlte Varianten als flache CSV-Prueftabelle."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "variant_key",
        "variant_name",
        "status",
        "parameter_key",
        "option_key",
        "resolved_value",
    ]

    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for variant, variant_values in selected_variants:
            for variant_value in variant_values:
                writer.writerow(
                    {
                        "variant_key": variant.variant_key,
                        "variant_name": variant.variant_name,
                        "status": variant.status,
                        "parameter_key": variant_value.parameter_key,
                        "option_key": variant_value.option_key,
                        "resolved_value": variant_value.resolved_value,
                    }
                )

    return path


def export_variant_report(
    report: VariantExportReport,
    output_path: str | Path,
) -> Path:
    """Schreibt den Exportbericht als JSON-Datei."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(report), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def export_variant_overview(
    all_variants: list[GeneratedVariant],
    selected_variants: list[GeneratedVariant],
    parameters: list[Parameter],
    option_sets: list[OptionSet],
    output_dir: str | Path = Path("data/exports"),
    option_values: list[OptionValue] | None = None,
    exported_at: str | None = None,
) -> VariantExportResult:
    """Schreibt JSON, CSV und Bericht fuer ausgewaehlte Varianten."""
    export_dir = Path(output_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    report = build_variant_export_report(
        all_variants=all_variants,
        selected_variants=selected_variants,
        parameters=parameters,
        option_sets=option_sets,
        option_values=option_values,
        exported_at=exported_at,
    )
    json_path = export_selected_variants_json(
        selected_variants,
        export_dir / "selected_variants.json",
    )
    csv_path = export_selected_variants_csv(
        selected_variants,
        export_dir / "selected_variants.csv",
    )
    report_path = export_variant_report(report, export_dir / "variant_report.json")

    return VariantExportResult(
        json_path=json_path,
        csv_path=csv_path,
        report_path=report_path,
        report=report,
    )
