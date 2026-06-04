"""Zuordnung vorhandener Ergebnisordner zu Varianten."""

from __future__ import annotations

from pathlib import Path

from ..variant_manager import Variant
from .models import SimulationResultFolder, VariantResultMapping

PROCESSED_VARIANT_SUFFIX = "_nutzdaten"


def _strip_result_suffix(name: str) -> str:
    if name.endswith(PROCESSED_VARIANT_SUFFIX):
        return name[: -len(PROCESSED_VARIANT_SUFFIX)]
    return name


def _normalize_candidate(name: str) -> str:
    return _strip_result_suffix(name).strip().casefold()


def _result_folder_key(path: Path) -> str:
    return _strip_result_suffix(path.name)


def discover_result_folders(results_root: str | Path = "data/database") -> list[SimulationResultFolder]:
    """Findet vorhandene aufbereitete Variantenordner."""
    root = Path(results_root)
    if not root.exists() or not root.is_dir():
        return []

    folders = []
    for child in sorted(root.iterdir(), key=lambda path: path.name.casefold()):
        if not child.is_dir():
            continue
        if not child.name.endswith(PROCESSED_VARIANT_SUFFIX):
            continue
        result_key = _result_folder_key(child)
        folders.append(
            SimulationResultFolder(
                result_key=result_key,
                result_dir=child,
                display_name=result_key,
            )
        )
    return folders


def resolve_result_folder(
    variant: Variant,
    result_folders: list[SimulationResultFolder],
    folder_override: str | None = None,
) -> SimulationResultFolder | None:
    """Findet den passendsten Ergebnisordner fuer eine Variante."""
    candidates = [variant.variant_key, variant.variant_name]
    if folder_override:
        candidates.insert(0, folder_override)

    normalized_candidates = {_normalize_candidate(candidate) for candidate in candidates if candidate}
    for result_folder in result_folders:
        folder_candidates = {
            _normalize_candidate(result_folder.result_key),
            _normalize_candidate(result_folder.result_dir.name),
            _normalize_candidate(result_folder.display_name),
        }
        if normalized_candidates & folder_candidates:
            return result_folder
    return None


def map_result_folders_to_variants(
    variants: list[Variant],
    results_root: str | Path = "data/database",
    folder_overrides: dict[str, str] | None = None,
) -> list[VariantResultMapping]:
    """Ordnet vorhandene Ergebnisordner einer Variantenliste zu."""
    result_folders = discover_result_folders(results_root)
    mappings: list[VariantResultMapping] = []
    for variant in variants:
        override = (folder_overrides or {}).get(variant.variant_key)
        result_folder = resolve_result_folder(
            variant=variant,
            result_folders=result_folders,
            folder_override=override,
        )
        if result_folder is None:
            mappings.append(
                VariantResultMapping(
                    variant_key=variant.variant_key,
                    variant_name=variant.variant_name,
                    result_dir=None,
                    result_display_name=None,
                    is_mapped=False,
                    notes=["Kein passender Ergebnisordner gefunden."],
                )
            )
            continue

        mappings.append(
            VariantResultMapping(
                variant_key=variant.variant_key,
                variant_name=variant.variant_name,
                result_dir=result_folder.result_dir,
                result_display_name=result_folder.display_name,
                is_mapped=True,
                notes=[],
            )
        )
    return mappings
