# Projektarchitektur

Dieser Bereich dokumentiert die Zielarchitektur des Masterarbeitsprojekts.
Er ist Planungs- und Entscheidungsgrundlage, keine Fachlogik.

## Dateien

- `TARGET_ARCHITECTURE.md`: Zielmodule, Workflow und Dashboard-Zuordnung.
- `UI_EXTRACTION_REVIEW.md`: Pruefung der bestehenden Oberflaechen und
  Historie der UI-Auslagerung.
- `UI_MIGRATION_PLAN.md`: Phasenplan fuer Streamlit, Tkinter und
  UI-neutrale Fachlogik.
- `MA_ANALYSE_INVENTORY.md`: Bestandsanalyse von `ma_analyse` fuer P005.
- `MA_ANALYSE_SERVICE_INTERFACE.md`: Zielvertrag fuer `AnalysisConfig`, `AnalysisResult` und `run_analysis(config)`.
- `workflow/`: aktuelle Workflow-Diagramme und fachliche Strukturreviews.
- `reviews/2026-07-15/`: datierter, nicht autoritativer P032-Benchmark mit
  Ist-Inventar, Modulgrenzen, Zieloptionen und Migrationsentwurf.

## Regeln

- Bestehende Module werden nicht automatisch umbenannt, verschoben oder aufgeteilt.
- Fachlogik bleibt in den Fachmodulen.
- `ma_ui` enthaelt aktuell ein Workflow-Dashboard, Kopfzeilen-Navigation,
  vorbereitete Streamlit-Komponenten unter `streamlit_app/` sowie angebundene
  Ansichten fuer Analyse, Varianten, Wetter und vorhandene
  Wirtschaftlichkeitsannahmen.
- Tkinter liegt als eigener technischer UI-Zweig unter `ma_ui/tkinter_app/`
  und wird nicht direkt mit Streamlit vermischt.
- Die bestehende Tkinter-Analyse dient fachlich weiter als Ablaufvorlage,
  nicht als technische Streamlit-Vorlage.
- `ma_workflow` enthaelt den zentralen Phasen-, Modul-, Workflow- und
  Statuskatalog, Dashboard-Aktionen, Kompatibilitaetslisten,
  Feedback-Routing und den Analyse-Adapter. Echte Fachservice-Orchestrierung
  bleibt ein spaeterer Ausbau.
- `ma_analyse` enthaelt keinen Tkinter-Kompatibilitaetspfad mehr; die
  Tkinter-Analyse liegt ausschliesslich unter
  `ma_ui.tkinter_app.module_views.analyse`.
