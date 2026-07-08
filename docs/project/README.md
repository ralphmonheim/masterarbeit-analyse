# Projektorganisation

Dieser Bereich enthaelt die aktive Projektsteuerung.

## Zweck

Planung, Architektur, Entscheidungen, Status, Projektdokumentation und
Archivierung nachvollziehbar fuehren.

## Eingaben

- freigegebene Plaene und Nutzerentscheidungen
- technische Entscheidungen, Pruefergebnisse und Projektstaende
- temporaere Entwicklungsinputs aus `data/project_inbox/`, wenn sie mit
  `projektinput aufnehmen` in bestehende Zielordner einsortiert werden

## Ausgaben

- aktive Steuerdokumente, Leitfaden, Architekturstand und Archive

## Abgrenzung

- kein Python-Paket
- keine Fachberechnung und kein Ersatz fuer Modulberichte

## Abhaengigkeiten

- dokumentierte Arbeitsroutinen und Ergebnisse aller Projektmodule

## Status

Verfuegbar. Die Dokumentationsinfrastruktur bleibt vollstaendig unter `docs`.

## Naechster Schritt

Planstatus, Entscheidungen und Changelog bei jedem freigegebenen Slice
fortschreiben.

- `MASTERARBEIT_LEITFADEN.md`: zentraler Orientierungsleitfaden fuer Ziel,
  Workflow, Module, Datenstruktur, UI und offene Strukturpunkte. Die aktive
  Datei fuehrt eine eigene Leitfaden-Version.
- `plans/`: Plaene, Status, Strukturreview, Cleanup-Plan und Umsetzungshinweise.
- `decisions/`: technische Entscheidungen, Nutzerentscheidungen und offene Entscheidungsfragen.
- `architecture/`: Zielarchitektur, Gesamtworkflow und UI-Auslagerungsreview.
- `archive/leitfaeden/`: archivierte Leitfadenfassungen und externe Referenzen.
- `archive/plans/`: archivierte und alte Planstaende.
- `archive/workflow/`: ersetzte Workflow-Grafiken und zugehoerige Reviews.

Temporaere neue Projektdateien koennen waehrend der Entwicklungsphase zuerst
unter `data/project_inbox/new/` gesammelt werden. Dieser Eingang ist kein
dauerhafter Dokumentationsbereich; Codex verteilt eindeutige Inhalte mit
`projektinput aufnehmen` in die bestehenden Projekt-, Modul- und lokalen
Datenordner.

Vor groesseren Umsetzungen zuerst `plans/PLAN_STATUS.md`, `plans/PLAN_INDEX.md`, `architecture/` und die offenen Nutzerentscheidungen pruefen.
