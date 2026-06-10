# Nutzerentscheidungen Masterarbeit Code

Stand: 2026-06-10

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
- Entscheidung: `docs/examples/plot_templates/` soll von jedem `ma_analyse`-Testbefehl das aktuellste wichtige Diagramm enthalten.
- Begruendung: Diese Beispiele sind fuer Pruefung und Dokumentation belastbar.
- Auswirkung: `docs/examples/plot_templates/` wird nicht wie `data/test_output/` behandelt.
- Betroffene Module oder Dateien: `docs/examples/plot_templates/`, `docs/ma_analyse/plot_template_examples.md`
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
- Betroffene Module oder Dateien: `src/ma_analyse/analysis/templates/`, `docs/ma_analyse/commands_analyse.md`, `docs/examples/plot_templates/`
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
- Betroffene Module oder Dateien: `src/ma_analyse/analysis/templates/`, `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/app/cli.py`, `src/ma_analyse/gui/app.py`
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
- Betroffene Module oder Dateien: `src/ma_ui/`, `src/ma_workflow/`, bestehend `src/ma_analyse/gui/`, `src/ma_variants/ui/`
- Status: getroffen
- Offene Folgefragen: Welche Fachseite wird als naechstes konkret angebunden?
- Quelle oder Chatbezug: P005 Gesamtmodulstruktur

## UD-016 ma_analyse-Fachlogik bleibt in ma_analyse

- Datum: 2026-06-08
- Thema: Analysemodul und UI-Auslagerung
- Entscheidung: Fachliche Analysefunktionen verbleiben in `ma_analyse`. Allgemein nutzbare UI-Bestandteile aus `ma_analyse` duerfen spaeter geprueft und nach Freigabe in `ma_ui` oder Legacy-Bestandteile in `ma_ui_legacy` ueberfuehrt werden.
- Begruendung: Die bestehende Analysepipeline ist funktionsfaehig und soll nicht durch eine direkte GUI-Verschiebung gefaehrdet werden.
- Auswirkung: `src/ma_analyse/gui/app.py` wird zuerst dokumentarisch bewertet. Eine Auslagerung braucht einen separaten Refactoring-Plan.
- Betroffene Module oder Dateien: `src/ma_analyse/gui/`, spaeter `src/ma_ui/pages/analyse.py`, `src/ma_ui_legacy/`
- Status: getroffen
- Offene Folgefragen: Welche Bestandteile der Tkinter-GUI sind fachliche Analyse, welche Legacy-UI und welche neutralen Helfer?
- Quelle oder Chatbezug: P005 Gesamtmodulstruktur

## UD-017 IDA-Export, IDA-Import, Simulation-Setup, Assessment und Feedback trennen

- Datum: 2026-06-08
- Thema: Gesamtworkflow
- Entscheidung: `ma_simulation_setup`, `ma_export_ida`, `ma_import_ida`, `ma_assessment` und `ma_feedback` werden als eigene Zielmodule gefuehrt. `ma_assessment` soll intern in Economics und Sustainability trennen.
- Begruendung: Simulationsrandbedingungen, IDA-Uebergabe, Ergebnisimport, Bewertung und Rueckkopplung haben unterschiedliche Verantwortlichkeiten.
- Auswirkung: Bestehende Logik in `ma_variants.ida_export`, `ma_variants.simulation_results` und `ma_variants.economic_analysis` bleibt vorerst bestehen und wird nur als spaetere Extraktionsquelle dokumentiert.
- Betroffene Module oder Dateien: `src/ma_variants/ida_export.py`, `src/ma_variants/simulation_results.py`, `src/ma_variants/economic_analysis/`, spaeter neue Zielmodule
- Status: getroffen
- Offene Folgefragen: Nach P005-UI-Migrationsplan zuerst `ma_analyse`-Bestandsanalyse und Schnittstellenentwurf pruefen.
- Quelle oder Chatbezug: P005 Gesamtmodulstruktur

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

## UD-019 Tkinter bleibt Legacy und wird nicht mit Streamlit vermischt

