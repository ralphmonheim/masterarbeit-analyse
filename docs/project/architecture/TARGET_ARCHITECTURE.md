# Zielarchitektur

Stand: 2026-07-08
Grundlage: P007

## Zweck

Dieses Dokument beschreibt die verbindliche technische Einordnung der
P007-Zielstruktur. Fachliche Detailumsetzungen werden weiterhin ueber
gesonderte Teilplaene analysiert, freigegeben und getestet.

## Architekturregeln

- Phase 0 bildet die technische Plattform; danach folgen sechs fachliche Phasen.
- Fachlogik bleibt UI-neutral und liegt in den Fachmodulen.
- `ma_workflow` ist die zentrale Quelle fuer Phasen, Module und Status.
- `ma_ui` zeigt Fachansichten oder neutrale Modul-Infoseiten.
- Paketexistenz bedeutet nicht automatisch fachliche Verfuegbarkeit.
- Bestehende Logik wird nicht ohne Migrationsplan verschoben.
- IDA ICE bleibt der manuelle externe Simulationsschritt.
- Import wird je Eingabemodul bevorzugt; manuelle Eingabe und Demo-Daten
  bleiben zulaessige Alternativen.
- Externe Dateiformate werden ueber Adapter in neutrale Fachmodelle
  ueberfuehrt.
- `ma_project` verwaltet die frei erweiterbare Simulationsprogrammliste und
  neutrale Varianten-Benennungsprofile.
- `ma_parameters` besitzt Parameterdefinitionen, Optionsgruppen und
  ausgewaehlte Werte; `ma_variants` konsumiert diese Daten.
- Produkt- und Materialbezeichnungen bleiben neutrale Katalogdaten.
- Programmspezifische Objekt- und Exportcodes liegen in den jeweiligen
  Simulationsadaptern.
- Eingabestaende verwenden formatneutrale `InputSource`-Metadaten.
- Fachmodule erzeugen strukturierte Diagnosen; Fehler blockieren, Warnungen
  benoetigen eine bewusste Freigabeentscheidung.
- Lauf- und Freigabeereignisse werden lokal append-only in
  `logs/sessions/<session_id>.jsonl` dokumentiert.

## Phase 0 und sechs Hauptphasen

| Phase | Module und Bereiche | Ziel |
|---|---|---|
| Phase 0 | `ma_core`, `ma_database`, `ma_ui`, `ma_workflow`, Dokumentationsinfrastruktur | technische und organisatorische Plattform |
| Phase 1 | `ma_project` | Projekt und Untersuchungsrahmen initialisieren |
| Phase 2 | `ma_weather`, `ma_building`, `ma_technical`, `ma_zones`, `ma_parameters` | Eingaben erfassen, validieren und vereinheitlichen |
| Phase 3 | `ma_analyse.stage_1_dimensioning`, `ma_variants`, `ma_simulation_setup`, `ma_export_simulation` | Referenz dimensionieren, Varianten und Run vorbereiten |
| Phase 4 | IDA ICE, `ma_import_simulation`, `ma_analyse.data_preparation`, `ma_analyse.stage_2_optimization`, `ma_analyse.stage_3_standards_compliance`, `ma_analyse.stage_4_sensitivity` | simulieren, Daten vorbereiten, optimieren, Norm-Nachweise und Sensitivitaet auswerten |
| Phase 5 | `ma_economy`, `ma_sustainability`, `ma_assessment` | wirtschaftlich, oekologisch und gesamthaft bewerten |
| Phase 6 | `ma_reporting`, `ma_data_export`, Projektdokumentation | Berichte, Datenpakete und Archivierung |

`ma_validation` und `ma_feedback` wirken phasenuebergreifend.

## Verbindlicher Datenfluss

```text
ma_weather
ma_building
ma_technical
ma_zones
    -> ma_validation Eingabecheckpoint
    -> ma_parameters
    -> ma_validation Parametercheckpoint
    -> ma_analyse.stage_1_dimensioning
    -> ma_variants
    -> ma_simulation_setup
    -> ma_export_simulation
       -> adapters.ida_ice
    -> manuelle IDA-ICE-Simulation
    -> ma_import_simulation
       -> adapters.ida_ice
    -> ma_analyse.data_preparation
    -> ma_analyse.stage_2_optimization
    -> ma_analyse.stage_3_standards_compliance
    -> ma_analyse.stage_4_sensitivity
    -> ma_economy
    -> ma_sustainability
    -> ma_assessment
    -> ma_reporting
    -> ma_data_export
    -> Projektdokumentation und Archivierung
```

