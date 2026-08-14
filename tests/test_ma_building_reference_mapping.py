
from ma_building.reference_mapping import build_small_office_5z_b1_mapping, enrich_b2_from_viewer_and_ifc


def test_b1_keeps_direct_5z_totals_and_marks_inconsistent_idm_detail(tmp_path):
    idm = tmp_path / "cooling.idm"
    idm.write_text(
        '((REPORT-OBJECT :N "Lobby" :T ZONE-INDATA-REPORT) '
        '(:PAR :N SURFACES-DATA :V (SURFS ((NAME "wall n" TYPE "Wand außen" AREA 40 AZIM 0)))) '
        '((REPORT-OBJECT :N "EG West" :T ZONE-INDATA-REPORT)',
        encoding="utf-8",
    )

    mapping = build_small_office_5z_b1_mapping(idm_path=idm)

    assert mapping.totals[0].window_area_m2 == 72.22
    assert mapping.totals[-1].uppermost_ceiling_area_m2 == 67.964
    assert mapping.conflicts
    assert mapping.details[0].mapping_status == "detail_only"


def test_b2_never_guesses_a_link_without_an_explicit_global_id(tmp_path):
    viewer = tmp_path / "viewer.xlsx"
    # A missing/non-readable viewer export is a permitted unresolved B2 case.
    ifc = tmp_path / "model.ifc"
    ifc.write_text("ISO-10303-21;DATA;#1=IFCWALL('gid',$,$,$,$,$,$,$);ENDSEC;END-ISO-10303-21;", encoding="utf-8")

    mapping = build_small_office_5z_b1_mapping()
    enriched = enrich_b2_from_viewer_and_ifc(mapping, viewer_excel_path=viewer, ifc_path=ifc)

    assert enriched.totals == mapping.totals
    assert len(enriched.sources) == 2
