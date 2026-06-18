# Projektarchitektur

Dieser Bereich dokumentiert die Zielarchitektur des Masterarbeitsprojekts.
Er ist Planungs- und Entscheidungsgrundlage, keine Fachlogik.

## Dateien

- `TARGET_ARCHITECTURE.md`: Zielmodule, Workflow und Dashboard-Zuordnung.
- `UI_EXTRACTION_REVIEW.md`: Pruefung der bestehenden Oberflaechen und Vorschlag fuer eine spaetere UI-Auslagerung.
- `UI_MIGRATION_PLAN.md`: Phasenplan fuer Streamlit-Ziel-UI, Tkinter-Legacy und UI-neutrale Fachlogik.
- `MA_ANALYSE_INVENTORY.md`: Bestandsanalyse von `ma_analyse` fuer P005.
- `MA_ANALYSE_SERVICE_INTERFACE.md`: Zielvertrag fuer `AnalysisConfig`, `AnalysisResult` und `run_analysis(config)`.
- `workflow/`: aktuelle Workflow-Diagramme und fachliche Strukturreviews.

## Regeln

- Bestehende Module werden nicht automatisch umbenannt, verschoben oder aufgeteilt.
- Fachlogik bleibt in den Fachmodulen.
- `ma_ui` enthaelt aktuell eine minimale Streamlit-Shell; Ziel sind Dashboard,
  Workflow-Views, `shared/`-Komponenten und `module_views/`.
- Tkinter-Bestand bleibt zunaechst Legacy und wird nicht direkt mit Streamlit vermischt.
- Die bestehende Tkinter-GUI dient als fachliche Ablaufvorlage, nicht als
  technische Streamlit-Vorlage.
- `ma_workflow` enthaelt einen ersten neutralen Workflow-Katalog und
  Prozessadapter zwischen UI und Fachmodulen; Ziel sind Dashboard-Aktionen,
  Pre-/Post-Process-Runner und Feedback-Routing.
- Eine Auslagerung aus `ma_analyse/gui/` braucht einen eigenen freigegebenen Refactoring-Plan.
