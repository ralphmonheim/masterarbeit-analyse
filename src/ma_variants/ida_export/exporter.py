"""Erzeugung einer vorbereiteten IDA-ICE-Uebergabestruktur."""

from __future__ import annotations

import json
import re
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..system_catalog import SystemTemplateResolution
from ..variant_manager import Variant, VariantValue
from .config import DEFAULT_IDA_EXPORT_CONFIG, IdaExportSettings, load_ida_export_settings
from .models import IdaExportResult, IdaVariantExportResult

GeneratedVariant = tuple[Variant, list[VariantValue]]

INVALID_FOLDER_CHARS = re.compile(r'[<>:"/\\|?*]+')


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_folder_name(folder_name: str, fallback: str) -> str:
    cleaned = INVALID_FOLDER_CHARS.sub("_", folder_name).strip().strip(".")
    cleaned = re.sub(r"\s+", "_", cleaned)
    return cleaned or fallback


def _format_variant_folder(variant: Variant, template: str) -> str:
    raw_folder_name = template.format(
        variant_key=variant.variant_key,
        variant_name=variant.variant_name,
        status=variant.status,
    )
    return _safe_folder_name(raw_folder_name, fallback=variant.variant_key)


def _variant_value_to_parameter(variant_value: VariantValue) -> dict[str, Any]:
    return {
        "parameter_key": variant_value.parameter_key,
        "option_key": variant_value.option_key,
        "resolved_value": variant_value.resolved_value,
        "unit": None,
        "source": "variant_value",
        "system_template_key": None,
    }


def _system_template_values_to_parameters(
    resolution: SystemTemplateResolution | None,
) -> list[dict[str, Any]]:
    if resolution is None:
        return []
    return [
        {
            "parameter_key": resolved_value.parameter_key,
            "option_key": None,
            "resolved_value": resolved_value.resolved_value,
            "unit": resolved_value.unit,
            "source": resolved_value.value_source,
            "system_template_key": resolved_value.system_template_key,
        }
        for resolved_value in resolution.resolved_values
    ]


def _resolved_parameters_payload(
    variant: Variant,
    variant_values: list[VariantValue],
    resolution: SystemTemplateResolution | None,
) -> dict[str, Any]:
    variant_parameters = [_variant_value_to_parameter(variant_value) for variant_value in variant_values]
    template_parameters = _system_template_values_to_parameters(resolution)
    return {
        "variant_key": variant.variant_key,
        "variant_name": variant.variant_name,
        "selected_system_templates": resolution.selected_template_keys if resolution is not None else [],
        "dependency_warnings": resolution.dependency_warnings if resolution is not None else [],
        "parameters": [*variant_parameters, *template_parameters],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_export_log(
    path: Path,
    *,
    variant: Variant,
    export_dir: Path,
    export_time: str,
    settings: IdaExportSettings,
    parameter_count: int,
) -> None:
    lines = [
        "IDA ICE export preparation",
        f"Variant: {variant.variant_key} - {variant.variant_name}",
        f"Status: {variant.status}",
        f"Export time: {export_time}",
        f"Source config: {settings.source_config}",
        f"Export directory: {export_dir}",
        "",
        "Steps:",
        "- Created variant export directory.",
        f"- Wrote {settings.metadata_filename}.",
        f"- Wrote {settings.resolved_parameters_filename} with {parameter_count} parameter value(s).",
        "- Wrote export log.",
        "- No existing IDA ICE files were modified.",
        "- IDA ICE variant manager was not started.",
        "- No simulation was started from Python.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_ida_variant_structure(
    selected_variants: list[GeneratedVariant],
    settings: IdaExportSettings | None = None,
    config_path: str | Path = DEFAULT_IDA_EXPORT_CONFIG,
    output_root: str | Path | None = None,
    system_template_resolutions: dict[str, SystemTemplateResolution] | None = None,
    export_time: str | None = None,
) -> IdaExportResult:
    """Erzeugt eine vorbereitete IDA-ICE-Uebergabestruktur je Variante."""
    resolved_settings = settings or load_ida_export_settings(config_path)
    if output_root is not None:
        resolved_settings = replace(resolved_settings, output_root=Path(output_root))

    export_root = resolved_settings.output_root
    export_root.mkdir(parents=True, exist_ok=True)
    resolved_export_time = export_time or _utc_timestamp()
    variant_results: list[IdaVariantExportResult] = []

    for variant, variant_values in selected_variants:
        export_dir = export_root / _format_variant_folder(variant, resolved_settings.variant_folder_template)
        export_dir.mkdir(parents=True, exist_ok=True)
        resolution = (system_template_resolutions or {}).get(variant.variant_key)

        metadata_path = export_dir / resolved_settings.metadata_filename
        resolved_parameters_path = export_dir / resolved_settings.resolved_parameters_filename
        export_log_path = export_dir / resolved_settings.export_log_filename

        metadata = {
            "variant_key": variant.variant_key,
            "variant_name": variant.variant_name,
            "export_time": resolved_export_time,
            "status": variant.status,
            "source_config": resolved_settings.source_config.as_posix(),
        }
        resolved_parameters = _resolved_parameters_payload(variant, variant_values, resolution)

        _write_json(metadata_path, metadata)
        _write_json(resolved_parameters_path, resolved_parameters)
        _write_export_log(
            export_log_path,
            variant=variant,
            export_dir=export_dir,
            export_time=resolved_export_time,
            settings=resolved_settings,
            parameter_count=len(resolved_parameters["parameters"]),
        )

        variant_results.append(
            IdaVariantExportResult(
                variant_key=variant.variant_key,
                export_dir=export_dir,
                metadata_path=metadata_path,
                resolved_parameters_path=resolved_parameters_path,
                export_log_path=export_log_path,
            )
        )

    return IdaExportResult(output_root=export_root, variant_exports=variant_results)
