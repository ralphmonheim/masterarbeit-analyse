from ma_building import (
    MASTER_THESIS_REFERENCE_IFC_FILENAME,
    MASTER_THESIS_REFERENCE_IFC_PATH,
    diagnose_building_source,
    scan_building_input_directory,
)
from ma_validation import DiagnosticSeverity


def test_scan_building_input_directory_filters_ifc_and_3dm(tmp_path):
    ifc_file = tmp_path / "model.ifc"
    rhino_file = tmp_path / "model.3dm"
    ignored_file = tmp_path / "notes.txt"
    ifc_file.write_text("IFC", encoding="utf-8")
    rhino_file.write_bytes(b"3dm")
    ignored_file.write_text("ignore", encoding="utf-8")

    paths = scan_building_input_directory(tmp_path)

    assert set(paths) == {ifc_file, rhino_file}
    assert ignored_file not in paths


def test_diagnose_ifc_file_counts_core_entities(tmp_path):
    ifc_file = tmp_path / "demo.ifc"
    ifc_file.write_text(
        "\n".join(
            [
                "ISO-10303-21;",
                "HEADER;",
                "FILE_SCHEMA(('IFC4'));",
                "ENDSEC;",
                "DATA;",
                "#1=IFCBUILDING('b');",
                "#2=IFCBUILDINGSTOREY('s');",
                "#3=IFCSPACE('r');",
                "#4=IFCWALLSTANDARDCASE('w');",
                "#5=IFCWINDOW('f');",
                "#6=IFCDOOR('d');",
                "ENDSEC;",
                "END-ISO-10303-21;",
            ]
        ),
        encoding="utf-8",
    )

    diagnostic = diagnose_building_source(ifc_file)

    assert diagnostic.source.data_format == "IFC"
    assert diagnostic.source.file_size_bytes is not None
    assert len(diagnostic.source.sha256 or "") == 64
    assert diagnostic.ifc_schema == "IFC4"
    assert diagnostic.entity_counts["IFCSPACE"] == 1
    assert diagnostic.entity_counts["IFCWALL"] == 1
    assert {message.severity for message in diagnostic.messages} == {DiagnosticSeverity.INFO}


def test_diagnose_3dm_file_records_parser_warning(tmp_path):
    rhino_file = tmp_path / "demo.3dm"
    rhino_file.write_bytes(b"rhino placeholder")

    diagnostic = diagnose_building_source(rhino_file)

    assert diagnostic.source.data_format == "3DM"
    assert diagnostic.messages[0].severity is DiagnosticSeverity.WARNING
    assert diagnostic.messages[0].code == "BUILDING_3DM_PARSER_NOT_ENABLED"


def test_diagnose_dwg_file_records_parser_warning(tmp_path):
    dwg_file = tmp_path / "demo.dwg"
    dwg_file.write_bytes(b"AC1018 placeholder")

    diagnostic = diagnose_building_source(dwg_file)

    assert diagnostic.source.data_format == "DWG"
    assert diagnostic.messages[0].severity is DiagnosticSeverity.WARNING
    assert diagnostic.messages[0].code == "BUILDING_DWG_PARSER_NOT_ENABLED"


def test_missing_building_source_returns_error_diagnostic(tmp_path):
    diagnostic = diagnose_building_source(tmp_path / "missing.ifc")

    assert diagnostic.messages[0].severity is DiagnosticSeverity.ERROR
    assert diagnostic.messages[0].code == "BUILDING_SOURCE_NOT_FOUND"


def test_master_thesis_reference_ifc_points_to_smalloffice_sample():
    assert MASTER_THESIS_REFERENCE_IFC_FILENAME == "SmallOffice_d_IFC2x3.ifc"
    assert MASTER_THESIS_REFERENCE_IFC_PATH.name == MASTER_THESIS_REFERENCE_IFC_FILENAME
