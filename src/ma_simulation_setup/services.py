"""Erstellung und Materialisierung neutraler P018-Run-Pakete."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import yaml

from ma_analyse import OutputRequirementProfile, default_output_requirements
from ma_parameters import BaselineParameterSnapshot, validate_baseline_parameter_snapshot
from ma_validation import ReleaseStatus
from ma_variants.preprocess import PreprocessVariant

from .models import (
    RunManifest,
    RunManifestV1,
    RunVariantReference,
    SimulationRun,
    SimulationRunStatus,
    SimulationRunV1,
    SimulationSetupSpecification,
)


def build_run_manifest(
    snapshot: BaselineParameterSnapshot,
    variant: PreprocessVariant,
    *,
    run_id: str,
    release: bool = False,
    simulation_setup: SimulationSetupSpecification | None = None,
    output_requirements: tuple[OutputRequirementProfile, ...] | None = None,
) -> RunManifest:
    """Baut ein RunManifest nur aus einem freigegebenen Baseline-Stand."""
    result = validate_baseline_parameter_snapshot(snapshot)
    if result.release_status is not ReleaseStatus.RELEASED:
        raise ValueError("Das Run-Paket benoetigt einen freigegebenen BaselineParameterSnapshot.")
    if variant.baseline_snapshot_id != snapshot.snapshot_id or variant.baseline_content_hash != snapshot.content_hash:
        raise ValueError("Die Variante referenziert nicht die angegebene Baseline.")
    status = SimulationRunStatus.RELEASED_FOR_SIMULATION if release else SimulationRunStatus.DRAFT
    return RunManifest(
        run=SimulationRun(
            run_id=run_id,
            variant_id=variant.variant_id,
            parameter_snapshot_id=snapshot.snapshot_id,
            parameter_snapshot_hash=snapshot.content_hash,
            variant_fingerprint=variant.fingerprint,
            status=status,
        ),
        output_requirements=output_requirements or default_output_requirements(),
        preparation_notes=("Manuelle Uebergabe an IDA ICE; kein Adapter oder Simulationsstart enthalten.",),
        simulation_setup=simulation_setup,
    )


def materialize_run_package(manifest: RunManifest, variant: PreprocessVariant, output_root: str | Path) -> Path:
    """Schreibt das begrenzte P018-Paket ohne bestehende Runs zu ueberschreiben."""
    run_dir = Path(output_root) / manifest.run.run_id
    if run_dir.exists():
        raise FileExistsError(f"Run-Verzeichnis existiert bereits: {run_dir}")
    run_dir.mkdir(parents=True)
    (run_dir / "run_manifest.yaml").write_text(
        yaml.safe_dump(_manifest_payload(manifest), sort_keys=False),
        encoding="utf-8",
    )
    (run_dir / "variant_config.yaml").write_text(yaml.safe_dump(asdict(variant), sort_keys=False), encoding="utf-8")
    (run_dir / "simulation_input.yaml").write_text(
        yaml.safe_dump({"run_id": manifest.run.run_id, "variant_id": manifest.run.variant_id, "status": manifest.run.status.value}, sort_keys=False),
        encoding="utf-8",
    )
    if manifest.simulation_setup is not None:
        (run_dir / "simulation_setup.yaml").write_text(
            yaml.safe_dump(asdict(manifest.simulation_setup), sort_keys=False),
            encoding="utf-8",
        )
    (run_dir / "preparation_report.md").write_text(
        "# Preparation Report\n\nNeutrales Run-Paket fuer die manuelle Simulation.\n",
        encoding="utf-8",
    )
    return run_dir


def build_run_manifest_v1(
    snapshot: BaselineParameterSnapshot,
    variants: tuple[PreprocessVariant, ...],
    *,
    run_id: str,
    selection_id: str,
    selection_fingerprint: str,
    simulation_setup: SimulationSetupSpecification,
    output_requirements: tuple[OutputRequirementProfile, ...],
    release: bool = False,
) -> RunManifestV1:
    """Baut den P018-Zielvertrag ohne Variantenwerte neu zu berechnen."""
    if validate_baseline_parameter_snapshot(snapshot).release_status is not ReleaseStatus.RELEASED:
        raise ValueError("Das Run-Paket benoetigt einen freigegebenen BaselineParameterSnapshot.")
    if not variants:
        raise ValueError("Ein RUN braucht mindestens eine finale Variante.")
    for variant in variants:
        if variant.baseline_snapshot_id != snapshot.snapshot_id or variant.baseline_content_hash != snapshot.content_hash:
            raise ValueError("Eine RUN-Variante referenziert nicht die angegebene Baseline.")
    status = SimulationRunStatus.RELEASED_FOR_SIMULATION if release else SimulationRunStatus.DRAFT
    return RunManifestV1(
        run=SimulationRunV1(
            run_id=run_id,
            selection_id=selection_id,
            selection_fingerprint=selection_fingerprint,
            parameter_snapshot_id=snapshot.snapshot_id,
            parameter_snapshot_hash=snapshot.content_hash,
            variants=tuple(RunVariantReference(item.variant_id, item.content_fingerprint) for item in variants),
            status=status,
        ),
        simulation_setup=simulation_setup,
        output_requirements=output_requirements,
        preparation_notes=("Manuelle Uebergabe; kein IDA-Adapter und kein Simulationsstart enthalten.",),
    )


def materialize_run_package_v1(
    manifest: RunManifestV1, variants: tuple[PreprocessVariant, ...], output_root: str | Path
) -> Path:
    """Materialisiert einen RUN mit gemeinsamem Setup und direktem RUN/VAR-Bezug."""
    if {item.variant_id for item in variants} != {item.variant_id for item in manifest.run.variants}:
        raise ValueError("RUN-Manifest und Variantenmenge stimmen nicht ueberein.")
    run_dir = Path(output_root) / manifest.run.run_id
    if run_dir.exists():
        raise FileExistsError(f"Run-Verzeichnis existiert bereits: {run_dir}")
    variants_dir = run_dir / "variants"
    variants_dir.mkdir(parents=True)
    (run_dir / "run_manifest.yaml").write_text(yaml.safe_dump(_manifest_v1_payload(manifest), sort_keys=False), encoding="utf-8")
    (run_dir / "simulation_setup.yaml").write_text(yaml.safe_dump(asdict(manifest.simulation_setup), sort_keys=False), encoding="utf-8")
    for variant in variants:
        variant_dir = variants_dir / variant.variant_id
        variant_dir.mkdir()
        (variant_dir / "variant_config.yaml").write_text(yaml.safe_dump(asdict(variant), sort_keys=False), encoding="utf-8")
        (variant_dir / "simulation_input.yaml").write_text(
            yaml.safe_dump({"run_id": manifest.run.run_id, "variant_id": variant.variant_id, "status": manifest.run.status.value}, sort_keys=False), encoding="utf-8"
        )
    return run_dir


def _manifest_payload(manifest: RunManifest) -> dict[str, object]:
    payload: dict[str, object] = {
        "run": {
            "run_id": manifest.run.run_id,
            "variant_id": manifest.run.variant_id,
            "parameter_snapshot_id": manifest.run.parameter_snapshot_id,
            "parameter_snapshot_hash": manifest.run.parameter_snapshot_hash,
            "variant_fingerprint": manifest.run.variant_fingerprint,
            "status": manifest.run.status.value,
        },
        "output_requirements": [asdict(requirement) for requirement in manifest.output_requirements],
        "preparation_notes": list(manifest.preparation_notes),
    }
    if manifest.simulation_setup is not None:
        payload["simulation_setup"] = asdict(manifest.simulation_setup)
    return payload


def _manifest_v1_payload(manifest: RunManifestV1) -> dict[str, object]:
    return {
        "run": {**asdict(manifest.run), "status": manifest.run.status.value},
        "output_requirements": [asdict(requirement) for requirement in manifest.output_requirements],
        "preparation_notes": list(manifest.preparation_notes),
    }
