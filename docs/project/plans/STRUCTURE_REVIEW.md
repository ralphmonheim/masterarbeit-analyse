# Strukturreview

Datum der Pruefung: 2026-06-22

Aktueller Nachtrag 2026-06-28: Dieser Review ist historisch. Die aktive
UI-Struktur liegt inzwischen unter `ma_ui.streamlit_app` und
`ma_ui.tkinter_app`; `ma_analyse.gui` wurde entfernt.

## Projektuebersicht

Das Projekt besitzt fachlich nutzbare Kernpakete und zusaetzliche leichte
Zielpakete mit unterschiedlichem Reifegrad:

- `ma_analyse`: bestehende Analysepipeline fuer IDA-ICE-Simulationsergebnisse.
- `ma_variants`: neuer Varianten-, Export-, Katalog- und Bewertungskern.
- `ma_weather`: Wetterkatalog und lokale TRY-Analysepipeline.
- `ma_workflow`: zentraler Phasen-, Modul-, Workflow- und Statuskatalog.
- `ma_ui`: zentrale Streamlit-Oberflaeche mit Dashboard und Modulansichten.
- Die P007-Zielmodule sind als importierbare, seiteneffektfreie Pakete
  vorbereitet. Ihre Paketexistenz aendert den fachlichen Status nicht.
- `ma_export_simulation` und `ma_import_simulation` sind die allgemeinen
  Schnittstellen; IDA ICE wird darunter als Adapter gefuehrt.

P007 ist seit 2026-06-21 die verbindliche Architektur- und
Roadmap-Grundlage. P002, P005 und P006 sind unveraendert archiviert; ihre
verbleibenden Facharbeiten werden in P007 und der Planserie P008 bis P028
weitergefuehrt.

## Gefundene Ordnerstruktur

- `src/ma_analyse/`: Analyse, CLI, Preprocessing, Plot-Templates.
- `src/ma_variants/`: Parameter, Optionen, Varianten, Datenbank, IDA-Export, Simulationsergebnisse, Wirtschaftlichkeit, Kataloge, UI.
- `src/ma_weather/`: Wetterkatalog, TRY-Import, Validierung, Kennwerte, Plots, Reports und Runner.
- `src/ma_workflow/`: zentraler Workflow- und Statuskatalog,
  Dashboard-Aktionen, Prozesslisten, Feedback-Routing und Analyse-Adapter.
- `src/ma_ui/`: Streamlit-Oberflaeche mit Workflow-Dashboard,
  Kopfzeilen-Navigation, `shared/`-Komponenten, `module_views/` und
  angebundenen Ansichten fuer Analyse, Varianten, Wetter und Bewertung.
- `src/ma_export_simulation/adapters/ida_ice/` und
  `src/ma_import_simulation/adapters/ida_ice/`: vorbereitete Adaptergrenzen
  ohne ungesicherte IDM-Manipulation oder IDA-API.
- Weitere Zielpakete: `ma_core`, `ma_database`, `ma_project`, `ma_building`,
  `ma_zones`, `ma_technical`, `ma_parameters`, `ma_simulation_setup`,
  `ma_economy`, `ma_sustainability`, `ma_assessment`, `ma_reporting`,
  `ma_data_export`, `ma_validation` und `ma_feedback`.
- Ziel fuer `src/ma_workflow/`: bestehende Katalog- und Adapterstruktur
  schrittweise mit echten Fachservice-Aufrufen erweitern.
- `docs/`: wurde in `project`, `ma_analyse`, `ma_variants`, `ma_weather`,
  `ma_ui`, `ma_workflow`, `common` und `examples` modularisiert.
- `config/ma_variants/`: Variantenbezogene Beispielkonfigurationen.
- `data/ma_analyse/`: aktive Rohdaten, aufbereitete Nutzdaten und regulaere Analyseausgaben der Analysepipeline.
- `data/ma_variants/`: Variantenbezogene Import-, Export- und IDA-Uebergabedaten.
- `data/ma_weather/`: lokale TRY-Eingaben, spaeter aufbereitete Wetterdaten, Diagrammausgaben, Exporte und Berichte.
- `data/catalogs/`: separater Bereich fuer Produkt-/Material-/Quellkataloge und Datenblaetter.
- `data/test_output/`: lokaler, semi-wichtiger Arbeits- und Smoke-Test-Ordner.
- `docs/project/plans/inbox/`: aktuelle, noch nicht archivierte Umsetzungsplaene.
- `docs/project/archive/plans/`: umgesetzte oder alte Plaene.
- `docs/project/architecture/`: Zielarchitektur, UI-Auslagerungsreview, UI-Migrationsplan, `ma_analyse`-Inventar und Service-Schnittstellenentwurf fuer P005.

## Staerken

- Die Quellcodepakete `ma_analyse` und `ma_variants` sind fachlich getrennt.
- Tests fuer beide Bereiche sind vorhanden.
- Die neue Dokumentationsstruktur ordnet Plaene und Modul-Dokumente klarer.
- `CHANGELOG.md` bleibt als zentrale Aenderungshistorie im Root.
- Produkt- und Materialdatenblaetter werden nicht in PostgreSQL gespeichert, sondern ueber Pfade referenziert.
- P001 bis P006 sind nach Pruefung archiviert; P008 bis P028 bilden die
  abgestuften Wetter-, Eingabe-, Analyse-, Bewertungs- und
  Querschnittsarbeiten ab.
