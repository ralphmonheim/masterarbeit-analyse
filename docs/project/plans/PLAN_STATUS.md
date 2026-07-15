# Plan Status

Stand: 2026-07-15

Diese Datei ist die aktive Planungsuebersicht. Sie wird nach Modulen gefuehrt und nach jeder Planumsetzung aktualisiert. Vollstaendige alte Planstaende liegen unter `docs/project/archive/plans/`.

## Projektorganisation

### Abgeschlossen

- Projektweites Compliance-System angelegt: `docs/compliance/` trennt
  gemeinsame, IDA-/EQUA-, DIN-/Nautos-/VDE-/VDI- und DWD-Regeln.
  `ma_core.compliance`
  setzt Metadaten-Preflight, Gruen-Gelb-Rot-/Unknown-Entscheidung, sichere
  Operationswrapper, Datenbereinigung und datensparsames JSONL-Audit um. Der
  DWD-TRY-2011-Konverter ist als erster produktiver Adapter gegatet.
- P003 Projektstruktur, Planungsbereich und Nutzerentscheidungen: modulare Dokumentationsstruktur, Planindex, Strukturreview, Cleanup-Plan, Implementierungshinweise und getrennter Bereich fuer Nutzerentscheidungen wurden vorbereitet. Betroffen: `docs/project/`, `docs/ma_analyse/`, `docs/ma_variants/`, `docs/ma_weather/`, `docs/common/`.
- `docs/project/archive/plans/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md` ist nach Umsetzung archiviert.
- `docs/project/archive/plans/250603_Plan_Variantenmodul_GUI_Logikpruefung.md` ist nach Abschluss von P001 archiviert.
- `docs/project/archive/plans/PLAN_Projektplan_Version_1_0_0.md` ist ein abgelegter Plan und nicht mehr die aktive Steuerdatei.
- `data/test_output/` bleibt ein lokaler, semi-wichtiger Arbeits- und Smoke-Test-Ordner. Der Nutzer leert ihn regelmaessig manuell.
- `docs/examples/plot_template_analyse/` bleibt die belastbare Referenzgalerie fuer aktuelle `ma_analyse`-Plot-Template-Beispiele; `docs/examples/plot_template_weather/` fuehrt Wetter-Template-Beispiele getrennt.
- Der leere, nicht versionierte Ordner `scripts/` wurde entfernt.
- `docs/project/UPDATE_ROUTINES.md` dokumentiert die festen Codex-Routinen `update repo`, `direkt update repo` und `update planung`.
- `docs/project/UPDATE_ROUTINES.md` dokumentiert zusaetzlich `tagesstart`, `tagesende`, `tagesende direkt`, `wochenabschluss`, `projektlage`, `plan aufnehmen`, `entscheidung festhalten` und `release check`.
- `docs/project/weekly_reviews/` ist als Ablage fuer Wochenzusammenfassungen vorbereitet.
- Der alte leere Root-Dokumentenordner wurde entfernt; Produkt- und Materialdatenblaetter liegen aktiv unter `data/catalogs/documents/`.
- Nutzerentscheidung dokumentiert: Website- und Portfolio-Chats werden von der Masterarbeits-Entscheidungsanalyse ausgeschlossen.
- Nutzerentscheidung dokumentiert: Echte Produkt-, Material- und Datenbankinhalte werden nicht ins Git-Repo uebernommen; versioniert werden Struktur und klar gekennzeichnete Beispieldaten.
- Nutzerentscheidung dokumentiert: Relative/absolute Cooling-Logik bleibt vorerst nur in Plot-Templates; Hauptportal und regulaerer `cooling`-Befehl werden erst nach Abschluss der Diagrammbearbeitung erneut geprueft.
- Nutzerentscheidungen aus P005 dokumentiert: `ma_parameters` ersetzt `ma_input`, `ma_ui` und `ma_workflow` werden getrennte Zielmodule, `ma_analyse`-Fachlogik bleibt in `ma_analyse`, IDA-Export/-Import, Simulation-Setup, Assessment und Feedback werden getrennt geplant.
- Nutzerentscheidungen aus P005 ergaenzt: Streamlit ist Zieltechnik fuer den
  aktuellen `ma_ui`-Haupteinstieg; Tkinter bleibt technisch getrennt und wird
  nicht mit Streamlit vermischt; `ma_analyse` soll langfristig eine
  UI-neutrale Service-Schnittstelle erhalten.
- Nutzerentscheidungen aus P005 verschaerft: `ma_simulation_setup` liegt zwischen Varianten und IDA-Export; die Tkinter-GUI dient als fachliche Ablaufvorlage, nicht als technische Streamlit-Vorlage; `ma_ui` zielt auf Dashboard, Workflow-Views, Shared-Komponenten und Module-Views.
- Nutzerentscheidungen zu den naechsten Strukturpunkten dokumentiert:
  Tkinter-Vorschau soll ueber einen temporaeren Vorschau-/Cachebereich laufen,
  freie Overlay-Datenreihen sollen flexibel aus der Datenbasis geladen werden
  koennen, und Wetterdiagramme bleiben fachlich im Modul `ma_weather`.
- Nutzerentscheidung dokumentiert: Normierungsfragen wie absolute Werte oder flaechenbezogene Werte `[W/m2]` sollen spaeter nicht nur fuer die Energiebilanz, sondern `ma_analyse`-weit fuer passende Auswertungen geplant werden.
- Nutzerentscheidung dokumentiert: `ma_economy` und `ma_sustainability` werden als eigene Zielmodule geplant; `ma_assessment` bleibt als Bewertungs-, Scoring- und Berichtsschicht ueber Analyse, Economy und Sustainability bestehen.
- Historische P005-Entscheidung dokumentiert: `ma_economy`,
  `ma_sustainability` und `ma_assessment` wurden dem damaligen Post-Process
  zugeordnet. P007 ersetzt diese aktive Gliederung durch Phase 5 und einen
  phasenuebergreifenden Feedback-Bereich.
- Leitfaden-Versionierung eingefuehrt: alte Leitfadenfassungen liegen unter
  `docs/project/archive/leitfaeden/`; Version 0.3.7 wurde vor der
  Strukturueberarbeitung unveraendert archiviert. Die aktive Fassung ist
  `MASTERARBEIT_LEITFADEN.md` Version 0.5.3 mit acht festen Hauptbereichen.
- Methodische Untersuchungsdimension aufgenommen: manuellen, softwareunterstuetzten und automatisierten Prozessaufwand nach aktiver Arbeitszeit, Maschinenlaufzeit, Fehlerkorrektur und Wissensstand vergleichen; konkrete Messmethode bleibt offen.
- Vollstaendigen Modulkatalog in den Leitfaden aufgenommen: Zweck, Eingaben, Ausgaben, Abgrenzung und Status sind fuer bestehende und geplante Module dokumentiert.
- Miro-Workflow-Diagramm v0.1.1 als historischen Ist-Entwurf analysiert; die
  korrigierte Zuordnung von `ma_economy`, `ma_sustainability` und
  `ma_assessment` ist im Aenderungsreview dokumentiert. Original-JPG und
  Review liegen versioniert unter `docs/project/architecture/workflow/`.
- Ersetzte Workflow-Fassung v0.1.0 mit Grafik und Review nach
  `docs/project/archive/workflow/` verschoben; v0.1.1 bleibt als
  Diagrammreferenz erhalten, wird strukturell aber durch P007 uebersteuert.
- Routine `aktualisieren` um einen belegbaren Modulstatusabgleich erweitert;
  Streamlit-Navigation, Workflow-Karten, Kennzahlen und Detailtabellen leiten
  ihre Statuswerte zentral aus `src/ma_workflow/catalog.py` ab;
  `actions.py` bleibt Kompatibilitaetszugriff.
