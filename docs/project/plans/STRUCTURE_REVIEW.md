# Strukturreview

Datum der Pruefung: 2026-06-10

## Projektuebersicht

Das Projekt besteht aktuell aus zwei produktiven Python-Paketen:

- `ma_analyse`: bestehende Analysepipeline fuer IDA-ICE-Simulationsergebnisse.
- `ma_variants`: neuer Varianten-, Export-, Katalog- und Bewertungskern.

`ma_weather` ist als eigenes Paket fuer Wetterdatenanalyse und TRY-Integration vorbereitet. Der aktuelle Stand umfasst Struktur, Katalog, TRY-Importer, Validierung, Kennwerte, Diagramme, Markdown-Bericht, Runner und Tests.

P005 ergaenzt eine Zielarchitektur mit Streamlit als Zieltechnik fuer `ma_ui`,
`ma_ui_legacy` fuer bestehenden Tkinter-Bestand, `ma_workflow`,
`ma_parameters`, `ma_building`, `ma_simulation_setup`, `ma_export_ida`,
`ma_import_ida`, `ma_assessment` und `ma_feedback`. `ma_ui` und `ma_workflow`
sind als minimale Pakete vorhanden. Die uebrigen Zielmodule duerfen nicht ohne
separaten Plan angelegt oder durch Verschiebung bestehender Logik erzwungen
werden.

Die verschaerfte P005-Planung legt zusaetzlich fest: `ma_simulation_setup`
liegt zwischen Variantenbildung und IDA-Export, `ma_assessment` wird als
Bewertungsoberstruktur fuer Economics und Sustainability geplant, und die
bestehende Tkinter-GUI aus `ma_analyse` ist fachliche Ablaufvorlage, aber keine
technische Vorlage fuer Streamlit.

## Gefundene Ordnerstruktur

- `src/ma_analyse/`: Analyse, CLI, GUI, Preprocessing, Plot-Templates.
- `src/ma_variants/`: Parameter, Optionen, Varianten, Datenbank, IDA-Export, Simulationsergebnisse, Wirtschaftlichkeit, Kataloge, UI.
- `src/ma_weather/`: Wetterkatalog, TRY-Import, Validierung, Kennwerte, Plots, Reports und Runner.
- `src/ma_workflow/`: neutraler Workflow-Katalog und Analyse-Adapter.
- `src/ma_ui/`: minimale Streamlit-Shell mit Startseite, Analyse-Seite, Navigation und Projektzustand.
- Ziel fuer `src/ma_ui/`: Dashboard, Workflow-Views, `shared/`-Komponenten und
  `module_views/`. Die aktuelle `pages/`-Struktur bleibt Zwischenstand.
- Ziel fuer `src/ma_workflow/`: Workflow-Manager, Dashboard-Aktionen,
  Pre-Process-Runner, Post-Process-Runner und Feedback-Routing.
- `docs/`: wurde in `project`, `ma_analyse`, `ma_variants`, `ma_weather`, `common` und `examples` modularisiert.
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
- P001 ist nach Pruefung archiviert; P002 liegt als Markdown-Plan in der Plan-Inbox vor.
- P002 ist mit einem Struktur-Slice teilweise umgesetzt; reale TRY-Dateien bleiben lokal und werden nicht versioniert.
- P005 liegt als Architektur-, Analyse- und erster UI-/Workflow-Slice teilweise umgesetzt vor und trennt Zielbild, UI, Workflowsteuerung, Fachmodule, `ma_analyse`-Bestand und Service-Fassade.
- Die P005-Verschaerfung verhindert eine direkte Vermischung von Tkinter,
  Streamlit, Workflowsteuerung und Fachlogik.

## Schwachstellen

