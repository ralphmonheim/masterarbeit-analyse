# Offene Nutzerentscheidungen

Stand: 2026-06-23

Diese Datei enthaelt nur offene Nutzerentscheidungen. Erledigte Entscheidungen
werden nach der Dokumentation als `UD-*` aus dieser Datei entfernt und stehen in
`USER_DECISIONS_MASTERTHESIS_CODE.md`.

## Offene Punkte

### OP-006 Cooling-Trennung spaeter ins Hauptportal uebernehmen

- Thema: ma_analyse Cooling-Auswertung
- Status: offen
- Frage: Soll nach Abschluss der Diagrammbearbeitung die relative/absolute Cooling-Trennung auch in den regulaeren `cooling`-Befehl und die GUI-Auswahl uebernommen werden?
- Auswirkung: Betrifft spaeter `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/app/cli.py` und `src/ma_analyse/gui/app.py`.

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

### OP-012 Umfang eines IFC-Lite-Imports

- Thema: ma_building und externe Gebaeudemodelle
- Status: offen
- Frage: Welche Inhalte sind in den konkreten IFC-Arbeitsstaenden belastbar
  vorhanden und koennen ohne umfangreiche Geometrieinterpretation sicher
  uebernommen werden?
- Auswirkung: Entscheidet, ob P012 nur Demo-/YAML-Daten oder zusaetzlich einen
  begrenzten IFC-Lite-Adapter umsetzt.

### OP-013 Verbindliche Importformate je Eingabemodul

- Thema: Eingabe- und Datenhaltungsarchitektur
- Status: offen
- Frage: Welche Datei- und Programmvorlagen werden fuer Building, Zones,
  Technical, Parameters und Naming im Masterarbeitsumfang verbindlich
  unterstuetzt?
- Auswirkung: Wird in P010 als Formatmatrix vorbereitet und vor den jeweiligen
  Fachimplementierungen entschieden.