- Aktuellen fachlichen Modulstand abgeglichen:
  - verfuegbar: Projektdokumentation;
  - teilweise: `ma_weather`, `ma_analyse`,
    `ma_analyse.data_preparation` und
    `ma_analyse.stage_2_optimization`;
  - geplant: alle weiteren Software- und Fachmodule einschliesslich
    vorhandener Gerueste und Prototypen;
  - manuell: IDA ICE.
- P005 Phase 1/2 dokumentiert: `ma_analyse`-Bestandsanalyse und Service-Schnittstellenentwurf liegen unter `docs/project/architecture/`.
- P002, P005 und P006 wurden unveraendert archiviert. P007 ist die
  verbindliche strukturelle Grundlage; P008 bis P028 konkretisieren
  fachliche, Demo-, Konzept-, Research- und Querschnittsarbeiten.
- Phase 0 und die sechs P007-Hauptphasen sind im zentralen Workflow-Katalog
  abgebildet. `ma_validation` und `ma_feedback` werden phasenuebergreifend
  gefuehrt.
- Fehlende Zielmodule sind als leichte importierbare Pakete und dokumentierte
  Infoseiten vorbereitet. Paketexistenz aendert den fachlichen Status nicht.
- Alle 28 katalogisierten Komponenten besitzen einen dokumentierten
  Modulsteckbrief; jede Dashboard-Karte oeffnet eine Fachansicht, eine
  Infoseite oder einen klar gekennzeichneten externen Schritt.

### Aktiver Rahmenplan

- P007 ist als verbindlicher Rahmenplan fuer die weitere VS-Code-Umsetzung
  aufgenommen. Die beschriebene Modulstruktur wurde nach Bestandsanalyse als
  leichtes Geruest umgesetzt; Fachstatus und bestehende Logik bleiben davon
  unberuehrt.
- Vor jeder Umsetzung aus P007 gilt die feste Reihenfolge Analyse, Planung,
  Freigabe, Umsetzung, Test und Dokumentation.
- Die P007-Bestandsanalyse und Strukturkonsolidierung sind abgeschlossen.
  Weitere Fachlogik, Migrationen oder Verschiebungen brauchen weiterhin
  getrennte Teilplaene und Freigaben.
- `ma_export_simulation` und `ma_import_simulation` sind die kanonischen
  allgemeinen Schnittstellenmodule. IDA ICE wird ueber Adapter angebunden;
  historische IDA-spezifische Schluessel bleiben nur als Uebergangsaliase.
- Phase 0 und die sechs P007-Hauptphasen ersetzen die bisherige aktive
  Vierer-Gliederung im Workflow und Dashboard.
- Paketexistenz allein aendert keinen Modulstatus von `planned` oder `partial`
  auf `available`.
- Der Katalogstatus beschreibt den fachlichen Reifegrad im
  Masterarbeitsworkflow. Vorhandener Prototypcode allein aendert ein Modul
  nicht von `planned` auf `partial`.

### Aktive Teilplaene

- P008 fuehrt `ma_weather` als konsolidierter Gesamtplan weiter:
  Standort-/Referenzstandortlogik, eigener Dateiimport,
  Status- und Importnachweis, offene Wetterdatensaetze, bewusste Aktivierung,
  Projekt-Default, Jahr-/Sommer-/Winterdatensatztypen, kritische
  Wetterereignisse, vereinfachte Pruefansicht, ortsgenaue
  TRY-Standorterkennung mit optionaler PLZ-Aufloesung und dokumentierte
  Uebergabegrenze zu `ma_parameters`.
- P010 ist umgesetzt und archiviert. Formatneutrale Eingabequellen,
  strukturierte Diagnosen, Freigaberegeln, IDs und append-only Sitzungslogs
  sind am TRY-Wetterimport erprobt.
- P027 begleitet alle Fachslices mit UI-, Workflow-, Validierungs- und
  Feedbackregeln.
- P027 ergaenzt die Vereinheitlichung von Template-Befehlen fuer Ausgabemodule
  wie `ma_analyse` und `ma_weather`; in der Tkinter-Analyse soll der erste
  Befehlsschritt `plot-template-analyse` als Default gesetzt werden.
- Der erste Tkinter-Analyse-Slice ist umgesetzt: die Befehlsauswahl startet
  jetzt standardmaessig mit `plot-template`; der Wetter-Template-Befehl folgt
  im naechsten Slice.
- P028 ist als erster gemeinsamer Streamlit-Slice umgesetzt und archiviert:
  freie Simulationsprogrammlisten, neutrale Varianten-Benennungsprofile,
  Demo-Optionsauswahl und gemeinsamer Sitzungsstand von `ma_project`,
  `ma_parameters` und `ma_variants` sind vorhanden.
- Der P028-Vorlagenschutz verhindert Aenderungen an versionierten Vorlagen.
  Eigene Dateien werden lokal gespeichert; kollidierende neue Dateinamen
  muessen geaendert werden. YAML bleibt nur der erste Schreibadapter.
- P011 ist als Projektidentitaet und spaetere digitale Projektakte
  konsolidiert. Quellenwahl bleibt nach P010 beim jeweiligen Fachmodul;
  `ma_project` erzeugt weder fachliche Freigaben noch Modellreferenzregister.
  P011-S1a stellt immutable Projektmodelle und reine Serialisierung ohne
  Persistenz, Assets, UI oder Naming-Pfadmigration bereit. P011-S1b bleibt
  ein eigener Pfad-, Speicherort- und Ignore-Gate-Scope.
- P009 bleibt bis zum validierten `RunManifest` aus P018 zurueckgestellt. Der
  vorhandene Basisexport in `ma_variants.ida_export` wird spaeter
  wiederverwendet, nicht dupliziert.
- P009 ist auf die P017/P018-Schnittstelle nachgezogen: Export und Import
  sollen ueber `RUN-ID + VAR-ID` zuordnen; `CASE-ID` und `SimulationCase`
  werden nicht als neue Hauptobjekte eingefuehrt.
- Direkte IDM-Manipulation, erfundene IDA-Befehle, automatischer
  Simulationsstart, Batch-Ausfuehrungen und Simulationsserver-Nutzung bleiben
  bis zu einer ausdruecklichen schriftlichen EQUA-Freigabe ausgeschlossen;
  `docs/compliance/ida_ice/` ist die verbindliche Vorpruefung.

### Modulplanserie P011 bis P028

- Eingabekette bis `ma_simulation_setup`: P011 bis P018.
- Analyse Stufe 2 Optimierung: P019 auf Basis vorhandener Befehle.
- Analyse Stufe 3 Norm-Nachweis: P020 unter dem kanonischen Namen
  `ma_analyse.stage_3_standards_compliance`; deutsche Normen zuerst,
  internationale Profile spaeter. Die technische Compliance-Vorpruefung ist
  vorhanden. Der Frankfurt-UAS-Nautos-Zugang ist fuer manuelle Recherche und
  Lektuere belegt; produktive Normlogik sowie DIN-/VDE-/VDI-KI-Verarbeitung
  bleiben bis zur bestaetigten Rechte- und Quellenpruefung gesperrt.
- Analyse Stufe 4 Sensitivitaet: P021 mit kritischen Wetterereignissen statt
  ausschliesslicher Jahresbetrachtung.
- Economy und Sustainability: P022 und P023 als kleine Demos mit
  vollstaendigem Fachkonzept.
- Assessment, Reporting und Datenexport: P024 bis P026 zunaechst
  konzeptuell.
- Gemeinsamer Projekt-, Parameter- und Naming-Slice: P028 ist als Demo
  umgesetzt; produktive Projektstammdaten und `ParameterSnapshot` folgen ueber
  P011 und P015.
