"""Zentraler Katalog fuer Phasen, Module und Workflow-Schritte."""

from __future__ import annotations

from .models import ModuleDefinition, WorkflowPhase, WorkflowStep

_WORKFLOW_PHASES: tuple[WorkflowPhase, ...] = (
    WorkflowPhase(
        "phase_0",
        "Phase 0 - Technische Plattform",
        0,
        "Gemeinsame technische und organisatorische Grundlage fuer alle Fachphasen.",
    ),
    WorkflowPhase(
        "phase_1",
        "Phase 1 - Projektinitialisierung",
        1,
        "Projekt anlegen, Randbedingungen festlegen und Vorlagen referenzieren.",
    ),
    WorkflowPhase(
        "phase_2",
        "Phase 2 - Eingangsdaten und Pre-Processing",
        2,
        "Gebaeude-, Wetter-, Zonen- und Technikdaten erfassen und vereinheitlichen.",
    ),
    WorkflowPhase(
        "phase_3",
        "Phase 3 - Variantenbildung und Simulationsvorbereitung",
        3,
        "Referenz dimensionieren, Varianten bilden, Run konfigurieren und Export vorbereiten.",
    ),
    WorkflowPhase(
        "phase_4",
        "Phase 4 - Simulation und technische Analyse",
        4,
        "IDA ICE manuell ausfuehren, Ergebnisse importieren und technisch auswerten.",
    ),
    WorkflowPhase(
        "phase_5",
        "Phase 5 - Wirtschaftlichkeit, Nachhaltigkeit und Gesamtbewertung",
        5,
        "Technische, wirtschaftliche und oekologische Ergebnisse bewerten.",
    ),
    WorkflowPhase(
        "phase_6",
        "Phase 6 - Reporting, Datenexport und Dokumentation",
        6,
        "Berichte und Datenpakete erzeugen sowie den Projektstand dokumentieren.",
    ),
)


def _module(
    module_key: str,
    label: str,
    page_key: str,
    status: str,
    category: str,
    purpose: str,
    *,
    inputs: tuple[str, ...] = (),
    outputs: tuple[str, ...] = (),
    boundaries: tuple[str, ...] = (),
    dependencies: tuple[str, ...] = (),
    next_step: str,
    python_package: str | None = None,
) -> ModuleDefinition:
    return ModuleDefinition(
        module_key=module_key,
        label=label,
        page_key=page_key,
        status=status,
        category=category,
        purpose=purpose,
        inputs=inputs,
        outputs=outputs,
        boundaries=boundaries,
        dependencies=dependencies,
        next_step=next_step,
        python_package=python_package,
    )


