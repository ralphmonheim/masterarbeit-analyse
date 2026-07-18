# Nutzerentscheidungen Masterarbeit Code

Stand: 2026-07-15

## UD-001 Modulare Projektstruktur

- Datum: 2026-06-04
- Thema: Projektorganisation
- Entscheidung: Dokumentation, Konfiguration und Datenbereiche sollen nach Modulen geordnet werden.
- Begruendung: Das Projekt wird groesser und soll nachvollziehbar bleiben.
- Auswirkung: `docs/`, `config/` und `data/` erhalten Modulbereiche fuer `ma_analyse`, `ma_variants`, `ma_weather` und gemeinsame Bereiche.
- Betroffene Module oder Dateien: `docs/`, `config/`, `data/`
- Status: getroffen
- Offene Folgefragen: keine
- Quelle oder Chatbezug: aktueller Codex-Chat zur Projektstruktur

## UD-002 PLAN_STATUS als aktive Steuerdatei

- Datum: 2026-06-04
- Thema: Planung
- Entscheidung: `PLAN_STATUS.md` ist die aktive Planungs- und Statusdatei und wird nach Modulen strukturiert.
- Begruendung: `PLAN.md` und `PLAN_STATUS.md` hatten vorher ueberlappende Aufgaben.
- Auswirkung: Der Projektplan Version 1.0.0 liegt als Plan-Dokument in der Plan-Inbox; aktive Punkte stehen in `docs/project/plans/PLAN_STATUS.md`.
- Betroffene Module oder Dateien: `docs/project/plans/`
- Status: getroffen
- Offene Folgefragen: keine
- Quelle oder Chatbezug: aktueller Codex-Chat zur Planstruktur

## UD-003 Manuelle Planablage

- Datum: 2026-06-04
- Thema: Externe Plaene
- Entscheidung: Externe Plaene werden vom Nutzer manuell in einen Planordner eingefuegt und danach in `PLAN_STATUS.md` zusammengefasst.
- Begruendung: Nicht jeder externe Plan soll automatisch umgesetzt werden.
- Auswirkung: `docs/project/plans/inbox/` dient als Eingang fuer neue Plaene.
- Betroffene Module oder Dateien: `docs/project/plans/inbox/`, `docs/project/plans/PLAN_INDEX.md`
- Status: getroffen
- Offene Folgefragen: Welche externen Plaene werden als naechstes abgelegt?
- Quelle oder Chatbezug: aktueller Codex-Chat zur Planstruktur

## UD-004 data/test_output bleibt semi-wichtig und lokal

- Datum: 2026-06-04
- Thema: Test- und Smoke-Ausgaben
- Entscheidung: `data/test_output/` enthaelt semi-wichtige lokale Prozesse und wird vom Nutzer regelmaessig manuell geleert.
- Begruendung: Der Ordner ist Arbeitsbereich, aber keine belastbare Referenzdokumentation.
- Auswirkung: Der Ordner bleibt separat und wird nicht in Modulbereiche verschoben.
- Betroffene Module oder Dateien: `data/test_output/`, `.gitignore`
- Status: getroffen
- Offene Folgefragen: Bei Bedarf vor dem Leeren wichtige Ergebnisse sichern.
- Quelle oder Chatbezug: aktueller Codex-Chat zu Testausgaben

## UD-005 Plot-Template-Beispiele sind Referenzgalerie

- Datum: 2026-06-04
- Thema: Dokumentationsbeispiele
- Entscheidung: `docs/examples/plot_template_analyse/` soll von jedem `ma_analyse`-Testbefehl das aktuellste wichtige Diagramm enthalten. Der fruehere Ordner `docs/examples/plot_templates/` wurde durch die getrennte Analyse-/Wettergalerie ersetzt.
- Begruendung: Diese Beispiele sind fuer Pruefung und Dokumentation belastbar.
- Auswirkung: `docs/examples/plot_template_analyse/` wird nicht wie `data/test_output/` behandelt.
- Betroffene Module oder Dateien: `docs/examples/plot_template_analyse/`, `docs/ma_analyse/plot_template_examples.md`
- Status: getroffen
- Offene Folgefragen: Spaetere Beispielordner fuer neue Module erst bei Bedarf anlegen.
- Quelle oder Chatbezug: aktueller Codex-Chat zu Beispielausgaben

## UD-006 Produkt- und Materialdokumente eigener Katalogbereich

- Datum: 2026-06-04
- Thema: Produkt- und Materialdaten
- Entscheidung: Produkt- und Materialdokumente werden in einem eigenen Datenbereich gefuehrt.
- Begruendung: Diese Dokumente betreffen nicht nur Varianten, sondern spaeter auch Bewertung, Quellen und Wirtschaftlichkeit.
- Auswirkung: Datenblaetter liegen unter `data/catalogs/documents/products/` und `data/catalogs/documents/materials/`.
- Betroffene Module oder Dateien: `data/catalogs/`, `config/ma_variants/products/`, `config/ma_variants/materials/`
- Status: getroffen
- Offene Folgefragen: Umgang mit echten Datenblaettern im Git-Repo klaeren.
- Quelle oder Chatbezug: aktueller Codex-Chat zur Datenstruktur

## UD-007 Harte Migration der ma_analyse-Datenpfade

- Datum: 2026-06-04
- Thema: Datenstruktur
- Entscheidung: `ma_analyse` nutzt ab jetzt die neuen Modulpfade `data/ma_analyse/ida_imports`, `data/ma_analyse/database` und `data/ma_analyse/output`; bisherige Daten werden transferiert und alte Root-Strukturen geloescht.
- Begruendung: Die Datenstruktur soll konsequent modular werden und keine parallelen Altpfade behalten.
- Auswirkung: CLI, GUI, Tests und Dokumentation verwenden keine Fallbacks auf die frueheren Root-Pfade fuer Analyse-Eingaben, Nutzdaten oder Ausgaben.
- Betroffene Module oder Dateien: `src/ma_analyse/`, `tests/`, `docs/ma_analyse/`, `data/ma_analyse/`, `.gitignore`
- Status: getroffen
- Offene Folgefragen: keine
- Quelle oder Chatbezug: aktueller Codex-Chat zur harten Datenpfadmigration

## UD-008 Codex-Routinen fuer Repo- und Planungsupdates

- Datum: 2026-06-05
- Thema: Projektorganisation
- Entscheidung: Repo-Updates und Planungsupdates werden als dokumentierte Codex-Routinen gefuehrt, nicht als eigener Python-CLI-Befehl.
- Begruendung: Git- und Planungsablaeufe bleiben kontrollierbar und fuer den Nutzer direkt nachvollziehbar.
- Auswirkung: `update repo`, `direkt update repo` und `update planung` sind in `docs/project/UPDATE_ROUTINES.md` und `docs/common/commands_common.md` dokumentiert.
- Betroffene Module oder Dateien: `docs/project/UPDATE_ROUTINES.md`, `docs/common/commands_common.md`, `docs/project/plans/IMPLEMENTATION_NOTES.md`
- Status: getroffen
- Offene Folgefragen: keine
- Quelle oder Chatbezug: aktueller Codex-Chat zu Repo-Update- und Planungsroutinen

## UD-009 Alter Root-Dokumentenordner wird entfernt

- Datum: 2026-06-05
- Thema: Datenstruktur
- Entscheidung: Der alte leere Root-Dokumentenordner wird entfernt; aktive Produkt- und Materialdatenblaetter liegen unter `data/catalogs/documents/`.
- Begruendung: Es soll keine parallele Dokumentenstruktur fuer Produkt- und Materialdaten geben.
- Auswirkung: Neue Dokumentpfade bleiben konsistent mit dem Katalogbereich.
- Betroffene Module oder Dateien: `data/catalogs/documents/`, `CHANGELOG.md`, `docs/project/plans/CLEANUP_PLAN.md`
- Status: getroffen
- Offene Folgefragen: Umgang mit echten Datenblaettern im Git-Repo klaeren.
- Quelle oder Chatbezug: aktueller Codex-Chat zur Bereinigung alter Datenstrukturen

## UD-010 Relative Cooling-Templates verwenden CSV-Rohwerte

- Datum: 2026-06-08
- Thema: ma_analyse Plot-Templates
- Entscheidung: Relative Cooling-Plot-Templates sollen `zone_energy_q_cool` exakt wie in den CSV-Dateien darstellen. Absolute Cooling-Templates sollen separat den Betrag `abs(zone_energy_q_cool)` positiv nach oben zeigen.
- Begruendung: Die relative Darstellung soll die Vorzeichenlogik der Simulation transparent zeigen und keine Werte stillschweigend umdrehen.
- Auswirkung: `cooling-year`, `cooling-month`, `cooling-week` und `cooling-day` nutzen Rohwerte; `cooling-absolute-year`, `cooling-absolute-month`, `cooling-absolute-week` und `cooling-absolute-day` nutzen Betraege.
- Betroffene Module oder Dateien: `src/ma_analyse/analysis/templates/`, `docs/ma_analyse/commands_analyse.md`, `docs/examples/plot_template_analyse/`
- Status: getroffen
- Offene Folgefragen: Soll dieselbe relative/absolute Logik spaeter auch fuer den regulaeren `cooling`-Befehl und die GUI-Auswahl gelten?
- Quelle oder Chatbezug: aktueller Codex-Chat zu Cooling-Plot-Templates

## UD-011 Website- und Portfolio-Chats ausschliessen

- Datum: 2026-06-08
- Thema: Chat-Analyse und Nutzerentscheidungen
- Entscheidung: Chats aus Codex oder Copilot zur Erstellung oder Bearbeitung einer Website fuer Portfolio und bearbeitete Projekte gehoeren nicht zur Masterarbeit und werden von der Entscheidungsanalyse ausgeschlossen.
- Begruendung: Nutzerentscheidungen fuer das Masterarbeitsprojekt sollen nicht mit Entscheidungen aus anderen Projekten vermischt werden.
- Auswirkung: Website- und Portfolio-Chats werden in `docs/project/decisions/chat_analysis/excluded_chats.md` dokumentiert und nicht in `USER_DECISIONS_MASTERTHESIS_CODE.md` ausgewertet.
- Betroffene Module oder Dateien: `docs/project/decisions/chat_analysis/`, `docs/project/decisions/USER_DECISIONS_OPEN_POINTS.md`
- Status: getroffen
- Offene Folgefragen: Konkrete Chat-Exportdateien erst nach Ablage im Repo einzeln zuordnen.
- Quelle oder Chatbezug: aktueller Codex-Chat zu Nutzerentscheidungen

## UD-012 Produkt-, Material- und Datenbankinhalte nicht versionieren

- Datum: 2026-06-08
- Thema: Produkt-, Material- und Datenbankdaten
- Entscheidung: Echte Produkt-, Material- und Datenbankinhalte werden nicht ins Git-Repo uebernommen; versioniert werden nur die Ordnerstruktur und bei Bedarf klar gekennzeichnete Beispieldaten.
- Begruendung: Das Repo soll keine echten Katalog-, Hersteller- oder Datenbankinhalte enthalten, sondern nur die Projektstruktur und reproduzierbare Beispielgrundlagen.
- Auswirkung: `data/catalogs/documents/` bleibt als Struktur erhalten; echte Datenblaetter und Datenbankinhalte werden extern abgelegt oder nur ueber Pfade/Metadaten referenziert.
- Betroffene Module oder Dateien: `data/catalogs/documents/`, `.gitignore`, spaetere Produkt- und Materialkataloge
- Status: getroffen
- Offene Folgefragen: Bei spaeteren Beispieldaten klar kennzeichnen, dass sie Test- oder Demodaten sind.
- Quelle oder Chatbezug: aktueller Codex-Chat zu Produkt- und Materialdaten

## UD-013 Relative/absolute Cooling-Logik bleibt vorerst in Templates

- Datum: 2026-06-08
- Thema: ma_analyse Cooling-Auswertung
- Entscheidung: Relative und absolute Cooling-Logik wird vorerst nur in den Plot-Templates getrennt. Der regulaere `cooling`-Befehl und die GUI-Auswahl werden noch nicht angepasst.
- Begruendung: Die Diagrammlogik soll zuerst fertig bearbeitet und geprueft werden, bevor sie in das Hauptportal uebernommen wird.
- Auswirkung: `cooling-year`, `cooling-month`, `cooling-week`, `cooling-day` und `cooling-absolute-*` bleiben die aktuelle Trennung. `python -m ma_analyse cooling ...` und die GUI behalten vorerst ihr bestehendes Verhalten.
- Betroffene Module oder Dateien: `src/ma_analyse/analysis/templates/`,
  `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/app/cli.py`,
  `src/ma_ui/tkinter_app/module_views/analyse/app.py`
- Status: getroffen
- Offene Folgefragen: Nach Abschluss der Diagrammbearbeitung pruefen, ob regulaerer Cooling-Befehl und GUI die Trennung ebenfalls erhalten sollen.
- Quelle oder Chatbezug: aktueller Codex-Chat zu Cooling-Logik

## UD-014 ma_parameters ersetzt ma_input

- Datum: 2026-06-08
- Thema: Gesamtmodulstruktur
- Entscheidung: `ma_input` wird nicht als Zielmodul verwendet. Parameter- und Optionslogik soll perspektivisch unter `ma_parameters` gefuehrt werden.
- Begruendung: Parameterdefinitionen sind fachlich mehr als reine Eingabedaten und sollen klar vom Dateieingang getrennt werden.
- Auswirkung: Bestehende Parameterlogik in `ma_variants.parameter_catalog` bleibt vorerst unveraendert; eine spaetere Extraktion nach `ma_parameters` braucht einen eigenen Plan.
- Betroffene Module oder Dateien: `src/ma_variants/parameter_catalog/`, spaeter `src/ma_parameters/`
- Status: getroffen
- Offene Folgefragen: Wann wird die Parameterlogik aus `ma_variants` herausgeloest?
- Quelle oder Chatbezug: P005 Gesamtmodulstruktur

## UD-015 ma_ui und ma_workflow als getrennte Zielmodule

- Datum: 2026-06-08
- Thema: Oberflaeche und Workflowsteuerung
- Entscheidung: `ma_ui` wird die gemeinsame Oberflaeche; `ma_workflow` wird die Orchestrierungsebene zwischen Oberflaeche und Fachmodulen.
- Begruendung: UI, Workflowsteuerung und Fachlogik sollen nicht vermischt werden.
- Auswirkung: Fachlogik bleibt in den Fachmodulen. Die minimale `ma_ui`-/`ma_workflow`-Shell ist umgesetzt und dient als Einstieg fuer spaetere Modulansichten.
- Betroffene Module oder Dateien: `src/ma_ui/`, `src/ma_workflow/`,
  `src/ma_ui/tkinter_app/module_views/analyse/`, `src/ma_variants/ui/`
- Status: getroffen
- Offene Folgefragen: Welche Fachseite wird als naechstes konkret angebunden?
- Quelle oder Chatbezug: P005 Gesamtmodulstruktur

## UD-016 ma_analyse-Fachlogik bleibt in ma_analyse

- Datum: 2026-06-08
- Thema: Analysemodul und UI-Auslagerung
- Entscheidung: Fachliche Analysefunktionen verbleiben in `ma_analyse`.
  Allgemein nutzbare UI-Bestandteile aus `ma_analyse` duerfen spaeter
  geprueft und nach Freigabe in `ma_ui` ueberfuehrt werden.
- Begruendung: Die bestehende Analysepipeline ist funktionsfaehig und soll nicht durch eine direkte GUI-Verschiebung gefaehrdet werden.
- Auswirkung: Die fruehere Tkinter-Analyse wurde zuerst dokumentarisch
  bewertet. Die Tkinter-Analyse liegt nach UD-062 unter `ma_ui.tkinter_app`;
  der alte `ma_analyse.gui`-Pfad wurde durch UD-064 entfernt.
- Betroffene Module oder Dateien: ehemals `src/ma_analyse/gui/`,
  `src/ma_ui/streamlit_app/pages/analyse.py`,
  `src/ma_ui/tkinter_app/module_views/analyse/`
- Status: historisch, durch UD-062 strukturell praezisiert und durch UD-064
  hart migriert
- Offene Folgefragen: Welche Bestandteile der Tkinter-GUI sind fachliche Analyse, welche Legacy-UI und welche neutralen Helfer?
- Quelle oder Chatbezug: P005 Gesamtmodulstruktur

## UD-017 IDA-Export, IDA-Import, Simulation-Setup, Assessment und Feedback trennen