- P012 ist mit dem ergaenzenden `ma_building`-Fachkonzept aktualisiert:
  `BuildingModelSpecification`, einfache Demo, lokale aktuelle
  IFC-Arbeitsdatei als Trainings-/Diagnosebasis, Reifegrade, Raumregister,
  Bauteile, Oeffnungen, Validierung und Schnittstellen zu `ma_zones`,
  `ma_parameters`, `ma_assessment` und `ma_export_simulation` sind geplant.
  IFC-Lite bleibt bis zur Analyse konkreter IFC-Arbeitsstaende offen; Rhino
  und direkte CAD-Integration bleiben Ausbaupfade ohne aktuelle
  Implementierungszusage.
- P012 v1 ist umgesetzt: `ma_building` enthaelt eine versionierte
  Demo-`BuildingModelSpecification`, einfache Fachmodelle, Validierung nach
  `ma_validation`, lokale IFC-Entity-Diagnose, 3DM-Metadatendiagnose,
  vorbereitete lokale Arbeitsdatenordner und eine Streamlit-Pruefansicht.
- P012-Referenzen getrennt: Fuer den fachlichen Teil wird lokal
  `SmallOffice_d_IFC2x3.ifc` als IDA-ICE-IFC-Referenzmodell verwendet; fuer
  BusinessIntegration und Softwaretests dient das Rhino-Testgebaeude
  `ma_building_testgebaeude_6x4x4_oeffnungen_v1.3dm` als Arbeitsreferenz.
  Verbindliche Softwarestruktur bleibt die kleine
  `BuildingModelSpecification`.
- P012-S2 ist umgesetzt: BusinessIntegration-LoD-1 liegt als versionierte
  `BuildingModelSpecification` vor. LoD beschreibt den Eingabeumfang; LoD-1
  enthaelt Kubatur, einfache Huellkennwerte, U-Werte, Fensteranteil und
  Annahmen, aber keine Raeume, Einzelfenster oder Host-Beziehungen.
- P013-S1 ist umgesetzt: `ma_zones` enthaelt eine versionierte
  BusinessIntegration-LoD-1-Zonenspezifikation mit einer Gesamtgebaeudezone,
  einfachem Buero-Nutzungsprofil, Sollwerten, internen Lasten,
  Betriebszeiten, Validierung und Streamlit-Pruefansicht.
- P013-S2 ist fachlich konsolidiert: Der bisherige Kurzplan wurde durch das
  Gesamtkonzept `ma_zones` ersetzt. Verbindlich festgehalten sind die
  Reihenfolge `ma_weather -> ma_building -> ma_technical -> ma_zones ->
  ma_validation -> ma_parameters`, das allgemeine Zonenobjekt, vollstaendige
  Raum-Zonen-Zuordnung im MVP, keine Raumteilung, getrennte
  Normprofilfassungen 2018/2025, Zeitprofile, Feiertagslogik,
  zonenbezogene Uebergabesysteme, Parameter-/Variantenregeln und offene
  Fachentscheidungen fuer Sonderhohlraeume, paralleles Heizen/Kuehlen,
  Prozentbedeutung, LoD-1-Variantenparameter und DIN-Datenabbildung.
- P013-S3b und P013-S3c sind umgesetzt: `ThermalBuildingModel` prueft die
  vollstaendige Raum-Zonen-Zuordnung gegen Building und Zone. Der darauf
  aufbauende payloadfreie `ReleasedZoneHandover` bindet kanonisch den
  vollstaendigen Zonenstand, Zuordnungen, Building-ID/-Revision und das
  P014-Modell-/Revisions-/Hash-Triple; er gibt keine Fachnutzlast weiter.
- P014-S1 ist umgesetzt und bleibt als Legacy-v1-Vertrag kompatibel:
  `ma_technical` enthaelt eine versionierte BusinessIntegration-LoD-1/Lite-
  Technikspezifikation mit einfachen Referenzannahmen fuer Heizung, Kuehlung
  und Lueftung, Validierung und Streamlit-Pruefansicht. Das parallele v2-Modell
  ist fachlich konsolidiert: Ziel sind zentrale Technik, typisierte Fachfelder,
  Serviceinterfaces statt direkter Zonenreferenzen, Revisionen/Branches und
  manuelle Bearbeitung. Die vorbereitenden Slices 0/1 legen Schutzgrenzen und
  v2-Kerntypen an. P014-S1.1 buendelt nun Geraete, Verteilungen, Speicher und
  Trinkwarmwassererzeugung im v2-Aggregat; Plant, AHU und Elektrik sind
  optional. P014-S1.2 validiert die v2-Struktur und Referenzen getrennt vom
  Legacy-v1-Vertrag; P014-S2 speichert erfolgreich validierte Modelle als
  ueberschreibgeschuetzte, hashgesicherte Revisionen. Die Technikansicht bietet
  getrennte Reiter fuer Heizung, Kuehlung, Lueftung, Speicher,
  Trinkwarmwasser und Elektrik. Jeder Reiter erlaubt `Nicht vorhanden`;
  Materialien und Konstruktionen bleiben in `ma_building`. Optionale lokale
  Katalogwerte bleiben `demo_unverified`, werden nicht versioniert oder
  veroeffentlicht und duerfen nicht in Revisionen, Parameter, Varianten oder
  Runs uebernommen werden. Die UI bleibt ohne lokale Katalogdateien nutzbar.
  P014-S3a liefert einen referenz-only Handover aus einer freigegebenen,
  hashkonsistenten v2-Revision an nachgelagerte Module. Zusammen mit P013-S3c
  ist daraus ein separat validierter P013-/P014-Checkpoint fuer P015 entstanden.
  Offen bleiben die v2-Werteherkunft und der Vollumfang von P015-S3b; v1-Demo,
  IDA-Adapter, Export, Templates und automatische Dimensionierung bleiben
  ausserhalb dieses Umfangs.
- Preprocess V1 ist als verbindlicher erster Durchstich festgelegt:
  Projekt- und Eingabequellen, freigegebene Baseline, Referenzdimensionierung,
  kleine Variantenstudie und ein neutrales, validiertes Run-Paket bilden den
  Umfang. P018 fuehrt getrenntes Setup, Variantenkonfigurationen,
  Simulationseingaben und technische Logs. Die Uebergabe an IDA ICE bleibt
  manuell und folgt der P018-Compliance-Grenze; P009 folgt mit einem kleinen
  neutralen Ergebnis-Postprocess erst nach stabilem Run-Paket. P014 beginnt
  dafuer mit der Vollstaendigkeit des
  v2-Aggregats und seiner Referenzen, vor Serialisierung, Branches oder einem
  Editor.
- P015-S1 ist umgesetzt: `ma_parameters` enthaelt `ParameterSnapshot`,
  `ParameterValue` und `ParameterSourceReference`, baut einen validierten
  BusinessIntegration-LoD-1-`ParameterSnapshot` v1 aus `ma_building`,
  `ma_zones` und `ma_technical` und zeigt ihn in Streamlit mit Quellen,
  Einheiten und Freigabestatus. Snapshot-Speicherung, Wetteruebernahme,
  manuelle Aenderungsnachweise, P013-S2-Zonenstand und
  Stage-1-Folgesnapshots bleiben Folgearbeit.
- P015-S2 ist umgesetzt: `ma_parameters` leitet aus dem vorhandenen
  `ParameterSnapshot` v1 einen `BaselineParameterSnapshot` v2 mit
  `parameter_value_id`, Scope-Typen, Parameterklassen, Variierbarkeit,
  erweiterten Quellenreferenzen, Referenzversionen, Content-Hash,
  Freigabe- und Aktualitaetsstatus ab. Streamlit zeigt den Baseline-v2-Stand
  in einer eigenen Pruefansicht.
- P015-S3a ist umgesetzt: `ma_parameters` fuehrt ein
  `ParameterInputPackage` als Eingangspaket-Checkpoint ein, uebernimmt den
  aktivierten und freigegebenen Projekt-Default aus `ma_weather` als
  Wetterquelle und blockiert fehlende, nicht aktivierte oder nicht
  freigegebene Wetterstaende. Streamlit zeigt das Eingangspaket getrennt von
  Snapshot v1 und Baseline v2.