- Reale TRY-Dateien bleiben lokal und werden nicht versioniert.
- Der zentrale Katalog prueft eindeutige Phasen, Module und Workflow-Schritte.
- Die zentrale UI verwendet Fachansichten fuer nutzbare Module und
  Informationsseiten fuer geplante Module.

## Schwachstellen

- Die Tkinter-Analyse unter `src/ma_ui/tkinter_app/module_views/analyse/app.py`
  ist sehr gross und sollte spaeter aufgeteilt werden.
- `src/ma_analyse/analysis/heating.py` und `src/ma_analyse/analysis/cooling.py` enthalten aehnliche Strukturen und sollten spaeter ueber gemeinsame Runner/Helper weiter vereinheitlicht werden.
- In `data/test_output/` liegen lokale Arbeits- und Testartefakte verschiedener Pruefungen. Der Ordner ist bewusst nicht als Referenzbereich gedacht.
- `ma_weather` benoetigt noch reale lokale Pruefungen der verbleibenden fuenf
  aktiven TRY-Jahresdatensaetze und eine fachliche Diagrammabstimmung.
- Mehrere Zielmodule enthalten bewusst noch keine Fachlogik. Gleichzeitig
  liegen Teilverantwortlichkeiten weiterhin in `ma_variants`, zum Beispiel
  Parameterkatalog, IDA-Uebergabe, Simulationsergebnisadapter und
  Wirtschaftlichkeit.
- Es gibt weiterhin mehrere UI-Bestaende: Tkinter in `ma_ui`, die
  modulbezogene Streamlit-UI in `ma_variants` und die zentrale Streamlit-UI
  `ma_ui`. `ma_ui` ist die Zieloberflaeche; Tkinter bleibt Legacy-Bestand.
- Die Kompatibilitaetswrapper unter `ma_ui/pages/` bestehen parallel zu den
  aktuellen `module_views/`; eine spaetere Bereinigung braucht einen eigenen
  Refactoring-Slice.
- Der aktuelle `ma_workflow`-Code ist noch kein vollstaendiger
  Workflow-Manager, sondern vor allem Katalog, Statusquelle und Adapter.

## Risiken

- Eine weitere GUI-Aufteilung sollte nicht parallel zu groesseren Analyse-Refactorings erfolgen.
- Die Plan-Inbox enthaelt aktive Plaene. Umgesetzte Plaene muessen konsequent nach `docs/project/archive/plans/` verschoben werden.
- Eine Zerlegung der Tkinter-Hauptdatei waere hohes Risiko, weil dort UI,
  Prozesssteuerung und Analyseoptionen eng gekoppelt sind.
- Eine direkte Vermischung von Tkinter und Streamlit wuerde die Zielarchitektur unklar machen.
- Eine zu fruehe Extraktion von `ma_parameters`, `ma_export_simulation` oder
  `ma_assessment` aus `ma_variants` kann funktionierende Tests und Importpfade
  destabilisieren.
- Eine vorschnelle Umbenennung von `ma_ui/pages/` oder `ma_workflow/actions.py`
  kann den bereits getesteten Zwischenstand unnoetig brechen.

## Empfehlungen

- P008 ueber reale Testlaeufe der verbleibenden TRY-Datensaetze, die
  fachliche Pruefung der Wetterdiagramme und die `weather_key`-Uebergabe
  weiterfuehren.
- P010 bis P018 fuer die Eingabekette, Stage 1, Variantenanbindung und das
  Run-Manifest priorisieren.
- P009 erst nach P018 fuer Referenzmodellkopie und Adapter-Mapping
  weiterfuehren; bestehendes `ma_variants.ida_export` wiederverwenden.
- P020 als Research-Plan fuer deutsche Norm-Nachweise fuehren; internationale
  Normen bleiben erweiterbare Profile.
- `data/test_output/` regelmaessig manuell leeren, aber nicht als Referenzgalerie verwenden.
- `docs/examples/plot_templates/` als wichtige Referenz fuer aktuelle `ma_analyse`-Plot-Templates behalten.
- Die aus P005 uebernommenen Restarbeiten nur in kleinen P007-Slices
  fortsetzen: Streamlit-/Tkinter-Analyse mit realen Projektdaten pruefen und
  erst danach Vorschau-Cache oder weitere Fachservice-Anbindungen planen.
- Vor jeder UI-Auslagerung zuerst `docs/project/architecture/UI_EXTRACTION_REVIEW.md` pruefen.
- Vor jeder Streamlit-Umsetzung zuerst `docs/project/architecture/UI_MIGRATION_PLAN.md` pruefen.
- Vor einer Bereinigung von `ma_ui/pages/` zuerst die bestehenden
  Kompatibilitaetsimporte und Tests erfassen.
- Vor jeder Bewertungserweiterung `ma_economy`, `ma_sustainability` und
  `ma_assessment` getrennt planen; bestehende Logik in
  `ma_variants.economic_analysis` nicht ungeprueft verschieben.
- P007 als verbindliche Strukturgrundlage pflegen; neue Fachlogik weiterhin
  nur ueber freigegebene Teilplaene umsetzen.

## Offene Fragen

- Welcher der verbleibenden TRY-Datensaetze wird als naechstes real geprueft?
- Soll als naechstes die Streamlit-/Tkinter-Analyse mit realen Projektdaten
  geprueft oder der temporaere Vorschau-Cache geplant werden?
- Welche fachlichen Felder muss das P009-Run-Manifest mindestens enthalten?
- Wann koennen die Kompatibilitaetswrapper unter `ma_ui/pages/` ohne
  Beeintraechtigung bestehender Importe und Tests bereinigt werden?
