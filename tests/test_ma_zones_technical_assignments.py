from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from ma_building import (
    BuildingInfo,
    BuildingInputDetailLevel,
    BuildingMaturityLevel,
    BuildingModelSpecification,
    BuildingModelVersion,
    PhysicalElement,
    ProjectInfo,
    Space,
    Storey,
)
from ma_technical import (
    ObjectReference,
    ReleasedTechnicalHandover,
    build_released_technical_handover,
    load_technical_model_specification,
    release_technical_model,
)
from ma_technical.handover import _service_interface_references_hash
from ma_ui.streamlit_app.module_views import zones_view
from ma_ui.streamlit_app.module_views.zones_assignment_support import (
    bind_zone_specification_to_project,
    stored_technical_assignment_draft,
    technical_assignment_check_token,
    technical_assignment_editor_rows,
    technical_assignment_project_payload,
    technical_assignments_from_rows,
    technical_handover_reference,
    technical_handover_rows,
    validate_technical_assignment_draft,
    zone_specification_content_hash,
    zone_specification_reference,
)
from ma_validation import ReleaseStatus
from ma_zones import (
    ThermalBuildingModel,
    ThermalZone,
    UsageProfile,
    ZoneInputDetailLevel,
    ZoneModelSpecification,
    ZoneTechnicalServiceAssignment,
    build_released_zone_handover,
    validate_zone_spec,
    validate_zone_technical_assignments,
    zone_specification_from_dict,
    zone_specification_to_dict,
)

REFERENCE_SPEC_PATH = (
    Path(__file__).resolve().parents[1]
    / "config"
    / "ma_technical"
    / "examples"
    / "technical_v2_reference_spec.yaml"
)


def _codes(result):
    return {message.code for message in result.messages}


def _assignments() -> tuple[ZoneTechnicalServiceAssignment, ...]:
    return (
        ZoneTechnicalServiceAssignment(
            assignment_id="ZONE-TECH-ASSIGNMENT-0001",
            zone_id="ZONE-0001",
            service_interface_id="SYNTHETIC-SERVICE-HEATING-0001",
            terminal_type="synthetic_terminal",
            assignment_origin="manual_confirmed",
        ),
        ZoneTechnicalServiceAssignment(
            assignment_id="ZONE-TECH-ASSIGNMENT-0002",
            zone_id="ZONE-0002",
            service_interface_id="SYNTHETIC-SERVICE-HEATING-0001",
            terminal_type="synthetic_terminal",
            assignment_origin="manual_confirmed",
        ),
    )


def _zone_spec() -> ZoneModelSpecification:
    return ZoneModelSpecification(
        schema_version="1.0",
        zone_model_id="SYNTHETIC-ZONE-MODEL-0001",
        project_id="SYNTHETIC-PROJECT-0001",
        building_id="SYNTHETIC-BUILDING-0001",
        source_building_version_id="SYNTHETIC-BUILDING-REV-0001",
        input_detail_level=ZoneInputDetailLevel.LOD_2,
        zones=(
            ThermalZone(
                zone_id="ZONE-0001",
                name="Synthetische Zone 1",
                usage_profile_id="PROFILE-0001",
                floor_area_m2=50.0,
                volume_m3=150.0,
                source_space_ids=("SPACE-0001",),
            ),
            ThermalZone(
                zone_id="ZONE-0002",
                name="Synthetische Zone 2",
                usage_profile_id="PROFILE-0001",
                floor_area_m2=50.0,
                volume_m3=150.0,
                source_space_ids=("SPACE-0002",),
            ),
        ),
        usage_profiles=(UsageProfile("PROFILE-0001", "Buero", 8.0, 18.0, 5, 20.0, 8.0, 10.0),),
        technical_assignments=_assignments(),
    )