- Datum: 2026-06-08
- Thema: Gesamtworkflow
- Entscheidung: `ma_simulation_setup`, `ma_export_ida`, `ma_import_ida`, Bewertung und `ma_feedback` werden als eigene Zielbereiche gefuehrt. Die Bewertungsstruktur wurde spaeter durch UD-036 praezisiert.
- Begruendung: Simulationsrandbedingungen, IDA-Uebergabe, Ergebnisimport, Bewertung und Rueckkopplung haben unterschiedliche Verantwortlichkeiten.
- Auswirkung: Bestehende Logik in `ma_variants.ida_export`, `ma_variants.simulation_results` und `ma_variants.economic_analysis` bleibt vorerst bestehen und wird nur als spaetere Extraktionsquelle dokumentiert.
- Betroffene Module oder Dateien: `src/ma_variants/ida_export.py`, `src/ma_variants/simulation_results.py`, `src/ma_variants/economic_analysis/`, spaeter neue Zielmodule
- Status: historisch, durch UD-043 auf allgemeine Simulationsschnittstellen
  praezisiert
- Offene Folgefragen: Nach P005-UI-Migrationsplan zuerst `ma_analyse`-Bestandsanalyse und Schnittstellenentwurf pruefen.
- Quelle oder Chatbezug: P005 Gesamtmodulstruktur, praezisiert durch UD-036

## UD-018 Streamlit als Zieltechnik fuer ma_ui

- Datum: 2026-06-08
- Thema: zentrale Oberflaeche
- Entscheidung: `ma_ui` wird als neue zentrale lokale Oberflaeche mit Streamlit umgesetzt.
- Begruendung: Streamlit passt besser zur schrittweisen Bedienoberflaeche fuer Tabellen, Diagramme, Statusanzeigen und Modulnavigation als eine direkte Erweiterung der bestehenden Tkinter-GUI.
- Auswirkung: Streamlit-Importe bleiben auf `ma_ui` begrenzt. Fachmodule liefern Services und neutrale Ergebnisse.
- Betroffene Module oder Dateien: `src/ma_ui/`, `docs/project/architecture/`
- Status: getroffen
- Offene Folgefragen: Analyse-Seite erweitern oder weitere Moduluebersichten anbinden.
- Quelle oder Chatbezug: P005 Anpassung Streamlit-Ziel-UI

## UD-019 Tkinter wird nicht mit Streamlit vermischt

- Datum: 2026-06-08
- Thema: Umgang mit bestehender Tkinter-GUI
- Entscheidung: Die bestehende Tkinter-Oberflaeche aus `ma_analyse` wird
  nicht direkt mit Streamlit vermischt. Die damalige Idee einer spaeteren
  Auslagerung nach `ma_ui_legacy` wurde durch UD-062 ersetzt.
- Begruendung: Die bestehende Arbeit soll gesichert werden, ohne die neue Streamlit-Zielarchitektur technisch zu vermischen.
- Auswirkung: Die echte Tkinter-Analyse liegt unter `ma_ui.tkinter_app`.
  Der fruehere Kompatibilitaetspfad `ma_analyse.gui` wurde durch UD-064
  entfernt.
- Betroffene Module oder Dateien: ehemals `src/ma_analyse/gui/`,
  `src/ma_ui/tkinter_app/`
- Status: historisch, durch UD-062 strukturell ersetzt und durch UD-064
  hart migriert
- Offene Folgefragen: konkrete Auslagerung erst nach Tkinter-Bestandsanalyse.
- Quelle oder Chatbezug: P005 Anpassung Streamlit-Ziel-UI

## UD-020 ma_analyse erhaelt eine UI-neutrale Service-Schnittstelle

- Datum: 2026-06-08
- Thema: Analysemodul und Service-Schnittstelle
- Entscheidung: `ma_analyse` wird ueber neutrale Modelle wie `AnalysisConfig` und `AnalysisResult` sowie eine Service-Funktion `run_analysis(config)` fuer Oberflaechen nutzbar gemacht.
- Begruendung: Streamlit, Tkinter oder andere UIs sollen dieselbe fachliche Analyse verwenden koennen, ohne Berechnungslogik in die UI zu verschieben.
- Auswirkung: Bestandsanalyse, Schnittstellenentwurf und erster Service-Code-Slice sind umgesetzt. Die minimale `ma_ui`-Analyse-Seite nutzt die Service-Fassade bereits ueber `ma_workflow`.
- Betroffene Module oder Dateien: `src/ma_analyse/services.py`,
  `src/ma_analyse/models.py`,
  `src/ma_ui/streamlit_app/pages/analyse.py`
- Status: getroffen
- Offene Folgefragen: Service-Fassade fachlich erweitern und Ergebnisobjekte detaillierter fuellen.
- Quelle oder Chatbezug: P005 Anpassung Streamlit-Ziel-UI

## UD-021 ma_simulation_setup liegt zwischen Varianten und IDA-Export

- Datum: 2026-06-10
- Thema: Gesamtworkflow
- Entscheidung: `ma_simulation_setup` wird als eigener Zielschritt zwischen `ma_variants` und `ma_export_ida` eingeordnet.
- Begruendung: Varianten legen fest, was simuliert wird. Das Simulation-Setup legt fest, wie simuliert wird, zum Beispiel Zeitraum, Zeitschritt, Szenario und Run-Metadaten.
- Auswirkung: `ma_export_ida` soll spaeter nicht selbst Variantenlogik oder Simulationsrandbedingungen definieren, sondern eine bereits konfigurierte Simulationsuebergabe vorbereiten.
- Betroffene Module oder Dateien: spaeter `src/ma_simulation_setup/`, `src/ma_export_ida/`, `src/ma_variants/`
- Status: historisch, durch UD-043 auf `ma_export_simulation` praezisiert
- Offene Folgefragen: Welche Simulationsrandbedingungen werden im ersten Slice von `ma_simulation_setup` benoetigt?
- Quelle oder Chatbezug: P005 verschaerfte Modulstruktur

## UD-022 Tkinter-GUI ist fachliche Ablaufvorlage, keine technische Vorlage

- Datum: 2026-06-10
- Thema: UI-Migration
- Entscheidung: Die bestehende Tkinter-GUI aus `ma_analyse` wird fuer den fachlichen Ablauf ausgewertet, aber nicht direkt nach Streamlit kopiert oder uebersetzt.
- Begruendung: Die Tkinter-Dateien enthalten wertvolle Bedienlogik, sind technisch aber stark mit Widgets, Messageboxen, Threads und GUI-State gekoppelt.
- Auswirkung: Streamlit-Ansichten werden neu ueber `ma_ui`, `ma_workflow`
  und UI-neutrale Fachservices aufgebaut. Tkinter liegt nach UD-062 als
  eigener UI-Zweig unter `ma_ui.tkinter_app`.
- Betroffene Module oder Dateien: `src/ma_ui/tkinter_app/module_views/analyse/`,
  `src/ma_ui/streamlit_app/module_views/analyse_view.py`,
  `src/ma_ui/tkinter_app/`
- Status: historisch, durch UD-062 strukturell praezisiert
- Offene Folgefragen: Welche konkreten GUI-Validierungen sollen in die Service-Schicht uebernommen werden?
- Quelle oder Chatbezug: P005 verschaerfte UI-Ueberfuehrung

## UD-023 ma_ui nutzt Dashboard, Workflow-Views, Shared-Komponenten und Module-Views

- Datum: 2026-06-10
- Thema: Streamlit-Zieloberflaeche
- Entscheidung: `ma_ui` soll langfristig aus Dashboard, Workflow-Ansichten, gemeinsamen UI-Komponenten und modulbezogenen Views bestehen.
- Begruendung: Die Oberflaeche soll den Gesamtworkflow fuehren, aber keine Fachlogik enthalten. Gemeinsame UI-Bausteine sollen nicht in einzelnen Modulseiten dupliziert werden.
- Auswirkung: Die Streamlit-Struktur liegt nach UD-062 unter
  `ma_ui.streamlit_app` mit `pages/`, `module_views/`, `shared/` und `state/`.
- Betroffene Module oder Dateien: `src/ma_ui/`, `docs/project/architecture/TARGET_ARCHITECTURE.md`
- Status: getroffen
- Offene Folgefragen: Wann wird die bestehende `pages/`-Shell auf die Zielstruktur migriert?
- Quelle oder Chatbezug: P005 verschaerfte Streamlit-Struktur

## UD-024 ma_assessment buendelt Economics und Sustainability

- Datum: 2026-06-10
- Thema: Bewertung
- Entscheidung: `ma_assessment` wird als Bewertungsoberstruktur fuer Wirtschaftlichkeit und Nachhaltigkeit geplant.
- Begruendung: Wirtschaftlichkeitsanalyse, betriebsbezogene Nachhaltigkeit, Produktdaten und spaetere Material-/Bauteilbezuege gehoeren fachlich zusammen, sollen intern aber getrennt bleiben.
- Auswirkung: Bestehende Wirtschaftlichkeitslogik in `ma_variants.economic_analysis` bleibt vorerst bestehen. Eine spaetere Extraktion nach `ma_assessment/economics/` erfolgt nur nach eigenem Plan.
- Betroffene Module oder Dateien: `src/ma_variants/economic_analysis/`, spaeter `src/ma_assessment/`
- Status: ueberholt durch UD-036
- Offene Folgefragen: keine, durch getrennte Zielmodule `ma_economy`, `ma_sustainability` und Berichtsschicht `ma_assessment` ersetzt.
- Quelle oder Chatbezug: P005 verschaerfte Bewertungsstruktur

## UD-025 Globaler Workflow nur auf der ma_ui-Startseite

- Datum: 2026-06-16
- Thema: Streamlit-Oberflaeche und Workflow-Dashboard
- Entscheidung: Der grafische Workflow, Workflow-Phasen, Workflow-Schritte, Dashboard-Aktionen und technische Detailtabellen sollen nur auf der `ma_ui`-Startseite erscheinen.
- Begruendung: Modulansichten sollen nicht durch globale Projektsteuerung ueberladen werden und nur den jeweils relevanten Fachbereich zeigen.
- Auswirkung: `src/ma_ui/streamlit_app/pages/home.py` bleibt der zentrale
  Ort fuer die Gesamtuebersicht; Modulviews importieren keine
  Workflow-Graph-Komponenten und zeigen keine globalen Workflow-Tabellen.
- Betroffene Module oder Dateien:
  `src/ma_ui/streamlit_app/pages/home.py`,
  `src/ma_ui/streamlit_app/module_views/`,
  `src/ma_ui/streamlit_app/workflow_graph.py`
- Status: getroffen
- Offene Folgefragen: keine
- Quelle oder Chatbezug: aktueller Codex-Chat zur Streamlit-UI-Bereinigung

## UD-026 Modulansichten zeigen nur modulbezogene Inhalte

- Datum: 2026-06-16
- Thema: Streamlit-Modulansichten
- Entscheidung: Modulbereiche in `ma_ui` zeigen nur Inhalte, die zum jeweiligen Modul gehoeren. Wenn ein Modul noch keine echte Bedienung oder Kataloganzeige besitzt, zeigt die Ansicht nur Seitentitel, Untertitel und eine blaue Hinweisbox.
- Begruendung: Platzhalterbereiche sollen nicht durch technische Ressourcenlisten oder globale Workflow-Informationen groesser wirken als sie fachlich sind.
- Auswirkung: Leere oder geplante Ansichten wie Parameter, Gebaeude, Simulation Setup, IDA Export, IDA Import und Feedback bleiben bewusst schlank; gefuellte Ansichten wie Wetterdaten, Varianten, Analyse und Bewertung behalten ihre fachlichen Inhalte.
- Betroffene Module oder Dateien:
  `src/ma_ui/streamlit_app/module_views/parameters_view.py`,
  `src/ma_ui/streamlit_app/module_views/building_view.py`,
  `src/ma_ui/streamlit_app/module_views/simulation_setup_view.py`,
  `src/ma_ui/streamlit_app/module_views/export_ida_view.py`,
  `src/ma_ui/streamlit_app/module_views/import_ida_view.py`,
  `src/ma_ui/streamlit_app/module_views/feedback_view.py`
- Status: getroffen
- Offene Folgefragen: Wann werden die leeren Modulansichten mit echten Fachservices befuellt?
- Quelle oder Chatbezug: aktueller Codex-Chat zur Streamlit-UI-Bereinigung

## UD-027 Streamlit-Analyse folgt der Tkinter-Zustandslogik

- Datum: 2026-06-16
- Thema: ma_ui Analysebedienung
- Entscheidung: Die Streamlit-Analyse soll sich fachlich an den bereits getroffenen Zustands- und Ablaufentscheidungen der bestehenden Tkinter-Analyse orientieren. Zuerst wird der Befehl gewaehlt; danach werden nur passende Folgeschritte eingeblendet, vorherige Schritte werden zusammengefasst und technische Pfade liegen unter `Erweiterte Pfade`.
- Begruendung: Die Tkinter-Oberflaeche enthaelt bereits wichtige Nutzerentscheidungen zur Bedienlogik. Streamlit soll diese fachliche Logik uebernehmen, aber nicht die Tkinter-Technik kopieren.
- Auswirkung: `src/ma_ui/streamlit_app/module_views/analyse_view.py`
  bleibt als schrittweiser Analyse-Wizard ausgelegt; die weitere P005-Arbeit
  prueft die Streamlit-Bedienung gegen den bestehenden Tkinter-Ablauf.
- Betroffene Module oder Dateien:
  `src/ma_ui/streamlit_app/module_views/analyse_view.py`,
  `src/ma_ui/tkinter_app/module_views/analyse/app.py`,
  `src/ma_analyse/services.py`
- Status: getroffen
- Offene Folgefragen: Welche weiteren Tkinter-Validierungen muessen noch in UI-neutrale Services uebernommen werden?
- Quelle oder Chatbezug: aktueller Codex-Chat zu P005 und Streamlit-Analyse

## UD-028 Tkinter-Analyse darf aus Streamlit als separates Fenster starten

- Datum: 2026-06-16
- Thema: Hybrid-Bedienung waehrend der UI-Migration
- Entscheidung: Solange die Streamlit-Analyse noch nicht alle gewuenschten
  Bedienentscheidungen der Tkinter-Analyse abbildet, darf `ma_ui` die
  Tkinter-Analyse als separates Fenster starten.
- Begruendung: Die vorhandene Tkinter-Analyse bleibt praktisch nutzbar, ohne Tkinter direkt in Streamlit einzubetten oder Fachlogik in die UI zu verschieben.
- Auswirkung: Die Hybrid-Bedienung ist eine Uebergangsloesung. Streamlit
  bleibt Haupteinstieg; Tkinter liegt getrennt unter `ma_ui.tkinter_app`.
- Betroffene Module oder Dateien:
  `src/ma_ui/streamlit_app/module_views/analyse_view.py`,
  `src/ma_ui/tkinter_app/module_views/analyse/app.py`
- Status: historisch, durch UD-062 strukturell praezisiert
- Offene Folgefragen: Wann ist die Streamlit-Analyse fachlich ausreichend, um die Legacy-Schaltflaeche zu entfernen?
- Quelle oder Chatbezug: aktueller Codex-Chat zu Streamlit und Tkinter-Analyse

## UD-029 ma_weather nutzt echte lokale TRY-Dateien

- Datum: 2026-06-16
- Thema: Wetterdatenanalyse und Testdaten
- Entscheidung: Fuer `ma_weather` werden keine synthetischen TRY-Testdateien angelegt. Echte TRY-Dateien werden vom Nutzer lokal unter `data/ma_weather/input/` bereitgestellt und im Wetterkatalog referenziert.
- Begruendung: Die Wetteranalyse soll mit realen Randbedingungsdaten geprueft werden; kuenstliche TRY-Dateien wuerden fuer die fachliche Bewertung nur begrenzt helfen.
- Auswirkung: Tests duerfen Struktur, Pflichtfelder und Pfadauflösung pruefen, aber keine echte TRY-Datei im Git-Repo voraussetzen. Reale Testlaeufe laufen lokal gegen vorhandene Dateien.
- Betroffene Module oder Dateien: `src/ma_weather/`, `config/ma_weather/datasets/example_weather_datasets.yaml`, `data/ma_weather/input/`, `.gitignore`
- Status: getroffen
- Offene Folgefragen: Welche weiteren realen TRY-Datensaetze werden als naechstes lokal durchlaufen?
- Quelle oder Chatbezug: aktueller Codex-Chat zu P002 und TRY-Dateien

## UD-030 ma_weather nutzt database fuer aufbereitete Daten und output fuer Diagramme

- Datum: 2026-06-16
- Thema: Wetterdatenpfade
- Entscheidung: `data/ma_weather/database/` ist der Bereich fuer aufbereitete Wetterdaten; `data/ma_weather/output/` ist der Bereich fuer erzeugte Wetterdiagramme.
- Begruendung: Die Begriffe sollen konsistent zur restlichen Projektstruktur sein und klar zwischen Datenbasis und grafischen Ausgaben trennen.
- Auswirkung: `processed/` wird nicht als Zielordner fuer aufbereitete Wetterdaten verwendet. Wetterdiagramme liegen nicht in `plots/`, sondern unter `output/`.
- Betroffene Module oder Dateien: `data/ma_weather/database/`, `data/ma_weather/output/`, `docs/ma_weather/`
- Status: getroffen
- Offene Folgefragen: keine
- Quelle oder Chatbezug: aktueller Codex-Chat zu ma_weather-Datenstruktur

