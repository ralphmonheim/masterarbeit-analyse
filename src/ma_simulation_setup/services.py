"""Erstellung und Materialisierung neutraler P018-Run-Pakete."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import yaml

from ma_analyse.stage_1_dimensioning import default_output_requirements
from ma_parameters import BaselineParameterSnapshot, validate_baseline_parameter_snapshot
from ma_validation import ReleaseStatus
from ma_variants.preprocess import PreprocessVariant

from .models import RunManifest, SimulationRun, SimulationRunStatus


def build_run_manifest(
    snapshot: BaselineParameterSnapshot,
    variant: PreprocessVariant,
    *,
    run_id: str,
    release: bool = False,
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
        output_requirements=default_output_requirements(),
        preparation_notes=("Manuelle Uebergabe an IDA ICE; kein Adapter oder Simulationsstart enthalten.",),
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
    (run_dir / "preparation_report.md").write_text(
        "# Preparation Report\n\nNeutrales Run-Paket fuer die manuelle Simulation.\n",
        encoding="utf-8",
    )
    return run_dir


def _manifest_payload(manifest: RunManifest) -> dict[str, object]:
    return {
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
