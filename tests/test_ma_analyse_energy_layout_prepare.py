import pandas as pd

from ma_analyse.preprocessing.prepare import prepare_energy_layout_variant_data
from ma_analyse.services import list_database_variant_names


def _write_prn(path, header, rows):
    path.write_text(
        f"# {header}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n",
        encoding="utf-8",
    )


def test_prepare_energy_layout_creates_legacy_compatible_room_csv(tmp_path):
    variant_dir = tmp_path / "new_variant"
    energy_dir = variant_dir / "energy"
    energy_dir.mkdir(parents=True)
    room_name = "201 Office"
    _write_prn(energy_dir / f"{room_name}.HEAT_BALANCE.prn", "time order qloss", [(0, 1, 10), (1, 1, 20)])
    _write_prn(energy_dir / f"{room_name}.IAQ.prn", "time order relhum", [(0, 1, 0.4), (1, 1, 0.5)])
    _write_prn(energy_dir / f"{room_name}.LOCAL-DE-COMF-DIAG-T.prn", "time order top", [(0, 1, 20), (1, 1, 21)])
    _write_prn(energy_dir / f"{room_name}.TEMPERATURES.prn", "time order tairmean top", [(0, 1, 20, 20), (1, 1, 21, 21)])
    _write_prn(energy_dir / f"{room_name}.ZONE-ENERGY.prn", "time order q_heat", [(0, 1, 100), (1, 1, 200)])

    result = prepare_energy_layout_variant_data(variant_dir, rooms=None, datenbank_dir=tmp_path / "database")

    assert result == {"variant_name": "new_variant", "processed_rooms": 1, "rows": 2}
    csv_file = tmp_path / "database" / "new_variant_nutzdaten" / "201_Office.csv"
    prepared = pd.read_csv(csv_file)
    assert prepared["room"].tolist() == [room_name, room_name]
    assert prepared["iaq_relhum"].tolist() == [40.0, 50.0]
    assert prepared["temperatures_top"].tolist() == [20, 21]
    assert prepared["zone_energy_q_heat"].tolist() == [100, 200]
    assert list_database_variant_names(tmp_path / "database") == ["new_variant"]