## UD-031 TRY-Zuordnung mit vollstaendigen Kennungen ohne Kuerzel

- Datum: 2026-06-16
- Thema: TRY-Dokumentation
- Entscheidung: Die TRY-Zuordnungsdatei soll vollstaendige Datei- oder Ordnerkennungen verwenden und keine zusaetzlichen Kuerzel in der Tabelle fuehren. Nach dem Einfuegen oder Importieren neuer TRY-Dateien soll die Zuordnung aktualisiert werden.
- Begruendung: Der Nutzer liefert teilweise nur Anfangszahlen; fuer spaetere Nachvollziehbarkeit muss die Dokumentation die vollstaendige lokale Kennung enthalten.
- Auswirkung: `docs/ma_weather/try_locations.md` bleibt die zentrale Zuordnung zwischen TRY-Dateien und Staedten wie Frankfurt am Main, Muenchen und Hamburg.
- Betroffene Module oder Dateien: `docs/ma_weather/try_locations.md`, `config/ma_weather/datasets/example_weather_datasets.yaml`
- Status: getroffen
- Offene Folgefragen: Bei neuen TRY-Dateien Stadt, Jahr und vollstaendige Kennung pruefen.
- Quelle oder Chatbezug: aktueller Codex-Chat zu TRY-Zuordnung

## UD-032 Tkinter-Vorschau nutzt temporaeren Vorschauausgabeort

- Datum: 2026-06-17
- Thema: ma_analyse Tkinter-Vorschau
- Entscheidung: Das Tkinter-Vorschaufenster soll Diagramme in einem temporaeren Vorschau- oder Cachebereich erzeugen, der automatisch geleert oder ueberschrieben werden kann.
- Begruendung: Die Vorschau soll helfen, Diagramme vor dem finalen Export zu pruefen, ohne den regulaeren Output-Ordner mit vielen falschen Diagrammen zu fuellen.
- Auswirkung: Der bestehende Button `Vorschau aktualisieren` soll perspektivisch nicht direkt dauerhaft in `data/ma_analyse/output/` schreiben, sondern einen getrennten Vorschaupfad nutzen und das Ergebnis im Vorschaufenster anzeigen.
- Betroffene Module oder Dateien:
  `src/ma_ui/tkinter_app/module_views/analyse/app.py`, spaeter
  Vorschau-/Cachepfad unter `data/test_output/` oder einem dedizierten
  Temp-Bereich
- Status: getroffen
- Offene Folgefragen: Konkreten Cachepfad und Loeschregel im Umsetzungsslice festlegen.
- Quelle oder Chatbezug: aktueller Codex-Chat zu strukturellen Entscheidungen

## UD-033 Overlay-Strategie bleibt frei, feste Additionen bleiben konfigurierbar

- Datum: 2026-06-17
- Thema: ma_analyse Diagramm-Overlays
- Entscheidung: Overlays sollen grundsaetzlich frei gestaltet werden koennen. Linien oder Datenreihen aus der Datenbank sollen in die aktuelle Ansicht geladen werden koennen. Feste Additionen wie Temperaturband, Bandbreite und vorhandene Standardoptionen bleiben dagegen als eigene, klar konfigurierte Optionen gefuehrt.
- Begruendung: Freie Datenreihen sind fuer flexible Diagrammvergleiche wichtig. Gleichzeitig brauchen fachlich feste Elemente wie Sollwert- oder Temperaturbaender stabile Optionen, damit sie nicht wie beliebige Datenreihen behandelt werden.
- Auswirkung: Hauptfunktionen und Plot-Templates sollen langfristig freie Datenreihen aus lokalen Analyse-/Datenbankdaten ergaenzen koennen. Bestehende Bandlogik und Achsenbereiche bleiben kontrollierte Diagrammoptionen.
- Betroffene Module oder Dateien: `src/ma_analyse/analysis/templates/`,
  `src/ma_analyse/analysis/heating.py`,
  `src/ma_analyse/analysis/cooling.py`,
  `src/ma_ui/tkinter_app/module_views/analyse/app.py`,
  `src/ma_ui/streamlit_app/module_views/analyse_view.py`
- Status: getroffen
- Offene Folgefragen: Bedienung und Validierung fuer freie Datenreihen in Hauptfunktionen separat umsetzen.
- Quelle oder Chatbezug: aktueller Codex-Chat zu strukturellen Entscheidungen

## UD-034 Wetterdiagramme bleiben vorerst in ma_weather

- Datum: 2026-06-17
- Thema: ma_weather und Plot-Template-Struktur
- Entscheidung: Wetterdiagramme bleiben vorerst im Modul `ma_weather` und werden nicht sofort als eigener Hauptbefehl `plot-template-weather` in die `ma_analyse`-/Analyse-UI-Struktur integriert.
- Begruendung: Wetterdatenanalyse ist fachlich ein eigenes Modul mit eigener Datensatzwahl. Eine Vermischung mit `ma_analyse`-Templates wuerde die aktuelle Analysebedienung unklarer machen.
- Auswirkung: `ma_ui` zeigt Wetterdiagramme ueber die Wetterdaten-Seite. `plot-template-weather` bleibt als spaeterer Strukturpunkt offen.
- Betroffene Module oder Dateien: `src/ma_weather/`,
  `src/ma_ui/streamlit_app/module_views/weather_view.py`, spaeter optional
  `src/ma_ui/streamlit_app/module_views/analyse_view.py`
- Status: getroffen
- Offene Folgefragen: Ob `plot-template-weather` spaeter als eigener UI-Befehl eingefuehrt wird, bleibt offen.
- Quelle oder Chatbezug: aktueller Codex-Chat zu strukturellen Entscheidungen
- Hinweis 2026-06-25: Die offene Folgefrage ist durch UD-063 geschlossen.
  Wetterdiagramme bleiben fachlich in `ma_weather`, `plot-template-weather`
  ist dort aber als eigener CLI-/UI-Befehl aufgebaut.

## UD-035 Normierung soll ma_analyse-weit gedacht werden

- Datum: 2026-06-17
- Thema: ma_analyse Ausgabe- und Diagrammnormierung
- Entscheidung: Die Frage nach absoluten oder flaechenbezogen normierten Werten soll nicht nur fuer die Energiebilanz behandelt werden, sondern spaeter grundsaetzlich auf alle passenden Auswertungen unter `ma_analyse` anwendbar sein.
- Begruendung: Die Einheit und Normierung beeinflussen Vergleichbarkeit, Diagrammgestaltung und spaetere Interpretation. Eine isolierte Sonderloesung nur fuer Energy Balance wuerde die Bedienung und Dokumentation inkonsistent machen.
- Auswirkung: Kuenftige Auswertungen sollen eine einheitliche Strategie fuer absolute Werte, flaechenbezogene Werte wie `[W/m2]` und ggf. weitere Bezugsflaechen erhalten. Die konkrete Umsetzung erfolgt erst nach separater Planung.
- Betroffene Module oder Dateien: `src/ma_analyse/analysis/`,
  `src/ma_analyse/analysis/templates/`,
  `src/ma_ui/tkinter_app/module_views/analyse/app.py`,
  `src/ma_ui/streamlit_app/module_views/analyse_view.py`,
  `docs/ma_analyse/`
- Status: getroffen
- Offene Folgefragen: Welche Bezugsflaeche gilt je Auswertung, woher kommt diese Flaeche, und welche Auswertungen duerfen fachlich normiert werden?
- Quelle oder Chatbezug: aktueller Codex-Chat zu strukturellen Entscheidungen

## UD-036 Economy, Sustainability und Assessment werden getrennt geplant

- Datum: 2026-06-18
- Thema: Bewertungsarchitektur
- Entscheidung: `ma_economy` und `ma_sustainability` werden langfristig als eigene Fachmodule geplant. `ma_assessment` bleibt als uebergeordnete Bewertungs-, Scoring- und Berichtsschicht bestehen.
- Begruendung: Der spaetere Umfang von Wirtschaftlichkeit und Nachhaltigkeit ist noch nicht sicher abschaetzbar. Getrennte Fachmodule verhindern, dass ein gemeinsames Bewertungsmodul zu breit wird. `ma_assessment` kann trotzdem spaeter Ergebnisse aus Analyse, Wirtschaftlichkeit und Nachhaltigkeit zu Berichten, Scores, Rankings oder Factsheets zusammenfuehren.
- Auswirkung: `ma_assessment` wird nicht mehr als Ort fuer die eigentliche Economy- oder Sustainability-Rechenlogik verstanden. Bestehende Wirtschaftlichkeitslogik in `ma_variants.economic_analysis` bleibt vorerst bestehen und wird erst nach eigenem Plan nach `ma_economy` oder eine passende Zwischenstruktur ueberfuehrt.
- Betroffene Module oder Dateien: spaeter `src/ma_economy/`, `src/ma_sustainability/`, `src/ma_assessment/`, aktuell `src/ma_variants/economic_analysis/`, `docs/project/MASTERARBEIT_LEITFADEN.md`, `docs/project/architecture/TARGET_ARCHITECTURE.md`
- Status: getroffen
- Offene Folgefragen: Wann werden `ma_economy`, `ma_sustainability` und `ma_assessment` als Codepakete angelegt?
- Quelle oder Chatbezug: aktueller Codex-Chat zum zusammengefuehrten Masterarbeitsleitfaden

## UD-037 Economy, Sustainability und Assessment gehoeren zum Post-Process

- Datum: 2026-06-18
- Thema: Workflow-Zielarchitektur
- Entscheidung: `ma_economy`, `ma_sustainability` und `ma_assessment` gehoeren in der Zielarchitektur zum Post-Process. `ma_feedback` bleibt danach als eigener Feedback-Block bestehen.
- Begruendung: Economy, Sustainability und Assessment bauen auf importierten, aufbereiteten und analysierten Simulationsdaten auf. Feedback hat eine andere Aufgabe: Auffaelligkeiten, Rueckspruenge und Folgearbeiten in Pre-Process-Module dokumentieren.
- Auswirkung: Der Zielworkflow lautet: Pre-Process, Simulation, Post-Process mit `ma_import_ida`, `ma_analyse`, `ma_economy`, `ma_sustainability`, `ma_assessment`, danach Feedback mit `ma_feedback`.
- Betroffene Module oder Dateien: `docs/project/MASTERARBEIT_LEITFADEN.md`, `docs/project/architecture/TARGET_ARCHITECTURE.md`, spaeter `src/ma_workflow/`
- Status: historisch, durch UD-042, UD-046 und UD-047 auf Phase 5 sowie
  phasenuebergreifendes Feedback praezisiert
- Offene Folgefragen: keine
- Quelle oder Chatbezug: aktueller Codex-Chat zur Zielarchitektur

## UD-038 Manuellen und automatisierten Prozessaufwand vergleichen

- Datum: 2026-06-18
- Thema: Methodik, Prozessinnovation und Wirtschaftlichkeit
- Entscheidung: Die Masterarbeit soll abschaetzen und nach Moeglichkeit messen, welchen Zeitaufwand ein Mitarbeiter fuer den Workflow manuell, softwareunterstuetzt und automatisiert benoetigt. Unterschiedliche Wissensstaende sollen als Szenarien oder Vergleichsgruppen beruecksichtigt werden. Aus aktiver Arbeitszeit und dokumentierten Stundensaetzen kann ein Personalkostenvergleich abgeleitet werden.
- Begruendung: Der Nutzen der entwickelten Software besteht nicht nur in technischen Ergebnissen, sondern auch in Zeitersparnis, geringerer Fehleranfaelligkeit, besserer Wiederholbarkeit und strukturierter Dokumentation.
- Auswirkung: Zeitarten wie aktive Arbeitszeit, Maschinenlaufzeit, Wartezeit, Einarbeitung, Fehlerkorrektur und Wiederholungsaufwand werden getrennt betrachtet. Die Ergebnisse koennen spaeter in `ma_economy` und `ma_assessment` einfliessen.
- Betroffene Module oder Dateien: `docs/project/MASTERARBEIT_LEITFADEN.md`, spaeter `ma_economy`, `ma_assessment` und eine methodische Erfassung der Prozesszeiten
- Status: getroffen
- Offene Folgefragen: Wissensprofile, Stundensaetze, Messmethode, Stichprobengroesse und Abgrenzung des betrachteten Workflows festlegen.
- Quelle oder Chatbezug: aktueller Codex-Chat zur Ergaenzung des Masterarbeitsleitfadens

## UD-039 Aktualisieren prueft Modulumsetzung und Streamlit-Status

- Datum: 2026-06-18
- Thema: Projektpflege und zentrale UI-Statusanzeigen
- Entscheidung: Die Routine `aktualisieren` prueft kuenftig, in welchem Umfang die Workflow-Module fachlich umgesetzt sind, und gleicht die zentralen Statuswerte fuer die Streamlit-Anzeigen damit ab.
- Begruendung: Statische, mehrfach gepflegte Statusangaben werden bei wachsendem Projekt schnell widerspruechlich. Die Startseite soll den tatsaechlichen, belegbaren Umsetzungsstand zeigen.
- Auswirkung: Fachpakete, Services, Views, Tests und Dokumentation werden als Nachweise geprueft. Die Statuswerte `available`, `partial`, `planned` und `manual` werden zentral in `ma_workflow` gepflegt; Navigation und Dashboard leiten ihre Anzeige daraus ab.
- Betroffene Module oder Dateien: `docs/project/UPDATE_ROUTINES.md`, `docs/common/commands_common.md`, `src/ma_workflow/actions.py`, `src/ma_ui/navigation.py`, `src/ma_ui/workflow_graph.py`
- Status: getroffen
- Offene Folgefragen: keine
- Quelle oder Chatbezug: aktueller Codex-Chat zur Erweiterung von `aktualisieren`

## UD-040 Plot-Template-Bedienung bleibt gruppenfrei und trennt Ausgabe, Overlay und Diagrammanpassung

- Datum: 2026-06-18
- Thema: ma_analyse Plot-Template-Wizard in Tkinter und Streamlit
- Entscheidung: Alle Plot-Templates werden ohne vorgelagerte Diagrammgruppen direkt als Unterbefehle angeboten. `Template / Diagramm` enthaelt Zeitwahl, Overlay-Aktivierung und eine ausklappbare Diagrammanpassung mit Mock-up. Der optionale Overlay-Schritt folgt erst nach Varianten und Raeumen. `Export / Ausgabe` ist die letzte Abfrage vor Vorschau und Analysestart.
- Begruendung: Die Gruppen sind in der Template-Sandbox nicht erforderlich und erschweren den direkten Zugriff auf Diagramme. Der Overlay-Katalog braucht dagegen eine konkrete Variante und einen konkreten Raum. Achsenanpassungen sollen vor der echten Vorschau nachvollziehbar sein.
- Auswirkung: Tkinter nutzt eine scrollbare Template-Liste. Streamlit und Tkinter verwenden die Reihenfolge `Befehl`, `Unterbefehl`, `Template / Diagramm`, `Varianten`, `Raeume`, optional `Overlay`, `Export / Ausgabe`, Aktionsbereich. Automatische Achsengrenzen sind Standard; manuelle Grenzen fuer primaere und sekundaere Y-Achsen sind moeglich. Als Overlay-Katalogreferenz dienen sichtbar die erste gewaehlte Variante und der erste Raum.
- Ausgabedefinition: `single` erzeugt fuer jede Variante-Raum-Kombination ein eigenes Diagramm. `compare` erzeugt eine gemeinsame Vergleichsausgabe; Zeitreihen werden als gemeinsame Datenreihen gezeichnet, komplexe Sammeltemplates als Teilplots in einer gemeinsamen Grafik gebuendelt.
- Betroffene Module oder Dateien: `src/ma_analyse/analysis_wizard.py`,
  `src/ma_analyse/analysis_ui.py`,
  `src/ma_analyse/analysis/templates/`,
  `src/ma_ui/tkinter_app/module_views/analyse/app.py`,
  `src/ma_ui/streamlit_app/module_views/analyse_view.py`,
  `docs/ma_ui/`, `docs/ma_analyse/`
- Status: umgesetzt
- Offene Folgefragen: Weitere Diagrammoptionen wie Farben, Linienstile, Legendenposition und Beschriftungen spaeter auf Basis gemeinsamer Renderer planen.
- Quelle oder Chatbezug: aktueller Codex-Chat zur Plot-Template-Bedienung
- Hinweis 2026-06-25: Die Reihenfolge wurde angepasst. Der optionale
  Overlay-Schritt folgt nun direkt nach `Template / Diagramm`; nur der
  Overlay-Katalog wird erst nach Varianten- und Raumauswahl befuellt.

## UD-041 P007 ist verbindlicher Rahmenplan fuer die VS-Code-Umsetzung

