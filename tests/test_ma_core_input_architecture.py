import json
from datetime import timezone

import pytest

from ma_core import (
    InputChange,
    InputSourceKind,
    SessionLogEvent,
    append_session_event,
    build_input_source,
    create_run_id,
    create_session_id,
)


def test_input_source_collects_file_metadata_and_checksum(tmp_path):
    source_file = tmp_path / "weather.dat"
    source_file.write_text("TRY data", encoding="utf-8")

    source = build_input_source(
        module_key="ma_weather",
        source_kind=InputSourceKind.IMPORT,
        data_format="TRY",
        source_path=source_file,
        adapter_key="ma_weather.try_importer",
    )

    assert source.source_id.startswith("source_")
    assert source.source_kind is InputSourceKind.IMPORT
    assert source.source_path == source_file
    assert source.file_size_bytes == len("TRY data")
    assert len(source.sha256 or "") == 64
    assert source.loaded_at.tzinfo is timezone.utc


def test_input_change_has_unique_id_and_utc_timestamp():
    first = InputChange("weather.location", "A", "B", "Standort korrigiert")
    second = InputChange("weather.location", "B", "C", "Standort erneut korrigiert")

    assert first.change_id.startswith("change_")
    assert first.change_id != second.change_id
    assert first.changed_at.tzinfo is timezone.utc


def test_session_and_run_ids_are_unique():
    first_session = create_session_id()
    second_session = create_session_id()
    first_run = create_run_id("weather")
    second_run = create_run_id("weather")

    assert first_session.startswith("session_")
    assert first_session != second_session
    assert first_run.startswith("weather_")
    assert first_run != second_run


def test_session_log_is_append_only_jsonl(tmp_path):
    session_id = create_session_id()
    first = SessionLogEvent(
        session_id=session_id,
        run_id=create_run_id("weather"),
        event_type="run_started",
        module_key="ma_weather",
        message="Start",
    )
    second = SessionLogEvent(
        session_id=session_id,
        run_id=first.run_id,
        event_type="diagnostic_recorded",
        module_key="ma_weather",
        severity="warning",
        diagnostic_code="WEATHER_TEST_WARNING",
        message="Testwarnung",
        related_id="diagnostic_test",
    )

    log_path = append_session_event(first, log_dir=tmp_path)
    append_session_event(second, log_dir=tmp_path)
    rows = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]

    assert [row["event_type"] for row in rows] == ["run_started", "diagnostic_recorded"]
    assert rows[1]["diagnostic_code"] == "WEATHER_TEST_WARNING"
    assert rows[1]["related_id"] == "diagnostic_test"
    assert rows[0]["event_id"] != rows[1]["event_id"]


def test_session_log_rejects_unsafe_session_id(tmp_path):
    event = SessionLogEvent(
        session_id="../outside",
        event_type="run_started",
        module_key="ma_weather",
    )

    with pytest.raises(ValueError, match="unzulaessige Zeichen"):
        append_session_event(event, log_dir=tmp_path)