`ma_parameters` ist die einzige fachliche Eingangsquelle fuer
`ma_variants`. Direkte Abhaengigkeiten von `ma_variants` zu Gebaeude, Wetter,
Zonen oder Technik sind im Zielbild nicht vorgesehen.

`ma_parameters` erzeugt versionierte `ParameterSnapshot`-Staende.
`ma_simulation_setup` referenziert diese in einem validierten `RunManifest`.
`ma_variants` wendet das von `ma_project` referenzierte neutrale
Benennungsprofil an, besitzt dessen Konfiguration aber nicht.

P028 bildet Projekt-, Parameter- und Naming-Demo in Streamlit ab. P015-S1
stellt darueber hinaus einen produktiven BusinessIntegration-LoD-1-
`ParameterSnapshot` v1 aus freigegebenen Demoquellen bereit. P013-S2
konsolidiert den Zielvertrag fuer den spaeteren vollstaendigen Zonenstand;
Status-/Fingerprint-Logik und Variantensperre bleiben Folgearbeit.

## Eingabequellen

- Die Quellenwahl erfolgt je Modul.
- Import ist bevorzugt; manuelle Eingabe und Demo sind zulaessig.
- Originaldatei, Adapter, Warnungen, Validierungsstatus und manuelle
  Aenderungen bleiben nachvollziehbar.
- Versionierte Vorlagen sind unveraenderlich. Eigene Arbeitsstaende werden in
  lokalen Modulpfaden gespeichert.
- Bei einem bereits vorhandenen neuen Dateinamen muss der Nutzer einen anderen
  Namen auswaehlen; automatische Ersatznamen sind ausgeschlossen.
- YAML ist das erste menschenlesbare Format, die Fachmodelle und Services
  bleiben jedoch fuer spaetere Formate offen.
- Building und Zones werden mindestens als Konzept und Demo aufgebaut.
- P012 konkretisiert fuer `ma_building` eine einfache
  `BuildingModelSpecification` als Demo- und Trainingsbasis.
- `SmallOffice_d_IFC2x3.ifc` dient dem fachlichen Teil als IDA-ICE-
  Referenzmodell; das Rhino-Testgebaeude dient BusinessIntegration und
  Softwaretests als lokale Arbeitsreferenz.
- Die aktuelle IFC-Arbeitsdatei darf lokal als Diagnose- und Trainingsquelle
  dienen; ein produktiver IFC-Lite-Import bleibt bis zur Analyse konkreter
  IFC-Arbeitsstaende offen.
- Rhino `.3dm` ist als BusinessIntegration-Referenz nutzbar, aber keine
  freigegebene produktive Importschnittstelle. P012-S2 setzt LoD-1 als
  Eingabeumfang um: Kubatur, Huellkennwerte, U-Werte und Fensteranteil.
  LoD-2/LoD-3 bleiben Folgeausbau.
- Direkte CAD-Integration gehoert nicht zum aktuellen Masterarbeitsumfang.

Die aktuelle Reifegradmatrix steht in
`docs/project/architecture/INPUT_DATA_FORMAT_MATRIX.md`. P010 hat die
Vertraege am TRY-Wetterimport erprobt. Weitere Fachmodule werden erst mit
ihrem jeweiligen Teilplan angebunden; eine zentrale Datenbank folgt nicht
vor stabilen Fachmodellen und konkreten Abfragen.

## Datenvorbereitung und Analysestufen

- Datenvorbereitung: `prepare` erzeugt nutzbare Raumtabellen,
  `analyze-data` erzeugt den Basisbericht vor Analyse Stufe 2.
- Stage 1: vereinfachte Referenzdimensionierung mit Ausbaupfad.
- Stage 2: Optimierung auf Basis vorhandener Analysebefehle.
- Stage 3: Norm-Nachweis unter
  `ma_analyse.stage_3_standards_compliance`; deutsche Normenprofile zuerst,
  internationale Profile spaeter.
- Stage 4: Sensitivitaet und Robustheit anhand kritischer Wetter- und
  Betriebsfaelle.

## Simulationsschnittstellen

Die kanonischen Hauptmodule sind:

- `ma_export_simulation`
- `ma_import_simulation`

Programmspezifische Logik liegt ausschliesslich unter:

```text
ma_export_simulation/adapters/ida_ice/
ma_import_simulation/adapters/ida_ice/
```

Historische Schluessel `ma_export_ida`, `ma_import_ida`, `export_ida` und
`import_ida` werden voruebergehend als Aliase aufgeloest. Neue Fachlogik darf
diese Namen nicht als neue Hauptmodule verwenden.

