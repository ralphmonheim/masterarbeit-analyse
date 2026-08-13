from pathlib import Path

import pytest
from openpyxl import Workbook

from ma_import_simulation.adapters.ida_ice import (
    RawIdaResult,
    StandardizedIdaResult,
    detect_ida_artifact,
    inspect_ida_package,
    parse_html_report,
    parse_prn_file,
    read_excel_metadata,
    sha256_file,
)


def test_hash_is_reproducible(tmp_path: Path):
    source = tmp_path / "zone.prn"
    source.write_text("# time load\n0 1\n", encoding="utf-8")
    assert sha256_file(source) == sha256_file(source)


def test_prn_parser_reads_header_and_variable_time(tmp_path: Path):
    source = tmp_path / "zone.prn"
    source.write_text("# time heating\n0.25 -12.5\n1.75 5\n", encoding="utf-8")
    assert parse_prn_file(source) == (("time", "heating"), ((0.25, -12.5), (1.75, 5.0)))


def test_prn_parser_does_not_silently_drop_malformed_rows(tmp_path: Path):
    source = tmp_path / "malformed.prn"
    source.write_text("# time heating\n0 1\n1 invalid\n", encoding="utf-8")

    with pytest.raises(ValueError, match="nichtnumerische"):
        parse_prn_file(source)


def test_html_report_parser_extracts_existing_meta_and_tables(tmp_path: Path):
    source = tmp_path / "report.html"
    source.write_text('<meta name="run" content="R-1"><table><tr><th>A</th></tr><tr><td>2</td></tr></table>', encoding="utf-8")
    metadata, tables = parse_html_report(source)
    assert metadata == {"run": "R-1"}
    assert tables == ((("A",), ("2",)),)


def test_html_report_parser_supports_ida_cells_without_end_tags(tmp_path: Path):
    source = tmp_path / "report.html"
    source.write_text(
        "<html><body><table><tr><th>Zone<th>Value<tr><td>A<td>1</table></body></html>",
        encoding="utf-8",
    )

    _, tables = parse_html_report(source)

    assert tables == ((("Zone", "Value"), ("A", "1")),)


def test_excel_metadata_uses_only_the_selected_file(tmp_path: Path):
    source = tmp_path / "selected.xlsx"
    workbook = Workbook()
    workbook.properties.title = "IDA report"
    workbook.save(source)
    metadata = read_excel_metadata(source)
    assert metadata["title"] == "IDA report"
    assert metadata["sheet_names"] == ("Sheet",)


def test_protected_and_unsupported_sources_are_diagnosed(tmp_path: Path):
    protected = tmp_path / "model.idm"
    protected.write_text("do not read", encoding="utf-8")
    unsupported = tmp_path / "notes.txt"
    unsupported.write_text("x", encoding="utf-8")
    assert detect_ida_artifact(protected)[1][0].code == "protected_source"
    assert detect_ida_artifact(unsupported)[1][0].code == "unsupported_artifact"


def test_package_is_manifest_scoped_and_keeps_cohorts_separate(tmp_path: Path):
    root = tmp_path / "five-zone"
    root.mkdir()
    (root / "result.prn").write_text("# time x\n0 1", encoding="utf-8")
    (root / "ida_result_manifest.json").write_text('{"cohort":"5Z","artifacts":["result.prn"]}', encoding="utf-8")
    package = inspect_ida_package(root)
    assert package.cohort == "5Z" and [item.path.name for item in package.artifacts] == ["result.prn"]

    other = tmp_path / "other"
    other.mkdir()
    (other / "ida_result_manifest.json").write_text('{"cohort":"29Z","artifacts":[]}', encoding="utf-8")
    with pytest.raises(ValueError, match="mindestens"):
        inspect_ida_package(other)


def test_package_rejects_ambiguous_or_external_manifest_entries(tmp_path: Path):
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside.prn"
    outside.write_text("# time x\n0 1", encoding="utf-8")
    (root / "ida_result_manifest.json").write_text('{"cohort":"ALT","artifacts":["../outside.prn"]}', encoding="utf-8")
    with pytest.raises(ValueError, match="keine erlaubten"):
        inspect_ida_package(root)


def test_raw_result_can_be_standardized_without_calculation():
    raw = RawIdaResult("1.0", "run", "variant", "model", "zone", "zone", "load", "W", "positive", 0.5, 12.0, "PRN", "a" * 64, "accepted")
    assert StandardizedIdaResult.from_raw(raw).value == 12.0
