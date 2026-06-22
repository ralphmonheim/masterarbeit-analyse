# Offene Nutzerentscheidungen

Stand: 2026-06-22

Diese Datei enthaelt nur offene Nutzerentscheidungen. Erledigte Entscheidungen
werden nach der Dokumentation als `UD-*` aus dieser Datei entfernt und stehen in
`USER_DECISIONS_MASTERTHESIS_CODE.md`.

## Offene Punkte

### OP-006 Cooling-Trennung spaeter ins Hauptportal uebernehmen

- Thema: ma_analyse Cooling-Auswertung
- Status: offen
- Frage: Soll nach Abschluss der Diagrammbearbeitung die relative/absolute Cooling-Trennung auch in den regulaeren `cooling`-Befehl und die GUI-Auswahl uebernommen werden?
- Auswirkung: Betrifft spaeter `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/app/cli.py` und `src/ma_analyse/gui/app.py`.

### OP-007 plot-template-weather spaeter als eigener UI-Befehl

- Thema: ma_weather und ma_ui Plot-Template-Struktur
- Status: offen
- Frage: Soll spaeter ein eigener Hauptbefehl `plot-template-weather` eingefuehrt werden, oder bleiben Wetterdiagramme dauerhaft nur im Modulbereich `ma_weather`?
- Auswirkung: Betrifft spaeter `src/ma_weather/`, `src/ma_ui/module_views/weather_view.py` und optional die Analyse-/Template-Navigation in `ma_ui`.

### OP-008 ma_analyse-weite Normierungsstrategie

- Thema: ma_analyse Auswertungen und Diagramme
- Status: offen
- Frage: Welche Auswertungen sollen absolute Werte, flaechenbezogene Werte oder beides anbieten, und welche Bezugsflaeche soll dafuer verwendet werden?
- Auswirkung: Betrifft spaeter `src/ma_analyse/analysis/`, Plot-Templates, Tkinter, Streamlit-Analyse und die Dokumentation der Diagrammeinheiten.

### OP-009 Methodik fuer Zeit- und Personalkostenvergleich

- Thema: Prozessaufwand und Automatisierungsnutzen
- Status: offen
- Frage: Welche Wissensprofile, Stundensaetze, Prozessgrenzen und Messmethoden sollen fuer den Vergleich zwischen manuellem, softwareunterstuetztem und automatisiertem Ablauf verwendet werden?
- Auswirkung: Beeinflusst die wissenschaftliche Vergleichbarkeit, die Prozesskostenrechnung sowie spaetere Ergebnisse in `ma_economy` und `ma_assessment`.