Der vorhandene Basisexport unter `ma_variants.ida_export` bleibt bestehen, bis
P009 einen sicheren Schnittstellenvertrag und Migrationsweg definiert.

## UI- und Workflow-Vertrag

- Das Dashboard zeigt Phase 0 bis Phase 6 in dieser Reihenfolge.
- `ma_validation` und `ma_feedback` stehen in einem eigenen
  phasenuebergreifenden Bereich.
- Jedes katalogisierte Modul besitzt eine klickbare Seite.
- Nutzbare Module behalten ihre Fachansicht.
- Geplante Module zeigen Zweck, Ein- und Ausgaben, Abgrenzung,
  Abhaengigkeiten, Status und naechsten Schritt.
- Geplante Seiten enthalten keine funktionslosen Fachbedienelemente.
- `ma_ui` fuehrt Streamlit und Tkinter als getrennte UI-Zweige:
  `ma_ui.streamlit_app` fuer den aktuellen Haupteinstieg und
  `ma_ui.tkinter_app` fuer getrennte Tkinter-Ansichten.
- `src/ma_ui/app.py` bleibt stabiler Streamlit-Einstieg und delegiert an
  `ma_ui.streamlit_app`.
- Tkinter wird nicht direkt mit Streamlit vermischt. Spaetere
  Tkinter-Fachansichten werden unter
  `ma_ui.tkinter_app.module_views/<fachbereich>/` geplant.
- `ma_analyse` enthaelt keinen Tkinter-Kompatibilitaetspfad mehr. Die
  Tkinter-Analyse wird ausschliesslich unter
  `ma_ui.tkinter_app.module_views.analyse` gestartet und nutzt das
  `ma_analyse`-Backend nur fachlich.

## Ergebnisverarbeitung

- `ma_assessment` aggregiert und bewertet Ergebnisse.
- `ma_reporting` erzeugt menschlich lesbare Reports und Factsheets.
- `ma_data_export` erzeugt maschinenlesbare Datenpakete.
- Fachmodulspezifische Exporte bleiben in ihren Fachmodulen.
- Die Projektdokumentation bleibt unter `docs` und ist kein Python-Paket.

## Aktueller Umsetzungsstand

| Status | Module |
|---|---|
| verfuegbar | Projektdokumentation |
| teilweise | `ma_weather`, `ma_building`, `ma_zones`, `ma_technical`, `ma_parameters`, `ma_analyse`, `ma_analyse.data_preparation`, `ma_analyse.stage_1_dimensioning`, `ma_analyse.stage_2_optimization` |
| geplant | `ma_core`, `ma_database`, `ma_ui`, `ma_workflow`, `ma_project`, `ma_analyse.stage_3_standards_compliance`, `ma_analyse.stage_4_sensitivity`, `ma_variants`, `ma_simulation_setup`, `ma_export_simulation`, `ma_import_simulation`, `ma_economy`, `ma_sustainability`, `ma_assessment`, `ma_reporting`, `ma_data_export`, `ma_validation`, `ma_feedback` |
| manuell | IDA ICE |

Die Statuswerte werden zentral in `ma_workflow` gepflegt und von Navigation
und Dashboard uebernommen. Sie beschreiben den fachlichen Reifegrad im
Masterarbeitsworkflow. Paketgerueste, Infoseiten und vorhandener Prototypcode
reichen nicht fuer den Status `teilweise` oder `verfuegbar`.

## Relevante Teilplaene

- P008: Wettermodul, eigene Wetterimporte und kritische Ereignisse.
- P010: Eingabe-, Diagnose- und Freigabearchitektur umgesetzt und archiviert.
- P011 bis P018: Eingabekette bis Run-Manifest.
- P019 bis P021: getrennte Analysestufen.
- P022 bis P026: abgestufte Demo- und Konzeptmodule.
- P027: begleitende Querschnittsfunktionen.
- P028: Projekt-, Parameter- und Naming-Demo in Streamlit umgesetzt und
  archiviert.
- P009: nach P018 zurueckgestellte Simulationsschnittstellen.

## Migrationsgrundsaetze

- Leichte Pakete duerfen frueh angelegt werden.
- Fachservices, Modelle und Konfigurationen entstehen erst mit konkretem Bedarf.
- Bestehende Importpfade werden bei Umbenennungen ueber Aliase oder
  Kompatibilitaetswrapper abgesichert.
- Verschiebungen von Fachlogik benoetigen Tests vor und nach der Migration.
- P002, P005 und P006 bleiben als unveraenderte historische Quellen archiviert.
