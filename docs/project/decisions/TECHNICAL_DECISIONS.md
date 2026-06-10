# Entscheidungen

Stand: 2026-06-10

Dieses Dokument sammelt technische und architektonische Entscheidungen. Echte Nutzerentscheidungen stehen getrennt in `USER_DECISIONS_MASTERTHESIS_CODE.md`.

## Entscheidung 1: Modularer Aufbau

Das Projekt wird modular weiterentwickelt. Der bestehende Analysecode bleibt als eigenes Analyse-Subsystem erhalten. Neue Funktionen fuer Parameterkatalog, Optionskatalog, Variantenmanagement, Auswahl, Naming, IDA-Export, Wirtschaftlichkeit und Reporting werden schrittweise getrennt vorbereitet.

Begruendung:

- Die vorhandene Analysepipeline ist bereits nutzbar und soll nicht durch einen grossen Umbau gefaehrdet werden.
- Neue fachliche Bereiche koennen einzeln getestet und dokumentiert werden.
- Spaetere Erweiterungen wie Produktkatalog, Materialkatalog und Weboberflaeche erhalten klare Grenzen.

## Entscheidung 2: PostgreSQL als spaetere zentrale Datenbank

PostgreSQL bleibt als spaetere zentrale Zieldatenbank vorgesehen. SQLAlchemy-Modelle, Alembic-Migrationen und Repository-Funktionen sind im Variantenkern vorbereitet.

Begruendung:

- Varianten, Parameter, Optionswerte, Systemvorlagen, Importlogs und spaetere Bewertungsergebnisse brauchen stabile Relationen.
- PostgreSQL ist robust fuer strukturierte Projektdaten und spaetere Auswertungen.
- SQLAlchemy und Alembic bilden die technische Grundlage fuer Modelle und Migrationen.

## Entscheidung 3: Bestehende Analysefunktionen bleiben unveraendert

Die vorhandenen Module unter `src/ma_analyse` werden in diesem Schritt nicht umgebaut, verschoben oder geloescht.

Begruendung:

- Sie bilden den aktuellen funktionsfaehigen Kern fuer Simulationsergebnis-Auswertung.
- Der neue Variantenkern soll zunaechst als Erweiterung daneben entstehen.
- Eine spaetere Anbindung erfolgt bewusst ueber Adapter oder klar definierte Schnittstellen.

## Entscheidung 4: Dokumentation vor Fachlogik

Vor der Implementierung neuer Varianten-, Datenbank- oder Exportlogik wird zuerst die Projektstruktur dokumentiert.

Begruendung:

- Die fachlichen Grenzen werden klarer.
- Der Umsetzungsumfang von Version 1 bleibt kontrollierbar.
- Spaetere Codeaenderungen lassen sich gegen Plan, Workflow und Datenmodell pruefen.

## Entscheidung 5: Modulare Dokumentationsstruktur

Die Dokumentation wird nach Projektorganisation und Fachmodulen gegliedert.

Begruendung:

- Das Projekt umfasst inzwischen Analyse, Variantenkern, spaetere Wetterdatenanalyse und Bewertung.
- Eine flache `docs/`-Struktur wuerde Planstatus, Fachworkflow und Entscheidungen vermischen.
- Modulbezogene Dokumente lassen sich gezielter pflegen.

## Entscheidung 6: ma_variants zuerst modular migrieren

Die Konfigurations- und Datenbereiche des neuen Variantenkerns werden zuerst modularisiert.

Begruendung:

- `ma_variants` ist neuer und klarer gekapselt als die bestehende Analysepipeline.
- Die Migration ist risikoaermer als eine sofortige Umstellung von `ma_analyse`.
- Tests koennen die neuen Pfade direkt pruefen.

## Entscheidung 7: ma_analyse-Datenpfade hart migriert

`ma_analyse` nutzt ab dem 2026-06-04 nur noch die Modulpfade `data/ma_analyse/ida_imports`, `data/ma_analyse/database` und `data/ma_analyse/output`.

Begruendung:

- Die Analysepipeline ist damit konsistent zur modularen Datenstruktur.
- Alte Root-Pfade werden nicht als Fallback erhalten.
- `data/test_output/` bleibt bewusst separat als lokaler Smoke-Test- und Arbeitsordner.

## Entscheidung 8: Produkt- und Materialdokumente als Katalogdaten

Produkt- und Materialdokumente liegen unter `data/catalogs/documents/` und nicht direkt im Variantenmodul.

Begruendung:

- Produkt- und Materialdaten betreffen spaeter auch Quellen, Bewertung und Wirtschaftlichkeit.
- PostgreSQL speichert nur Pfade und Metadaten, nicht die Datenblaetter selbst.
- Der Katalogbereich bleibt fachlich klarer als eine Ablage unter `data/ma_variants/`.

## Entscheidung 9: Dokumentierte Codex-Routinen statt Python-CLI fuer Repo-Updates

Repo-Updates, direkte Repo-Updates und Planungsupdates werden als dokumentierte Arbeitsroutinen gefuehrt.

Begruendung:

- Die Ablaeufe betreffen Git, Changelog, Versionierung und Planstatus, nicht die Fachlogik des Python-Pakets.
- Eine Dokumentationsroutine ist fuer den Nutzer transparenter als ein zusaetzlicher CLI-Befehl.
- Die Dateien `pyproject.toml`, `src/ma_analyse/__init__.py`, `CHANGELOG.md`, `PLAN_INDEX.md`, `PLAN_STATUS.md` und die Entscheidungsdateien bleiben explizit als Pruefstellen dokumentiert.