- P015-S3b-prep ist umgesetzt: Ein freigegebener `ReleasedTechnicalHandover`
  aus P014 wird additiv in eine echte technische `ParameterSourceReference`
  mit Modell-ID, Revisions-ID, Content-Hash und Freigabestatus ueberfuehrt.
  Bestehende v1-Parameterwerte und das P015-S3a-Eingangspaket bleiben dabei
  unveraendert.
- P013-S3c/P015-S3b-T2 ist umgesetzt: `ParameterInputPackage` und
  `BaselineParameterSnapshot` fuehren opt-in getrennte
  `checkpoint_references` fuer genau ein passendes, freigegebenes und aktuelles
  P013-/P014-Paar. Sie sind keine Wertquellen; der Baseline-Content-Hash bindet
  ihre Referenz-Content-Hashes und fehlende, nicht freigegebene oder veraltete
  Checkpoints blockieren nur diesen neuen Checkpointmodus.
- P015 ist fachlich konsolidiert: Zielbild sind
  `BaselineParameterSnapshot`, `ReferenceDimensioningResult` und
  `ParameterVariationSpecification` mit Scopes, Parameterklassen,
  Variationsmodell, Status/Freshness, Persistenz und stabilem Handover an
  `ma_variants`. Der P013-/P014-Anschluss und sein Referenzcheckpoint sind
  umgesetzt. Offen bleiben die v2-basierte Werteherkunft und der verbleibende
  P015-S3b-Vollumfang; beide brauchen einen getrennten Folgeslice.
- P016-S1 ist umgesetzt: `ma_analyse.stage_1_dimensioning` berechnet aus dem
  validierten `ParameterSnapshot` v1 eine LoD-1-Referenzdimensionierung mit
  Transmissions-Heizlast, Lueftungs-Heizlast, Gesamt-Heizlast, Mindest-
  Luftvolumenstrom, interner Kuehllastannahme, Rechenweg und Hinweisen.
  Normverfahren, IDA-Plausibilisierung und Folgesnapshot bleiben Folgearbeit.
- P016 ist auf P017 vorbereitet: Stage 1 bleibt frei von Variantenbildung,
  soll aber spaeter `DimensioningRequest`-Gruppen aus `VariantVerification`
  ueber `ma_workflow` beantworten koennen.
- P017 ist fachlich konsolidiert: aktive erste Ausbaustufe ist
  `VariantSpace -> VariantVerification -> VariantCatalog ->
  VariantSelection -> VariantGeneration -> ma_simulation_setup`.
  `VCAT` ist auf 500 Eintraege begrenzt, `VSEL` nutzt zuerst `all`,
  `manual` und `random`, `SimulationCase` und `CASE` entfallen.
- P018 ist als neutrales Run-Paket konsolidiert: `ma_simulation_setup`
  uebernimmt vollstaendig erzeugte Varianten nach `VGEN`, ergaenzt ein
  getrenntes gemeinsames Setup je Run, materialisiert neutrale
  Variantenartefakte und fuehrt direkte `RUN -> VAR`-Zuordnungen. P018 schreibt
  nur technische Logs.
- P030 ist als externe Forschungsschicht geplant: Es erfasst manuelle und
  logbasierte Pre-, Simulations- und Postprocessing-Zeiten getrennt,
  vergleicht Prozessmodi und beeinflusst keine produktiven Fachobjekte.
- P031 ordnet das repo-lokale Codex Project Operating System ohne neue
  Parallelwahrheiten: Der Plan buendelt Audit, Konfliktregister,
  Capability-Snapshot und Backlog; `AGENTS.md`, `.codex/`,
  `UPDATE_ROUTINES.md`, Decisions und Compliance behalten getrennte
  Eigentuemerschaft. Zwei duenne Skills und ein Contract-Test bilden die
  lokale Baseline. Graphify, neue MCPs, globale Konfiguration, Hook-
  Aenderungen, Obsidian/Zotero und geschuetzte PDF-/IDA-Verarbeitung bleiben
  gesperrt oder manuell freizugeben. UD-089 delegiert nur klar abgegrenzte,
  lokale und reversible Folgeslices nach dokumentierter Council-Mehrheit;
  Rechte-, externe und irreversible Gates bleiben konkret freizugeben.
- P032 dokumentiert den professionellen Architektur-Benchmark als datierten
  Snapshot unter `docs/project/architecture/reviews/2026-07-15/`. ADR-P032
  ist mit der konservativen Konsolidierung der bestehenden `ma_*`-Pakete
  angenommen; bis zum MVP gilt das Workspace-Betriebsmodell und
  `ma_parameters` besitzt die Parameter-/Optionskataloge. P032-W0, der
  additive Guardrail-Slice W1a und der reine Code-Owner-Transfer W2a sind
  abgeschlossen: lokaler Wheel-Smoke, aktuelle README-Pfade,
  Katalog-Ignore-Defense, Importcontracts und identitaetsgleiche
  Legacy-Reexports sind nachgewiesen. Die Katalog-Defaultpfade bleiben
  unveraendert unter `config/ma_variants/`; W2b und alle weiteren Wellen
  brauchen einen exakten Council-Mehrheitsbeschluss nach UD-089. Externe Tools
  und Sondergates bleiben weiterhin getrennt.
- Masterarbeits-MVP V1 ist der uebergeordnete erste Nutzennachweis: von
  Projekt- und Eingabeaufnahme ueber Baseline, Varianten und neutrales
  Run-Paket bis zu manueller Simulation, neutraler Ergebnisaufnahme, drei
  Diagrammtypen und P030-Prozessvergleich. Preprocess V1 bleibt darin der
  erste Teilmeilenstein bis zum freigegebenen Run-Paket.
- Der Handover-Abgleich liefert jetzt `ThermalBuildingModel` und den
  payloadfreien `ReleasedZoneHandover`; P016/`ma_analyse` definieren drei
  `OutputRequirementProfiles`. P018 referenziert die Vertraege, ohne ihre
  Fachlogik zu duplizieren.
- P027 begleitet P017 mit Checkpoints fuer `VSP`, `VVER`, `VCAT`, `VSEL`
  und `VGEN`, Reload-/Abort-Logik und der technischen
  Dimensionierungsunterbrechung innerhalb von `VVER`.
- Nutzerentscheidung UD-066 festgehalten: DWG bleibt im aktuellen
  Masterarbeitsumfang lokale ungepruefte CAD-Quelle; ein produktiver
  DWG-Parser oder DWG-Importadapter wird nicht aufgebaut.

### Teilweise umgesetzt

- P005 Architektur-Slice umgesetzt: Zielarchitektur und UI-Auslagerungsreview liegen unter `docs/project/architecture/`.
- P005 ordnet den Workflow als Pre-Process, Simulation, Post-Process und Feedback ein.
- P005 bewertet bestehende Oberflaechen: Die Tkinter-Analyse liegt inzwischen
  unter `src/ma_ui/tkinter_app/module_views/analyse/` und wurde fachlich an
  den neuen Plot-Template-Ablauf angeglichen; `src/ma_variants/ui/services.py`
  dient als positives Muster fuer Trennung von UI und Fachlogik.
- P005 Streamlit-/Tkinter-Anpassung dokumentiert: `docs/project/architecture/UI_MIGRATION_PLAN.md` beschreibt Bestandsanalyse, Schnittstellenentwurf, Bereinigung, Legacy-Auslagerung, Streamlit-Aufbau und spaetere Modulanbindung.
- P005 Bestandsanalyse aktualisiert: `ma_analyse` hat weder Streamlit- noch
  Tkinter-Abhaengigkeit; die getrennte Tkinter-Analyse liegt unter `ma_ui`.
