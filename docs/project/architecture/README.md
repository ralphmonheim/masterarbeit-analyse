# Projektarchitektur

Dieser Bereich dokumentiert die Zielarchitektur des Masterarbeitsprojekts.
Er ist Planungs- und Entscheidungsgrundlage, keine Fachlogik.

## Dateien

- `TARGET_ARCHITECTURE.md`: Zielmodule, Workflow und Dashboard-Zuordnung.
- `UI_EXTRACTION_REVIEW.md`: Pruefung der bestehenden Oberflaechen und Vorschlag fuer eine spaetere UI-Auslagerung.
- `UI_MIGRATION_PLAN.md`: Phasenplan fuer Streamlit-Ziel-UI, Tkinter-Legacy und UI-neutrale Fachlogik.

## Regeln

- Bestehende Module werden nicht automatisch umbenannt, verschoben oder aufgeteilt.
- Fachlogik bleibt in den Fachmodulen.
- `ma_ui` soll spaeter die zentrale Streamlit-Oberflaeche und Navigation enthalten.
- Tkinter-Bestand bleibt zunaechst Legacy und wird nicht direkt mit Streamlit vermischt.
- `ma_workflow` soll spaeter Prozesssteuerung zwischen UI und Fachmodulen enthalten.
- Eine Auslagerung aus `ma_analyse/gui/` braucht einen eigenen freigegebenen Refactoring-Plan.
