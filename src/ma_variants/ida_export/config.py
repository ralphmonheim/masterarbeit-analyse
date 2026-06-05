"""Konfiguration fuer die vorbereitete IDA-ICE-Uebergabestruktur."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..importing.io import load_config_file
from ..validation import require_non_empty

DEFAULT_IDA_EXPORT_CONFIG = Path("config/ma_variants/export/example_ida_export.yaml")


@dataclass(frozen=True, slots=True)
class IdaExportSettings:
    """Einstellungen fuer den dateibasierten IDA-ICE-Basisexport."""

    output_root: Path
    variant_folder_template: str
    metadata_filename: str
    resolved_parameters_filename: str
    export_log_filename: str
    source_config: Path

    def __post_init__(self) -> None:
        model_name = type(self).__name__
        require_non_empty(self.variant_folder_template, "variant_folder_template", model_name)
        require_non_empty(self.metadata_filename, "metadata_filename", model_name)
        require_non_empty(self.resolved_parameters_filename, "resolved_parameters_filename", model_name)
        require_non_empty(self.export_log_filename, "export_log_filename", model_name)


def _get_string(raw_config: dict[str, Any], key: str, default: str) -> str:
    value = raw_config.get(key, default)
    if not isinstance(value, str):
        raise ValueError(f"ida_export.{key} muss ein Textwert sein.")
    return value


def load_ida_export_settings(config_path: str | Path = DEFAULT_IDA_EXPORT_CONFIG) -> IdaExportSettings:
    """Laedt die Exportkonfiguration aus YAML oder JSON."""
    path = Path(config_path)
    data = load_config_file(path)
    raw_config = data.get("ida_export")
    if not isinstance(raw_config, dict):
        raise ValueError("Konfiguration muss ein Objekt 'ida_export' enthalten.")

    output_root = raw_config.get("output_root", "data/ma_variants/ida_exports")
    if not isinstance(output_root, str):
        raise ValueError("ida_export.output_root muss ein Textwert sein.")

    return IdaExportSettings(
        output_root=Path(output_root),
        variant_folder_template=_get_string(raw_config, "variant_folder_template", "{variant_key}"),
        metadata_filename=_get_string(raw_config, "metadata_filename", "metadata.json"),
        resolved_parameters_filename=_get_string(
            raw_config,
            "resolved_parameters_filename",
            "resolved_parameters.json",
        ),
        export_log_filename=_get_string(raw_config, "export_log_filename", "export_log.txt"),
        source_config=path,
    )