- Datum: 2026-06-21
- Thema: Gesamtprojektplanung und Umsetzungsreihenfolge
- Entscheidung: Der Projektplan P007 ist die verbindliche Planungsgrundlage fuer die weitere Entwicklung. Seine Modulstruktur ist eine fachliche Zielstruktur und darf nicht ungeprueft als parallele neue Ordnerstruktur angelegt werden. Fuer groessere Aenderungen gilt die Reihenfolge Analyse, Planung, Freigabe, Umsetzung, Test und Dokumentation.
- Begruendung: Die vorhandene Projektstruktur und bereits umgesetzte Logik sollen erhalten und kontrolliert in das erweiterte Zielbild eingeordnet werden.
- Auswirkung: Der erste P007-Schritt ist Arbeitspaket 1 Bestandsanalyse. Neue Zielmodule, Verschiebungen oder Umbenennungen benoetigen danach einen konkreten Plan und eine separate Freigabe.
- Betroffene Module oder Dateien: `docs/project/plans/inbox/Masterarbeit_VSCode_Projektplan_2026-06-21.md`, `docs/project/plans/PLAN_INDEX.md`, `docs/project/plans/PLAN_STATUS.md`, spaeter gesamtes Projekt
- Status: getroffen
- Offene Folgefragen: keine; Modulnamen und Phasenmodell sind durch UD-042 und UD-043 geklaert.
- Quelle oder Chatbezug: Nutzerauftrag `plan aufnehmen` und anschliessende Freigabe am 2026-06-21

## UD-042 Phase 0 und sechs fachliche Hauptphasen

- Datum: 2026-06-21
- Thema: Gesamtworkflow und Dashboard
- Entscheidung: Die aktive Workflow-Struktur besteht aus Phase 0 als technischer Plattform sowie den sechs fachlichen P007-Hauptphasen. Diese Struktur ersetzt die bisherige aktive Gliederung in Pre-Process, Simulation, Post-Process und Feedback.
- Begruendung: Technische Infrastruktur und fachlicher Arbeitsablauf werden klar getrennt, waehrend die fachlichen Phasen direkt dem Masterarbeitsprozess entsprechen.
- Auswirkung: `ma_workflow`, Dashboard, Navigation, Leitfaden und Zielarchitektur verwenden Phase 0 bis Phase 6.
- Betroffene Module oder Dateien: `src/ma_workflow/`, `src/ma_ui/`, P007, Leitfaden und Zielarchitektur
- Status: getroffen
- Offene Folgefragen: keine
- Quelle oder Chatbezug: gemeinsamer P007-Abgleich am 2026-06-21

## UD-043 Allgemeine Simulationsschnittstellen mit IDA-ICE-Adaptern

- Datum: 2026-06-21
- Thema: Export- und Importarchitektur
- Entscheidung: Die kanonischen Zielmodule heissen `ma_export_simulation` und `ma_import_simulation`. IDA ICE wird jeweils ueber `adapters/ida_ice` angebunden. Historische IDA-spezifische Schluessel bleiben nur als dokumentierte Uebergangsaliase bestehen.
- Begruendung: Die Kernarchitektur bleibt simulationsprogrammunabhaengig, ohne die Masterarbeit um eine echte Mehrprogrammunterstuetzung zu erweitern.
- Auswirkung: P006 wird archiviert; P009 fuehrt die verbleibende IDA-Adapterarbeit weiter und verwendet den bestehenden Basisexport wieder.
- Betroffene Module oder Dateien: `src/ma_export_simulation/`, `src/ma_import_simulation/`, `src/ma_workflow/`, P009
- Status: getroffen
- Offene Folgefragen: konkrete verifizierte IDA-Dateiformate, Mappings und Schnittstellen
- Quelle oder Chatbezug: gemeinsamer P007-Abgleich am 2026-06-21

## UD-044 Getrennte Eingabemodule und zentrale Parameterquelle

- Datum: 2026-06-21
- Thema: Eingangsdaten und Modulgrenzen
- Entscheidung: `ma_building`, `ma_zones` und `ma_technical` bleiben getrennte Fachmodule. Zusammen mit `ma_weather` liefern sie ihre validierten Daten an `ma_parameters`. `ma_variants` bezieht fachliche Eingaben ausschliesslich aus `ma_parameters`.
- Begruendung: Geometrie, Nutzung, technische Systeme und Variantenerzeugung besitzen unterschiedliche Datenlogiken und Verantwortlichkeiten.
- Auswirkung: Direkte langfristige Abhaengigkeiten von `ma_variants` zu den Eingabefachmodulen werden ausgeschlossen.
- Betroffene Module oder Dateien: spaeter `ma_building`, `ma_zones`, `ma_technical`, `ma_weather`, `ma_parameters`, `ma_variants`
- Status: getroffen
- Offene Folgefragen: konkrete Datenmodelle und Uebergabeformate
- Quelle oder Chatbezug: gemeinsamer P007-Abgleich am 2026-06-21

## UD-045 Leichte Zielpakete und klickbare Modul-Infoseiten

- Datum: 2026-06-21
- Thema: Sichtbarkeit der Gesamtstruktur
- Entscheidung: Alle bestaetigten Zielmodule werden frueh als leichte importierbare Pakete angelegt. Der zentrale Katalog beschreibt Zweck, Ein- und Ausgaben, Abgrenzung, Abhaengigkeiten, Status und naechsten Schritt. Noch nicht umgesetzte Module erhalten klickbare Infoseiten ohne funktionslose Bedienfelder.
- Begruendung: Die Gesamtstruktur soll in Code, Dokumentation und Dashboard vollstaendig nachvollziehbar sein, ohne einen fachlichen Reifegrad vorzutaeuschen.
- Auswirkung: Paketexistenz allein aendert keinen Modulstatus. Services, Modelle und Konfigurationen entstehen erst mit konkreten Fachslices.
- Betroffene Module oder Dateien: `src/`, `docs/`, `src/ma_workflow/`, `src/ma_ui/`
- Status: getroffen
- Offene Folgefragen: keine
- Quelle oder Chatbezug: gemeinsamer P007-Abgleich am 2026-06-21

## UD-046 Validation und Feedback sind phasenuebergreifend

- Datum: 2026-06-21
- Thema: Validierung, Freigabe und Iteration
- Entscheidung: Fachmodule pruefen ihre Inhalte lokal. `ma_validation` sammelt Pruefergebnisse und verwaltet moduluebergreifende Freigaben. `ma_feedback` klassifiziert Auffaelligkeiten und steuert Rueckspruenge aus allen Phasen.
- Begruendung: Pruefungen und Iterationen treten mehrfach auf und sind keine einmaligen sequenziellen Endschritte.
- Auswirkung: Dashboard und Workflow zeigen beide Module in einem eigenen phasenuebergreifenden Bereich.
- Betroffene Module oder Dateien: `ma_validation`, `ma_feedback`, `ma_workflow`, `ma_ui`
- Status: getroffen
- Offene Folgefragen: konkrete Freigabestufen und Ruecksprungregeln
- Quelle oder Chatbezug: gemeinsamer P007-Abgleich am 2026-06-21

## UD-047 Assessment, Reporting, Datenexport und Dokumentation bleiben getrennt

- Datum: 2026-06-21
- Thema: Ergebnisverarbeitung und Dokumentation
- Entscheidung: `ma_assessment` bewertet und aggregiert Ergebnisse, `ma_reporting` erzeugt menschlich lesbare Berichte und Factsheets, `ma_data_export` paketiert maschinenlesbare Daten. Die Projektdokumentation bleibt unter `docs` und wird nicht als leeres Python-Paket angelegt.
- Begruendung: Bewertung, Darstellung, Datenaustausch und Projektsteuerung haben unterschiedliche Verantwortlichkeiten.
- Auswirkung: Phase 6 fuehrt Reporting, Datenexport und Dokumentations-/Archivierungsaktivitaeten getrennt.
- Betroffene Module oder Dateien: `ma_assessment`, `ma_reporting`, `ma_data_export`, `docs/`
- Status: getroffen
- Offene Folgefragen: konkrete Berichtsvorlagen und Exportformate
- Quelle oder Chatbezug: gemeinsamer P007-Abgleich am 2026-06-21

## UD-048 Alte Plaene unveraendert archivieren und ueber Teilplaene fortfuehren

- Datum: 2026-06-21
- Thema: Planhistorie
- Entscheidung: P002, P005 und P006 werden unveraendert archiviert. P007 uebernimmt die verbindliche Struktur. P008 fuehrt Wetter-Restarbeiten weiter; P009 fuehrt die allgemeinen Simulationsschnittstellen und IDA-Adapter weiter.
- Begruendung: Historische Entscheidungen bleiben nachvollziehbar, waehrend aktive Plaene keine ueberholten Strukturannahmen enthalten.
- Auswirkung: Planindex und Planstatus unterscheiden klar zwischen Archiv, Rahmenplan und aktiven Teilplaenen.
- Betroffene Module oder Dateien: `docs/project/archive/plans/`, P007, P008, P009
- Status: getroffen
- Offene Folgefragen: keine
- Quelle oder Chatbezug: gemeinsamer P007-Abgleich am 2026-06-21

## UD-049 Eingabekette bis ma_simulation_setup hat Vorrang

- Datum: 2026-06-22
- Thema: Masterarbeitsumfang und Umsetzungsreihenfolge
- Entscheidung: Die funktionsfaehige Eingabekette fuer Randbedingungen,
  zentrale Parameter, Stage 1, Varianten und `ma_simulation_setup` hat Vorrang
  vor einer vertieften Exportautomatisierung.
- Begruendung: Diese Schritte bilden den wissenschaftlich und praktisch
  relevanten Kern. Direkte Modellmanipulation wuerde den Rahmen der
  Masterarbeit voraussichtlich sprengen.
- Auswirkung: P010 bis P018 werden vor P009 priorisiert.
- Betroffene Module oder Dateien: P007 bis P018
- Status: getroffen
- Offene Folgefragen: konkrete Importformate stehen in OP-013.
- Quelle oder Chatbezug: aktueller Codex-Chat zum weiteren Strukturplan

## UD-050 Import je Modul bevorzugen, manuell und Demo als Alternativen

- Datum: 2026-06-22
- Thema: Eingabefunktionen und UI
- Entscheidung: Die Eingabequelle wird je Fachmodul gewaehlt. Import wird
  bevorzugt; manuelle Eingabe und Demo-Daten bleiben verfuegbar, wenn kein
  geeigneter Import vorliegt.
- Begruendung: Gebaeude, Wetter, technische Daten, Parameter und Naming haben
  unterschiedliche realistische Quellen.
- Auswirkung: P010 und P027 planen Quellenwahl, Diagnose, Validierung und
  manuelle Ergaenzung gemeinsam.
- Betroffene Module oder Dateien: P010 bis P015, P017, P027
- Status: getroffen
- Offene Folgefragen: konkrete Formatmatrix und Pflichtimporte.
- Quelle oder Chatbezug: aktueller Codex-Chat zum Input-MVP

## UD-051 Building und Zones mindestens konzeptuell mit Demo

- Datum: 2026-06-22
- Thema: Gebaeude- und Zoneninput
- Entscheidung: `ma_building` und `ma_zones` werden fuer die Masterarbeit
  mindestens konzeptuell und mit Demo-Datensaetzen aufgebaut. Eine
  formatneutrale Importarchitektur wird vorgesehen; IFC-Lite bleibt offen.
- Begruendung: Die vorhandene IFC-Datei besitzt je Arbeitsstand
  unterschiedliche Inhalte. Eine allgemeine IFC- oder CAD-Loesung ist nicht
  verlaesslich innerhalb des Masterarbeitsrahmens.
- Auswirkung: P012 und P013 trennen sichere Demo-Funktionen von optionalen
  Importadaptern.
- Betroffene Module oder Dateien: ma_building, ma_zones, P012, P013
- Status: getroffen
- Offene Folgefragen: OP-012.
- Quelle oder Chatbezug: aktueller Codex-Chat zur IFC-Rolle

## UD-052 Stage 1 startet vereinfacht und bleibt ausbaubar

- Datum: 2026-06-22
- Thema: Referenzdimensionierung
- Entscheidung: Stage 1 setzt zuerst transparente vereinfachte Verfahren fuer
  Heizlast, Kuehllast und Luftmengen um und bereitet einen Ausbau zu
  ausfuehrlicheren oder normnaeheren Verfahren vor.
- Begruendung: Eine nachvollziehbare Lite-Berechnung ist im
  Masterarbeitsrahmen realistisch und kann gegen IDA-Referenzwerte
  plausibilisiert werden.
- Auswirkung: P016 trennt Lite-Verfahren und spaetere Ausbaustufe.
- Betroffene Module oder Dateien: ma_analyse.stage_1_dimensioning, P016
- Status: getroffen
- Offene Folgefragen: konkrete Verfahren und Toleranzen.
- Quelle oder Chatbezug: aktueller Codex-Chat zur Stage-1-Tiefe

## UD-053 Analysestufen und Abschlussmodule werden abgestuft umgesetzt

- Datum: 2026-06-22
- Thema: Analyse, Bewertung und Reporting
- Entscheidung: Stage 2 nutzt vorhandene Optimierungsbefehle. Stage 3 heisst
  `ma_analyse.stage_3_standards_compliance` und fuehrt Norm-Nachweise fuer
  deutsche, spaeter internationale Normenprofile aus. Stage 4 verbindet
  kritische Wetterereignisse mit vorhandenen Zeitfensteranalysen. Economy und
  Sustainability erhalten kleine Demos; Assessment, Reporting und Datenexport
  bleiben zunaechst konzeptuell.
- Begruendung: Der Funktionsumfang wird auf wissenschaftlich relevante und
  realistisch umsetzbare Teile begrenzt.
- Auswirkung: P019 bis P026 bilden die abgestufte Planserie.
- Betroffene Module oder Dateien: ma_analyse, ma_economy, ma_sustainability,
  ma_assessment, ma_reporting, ma_data_export
- Status: getroffen
- Offene Folgefragen: konkrete Normenmatrix, Emissionsfaktoren und
  Bewertungsmethoden.
- Quelle oder Chatbezug: aktueller Codex-Chat zu Stufe 2 bis 4 und
  Abschlussmodulen

## UD-054 Fachstatus bewertet den Gesamtworkflow

- Datum: 2026-06-22
- Thema: Modulstatus und Streamlit-Infokarten
- Entscheidung: Nur `ma_weather`, `ma_analyse` und die darin teilweise
  umgesetzte Stage 2 erhalten den Fachstatus `partial`. Alle weiteren
  Software- und Fachmodule bleiben trotz vorhandener Gerueste oder Prototypen
  `planned`. Nur die Projektdokumentation ist organisatorisch `available`;
  IDA ICE bleibt `manual`.
- Begruendung: Der Status soll die fachliche Nutzbarkeit im
  Masterarbeitsworkflow und nicht die blosse Existenz von Code oder Paketen
  ausdruecken.
- Auswirkung: Dashboard, Navigation, Infokarten, Zielarchitektur und
  Planstatus verwenden die strengere Einstufung.
- Betroffene Module oder Dateien: `ma_workflow`, `ma_ui`, P007,
  Zielarchitektur und Leitfaden
- Status: getroffen
- Offene Folgefragen: Ein separater technischer Reifegrad kann spaeter geplant
  werden.
- Quelle oder Chatbezug: aktueller Codex-Chat zu Modulstatus und Infokarten

## UD-055 Projekt-, Parameter- und Benennungsverantwortung

- Datum: 2026-06-23
- Thema: Simulationsprogramme, Parameter, Naming und Vorlagen
- Entscheidung: `ma_project` verwaltet eine frei erweiterbare
  Simulationsprogrammliste und neutrale Varianten-Benennungsprofile.
  `ma_parameters` verwaltet Parameterdefinitionen, Optionsgruppen und
  ausgewaehlte Werte. `ma_variants` erzeugt Varianten und wendet den
  referenzierten Benennungsstand nur an. Produkt- und Materialbezeichnungen
  bleiben neutrale Katalogdaten; programmspezifische Objekt- und Exportcodes
  gehoeren in die jeweiligen Adapter.
- Begruendung: Fachlich neutrale Bezeichnungen duerfen nicht an IDA ICE oder
  ein anderes Simulationsprogramm gekoppelt werden.
- Auswirkung: P011, P015, P017 und P028 trennen Konfiguration, Parameterquelle,
  Variantenerzeugung und Adaptermapping.
- Betroffene Module oder Dateien: `ma_project`, `ma_parameters`,
  `ma_variants`, `ma_core`, Simulationsadapter
- Status: getroffen
- Offene Folgefragen: Die optionale Projektkennung im Variantennamen bleibt
  eine Zukunftsidee und ist nicht Teil von P028.
- Quelle oder Chatbezug: aktueller Codex-Chat zu Demo-Parametern und Naming