- P005 Schnittstellenentwurf dokumentiert: `AnalysisConfig`, `AnalysisResult` und `run_analysis(config)` bilden die UI-neutrale Service-Fassade.
- P005 erster Service-Code-Slice umgesetzt: `src/ma_analyse/models.py` und `src/ma_analyse/services.py` stellen `AnalysisConfig`, `AnalysisResult` und `run_analysis(config)` als UI-neutrale Fassade bereit.
- P005 Workflow-/UI-Shell umgesetzt: `src/ma_workflow/` enthaelt Workflow-Katalog und Analyse-Adapter; `src/ma_ui/` enthaelt eine Streamlit-Shell mit Startseite, Analyse-Seite, Navigation und Projektzustand.
- UI-Strukturumzug umgesetzt: Streamlit liegt unter
  `ma_ui.streamlit_app`, Tkinter unter `ma_ui.tkinter_app`.
  `src/ma_ui/app.py` bleibt stabiler Streamlit-Einstieg; die alte
  `ma_analyse.gui`-Kompatibilitaetsfassade und `python -m ma_analyse gui`
  wurden entfernt.
- P005 Startseite erweitert: `ma_ui` zeigt Workflow-Statuskennzahlen,
  Phasenuebersicht, Workflow-Schritte und Dashboard-Aktionen aus
  `ma_workflow`.
- P005 Analyse-Seite erweitert: `ma_analyse` sammelt erzeugte Dateien in `AnalysisResult.created_files`; `ma_ui` zeigt Status, Fehler, Hinweise, erzeugte Dateien und Log strukturiert an.
- P005 Varianten-Uebersicht in `ma_ui` ergaenzt: Parameter, Optionen, Variantenraum, Auswahlmethoden und Exportdateien werden ueber bestehende `ma_variants`-Services angezeigt.
- P005 Wetter-Uebersicht in `ma_ui` ergaenzt: lokale TRY-Datensaetze werden aus dem `ma_weather`-Katalog angezeigt, ohne TRY-Dateien zu importieren.
- P005 Bewertungs-Uebersicht in `ma_ui` ergaenzt: generische Systemkosten, Energiepreise und Szenarien werden aus bestehenden Wirtschaftlichkeitsannahmen angezeigt, ohne Variantenkosten zu berechnen.
- P005 Planoptimierung nach verschaerfter Nutzer-Ausarbeitung umgesetzt:
  Zielstruktur fuer `ma_ui`, `ma_workflow`, `ma_economy`,
  `ma_sustainability`, `ma_assessment`, `ma_simulation_setup` und den
  getrennten Tkinter-Zweig ist dokumentiert.
- P005 kompatibler Struktur-Slice umgesetzt: `ma_ui.streamlit_app.shared`,
  `ma_ui.streamlit_app.module_views`, `ma_ui.streamlit_app.main_dashboard`,
  `ma_ui.streamlit_app.workflow_view`, `ma_ui.streamlit_app.pre_process_view`,
  `ma_ui.streamlit_app.post_process_view` sowie die geplanten
  `ma_workflow`-Dateien fuer Dashboard-Aktionen, Pre-/Post-Process und
  Feedback sind vorbereitet. Alte `ma_ui.*`-Importpfade bleiben ueber
  Kompatibilitaetswrapper erreichbar.
- P005 Analyse-View fachlich erweitert:
  `ma_ui.streamlit_app.module_views.analyse_view` bildet Prepare-, Comfort-,
  Heating-/Cooling- und Plot-Template-Optionen auf `AnalysisConfig` ab;
  `ma_ui.streamlit_app.pages.analyse` bleibt Streamlit-Zwischenebene.
- P005 Analyse-View gegen Tkinter-Ablauf weiter abgeglichen: `analyze-data`
  ist als eigener Excel-Auswertungsschritt mit `separate`/`combined`
  abgebildet.
- P007-Workflow ergaenzt: `Datenvorbereitung` ist als eigener Schritt in
  Phase 4 zwischen Simulationsergebnisimport und Analyse Stufe 2 eingeordnet.
  `prepare` und `analyze-data` bleiben in `ma_analyse`, gehoeren fachlich aber
  zu diesem vorbereitenden Schritt.
- P005 Analyseumfang in Streamlit ergaenzt: `Eine Variante`, `Mehrere Varianten`
  und `Alle Varianten` werden erfasst; `Alle Varianten` wird als automatische
  Variantenauswahl an die Service-Fassade uebergeben.
- P005 automatische Analyseauswahl ergaenzt: Variantenlisten fuer Prepare- und
  Datenbankaufrufe sowie Raumlisten werden ueber `ma_analyse.services`
  bereitgestellt; manuelle Texteingabe bleibt als Fallback.
- P005 freie Overlay-Linien in der Analyse-View ergaenzt: einfache Texteingabe
  im Format `source,column,label,axis` wird in Plot-Template-Optionen
  uebersetzt.
- P005 einfache Overlay-Katalogauswahl ergaenzt: `ma_analyse.services`
  stellt CSV-/AUX-Spalten fuer Plot-Template-Overlays bereit; die Analyse-View
  kann daraus eine Overlay-Zeile uebernehmen.
- P005 Streamlit-Importrobustheit ergaenzt: optionale Overlay-Katalogfunktion
  wird in der Analyse-View defensiv zur Laufzeit geladen; Startdokumentation
  empfiehlt den venv-basierten Modulaufruf.
- P005 Plot-Template-Auswahl in Streamlit an Tkinter-Logik angenaehert:
  Nach Auswahl des Befehls `plot-template` werden Zeitfelder aus dem Template
  abgeleitet, Einzelraum-/Mehrraumlogik wird beachtet, Template-Defaults werden
  geladen, feste/freie Overlays sind bedienbar und erzeugte Bilddateien werden
  direkt als Vorschau angezeigt.
- P005 Analyse-Wizard umgesetzt: Die Streamlit-Analyse-Seite startet mit der
  Befehlsauswahl, blendet Folgeschritte nach der vorhandenen Tkinter-
  Zustandslogik ein, fasst vorherige Schritte zusammen und fuehrt technische
  Pfade unter `Erweiterte Pfade`.
- P005 Analyse-Wizard weiter angepasst: Streamlit nutzt eine sichtbare
  Schrittstruktur mit `Befehl`, `Unterbefehl`, `Template / Diagramm`,
  `Varianten`, `Raeume`, optional `Overlay`, abschliessend
  `Export / Ausgabe` und `Analyse starten`.
- P005 Analyse-Wizard bereinigt: Der allgemeine Bereich `Optionen` wurde aus
  der aktiven UI-Struktur entfernt; befehlsspezifische Einstellungen liegen in
  `Export` oder `Template / Diagramm`.
- P005 Comfort-Ablauf angepasst: Die separate Analyseebene wurde entfernt;
  alle vier Comfort-Unterbefehle bleiben sichtbar und Varianten-/Raumumfang
  steuern die Auswahl.
- P005 Varianten- und Raumauswahl angepasst: Variantenumfang und Raumumfang
  liegen in den jeweiligen Bereichen; `Alle Varianten` wird an die
  Service-Fassade als automatische Variantenauswahl uebergeben.
- P005 Plot-Template-Ablauf angepasst: Alle Templates werden direkt als
  Unterbefehle angezeigt. Zeitansicht, Overlay-Aktivierung und ausklappbare
  Diagrammanpassung liegen unter `Template / Diagramm`; der optionale
  Overlay-Schritt folgt direkt danach und befuellt den Katalog erst nach
  Varianten- und Raumauswahl.