def _building_spec() -> BuildingModelSpecification:
    return BuildingModelSpecification(
        schema_version="1.0",
        project=ProjectInfo(project_id="SYNTHETIC-PROJECT-0001", name="Synthetisches Testprojekt"),
        building=BuildingInfo(
            building_id="SYNTHETIC-BUILDING-0001",
            name="Synthetisches Testgebaeude",
            unit="m",
            north_angle_deg=0.0,
            length_m=10.0,
            width_m=10.0,
            height_m=3.0,
        ),
        model_version=BuildingModelVersion(
            version_id="SYNTHETIC-BUILDING-REV-0001",
            source_input_level=BuildingMaturityLevel.BIL_1,
            detected_input_level=BuildingMaturityLevel.BIL_1,
            confirmed_input_level=BuildingMaturityLevel.BIL_1,
            current_maturity_level=BuildingMaturityLevel.BIL_1,
            target_maturity_level=BuildingMaturityLevel.BIL_1,
        ),
        storeys=(Storey("STOREY-0001", "EG", 0.0, 3.0),),
        spaces=(
            Space("SPACE-0001", "Raum 1", "STOREY-0001", 50.0, 150.0),
            Space("SPACE-0002", "Raum 2", "STOREY-0001", 50.0, 150.0),
        ),
        elements=(PhysicalElement("ELEMENT-0001", "wall", "AW", "STOREY-0001", 30.0),),
        input_detail_level=BuildingInputDetailLevel.LOD_2,
    )


def _technical_handover(tmp_path: Path) -> ReleasedTechnicalHandover:
    revision = release_technical_model(
        load_technical_model_specification(REFERENCE_SPEC_PATH),
        revision_id="SYNTHETIC-TECHNICAL-REV-0001",
        target_dir=tmp_path,
    )
    return build_released_technical_handover(revision)


def _thermal_building_model(technical_handover: ReleasedTechnicalHandover) -> ThermalBuildingModel:
    return ThermalBuildingModel(
        thermal_building_model_id="SYNTHETIC-THERMAL-BUILDING-0001",
        project_id="SYNTHETIC-PROJECT-0001",
        building_id="SYNTHETIC-BUILDING-0001",
        building_revision_id="SYNTHETIC-BUILDING-REV-0001",
        zone_model_id="SYNTHETIC-ZONE-MODEL-0001",
        technical_model_id=technical_handover.technical_model_id,
        technical_revision_id=technical_handover.revision_id,
        technical_content_hash=technical_handover.content_hash,
        room_zone_assignments=(
            ("SPACE-0001", "ZONE-0001"),
            ("SPACE-0002", "ZONE-0002"),
        ),
    )


def _released_zone_handover(
    tmp_path: Path,
    *,
    zone_spec: ZoneModelSpecification | None = None,
    technical_handover: ReleasedTechnicalHandover | None = None,
):
    selected_handover = technical_handover or _technical_handover(tmp_path)
    return build_released_zone_handover(
        _building_spec(),
        zone_spec or _zone_spec(),
        _thermal_building_model(selected_handover),
        selected_handover,
    )


def test_zone_technical_assignments_are_immutable_and_roundtrip():
    spec = _zone_spec()

    payload = zone_specification_to_dict(spec)

    assert zone_specification_from_dict(payload) == spec
    assert payload["technical_assignments"][0]["assignment_origin"] == "manual_confirmed"
    with pytest.raises(FrozenInstanceError):
        spec.technical_assignments[0].terminal_type = "changed"


def test_direct_ui_binds_only_project_context_and_requires_exact_building():
    spec = replace(_zone_spec(), project_id="SOURCE-PROJECT")
    building_reference = ObjectReference(
        object_id=spec.building_id,
        revision_id=spec.source_building_version_id,
        object_type="BuildingModelSpecification",
    )

    bound = bind_zone_specification_to_project(
        spec,
        project_id="WORKSPACE-PROJECT",
        building_reference=building_reference,
    )

    assert bound.project_id == "WORKSPACE-PROJECT"
    assert bound.building_id == spec.building_id
    assert bound.source_building_version_id == spec.source_building_version_id
    assert spec.project_id == "SOURCE-PROJECT"
    with pytest.raises(ValueError, match="Building-IDs"):
        bind_zone_specification_to_project(
            spec,
            project_id="WORKSPACE-PROJECT",
            building_reference=replace(building_reference, object_id="OTHER-BUILDING"),
        )


