# Entscheidungen

Stand: 2026-06-05

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

`ma_analyse` nutzt ab dem 2026-06-04 nur noch die Modulpfade `data/ma_analyse/input`, `data/ma_analyse/database` und `data/ma_analyse/output`.

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