- Datum: 2026-06-08
- Thema: Umgang mit bestehender Tkinter-GUI
- Entscheidung: Die bestehende Tkinter-Oberflaeche aus `ma_analyse` wird vorerst als Legacy-Bestand behandelt und nicht direkt mit Streamlit vermischt. Eine spaetere Auslagerung nach `ma_ui_legacy` wird geplant.
- Begruendung: Die bestehende Arbeit soll gesichert werden, ohne die neue Streamlit-Zielarchitektur technisch zu vermischen.
- Auswirkung: `src/ma_analyse/gui/` bleibt zunaechst bestehen. Eine Verschiebung nach `src/ma_ui_legacy/` erfolgt nur nach Bestandsanalyse und Freigabe.
- Betroffene Module oder Dateien: `src/ma_analyse/gui/`, spaeter `src/ma_ui_legacy/`
- Status: getroffen
- Offene Folgefragen: konkrete Auslagerung erst nach Tkinter-Bestandsanalyse.
- Quelle oder Chatbezug: P005 Anpassung Streamlit-Ziel-UI

## UD-020 ma_analyse erhaelt eine UI-neutrale Service-Schnittstelle

- Datum: 2026-06-08
- Thema: Analysemodul und Service-Schnittstelle
- Entscheidung: `ma_analyse` wird ueber neutrale Modelle wie `AnalysisConfig` und `AnalysisResult` sowie eine Service-Funktion `run_analysis(config)` fuer Oberflaechen nutzbar gemacht.
- Begruendung: Streamlit, Tkinter oder andere UIs sollen dieselbe fachliche Analyse verwenden koennen, ohne Berechnungslogik in die UI zu verschieben.
- Auswirkung: Bestandsanalyse, Schnittstellenentwurf und erster Service-Code-Slice sind umgesetzt. Die minimale `ma_ui`-Analyse-Seite nutzt die Service-Fassade bereits ueber `ma_workflow`.
- Betroffene Module oder Dateien: `src/ma_analyse/services.py`, `src/ma_analyse/models.py`, `src/ma_ui/pages/analyse.py`
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
- Status: getroffen
- Offene Folgefragen: Welche Simulationsrandbedingungen werden im ersten Slice von `ma_simulation_setup` benoetigt?
- Quelle oder Chatbezug: P005 verschaerfte Modulstruktur

## UD-022 Tkinter-GUI ist fachliche Ablaufvorlage, keine technische Vorlage

- Datum: 2026-06-10
- Thema: UI-Migration
- Entscheidung: Die bestehende Tkinter-GUI aus `ma_analyse` wird fuer den fachlichen Ablauf ausgewertet, aber nicht direkt nach Streamlit kopiert oder uebersetzt.
- Begruendung: Die Tkinter-Dateien enthalten wertvolle Bedienlogik, sind technisch aber stark mit Widgets, Messageboxen, Threads und GUI-State gekoppelt.
- Auswirkung: Streamlit-Ansichten werden neu ueber `ma_ui`, `ma_workflow` und UI-neutrale Fachservices aufgebaut. Tkinter bleibt bis zu einem separaten Refactoring-Slice Legacy-Bestand.
- Betroffene Module oder Dateien: `src/ma_analyse/gui/`, spaeter `src/ma_ui/module_views/analyse_view.py`, `src/ma_ui_legacy/`
- Status: getroffen
- Offene Folgefragen: Welche konkreten GUI-Validierungen sollen in die Service-Schicht uebernommen werden?
- Quelle oder Chatbezug: P005 verschaerfte UI-Ueberfuehrung

## UD-023 ma_ui nutzt Dashboard, Workflow-Views, Shared-Komponenten und Module-Views

- Datum: 2026-06-10
- Thema: Streamlit-Zieloberflaeche
- Entscheidung: `ma_ui` soll langfristig aus Dashboard, Workflow-Ansichten, gemeinsamen UI-Komponenten und modulbezogenen Views bestehen.
- Begruendung: Die Oberflaeche soll den Gesamtworkflow fuehren, aber keine Fachlogik enthalten. Gemeinsame UI-Bausteine sollen nicht in einzelnen Modulseiten dupliziert werden.
- Auswirkung: Die bestehende `src/ma_ui/pages/`-Shell bleibt ein Zwischenstand. Eine spaetere Migration nach `module_views/` und `shared/` braucht einen eigenen Umsetzungsslice.
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
- Status: getroffen
- Offene Folgefragen: Wann beginnt die Trennung von Economics und Sustainability?
- Quelle oder Chatbezug: P005 verschaerfte Bewertungsstruktur