## UD-056 Vorlagen bleiben unveraendert und Formate erweiterbar

- Datum: 2026-06-23
- Thema: Speichern eigener Konfigurationen
- Entscheidung: Versionierte Vorlagen werden niemals ueberschrieben. Eigene
  Arbeitsstaende liegen lokal in den verantwortlichen Modulpfaden. Existiert
  ein gewaehlter neuer Dateiname bereits, muss der Nutzer einen anderen Namen
  auswaehlen. YAML wird fuer den ersten Slice verwendet, darf spaeter aber
  durch weitere Formate ergaenzt oder ersetzt werden.
- Begruendung: Vorlagen sollen reproduzierbar bleiben; Dateikollisionen und
  Formatwechsel muessen bewusst und nachvollziehbar behandelt werden.
- Auswirkung: P010 und P028 verlangen Vorlagenschutz, bestaetigtes
  Ueberschreiben eigener Dateien, neue Namen bei Kollisionen und
  formatneutrale Fachservices.
- Betroffene Module oder Dateien: `ma_core`, `ma_project`, `ma_parameters`,
  `ma_ui`, lokale Modulkonfigurationen
- Status: getroffen
- Offene Folgefragen: konkrete zusaetzliche Speicher- und Importformate werden
  spaeter je Modul entschieden.
- Quelle oder Chatbezug: aktueller Codex-Chat zur Plananpassung

## UD-057 Warnungen erhalten IDs und einen Sitzungsnachweis

- Datum: 2026-06-23
- Thema: Eingabediagnose und Freigabe
- Entscheidung: Warnungen, Fehler, Laeufe und Freigabeentscheidungen erhalten
  automatisch eindeutige IDs. Neben der ID werden Problem, Fundstelle,
  getroffene Auswahl, resultierender Status und eine optionale Notiz in einem
  lokalen Sitzungslog dokumentiert. Streamlit haelt die aktuelle Entscheidung
  zugleich im Sitzungszustand.
- Begruendung: Warnungen sollen nicht nur angezeigt, sondern einem konkreten
  Lauf und einer nachvollziehbaren Entscheidung zugeordnet werden koennen.
- Auswirkung: P010 verwendet append-only JSONL-Protokolle unter
  `logs/sessions/`; bestehende Analyse-Textlogs bleiben erhalten.
- Betroffene Module oder Dateien: `ma_core`, `ma_validation`, `ma_weather`,
  `ma_ui`, `logs/`
- Status: umgesetzt
- Offene Folgefragen: Spaetere Fachmodule entscheiden in ihren Plaenen,
  welche zusaetzlichen Ereignisse sie protokollieren.
- Quelle oder Chatbezug: aktueller Codex-Chat zur P010-Umsetzung

## UD-058 ma_weather nutzt Stadtwahl, UI-Karte und bewusste Freigabe

- Datum: 2026-06-24
- Thema: ma_weather Auswahl, UI und Freigabe
- Entscheidung: Die Stadt ist der primaere Auswahlpunkt fuer Wetterdaten.
  Klimaregion und TRY-Referenzstandort werden automatisch ermittelt. Die
  Klimaregionenkarte liegt im UI-Assetbereich. TRY-Referenzdatensaetze stehen
  als Empfehlung vor standortgenauen Datensaetzen; standortgenaue
  Wetterdaten duerfen zusaetzlich angeboten werden. Gueltige Importe werden
  nicht automatisch aktiviert und aktivierte Datensaetze werden nicht
  automatisch Projekt-Default.
- Begruendung: Wetterauswahl, fachliche Referenzlogik und Freigabe sollen fuer
  den Nutzer nachvollziehbar bleiben und keine stillschweigenden
  Ersatzzuordnungen erzeugen.
- Auswirkung: `ma_weather` trennt Referenzstandort und standortgenaue
  Datensaetze. Streamlit zeigt Karte, Stadt, Klimaregion, Referenzstandort,
  Datensatzstatus, Aktivierung und Projekt-Default bewusst in der Wetterseite.
- Betroffene Module oder Dateien: `src/ma_weather/`,
  `src/ma_ui/streamlit_app/pages/weather.py`,
  `src/ma_ui/assets/weather/`, `config/ma_weather/`
- Status: umgesetzt
- Offene Folgefragen: Fachliche Ergaenzung weiterer TRY-Referenzstandorte und
  realer Standortdatensaetze.
- Quelle oder Chatbezug: aktueller Codex-Chat zu P008 ma_weather Slices 1 bis 3

## UD-059 Sommer- und Winter-TRY-Dateien sind eigene Wetterdatensaetze

- Datum: 2026-06-24
- Thema: ma_weather Datensatztypen und kritische Wetterereignisse
- Entscheidung: Jahres-, Sommer- und Winter-TRY-Dateien werden als getrennte
  Wetterdatensaetze gefuehrt. Kritische Wetterereignisse werden immer aus dem
  bewusst ausgewaehlten Datensatz abgeleitet und nicht automatisch ueber
  Jahr, Sommer und Winter gemischt.
- Begruendung: Sommer- und Winterdateien sind fachlich eigene
  Randbedingungen. Die spaetere P021-Nutzung muss eindeutig auf den
  ausgewaehlten Wetterdatensatz rueckfuehrbar bleiben.
- Auswirkung: Der Wetterkatalog fuehrt Datensatztypen. `ma_weather` liefert
  strukturierte Ereignisse mit Wetterdatensatzbezug; Streamlit zeigt die
  Ereignisse nur als Vorbereitung fuer P021 und uebergibt sie noch nicht
  automatisch.
- Betroffene Module oder Dateien: `config/ma_weather/datasets/`,
  `src/ma_weather/weather_events.py`, `src/ma_weather/run_weather_analysis.py`,
  `src/ma_ui/streamlit_app/pages/weather.py`
- Status: umgesetzt
- Offene Folgefragen: Fachliche Feinschaerfung der Ereignisdefinitionen und
  spaetere P021-Anbindung.
- Quelle oder Chatbezug: aktueller Codex-Chat zu P008 ma_weather Slice 4

## UD-060 ma_weather Importbutton liegt im Wetterdatensatzbereich

- Datum: 2026-06-24
- Thema: ma_weather UI und lokaler Wetterdatenimport
- Entscheidung: Der Import eigener Wetterdatensaetze wird unten im Bereich
  `Wetterdatensaetze` gefuehrt. Dort steht zuerst der Importbutton, danach
  folgt die Uebersicht der aktiven Wetterdatensaetze und anschliessend eine
  getrennte Uebersicht fuer offene Wetterdatensaetze.
- Begruendung: Die Standort- und Wetterauswahl oben bleibt schlank. Import,
  aktiver Bestand und offene Nacharbeit gehoeren fachlich zur
  Datensatzverwaltung.
- Auswirkung: Streamlit zeigt den Importdialog nicht in der oberen
  Stadt-/Datensatzauswahl. Lokale Imports werden projektlokal abgelegt und
  in einem lokalen, nicht versionierten Wetterkatalog registriert.
- Betroffene Module oder Dateien:
  `src/ma_ui/streamlit_app/pages/weather.py`,
  `src/ma_weather/weather_imports.py`, `src/ma_weather/weather_catalog.py`,
  `data/ma_weather/input/custom/`,
  `data/ma_weather/config/datasets/weather_datasets_local.yaml`
- Status: umgesetzt
- Offene Folgefragen: ZIP-Import, automatische DWD-Downloads und neue
  Standortpflege bleiben spaetere Slices.
- Quelle oder Chatbezug: aktueller Codex-Chat zu P008 ma_weather Slice 5

## UD-061 Datenvorbereitung als eigener Workflow-Schritt

- Datum: 2026-06-24
- Thema: ma_analyse Workflow und Analysestufen
- Entscheidung: `prepare` und `analyze-data` werden fachlich als eigener
  Workflow-Schritt `Datenvorbereitung` zwischen Simulationsergebnisimport und
  Analyse Stufe 2 eingeordnet. Die Logik bleibt weiterhin in `ma_analyse`,
  aber der Schritt steht neben den Analysestufen 1 bis 4.
- Begruendung: `prepare` erzeugt die nutzbare Datenbasis und `analyze-data`
  den Basisbericht. Beides ist Voraussetzung fuer die spaetere Analyse und
  keine Optimierungs-, Norm- oder Sensitivitaetsauswertung.
- Auswirkung: `ma_workflow` fuehrt `ma_analyse.data_preparation` als eigenen
  Schritt in Phase 4. Stage 2 haengt fachlich von der Datenvorbereitung ab.
- Betroffene Module oder Dateien: `src/ma_workflow/`,
  `src/ma_analyse/data_preparation/`, `docs/ma_analyse/`,
  `docs/project/architecture/TARGET_ARCHITECTURE.md`
- Status: getroffen
- Offene Folgefragen: Nach erfolgreichem Simulationsergebnisimport soll
  `prepare` als Standard-Folgeschritt angeboten oder automatisiert werden;
  `analyze-data` bleibt als sichtbarer Basisbericht konfigurierbar.
- Quelle oder Chatbezug: aktueller Codex-Chat zur Einordnung von `prepare`
  und `analyze-data`

## UD-062 Streamlit und Tkinter als UI-Zweige unter ma_ui

- Datum: 2026-06-24
- Thema: UI-Struktur und Fachmodulansichten
- Entscheidung: `ma_ui` fuehrt Streamlit und Tkinter als getrennte,
  gleichwertig eingeordnete UI-Zweige. Streamlit bleibt der aktuelle
  Haupteinstieg. Tkinter wird nicht nur als Analyse-Legacy behandelt, sondern
  strukturell so eingeordnet, dass spaeter weitere Fachmodulansichten ergaenzt
  werden koennen.
- Begruendung: Die UI-Technologien sollen technisch getrennt bleiben, aber
  beide gehoeren zur Bedienoberflaeche und nicht in den Fachkern
  `ma_analyse`. `ma_analyse` bleibt dadurch UI-neutraler, waehrend bestehende
  Tkinter-Funktionalitaet kompatibel erreichbar bleibt.
- Auswirkung: Die Streamlit-Logik liegt unter `ma_ui.streamlit_app`.
  `src/ma_ui/app.py` bleibt stabiler Streamlit-Einstieg. Die Tkinter-Analyse
  liegt unter `ma_ui.tkinter_app.module_views.analyse`. Alte
  `ma_analyse.gui.*`-Importe wurden durch UD-064 entfernt.
- Betroffene Module oder Dateien: `src/ma_ui/app.py`,
  `src/ma_ui/streamlit_app/`, `src/ma_ui/tkinter_app/`,
  ehemals `src/ma_analyse/gui/`, `docs/ma_ui/`,
  `docs/project/architecture/`
- Status: umgesetzt, durch UD-064 verschaerft
- Offene Folgefragen: Welche weiteren Fachmodule spaeter eine Tkinter-Ansicht
  erhalten, wird nur ueber eigene Fachslices entschieden.
- Quelle oder Chatbezug: aktueller Codex-Chat zum kombinierten
  UI-Strukturumzug nach `ma_ui`

## UD-063 plot-template-weather wird als ma_weather-Befehl aufgebaut

- Datum: 2026-06-25
- Thema: ma_weather, ma_ui und Wetterdiagramme
- Entscheidung: `plot-template-weather` wird als eigener Wetter-Template-
  Befehl in `ma_weather` aufgebaut. Er erhaelt einen Diagramm-Katalog fuer
  `all` und die vorhandenen einzelnen Wetterdiagramme. Die Streamlit-Wetterseite
  delegiert diesen Befehl an `ma_weather`; `ma_analyse` wird dafuer nicht
  erweitert.
- Begruendung: Wetterdiagramme gehoeren fachlich zu Wetterdaten und nicht zur
  IDA-Zonenergebnisanalyse. Der eigene Befehl macht die Diagrammauswahl
  trotzdem sichtbar und testbar, ohne die Analyse-Navigation fachlich zu
  vermischen.
- Auswirkung: `plot-template-weather <diagramm> --weather-key ...` ist ein
  eigener CLI-Einstieg. Streamlit bietet die Auswahl `Alle Wetterdiagramme`
  oder einen einzelnen Diagramm-Schluessel im Wettermodul an.
- Betroffene Module oder Dateien: `src/ma_weather/weather_plots.py`,
  `src/ma_weather/run_weather_analysis.py`,
  `src/ma_ui/streamlit_app/pages/weather.py`, `pyproject.toml`,
  `docs/ma_weather/commands_weather.md`
- Status: umgesetzt
- Offene Folgefragen: Ob spaeter weitere Wetterdiagramme oder Wetter-Templates
  hinzukommen, wird ueber den Wetterdiagramm-Katalog erweitert.
- Quelle oder Chatbezug: aktueller Codex-Chat zur UI-/Workflow-Anpassung

## UD-064 ma_analyse.gui-Kompatibilitaet wird entfernt

- Datum: 2026-06-28
- Thema: Harte Tkinter-Migration aus `ma_analyse`
- Entscheidung: `ma_analyse` fuehrt keinen `gui`-Unterbefehl und kein
  `ma_analyse.gui.*`-Paket mehr. Die Tkinter-Analyse wird ausschliesslich ueber
  `ma_ui.tkinter_app.module_views.analyse` und den Streamlit-Launcher
  gestartet.
- Begruendung: Tkinter gehoert zur Bedienoberflaeche und nicht in den
  fachlichen Analyse-Kern. Der harte Schnitt reduziert doppelte Startpfade und
  macht die Grenze zwischen `ma_ui` und `ma_analyse` eindeutiger.
- Auswirkung: `python -m ma_analyse gui` ist bewusst kein gueltiger Befehl
  mehr. `ma_ui` besitzt den GUI-Parser fuer Tkinter-Startwerte; `ma_analyse`
  stellt weiterhin fachliche Services, Runner, Templates und Konfigurationen
  bereit.
- Betroffene Module oder Dateien: `src/ma_analyse/app/cli.py`,
  `src/ma_analyse/app/commands.py`, ehemals `src/ma_analyse/gui/`,
  `src/ma_ui/tkinter_app/module_views/analyse/`, `docs/ma_analyse/`,
  `docs/ma_ui/`, `docs/project/architecture/`
- Status: getroffen und umgesetzt
- Offene Folgefragen: Die grosse Tkinter-Hauptdatei unter `ma_ui` soll erst in
  einem spaeteren Folgeslice zerlegt werden.
- Quelle oder Chatbezug: freigegebener P029-Slice zur harten Tkinter-Migration

## UD-065 Relative/absolute Cooling-Trennung ins Hauptportal uebernehmen

- Datum: 2026-07-01
- Thema: ma_analyse Cooling-Auswertung
- Entscheidung: Die relative/absolute Cooling-Trennung soll spaeter auch in
  den regulaeren `cooling`-Befehl und in die GUI-Auswahl uebernommen werden.
- Begruendung: Die bereits getrennten Plot-Templates sollen nicht dauerhaft
  eine Sonderlogik bleiben; regulaerer Cooling-Befehl, Streamlit-Analyse und
  Tkinter-Analyse sollen dieselbe fachliche Auswahl anbieten.
- Auswirkung: OP-006 ist geschlossen. Die Umsetzung wird als Folgeaufgabe fuer
  `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/app/cli.py`,
  `src/ma_ui/streamlit_app/module_views/analyse_view.py` und
  `src/ma_ui/tkinter_app/module_views/analyse/` gefuehrt.
- Betroffene Module oder Dateien: `src/ma_analyse/analysis/cooling.py`,
  `src/ma_analyse/app/cli.py`, `src/ma_ui/streamlit_app/module_views/analyse_view.py`,
  `src/ma_ui/tkinter_app/module_views/analyse/`, `docs/ma_analyse/`,
  `docs/ma_ui/`
- Status: getroffen
- Offene Folgefragen: Konkrete CLI-Option, UI-Wording und Rueckwaertskompatibilitaet
  im Umsetzungsslice festlegen.
- Quelle oder Chatbezug: Nutzerantwort auf OP-006 am 2026-07-01

## UD-066 DWG bleibt kein produktiver ma_building-Importpfad

- Datum: 2026-07-02
- Thema: ma_building, CAD-Dateien und DWG-Parser
- Entscheidung: Fuer den aktuellen Masterarbeitsumfang wird kein DWG-Parser,
  Add-on oder externe DWG-Library als produktiver Importpfad in `ma_building`
  aufgenommen. DWG-Dateien duerfen lokal als ungepruefte CAD-Quellen
  aufbewahrt und mit Metadaten diagnostiziert werden. Fachlich belastbare
  Gebaeudemodelldaten sollen bevorzugt ueber IFC oder bei Bedarf ueber einen
  vorher bewusst erzeugten DXF-/IFC-Export geprueft werden.
