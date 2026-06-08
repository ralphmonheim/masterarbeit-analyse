# Offene Nutzerentscheidungen

Stand: 2026-06-08

Diese Datei enthaelt nur offene Nutzerentscheidungen. Erledigte Entscheidungen
werden nach der Dokumentation als `UD-*` aus dieser Datei entfernt und stehen in
`USER_DECISIONS_MASTERTHESIS_CODE.md`.

## Offene Punkte

### OP-006 Cooling-Trennung spaeter ins Hauptportal uebernehmen

- Thema: ma_analyse Cooling-Auswertung
- Status: offen
- Frage: Soll nach Abschluss der Diagrammbearbeitung die relative/absolute Cooling-Trennung auch in den regulaeren `cooling`-Befehl und die GUI-Auswahl uebernommen werden?
- Auswirkung: Betrifft spaeter `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/app/cli.py` und `src/ma_analyse/gui/app.py`.
