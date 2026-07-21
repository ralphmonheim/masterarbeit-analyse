"""Varianten-Seite der zentralen Streamlit-Oberflaeche."""

from __future__ import annotations

import streamlit as st

from ma_parameters import (
    build_business_integration_lod1_baseline_parameter_snapshot,
    load_reference_variation_specification,
)
from ma_ui.streamlit_app.shared import normalize_table_for_streamlit, render_configuration_return
from ma_variants import (
    build_variant_workflow,
    catalog_rows,
    generate_selected_variants,
    rule_rows,
    select_catalog_candidates,
)


def render() -> None:
    """Zeigt den fachlichen P017-Ablauf aus der freigegebenen Referenz."""
    st.title("Varianten")
    st.caption("Verifizierter Variantenraum aus der freigegebenen Parameter-Referenz")
    render_configuration_return()

    try:
        baseline = build_business_integration_lod1_baseline_parameter_snapshot()
        specification = load_reference_variation_specification(baseline)
        workflow = build_variant_workflow(baseline, specification)
    except Exception as exc:  # noqa: BLE001 - UI stellt fachliche Aufbaufehler dar.
        st.error(f"Variantenraum konnte nicht aufgebaut werden: {exc}")
        return

    st.info(
        f"Baseline: {baseline.snapshot_id} | Variationsspezifikation: {specification.specification_id}"
    )
    metric_columns = st.columns(4)
    metric_columns[0].metric("Freie Bereiche", len({item.module_key for item in specification.unlocked_dimensions}))
    metric_columns[1].metric("Variationsdimensionen", len(specification.unlocked_dimensions))
    metric_columns[2].metric("Regeln", len(workflow.rules))
    metric_columns[3].metric("Verifizierte Varianten", len(workflow.catalog.candidates))

    tabs = st.tabs(["Variationsraum", "Regeln", "Variantenkatalog", "Auswahl", "Generierung"])

    with tabs[0]:
        st.caption("VSP: Kandidaten entstehen nur aus den in Parameter freigegebenen Dimensionen.")
        st.dataframe(
            normalize_table_for_streamlit(
                [
                    {
                        "Dimension": dimension.label,
                        "Scope": dimension.scope_id,
                        "Werte": ", ".join(option.label for option in dimension.options),
                        "Kopplung": dimension.coupling_key or "-",
                    }
                    for dimension in specification.unlocked_dimensions
                ]
            ),
            hide_index=True,
            width="stretch",
        )

    with tabs[1]:
        st.caption("Regeln werden in Fachmodulen definiert, hier gesammelt und in VVER angewendet.")
        st.dataframe(normalize_table_for_streamlit(rule_rows(workflow.rules)), hide_index=True, width="stretch")
        for rule in workflow.rules:
            with st.expander(rule.title):
                st.write(rule.details)
                st.caption(f"Geltung: {rule.scope_type} {rule.scope_id} | Quellmodul: {rule.owner_module}")

    with tabs[2]:
        st.caption(
            f"VCAT: {len(workflow.candidates)} Kandidaten, {workflow.catalog.rejected_count} ausgeschlossen, "
            f"{len(workflow.catalog.candidates)} verifiziert."
        )
        st.dataframe(normalize_table_for_streamlit(catalog_rows(workflow.catalog)), hide_index=True, width="stretch")

    candidate_ids = [candidate.candidate_id for candidate in workflow.catalog.candidates]
    with tabs[3]:
        selected_ids = st.multiselect(
            "Varianten fuer die Generierung waehlen",
            options=candidate_ids,
            default=candidate_ids[:1],
            key="p017_selected_variant_ids",
        )
        selection = select_catalog_candidates(workflow.catalog, tuple(selected_ids))
        st.caption(f"VSEL: {len(selection.candidate_ids)} Varianten aus {selection.catalog_id} ausgewaehlt.")

    with tabs[4]:
        selected_ids = tuple(st.session_state.get("p017_selected_variant_ids", candidate_ids[:1]))
        selection = select_catalog_candidates(workflow.catalog, selected_ids)
        if st.button("Ausgewaehlte Varianten generieren", type="primary"):
            st.session_state["p017_generated_variants"] = generate_selected_variants(
                baseline,
                workflow.catalog,
                selection,
            )
        generated = st.session_state.get("p017_generated_variants", ())
        st.caption("VGEN erzeugt nur die ausgewaehlten vollstaendigen Varianten; die Baseline bleibt unveraendert.")
        st.dataframe(
            normalize_table_for_streamlit(
                [
                    {
                        "VAR-ID": variant.variant_id,
                        "Bezeichnung": variant.label,
                        "Baseline": variant.baseline_snapshot_id,
                        "Aenderungen": len(variant.values),
                        "Fingerprint": variant.fingerprint,
                    }
                    for variant in generated
                ]
            ),
            hide_index=True,
            width="stretch",
        )