def test_direct_ui_rows_do_not_preselect_and_require_manual_confirmation(tmp_path):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())
    rows = technical_assignment_editor_rows(spec, handover)

    assert rows
    assert all(not row["Zuordnen"] for row in rows)
    assert all(not row["Manuell bestaetigt"] for row in rows)

    rows[0]["Zuordnen"] = True
    unconfirmed = technical_assignments_from_rows(spec, handover, rows)
    _draft, validation = validate_technical_assignment_draft(spec, handover, unconfirmed)
    assert validation.release_status is ReleaseStatus.BLOCKED
    assert "ZONE_TECHNICAL_ASSIGNMENT_FIELD_MISSING" in _codes(validation)

    rows[0]["Manuell bestaetigt"] = True
    confirmed = technical_assignments_from_rows(spec, handover, rows)
    _draft, validation = validate_technical_assignment_draft(spec, handover, confirmed)
    assert validation.release_status is ReleaseStatus.RELEASED
    assert confirmed[0].assignment_origin == "manual_confirmed"


def test_direct_ui_payload_is_additive_and_bound_to_exact_handover(tmp_path):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())
    rows = technical_assignment_editor_rows(spec, handover)
    rows[0]["Zuordnen"] = True
    rows[0]["Manuell bestaetigt"] = True
    assignments = technical_assignments_from_rows(spec, handover, rows)
    original = {
        "schema_version": "1.0",
        "project_id": spec.project_id,
        "model_drafts": {"5Z": {"profile_assignments": {"ZONE-0001": "PROFILE-0001"}}},
    }

    updated = technical_assignment_project_payload(
        original,
        project_id=spec.project_id,
        model_key="5Z",
        zone_spec=spec,
        handover=handover,
        assignments=assignments,
    )
    draft = updated["model_drafts"]["5Z"]

    assert original["model_drafts"]["5Z"] == {
        "profile_assignments": {"ZONE-0001": "PROFILE-0001"}
    }
    assert draft["profile_assignments"] == {"ZONE-0001": "PROFILE-0001"}
    assert draft["technical_assignments"][0]["assignment_origin"] == "manual_confirmed"
    assert draft["technical_handover_reference"] == technical_handover_reference(handover)
    assert draft["zone_specification_reference"] == zone_specification_reference(spec)
    assert draft["zone_handover_status"] == "not_created"

    reloaded = stored_technical_assignment_draft(
        updated,
        model_key="5Z",
        zone_spec=spec,
        handover=handover,
    )
    assert reloaded.matches_active_handover
    assert reloaded.assignments == assignments


def test_direct_ui_does_not_prefill_stale_handover_draft(tmp_path):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())
    rows = technical_assignment_editor_rows(spec, handover)
    rows[0]["Zuordnen"] = True
    rows[0]["Manuell bestaetigt"] = True
    assignments = technical_assignments_from_rows(spec, handover, rows)
    payload = technical_assignment_project_payload(
        {},
        project_id=spec.project_id,
        model_key="5Z",
        zone_spec=spec,
        handover=handover,
        assignments=assignments,
    )
    changed_handover = replace(handover, revision_id="OTHER-REVISION")

    stored = stored_technical_assignment_draft(
        payload,
        model_key="5Z",
        zone_spec=spec,
        handover=changed_handover,
    )

    assert stored.has_stored_draft
    assert not stored.matches_active_handover
    assert stored.assignments == ()


def test_direct_ui_check_token_changes_with_the_assignment(tmp_path):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())
    first = (_assignments()[0],)
    changed = (replace(first[0], terminal_type=""),)

    assert technical_assignment_check_token(spec, handover, first) != technical_assignment_check_token(
        spec,
        handover,
        changed,
    )


def test_direct_ui_empty_assignment_keeps_legacy_assignment_shape(tmp_path):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())

    payload = technical_assignment_project_payload(
        {},
        project_id=spec.project_id,
        model_key="5Z",
        zone_spec=spec,
        handover=handover,
        assignments=(),
    )
    draft = payload["model_drafts"]["5Z"]

    assert "technical_assignments" not in draft
    assert draft["technical_assignment_status"] == "empty_validated_draft"
    reloaded = stored_technical_assignment_draft(
        payload,
        model_key="5Z",
        zone_spec=spec,
        handover=handover,
    )
    assert reloaded.has_stored_draft
    assert reloaded.matches_active_handover
    assert reloaded.assignments == ()


def test_direct_ui_blocks_foreign_existing_project_payload(tmp_path):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())

    with pytest.raises(ValueError, match="nicht zum aktiven Projekt"):
        technical_assignment_project_payload(
            {"project_id": "OTHER-PROJECT", "model_drafts": {"5Z": {"foreign": True}}},
            project_id=spec.project_id,
            model_key="5Z",
            zone_spec=spec,
            handover=handover,
            assignments=(),
        )