_MODULE_DEFINITIONS: tuple[ModuleDefinition, ...] = (
    _module(
        "ma_core",
        "Technische Grundlagen",
        "core",
        "planned",
        "infrastructure",
        "Gemeinsame Pfad-, Konfigurations-, Logging-, ID- und Vorlagenregeln bereitstellen.",
        outputs=("technische Grundregeln", "gemeinsame Konfiguration", "Logging-Konventionen"),
        boundaries=("keine Fachberechnungen",),
        next_step="Bestehende gemeinsame Logik inventarisieren und erst danach zentralisieren.",
        python_package="ma_core",
    ),
    _module(
        "ma_database",
        "Datenbank",
        "database",
        "planned",
        "infrastructure",
        "Spaetere moduluebergreifende Persistenz und Datenbankzugriffe kapseln.",
        inputs=("fachliche Datenmodelle",),
        outputs=("persistierte Projektdaten", "Repository-Schnittstellen"),
        boundaries=("bestehende Datenbanklogik in ma_variants bleibt vorerst bestehen",),
        dependencies=("ma_core",),
        next_step="Moduluebergreifenden Persistenzbedarf vor einer Extraktion festlegen.",
        python_package="ma_database",
    ),
    _module(
        "ma_ui",
        "Benutzeroberflaeche",
        "ui",
        "planned",
        "infrastructure",
        "Den Gesamtworkflow, Modulansichten und neutrale Serviceergebnisse in Streamlit darstellen.",
        inputs=("Workflow-Katalog", "neutrale Serviceergebnisse"),
        outputs=("Benutzerauswahl", "Status- und Ergebnisdarstellung"),
        boundaries=("keine Fachlogik",),
        dependencies=("ma_workflow",),
        next_step="Reale Analyseablaeufe pruefen und Modulansichten schrittweise anbinden.",
        python_package="ma_ui",
    ),
    _module(
        "ma_workflow",
        "Workflow-Steuerung",
        "workflow",
        "planned",
        "infrastructure",
        "Phasen, Module, Status und spaetere Serviceaufrufe zentral orchestrieren.",
        inputs=("Projektzustand", "Benutzeraktionen"),
        outputs=("Workflow-Status", "koordinierte Serviceaufrufe"),
        boundaries=("keine Fachberechnung", "keine Darstellung"),
        dependencies=("ma_core",),
        next_step="Katalog schrittweise mit echten Fachservice-Aufrufen verbinden.",
        python_package="ma_workflow",
    ),
    _module(
        "project_documentation",
        "Projektdokumentation",
        "documentation",
        "available",
        "documentation",
        "Planung, Entscheidungen, Architektur, Nachweise und Projektstand nachvollziehbar dokumentieren.",
        inputs=("Projektentscheidungen", "Umsetzungs- und Testergebnisse"),
        outputs=("Plaene", "Entscheidungsprotokolle", "Leitfaden", "Changelog"),
        boundaries=("kein eigenes Python-Paket",),
        next_step="P007 und aktive Teilplaene als kanonische Steuerung pflegen.",
    ),
    _module(
        "ma_project",
        "Projektinitialisierung",
        "project",
        "planned",
        "workflow",
        "Projektstammdaten, Untersuchungsziele, Simulationsprogramme, neutrales Naming und Projektstatus verwalten.",
        inputs=("Projektangaben", "Standardvorlagen", "Simulationsprogrammprofile"),
        outputs=("Projektkonfiguration", "aktives Simulationsprogramm", "Benennungsprofil", "Projektstatus"),
        dependencies=("ma_core",),
        next_step="Datenmodell und minimalen Projektanlage-Workflow planen.",
        python_package="ma_project",
    ),
    _module(
        "ma_building",
        "Gebaeude",
        "building",
        "planned",
        "workflow",
        "Gebaeudemodell, Bauteile und bauphysikalische Randbedingungen verwalten.",
        inputs=("Geometrie", "Bauteile", "Materialkennwerte"),
        outputs=("validierte Gebaeudedaten fuer ma_parameters",),
        boundaries=("keine Zonenprofile", "keine technische Anlagenlogik"),
        dependencies=("ma_project",),
        next_step="Fachlichen Minimalumfang und neutrale Datenmodelle planen.",
        python_package="ma_building",
    ),
    _module(
        "ma_weather",
        "Wetterdaten",
        "weather",
        "partial",
        "workflow",
        "TRY-Datensaetze katalogisieren, importieren, validieren, analysieren und dokumentieren.",
        inputs=("lokale TRY-Dateien", "Wetterkatalog"),
        outputs=("weather_key", "Wetterkennwerte", "Diagramme", "Berichte"),
        boundaries=("keine IDA-Zonenergebnisanalyse",),
        dependencies=("ma_project",),
        next_step="P008: Restdatensaetze real pruefen und weather_key an ma_parameters anbinden.",
        python_package="ma_weather",
    ),
    _module(
        "ma_zones",
        "Zonen",
        "zones",
        "planned",
        "workflow",
        "Thermische Zonen, Nutzungen, Sollwerte, interne Lasten und Profile verwalten.",
        inputs=("Raumdaten", "Nutzungsanforderungen"),
        outputs=("validierte Zonendaten fuer ma_parameters",),
        boundaries=("keine Gebaeudegeometrie", "keine Anlagenberechnung"),
        dependencies=("ma_building",),
        next_step="Zonenmodell und Schnittstelle zu Gebaeude und Technik planen.",
        python_package="ma_zones",
    ),
    _module(
        "ma_technical",
        "Technische Systeme",
        "technical",
        "planned",
        "workflow",
        "Erzeugung, Verteilung, Uebergabe, Regelung und technische Komponenten beschreiben.",
        inputs=("Zonenanforderungen", "System- und Produktdaten"),
        outputs=("validierte Technikdaten fuer ma_parameters",),
        boundaries=("keine Variantenbildung",),
        dependencies=("ma_zones",),
        next_step="Referenzsysteme und technischen Minimalumfang planen.",
        python_package="ma_technical",
    ),
    _module(
        "ma_parameters",
        "Zentrale Parameter",
        "parameters",
        "planned",
        "workflow",
        "Eingaben vereinheitlichen und als einzige fachliche Quelle fuer ma_variants bereitstellen.",
        inputs=("Gebaeude", "Wetter", "Zonen", "Technik", "Dimensionierungsvorschlaege"),
        outputs=("validierte zentrale Parameterliste", "Optionsgruppen", "ausgewaehlte Werte"),
        boundaries=("keine Variantenbildung",),
        dependencies=("ma_building", "ma_weather", "ma_zones", "ma_technical"),
        next_step="Bestehende Parameter- und Optionslogik aus ma_variants inventarisieren.",
        python_package="ma_parameters",
    ),
    _module(
        "ma_analyse.stage_1_dimensioning",
        "Referenzdimensionierung",
        "dimensioning",
        "planned",
        "workflow",
        "Heizlast, Kuehllast und Luftmengen fuer die Referenz fachlich dimensionieren.",
        inputs=("validierte zentrale Parameterliste", "Norm- und Auslegungsannahmen"),
        outputs=("Dimensionierungsvorschlaege fuer die Referenz"),
        boundaries=("keine Variantenbildung", "keine Ergebnisanalyse der Simulationslaeufe"),
        dependencies=("ma_parameters",),
        next_step="Fachlichen Minimalumfang und belastbare Referenzfaelle planen.",
        python_package="ma_analyse.stage_1_dimensioning",
    ),
    _module(
        "ma_analyse",
        "Analyse-Grundlagen",
        "analysis_core",
        "partial",
        "workflow",
        "Gemeinsame Services, Datenzugriffe, Diagramme und Exporte fuer die Analysestufen bereitstellen.",
        inputs=("standardisierte Simulationsergebnisse", "Projekt- und Variantenmetadaten"),
        outputs=("Kennwerte", "Diagramme", "Tabellen", "Analyseberichte"),
        boundaries=("keine Kosten- oder Nachhaltigkeitsrechnung",),
        dependencies=("ma_import_simulation",),
        next_step="Gemeinsame Analysefunktionen stabil halten und ueber die Stufenplaene weiterentwickeln.",
        python_package="ma_analyse",
    ),
    _module(
        "ma_analyse.stage_2_optimization",
        "Analyse Stufe 2 - Optimierung",
        "analyse",
        "partial",
        "workflow",
        "Varianten mit vorhandenen Energie-, Leistungs-, Komfort- und Zeitreihenanalysen vergleichen.",
        inputs=("standardisierte Simulationsergebnisse", "Varianten- und Raumwahl"),
        outputs=("Variantenvergleiche", "Optimierungshinweise", "Diagramme und Tabellen"),
        boundaries=("kein Norm-Nachweis", "keine Sensitivitaetsbewertung"),
        dependencies=("ma_analyse", "ma_import_simulation"),
        next_step="P019: vorhandene Befehle zu einem dokumentierten Optimierungsablauf buendeln.",
        python_package="ma_analyse.stage_2_optimization",
    ),
    _module(
        "ma_analyse.stage_3_standards_compliance",
        "Analyse Stufe 3 - Norm-Nachweis",
        "standards_compliance",
        "planned",
        "workflow",
        "Varianten gegen nachvollziehbare deutsche und spaeter internationale Normenprofile pruefen.",
        inputs=("Analysekennwerte", "Normenprofil", "Projekt- und Nutzungsrandbedingungen"),
        outputs=("ComplianceReport", "Pass/Fail/Warnung/Not-evaluable je Nachweis"),
        boundaries=("keine ungeprueften Grenzwerte", "keine allgemeine Modellvalidierung"),
        dependencies=("ma_analyse.stage_2_optimization",),
        next_step="P020: deutsche Normen, Ausgaben, Abschnitte und Berechnungsmethoden recherchieren.",
        python_package="ma_analyse.stage_3_standards_compliance",
    ),
    _module(
        "ma_analyse.stage_4_sensitivity",
        "Analyse Stufe 4 - Sensitivitaet",
        "sensitivity",
        "planned",
        "workflow",
        "Robustheit und Parametereinfluss fuer kritische Wetter- und Betriebsfaelle untersuchen.",
        inputs=("Wetterereignisse", "Varianten", "Zeitfenster", "Parameterstudien"),
        outputs=("Sensitivitaetsvergleiche", "kritische Zeitraeume", "Robustheitshinweise"),
        boundaries=("keine vollstaendige probabilistische Risikoanalyse",),
        dependencies=("ma_weather", "ma_analyse.stage_2_optimization"),
        next_step="P021: Wetterereigniserkennung mit vorhandenen Tages- und Wochenanalysen verbinden.",
        python_package="ma_analyse.stage_4_sensitivity",
    ),
    _module(
        "ma_variants",
        "Varianten",
        "variants",
        "planned",
        "workflow",
        "Variantenraum, Regeln, Generierung, Auswahl und Benennung verwalten.",
        inputs=("zentrale Parameterliste aus ma_parameters", "Benennungsprofil aus ma_project"),
        outputs=("Varianten", "Variantenwerte", "Auswahlmengen", "Variantenmetadaten"),
        boundaries=("keine direkte Abhaengigkeit von Eingabefachmodulen", "kein Simulationssetup"),
        dependencies=("ma_parameters",),
        next_step="Bestehenden Kern stabil halten und spaetere Extraktionen getrennt planen.",
        python_package="ma_variants",
    ),
    _module(
        "ma_simulation_setup",
        "Simulation konfigurieren",
        "simulation_setup",
        "planned",
        "workflow",
        "Run, Variantenmenge, Zeitraum, Zeitschritt, Ausgabeintervall und Szenario festlegen.",
        inputs=("ausgewaehlte Varianten", "Projekt- und Wetterreferenzen"),
        outputs=("validierte Run- und Simulationskonfiguration"),
        boundaries=("keine Variantenbildung", "keine Simulationsdateibearbeitung"),
        dependencies=("ma_variants",),
        next_step="Run-Modell, IDs und Standard-Jahressimulation planen.",
        python_package="ma_simulation_setup",
    ),
    _module(
        "ma_export_simulation",
        "Simulationsexport",
        "export_simulation",
        "planned",
        "workflow",
        "Varianten und Run-Konfiguration programmunabhaengig fuer Simulationsadapter vorbereiten.",
        inputs=("Varianten", "Run-Konfiguration", "Referenzmodell", "Parametermapping"),
        outputs=("Exportpaket", "Run-Manifest", "Adapterartefakte"),
        boundaries=("kein Simulationsstart", "keine ungesicherte IDM-Manipulation"),
        dependencies=("ma_variants", "ma_simulation_setup"),
        next_step="P009: vorhandenen Basisexport einbinden und IDA-ICE-Adapter planen.",
        python_package="ma_export_simulation",
    ),
    _module(
        "ida_ice",
        "IDA ICE",
        "ida_ice",
        "manual",
        "external",
        "Externe Simulationsumgebung fuer den manuellen Simulationslauf.",
        inputs=("IDA-ICE-Exportpaket",),
        outputs=("Simulationsergebnisse", "Simulationsmeldungen"),
        boundaries=("kein Python-Paket dieses Projekts",),
        dependencies=("ma_export_simulation",),
        next_step="Manuellen Ablauf und erforderliche Ergebnisdateien dokumentieren.",
    ),
    _module(
        "ma_import_simulation",
        "Simulationsergebnisimport",
        "import_simulation",
        "planned",
        "workflow",
        "Ergebnisdateien programmunabhaengig erkennen, zuordnen und vereinheitlichen.",
        inputs=("Simulationsergebnisse", "Run- und Variantenmetadaten"),
        outputs=("standardisierte Ergebnisdaten fuer ma_analyse",),
        boundaries=("keine fachliche Ergebnisbewertung",),
        dependencies=("ma_export_simulation",),
        next_step="IDA-ICE-Adaptergrenze und bestehende Importlogik inventarisieren.",
        python_package="ma_import_simulation",
    ),
    _module(
        "ma_economy",
        "Wirtschaftlichkeit",
        "economy",
        "planned",
        "workflow",
        "Investitions-, Betriebs-, Lebenszyklus- und Prozesskosten bewerten.",
        inputs=("technische Kennwerte", "Kosten", "Preise", "Lebensdauern", "Arbeitszeiten"),
        outputs=("wirtschaftliche Vergleichsergebnisse",),
        boundaries=("keine Nachhaltigkeits- oder Gesamtbewertung",),
        dependencies=("ma_analyse",),
        next_step="Bestehende Wirtschaftlichkeitslogik inventarisieren und Zielumfang planen.",
        python_package="ma_economy",
    ),
    _module(
        "ma_sustainability",
        "Nachhaltigkeit",
        "sustainability",
        "planned",
        "workflow",
        "Betriebliche und spaeter graue Umweltwirkungen von Varianten bewerten.",
        inputs=("Energiekennwerte", "Emissionsfaktoren", "Produkt- und Materialdaten"),
        outputs=("CO2-, GWP- und Nachhaltigkeitsergebnisse",),
        boundaries=("keine Wirtschaftlichkeits- oder Gesamtbewertung",),
        dependencies=("ma_analyse",),
        next_step="Systemgrenzen, Datenquellen und Minimalumfang festlegen.",
        python_package="ma_sustainability",
    ),
    _module(
        "ma_assessment",
        "Gesamtbewertung",
        "assessment",
        "planned",
        "workflow",
        "Technische, wirtschaftliche und oekologische Ergebnisse aggregieren und bewerten.",
        inputs=("Analyse-", "Economy- und Sustainability-Ergebnisse", "Gewichtungen"),
        outputs=("Scores", "Rankings", "Pareto-Loesungen", "Entscheidungsvorlagen"),
        boundaries=("keine primaere Fachberechnung", "keine Berichtserzeugung"),
        dependencies=("ma_analyse", "ma_economy", "ma_sustainability"),
        next_step="Bewertungsregeln und Umgang mit Pareto-/Scoring-Verfahren planen.",
        python_package="ma_assessment",
    ),
    _module(
        "ma_reporting",
        "Reporting",
        "reporting",
        "planned",
        "workflow",
        "Menschlich lesbare Berichte, Factsheets und Ergebnisdarstellungen erzeugen.",
        inputs=("Analyse- und Bewertungsergebnisse", "Berichtsvorlagen"),
        outputs=("Berichte", "Factsheets", "Abbildungen"),
        boundaries=("keine primaere Berechnung", "keine Datenpaketierung"),
        dependencies=("ma_assessment",),
        next_step="Vorhandene Reportfunktionen inventarisieren und zentrale Vorlagen planen.",
        python_package="ma_reporting",
    ),
    _module(
        "ma_data_export",
        "Datenexport",
        "data_export",
        "planned",
        "workflow",
        "Maschinenlesbare Ergebnisdaten auswaehlen, paketieren und archivieren.",
        inputs=("fachmodulspezifische Exporte", "Projektmetadaten"),
        outputs=("CSV-, JSON-, Excel- und Archivpakete"),
        boundaries=("fachmodulspezifische Exporte bleiben in den Fachmodulen",),
        dependencies=("ma_reporting",),
        next_step="Zentrale Paketformate und Auswahlregeln planen.",
        python_package="ma_data_export",
    ),
    _module(
        "ma_validation",
        "Zentrale Validierung",
        "validation",
        "planned",
        "cross_cutting",
        "Lokale Pruefergebnisse sammeln und moduluebergreifende Freigaben verwalten.",
        inputs=("lokale Validierungsberichte", "Workflow-Zustand"),
        outputs=("Freigabestatus", "blockierende Fehler", "Warnungen"),
        boundaries=("Fachregeln bleiben in den Fachmodulen",),
        dependencies=("ma_workflow",),
        next_step="Gemeinsames Validierungsergebnis und Freigabestufen planen.",
        python_package="ma_validation",
    ),
    _module(
        "ma_feedback",
        "Feedback und Rueckspruenge",
        "feedback",
        "planned",
        "cross_cutting",
        "Auffaelligkeiten klassifizieren und Rueckspruenge in verantwortliche Module steuern.",
        inputs=("Fehler", "Warnungen", "Analyse- und Bewertungsergebnisse"),
        outputs=("Ruecksprungziel", "Korrekturauftrag", "dokumentierte Iteration"),
        boundaries=("keine automatische Aenderung von Fachmoduldaten",),
        dependencies=("ma_validation", "ma_workflow"),
        next_step="Problemtypen und Ruecksprungregeln planen.",
        python_package="ma_feedback",
    ),
)

