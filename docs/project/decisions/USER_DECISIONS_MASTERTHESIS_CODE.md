# Nutzerentscheidungen Masterarbeit Code

Stand: 2026-06-08

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
- Entscheidung: `ma_analyse` nutzt ab jetzt die neuen Modulpfade `data/ma_analyse/input`, `data/ma_analyse/database` und `data/ma_analyse/output`; bisherige Daten werden transferiert und alte Root-Strukturen geloescht.
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
