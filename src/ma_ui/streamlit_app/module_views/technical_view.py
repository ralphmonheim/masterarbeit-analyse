"""Fachansicht fuer technische Systeme."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from pathlib import Path

import streamlit as st

from ma_database import CatalogSelection, DemoCatalogRecord, load_demo_catalog, select_demo_record
from ma_technical import (
    ReleasedTechnicalHandover,
    TechnicalModelSpecification,
    TechnicalSystemSpecification,
    adapt_legacy_v1_to_v2,
    load_business_integration_lod1_technical_spec,
    load_small_office_5z_endvariant_02_technical_spec,
    load_synthetic_v2_reference_technical_spec,
    load_technical_excel_catalog,
    next_technical_model_id,
    next_technical_revision_id,
    release_workspace_technical_model,
    technical_catalog_record_status,
    technical_model_content_hash,
    technical_revisions_directory,
    validate_technical_model,
    validate_technical_spec,
)
from ma_ui.streamlit_app.module_views.technical_release_support import (
    SelectedBuildingContext,
    StaleActiveTechnicalRevisionError,
    legacy_technical_source_rows,
    load_active_technical_revision,
    load_legacy_technical_source,
    resolve_selected_building_context,
    store_active_technical_revision,
)
from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_ui.streamlit_app.shared.tables import normalize_table_for_streamlit
from ma_ui.streamlit_app.state import (
    clear_workspace_draft,
    get_active_workspace,
    mark_workspace_draft,
)
from ma_validation import DiagnosticMessage, DiagnosticSeverity, ReleaseStatus
from ma_workflow import get_module_definition
from ma_workspace import load_project_module_config, save_project_module_config

TECHNICAL_WORKSPACE_TAB_LABELS = ("Technikmodell", "Übersicht", "Auswahl")
TECHNICAL_SELECTION_TAB_LABELS = (
    "Heizung",
    "Kuehlung",
    "Lueftung",
    "Speicher",
    "Trinkwarmwasser",
    "Elektrik",
)
TECHNICAL_CATALOG_DIRECTORY = Path("data/catalogs/technical_systems")
PROJECT_ROOT = Path(__file__).resolve().parents[4]
TECHNICAL_V2_DRAFT_KEY = "ma_technical_v2_draft"
TECHNICAL_V2_VALIDATED_DRAFT_KEY = "ma_technical_v2_validated_draft"
TECHNICAL_V2_DRAFT_SOURCE_KEY = "ma_technical_v2_draft_source"
TECHNICAL_V2_RELEASE_CONFIRM_KEY = "ma_technical_confirm_v2_release"


def technical_scope_rows() -> list[dict[str, object]]:
    """Liefert den aktuellen geplanten Umfang von ma_technical."""
    module = get_module_definition("ma_technical")
    return [
        {"Bereich": "Status", "Stand": module.status, "Einordnung": "P014-S1 Lite"},
        {"Bereich": "Eingabe", "Stand": "Gebaeudedaten", "Einordnung": "kommt validiert aus ma_building"},
        {"Bereich": "Eingabe", "Stand": "System- und Produktdaten", "Einordnung": "LoD-1-Demo vorhanden"},
        {
            "Bereich": "Ausgabe",
            "Stand": "Systeme und Serviceinterface-IDs",
            "Einordnung": "zonenfrei fuer ma_zones",
        },
        {"Bereich": "Abgrenzung", "Stand": "keine Variantenbildung", "Einordnung": "bleibt in ma_variants"},
        {"Bereich": "Naechster Fokus", "Stand": "ParameterSnapshot", "Einordnung": "folgt in P015"},
    ]


def legacy_technical_summary_rows(spec: TechnicalSystemSpecification) -> list[dict[str, object]]:
    """Liefert kompakte Kennwerte des fallbezogenen Legacy-Uebergangsstands."""
    return [
        {"Kennwert": "Technikmodell", "Wert": spec.technical_model_id},
        {"Kennwert": "Gebaeude", "Wert": spec.building_id},
        {"Kennwert": "Zonenmodell", "Wert": spec.source_zone_model_id},
        {"Kennwert": "Eingabe-LoD", "Wert": _display_value(spec.input_detail_level)},
        {"Kennwert": "Systeme", "Wert": len(spec.systems)},
    ]


def technical_summary_rows(spec: TechnicalModelSpecification) -> list[dict[str, object]]:
    """Liefert zonenfreie Kennwerte einer v2-TechnicalModelSpecification."""
    return [
        {"Kennwert": "Technikmodell", "Wert": spec.technical_model_id},
        {"Kennwert": "Projekt", "Wert": spec.project_id},
        {"Kennwert": "Gebaeude", "Wert": spec.building_reference.object_id},
        {"Kennwert": "Gebaeuderevision", "Wert": spec.building_reference.revision_id},
        {
            "Kennwert": "Gebaeude-Content-Hash",
            "Wert": spec.building_reference.content_hash or "nicht vorhanden",
        },
        {"Kennwert": "Eingabe-LoD", "Wert": _display_value(spec.declared_detail_level)},
        {"Kennwert": "Technische Objekte", "Wert": len(technical_object_rows(spec))},
        {"Kennwert": "Serviceinterfaces", "Wert": len(spec.service_interfaces)},
    ]


def technical_object_rows(spec: TechnicalModelSpecification) -> list[dict[str, object]]:
    """Zeigt zentrale technische Objekt-IDs ohne direkte Zonenreferenzen."""
    rows = [
        {
            "Objekt-ID": equipment.equipment_id,
            "Objekttyp": "PhysicalEquipment",
            "Fachtyp": equipment.equipment_type,
            "Verfuegbarkeit": _display_value(equipment.availability),
            "Darstellung": _display_value(equipment.representation_mode),
        }
        for equipment in spec.equipment_register
    ]
    optional_objects = (
        (spec.plant, "plant_id", "TechnicalPlant"),
        (spec.air_handling_unit, "ahu_id", "AirHandlingUnit"),
        (spec.electrical_system, "electrical_system_id", "ElectricalSystem"),
    )
    for technical_object, id_attribute, object_type in optional_objects:
        if technical_object is not None:
            rows.append(
                {
                    "Objekt-ID": getattr(technical_object, id_attribute),
                    "Objekttyp": object_type,
                    "Fachtyp": "",
                    "Verfuegbarkeit": _display_value(getattr(technical_object, "availability", "")),
                    "Darstellung": _display_value(getattr(technical_object, "representation_mode", "")),
                }
            )
    return rows


def technical_service_interface_rows(spec: TechnicalModelSpecification) -> list[dict[str, object]]:
    """Bereitet die von ma_technical definierten Serviceinterfaces fuer die UI auf."""
    return [
        {
            "Serviceinterface-ID": interface.interface_id,
            "Service": _display_value(interface.service_type),
            "Medium": _display_value(interface.medium),
            "Quellobjekt-ID": interface.source_system_reference.object_id,
            "Quellobjekttyp": interface.source_system_reference.object_type,
            "Kompatible Terminaltypen": ", ".join(interface.compatible_terminal_types),
            "Kapazitaetsmodus": _display_value(interface.capacity_mode),
            "Verfuegbarkeit": _display_value(interface.availability),
        }
        for interface in spec.service_interfaces
    ]


def technical_system_rows(spec: TechnicalSystemSpecification) -> list[dict[str, object]]:
    """Bereitet technische Systeme fuer die UI auf."""
    return [
        {
            "System": system.system_id,
            "Name": system.name,
            "Typ": system.system_type,
            "Zonen": ", ".join(system.served_zone_ids),
            "Leistung [W/m2]": system.design_power_w_m2,
            "Zuluft/Versorgung [Grad C]": system.supply_temperature_c,
            "Ruecklauf [Grad C]": system.return_temperature_c,
            "Leistungszahl": system.performance_factor,
            "Luftwechsel [1/h]": system.air_change_rate_1_h,
            "WRG [%]": system.heat_recovery_efficiency_percent,
            "Regelung": system.control_strategy,
        }
        for system in spec.systems
    ]


def render() -> None:
    """Zeigt Legacy-Uebergang und zonenfreie v2-Struktur klar getrennt."""
    module = get_module_definition("ma_technical")
    render_page_header(module.label, module.purpose)
    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.warning("Bitte zuerst ein Projekt auswaehlen.")
        return
    try:
        legacy_spec = (
            load_small_office_5z_endvariant_02_technical_spec()
            if workspace.project.identity.title == "Masterarbeit-Analyse"
            else load_business_integration_lod1_technical_spec()
        )
        v2_reference_spec = load_synthetic_v2_reference_technical_spec()
    except (OSError, ValueError) as exc:
        st.error(f"Technikspezifikation konnte nicht geladen werden: {exc}")
        return

    legacy_validation = validate_technical_spec(legacy_spec)
    v2_validation = validate_technical_model(v2_reference_spec)
    section = st.segmented_control(
        "Technikbereich",
        TECHNICAL_WORKSPACE_TAB_LABELS,
        default=TECHNICAL_WORKSPACE_TAB_LABELS[0],
        key="ma_technical_workspace_section",
        selection_mode="single",
    )
    section = section or TECHNICAL_WORKSPACE_TAB_LABELS[0]
    if section == "Technikmodell":
        st.subheader("Legacy-Referenzstand fuer den bekannten Demo-Fall")
        st.caption(
            "Dieser bisherige Referenzstand enthaelt noch direkte Zonenbezuege. "
            "Er ist weder das zonenfreie Zielmodell noch ein v2-Handover."
        )
        st.metric("Legacy-Strukturpruefung", _structural_validation_label(legacy_validation.messages))
        st.dataframe(
            normalize_table_for_streamlit(legacy_technical_summary_rows(legacy_spec)),
            hide_index=True,
            width="stretch",
        )
        st.dataframe(
            normalize_table_for_streamlit(technical_system_rows(legacy_spec)), hide_index=True, width="stretch"
        )
        if legacy_spec.assumptions:
            st.dataframe(
                normalize_table_for_streamlit(
                    [
                        {
                            "ID": assumption.assumption_id,
                            "Fundstelle": assumption.location or "",
                            "Annahme": assumption.text,
                        }
                        for assumption in legacy_spec.assumptions
                    ]
                ),
                hide_index=True,
                width="stretch",
            )
        _render_messages(legacy_validation.messages, structure_only=True)

        st.subheader("Zonenfreie v2-Strukturreferenz (synthetisch)")
        st.warning(
            "Nur synthetische, ausschliesslich lesend geladene Testreferenz: kein aktiver Projektstand, "
            "keine Projektfreigabe und nicht fuer Dimensionierung oder Simulation."
        )
        st.metric("v2-Strukturpruefung", _structural_validation_label(v2_validation.messages))
        st.dataframe(
            normalize_table_for_streamlit(technical_summary_rows(v2_reference_spec)),
            hide_index=True,
            width="stretch",
        )
        st.dataframe(
            normalize_table_for_streamlit(technical_object_rows(v2_reference_spec)),
            hide_index=True,
            width="stretch",
        )
        st.dataframe(
            normalize_table_for_streamlit(technical_service_interface_rows(v2_reference_spec)),
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "Der Kapazitaetsmodus der Testreferenz ist eine synthetische Modellannahme, "
            "kein Leistungs-, Eignungs- oder Versorgungsnachweis."
        )
        _render_messages(v2_validation.messages, structure_only=True)
        _render_project_technical_release(workspace)

    elif section == "Übersicht":
        _render_fixed_technical_reference(legacy_spec, v2_reference_spec)
    else:
        _render_fixed_technical_selection(legacy_spec)


def prepare_project_technical_draft(
    workspace,
    building_context: SelectedBuildingContext,
    *,
    selection_key: str,
    technical_model_id: str,
) -> TechnicalModelSpecification:
    """Bereitet einen projektgebundenen v2-Entwurf ohne Workspace-Schreibzugriff vor."""
    legacy_specification, source_path = load_legacy_technical_source(selection_key)
    resolved_source_path = source_path.resolve()
    if not resolved_source_path.is_relative_to(PROJECT_ROOT):
        raise ValueError("Die Legacy-Technikquelle liegt ausserhalb des Repositorys.")
    source_sha256 = hashlib.sha256(resolved_source_path.read_bytes()).hexdigest()
    return adapt_legacy_v1_to_v2(
        legacy_specification,
        technical_model_id=technical_model_id,
        project_id=workspace.project.identity.project_id,
        building_reference=building_context.reference,
        legacy_source_reference=resolved_source_path.relative_to(PROJECT_ROOT).as_posix(),
        legacy_source_sha256=source_sha256,
    )


def technical_handover_rows(
    handover: ReleasedTechnicalHandover,
    revision_path: Path,
    *,
    workspace_root: Path,
) -> list[dict[str, object]]:
    """Zeigt die aktive, reload-gepruefte Technikuebergabe kompakt an."""
    building_reference = handover.building_reference
    relative_path = revision_path.resolve().relative_to(workspace_root.resolve()).as_posix()
    return [
        {"Merkmal": "Technikmodell-ID", "Wert": handover.technical_model_id},
        {"Merkmal": "Revision-ID", "Wert": handover.revision_id},
        {"Merkmal": "Projekt-ID", "Wert": handover.project_id},
        {
            "Merkmal": "Building-ID",
            "Wert": building_reference.object_id if building_reference is not None else "",
        },
        {
            "Merkmal": "Building-Version",
            "Wert": building_reference.revision_id if building_reference is not None else "",
        },
        {"Merkmal": "Content-Hash", "Wert": handover.content_hash},
        {
            "Merkmal": "Building-Content-Hash",
            "Wert": (
                building_reference.content_hash
                if building_reference is not None and building_reference.content_hash
                else "nicht vorhanden"
            ),
        },
        {"Merkmal": "Freigabenachweis-Hash", "Wert": handover.release_evidence_hash},
        {"Merkmal": "Handover-Hash", "Wert": handover.handover_content_hash},
        {"Merkmal": "Serviceinterfaces", "Wert": len(handover.service_interface_references)},
        {"Merkmal": "Revisionsdatei", "Wert": relative_path},
    ]


def _render_project_technical_release(workspace) -> None:
    """Fuehrt Entwurf, Strukturpruefung und explizite Revision getrennt aus."""
    st.subheader("Projektbezogene v2-Technikrevision")
    st.caption(
        "Der Legacy-Stand dient nur als nachvollziehbare Quelle. Die v2-Revision definiert Systeme und "
        "Serviceinterface-IDs, aber keine Zonenbelegung, Lastberechnung oder Dimensionierung."
    )
    try:
        building_context = resolve_selected_building_context(workspace)
    except (OSError, ValueError) as exc:
        st.warning(f"Freigabe noch gesperrt: {exc}")
        st.caption("Korrekturziel: Modul Gebaeude. Dort zuerst einen Building-Stand projektbezogen uebernehmen.")
        return

    stale_model_id = ""
    try:
        active_revision = load_active_technical_revision(
            workspace,
            building_context.reference,
        )
    except StaleActiveTechnicalRevisionError as exc:
        st.warning(
            "Der bisher aktive Technikstand gehoert zu einer frueheren Building-Version. "
            "Bitte fuer den aktuellen Building-Stand einen neuen v2-Entwurf pruefen und freigeben."
        )
        active_revision = None
        stale_model_id = exc.technical_model_id
    except (OSError, ValueError) as exc:
        st.error(f"Aktive Technikrevision ist nicht konsistent: {exc}")
        return

    if active_revision is None:
        if stale_model_id:
            technical_model_id = stale_model_id
        else:
            st.info("Fuer das ausgewaehlte Building ist noch keine aktive v2-Technikrevision freigegeben.")
            technical_model_id = next_technical_model_id(workspace.paths.root)
    else:
        _revision, active_handover, active_path = active_revision
        st.success("Aktiver, hashgepruefter Technik-Handover fuer dieses Building.")
        st.dataframe(
            normalize_table_for_streamlit(
                technical_handover_rows(
                    active_handover,
                    active_path,
                    workspace_root=workspace.paths.root,
                )
            ),
            hide_index=True,
            width="stretch",
        )
        technical_model_id = active_handover.technical_model_id

    source_rows = legacy_technical_source_rows()
    source_labels = {row["Schluessel"]: row["Name"] for row in source_rows}
    source_paths = {row["Schluessel"]: row["Quelle"] for row in source_rows}
    selected_source_key = st.selectbox(
        "Legacy-Quelle fuer den v2-Entwurf",
        tuple(source_labels),
        format_func=source_labels.__getitem__,
        key="ma_technical_v2_source_selection",
    )
    st.caption(f"Versionierte Quelle: `{source_paths[selected_source_key]}`")

    if st.button("v2-Entwurf vorbereiten", key="ma_technical_prepare_v2_draft"):
        try:
            draft = prepare_project_technical_draft(
                workspace,
                building_context,
                selection_key=selected_source_key,
                technical_model_id=technical_model_id,
            )
        except (OSError, ValueError) as exc:
            st.error(f"v2-Entwurf konnte nicht vorbereitet werden: {exc}")
        else:
            st.session_state[TECHNICAL_V2_DRAFT_KEY] = draft
            st.session_state[TECHNICAL_V2_DRAFT_SOURCE_KEY] = selected_source_key
            st.session_state.pop(TECHNICAL_V2_VALIDATED_DRAFT_KEY, None)
            st.session_state[TECHNICAL_V2_RELEASE_CONFIRM_KEY] = False
            mark_workspace_draft(st.session_state, "ma_technical")
            st.success("v2-Entwurf wurde nur im Sitzungszustand vorbereitet; es wurde keine Revision geschrieben.")

    draft = st.session_state.get(TECHNICAL_V2_DRAFT_KEY)
    if not isinstance(draft, TechnicalModelSpecification):
        return
    if draft.project_id != workspace.project.identity.project_id or draft.building_reference != building_context.reference:
        st.warning("Der Sitzungsentwurf gehoert nicht mehr zum aktiven Projekt- und Building-Stand.")
        return

    draft_source_key = st.session_state.get(TECHNICAL_V2_DRAFT_SOURCE_KEY)
    if draft_source_key != selected_source_key:
        st.warning("Die Quellenauswahl wurde geaendert. Bitte den v2-Entwurf erneut vorbereiten.")
        return

    draft_validation = validate_technical_model(draft)
    draft_hash = technical_model_content_hash(draft)
    next_revision_id = next_technical_revision_id(
        workspace.paths.root,
        building_id=building_context.reference.object_id,
        technical_model_id=draft.technical_model_id,
    )
    target_path = (
        technical_revisions_directory(
            workspace.paths.root,
            building_id=building_context.reference.object_id,
            technical_model_id=draft.technical_model_id,
        )
        / f"{next_revision_id}.yaml"
    )
    st.dataframe(
        normalize_table_for_streamlit(technical_summary_rows(draft)),
        hide_index=True,
        width="stretch",
    )
    st.dataframe(
        normalize_table_for_streamlit(technical_object_rows(draft)),
        hide_index=True,
        width="stretch",
    )
    st.dataframe(
        normalize_table_for_streamlit(technical_service_interface_rows(draft)),
        hide_index=True,
        width="stretch",
    )
    st.dataframe(
        normalize_table_for_streamlit(
            [
                {"Merkmal": "Legacy-Quelle", "Wert": draft.source_metadata.source_reference},
                {"Merkmal": "Mapping", "Wert": draft.source_metadata.input_source.adapter_key},
                {"Merkmal": "Quellen-SHA-256", "Wert": draft.source_metadata.input_source.sha256},
                {"Merkmal": "Entwurfs-Content-Hash", "Wert": draft_hash},
                {"Merkmal": "Naechste Revision-ID", "Wert": next_revision_id},
                {
                    "Merkmal": "Zielpfad",
                    "Wert": target_path.relative_to(workspace.paths.root).as_posix(),
                },
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    st.caption(
        "Legacy-Kennwerte und die Anzahl verworfener Zonenbindungen bleiben als Annahmen nachvollziehbar. "
        "Sie werden nicht in absolute Leistungen oder eine Dimensionierung umgerechnet."
    )

    if st.button("Struktur prüfen", key="ma_technical_validate_v2_draft"):
        if draft_validation.release_status is not ReleaseStatus.BLOCKED:
            st.session_state[TECHNICAL_V2_VALIDATED_DRAFT_KEY] = draft
            if draft_validation.release_status is ReleaseStatus.CONFIRMATION_REQUIRED:
                st.warning("Die v2-Struktur hat bestaetigungspflichtige Warnungen, aber keine blockierenden Fehler.")
            else:
                st.success("Die v2-Struktur ist fehlerfrei und fuer eine bewusste Freigabe geeignet.")
        else:
            st.session_state.pop(TECHNICAL_V2_VALIDATED_DRAFT_KEY, None)
            st.error("Die v2-Struktur ist noch nicht freigabefaehig.")
    _render_messages(draft_validation.messages, structure_only=True)

    validation_matches = st.session_state.get(TECHNICAL_V2_VALIDATED_DRAFT_KEY) == draft
    confirmation_label = (
        "Ich habe die angezeigten Warnungen geprueft und akzeptiere sie fuer diese Revision; "
        "Projekt, Building, Quelle und zonenfreie v2-Struktur sind bestaetigt."
        if draft_validation.release_status is ReleaseStatus.CONFIRMATION_REQUIRED
        else "Ich bestaetige Projekt, Building, Quelle und die zonenfreie v2-Struktur."
    )
    release_confirmed = st.checkbox(
        confirmation_label,
        key=TECHNICAL_V2_RELEASE_CONFIRM_KEY,
        disabled=not validation_matches,
    )
    if st.button(
        "Revision freigeben",
        key="ma_technical_release_v2_revision",
        disabled=not validation_matches or not release_confirmed,
    ):
        _release_project_technical_draft(
            workspace,
            building_context,
            draft,
            warnings_confirmed=release_confirmed,
        )


def _release_project_technical_draft(
    workspace,
    building_context: SelectedBuildingContext,
    draft: TechnicalModelSpecification,
    *,
    warnings_confirmed: bool,
) -> None:
    """Schreibt erst nach dem Button und baut den Handover aus dem Reload auf."""
    try:
        current_building_context = resolve_selected_building_context(workspace)
        if current_building_context.reference != building_context.reference:
            raise ValueError("Der ausgewaehlte Building-Stand hat sich seit der Strukturpruefung geaendert.")
        if draft.project_id != workspace.project.identity.project_id:
            raise ValueError("Der v2-Entwurf gehoert nicht zum aktiven Projekt.")
        revision = release_workspace_technical_model(
            draft,
            workspace_root=workspace.paths.root,
            building_reference=building_context.reference,
            warnings_confirmed=warnings_confirmed,
        )
        revision_path = (
            technical_revisions_directory(
                workspace.paths.root,
                building_id=building_context.reference.object_id,
                technical_model_id=revision.technical_model_id,
            )
            / f"{revision.revision_id}.yaml"
        )
    except (OSError, RuntimeError, ValueError) as exc:
        st.error(f"Technikrevision konnte nicht freigegeben werden: {exc}")
        return

    try:
        reloaded_revision, handover = store_active_technical_revision(
            workspace,
            revision_path=revision_path,
        )
        if reloaded_revision.revision_id != revision.revision_id:
            raise ValueError("Die aktivierte Revision stimmt nicht mit dem Freigabeereignis ueberein.")
    except (OSError, RuntimeError, ValueError) as exc:
        relative_path = revision_path.relative_to(workspace.paths.root).as_posix()
        st.error(
            "Die Revision wurde append-only gespeichert, konnte aber nicht als aktiver Technikstand "
            f"referenziert werden: `{relative_path}`. Ursache: {exc}"
        )
        return

    clear_workspace_draft(st.session_state, "ma_technical")
    st.session_state.pop(TECHNICAL_V2_DRAFT_KEY, None)
    st.session_state.pop(TECHNICAL_V2_VALIDATED_DRAFT_KEY, None)
    st.session_state.pop(TECHNICAL_V2_DRAFT_SOURCE_KEY, None)
    st.session_state.pop(TECHNICAL_V2_RELEASE_CONFIRM_KEY, None)
    st.success("Die neue Technikrevision wurde append-only gespeichert, neu geladen und als aktiv referenziert.")
    st.dataframe(
        normalize_table_for_streamlit(
            technical_handover_rows(
                handover,
                revision_path,
                workspace_root=workspace.paths.root,
            )
        ),
        hide_index=True,
        width="stretch",
    )


def _render_fixed_technical_reference(
    legacy_spec: TechnicalSystemSpecification,
    v2_reference_spec: TechnicalModelSpecification,
) -> None:
    """Zeigt Legacy- und v2-Referenz ohne ihre fachlichen Rollen zu vermischen."""

    st.subheader("Legacy-Referenzsatz fuer den bekannten Demo-Fall")
    st.caption("Uebergangsbestand mit direkten Zonenbezuegen; kein v2-Handover.")
    st.dataframe(normalize_table_for_streamlit(technical_system_rows(legacy_spec)), hide_index=True, width="stretch")
    st.subheader("Synthetische v2-Testreferenz")
    st.caption("Zonenfrei und nur lesend; nicht projektfreigegeben und nicht simulationsbereit.")
    st.dataframe(
        normalize_table_for_streamlit(technical_service_interface_rows(v2_reference_spec)),
        hide_index=True,
        width="stretch",
    )
    st.caption("Der Kapazitaetsmodus ist hier nur eine synthetische Modellannahme, kein Leistungsnachweis.")


def _render_fixed_technical_selection(spec: TechnicalSystemSpecification) -> None:
    """Zeigt Excel-Datensaetze und uebernimmt nur bewusst ausgewaehlte Quellen."""

    workspace = get_active_workspace(st.session_state)
    if workspace is None:
        st.error("Bitte zuerst ein Projekt auswaehlen.")
        return
    selected_area = st.segmented_control(
        "Systembereich",
        TECHNICAL_SELECTION_TAB_LABELS,
        default=TECHNICAL_SELECTION_TAB_LABELS[0],
        key="ma_technical_excel_system_area",
        selection_mode="single",
    )
    selected_area = selected_area or TECHNICAL_SELECTION_TAB_LABELS[0]
    st.caption(
        f"Bearbeitungsbereich: {selected_area}. Die Excel-Zeile bleibt die einzige Inhaltsquelle."
    )
    catalog_files = tuple(sorted(TECHNICAL_CATALOG_DIRECTORY.glob("*.xlsx")))
    if not catalog_files:
        st.warning(
            "Quelle fehlt: Für technische Systempakete ist noch kein Excel-Katalog unter "
            f"`{TECHNICAL_CATALOG_DIRECTORY.as_posix()}` vorhanden. Es werden keine Produktdaten erfunden."
        )
        st.caption("Die vorhandene Config bleibt nur als Referenzvorlage sichtbar.")
        st.dataframe(
            normalize_table_for_streamlit(technical_system_rows(spec)),
            hide_index=True,
            width="stretch",
        )
        return

    selected_catalog = st.selectbox(
        "Techniksystem-Katalog",
        catalog_files,
        format_func=lambda path: path.name,
        key="technical_catalog_file",
    )
    try:
        catalog = load_technical_excel_catalog(selected_catalog)
    except (OSError, ValueError) as exc:
        st.error(f"Techniksystem-Katalog konnte nicht gelesen werden: {exc}")
        return

    st.caption(f"Excel-Quelle: {catalog.source_path.as_posix()} · SHA-256: {catalog.source_sha256}")
    st.dataframe(
        normalize_table_for_streamlit(technical_excel_catalog_rows(catalog.rows, catalog.id_column)),
        hide_index=True,
        width="stretch",
    )
    selected_id = st.selectbox(
        "Techniksystem-Entwurf",
        [str(row[catalog.id_column]) for row in catalog.rows],
        format_func=lambda record_id: _technical_excel_option_label(catalog.rows, catalog.id_column, record_id),
        key="technical_excel_catalog_selection",
        on_change=_mark_technical_draft,
    )
    selected_record = next(row for row in catalog.rows if str(row[catalog.id_column]) == selected_id)
    active, validated, validation_status = technical_catalog_record_status(selected_record)
    st.dataframe(
        normalize_table_for_streamlit(
            [
                {"Merkmal": "Auswahl", "Wert": selected_id},
                {"Merkmal": "Aktiv", "Wert": "ja" if active else "nein"},
                {"Merkmal": "Validiert", "Wert": "ja" if validated else "nein"},
                {"Merkmal": "Validierungsstatus", "Wert": validation_status},
                *[{"Merkmal": key, "Wert": value} for key, value in selected_record.items()],
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    if not active or not validated:
        st.warning("Nur aktive und validierte Excel-Datensaetze duerfen projektbezogen uebernommen werden.")
    if st.button(
        "Ausgewählten Techniksystem-Entwurf projektbezogen übernehmen",
        key="technical_apply_excel_catalog_selection",
        disabled=not active or not validated,
    ):
        payload = _technical_project_payload(workspace)
        payload["excel_catalog_selection"] = {
            **technical_excel_selection_payload(catalog, selected_record),
            "system_area": selected_area,
        }
        try:
            save_project_module_config(workspace, "ma_technical", payload)
        except (OSError, ValueError) as exc:
            st.error(f"Projektkonfiguration konnte nicht gespeichert werden: {exc}")
        else:
            clear_workspace_draft(st.session_state, "ma_technical")
            st.success("Der validierte Techniksystem-Entwurf wurde projektbezogen gespeichert.")


def technical_excel_catalog_rows(rows: tuple[dict[str, object], ...], id_column: str) -> list[dict[str, object]]:
    """Add transparent source statuses without changing the Excel record content."""
    result: list[dict[str, object]] = []
    for row in rows:
        active, validated, status = technical_catalog_record_status(row)
        result.append(
            {
                id_column: row[id_column],
                "Aktiv": "ja" if active else "nein",
                "Validiert": "ja" if validated else "nein",
                "Validierungsstatus": status,
                **{key: value for key, value in row.items() if key != id_column},
            }
        )
    return result


def technical_excel_selection_payload(catalog, record: dict[str, object]) -> dict[str, object]:
    """Create the small project-owned reference to a selected, unchanged Excel record."""
    active, validated, validation_status = technical_catalog_record_status(record)
    if not active or not validated:
        raise ValueError("Nur aktive und validierte Techniksystem-Datensaetze duerfen uebernommen werden.")
    return {
        "catalog_record_id": str(record[catalog.id_column]),
        "source_path": catalog.source_path.as_posix(),
        "source_version": f"sha256:{catalog.source_sha256[:12]}",
        "source_sha256": catalog.source_sha256,
        "source_sheet": "Übersicht",
        "active": active,
        "validated": validated,
        "validation_status": validation_status,
        "record": dict(record),
    }


def _technical_excel_option_label(rows: tuple[dict[str, object], ...], id_column: str, record_id: str) -> str:
    row = next(row for row in rows if str(row[id_column]) == record_id)
    active, validated, status = technical_catalog_record_status(row)
    return f"{record_id} · {'aktiv' if active else 'inaktiv'} · {status} · {'validiert' if validated else 'nicht validiert'}"


def _technical_project_payload(workspace) -> dict[str, object]:
    payload = load_project_module_config(workspace, "ma_technical")
    if not isinstance(payload, dict):
        payload = {}
    payload.setdefault("schema_version", "1.0")
    payload.setdefault("project_id", workspace.project.identity.project_id)
    return payload


def _mark_technical_draft() -> None:
    mark_workspace_draft(st.session_state, "ma_technical")


def _render_technical_topic(topic_key: str, label: str, catalog_category: str | None = None) -> None:
    """Shows one technical topic with an explicit not-installed option."""
    catalog = None
    records = ()
    if catalog_category is not None:
        try:
            catalog = load_demo_catalog()
        except FileNotFoundError:
            st.info("Lokale Katalogdaten sind nicht Bestandteil des Repositorys und wurden hier nicht gefunden.")
        except (OSError, ValueError) as exc:
            st.error(f"Lokaler Demo-Katalog konnte nicht geladen werden: {exc}")
        else:
            records = catalog.records_for(catalog_category)
    options = ["not_installed", *[record.record_id for record in records]]
    if not records:
        options.append("present_without_demo_record")
    selected_id = st.selectbox(
        label,
        options,
        format_func=lambda option_id, available_records=records: _technical_option_label(available_records, option_id),
        key=f"technical_topic_{topic_key}",
    )
    selection_key = f"technical_topic_draft_selection_{topic_key}"
    if selected_id == "not_installed":
        st.session_state[selection_key] = {"availability": "not_installed", "topic": topic_key}
        st.dataframe(
            normalize_table_for_streamlit(
                [
                    {"Merkmal": "Status", "Wert": "Nicht vorhanden"},
                    {"Merkmal": "Verfuegbarkeit", "Wert": "not_installed"},
                ]
            ),
            hide_index=True,
            width="stretch",
        )
        return
    if selected_id == "present_without_demo_record":
        st.session_state[selection_key] = {"availability": "planned", "topic": topic_key}
        st.dataframe(
            normalize_table_for_streamlit(
                [
                    {"Merkmal": "Status", "Wert": "Vorhanden, noch ohne Demo-Datensatz"},
                    {"Merkmal": "Verfuegbarkeit", "Wert": "planned"},
                ]
            ),
            hide_index=True,
            width="stretch",
        )
        return

    if catalog is None or catalog_category is None:
        raise RuntimeError("Eine lokale Katalogauswahl braucht einen geladenen Katalog und eine Kategorie.")
    selection = select_demo_record(catalog, category=catalog_category, record_id=selected_id)
    st.session_state[selection_key] = selection
    selected_record = next(record for record in records if record.record_id == selected_id)
    st.warning("Demo-Wert: fachlich nicht verifiziert und nicht simulationsbereit.")
    st.dataframe(
        normalize_table_for_streamlit(_demo_record_rows(selected_record, selection)),
        hide_index=True,
        width="stretch",
    )


def _render_technical_selection_overview() -> None:
    """Displays the session-only choices from the individual technical tabs."""
    topic_labels = {
        "heating": "Heizung",
        "cooling": "Kuehlung",
        "ventilation": "Lueftung",
        "storage": "Speicher",
        "domestic_hot_water": "Trinkwarmwasser",
        "electrical": "Elektrik",
    }
    rows = []
    for topic_key, label in topic_labels.items():
        selection = st.session_state.get(f"technical_topic_selection_{topic_key}")
        if isinstance(selection, CatalogSelection):
            value = selection.label
            status = selection.selection_status
        elif isinstance(selection, dict):
            value = (
                "Nicht vorhanden"
                if selection.get("availability") == "not_installed"
                else "Vorhanden ohne Demo-Datensatz"
            )
            status = str(selection.get("availability"))
        else:
            value = "Noch nicht ausgewaehlt"
            status = "unknown"
        rows.append({"Thema": label, "Auswahl": value, "Status": status})
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")


def _save_technical_selection() -> None:
    """Uebernimmt nur den sichtbaren Sitzungsentwurf, ohne die Ansicht zu verlassen."""
    for topic_key in (
        "heating",
        "cooling",
        "ventilation",
        "storage",
        "domestic_hot_water",
        "electrical",
    ):
        draft_key = f"technical_topic_draft_selection_{topic_key}"
        if draft_key in st.session_state:
            st.session_state[f"technical_topic_selection_{topic_key}"] = st.session_state[draft_key]


def _technical_option_label(records: tuple[DemoCatalogRecord, ...], option_id: str) -> str:
    if option_id == "not_installed":
        return "Nicht vorhanden"
    if option_id == "present_without_demo_record":
        return "Vorhanden, noch ohne Demo-Datensatz"
    return _demo_label(records, option_id)


def _demo_label(records: tuple[DemoCatalogRecord, ...], record_id: str) -> str:
    record = next(record for record in records if record.record_id == record_id)
    return f"{record.label} ({record.record_id})"


def _demo_record_rows(record: DemoCatalogRecord, selection: CatalogSelection) -> list[dict[str, object]]:
    """Keeps the selected record inspectable without exposing it as an editable model."""
    fields = [
        ("ID", record.record_id),
        ("Name", record.label),
        ("Kategorie", record.category),
        ("Auswahlstatus", selection.selection_status),
        ("Pruefstatus", record.data["verification_status"]),
        ("Bestaetigung", record.data["confirmation_status"]),
    ]
    return [{"Merkmal": name, "Wert": value} for name, value in fields]


def _display_value(value) -> str:
    return str(value.value if hasattr(value, "value") else value)


def _structural_validation_label(messages: Sequence[DiagnosticMessage]) -> str:
    """Formuliert eine Strukturpruefung ohne sie als Projektfreigabe auszugeben."""
    if any(message.severity is DiagnosticSeverity.ERROR for message in messages):
        return "blockiert"
    if any(message.severity is DiagnosticSeverity.WARNING for message in messages):
        return "pruefbeduerftig"
    return "fehlerfrei"


def _render_messages(
    messages: Sequence[DiagnosticMessage],
    *,
    structure_only: bool = False,
) -> None:
    rows = [
        {
            "Schwere": message.severity.value,
            "Code": message.code,
            "Meldung": message.message,
            "Fundstelle": message.location,
        }
        for message in messages
    ]
    if not rows:
        st.success("Keine Validierungsmeldungen.")
        return
    if any(row["Schwere"] == DiagnosticSeverity.ERROR.value for row in rows):
        st.error("Fehler blockieren die Strukturpruefung." if structure_only else "Fehler blockieren die Freigabe.")
    elif any(row["Schwere"] == DiagnosticSeverity.WARNING.value for row in rows):
        st.warning(
            "Warnungen benoetigen eine fachliche Strukturpruefung."
            if structure_only
            else "Warnungen benoetigen eine bewusste Freigabeentscheidung."
        )
    else:
        st.info("Nur Informationsmeldungen vorhanden.")
    st.dataframe(normalize_table_for_streamlit(rows), hide_index=True, width="stretch")