MODULE_KEY_ALIASES = {
    "ma_export_ida": "ma_export_simulation",
    "ma_import_ida": "ma_import_simulation",
    "ma_analyse.stage_3_verification": "ma_analyse.stage_3_standards_compliance",
}

STEP_KEY_ALIASES = {
    "analyse": "optimization",
    "export_ida": "export_simulation",
    "import_ida": "import_simulation",
    "ida_export": "export_simulation",
    "ida_import": "import_simulation",
    "stage_3_verification": "standards_compliance",
    "verification": "standards_compliance",
}


def _phase_label(phase_key: str) -> str:
    for phase in _WORKFLOW_PHASES:
        if phase.phase_key == phase_key:
            return phase.label
    if phase_key == "cross_cutting":
        return "Phasenuebergreifend"
    raise KeyError(f"Unbekannte Workflow-Phase: {phase_key}")


def _step(
    step_key: str,
    label: str,
    phase_key: str,
    module_key: str,
    description: str,
    *,
    is_cross_cutting: bool = False,
    is_external: bool = False,
) -> WorkflowStep:
    module = get_module_definition(module_key)
    return WorkflowStep(
        step_key=step_key,
        label=label,
        phase=_phase_label(phase_key),
        module_key=module.module_key,
        status=module.status,
        description=description,
        phase_key=phase_key,
        is_cross_cutting=is_cross_cutting,
        is_external=is_external,
    )