- P005 Analyse-Wizard weiter strukturiert: `plot-template-analyse` ist in
  Streamlit der UI-Befehl fuer Analyse-Templates, `single`/`compare` liegt
  unter `Export / Ausgabe`, Comfort nutzt `t_op / rel_hum` als Unterbefehl und
  die vier bisherigen Comfort-Ausgaben liegen unter `Template / Diagramm`.
- P005 Aktionsbereich angepasst: In Streamlit stehen `Vorschau aktualisieren`
  und `Analyse starten` sichtbar ausserhalb der Hauptschritte.
- P005 Tkinter-Vorschau vorbereitet: In der Tkinter-Analyse steht
  `Vorschau aktualisieren` zwischen `Zuruecksetzen` und `Start` und nutzt
  inzwischen den normalen `AnalysisConfig`-/`ma_workflow`-Analysepfad mit
  aktuellen Einstellungen.
- P005 Tkinter-Analyse pragmatisch angeglichen: Variantenumfang und
  Raumumfang liegen in den jeweiligen Karten, Comfort nutzt keine verpflichtende
  Analyseebene mehr.
- P005 Tkinter-Analyse korrigiert: Bei `plot-template` zeigt eine scrollbare
  Liste alle Diagramme direkt als Unterbefehle. `single`/`compare` liegt wie
  in Streamlit im letzten Schritt `Export / Ausgabe`.
- P005 Plot-Template-Ausgabe erweitert: `single` erzeugt je
  Variante-Raum-Kombination eine eigene Datei. `compare` zeichnet
  Heating-/Cooling-Zeitreihen gemeinsam und buendelt komplexe
  Sammeltemplates als Teilplots in einer Vergleichsgrafik.
- P005 Diagrammanpassung erweitert: Automatische Achsengrenzen sind Standard;
  manuelle Grenzen fuer primaere und sekundaere Y-Achsen werden in einem
  Mock-up sichtbar und an die unterstuetzten Plot-Renderer weitergegeben.
- P005 Overlay-Ablauf erweitert: Der eigene Overlay-Schritt wird ueber eine
  Checkbox aktiviert. Als Katalogreferenz dienen sichtbar die erste Variante
  und der erste Raum; weitere Kombinationen werden beim Lauf validiert.
- P005 Streamlit-Exportbereich verschoben: `Export / Ausgabe` ist die letzte
  Abfrage vor dem Aktionsbereich und enthaelt den Expander
  `Erweiterte Pfade`.
- P005 UI-neutrale Analyse-Helfer ausgelagert: Auswahl-, Zeit-, Overlay- und
  Config-Aufbereitung liegen in `src/ma_analyse/analysis_ui.py`.
- P005 Hybrid-Bedienung vorbereitet: Die Streamlit-Analyse-Seite kann die
  Tkinter-Analyse als separates Fenster unter
  `ma_ui.tkinter_app.module_views.analyse` starten, ohne Tkinter in Streamlit
  einzubetten.
- P029 harter Tkinter-Migrationsslice umgesetzt: `ma_ui` ist alleiniger
  Eigentumer der Tkinter-Analyse; `ma_analyse` stellt nur noch fachliche
  Services, Runner, Templates und Konfigurationen bereit.
- P005 grafisches Workflow-Dashboard umgesetzt: Die `ma_ui`-Startseite zeigt
  Phasen, Workflow-Karten, Statusfarben, Iterationspfade und Buttons zu
  vorhandenen Modulansichten; Detailtabellen bleiben im Expander erreichbar.
- Historischer P005-Slice: Die damaligen Platzhalter-Views zeigten
  Workflow-Kontext und vorhandene Projektressourcen. P007 ersetzt sie aktiv
  durch kataloggesteuerte Modul-Infoseiten; historische IDA-Views bleiben
  Kompatibilitaetswrapper auf die allgemeinen Schnittstellen.
- P028 umgesetzt: Projekt-, Parameter- und Variantenansicht teilen einen
  Sitzungsstand, wenden neutrale Benennungsprofile an und speichern eigene
  YAML-Arbeitsstaende mit technischem Vorlagenschutz.
- P010 umgesetzt: `InputSource`, strukturierte Diagnose- und
  Freigabemodelle, Dateipruefsummen und JSONL-Sitzungslogs sind vorhanden.
  Der TRY-Wetterpilot zeigt Quellen, Warnungs-IDs, Fundstellen und
  Freigabeentscheidungen in Streamlit.

### Offen

- P008 liegt als aktiver konsolidierter Gesamtplan fuer das Wettermodul in der
  Plan-Inbox. Die beiden Ausgangsplaene wurden archiviert.
- P010-Vertraege in P011, P012, P013, P014 und P015 nur mit dem jeweiligen
  Fachslice anbinden.
- Die P013-S3-Referenzzuordnung und der P013-/P014-Checkpoint sind umgesetzt.
  Offen bleibt die fachlich zentrale Technikmodellierung vor weiterem
  Zonen-/Parameterausbau; die bestehende LoD-1-Technikdemo nutzt weiterhin
  `source_zone_model_id` und `served_zone_ids`.
- P020 beginnt mit der noch offenen Vertrags- und Rechteklaerung fuer DIN,
  VDE und VDI. Vor einer belastbaren Normen- und Methodenmatrix sowie gruen
  freigegebener Provenienz duerfen keine extrahierten Grenzwerte oder
  normbasierten Softwareregeln als Norm-Nachweis implementiert werden.
- Aus P005 nach P007 uebernommen: Analyse-View in laufender Streamlit-App manuell gegen
  reale `ida_imports`-/Datenbankordner pruefen.
- Aus P005 nach P007 uebernommen: Schrittweisen Analyse-Wizard in der laufenden
  Streamlit-App fachlich gegen den bisherigen Tkinter-Ablauf pruefen,
  insbesondere Comfort, Heating/Cooling, Plot-Template-Overlays,
  Diagrammbearbeitung und Vorschau.
- Aus P005 nach P007 uebernommen: Comfort-Unterbefehl und
  Comfort-Diagrammauswahl in der Tkinter-Analyse
  noch vollstaendig an die Streamlit-Struktur angleichen.
- Aus P005 nach P007 uebernommen: Eingebettetes Bild-Vorschaufenster fuer den
  Vorschau-Button ergaenzen. Die Vorschau soll einen temporaeren
  Vorschau-/Cachebereich nutzen, damit der regulaere Output-Ordner nicht mit
  fehlerhaften Testdiagrammen gefuellt wird.
- P007 spaeterer Schritt: Weitere Tkinter-Fachansichten unter
  `ma_ui.tkinter_app.module_views/` nur mit eigenem Fachslice ergaenzen.
- P007 spaeterer Schritt: `ma_workflow` schrittweise mit echten
  Fachservice-Aufrufen erweitern.
- P007 spaeterer Schritt: `ma_economy`, `ma_sustainability` und
  `ma_assessment` getrennt planen, bevor Wirtschaftlichkeitslogik aus
  `ma_variants` verschoben oder erweitert wird.
- Neue externe Plaene nach manueller Ablage in `docs/project/plans/inbox/` pruefen und in `PLAN_INDEX.md` sowie in diese Statusdatei uebernehmen.
- Nach groesseren Aenderungen pruefen, ob alte Planstaende nach `docs/project/archive/plans/` ausgelagert werden sollen.

## Modul ma_analyse

### Abgeschlossen