- Begruendung: DWG ist ein proprietaeres Binaerformat. Ohne externen Parser
  kann `ma_building` nicht belastbar erkennen, ob eine DWG ein fachlich
  nutzbares Gebaeudemodell enthaelt. Ein produktiver DWG-Import wuerde den
  aktuellen Masterarbeitsumfang technisch und wartungsseitig unnoetig
  erweitern.
- Auswirkung: `data/ma_building/input/cad/` bleibt ein lokaler Ablageort fuer
  ungepruefte CAD-Beispieldateien. Die Streamlit- und Diagnoseansicht darf DWG
  als Quelle anzeigen, aber nur mit Parser-Warnung und ohne
  Gebaeudemodell-Importversprechen. `SmallOffice_d_IFC2x3.ifc` bleibt die
  Fachteil-Referenz; UD-067 trennt davon das Rhino-Testgebaeude fuer
  BusinessIntegration.
- Betroffene Module oder Dateien: `src/ma_building/diagnostics.py`,
  `data/ma_building/input/cad/`, `docs/ma_building/README.md`,
  `docs/project/plans/inbox/260622_Plan_P012_ma_building_Gebaeudeinput.md`,
  `docs/project/architecture/INPUT_DATA_FORMAT_MATRIX.md`
- Status: getroffen
- Offene Folgefragen: Nur falls DWG spaeter fachlich zwingend wird, braucht
  es einen eigenen Tool-/Parser-Entscheid. Dieser gehoert nicht zu P012 v1.
- Quelle oder Chatbezug: Nutzerentscheidung am 2026-07-02 nach Rueckfrage zum
  DWG-Parser

## UD-067 P012 Referenzmodelle fuer Fachteil und BusinessIntegration trennen

- Datum: 2026-07-03
- Thema: ma_building, Referenzmodelle und Level of Detail
- Entscheidung: `SmallOffice_d_IFC2x3.ifc` wird fuer den fachlichen Teil der
  Masterarbeit genutzt. Fuer den BusinessIntegration- und Softwareteil wird
  das Rhino-Testgebaeude
  `ma_building_testgebaeude_6x4x4_oeffnungen_v1.3dm` als lokale
  Arbeitsreferenz verwendet. Der Einstieg in P012 soll klein bleiben und
  verschiedene Level of Detail als Eingabeumfang abbilden.
- Begruendung: Fachlicher IDA-ICE-Bezug und BusinessIntegration-/Softwaretest
  haben unterschiedliche Nachweisziele. SmallOffice eignet sich als
  fachliches IDA-/IFC-Referenzmodell; das Rhino-Testgebaeude eignet sich als
  kontrollierbare, einfache Arbeitsquelle fuer Demo, UI und Validierung.
- Auswirkung: P012 unterscheidet kuenftig Fachteil-Referenz und
  BusinessIntegration-Referenz. Verbindliche Softwarestruktur bleibt eine
  kleine daraus abgeleitete `BuildingModelSpecification`; ein produktiver
  Rhino-Import ist dadurch nicht freigegeben. LOD-1 reicht fuer erste
  Trainings- und UI-Tests, LOD-2/LOD-3 bleiben Ziel fuer spaetere analysefaehige
  Pflichtdaten.
- Betroffene Module oder Dateien: `src/ma_building/paths.py`,
  `src/ma_ui/streamlit_app/module_views/building_view.py`,
  `docs/ma_building/README.md`,
  `docs/project/plans/inbox/260622_Plan_P012_ma_building_Gebaeudeinput.md`,
  `docs/project/architecture/INPUT_DATA_FORMAT_MATRIX.md`
- Status: getroffen
- Offene Folgefragen: LoD-2 und LoD-3 klaeren spaeter, welche weiteren Inhalte
  aus dem Rhino-Testgebaeude in die `BuildingModelSpecification` uebernommen
  werden.
- Quelle oder Chatbezug: Nutzerentscheidung am 2026-07-03 zur Trennung von
  fachlichem SmallOffice-Modell und Rhino-Testgebaeude fuer
  BusinessIntegration

## UD-068 LoD beschreibt in P012 den Umfang der Eingabe

- Datum: 2026-07-05
- Thema: ma_building, Eingabe-LoD und BusinessIntegration-LoD-1
- Entscheidung: Level of Detail wird in P012 als Umfang der Eingabe
  verstanden, nicht als Detailgrad einer CAD-/BIM-Geometrie. LoD-1 umfasst
  Kubatur, einfache Aussenwand-/Huellflaechen, U-Werte fuer Aussenwand und
  Fenster, Fensterflaechenanteil in Prozent sowie optionale Dach- und
  Bodenkennwerte. LoD-3 beschreibt die vollstaendige Eingabe aller fuer die
  Software benoetigten Gebaeudedaten in der Eingabephase.
- Begruendung: Fuer erste Dimensionierung und einfache Analysen ist ein
  kleiner, nachvollziehbarer Eingabeumfang wichtiger als ein komplexer
  CAD-Parser. Dadurch bleibt `ma_building` fuer die Masterarbeit erklaerbar
  und testbar.
- Auswirkung: P012-S2 setzt `BuildingInputDetailLevel`, `SimpleEnvelopeInput`
  und eine versionierte BusinessIntegration-LoD-1-Spec um. LoD-1 darf ohne
  Raeume, Einzelfenster und Host-Beziehungen freigegeben werden, wenn Kubatur,
  U-Werte, Fensteranteil und Annahmen valide sind. BIL bleibt davon getrennt
  der Informations-/Modellreifegrad.
- Betroffene Module oder Dateien: `src/ma_building/models.py`,
  `src/ma_building/validation.py`,
  `config/ma_building/examples/business_integration_lod1_building_spec.yaml`,
  `src/ma_ui/streamlit_app/module_views/building_view.py`,
  `docs/project/plans/inbox/260622_Plan_P012_ma_building_Gebaeudeinput.md`
- Status: getroffen und umgesetzt fuer LoD-1
- Offene Folgefragen: LoD-2 und LoD-3 brauchen eigene Umfangsentscheidungen,
  bevor Raum-/Bauteilstruktur oder vollstaendige Eingabephase umgesetzt
  werden.
- Quelle oder Chatbezug: Nutzerentscheidung am 2026-07-05 zur Bedeutung von
  LoD als Eingabeumfang und Freigabe des LoD-1-Slices

## UD-069 BusinessIntegration-LoD-1 als naechster grosser Slice

- Datum: 2026-07-07
- Thema: ma_building, ma_zones, ma_technical und ma_parameters
- Entscheidung: Der naechste grosse Umsetzungsslice ist die
  BusinessIntegration-LoD-1-Eingabekette. Aus dem kleinen Rhino-Testgebaeude
  wird nach `ma_building` eine einfache Gesamtgebaeudezone in `ma_zones`, eine
  einfache Referenztechnik in `ma_technical` und eine nicht-produktive
  Parameter-Vorschau in `ma_parameters` aufgebaut.
- Begruendung: Der Slice bleibt klein und erklaerbar, zeigt aber den
  fachlichen Durchstich von Gebaeude ueber Nutzung und Technik bis zur
  Parameter-Vorschau. Damit eignet er sich fuer die BusinessIntegration-
  Argumentation der Masterarbeit.
- Auswirkung: `ma_zones` und `ma_technical` erhalten versionierte YAML-Demos,
  Fachmodelle, Loader, Validierung, Tests und Streamlit-Pruefansichten. P015
  bekommt nur eine Vorschau; ein produktiver `ParameterSnapshot` bleibt
  Folgearbeit.
- Betroffene Module oder Dateien: `src/ma_zones/`, `src/ma_technical/`,
  `src/ma_parameters/previews.py`, `config/ma_zones/examples/`,
  `config/ma_technical/examples/`, `src/ma_ui/streamlit_app/module_views/`
- Status: getroffen und umgesetzt fuer LoD-1
- Offene Folgefragen: LoD-2/LoD-3 fuer Raum-Zonen-Zuordnung,
  Nutzungsprofilbibliothek, Referenzsysteme und produktiver
  `ParameterSnapshot` bleiben separat zu klaeren.
- Quelle oder Chatbezug: Nutzerfreigabe am 2026-07-07 fuer den grossen
  BusinessIntegration-LoD-1-Slice

## UD-070 ParameterSnapshot v1 als naechster grosser Slice

- Datum: 2026-07-07
- Thema: ma_parameters, P015 und BusinessIntegration-LoD-1
- Entscheidung: Der naechste grosse Umsetzungsslice nach der
  BusinessIntegration-LoD-1-Eingabekette ist ein produktiver
  `ParameterSnapshot` v1. Der Snapshot buendelt die validierten Werte aus
  `ma_building`, `ma_zones` und `ma_technical` mit Quellenreferenz, Einheit,
  Version und Freigabestatus.
- Begruendung: Ohne Snapshot bleibt die LoD-1-Kette nur eine Demo- und
  UI-Vorschau. Der Snapshot schafft den stabilen Datenvertrag fuer Stage 1,
  Variantenbildung und spaeteres Simulation Setup.
- Auswirkung: `ma_parameters` enthaelt Snapshot-Fachmodelle, Builder,
  Validierung, Streamlit-Pruefansicht und Tests. Stage 1 und `ma_variants`
  sollen kuenftig auf freigegebene Snapshot-Werte zugreifen, nicht direkt auf
  Building-, Zonen- oder Technik-Demos.
- Betroffene Module oder Dateien: `src/ma_parameters/models.py`,
  `src/ma_parameters/snapshots.py`, `src/ma_parameters/validation.py`,
  `src/ma_ui/streamlit_app/module_views/parameters_view.py`,
  `docs/project/plans/inbox/260622_Plan_P015_ma_parameters_Zentrale_Parameter.md`
- Status: getroffen und umgesetzt fuer Snapshot v1
- Offene Folgefragen: Snapshot-Speicherung, manuelle Aenderungsnachweise,
  Wetteruebernahme, Stage-1-Folgesnapshots und Variantenanbindung bleiben
  separat zu klaeren.
- Quelle oder Chatbezug: Nutzerfreigabe am 2026-07-07 fuer P015-S1
  `ParameterSnapshot` v1

## UD-071 LoD-1-Referenzdimensionierung als naechster grosser Slice

- Datum: 2026-07-07
- Thema: P016, ma_analyse.stage_1_dimensioning und ParameterSnapshot v1
- Entscheidung: Nach dem `ParameterSnapshot` v1 wird als naechster grosser
  Slice eine LoD-1-Referenzdimensionierung umgesetzt. Sie liest ausschliesslich
  aus dem freigegebenen Snapshot v1 und berechnet transparente Startwerte fuer
  Heizlast, Lueftungs-Heizlast, interne Kuehllastannahme und Luftvolumenstrom.
- Begruendung: Nach der Eingabekette entsteht damit erstmals ein fachlich
  sichtbares Berechnungsergebnis. Der Slice bleibt klein genug fuer die
  Masterarbeit und vermeidet vorerst normative oder dynamische Verfahren.
- Auswirkung: `ma_analyse.stage_1_dimensioning` enthaelt Fachmodelle,
  LoD-1-Service, Rechenweg, Diagnosehinweise, Tests und eine Streamlit-
  Pruefansicht. Stage 1 greift nicht direkt auf Building-, Zonen- oder
  Technikdemos zu.
- Betroffene Module oder Dateien: `src/ma_analyse/stage_1_dimensioning/`,
  `src/ma_ui/streamlit_app/module_views/dimensioning_view.py`,
  `src/ma_workflow/catalog.py`,
  `docs/project/plans/inbox/260622_Plan_P016_Stage1_Dimensionierung.md`
- Status: getroffen und umgesetzt fuer P016-S1
- Offene Folgefragen: Normverfahren, IDA-/SmallOffice-Plausibilisierung,
  Folgesnapshot fuer Stage-1-Ergebnisse und Variantenanbindung bleiben
  separat zu klaeren.
- Quelle oder Chatbezug: Nutzerfreigabe am 2026-07-07 fuer P016-S1
  LoD-1-Referenzdimensionierung

## UD-072 P013-S2 Gesamtkonzept ma_zones verbindlich konsolidieren

- Datum: 2026-07-08
- Thema: ma_zones, Eingabeworkflow, Parameter- und Variantenkette
- Entscheidung: Der bisherige Kurzplan P013 wird durch das fachlich
  konsolidierte Gesamtkonzept `ma_zones` ersetzt. Verbindlich ist die
  Eingabereihenfolge `ma_weather -> ma_building -> ma_technical -> ma_zones
  -> ma_validation -> ma_parameters`, ein allgemeines Zonenobjekt statt
  getrennter Zonentypen, vollstaendige Raum-Zonen-Zuordnung im MVP, keine
  Raumteilung, getrennte Normprofilfassungen 2018/2025, modulinterne
  `ma_zones`-Pruefung und spaetere Uebergabe des freigegebenen Zonenstands an
  `ma_parameters`.
- Begruendung: Der LoD-1-Demo-Stand war konsistent, aber zu kurz und noch auf
  thermische Zonen sowie einen Rueckfluss zu `ma_technical` fokussiert. P013-S2
  klaert die fachliche Zielstruktur, ohne die vorhandene Demo ungeplant zu
  brechen.
- Auswirkung: `ma_workflow`, `ma_ui`, P014, P015, P017 und die zentrale
  Dokumentation muessen die neue Reihenfolge und die Uebergangsgrenze
  beachten. Die aktuelle P014-LoD-1-Demo mit `source_zone_model_id` und
  `served_zone_ids` bleibt kompatibler Uebergangsbestand und wird nicht
  stillschweigend als Zielvertrag verstanden.
- Betroffene Module oder Dateien: `src/ma_zones/`, `src/ma_technical/`,
  `src/ma_parameters/`, `src/ma_workflow/catalog.py`,
  `docs/project/plans/inbox/260622_Plan_P013_ma_zones_Zonen_Nutzungen.md`,
  P014, P015, P017, `docs/project/plans/PLAN_INDEX.md`,
  `docs/project/plans/PLAN_STATUS.md`
- Status: getroffen; P013-S2 dokumentarisch und im Workflow-Katalog
  konsolidiert
- Offene Folgefragen: Sonderhohlraeume, gleichzeitiger Heiz-/Kuehlbetrieb,
  Bedeutung des Prozentwerts bei Uebergabesystemen, LoD-1-
  Variantenparameter und konkrete DIN-Datenabbildung bleiben als
  P013-Folgeentscheidungen offen.
- Quelle oder Chatbezug: Nutzerfreigabe am 2026-07-08 fuer P013-S2

## UD-073 P015/P017 Handover ohne SimulationCase konsolidieren

- Datum: 2026-07-12
- Thema: ma_parameters, ma_variants, ma_simulation_setup,
  Simulationsschnittstellen
- Entscheidung: Der neue Inputstand zu P015 und das aktualisierte
  `ma_variants`-Handover werden in die bestehenden Plaene verteilt, ohne neue
  Parallelplaene anzulegen. P015 fuehrt `BaselineParameterSnapshot`,
  `ReferenceDimensioningResult` und `ParameterVariationSpecification` als
  Zielvertrag. P017 fuehrt den aktiven Prozess `VSP -> VVER -> VCAT -> VSEL ->
  VGEN -> ma_simulation_setup`. `SimulationCase`, `CASE-ID` und ein separates
  Varianten-Handover-Objekt gehoeren nicht zur aktiven Architektur.
- Begruendung: Die Variantenkette bleibt fuer die Masterarbeit
  nachvollziehbar, begrenzt und modular. Fachliche Provenienz verbleibt in
  `ma_variants`, waehrend P018/P009 nur simulationsrelevante Varianten- und
  Run-Daten erhalten.
- Auswirkung: P015, P016, P017, P018, P009, P014 und P027 wurden
  dokumentarisch auf den neuen Schnittstellenstand gebracht. P018 und P009
  verwenden als Zielvertrag direkte `RUN-ID + VAR-ID`-Zuordnung.
- Betroffene Module oder Dateien: `docs/project/plans/inbox/260622_Plan_P015_ma_parameters_Zentrale_Parameter.md`,
  `docs/project/plans/inbox/260622_Plan_P017_ma_variants_Naming_Anbindung.md`,
  P014, P016, P018, P009, P027, `docs/project/plans/PLAN_INDEX.md`,
  `docs/project/plans/PLAN_STATUS.md`,
  `docs/project/architecture/TARGET_ARCHITECTURE.md`,
  `docs/project/architecture/INPUT_DATA_FORMAT_MATRIX.md`
- Status: getroffen; dokumentarisch konsolidiert, Codeumsetzung offen
- Offene Folgefragen: Regelkatalog-Grenze, finale Variantennamen und
  Exportpfade, erweiterte Samplingmethoden sowie iterative Prozesse bleiben
  getrennte Folgeentscheidungen.
- Quelle oder Chatbezug: Nutzerfreigabe `frei` am 2026-07-12 zur Verteilung
  der neuen Inputdaten auf bestehende Plaene

## UD-074 P014 ma_technical Gesamtplan und Schema v2 aufnehmen

