import json

import pandas as pd

from ma_variants.simulation_results import (
    collect_simulation_metrics,
    discover_result_folders,
    export_simulation_metrics_to_json,
    map_result_folders_to_variants,
    read_room_metrics,
)
from ma_variants.variant_manager import Variant

FIXED_EXPORTED_AT = "2026-06-03T15:00:00+00:00"


def _write_room_csv(result_dir, room_name, rows):
    result_dir.mkdir(parents=True, exist_ok=True)
    csv_path = result_dir / f"{room_name.replace(' ', '_')}.csv"
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    return csv_path


def _example_rows():
    return [
        {
            "time": 0,
            "zone_energy_q_heat": 1000,
            "zone_energy_q_cool": 0,
            "temperatures_top": 21,
            "iaq_relhum": 50,
            "iaq_xco2vol": 600,
            "local_de_comf_diag_t_ppd": 6,
            "local_de_comf_diag_t_pmv": 0.1,
        },
        {
            "time": 1,
            "zone_energy_q_heat": 500,
            "zone_energy_q_cool": -300,
            "temperatures_top": 26,
            "iaq_relhum": 45,
            "iaq_xco2vol": 900,
            "local_de_comf_diag_t_ppd": 8,
            "local_de_comf_diag_t_pmv": 0.3,
        },
        {
            "time": 2,
            "zone_energy_q_heat": 0,
            "zone_energy_q_cool": -700,
            "temperatures_top": 28,
            "iaq_relhum": 35,
            "iaq_xco2vol": 1100,
            "local_de_comf_diag_t_ppd": 12,
            "local_de_comf_diag_t_pmv": 0.6,
        },
    ]


def test_discover_and_map_result_folders_to_variants(tmp_path):
    root = tmp_path / "database"
    (root / "Variant_A_nutzdaten").mkdir(parents=True)
    (root / "ignore_me").mkdir()
    variants = [
        Variant(variant_key="Variant_A", variant_name="Variante A", status="simulated"),
        Variant(variant_key="Variant_B", variant_name="Variante B", status="missing"),
    ]

    folders = discover_result_folders(root)
    mappings = map_result_folders_to_variants(variants, results_root=root)

    assert [folder.result_key for folder in folders] == ["Variant_A"]
    assert mappings[0].is_mapped is True
    assert mappings[0].result_dir == root / "Variant_A_nutzdaten"
    assert mappings[1].is_mapped is False
    assert "Kein passender Ergebnisordner" in mappings[1].notes[0]


def test_read_room_metrics_from_small_csv(tmp_path):
    csv_path = _write_room_csv(tmp_path, "101 lobby", _example_rows())

    result = read_room_metrics(csv_path, variant_key="Variant_A", variant_name="Variante A")

    assert result.room_name == "101 lobby"
    assert result.metrics["heating_energy_kwh"] == 1.5
    assert result.metrics["cooling_energy_kwh"] == 1.0
    assert result.metrics["max_heating_power_w"] == 1000
    assert result.metrics["max_cooling_power_w"] == 700
    assert result.metrics["overtemperature_hours_25"] == 2
    assert result.metrics["overtemperature_hours_27"] == 1
    assert result.metrics["max_co2_ppm"] == 1100
    assert result.metrics["mean_co2_ppm"] == 866.6666666666666
    assert result.metrics["max_ppd_percent"] == 12
    assert result.metrics["max_pmv"] == 0.6
    assert result.missing_columns == {}


def test_collect_simulation_metrics_aggregates_rooms(tmp_path):
    root = tmp_path / "database"
    result_dir = root / "Variant_A_nutzdaten"
    _write_room_csv(result_dir, "101 lobby", _example_rows())
    _write_room_csv(
        result_dir,
        "109 office",
        [
            {
                "time": 0,
                "zone_energy_q_heat": 200,
                "zone_energy_q_cool": -100,
                "temperatures_top": 24,
                "iaq_relhum": 50,
                "iaq_xco2vol": 700,
            }
        ],
    )
    variant = Variant(variant_key="Variant_A", variant_name="Variante A", status="simulated")
    mappings = map_result_folders_to_variants([variant], results_root=root)

    results = collect_simulation_metrics(mappings)

    assert len(results) == 1
    assert [room.room_name for room in results[0].room_metrics] == ["101 lobby", "109 office"]
    assert results[0].summary_metrics["heating_energy_kwh"] == 1.7
    assert results[0].summary_metrics["cooling_energy_kwh"] == 1.1
    assert results[0].summary_metrics["max_heating_power_w"] == 1000
    assert results[0].summary_metrics["max_cooling_power_w"] == 700


def test_export_simulation_metrics_to_json(tmp_path):
    root = tmp_path / "database"
    result_dir = root / "Variant_A_nutzdaten"
    _write_room_csv(result_dir, "101 lobby", _example_rows())
    variant = Variant(variant_key="Variant_A", variant_name="Variante A", status="simulated")
    mappings = map_result_folders_to_variants([variant], results_root=root)
    metric_results = collect_simulation_metrics(mappings)

    output_path = export_simulation_metrics_to_json(
        metric_results,
        tmp_path / "simulation_metrics.json",
        exported_at=FIXED_EXPORTED_AT,
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["exported_at"] == FIXED_EXPORTED_AT
    assert payload["variant_count"] == 1
    assert payload["variants"][0]["variant_key"] == "Variant_A"
    assert payload["variants"][0]["room_metrics"][0]["source_file"].endswith("101_lobby.csv")
