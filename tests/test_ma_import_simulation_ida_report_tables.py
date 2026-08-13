from ma_import_simulation.adapters.ida_ice import extract_zone_report_rows


def test_zone_report_rows_are_found_and_nil_stays_missing(tmp_path):
    report = tmp_path / "heating.html"
    report.write_text(
        "<table><tr><th>Zone<th>Gruppe<th>Fläche, m2<th>Wärmeabgabe*, W"
        "<tr><td>EG Ost<td>Office<td>67,96<td>5436"
        "<tr><td>Lobby<td>Lobby<td>65.4<td>NIL</table>",
        encoding="utf-8",
    )

    rows = extract_zone_report_rows(report)

    assert rows[0]["zone"] == "EG Ost"
    assert rows[0]["flache_m2"] == 67.96
    assert rows[0]["warmeabgabe_w"] == 5436.0
    assert rows[1]["warmeabgabe_w"] is None