## Entscheidung 10: Plot-Template-Varianten ueber Template-Namen statt Modusoption

Heating-Overlay und Cooling-Absolute werden als eigene Plot-Template-Namen gefuehrt.

Begruendung:

- Die Galerie unter `docs/examples/plot_templates/` kann fuer jede fachliche Darstellung ein stabiles Referenzbild enthalten.
- Die CLI bleibt fuer einzelne Diagrammideen eindeutig: `heating-overlay` und `cooling-absolute-year` beschreiben direkt die gewuenschte Darstellung.
- Bestehende Templates bleiben rueckwaertskompatibel nutzbar, ohne eine zusaetzliche globale Modusoption einzufuehren.

## Entscheidung 11: ma_weather getrennt von ma_analyse

Das Wettermodul wird als eigenes Paket `src/ma_weather/` aufgebaut. TRY-Dateien
bleiben lokale Eingangs- und Randbedingungsdaten unter `data/ma_weather/input/`
und werden nicht mit den IDA-ICE-Zonenwerten aus `ma_analyse` vermischt.

Begruendung:

- Wetterdaten beschreiben Randbedingungen, waehrend `ma_analyse` Simulationsergebnisse auswertet.
- Reale TRY-Dateien sollen lokal bereitgestellt und nicht im Git-Repo versioniert werden.
- Die spaetere Verbindung zu Varianten kann ueber den technischen `weather_key` erfolgen.

## Entscheidung 12: ma_analyse-Service zuerst als Fassade umsetzen

Die UI-neutrale Service-Schnittstelle fuer `ma_analyse` wird zuerst als Fassade
ueber bestehender Logik umgesetzt. `AnalysisConfig`, `AnalysisResult` und
`run_analysis(config)` ermoeglichen die spaetere UI-Anbindung, ohne die
bestehende CLI, Tkinter-GUI oder Fachmodule sofort umzubauen.

Begruendung:

- `src/ma_analyse/gui/app.py` ist stark mit Tkinter-State, Worker-Thread und
  Pipelineaufrufen gekoppelt.
- `src/ma_analyse/app/commands.py` ist bereits ein guter Einstiegspunkt, aber
  noch CLI-nah durch `argparse.Namespace`, `print()` und `SystemExit`.
- Eine Fassade reduziert Risiko, weil sie bestehende Funktionen nutzt und
  spaeter schrittweise bessere Rueckgabeobjekte ermoeglicht.
- Streamlit kann spaeter ueber `ma_ui` dieselbe Service-Schicht nutzen, ohne
  Fachlogik in der Oberflaeche zu duplizieren.

## Entscheidung 13: ma_workflow und ma_ui zuerst als minimale Shell

`ma_workflow` wird zuerst als neutrale Orchestrierungsschicht mit Workflow-
Katalog und Analyse-Adapter umgesetzt. `ma_ui` wird zuerst als minimale
Streamlit-Shell mit Startseite, Navigation, Projektzustand und Analyse-Seite
umgesetzt.

Begruendung:

- Die neue UI braucht stabile Einstiegspunkte, darf aber keine Fachlogik
  enthalten.
- `ma_workflow` trennt UI-Bedienaktionen von Fachmodulaufrufen.
- Die bestehende Tkinter-GUI bleibt unveraendert, bis ein eigener
  Legacy-Auslagerungsslice freigegeben ist.
- Weitere Fachseiten koennen spaeter einzeln angebunden werden.

## Entscheidung 14: P005-Zielstruktur strenger als aktueller Codezustand

Die aktuelle `ma_ui`- und `ma_workflow`-Implementierung ist ein bewusst kleiner
Zwischenstand. Die Zielstruktur sieht spaeter eine klarere Aufteilung vor:

- `ma_ui/main_dashboard.py`
- `ma_ui/workflow_view.py`
- `ma_ui/pre_process_view.py`
- `ma_ui/post_process_view.py`
- `ma_ui/shared/`
- `ma_ui/module_views/`
- `ma_workflow/workflow_manager.py`
- `ma_workflow/dashboard_actions.py`
- `ma_workflow/pre_process_runner.py`
- `ma_workflow/post_process_runner.py`
- `ma_workflow/feedback_router.py`

Begruendung:

- Die UI soll den Gesamtworkflow fuehren und gemeinsame Komponenten nicht in
  einzelnen Seiten duplizieren.
- `ma_workflow` soll Button-/Dashboard-Aktionen von Fachservices trennen.
- Eine sofortige Umbenennung bestehender Dateien waere unnoetiges Risiko,
  weil Tests und Importpfade betroffen sind.

## Entscheidung 15: Tkinter wird nicht technisch nach Streamlit uebersetzt

Die bestehende Tkinter-GUI in `src/ma_analyse/gui/` wird als fachliche
Ablaufquelle genutzt, aber nicht als technische Vorlage fuer Streamlit.

Begruendung:

- Tkinter-Widgets, Messageboxen, Worker-Threads und GUI-State sind eng mit der
  aktuellen Datei `src/ma_analyse/gui/app.py` gekoppelt.
- Streamlit braucht eine andere Zustands- und Anzeigeform.
- Die fachliche Analyse muss ueber neutrale Services nutzbar bleiben.

Technische Folge:

- Allgemeine Anzeige- und Bedienbausteine entstehen spaeter in `ma_ui/shared/`.
- Analysebezogene Bedienung entsteht spaeter in
  `ma_ui/module_views/analyse_view.py`.
- Fachliche Analysefunktionen bleiben in `ma_analyse`.