- Datum: 2026-07-13
- Thema: ma_technical, P014-S2, technische Systeme und Nachbarmodulvertraege
- Entscheidung: Der konsolidierte Gesamtplan fuer `ma_technical` wird als
  verbindliches Zielbild in P014 aufgenommen. Die bestehende
  BusinessIntegration-LoD-1/Lite-Demo bleibt als Legacy-v1-Vertrag
  kompatibel. Parallel wird ein Schema v2 aufgebaut, das zentrale Plant-,
  Heizungs-, Kuehlungs-, Speicher-/DHW-, AHU-, Elektro-, Topologie-,
  Zeitplan- und Serviceinterface-Objekte typisiert beschreibt. Direkte
  Zonenreferenzen sind Legacy; Ziel sind Serviceinterfaces, die spaeter von
  `ma_zones` zugeordnet werden.
- Begruendung: Der neue Plan klaert die Modulgrenze deutlich: `ma_technical`
  beschreibt zentrale technische Systeme und Regel-/Parameterquellen, erzeugt
  aber keine Varianten und fuehrt keine Simulation oder automatische
  Dimensionierung aus. Dadurch bleibt die Eingabekette fuer die Masterarbeit
  nachvollziehbar und die bestehende v1-Demo wird nicht ungeplant gebrochen.
- Auswirkung: P014, Planindex, Planstatus, Modul-README und Changelog werden
  nachgezogen. In `src/ma_technical/` entstehen v2-Kerntypen parallel zum
  bisherigen v1-Modell. `ma_parameters`, `ma_zones`, `ma_variants`,
  `ma_validation`, `ma_workflow`, `ma_ui`, `ma_analyse` und
  `ma_simulation_setup` behalten ihre bestehenden Vertraege, bis spaetere
  Slices Migration, Serviceinterface-Zuordnung, Parameterexport und
  Revisionen bewusst umsetzen.
- Betroffene Module oder Dateien: `src/ma_technical/`,
  `docs/project/plans/inbox/260622_Plan_P014_ma_technical_Technische_Systeme.md`,
  `docs/ma_technical/README.md`, `docs/project/plans/PLAN_INDEX.md`,
  `docs/project/plans/PLAN_STATUS.md`
- Status: getroffen; Slice 0/1 freigegeben
- Offene Folgefragen: lokale Repository-/Revisionsstruktur,
  v1-zu-v2-Migration, Serviceinterface-Zuordnung in `ma_zones`,
  Parametersicht fuer `ma_parameters`, technische Regeln und UI-Draft-Editor.
- Quelle oder Chatbezug: Nutzerfreigabe `frei` am 2026-07-13 zum
  konsolidierten `ma_technical`-Plan

## UD-075 Codex-Council mit Tera-Hauptmodell und kontrollierter Autonomie

- Datum: 2026-07-13
- Thema: Codex-Arbeitsroutine, Modellwahl und Freigabegrenzen
- Entscheidung: `gpt-5.6-terra` wird als wirtschaftliches Hauptmodell fuer
  die normale Projektarbeit verwendet. Luna darf fuer schnelle read-only
  Exploration eingesetzt werden. Sol uebernimmt gezielte technische und
  wissenschaftliche Qualitaetspruefungen. Vor einer Umsetzungsfreigabe
  arbeiten alle Council-Mitglieder read-only; nach der Freigabe darf ein
  Tera-Worker klar abgegrenzte Umsetzungspakete uebernehmen.
- Begruendung: Die meiste Projektarbeit soll wirtschaftlich mit Tera erfolgen,
  waehrend Sol bei groesseren Risiken und wissenschaftlich kritischen Punkten
  die hoechste Qualitaet absichert. Klare Rollen vermeiden Doppelarbeit und
  unkontrollierte parallele Aenderungen.
- Auswirkung: Das Root-`AGENTS.md`, `.codex/config.toml`, projektlokale
  Agentendateien und die Council-Routinen bilden die dauerhafte Steuerung.
  Einzelne read-only Council-Einsaetze benoetigen keine weitere Freigabe;
  Schreibzugriffe bleiben an den zuvor freigegebenen Umfang gebunden.
- Betroffene Module oder Dateien: `AGENTS.md`, `.codex/config.toml`,
  `.codex/agents/`, `.github/agents/Professor.md`,
  `docs/common/commands_common.md`
- Status: getroffen und als Council-Basis umgesetzt
- Offene Folgefragen: praktische Kalibrierung der Einsatzschwellen nach den
  ersten Council-Laeufen; P018 kann als erster Pilot dienen.
- Quelle oder Chatbezug: Nutzerfreigabe `Freigegeben fuer Council-Basis mit
  kontrollierter Autonomie.` am 2026-07-13

## UD-076 IDA-ICE-Compliance-Grenze fuer Hochschullizenz und Automatisierung

- Datum: 2026-07-13
- Thema: IDA ICE 5.1 Hochschullizenz, `.idm`, Bibliotheken, Cloud-Verarbeitung
  und Simulationsautomatisierung
- Entscheidung: Bis zu einer ausdruecklichen schriftlichen EQUA-Freigabe
  erzeugt die eigene Software nur neutrale Variantendaten und bereitet den
  Lauf vor. Uebergabe an IDA ICE und Simulationsstart bleiben manuell.
  Vollstaendige oder unbekannte IDA-Dateien, mitgelieferte Bibliotheken,
  NMF-Modelle und Drittinhalte werden vor jeder Verarbeitung anhand der
  Compliance-Vorpruefung klassifiziert; bei Unklarheit gilt `stop`.
- Begruendung: Die EULA 2023/12 untersagt automatisierte Simulationsstarts
  ohne EQUA-Autorisierung und schuetzt Softwarestruktur, Organisation und
  Code. Die konkrete Zusammensetzung einer `.idm` und Rechte an Drittinhalten
  sind nicht pauschal als Nutzerinhalte belegbar.
- Auswirkung: `ma_simulation_setup`, `ma_export_simulation`,
  `ma_import_simulation` und der IDA-ICE-Adapter bilden keine automatische
  Simulationssteuerung. Kuenftige IDA-bezogene Arbeiten dokumentieren vorab
  eine `compliance_decision` nach `docs/compliance/ida_ice/`.
- Betroffene Dateien: `docs/compliance/ida_ice/`, `docs/ida_ice/README.md`,
  P018, P009, die Export-/Import-READMEs, Zielarchitektur, Planstatus und
  Changelog.
- Status: getroffen; technische Umsetzung einer IDA-Steuerung bleibt
  ausgeschlossen
- Offene Folgefragen: Hochschullizenzuntertyp, projektspezifisches lokales
  `.idm`-Parsing, Cloud-Analyse einer bereinigten Datei, Vorlagen-/Bibliothek-
  auszug und API-/Makro-Umfang werden bei EQUA schriftlich geklaert.
- Quelle oder Chatbezug: Nutzerfreigabe `Freigegeben fuer die erweiterte
  IDA-ICE-Compliance-Dokumentation.` am 2026-07-13

## UD-077 Projektweites Compliance-System fuer IDA, DIN/Nautos und DWD

- Datum: 2026-07-13
- Thema: technische Schutzgrenzen fuer geschuetzte Datei- und
  Systemoperationen
- Entscheidung: Die freigegebene Compliance-Dokumentation wird als zentrale
  Komponente `ma_core.compliance` technisch durchgesetzt. Gruen erlaubt nur
  den dokumentierten Umfang. Gelb erfordert eine explizite
  Nutzerbestaetigung und alle verlangten Rechte-/Hochschulbelege. Rot und
  unbekannte Herkunft stoppen. Reale geschuetzte Dateien und Wetterdaten
  bleiben lokal und unversioniert.
- Begruendung: Dokumentation allein verhindert keinen versehentlichen
  Dateiinhaltzugriff. Ein gemeinsamer Preflight und sichere Wrapper machen die
  bereits festgelegten IDA-/EQUA-, DIN-/Nautos- und DWD-Grenzen testbar und
  reproduzierbar.
- Auswirkung: Policies, Schemas, Audit, Warntexte und Testmatrix liegen unter
  `src/ma_core/compliance/`. Der DWD-TRY-2011-Konverter verlangt vor dem Lesen
  eine Bezugsrechtsreferenz. P008, P018, P020 und P027 sowie Architektur- und
  Modul-Dokumentation werden synchronisiert.
- Betroffene Dateien: `src/ma_core/compliance/`,
  `src/ma_weather/dwd_try2011_converter.py`, `docs/compliance/`, P008, P018,
  P020, P027, Planindex, Planstatus, Zielarchitektur und Changelog
- Status: getroffen und technisch umgesetzt
- Offene Folgefragen: schriftliche EQUA-Antwort, Hochschul-/DIN-KI-Lizenz,
  produktspezifischer DWD-TRY-Bezugsnachweis und risikobasierte Anbindung
  weiterer Dateioperationen.
- Quelle oder Chatbezug: Nutzerauftrag `Schliess den letzten Prozess ab` und
  konsolidierte ChatGPT-Uebergabe vom 2026-07-13

## UD-078 Projektweiter Compliance-Agent als stoppendes Council-Mitglied

- Datum: 2026-07-13
- Thema: Codex-Council, Compliance-Pruefung und Aufnahme neuer Plaene und
  Projektinputs
- Entscheidung: Der read-only `compliance_auditor` arbeitet projektweit mit
  Sol und hohem Reasoning. Er wird bei erkennbaren Compliance-Risiken sowie
  bei `plan aufnehmen` und `projektinput aufnehmen` automatisch einbezogen.
  Ein belegter Compliance-Blocker stoppt den betroffenen Vorgang.
- Begruendung: Die vorhandenen projektweiten Regeln unter `docs/compliance/`
  sollen nicht nur dokumentiert, sondern auch in den Codex-Arbeitsroutinen
  konsistent angewendet werden. Die Spezialisierung trennt Rechte-, Lizenz-,
  Datenschutz- und Veroeffentlichungsfragen von technischer Qualitaet und
  wissenschaftlicher Methodik.
- Auswirkung: Neue Plandokumente durchlaufen vor dem Inhaltszugriff einen
  Metadaten-Preflight. Ist das Dokument selbst zulaessig, bleiben spaetere
  Umsetzungsblocker in Planindex oder Planstatus sichtbar. Unklare oder
  blockierte Inbox-Originale werden nicht extrahiert, verschoben oder
  eingearbeitet und bleiben am aktuellen Eingangspfad. Vor jeder
  Veroeffentlichung wird eine gueltige Entscheidung fuer den konkreten Stand
  geprueft.
- Betroffene Dateien: `.codex/agents/compliance-auditor.toml`, `AGENTS.md`,
  `docs/common/commands_common.md`, `docs/project/UPDATE_ROUTINES.md`,
  `docs/project/PROJECT_INPUT_WORKFLOW.md`, `docs/compliance/`
- Status: getroffen und in die Codex-Routinen integriert
- Offene Folgefragen: Einsatzschwellen und Fehlalarme werden anhand der ersten
  realen Plan- und Inbox-Pruefungen kalibriert. Der Hauptagent dokumentiert
  Entscheidungen und Belegreferenzen; der Agent erteilt weiterhin keine
  Rechts-, Vertrags- oder Fachfreigabe. Die technische Prioritaet kombinierter
  `red`-/`unknown`-Regeln bleibt ein separater Code-Folgeslice.
- Quelle oder Chatbezug: Nutzerfreigabe `Freigegeben fuer Compliance-Agent und
  Routine-Integration.` am 2026-07-13

## UD-079 Preprocess V1 bis zum RunManifest festlegen

- Datum: 2026-07-14
- Thema: Preprocess, P011 bis P018, P027 und manuelle IDA-ICE-Uebergabe
- Entscheidung: Der erste verbindliche Software-Meilenstein ist
  `Preprocess V1`. Er endet mit einem validierten, reproduzierbaren
  `RunManifest` fuer eine freigegebene Baseline und eine kleine explizite
  Variantenstudie. Die Reihenfolge ist Projekt, Wetter, Gebaeude, Technik,
  Zonen, Parameter, Referenzdimensionierung, Varianten und
  Simulationssetup.
- Begruendung: Der Meilenstein zeigt den kompletten fachlichen Durchstich bis
  zur Simulationsvorbereitung, bleibt aber fuer die Masterarbeit beherrschbar.
  Ein reiner Baseline-Durchlauf bleibt Testmodus; eine kleine Variantenstudie
  prueft den eigentlichen Zweck der Software.
- Auswirkung: P014 schliesst zuerst die Vollstaendigkeit des v2-Aggregats und
  die Referenzintegritaet. P012/P013 liefern einen kleinen manuellen
  Raum-/Zonenstand. P015 liefert Fingerprints und Aktualitaetspruefung,
  P016 einen eigenen Ergebnisstand, P017 die minimale Variantenkette und P018
  das RunManifest mit Compliance-Entscheidungsreferenz. P027 begleitet die
  Checkpoints.
- Nicht Teil: produktiver IFC-/Rhino-Import, IDA-ICE-Adapter und
  Modellmanipulation, Produktkataloge, technische Regelengine, Draft-Branches
  und vollstaendige Facheditoren.
- Status: getroffen; Planungsdokumentation freigegeben, Umsetzung folgt in
  einzelnen freizugebenden Slices.
- Quelle oder Chatbezug: Nutzerfreigabe `frei Fahrplan Preprocess V1` am
  2026-07-13

## UD-080 P014-v2-Aggregat, Freigabe und Handover staffeln

- Datum: 2026-07-14
- Thema: P014 `ma_technical`, v2-Aggregat, Referenzintegritaet und Preprocess-V1-Handover
- Entscheidung: P014 wird fuer Preprocess V1 in die aufeinanderfolgenden
  Slices P014-S1.1 Aggregat/Referenzen, P014-S1.2 getrennte
  Strukturvalidierung, P014-S2 Persistenz/freigegebene Revision,
  P014-S3 P013/P015-Handover und P014-S4 Referenzfall/Abnahme gegliedert.
  `plant`, RLT und Electrical sind optionale Primaerbereiche; fehlende
  Bereiche werden nicht durch Dummy-Objekte ersetzt. Nur eine erfolgreich
  validierte Revision darf an P015 uebergeben werden. Der Content-Hash umfasst
  fachliche Daten, Quellenreferenzen und Annahmen, nicht aber lokale Pfade oder
  Erstellungszeitpunkte. P013 erhaelt zentrale Serviceinterface-Referenzen;
  lokale Terminal- und Zonenzuordnung verbleiben in P013.
- Auswirkung: Der Legacy-v1-Vertrag und sein Validator bleiben unveraendert.
  P014 erhaelt einen separaten v2-Validator und eine klar abgegrenzte
  Freigabegrenze vor `ma_parameters`; weitergehende Eignungspruefungen,
  Draft-Branches, Editor und IDA-Anbindung bleiben Folgearbeit.
- Betroffene Module oder Dateien: `src/ma_technical/`, P014, P013, P015,
  `docs/project/plans/PLAN_INDEX.md`, `docs/project/plans/PLAN_STATUS.md`
- Status: getroffen; P014-S1.1 als naechster Umsetzungsslice geplant
- Quelle oder Chatbezug: Nutzerfreigabe `passt machen wir so` am 2026-07-14

## UD-081 DBIS-, Nautos-, VDE- und VDI-Rechte quellenabhaengig dokumentieren

- Datum: 2026-07-14
- Thema: Hochschulzugang, technische Regelwerke, KI-Verarbeitung und
  Veroeffentlichungsgrenzen
- Entscheidung: Die DBIS-Eintraege 105040 und 103475 werden als Belege fuer
  den manuellen Frankfurt-UAS-Zugang zu Nautos und VDE-NormenBibliothek
  aufgenommen. Der VDE-Zugang erlaubt Ansicht, aber keinen Download oder
  Druck. Rechte werden nicht allein nach
  Plattform, sondern getrennt nach Regelwerk, Rechteinhaber, Bezugsweg und
  konkreten Vertragsbedingungen bewertet. VDE- und VDI-KI-Verarbeitung bleibt
  bis zu einem passenden schriftlichen Rechtebeleg gesperrt.
- Begruendung: Campus- oder VPN-Zugang beweist keine KI-, Maschinen-,
  Weitergabe-, Software- oder Veroeffentlichungsrechte. Die VDE-VERLAG-AGB,
  der NormenBibliothek-Nutzungsvertrag, die DIN-Media-Regeln und die
  VDI-Lizenzhinweise haben unterschiedliche Geltungsbereiche.
- Auswirkung: `docs/compliance/din_nautos/` erhaelt den DBIS-Nachweis,
  getrennte VDE-/VDI-Profile, korrigierte Gruen-Gelb-Rot-Grenzen und separate
  Anfrageentwuerfe fuer Hochschule und Rechteinhaber. Normbasierte Parameter
  oder Softwarelogik sind nicht pauschal gruen; lokale Pruefdaten bleiben
  `review_required` und unversioniert.