- `src/ma_analyse/gui/app.py` ist sehr gross und sollte spaeter aufgeteilt werden.
- `src/ma_analyse/analysis/heating.py` und `src/ma_analyse/analysis/cooling.py` enthalten aehnliche Strukturen und sollten spaeter ueber gemeinsame Runner/Helper weiter vereinheitlicht werden.
- In `data/test_output/` liegen lokale Arbeits- und Testartefakte verschiedener Pruefungen. Der Ordner ist bewusst nicht als Referenzbereich gedacht.
- `ma_weather` benoetigt noch reale lokale TRY-Pruefung und fachliche Diagrammabstimmung.
- Mehrere Zielmodule aus P005 existieren noch nicht als Code. `ma_ui` und `ma_workflow` sind nur minimale Shells. Gleichzeitig liegen Teilverantwortlichkeiten bereits in `ma_variants`, zum Beispiel Parameterkatalog, IDA-Uebergabe, Simulationsergebnisadapter und Wirtschaftlichkeit.
- Es gibt zwei unterschiedliche UI-Bestaende: Tkinter in `ma_analyse` und Streamlit in `ma_variants`. Streamlit ist nun Zieltechnik; Tkinter bleibt Legacy-Bestand.
- Der aktuelle `ma_ui`-Code nutzt noch eine einfache `pages/`-Struktur, waehrend
  die verschaerfte Zielarchitektur langfristig `module_views/` und `shared/`
  vorsieht.
- Der aktuelle `ma_workflow`-Code ist noch kein vollstaendiger Workflow-Manager,
  sondern ein erster Katalog- und Analyse-Adapter.

## Risiken

- Eine weitere GUI-Aufteilung sollte nicht parallel zu groesseren Analyse-Refactorings erfolgen.
- Die Plan-Inbox enthaelt aktive Plaene. Umgesetzte Plaene muessen konsequent nach `docs/project/archive/plans/` verschoben werden.
- Eine direkte Verschiebung von `ma_analyse/gui/app.py` in `ma_ui` waere hohes Risiko, weil dort UI, Prozesssteuerung und Analyseoptionen eng gekoppelt sind.
- Eine direkte Vermischung von Tkinter und Streamlit wuerde die Zielarchitektur unklar machen.
- Eine zu fruehe Extraktion von `ma_parameters`, `ma_export_ida` oder `ma_assessment` aus `ma_variants` kann funktionierende Tests und Importpfade destabilisieren.
- Eine vorschnelle Umbenennung von `ma_ui/pages/` oder `ma_workflow/actions.py`
  kann den bereits getesteten Zwischenstand unnoetig brechen.

## Empfehlungen

- P002 erst nach gesonderter Bestandspruefung des TRY-Plans vorbereiten.
- P002 als naechstes ueber TRY-Importer und Validierung weiterfuehren.
- `data/test_output/` regelmaessig manuell leeren, aber nicht als Referenzgalerie verwenden.
- `docs/examples/plot_templates/` als wichtige Referenz fuer aktuelle `ma_analyse`-Plot-Templates behalten.
- P005 nur in kleinen Slices fortsetzen: nach der ersten `ma_ui`-/`ma_workflow`-Shell entweder Analyse-Seite erweitern oder weitere Moduluebersichten anbinden.
- Vor jeder UI-Auslagerung zuerst `docs/project/architecture/UI_EXTRACTION_REVIEW.md` pruefen.
- Vor jeder Streamlit-Umsetzung zuerst `docs/project/architecture/UI_MIGRATION_PLAN.md` pruefen.
- Vor jeder Umstrukturierung von `ma_ui` zuerst entscheiden, ob der aktuelle
  Zwischenstand weiter ausgebaut oder auf die Zielstruktur migriert wird.
- Vor jeder Bewertungserweiterung zuerst klaeren, ob sie noch in
  `ma_variants.economic_analysis` bleibt oder als erster `ma_assessment`-Slice
  geplant wird.

## Offene Fragen

- Welche naechsten Schritte ergeben sich nach Pruefung des P002-TRY-Plans?
- Soll P005 vor P002 weitergefuehrt werden, oder bleibt P002 der naechste fachliche Umsetzungsschritt?
- Soll als naechstes die Analyse-Seite fachlich erweitert werden oder zuerst eine weitere Moduluebersicht in `ma_ui` entstehen?
- Soll die bestehende `ma_ui/pages/`-Shell vorerst bleiben oder als separater
  Slice in `module_views/` und `shared/` ueberfuehrt werden?
