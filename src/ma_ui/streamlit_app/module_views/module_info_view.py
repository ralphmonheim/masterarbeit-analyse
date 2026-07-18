"""Generische Informationsseite fuer Projektmodule ohne eigene Fachansicht."""

from __future__ import annotations

import streamlit as st

from ma_ui.streamlit_app.shared.layout import render_page_header
from ma_workflow import ModuleDefinition, get_module_definition

STATUS_LABELS = {
    "available": "Verfuegbar",
    "partial": "Teilweise umgesetzt",
    "planned": "Geplant",
    "manual": "Manuell / extern",
}

V1_STATUS_MESSAGES = {
    "available": "Der dokumentierte V1-Umfang ist fuer diesen Modulbereich verfuegbar.",
    "partial": (
        "Der dokumentierte V1-Umfang ist nur teilweise umgesetzt. "
        "Massgeblich sind ausschliesslich die sichtbar verfuegbaren Funktionen."
    ),
    "planned": (
        "Der vorgesehene V1-Rahmen ist fachlich noch nicht freigegeben. "
        "Sichtbar verfuegbare Funktionen koennen Demonstrations- oder Uebergangsstand sein."
    ),
    "manual": "Dieser Schritt bleibt in V1 bewusst manuell oder extern.",
}

# Die Erklaerungen bleiben zentral in der Infokarte. Die Fachansichten zeigen
# weiterhin nur ihre Daten und Bedienelemente.
COMMON_INFO_TERMS = (
    (
        "V1-Rahmen",
        "Der fuer die erste Demonstration dokumentierte Umfang; er ist keine Zusage fuer spaetere Ausbaustufen.",
    ),
    ("Freigabestatus", "Ergebnis der technischen Validierung; Fehler blockieren eine Freigabe."),
    ("Annahme", "Bewusst dokumentierte Vereinfachung oder noch nicht verifizierte Eingabe."),
    (
        "Demo- oder Uebergangsstand",
        "Sichtbare Funktion oder Datenstand fuer die Demonstration, nicht automatisch fachlich verifiziert oder produktiv.",
    ),
)

MODULE_INFO_TERMS: dict[str, tuple[tuple[str, str], ...]] = {
    "ma_building": (
        ("Reifegrad (BIL)", "Beschreibt den Informations- und Pruefstand des Gebaeudemodells."),
        ("BIL-0", "2D-Referenzmodell mit Linien, Grundrissen oder Schnitten."),
        ("BIL-1", "Geometrisches Oberflaechenmodell."),
        ("BIL-2", "Objektbasiertes Gebaeudemodell mit Waenden, Daechern, Fenstern und Raeumen."),
        ("BIL-3", "Bauteildefiniertes Architekturmodell mit Typen, Schichten und Materialien."),
        ("BIL-4", "Analysefaehiges Gebaeudemodell mit validierter Geometrie und Pflichtdaten."),
        ("BIL-5", "Koordiniertes Gesamtmodell mit Architektur, Raeumen, Zonierung und gegebenenfalls Technik."),
        (
            "Level of Detail (LoD)",
            "Beschreibt im Projekt den Umfang der Eingabedaten, nicht den CAD-Geometriedetailgrad.",
        ),
        ("LoD-1", "Minimaler Gebaeudeinput: Kubatur, einfache Huellkennwerte, U-Werte und Fensterflaechenanteil."),
        (
            "LoD-2",
            "Strukturierter Gebaeudeinput mit Geschossen, Raeumen oder Zonen, Bauteilen, Oeffnungen, Flaechen und Volumen.",
        ),
        (
            "LoD-3",
            "Vollstaendige Eingabe der fuer die geplante Softwareanalyse benoetigten Raeume, Bauteile und Beziehungen.",
        ),
    ),
    "ma_technical": (
        ("Revision", "Nachvollziehbarer, freigegebener Stand einer technischen Spezifikation."),
        ("Content-Hash", "Pruefsumme des Spezifikationsinhalts zur Erkennung von Aenderungen."),
        (
            "Demo-Auswahl",
            "Synthetische Sitzungsdarstellung; sie ist nicht automatisch fachlich verifiziert oder simulationsbereit.",
        ),
    ),
    "ma_zones": (
        ("Nutzungsprofil", "Zusammenfassung von Nutzungsannahmen wie Betriebszeiten und internen Lasten."),
        ("Demo-Profil", "Synthetische Darstellungsoption, keine normative Nutzungsdefinition."),
    ),
}


def _render_text_list(title: str, values: tuple[str, ...]) -> None:
    if not values:
        return
    st.subheader(title)
    for value in values:
        st.markdown(f"- {value}")


def v1_status_message(status: str) -> str:
    """Erlaeutert den V1-Rahmen ohne Fachreife aus Metadaten abzuleiten."""
    return V1_STATUS_MESSAGES.get(status, "Der aktuelle V1-Umfang ist im Modulkatalog dokumentiert.")


def info_terms(module_key: str) -> tuple[tuple[str, str], ...]:
    """Liefert zentral gepflegte Erklaerungen fuer Begriffe einer Infokarte."""
    return COMMON_INFO_TERMS + MODULE_INFO_TERMS.get(module_key, ())


def _render_v1_frame(module: ModuleDefinition) -> None:
    """Rendert die einheitliche V1-Erlaeuterung aus dem kanonischen Modulkatalog."""
    st.subheader("V1-Rahmen")
    st.info(v1_status_message(module.status))
    st.markdown(f"**Was:** {module.purpose}")

    if module.inputs or module.outputs:
        st.markdown("**Wie:** Das Modul verarbeitet die folgenden Ein- und Ausgaben.")
        input_column, output_column = st.columns(2)
        with input_column:
            _render_text_list("Eingaben", module.inputs)
        with output_column:
            _render_text_list("Ausgaben", module.outputs)

    _render_text_list("Warum der Umfang begrenzt bleibt", module.boundaries)
    st.markdown("**Wann es weitergeht:**")
    st.info(module.next_step)

    terms = info_terms(module.module_key)
    if terms:
        st.subheader("Begriffe in dieser Ansicht")
        for term, explanation in terms:
            st.markdown(f"**{term}:** {explanation}")


def render_module_definition(module: ModuleDefinition) -> None:
    """Zeigt die zentrale Moduldefinition ohne funktionslose Bedienelemente."""
    render_page_header(module.label, module.purpose)
    status_label = STATUS_LABELS.get(module.status, module.status)
    metric_columns = st.columns(3)
    metric_columns[0].metric("Status", status_label)
    metric_columns[1].metric("Bereich", module.category)
    metric_columns[2].metric("Python-Paket", module.python_package or "kein Paket")

    _render_v1_frame(module)
    _render_text_list("Abhaengigkeiten", module.dependencies)


def render(module_key: str) -> None:
    """Laedt und zeigt eine Moduldefinition aus dem zentralen Katalog."""
    render_module_definition(get_module_definition(module_key))