- Status: getroffen; Dokumentationsabgleich freigegeben und umgesetzt
- Offene Folgefragen: konkreter Hochschulvertrag, institutionelle
  Sonderbedingungen, Nutzung kopierter VDE-Einzelpassagen,
  Individualgenehmigungen, Zitat-/Abdruckumfang und eine
  spaetere VDE-/VDI-spezifische Erweiterung der Laufzeit-SourceTypes.
- Quelle oder Chatbezug: Nutzerfreigabe `Freigegeben fuer den
  DBIS-/Nautos-/VDE-/VDI-Dokumentationsabgleich.` am 2026-07-14

## UD-082 Masterarbeits-MVP mit neutralem Run-Paket und Forschungsauswertung

- Datum: 2026-07-14
- Thema: P018, P030, P027, P009 und messbarer Durchlauf der Masterarbeit
- Entscheidung: P018 erzeugt fuer die Masterarbeit ein neutrales,
  reproduzierbares Run-Paket mit getrenntem SimulationSetup,
  Variantenartefakten, Validierung, Freigabe und technischen Logs. P027
  verantwortet dazu Ereignis-, Diagnose- und Workflowvertrag, nicht aber die
  wissenschaftliche Messung. P030 `research_tools` erfasst und vergleicht
  ausserhalb der Produktivsoftware Preprocessing-, Simulations- und
  Postprocessing-Zeit, aktive Nutzerzeit, Maschinenzeit sowie Prozessqualitaet.
  P009 erhaelt nach einem stabilen Run-Paket einen begrenzten manuellen
  Ergebnis-Postprocess fuer die ersten Diagramme.
- Auswirkung: Ein erster Masterarbeits-MVP reicht von der Eingabeaufnahme bis
  zu neutral vorbereiteten Runs, manueller Simulation, kontrollierter
  Ergebnisaufnahme und einfacher Analyse. IDA-Adapter, `.idm`-Bearbeitung,
  automatischer Simulationsstart und wissenschaftliche Logik in Fachmodulen
  bleiben ausgeschlossen.
- Betroffene Plaene oder Module: P009, P018, P027, P030,
  `ma_workflow`, `ma_simulation_setup`, `ma_import_simulation`, `ma_analyse`
- Status: getroffen; Plan- und Workflow-Integration freigegeben
- Quelle oder Chatbezug: Nutzerfreigabe `frei` zur
  P018/P030-MVP-Integration am 2026-07-14

## UD-083 Masterarbeits-MVP V1 und Handover-Vertraege festlegen

- Datum: 2026-07-14
- Thema: Gesamtziel V1, P013, P016, P018, P027, P009 und P030
- Entscheidung: Der erste Masterarbeits-MVP endet nicht beim RunManifest,
  sondern bei ersten Simulationszahlen, drei definierten Diagrammtypen und
  einem nachvollziehbaren Prozessvergleich. `Preprocess V1` bleibt darin der
  Teilmeilenstein bis zum neutralen P018-Run-Paket. P013 liefert nach dem
  manuellen Raum-Zonen-Slice ein kleines, freigegebenes
  `ThermalBuildingModel`; P016 und `ma_analyse` definieren drei neutrale
  `OutputRequirementProfiles` fuer Last, Raumklima/Komfort sowie Jahres- oder
  Spitzenwertvergleich. P009 nimmt Ergebnisse manuell und neutral auf; P030
  misst Produktiv- und Nutzerzeit ausserhalb der Fachsoftware.
- Auswirkung: P018 referenziert den Gebaeude-/Zonenabschluss und die
  Ausgabeanforderungen, dupliziert aber weder deren Fachlogik noch die
  wissenschaftliche Messung. Die MVP-Abnahme verlangt Baseline, mindestens
  eine Variante, manuelle Simulation, Ergebnisaufnahme, drei Diagramme und
  vergleichbare Prozessdaten.
- Status: getroffen; Handover-Abgleich und MVP-V1-Planung freigegeben
- Quelle oder Chatbezug: Nutzerfreigabe `Handover-Abgleich-Slice: frei` und
  `dann MVP-V1 frei` am 2026-07-14

## UD-084 Demo-Seed-Katalog fuer die Bedien- und Ablaufpruefung

- Datum: 2026-07-15
- Thema: `ma_database`, technische Katalogauswahl und fachliche Abgrenzung
- Entscheidung: Der vom Nutzer mit ChatGPT erstellte Seed-Katalog wird als
  versionierter read-only Demo-Katalog in das Projekt aufgenommen. Seine
  Materialien, Konstruktionen sowie Heiz-/Kuehlerzeuger und Speicher duerfen
  in Streamlit ausgewaehlt werden. Alle Werte bleiben `draft_unverified` bzw.
  `demo_unverified` und duerfen weder freigegebene Technikrevisionen noch
  Simulationen oder wissenschaftliche Referenzwerte unbemerkt beeinflussen.
- Begruendung: Fuer die erste Programmversion soll die Auswahl- und
  Prozesskette funktionieren; fachlich belastbare Produkt- oder Normdaten
  sind dafuer noch nicht erforderlich.
- Auswirkung: `ma_database` bleibt eine kleine lesende Katalogschicht.
  Persistenz, automatische Uebernahme in Technikmodelle, Dimensionierung und
  Produktdatenbank bleiben Folgearbeit mit eigener Validierung.
- Status: fuer die lokale Nutzung umgesetzt; die vorgesehene Versionierung ist
  durch UD-086 ersetzt
- Quelle oder Chatbezug: Nutzerhinweis `gehe von demo daten aus` und
  Umsetzungsfreigabe `frei` am 2026-07-15

## UD-085 Fachreiter und Baukonstruktionsgrenze in der Eingabe-UI

- Datum: 2026-07-15
- Thema: Bearbeitungsnavigation, `ma_building`, `ma_technical` und Demo-Daten
- Entscheidung: Die Bearbeitungsnavigation folgt der kanonischen
  Eingabereihenfolge Projekt, Wetter, Gebaeude, Technische Systeme, Zonen und
  Zentrale Parameter. `ma_technical` fuehrt Heizung, Kuehlung, Lueftung,
  Speicher, Trinkwarmwasser und Elektrik als getrennte Themen; jedes Thema
  kann explizit als `not_installed` erfasst werden. Materialien und
  Konstruktionen werden ausschliesslich in `ma_building` angezeigt und dort
  nur sitzungsbezogen zu Bauteilen oder Oeffnungen ausgewaehlt.
- Begruendung: Baukonstruktionen beschreiben die Gebaeudehuelle, technische
  Systeme die Anlagenseite. Die Trennung erleichtert die fachliche Eingabe und
  verhindert eine unklare Datenverantwortung.
- Auswirkung: Die aktuelle IFC-Diagnose bleibt eine Entity-Zaehldiagnose. Sie
  darf keine einzelnen Bauteile vortaeuschen; IFC-Lite-Extraktion von Bauteil-
  IDs und Attributen ist ein eigener Folgeslice.
- Status: getroffen und umgesetzt; IFC-Lite bleibt offen
- Quelle oder Chatbezug: Nutzerfreigabe `frei` am 2026-07-15

## UD-086 Katalogdaten lokal halten und nicht veroeffentlichen

- Datum: 2026-07-15
- Thema: `ma_database`, Demo-Katalog und oeffentlicher Repository-Release
- Entscheidung: Die Katalogdaten unter `config/ma_database/catalogs/` bleiben
  ausschliesslich lokal. Sie werden durch Git ignoriert, nicht versioniert und
  nicht zum oeffentlichen `origin` uebertragen. Loader und UI duerfen die
  Daten optional verwenden; ein frischer Clone muss ohne diese Dateien
  funktionieren und die manuellen Statusoptionen weiterhin anbieten.
- Begruendung: Die Katalogwerte sollen nicht veroeffentlicht werden.
- Auswirkung: Tests verwenden neutrale, zur Laufzeit erzeugte Fixtures statt
  der lokalen Katalogdateien. Dokumentation und Release-Compliance schliessen
  die Katalogdaten ausdruecklich aus.
- Status: getroffen und umgesetzt
- Quelle oder Chatbezug: Nutzerentscheidung `nein die Katalogdaten nicht
  veroeffentlichen` am 2026-07-15

## UD-087 Project-OS-Duplikate durch Council-Konsens aufloesen

- Datum: 2026-07-15
- Thema: Codex Project Operating System, Dokumentduplikate und fuehrende
  Projektwahrheiten
- Entscheidung: Wenn bestehende und vorgeschlagene Agenten-, Status-,
  Ablauf-, Architektur- oder Compliance-Dokumente dieselbe Aufgabe
  beanspruchen, diskutiert das Council die Varianten und legt eine
  strukturierte Single-Source-of-Truth-Loesung fest. Fuer P031 bleibt die
  vorhandene Projektstruktur fuehrend: Ein aktiver P031-Plan buendelt Audit,
  Konflikte, Capability-Snapshot und Backlog; neue parallele Root-, Status-
  oder Architekturwahrheiten werden nicht angelegt.
- Begruendung: Mehrere gleichwertige Wahrheiten wuerden den bereits
  festgestellten Routinenkonflikt wiederholen und spaetere Pflege erschweren.
  Die einstimmige Council-Loesung nutzt bestehende Eigentuemerschaften und
  ergaenzt nur pruefbare Router.
- Auswirkung: `UPDATE_ROUTINES.md` ist alleinige Ablaufwahrheit,
  `commands_common.md` Triggerindex, `AGENTS.md` Freigaberouter, `.codex/`
  Runtime und Rollen, `.agents/skills/` duenne Workflow-Router,
  `docs/compliance/` alleinige Rechteinstanz und P031 der einzige aktive
  Master-System-Audit-/Backlogtraeger.
- Status: getroffen und lokale Baseline umgesetzt
- Quelle oder Chatbezug: Nutzerauftrag `wenn es duplikate geben sollte
  muessen wir uns auf eine strukturierte Loesung einigen. Disktiert
  untereinander und entscheidet euch fuer eine Loesung` am 2026-07-15

## UD-088 P032 Zielarchitektur, Workspace-Betriebsmodell und Katalogownership

- Datum: 2026-07-15
- Thema: Architecture Benchmark, Paketownership und Workspace-Semantik
- Entscheidung: ADR-P032 mit Option 1 ist angenommen. Das Projekt bleibt bis
  zum MVP eine Workspace-Anwendung. `ma_parameters` ist kanonischer Owner der
  Parameter- und Optionskataloge; `ma_variants` konsumiert diese Vertraege und
  darf nur befristete, getestete Kompatibilitaets-Reexports anbieten.
- Begruendung: Die konservative Konsolidierung erhaelt die vorhandenen
  `ma_*`-Pakete, vermeidet einen vorzeitigen Packaging- oder Namespaceumbau
  und loest den Parameter-/Variantenzyklus ueber fachliche Ownership.
- Auswirkung: P032-W1 und P032-W2 sind dadurch nicht produktiv freigegeben.
  Jeder Move, Rename, API-Umbau, Dependency-, Hook-, CI-, Tool-, Daten- oder
  externe Verarbeitungsslice bleibt eine eigene Entscheidung mit konkretem
  Scope und den anwendbaren Gates.
- Status: getroffen; keine produktive Migration freigegeben
- Quelle oder Chatbezug: Nutzerfreigabe `Dann geb ich hiermit die Freigabe`
  nach der Vorstellung der drei P032-Kernpunkte am 2026-07-15

## UD-089 Council-Mehrheit fuer interne Folgeslices

- Datum: 2026-07-15
- Thema: Umsetzungsfreigaben, Council und kontrollierte Projektautonomie
- Entscheidung: Klar abgegrenzte, lokale und reversible Repo-Slices duerfen
  ohne weitere Einzelrueckfrage umgesetzt werden, wenn mindestens drei der
  fuenf definierten Council-Rollen dieselbe Empfehlung fuer den exakten Scope
  abgeben. Der Hauptagent dokumentiert Vote, Scope, Validation und Ergebnis in
  den kanonischen Plan- und Entscheidungsquellen.
- Begruendung: Der Nutzer moechte den weiteren Projektfortschritt nicht an
  wiederholten Einzelrueckfragen ausrichten, solange das Council eine
  nachvollziehbare Mehrheit erreicht.
- Auswirkung: P032-W1a ist nach dem einstimmigen Votum von Mira, Vera und
  Justus als interner Guardrail-Slice freigegeben. Die Delegation ersetzt keine
  Rechte- oder Complianceentscheidung und deckt keine Dependencies,
  Installationen, globale Codex-Konfiguration, Hooks, CI, MCP, Graphify,
  Obsidian/Zotero, externe APIs, geschuetzten oder realen Daten, Loeschungen,
  brechenden APIs, Commits, Pushes, Tags oder Veroeffentlichungen ab.
- Status: getroffen; operative Regeln in `AGENTS.md` verankert
- Quelle oder Chatbezug: Nutzerfreigabe `ich geb dir jetzt heirmit freigabe
  für alle weiter teile, solange eine mehrheit im council bei entscheidungen
  erricht werden kann, für eine gewisse entscheidung.` am 2026-07-15

## UD-090 P011-Gesamtentwurf lokal freigegeben

- Datum: 2026-07-15
- Thema: `ma_project`, Projektinitialisierung und digitale Projektakte
- Entscheidung: Der vom Nutzer bereitgestellte P011-Gesamtentwurf darf lokal
  inhaltlich geprueft und als kontrollierte Grundlage fuer den kanonischen
  P011-Plan verwendet werden.
- Begruendung: Der bisherige P011-Kurzplan reicht fuer die gewuenschte
  Projektidentitaet und die spaetere digitale Projektakte nicht aus.
- Auswirkung: Council und Compliance pruefen die Abweichungen zu P010, P028
  und P032. Reale Dateien, Assets, absolute lokale Quellpfade, externe Modelle
  und jede Naming-Pfadmigration bleiben von dieser Dokumentfreigabe getrennt.
- Status: getroffen
- Quelle oder Chatbezug: Nutzerfreigabe `p011 ist freigewgeben` am 2026-07-15

## UD-091 V1-Infokarten und priorisierte P014-v2-Folgearbeit

- Datum: 2026-07-18
- Thema: Streamlit-V1, Modulinfokarten, Wetter- und Technikansicht sowie
  Priorisierung des technischen v2-Modells
- Entscheidung: Zuerst wird der abgestimmte lokale V1-UI-Slice umgesetzt.
  Die V1-Erklaerungen stehen ausschliesslich in der vorhandenen zentralen
  `Infokarte`, nicht nochmals als Karte oder Reiter in den praktischen
  Modulansichten. Die Wetteransicht wird in `Analyse | Verwaltung`, die
  Technikansicht in `Technikmodell | Technik-Katalog` gegliedert. Das
  P014-v2-Modell bleibt danach ein hoch priorisierter, aber fachlich und
  technisch getrennter Folgeslice.
- Begruendung: Die erste Demonstration soll die vorhandenen, sichtbaren
  Funktionen einfach pruefbar machen. Erklaerungen zu Was, Wie, Warum und
  Wann muessen fuer alle Module einheitlich erreichbar sein, ohne die
  Arbeitsansichten mit funktionslosen V1-Hinweisen zu ueberladen.
- Auswirkung: Die Infokarte nutzt weiter ausschliesslich den kanonischen
  `ma_workflow`-Modulkatalog. Die V1-UI fuegt keine reale Import-,
  Persistenz-, Katalog-, v2-Editor- oder Simulationsfunktion hinzu.
  P014-v2 wird erst im naechsten separat abgegrenzten Fachslice weitergebaut;
  bestehende Vertrags-, Architektur- und Compliance-Gates bleiben wirksam.
- Status: getroffen und im lokalen V1-UI-Slice umgesetzt
- Quelle oder Chatbezug: Nutzerentscheidung `dann lass erstmal v1 bauen aber
  v2 hat hier schonmal ne hohe Prio` am 2026-07-18

## UD-092 Tagesende dokumentiert Nutzerentscheidungen explizit

- Datum: 2026-07-18
- Thema: Codex-Routine `tagesende`
- Entscheidung: Die Tagesende-Routine soll bei getroffenen
  Nutzerentscheidungen den Einzelschritt `entscheidung festhalten` sichtbar
  ausfuehren, bevor der Release vorbereitet wird.
- Begruendung: Entscheidungen sollen im Tagesabschluss nachvollziehbar und
  nicht nur implizit als Teil der allgemeinen Dokumentationspflege bleiben.
- Auswirkung: `UPDATE_ROUTINES.md` und der Triggerindex nennen den Schritt
  jetzt ausdruecklich. `entscheidung festhalten` bleibt ein Einzelbefehl und
  wird dadurch nicht selbst zu einem Sammelbefehl.
- Status: getroffen und dokumentiert
- Quelle oder Chatbezug: Nutzerentscheidung `dann bitte bei tagesende mit
  einbauen` am 2026-07-18