- Plot-Template-Katalog aktualisiert: `heating-year` ist overlayfrei, `heating-overlay` fuehrt die festen Heating-Overlays separat.
- Cooling-Plot-Templates getrennt: `cooling-year`, `cooling-month`, `cooling-week` und `cooling-day` verwenden Rohwerte aus `zone_energy_q_cool`; `cooling-absolute-year`, `cooling-absolute-month`, `cooling-absolute-week` und `cooling-absolute-day` zeigen Betraege positiv nach oben.
- Plot-Template-Referenzgalerie unter `docs/examples/plot_template_analyse/` wurde mit 33 aktuellen Analyse-Beispielen bereitgestellt.
- GUI-Mousewheel-Handler faengt nicht aufloesbare Tkinter-Combobox-Popups robust ab und verhindert `KeyError: 'popdown'`.
- IDA-Importordner umbenannt: `ma_analyse` nutzt fuer Rohdatenvarianten `data/ma_analyse/ida_imports`; der bisherige Eingangsordner wurde entfernt.
- Datenvorbereitung als eigener Workflow-Schritt eingeordnet:
  `prepare` erzeugt die nutzbaren Raumtabellen und `analyze-data` den
  Basisbericht vor Analyse Stufe 2. Die Fachlogik bleibt in `ma_analyse`.

### Teilweise umgesetzt

- Plot-Template-Katalog: Referenzbilder liegen unter `docs/examples/plot_template_analyse/`; die Dokumentation liegt unter `docs/ma_analyse/plot_template_examples.md`.
- Heating-Jahresplot nutzt eine gemeinsame Layoutbasis. Absolute Cooling-Jahresplots koennen diese Layoutbasis ebenfalls nutzen; relative Cooling-Templates bleiben als eigene signierte Darstellung erhalten.
- Interne Lasten und Energiebilanz sind als Plot-Template-Experimente vorhanden.
- P029 ist als aktiver Aufraeumplan aufgenommen: Zuerst wird der
  Service-/Runner-Vertrag von `ma_analyse` stabilisiert, danach erst folgen
  groessere Zerlegungen von `heating.py`, `cooling.py` oder Tkinter.
- P029 Service-Slice erweitert: `ma_analyse.services` trennt
  `AnalysisRuntimeOptions` als interne Laufstruktur vom aktuellen
  Legacy-`argparse.Namespace`; `run_analysis(config)` bleibt die oeffentliche
  Fassade fuer UI und Workflow.
- P029 Legacy-Adapter-Slice umgesetzt: `_execute_legacy_analysis(...)`
  kapselt `run_all()`, `execute_steps()`, stdout-/stderr-Sammlung,
  `SystemExit`-Uebersetzung und unerwartete Exceptions; `run_analysis(config)`
  baut daraus weiterhin `AnalysisResult`.
- P029 Pipeline-Runtime-Slice umgesetzt: `build_runtime_args(...)` liefert mit
  `PipelineRuntimeArgs` einen typisierten internen Schrittvertrag statt eines
  freien `argparse.Namespace`; CLI, Tkinter und Streamlit bleiben kompatibel.
- P029 Precondition-Slice umgesetzt: `check_required_data(...)` liefert
  strukturierte Datenvorbedingungs-Ergebnisse; `ensure_required_data(...)`
  bleibt als kompatibler `print()`-/`SystemExit`-Wrapper bestehen.
- P029 Service-Precondition-Slice umgesetzt: `ma_analyse.services` nutzt
  `check_required_data(...)` vor `run_all()`/`execute_steps()`; fehlende
  Nutzdaten werden im Service als strukturierte Fehler gemeldet, waehrend CLI
  und Tkinter kompatibel bleiben.
- P029 Tkinter-Struktur-Slice umgesetzt: Die Tkinter-Analyse unter
  `ma_ui.tkinter_app.module_views.analyse` ist intern in Mixins fuer
  Initialisierung, Fenster/Style, Layout, Schrittfluss, Auswahl-State,
  Plot-Template-State und Pipeline-Runner zerlegt; `app.py` bleibt als
  135-Zeilen-Fassade fuer die oeffentlichen Startpunkte erhalten.
- P029 Tkinter-Service-Adapter-Slice umgesetzt: `pipeline_config.py` baut
  `AnalysisConfig` aus dem Tkinter-Zustand; `pipeline_runner.py` startet ueber
  `ma_workflow.run_analysis_action`. Direkte Tkinter-Runner-Aufrufe von
  `build_runtime_args`, `execute_steps` und `run_all` sind entfernt.
- P029 Mapping-Slice umgesetzt: `pipeline_config.py` delegiert die
  `AnalysisConfig`-Erzeugung an `ma_analyse.analysis_ui.build_analysis_config`.
  Der gemeinsame Builder akzeptiert Text- und Listenwerte fuer Varianten und
  Raeume und setzt `load_kind` fuer Heating-/Cooling-Laeufe.

### Offen

- Overlay-Uebernahme in Hauptfunktionen umsetzen: freie Datenreihen sollen aus
  lokalen Analyse-/Datenbankdaten in die aktuelle Ansicht geladen werden
  koennen; feste Additionen wie Temperaturband und Achsenbereiche bleiben
  eigene kontrollierte Diagrammoptionen. Betroffen:
  `src/ma_analyse/analysis/heating.py`, `src/ma_analyse/analysis/cooling.py`,
  `src/ma_ui/tkinter_app/module_views/analyse/app.py`,
  `src/ma_analyse/app/cli.py`.
- UD-065 umsetzen: Der normale `cooling`-Befehl und die GUI sollen relative
  Rohwerte und absolute Betraege als eigene Modi erhalten.
- Tkinter-Folgeslice planen: Vorschau in einen temporaeren Cachebereich legen,
  Ergebnis-/Loganzeige weiter aus `AnalysisResult` strukturieren und verbleibende
  Options-/Preview-Dopplung zwischen Streamlit-Analyse und Tkinter-Analyse
  reduzieren.
- Heating und Cooling weiter in Datenladen, Runner und Plotmodule zerlegen. Betroffen: `src/ma_analyse/analysis/heating.py`, `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/analysis/energy/`.
- P029 Folgearbeit: `ma_analyse.app.commands` nach Runtime-Options-,
  Legacy-Adapter- und Pipeline-Runtime-Slice schrittweise weiter von
  `print()` und `SystemExit` als internem Service-Vertrag entkoppeln; naechste
  Kandidaten sind fachliche Runner-Ausgaben und Schrittstatus.
- Datenvorbereitung nach erfolgreichem Simulationsergebnisimport in
  `ma_workflow`/`ma_ui` als Folgeschritt anbieten, ohne die Importadapter mit
  Analysefachlogik zu vermischen.

### Unklar

- Soll aus den Internal-Loads-Templates ein eigener Befehl entstehen oder eine Integration in bestehende Auswertungen?
- Welche `ma_analyse`-Auswertungen sollen absolute Werte, flaechenbezogene Werte
  wie `[W/m2]` oder beides anbieten, und welche Bezugsflaeche gilt dafuer?

## Modul ma_variants

### Abgeschlossen

- `ma_variants` ist als eigenes Paket unter `src/ma_variants/` vorhanden.
- Variantenbezogene Konfigurationen liegen unter `config/ma_variants/`.
- Variantenbezogene Import-, Export- und IDA-Uebergabeordner liegen unter `data/ma_variants/`.
- Produkt- und Materialdokumente liegen als eigener Katalogbereich unter `data/catalogs/documents/`.
- P001 Bestandspruefung: Import, Optionsimport, Variantenzahlung, Variantenerzeugung, Auswahl, Namensgebung und Export sind bereits als testbare Module vorhanden.
- P001 Variantenoberflaeche: `src/ma_variants/ui/app.py` bildet Parameter/Optionen, Variantenraum, Auswahl, Namensgebung, Export, Ergebnisse und Status getrennt ab.
- P001 UI-Services: `src/ma_variants/ui/services.py` kapselt manuelle Auswahl, reproduzierbare Zufallsauswahl, Filterauswahl und Namensgenerierung ausserhalb der Streamlit-Datei.
- P001 Variantenmodul GUI und Logikpruefung ist abgeschlossen: `tests -k ma_variants` wurde erfolgreich ausgefuehrt und die Streamlit-App wurde headless gestartet.
- P001 wurde nach `docs/project/archive/plans/250603_Plan_Variantenmodul_GUI_Logikpruefung.md` verschoben.

