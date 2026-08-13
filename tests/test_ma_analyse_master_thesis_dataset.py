from openpyxl import Workbook

from ma_analyse.analysis.master_thesis_dataset import build_model_zone_tables


def test_model_zone_table_combines_metadata_and_prn_metrics(tmp_path):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Zonen"])
    sheet.append(["Name", "Gruppe", "Bodenfläche, m2"])
    sheet.append(["EG Ost", "Office", 10.0])
    sheet.append([])
    sheet.append(["Zonen - total"])
    sheet.append(["Name", "Zonenmultiplikator"])
    sheet.append(["EG Ost", 1])
    sheet.append([])
    sheet.append(["Zonen Sollwerte"])
    sheet.append(["Name", "Max VVS Abluft, L/(s m2)", "Max VVS Zuluft, L/(s m2)"])
    sheet.append(["EG Ost", 2.0, 3.0])
    workbook.save(tmp_path / "Dimensionierung_5Z_Eingabe_Allgemein.xlsx")

    energy = tmp_path / "Masterthesis_Dimensionierung_5Z" / "energy"
    energy.mkdir(parents=True)
    (energy / "EG Ost.TEMPERATURES.prn").write_text(
        "# time order tairmean top\n0 1 20 20.5\n1 1 22 22.5\n2 1 21 21.5\n",
        encoding="utf-8",
    )
    (energy / "EG Ost.IAQ.prn").write_text(
        "# time order air_age relhum xco2vol\n0 1 1 0.4 500\n1 1 2 0.6 900\n2 1 1 0.5 600\n",
        encoding="utf-8",
    )
    (energy / "EG Ost.ZONE-ENERGY.prn").write_text(
        "# time order q_heat q_cool\n0 1 1000 0\n1 1 1000 -500\n2 1 0 0\n",
        encoding="utf-8",
    )

    result = build_model_zone_tables(tmp_path, "5Z")

    row = result.zone_table.iloc[0]
    assert row["Max. Lufttemperatur [°C]"] == 22.0
    assert row["Max. CO₂ [ppm]"] == 900.0
    assert row["Raumheizung [kWh]"] == 1.5
    assert row["Raumkühlung [kWh]"] == 0.5
    assert row["Datenabdeckung [%]"] == 60.0
    assert row["Auswertungsstatus"] == "PARTIAL"