def resolve_module_key(module_key: str) -> str:
    """Loest historische Modulschluessel auf den kanonischen Schluessel auf."""
    return MODULE_KEY_ALIASES.get(module_key, module_key)


def get_module_definition(module_key: str) -> ModuleDefinition:
    """Findet ein Modul einschliesslich dokumentierter Uebergangsaliase."""
    canonical_key = resolve_module_key(module_key)
    for module in _MODULE_DEFINITIONS:
        if module.module_key == canonical_key:
            return module
    raise KeyError(f"Unbekanntes Projektmodul: {module_key}")


_WORKFLOW_STEPS: tuple[WorkflowStep, ...] = (
    _step("core", "Technische Grundlagen", "phase_0", "ma_core", "Gemeinsame technische Regeln bereitstellen."),
    _step("database", "Datenbank", "phase_0", "ma_database", "Persistenz und Datenbankgrenzen vorbereiten."),
    _step("ui", "Benutzeroberflaeche", "phase_0", "ma_ui", "Zentrale Streamlit-Oberflaeche bereitstellen."),
    _step("workflow", "Workflow-Steuerung", "phase_0", "ma_workflow", "Phasen und Modulstatus orchestrieren."),
    _step(
        "documentation_infrastructure",
        "Dokumentationsinfrastruktur",
        "phase_0",
        "project_documentation",
        "Planungs-, Architektur- und Entscheidungsstruktur bereitstellen.",
    ),
    _step("project", "Projekt initialisieren", "phase_1", "ma_project", "Projekt und Untersuchungsrahmen anlegen."),
    _step("building", "Gebaeudedaten", "phase_2", "ma_building", "Gebaeudemodell und Bauteile erfassen."),
    _step("weather", "Wetterdaten", "phase_2", "ma_weather", "TRY- und Standortdaten aufbereiten."),
    _step("zones", "Zonendaten", "phase_2", "ma_zones", "Zonen, Nutzungen und Profile festlegen."),
    _step("technical", "Technische Systeme", "phase_2", "ma_technical", "Referenzsysteme und Technikdaten erfassen."),
    _step("parameters", "Parameter vereinheitlichen", "phase_2", "ma_parameters", "Zentrale Parameterliste erzeugen."),
    _step(
        "dimensioning",
        "Referenz dimensionieren",
        "phase_3",
        "ma_analyse.stage_1_dimensioning",
        "Stage 1 fuer Heizlast, Kuehllast und Luftmengen vorbereiten.",
    ),
    _step("variants", "Varianten bilden", "phase_3", "ma_variants", "Varianten erzeugen, auswaehlen und benennen."),
    _step(
        "simulation_setup",
        "Simulation konfigurieren",
        "phase_3",
        "ma_simulation_setup",
        "Run und gemeinsame Simulationskonfiguration festlegen.",
    ),
    _step(
        "export_simulation",
        "Simulationsexport vorbereiten",
        "phase_3",
        "ma_export_simulation",
        "Programmunabhaengiges Exportpaket und IDA-ICE-Adapterartefakte erzeugen.",
    ),
    _step(
        "simulation",
        "IDA ICE simulieren",
        "phase_4",
        "ida_ice",
        "Simulation manuell in IDA ICE ausfuehren.",
        is_external=True,
    ),
    _step(
        "import_simulation",
        "Simulationsergebnisse importieren",
        "phase_4",
        "ma_import_simulation",
        "Ergebnisdateien zuordnen und vereinheitlichen.",
    ),
    _step(
        "optimization",
        "Analyse Stufe 2 - Optimierung",
        "phase_4",
        "ma_analyse.stage_2_optimization",
        "Varianten mit vorhandenen Analysewerkzeugen vergleichen und Optimierungspotenziale bestimmen.",
    ),
    _step(
        "standards_compliance",
        "Analyse Stufe 3 - Norm-Nachweis",
        "phase_4",
        "ma_analyse.stage_3_standards_compliance",
        "Varianten anhand versionierter Normenprofile nachvollziehbar nachweisen.",
    ),
    _step(
        "sensitivity",
        "Analyse Stufe 4 - Sensitivitaet",
        "phase_4",
        "ma_analyse.stage_4_sensitivity",
        "Kritische Wetterfaelle, Robustheit und Parametereinfluss untersuchen.",
    ),
    _step("economy", "Wirtschaftlichkeit bewerten", "phase_5", "ma_economy", "Kosten und Prozessaufwand bewerten."),
    _step(
        "sustainability",
        "Nachhaltigkeit bewerten",
        "phase_5",
        "ma_sustainability",
        "Umweltwirkungen und Nachhaltigkeitskennwerte bewerten.",
    ),
    _step("assessment", "Gesamtbewertung", "phase_5", "ma_assessment", "Ergebnisse aggregieren und Vorzugsvarianten bestimmen."),
    _step("reporting", "Berichte erzeugen", "phase_6", "ma_reporting", "Berichte und Factsheets erzeugen."),
    _step("data_export", "Daten exportieren", "phase_6", "ma_data_export", "Maschinenlesbare Datenpakete erstellen."),
    _step(
        "documentation_archive",
        "Dokumentieren und archivieren",
        "phase_6",
        "project_documentation",
        "Projektstand, Entscheidungen und Ergebnisse archivieren.",
    ),
    _step(
        "validation",
        "Zentrale Validierung",
        "cross_cutting",
        "ma_validation",
        "Lokale Pruefergebnisse sammeln und Phasenfreigaben verwalten.",
        is_cross_cutting=True,
    ),
    _step(
        "feedback",
        "Feedback und Rueckspruenge",
        "cross_cutting",
        "ma_feedback",
        "Probleme klassifizieren und Iterationen in verantwortliche Module steuern.",
        is_cross_cutting=True,
    ),
)


