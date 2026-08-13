from openpyxl import Workbook

from ma_data_preparation.zone_metadata import read_zone_metadata


def test_zone_metadata_combines_three_explicit_sections(tmp_path):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Zonen"])
    sheet.append(["Name", "Gruppe", "Bodenfläche, m2"])
    sheet.append(["EG Ost", "Office", 67.96])
    sheet.append([])
    sheet.append(["Zonen - total"])
    sheet.append(["Name", "Gruppe", "Zonenmultiplikator"])
    sheet.append(["EG Ost", "Office", 1])
    sheet.append([])
    sheet.append(["Zonen Sollwerte"])
    sheet.append(["Name", "Gruppe", "Max VVS Abluft, L/(s m2)", "Max VVS Zuluft, L/(s m2)"])
    sheet.append(["EG Ost", "Office", 3.0, 4.0])
    target = tmp_path / "zones.xlsx"
    workbook.save(target)

    zones = read_zone_metadata(target)

    assert len(zones) == 1
    assert zones[0].zone == "EG Ost"
    assert zones[0].area_m2 == 67.96
    assert zones[0].multiplier == 1.0
    assert zones[0].max_exhaust_airflow_l_s_m2 == 3.0
    assert zones[0].max_supply_airflow_l_s_m2 == 4.0