@pytest.mark.parametrize("stored_project_id", ("", 0, False, None))
def test_direct_ui_blocks_invalid_existing_project_ids_on_prefill(
    tmp_path,
    stored_project_id,
):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())

    with pytest.raises(ValueError, match="keine gueltige Projekt-ID"):
        stored_technical_assignment_draft(
            {"project_id": stored_project_id},
            model_key="5Z",
            zone_spec=spec,
            handover=handover,
        )


def test_direct_ui_blocks_foreign_project_id_on_prefill(tmp_path):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())

    with pytest.raises(ValueError, match="nicht zum aktiven Projekt"):
        stored_technical_assignment_draft(
            {"project_id": "OTHER-PROJECT"},
            model_key="5Z",
            zone_spec=spec,
            handover=handover,
        )


@pytest.mark.parametrize(
    "payload",
    (
        {"model_drafts": "broken"},
        {"model_drafts": {"5Z": "broken"}},
    ),
)
def test_direct_ui_blocks_damaged_existing_draft_structures(tmp_path, payload):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())

    with pytest.raises(ValueError, match="ungueltiges Format"):
        technical_assignment_project_payload(
            payload,
            project_id=spec.project_id,
            model_key="5Z",
            zone_spec=spec,
            handover=handover,
            assignments=(),
        )


def test_direct_ui_rejects_text_instead_of_checkbox_values(tmp_path):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())
    rows = technical_assignment_editor_rows(spec, handover)
    rows[0]["Zuordnen"] = "False"

    with pytest.raises(ValueError, match="expliziter Checkboxwert"):
        technical_assignments_from_rows(spec, handover, rows)


def test_direct_ui_stale_zone_content_is_not_prefilled(tmp_path):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())
    rows = technical_assignment_editor_rows(spec, handover)
    rows[0]["Zuordnen"] = True
    rows[0]["Manuell bestaetigt"] = True
    assignments = technical_assignments_from_rows(spec, handover, rows)
    payload = technical_assignment_project_payload(
        {},
        project_id=spec.project_id,
        model_key="5Z",
        zone_spec=spec,
        handover=handover,
        assignments=assignments,
    )
    changed_zone = replace(spec.zones[0], source_space_ids=("SPACE-CHANGED",))
    changed_spec = replace(spec, zones=(changed_zone, *spec.zones[1:]))

    stored = stored_technical_assignment_draft(
        payload,
        model_key="5Z",
        zone_spec=changed_spec,
        handover=handover,
    )

    assert zone_specification_content_hash(changed_spec) != zone_specification_content_hash(spec)
    assert stored.has_stored_draft
    assert not stored.matches_active_handover
    assert stored.assignments == ()
    assert technical_assignment_check_token(
        changed_spec,
        handover,
        assignments,
    ) != technical_assignment_check_token(spec, handover, assignments)


def test_direct_ui_render_blocks_before_editor_without_active_handover(monkeypatch):
    spec = replace(_zone_spec(), technical_assignments=())
    reference = ObjectReference(
        object_id=spec.building_id,
        revision_id=spec.source_building_version_id,
        object_type="BuildingModelSpecification",
    )
    workspace = SimpleNamespace(
        project=SimpleNamespace(identity=SimpleNamespace(project_id=spec.project_id))
    )

    class FakeStreamlit:
        session_state: dict[str, object] = {}
        warnings: list[str] = []

        @staticmethod
        def caption(*_args, **_kwargs):
            return None

        @classmethod
        def warning(cls, message, **_kwargs):
            cls.warnings.append(str(message))

        @staticmethod
        def error(*_args, **_kwargs):
            return None

        @staticmethod
        def data_editor(*_args, **_kwargs):
            raise AssertionError("Ohne aktiven P014-Handover darf kein Editor erscheinen.")

    monkeypatch.setattr(zones_view, "st", FakeStreamlit())
    monkeypatch.setattr(
        zones_view,
        "resolve_selected_building_context",
        lambda _workspace: SimpleNamespace(reference=reference),
    )
    monkeypatch.setattr(
        zones_view,
        "load_active_technical_revision",
        lambda _workspace, _reference: None,
    )

    zones_view._render_technical_assignment(
        workspace,
        {},
        model_key="5Z",
        zone_spec=spec,
    )

    assert any("kein aktiver P014-Handover" in message for message in FakeStreamlit.warnings)