### Offen

- Falls weitere Modulordner unter `data/ma_variants/` gebraucht werden, zuerst im Planstatus dokumentieren.

## Modul ma_weather

### Teilweise umgesetzt

- P002 Struktur-Slice umgesetzt: `src/ma_weather/` ist als importierbares Paket vorbereitet.
- Wetterkatalog mit `WeatherDataset` und YAML-Import liegt unter `src/ma_weather/weather_catalog.py`.
- Beispielkatalog liegt unter `config/ma_weather/datasets/example_weather_datasets.yaml`.
- Reale TRY-Dateien werden lokal unter `data/ma_weather/input/` bereitgestellt und nicht versioniert.
- `data/ma_weather/database/` ist fuer spaeter aufbereitete Wetterdaten vorbereitet.
- `data/ma_weather/output/` ist fuer spaeter erzeugte Wetterdiagramme vorbereitet.
- Dokumentation liegt unter `docs/ma_weather/README.md`, `docs/ma_weather/workflow.md`, `docs/ma_weather/data_model.md` und `docs/ma_weather/commands_weather.md`.
- P002 Analyse-Slice umgesetzt: TRY-Importer, Wettervalidierung, Kennwerte,
  Diagramme, Markdown-Bericht und Runner sind als erste lokale Pipeline
  vorhanden.
- P002 Real-Testlauf fuer `TRY_FFM_2015_JAHR` erfolgreich: Validierung `ok`, 8760 Stunden,
  sechs Diagramme, aufbereitete CSV und Markdown-Bericht wurden lokal erzeugt.
- P008 Standort- und Rollen-Slice umgesetzt: YAML-Standortkatalog,
  Klimaregions-/Referenzstandortlogik, optionale Datensatzrollen
  `try_reference` und `site_specific` sowie zweispaltige Streamlit-Auswahl
  mit Klimaregionenkarte im UI-Assetbereich sind vorhanden.
- P008 Status-, Import- und Freigabe-Slices umgesetzt: Datei- und
  Importstatus, offene Wetterdatensaetze, stabile `import_id`,
  Verknuepfung mit Sitzungs-/Run-Nachweis, bewusste Aktivierung und
  bewusstes Setzen eines Projekt-Defaults sind vorbereitet.
- P008 Datensatztyp- und Ereignis-Slice umgesetzt: Jahr-, Sommer- und
  Winter-TRY-Dateien sind als eigene Datensaetze katalogisiert; kritische
  Wetterereignisse werden aus dem bewusst ausgewaehlten Datensatz abgeleitet
  und in Streamlit tabellarisch angezeigt.
- P008 Import-/Scan-/Pruefungsslice teilweise umgesetzt:
  Streamlit fuehrt die Schritte `Import`, `Scannen` und `Pruefen` im Bereich
  `Wetterdatensaetze`; eigene entpackte TRY-`.dat`-Dateien koennen lokal
  abgelegt, lokale TRY-Dateien als Datensatzentwuerfe gescannt und
  Parameter bewusst geprueft werden. Bestaetigtes TRY-Ordner-Mapping
  darf vorbelegen, Standortverweise aus TRY-Kopfzeilen werden erkannt und
  Konflikte blockieren die Registrierung. Die EPSG:3034-Standortaufloesung
  nutzt die lokal aktivierte BKG-VG250-Gemeindequelle; Berlin- und Potsdam-
  TRY-Testdateien werden als Berlin beziehungsweise Potsdam erkannt. Aktive
  und offene Wetterdatensaetze werden getrennt angezeigt.

### Offen

- Fehlende TRY-Jahres-, Sommer- und Winterdateien beim Deutschen
  Wetterdienst herunterladen und lokal unter `data/ma_weather/input/`
  ablegen oder ueber den lokalen Streamlit-Import registrieren.
- Weitere aktive Jahr-, Sommer- und Winterdatensaetze real gegen lokal
  vorhandene TRY-Dateien pruefen und Testergebnisse dokumentieren.
- Fachliche Definition der kritischen Wetterereignisse fuer P021 schaerfen
  und mit vorhandenen Tages- und Wochenzeitfenstern verbinden.
- TRY-Referenzdatensaetze fuer Referenzstandorte wie Mannheim und Passau
  fachlich ergaenzen oder bewusst als fehlend dokumentieren.
- Weitere ortsgenaue TRY-Dateien gegen die aktivierte BKG-VG250-
  Gemeindeaufloesung testen und erkannte Standortwerte dokumentieren.
- PLZ-Datenquelle lizenzrechtlich pruefen und bei Bedarf als optionale
  Aufloesung aktivieren.
- Diagrammgestaltung fachlich pruefen und bei Bedarf an Masterarbeitslayout anpassen.
- Strukturpunkt geschlossen: Wetterdiagramme bleiben fachlich im Modul
  `ma_weather`; `plot-template-weather` ist dort als eigener CLI-/UI-Befehl
  mit Unterauswahl fuer einzelne vorhandene Wetterdiagramme aufgebaut.
- Konsolidierten P008-Gesamtplan erst abschliessen und archivieren, wenn die
  vorgesehenen realen TRY-Datensaetze lokal erfolgreich verarbeitet, die
  P021-Ereignisdefinition fachlich bestaetigt und die
  P007-/`ma_parameters`-Schnittstelle geklaert wurden.

## Offene Nutzerentscheidungen

- Klaeren, welche `ma_analyse`-Auswertungen absolute Werte, flaechenbezogene
  Werte oder beides anbieten sollen und welche Bezugsflaeche verwendet wird.
- Wissensprofile, Stundensaetze, Prozessgrenzen und Messmethoden fuer den
  Vergleich von manuellem, softwareunterstuetztem und automatisiertem Aufwand
  festlegen.
- P031-Folgeaktivierungen getrennt entscheiden: Bedeutung von `keine Hooks`,
  effektive MCP-Grenze, Agentenlimit 3 oder 4, Graphify-Scope,
  Obsidian-/Zotero-Ziel sowie objektbezogene PDF- und IDA-Rechte.

## Archiv

- `docs/project/archive/plans/2026-05-26.md`: alter Planstatus vor der modularen Struktur.
- `docs/project/archive/plans/250603_Plan_Variantenmodul_GUI_Logikpruefung.md`: abgeschlossener P001-Plan.
- `docs/project/archive/plans/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md`: umgesetzter Strukturplan P003.
- `docs/project/archive/plans/PLAN_Projektplan_Version_1_0_0.md`: abgelegter Projektplan Version 1.0.0.
- `docs/project/archive/plans/250603_Plan_Wetterdatenanalyse_TRY_Integration.md`: teilweise umgesetzter P002-Ursprungsplan; Restarbeiten stehen in P008.
- `docs/project/archive/plans/260621_Plan_P008_Wettermodul_Abschluss_P007_Anbindung.md`: archivierter P008-Ausgangsplan; Inhalte stehen im konsolidierten P008-Gesamtplan.
- `docs/project/archive/plans/Implementierungsplan_ma_weather.md`: archivierter unnummerierter ma_weather-Ausgangsplan; Inhalte stehen im konsolidierten P008-Gesamtplan.
- `docs/project/archive/plans/260627_Planergaenzung_P008_ma_weather_Standorterkennung_PLZ.md`: archivierte P008-Planergaenzung; Inhalte stehen im aktualisierten P008-Gesamtplan.
- `docs/project/archive/plans/250608_Plan_Gesamtmodulstruktur_PreProcess_PostProcess_Dashboard.md.txt`: teilweise umgesetzter P005-Strukturplan; gueltige Inhalte sind in P007 konsolidiert.
- `docs/project/archive/plans/260618_Plan_ma_export_ida_IDM_Exportentwurf.md`: historischer P006-Entwurf; verbleibende Schnittstellenarbeit steht in P009.
