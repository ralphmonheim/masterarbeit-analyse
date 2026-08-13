from pathlib import Path

import pytest

from ma_analyse.stage_2_optimization.historical import build_historical_optimization_table


def _write_zone_energy(path: Path, heat: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# time q_heat q_cool\n0 {heat} -10\n1 {heat} -20\n", encoding="utf-8")


def test_historical_table_compares_variant_to_dimensionierung(tmp_path: Path) -> None:
    _write_zone_energy(tmp_path / "ALT" / "Dimensionierung" / "Zone A" / "ZONE-ENERGY.prn", 100)
    _write_zone_energy(tmp_path / "ALT" / "Variante" / "Zone A" / "ZONE-ENERGY.prn", 80)

    table = build_historical_optimization_table(tmp_path)

    variant = table[table["Variante"] == "Variante"].iloc[0]
    assert variant["Heizenergie [kWh]"] == 0.08
    assert variant["Delta zu Basis: Heizenergie [kWh]"] == pytest.approx(-0.02)
    assert variant["Auswertungsstatus"] == "PARTIAL"
