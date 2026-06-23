# P027 Querschnitt UI, Workflow, Validation und Feedback

Stand: 2026-06-23
Status: Aktiv, begleitend
Prioritaet: Hoch
Abhaengigkeiten: alle P007-Teilplaene

## Ziel

Quellenwahl, Modulstatus, Warnungen, Freigaben, Rueckspruenge und
Serviceaufrufe ueber alle Fachslices konsistent darstellen und steuern.

## Arbeitspakete

- `ma_ui`: Import, manuell und Demo je Modul auswaehlbar darstellen.
- `ma_workflow`: nur freigegebene Fachservices orchestrieren.
- `ma_validation`: gemeinsames Ergebnis fuer Fehler, Warnungen und Freigaben
  definieren.
- `ma_feedback`: Ruecksprungziel und Korrekturauftrag dokumentieren.
- Tkinter-Vorschau, Streamlit-Abgleich und Vorschau-Cache als getrennte
  spaetere Slices fuehren.
- Gezielte Modulverweise mit Ruecksprungziel fuer zentrale Einstellungen in
  `ma_project` und `ma_parameters` bereitstellen.
- Vorlagen in der UI als schreibgeschuetzt kennzeichnen. Bei kollidierenden
  neuen Dateinamen muss eine neue Nutzereingabe erfolgen.

## Akzeptanzkriterien

- Keine Fachberechnung liegt in UI oder Workflow.
- Status stammt weiterhin aus dem zentralen Katalog.
- Jede geplante Karte zeigt eine Infoseite statt funktionsloser Bedienung.
- Freigaben und Rueckspruenge sind fuer den Nutzer nachvollziehbar.