def list_workflow_phases() -> tuple[WorkflowPhase, ...]:
    """Gibt Phase 0 und die sechs fachlichen Phasen in Reihenfolge zurueck."""
    return _WORKFLOW_PHASES


def list_module_definitions() -> tuple[ModuleDefinition, ...]:
    """Gibt alle fachlichen, technischen und dokumentarischen Module zurueck."""
    return _MODULE_DEFINITIONS


def list_workflow_steps() -> tuple[WorkflowStep, ...]:
    """Gibt alle Workflow- und Querschnittsschritte zurueck."""
    return _WORKFLOW_STEPS


def resolve_step_key(step_key: str) -> str:
    """Loest historische Workflow-Schluessel auf."""
    return STEP_KEY_ALIASES.get(step_key, step_key)


def get_workflow_step(step_key: str) -> WorkflowStep:
    """Findet einen Workflow-Schritt einschliesslich Uebergangsaliase."""
    canonical_key = resolve_step_key(step_key)
    for step in _WORKFLOW_STEPS:
        if step.step_key == canonical_key:
            return step
    raise KeyError(f"Unbekannter Workflow-Schritt: {step_key}")


def steps_by_phase() -> dict[str, tuple[WorkflowStep, ...]]:
    """Gruppiert Workflow-Schritte nach kanonischem Phasenschluessel."""
    return {
        phase.phase_key: tuple(step for step in _WORKFLOW_STEPS if step.phase_key == phase.phase_key)
        for phase in _WORKFLOW_PHASES
    }


def list_cross_cutting_steps() -> tuple[WorkflowStep, ...]:
    """Gibt phasenuebergreifende Validierungs- und Feedbackschritte zurueck."""
    return tuple(step for step in _WORKFLOW_STEPS if step.is_cross_cutting)