def test_direct_ui_render_checks_without_write_and_saves_only_checked_draft(
    tmp_path,
    monkeypatch,
):
    handover = _technical_handover(tmp_path)
    spec = replace(_zone_spec(), technical_assignments=())
    workspace = SimpleNamespace(
        project=SimpleNamespace(identity=SimpleNamespace(project_id=spec.project_id))
    )
    saved_payloads: list[dict[str, object]] = []

    class FakeStreamlit:
        session_state: dict[str, object] = {}
        mode = "check"
        info_messages: list[str] = []
        markdown_messages: list[str] = []

        @staticmethod
        def caption(*_args, **_kwargs):
            return None

        @classmethod
        def markdown(cls, message, **_kwargs):
            cls.markdown_messages.append(str(message))

        @staticmethod
        def dataframe(*_args, **_kwargs):
            return None

        @classmethod
        def info(cls, message, **_kwargs):
            cls.info_messages.append(str(message))

        @staticmethod
        def warning(*_args, **_kwargs):
            return None

        @staticmethod
        def error(*_args, **_kwargs):
            return None

        @staticmethod
        def success(*_args, **_kwargs):
            return None

        @staticmethod
        def data_editor(rows, **_kwargs):
            edited = rows.copy()
            edited.loc[0, "Zuordnen"] = True
            edited.loc[0, "Manuell bestaetigt"] = True
            return edited

        @classmethod
        def button(cls, label, **_kwargs):
            return (cls.mode == "check" and label == "Technische Zuordnungen prüfen") or (
                cls.mode == "save" and label == "Geprüfte technische Zuordnungen übernehmen"
            )

    fake_streamlit = FakeStreamlit()
    monkeypatch.setattr(zones_view, "st", fake_streamlit)
    monkeypatch.setattr(
        zones_view,
        "resolve_selected_building_context",
        lambda _workspace: SimpleNamespace(reference=handover.building_reference),
    )
    monkeypatch.setattr(
        zones_view,
        "load_active_technical_revision",
        lambda _workspace, _reference: (object(), handover, tmp_path / "revision.yaml"),
    )
    monkeypatch.setattr(
        zones_view,
        "save_project_module_config",
        lambda _workspace, _module, payload: saved_payloads.append(payload),
    )

    zones_view._render_technical_assignment(
        workspace,
        {},
        model_key="5Z",
        zone_spec=spec,
    )
    assert saved_payloads == []
    assert "ma_zones_checked_technical_assignment" in fake_streamlit.session_state

    FakeStreamlit.mode = "save"
    zones_view._render_technical_assignment(
        workspace,
        {},
        model_key="5Z",
        zone_spec=spec,
    )

    assert len(saved_payloads) == 1
    saved_draft = saved_payloads[0]["model_drafts"]["5Z"]
    assert saved_draft["technical_assignments"][0]["assignment_origin"] == "manual_confirmed"
    assert any("kein Nachweis vollständiger Versorgung" in message for message in FakeStreamlit.info_messages)
    assert any("Handover-Hash" in message for message in FakeStreamlit.markdown_messages)


def test_direct_ui_marks_missing_terminal_compatibility_as_not_declared(tmp_path):
    handover = _technical_handover(tmp_path)
    handover_without_terminal_types = replace(
        handover,
        service_interface_references=(
            replace(handover.service_interface_references[0], compatible_terminal_types=()),
        ),
    )

    rows = technical_handover_rows(handover_without_terminal_types)

    assert rows[0]["Kompatible Terminaltypen"] == "nicht deklariert"


def test_loader_does_not_invent_manual_confirmation():
    payload = zone_specification_to_dict(_zone_spec())
    del payload["technical_assignments"][0]["assignment_origin"]

    loaded = zone_specification_from_dict(payload)
    result = validate_zone_spec(loaded)

    assert loaded.technical_assignments[0].assignment_origin == ""
    assert result.release_status is ReleaseStatus.BLOCKED
    assert "ZONE_TECHNICAL_ASSIGNMENT_FIELD_MISSING" in _codes(result)


def test_empty_technical_assignments_keep_legacy_serialization_shape():
    payload = zone_specification_to_dict(replace(_zone_spec(), technical_assignments=()))

    assert "technical_assignments" not in payload


