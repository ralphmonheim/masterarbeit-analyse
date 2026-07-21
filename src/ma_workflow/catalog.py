"""Zentraler Katalog fuer Phasen, Module und Workflow-Schritte."""

from __future__ import annotations

from .models import ModuleDefinition, WorkflowPhase, WorkflowStep

_WORKFLOW_PHASES: tuple[WorkflowPhase, ...] = (
    WorkflowPhase(
        "pre_process",
        "Pre-Process",
        0,
        "Projekt, Wetter, Gebaeude, Technik, Zonen, Parameter, Referenzdimensionierung, Varianten und Simulation-Setup.",
    ),
    WorkflowPhase(
        "main_process",
        "Main-Process",
        1,
        "Simulationsexport, manueller Simulationslauf und Ergebnisimport.",
    ),
    WorkflowPhase(
        "post_process",
        "Post-Process",
        2,
        "Daten vorbereiten, analysieren, bewerten, berichten und exportieren.",
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
        outputs=("technische Grundregeln", "InputSource", "IDs", "Sitzungslogs"),
        boundaries=("keine Fachberechnungen",),
        next_step="P010-Vertraege in P011 bis P015 fachmodulweise anwenden.",
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
        next_step="Startseite als Moduluebersicht leicht halten und Workflow-Referenz nur in ma_workflow pflegen.",
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
        next_step="P027-Checkpoints, Reloads und Abbrueche fuer P017 schrittweise an echte Fachservices anbinden.",
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
        "Projektidentitaet, Untersuchungsrahmen, Simulationsprogramme und neutrales Naming ohne fachlichen Projektstatus verwalten.",
        inputs=("Projektangaben", "Standardvorlagen", "Simulationsprogrammprofile"),
        outputs=("ProjectContext", "aktive Simulationsprogrammreferenz", "Benennungsprofil"),
        dependencies=("ma_core",),
        next_step="P011-S1b als separaten Pfad- und Persistenzvertrag mit Speicherort- und Ignore-Gate abgrenzen.",
        python_package="ma_project",
    ),
    _module(
        "ma_building",
        "Gebaeude",
        "building",
        "partial",
        "workflow",
        "Gebaeudemodell, Bauteile und bauphysikalische Randbedingungen verwalten.",
        inputs=("BuildingModelSpecification", "BusinessIntegration-LoD-1", "SmallOffice-IFC", "Rhino-Testgebaeude"),
        outputs=("validierbare Demo-Gebaeudedaten", "LoD-1-Huellkennwerte", "strukturierte Quelldiagnosen"),
        boundaries=("kein produktiver IFC-/Rhino-Import", "keine Zonenprofile", "keine technische Anlagenlogik"),
        dependencies=("ma_project",),
        next_step="LoD-2-Raum-/Bauteilumfang klaeren und IFC-Lite-Umfang getrennt freigeben.",
        python_package="ma_building",
    ),
    _module(
        "ma_weather",
        "Wetterdaten",
        "weather",
        "available",
        "workflow",
        "TRY-Datensaetze katalogisieren, importieren, validieren, analysieren und dokumentieren.",
        inputs=("lokale TRY-Dateien", "Wetterkatalog"),
        outputs=("weather_key", "Wetterkennwerte", "Diagnosen", "Freigabestatus", "Berichte"),
        boundaries=("keine IDA-Zonenergebnisanalyse",),
        dependencies=("ma_project",),
        next_step="P008: Reale Wetterdatensaetze pruefen, P021-Ereignisdefinition schaerfen und Freshness-Abgleich fuer ma_parameters vorbereiten.",
        python_package="ma_weather",
    ),
    _module(
        "ma_zones",
        "Zonen",
        "zones",
        "partial",
        "workflow",
        "Zonen, Nutzungen, Profile, Konditionierung und zonenbezogene Uebergabe verwalten.",
        inputs=("freigegebene Gebaeude-/Raumdaten", "zentrale technische Systemreferenzen", "Nutzungsanforderungen"),
        outputs=(
            "validierte Zonendaten fuer ma_parameters",
            "ReleasedZoneHandover als payloadfreier Referenzcheckpoint",
            "zonenbezogene Uebergabe- und Betriebszuordnungen",
        ),
        boundaries=(
            "keine Gebaeudegeometrie",
            "keine zentralen Erzeugungsanlagen",
            "keine automatische Zonenbildung im MVP",
        ),
        dependencies=("ma_building", "ma_technical"),
        next_step="P015-S3b-Werteherkunft und P032-W3a Technik-Zonen-Richtung jeweils als getrennten Council-Slice abgrenzen.",
        python_package="ma_zones",
    ),
    _module(
        "ma_technical",
        "Technische Systeme",
        "technical",
        "partial",
        "workflow",
        "Zentrale technische Systeme, Kreise, Anlagen und generische technische Datensaetze beschreiben.",
        inputs=("freigegebene Gebaeudedaten", "einfache Referenzsystemannahmen"),
        outputs=("validierte LoD-1-Technikdaten fuer ma_parameters", "zentrale Systemreferenzen fuer ma_zones"),
        boundaries=("keine Variantenbildung", "keine zonenbezogene Uebergabekonfiguration", "keine Produktdatenbank"),
        dependencies=("ma_building",),
        next_step="P014-S4-Persistenz/YAML und eine v2-Werteherkunft nur in getrennt freigegebenen Folgeslices behandeln.",
        python_package="ma_technical",
    ),
    _module(
        "ma_parameters",
        "Zentrale Parameter",
        "parameters",
        "partial",
        "workflow",
        "Eingaben vereinheitlichen, Parameter-/Optionskataloge besitzen und als stabile fachliche Quelle fuer ma_variants bereitstellen.",
        inputs=("Gebaeude", "Wetter", "Zonen", "Technik", "ReferenceDimensioningResult"),
        outputs=(
            "validierter ParameterSnapshot v1",
            "ParameterInputPackage",
            "BaselineParameterSnapshot",
            "ParameterVariationSpecification",
        ),
        boundaries=("keine Variantenbildung",),
        dependencies=("ma_weather", "ma_building", "ma_technical", "ma_zones"),
        next_step="P015-S3b-Werteherkunft und den verbleibenden Vollumfang nach dem abgeschlossenen P013-/P014-Checkpoint getrennt abgrenzen.",
        python_package="ma_parameters",
    ),
    _module(
        "ma_analyse.stage_1_dimensioning",
        "Referenzdimensionierung",
        "dimensioning",
        "partial",
        "workflow",
        "Heizlast, Kuehllast und Luftmengen fuer die Referenz fachlich dimensionieren.",
        inputs=("validierter ParameterSnapshot v1", "Norm- und Auslegungsannahmen"),
        outputs=("LoD-1-Referenzdimensionierung", "ReferenceDimensioningResult", "Dimensionierungshinweise"),
        boundaries=(
            "keine Variantenbildung",
            "kein normatives Lastverfahren",
            "keine Ergebnisanalyse der Simulationslaeufe",
        ),
        dependencies=("ma_parameters",),
        next_step="VariantVerification-Anfragen ueber ma_workflow und spaetere IDA-Plausibilisierung planen.",
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
        "ma_analyse.data_preparation",
        "Datenvorbereitung",
        "data_preparation",
        "partial",
        "workflow",
        "Importierte Simulationsergebnisse in nutzbare Raumtabellen und Basisberichte ueberfuehren.",
        inputs=("standardisierte Simulationsergebnisse", "IDA-Rohdatenvarianten"),
        outputs=("aufbereitete Raumtabellen", "Basisbericht", "Excel-Datenuebersicht"),
        boundaries=("keine Variantenoptimierung", "kein Norm-Nachweis", "keine Sensitivitaetsbewertung"),
        dependencies=("ma_analyse", "ma_import_simulation"),
        next_step="Prepare und analyze-data als gemeinsamen Datenvorbereitungsschritt fachlich buendeln.",
        python_package="ma_analyse.data_preparation",
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
        dependencies=("ma_analyse.data_preparation",),
        next_step="P019: vorhandene Analysebefehle nach der Datenvorbereitung zu einem dokumentierten Optimierungsablauf buendeln.",
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
        "Variantenraum, Verifikation, Katalog, Auswahl, Generierung und Benennung verwalten.",
        inputs=(
            "BaselineParameterSnapshot",
            "ReferenceDimensioningResult",
            "ParameterVariationSpecification",
            "Benennungsprofil aus ma_project",
        ),
        outputs=("VariantSpace", "VariantVerification", "VariantCatalog", "VariantSelection", "VariantGeneration"),
        boundaries=("keine direkte Abhaengigkeit von Eingabefachmodulen", "kein Simulationssetup"),
        dependencies=("ma_parameters",),
        next_step="P017-S1: Grundobjekte, IDs, VariantSpace, Zaehlmodell und stabile Eingangsreferenzen planen.",
        python_package="ma_variants",
    ),
    _module(
        "ma_simulation_setup",
        "Simulation konfigurieren",
        "simulation_setup",
        "planned",
        "workflow",
        "Neutrales Run-Paket mit Manifest, Setup, Variantenartefakten und technischen Logs fuer erzeugte Varianten vorbereiten.",
        inputs=("vollstaendige Varianten nach VGEN", "VariantSelection", "Projekt- und Wetterreferenzen"),
        outputs=("RunManifest", "SimulationSetup", "RUN-ID", "direkte RUN -> VAR-Zuordnung", "technische Logs"),
        boundaries=(
            "keine Variantenbildung",
            "keine Simulationsdateibearbeitung",
            "keine wissenschaftliche Zeitmessung",
        ),
        dependencies=("ma_variants",),
        next_step="P018-S1: Neutrale Modelle, Status und YAML-Schemas fuer das Run-Paket umsetzen.",
        python_package="ma_simulation_setup",
    ),
    _module(
        "ma_export_simulation",
        "Simulationsexport",
        "export_simulation",
        "planned",
        "workflow",
        "Varianten und Run-Konfiguration programmunabhaengig fuer Simulationsadapter vorbereiten.",
        inputs=("VariantGeneration", "RunManifest", "Referenzmodell", "Parametermapping"),
        outputs=("Exportpaket", "Run-Manifest", "Adapterartefakte"),
        boundaries=("kein Simulationsstart", "keine ungesicherte IDM-Manipulation"),
        dependencies=("ma_variants", "ma_simulation_setup"),
        next_step="P009 nach P018 ueber RUN-ID und VAR-ID weiterfuehren.",
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
        inputs=("Simulationsergebnisse", "RUN-ID", "VAR-ID", "Run-Manifest"),
        outputs=("standardisierte Ergebnisdaten fuer ma_analyse",),
        boundaries=("keine fachliche Ergebnisbewertung",),
        dependencies=("ma_export_simulation",),
        next_step="P009-MVP: Manuell bereitgestellte Ergebnisdateien neutral ueber RUN-ID und VAR-ID zuordnen.",
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
        next_step="P027-Checkpoints fuer VSP, VVER, VCAT, VSEL und VGEN an Freigabeentscheidungen anbinden.",
        python_package="ma_validation",
    ),
    _module(
        "ma_feedback",
        "Feedback und Rueckspruenge",
        "feedback",
        "planned",
        "cross_cutting",
        "Auffaelligkeiten klassifizieren und Rueckspruenge in verantwortliche Module steuern.",
        inputs=("Fehler", "Warnungen", "Analyse- und Bewertungsergebnisse", "P017-Checkpointstatus"),
        outputs=("Ruecksprungziel", "Reload- oder Abort-Entscheidung", "dokumentierte Iteration"),
        boundaries=("keine automatische Aenderung von Fachmoduldaten",),
        dependencies=("ma_validation", "ma_workflow"),
        next_step="P027-Problemtypen, Reload-Regeln und Abbruchgrenzen fuer Variantenlaeufe ausarbeiten.",
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
    "analyze-data": "data_preparation",
    "analyze_data": "data_preparation",
    "prepare": "data_preparation",
    "prepare_data": "data_preparation",
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
    _step("core", "Technische Grundlagen", "cross_cutting", "ma_core", "Gemeinsame technische Regeln bereitstellen."),
    _step("database", "Datenbank", "cross_cutting", "ma_database", "Persistenz und Datenbankgrenzen vorbereiten."),
    _step("ui", "Benutzeroberflaeche", "cross_cutting", "ma_ui", "Zentrale Streamlit-Oberflaeche bereitstellen."),
    _step(
        "workflow",
        "Workflow-Steuerung",
        "cross_cutting",
        "ma_workflow",
        "Phasen, Modulstatus und P017-Checkpoints orchestrieren.",
    ),
    _step(
        "documentation_infrastructure",
        "Dokumentationsinfrastruktur",
        "cross_cutting",
        "project_documentation",
        "Planungs-, Architektur- und Entscheidungsstruktur bereitstellen.",
    ),
    _step("project", "Projekt initialisieren", "pre_process", "ma_project", "Projekt und Untersuchungsrahmen anlegen."),
    _step("weather", "Wetterdaten", "pre_process", "ma_weather", "TRY- und Standortdaten aufbereiten."),
    _step("building", "Gebaeudedaten", "pre_process", "ma_building", "Gebaeudemodell und Bauteile erfassen."),
    _step(
        "technical",
        "Technische Systeme",
        "pre_process",
        "ma_technical",
        "Referenzsysteme, Grenzen und Technikdaten erfassen.",
    ),
    _step("zones", "Zonendaten", "pre_process", "ma_zones", "Zonen, Nutzungen, Profile und lokale Uebergabe festlegen."),
    _step(
        "parameters",
        "Parameter vereinheitlichen",
        "pre_process",
        "ma_parameters",
        "Eingangspaket, BaselineParameterSnapshot und ParameterVariationSpecification vorbereiten.",
    ),
    _step(
        "dimensioning",
        "Referenz dimensionieren",
        "pre_process",
        "ma_analyse.stage_1_dimensioning",
        "ReferenceDimensioningResult fuer Referenz und spaetere VariantVerification bereitstellen.",
    ),
    _step(
        "variants",
        "Varianten bilden",
        "pre_process",
        "ma_variants",
        "VariantSpace, Verification, Catalog, Selection und Generation fuehren.",
    ),
    _step(
        "simulation_setup",
        "Simulation konfigurieren",
        "pre_process",
        "ma_simulation_setup",
        "Neutrales Run-Paket mit direkter RUN-zu-VAR-Zuordnung und technischen Logs vorbereiten.",
    ),
    _step(
        "export_simulation",
        "Simulationsexport vorbereiten",
        "main_process",
        "ma_export_simulation",
        "Exportpaket nach RunManifest mit RUN-ID und VAR-ID vorbereiten.",
    ),
    _step(
        "simulation",
        "IDA ICE simulieren",
        "main_process",
        "ida_ice",
        "Simulation manuell in IDA ICE ausfuehren.",
        is_external=True,
    ),
    _step(
        "import_simulation",
        "Simulationsergebnisse importieren",
        "main_process",
        "ma_import_simulation",
        "Ergebnisdateien ueber RUN-ID und VAR-ID zuordnen und vereinheitlichen.",
    ),
    _step(
        "data_preparation",
        "Daten vorbereiten",
        "post_process",
        "ma_analyse.data_preparation",
        "Prepare und analyze-data fuer die nutzbare Analysebasis ausfuehren.",
    ),
    _step(
        "optimization",
        "Analyse Stufe 2 - Optimierung",
        "post_process",
        "ma_analyse.stage_2_optimization",
        "Varianten mit vorhandenen Analysewerkzeugen vergleichen und Optimierungspotenziale bestimmen.",
    ),
    _step(
        "standards_compliance",
        "Analyse Stufe 3 - Norm-Nachweis",
        "post_process",
        "ma_analyse.stage_3_standards_compliance",
        "Varianten anhand versionierter Normenprofile nachvollziehbar nachweisen.",
    ),
    _step(
        "sensitivity",
        "Analyse Stufe 4 - Sensitivitaet",
        "post_process",
        "ma_analyse.stage_4_sensitivity",
        "Kritische Wetterfaelle, Robustheit und Parametereinfluss untersuchen.",
    ),
    _step("economy", "Wirtschaftlichkeit bewerten", "post_process", "ma_economy", "Kosten und Prozessaufwand bewerten."),
    _step(
        "sustainability",
        "Nachhaltigkeit bewerten",
        "post_process",
        "ma_sustainability",
        "Umweltwirkungen und Nachhaltigkeitskennwerte bewerten.",
    ),
    _step(
        "assessment",
        "Gesamtbewertung",
        "post_process",
        "ma_assessment",
        "Ergebnisse aggregieren und Vorzugsvarianten bestimmen.",
    ),
    _step("reporting", "Berichte erzeugen", "post_process", "ma_reporting", "Berichte und Factsheets erzeugen."),
    _step("data_export", "Daten exportieren", "post_process", "ma_data_export", "Maschinenlesbare Datenpakete erstellen."),
    _step(
        "documentation_archive",
        "Dokumentieren und archivieren",
        "post_process",
        "project_documentation",
        "Projektstand, Entscheidungen und Ergebnisse archivieren.",
    ),
    _step(
        "validation",
        "Zentrale Validierung",
        "cross_cutting",
        "ma_validation",
        "Lokale Pruefergebnisse und P017-Checkpointfreigaben verwalten.",
        is_cross_cutting=True,
    ),
    _step(
        "feedback",
        "Feedback und Rueckspruenge",
        "cross_cutting",
        "ma_feedback",
        "Probleme klassifizieren und Reloads oder Abbrueche in verantwortliche Module steuern.",
        is_cross_cutting=True,
    ),
)


def list_workflow_phases() -> tuple[WorkflowPhase, ...]:
    """Gibt die drei sichtbaren Prozessphasen in Reihenfolge zurueck."""
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
