# ma_workflow

`ma_workflow` ist die neutrale Orchestrierungsschicht zwischen Oberflaeche und
Fachmodulen.

## Rolle

- beschreibt den Gesamtworkflow der Masterarbeit
- gruppiert Schritte nach Pre-Process, Simulation, Post-Process und Feedback
- stellt Adapter fuer Fachmodulaufrufe bereit
- enthaelt keine Streamlit- oder Tkinter-Abhaengigkeit
- enthaelt keine fachliche Berechnungslogik

## Aktueller Stand

- Workflow-Katalog ist umgesetzt.
- `workflow_manager.py` stellt den zentralen Zugriff auf Workflow-Schritte bereit.
- `dashboard_actions.py` dokumentiert UI-Aktionen wie `open_weather`,
  `open_simulation_setup`, `run_analysis` und `run_assessment`.
- `pre_process_runner.py` und `post_process_runner.py` trennen die geplanten
  Schritte vor und nach der IDA-ICE-Simulation.
- `feedback_router.py` enthaelt die geplanten Ruecksprungziele fuer Feedback.
- Analyse-Adapter ruft `ma_analyse.services.run_analysis(config)` auf.
- Weitere Adapter fuer Varianten, Wetterdaten, IDA-Export, IDA-Import und
  Bewertung folgen spaeter nach separaten Slices.