def test_zone_spec_blocks_unknown_zone_duplicate_assignment_and_unconfirmed_origin():
    assignment = _assignments()[0]
    invalid_spec = replace(
        _zone_spec(),
        technical_assignments=(
            replace(assignment, zone_id="ZONE-UNKNOWN"),
            replace(assignment, assignment_id="ZONE-TECH-ASSIGNMENT-0003"),
            replace(
                assignment,
                assignment_id="ZONE-TECH-ASSIGNMENT-0004",
                assignment_origin="suggested",
            ),
        ),
    )

    result = validate_zone_spec(invalid_spec)

    assert result.release_status is ReleaseStatus.BLOCKED
    assert {
        "ZONE_TECHNICAL_ZONE_UNKNOWN",
        "ZONE_TECHNICAL_ASSIGNMENT_DUPLICATE",
        "ZONE_TECHNICAL_ASSIGNMENT_NOT_CONFIRMED",
    } <= _codes(result)


def test_zone_spec_blocks_duplicate_assignment_ids():
    first, second = _assignments()
    result = validate_zone_spec(
        replace(
            _zone_spec(),
            technical_assignments=(first, replace(second, assignment_id=first.assignment_id)),
        )
    )

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "ZONE_OBJECT_ID_DUPLICATE" in _codes(result)


def test_direct_assignment_construction_normalizes_whitespace():
    assignment = ZoneTechnicalServiceAssignment(
        assignment_id="   ",
        zone_id=" ZONE-0001 ",
        service_interface_id=" SYNTHETIC-SERVICE-HEATING-0001 ",
        assignment_origin=" manual_confirmed ",
    )
    result = validate_zone_spec(replace(_zone_spec(), technical_assignments=(assignment,)))

    assert assignment.assignment_id == ""
    assert assignment.zone_id == "ZONE-0001"
    assert result.release_status is ReleaseStatus.BLOCKED
    assert "ZONE_OBJECT_ID_MISSING" in _codes(result)


def test_zone_spec_blocks_two_terminal_types_for_the_same_zone_interface_relation():
    first = _assignments()[0]
    result = validate_zone_spec(
        replace(
            _zone_spec(),
            technical_assignments=(
                first,
                replace(
                    first,
                    assignment_id="ZONE-TECH-ASSIGNMENT-OTHER",
                    terminal_type="other_terminal",
                ),
            ),
        )
    )

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "ZONE_TECHNICAL_ASSIGNMENT_DUPLICATE" in _codes(result)


def test_zone_assignments_validate_against_builder_generated_technical_handover(tmp_path):
    first, second = _assignments()
    spec_with_optional_terminal = replace(
        _zone_spec(),
        technical_assignments=(replace(first, terminal_type=""), second),
    )

    result = validate_zone_technical_assignments(spec_with_optional_terminal, _technical_handover(tmp_path))

    assert result.release_status is ReleaseStatus.RELEASED


@pytest.mark.parametrize(
    ("changed_assignment", "expected_code"),
    [
        (
            replace(_assignments()[0], service_interface_id="SYNTHETIC-SERVICE-UNKNOWN"),
            "ZONE_TECHNICAL_INTERFACE_UNKNOWN",
        ),
        (
            replace(_assignments()[0], terminal_type="incompatible_terminal"),
            "ZONE_TECHNICAL_TERMINAL_INCOMPATIBLE",
        ),
    ],
)
def test_zone_assignments_block_unknown_interface_or_incompatible_terminal(
    tmp_path,
    changed_assignment,
    expected_code,
):
    spec = replace(_zone_spec(), technical_assignments=(changed_assignment, *_assignments()[1:]))

    result = validate_zone_technical_assignments(spec, _technical_handover(tmp_path))

    assert result.release_status is ReleaseStatus.BLOCKED
    assert expected_code in _codes(result)


def test_zone_assignments_block_changed_or_unreleased_technical_handover(tmp_path):
    handover = _technical_handover(tmp_path)
    changed_reference = replace(
        handover.service_interface_references[0],
        compatible_terminal_types=("changed_terminal",),
    )

    changed_references = (changed_reference,)
    changed_result = validate_zone_technical_assignments(
        _zone_spec(),
        replace(
            handover,
            service_interface_references=changed_references,
            service_interface_references_hash=_service_interface_references_hash(changed_references),
        ),
    )
    unreleased_result = validate_zone_technical_assignments(
        _zone_spec(),
        replace(handover, release_status=ReleaseStatus.BLOCKED),
    )

    assert "ZONE_TECHNICAL_HANDOVER_CONTENT_HASH_MISMATCH" in _codes(changed_result)
    assert "ZONE_TECHNICAL_HANDOVER_NOT_RELEASED" in _codes(unreleased_result)


def test_zone_assignments_block_context_mismatch_and_duplicate_interface_reference(tmp_path):
    handover = _technical_handover(tmp_path)
    duplicate_reference_handover = replace(
        handover,
        service_interface_references=(
            handover.service_interface_references[0],
            handover.service_interface_references[0],
        ),
    )

    context_result = validate_zone_technical_assignments(
        _zone_spec(),
        replace(handover, project_id="SYNTHETIC-PROJECT-OTHER"),
    )
    missing_revision_result = validate_zone_technical_assignments(
        _zone_spec(),
        replace(handover, building_reference=replace(handover.building_reference, revision_id="")),
    )
    duplicate_result = validate_zone_technical_assignments(_zone_spec(), duplicate_reference_handover)

    assert "ZONE_TECHNICAL_PROJECT_REFERENCE_MISMATCH" in _codes(context_result)
    assert "ZONE_TECHNICAL_BUILDING_REVISION_MISMATCH" in _codes(missing_revision_result)
    assert "ZONE_TECHNICAL_INTERFACE_REFERENCE_DUPLICATE" in _codes(duplicate_result)


def test_zone_assignments_reject_non_handover_input():
    result = validate_zone_technical_assignments(_zone_spec(), object())

    assert result.release_status is ReleaseStatus.BLOCKED
    assert "ZONE_TECHNICAL_HANDOVER_TYPE_INVALID" in _codes(result)


def test_zone_handover_hash_is_assignment_order_independent(tmp_path):
    original = _released_zone_handover(tmp_path)
    reordered_spec = replace(_zone_spec(), technical_assignments=tuple(reversed(_assignments())))

    reordered = _released_zone_handover(tmp_path / "reordered", zone_spec=reordered_spec)

    assert reordered.content_hash == original.content_hash
    assert reordered.revision_id == original.revision_id


def test_zone_handover_binds_the_complete_technical_handover_hash(tmp_path):
    technical_handover = _technical_handover(tmp_path)

    zone_handover = _released_zone_handover(tmp_path / "zone", technical_handover=technical_handover)

    assert zone_handover.technical_handover_content_hash == technical_handover.handover_content_hash


def test_zone_handover_hash_changes_for_semantic_assignment_mutation(tmp_path):
    original = _released_zone_handover(tmp_path)
    changed_assignment = replace(_assignments()[0], assignment_id="ZONE-TECH-ASSIGNMENT-CHANGED")
    changed_spec = replace(_zone_spec(), technical_assignments=(changed_assignment, *_assignments()[1:]))

    changed = _released_zone_handover(tmp_path / "changed", zone_spec=changed_spec)

    assert changed.content_hash != original.content_hash
    assert changed.revision_id != original.revision_id


def test_zone_handover_blocks_assignment_with_changed_interface_reference(tmp_path):
    handover = _technical_handover(tmp_path)
    changed_reference = replace(
        handover.service_interface_references[0],
        compatible_terminal_types=("changed_terminal",),
    )

    changed_references = (changed_reference,)
    with pytest.raises(ValueError, match="Technische Zonenzuordnungen"):
        _released_zone_handover(
            tmp_path / "changed",
            technical_handover=replace(
                handover,
                service_interface_references=changed_references,
                service_interface_references_hash=_service_interface_references_hash(changed_references),
            ),
        )


@pytest.mark.parametrize(
    "assignment",
    [
        replace(_assignments()[0], service_interface_id="SYNTHETIC-SERVICE-UNKNOWN"),
        replace(_assignments()[0], terminal_type="incompatible_terminal"),
    ],
)
def test_zone_handover_release_gateway_blocks_invalid_assignments(tmp_path, assignment):
    invalid_spec = replace(_zone_spec(), technical_assignments=(assignment, *_assignments()[1:]))

    with pytest.raises(ValueError, match="Technische Zonenzuordnungen"):
        _released_zone_handover(tmp_path, zone_spec=invalid_spec)
