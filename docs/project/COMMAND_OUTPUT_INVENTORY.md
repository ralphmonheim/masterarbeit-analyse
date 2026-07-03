# Befehls- und Ausgabeninventar

Stand: 2026-07-03

Diese Uebersicht buendelt die bisher aufgebauten Befehle, Ausgaben und
Frontend-/Backend-Verbindungen. Sie ersetzt nicht die Modul-Befehlsdateien,
sondern dient als schneller Statusabgleich.

## Aktive Befehle

| Modul | Befehl oder Ausgabe | Backend | Streamlit | Tkinter | Status | Nachweis |
|---|---|---:|---:|---:|---|---|
| `ma_ui` | `python -m streamlit run src/ma_ui/app.py` | ja, UI-Shell | ja | nein | nutzbar | `docs/ma_ui/commands_ui.md`, `src/ma_ui/app.py` |
| `ma_ui` | Workspace-/Workflow-Modus | ja, Navigation | ja | nein | minimal umgesetzt | `src/ma_ui/streamlit_app/app.py`, `src/ma_ui/streamlit_app/navigation.py` |
| `ma_ui` | `Tkinter-Analyse oeffnen` | ja, Launcher und `AnalysisConfig`-Adapter | ja | ja, separater Prozess | nutzbar | `src/ma_ui/tkinter_app/launcher.py`, `src/ma_ui/tkinter_app/module_views/analyse/pipeline_config.py`, `src/ma_ui/tkinter_app/module_views/analyse/pipeline_runner.py` |
| `ma_workflow` | zentraler Modulkatalog | ja | ja, Modulinfos und Startseite | nein | nutzbar | `src/ma_workflow/catalog.py`, `docs/ma_workflow/commands_workflow.md` |
| `ma_weather` | `python -m ma_weather.run_weather_analysis --weather-key ...` | ja | ja, Wetterdaten-Seite | nein | nutzbar | `src/ma_weather/run_weather_analysis.py`, `docs/ma_weather/commands_weather.md` |
| `ma_weather` | `plot-template-weather <diagramm> --weather-key ...` | ja | ja, Wetterdiagramm-Auswahl | nein | nutzbar | `pyproject.toml`, `src/ma_weather/run_weather_analysis.py` |
| `ma_weather` | Wetterdiagramme `all`, `temperature_year`, `temperature_heatmap`, `monthly_radiation`, `monthly_degree_hours`, `wind_rose`, `temperature_humidity_scatter` | ja | ja | nein | nutzbar | `src/ma_weather/weather_plots.py` |
| `ma_weather` | TRY-Import, Scan, Validierung, Aktivierung | ja | ja | nein | teilweise umgesetzt | `src/ma_ui/streamlit_app/pages/weather.py`, `src/ma_weather/weather_file_discovery.py` |
| `ma_analyse` | `prepare` | ja | ja, Analyse-Wizard | ja | nutzbar | `docs/ma_analyse/commands_analyse.md`, `src/ma_analyse/app/cli.py` |
| `ma_analyse` | `comfort` | ja | ja, Analyse-Wizard | ja | nutzbar | `docs/ma_analyse/commands_analyse.md`, `src/ma_analyse/analysis_wizard.py` |
| `ma_analyse` | `analyze-data` | ja | ja, Analyse-Wizard | ja | nutzbar | `docs/ma_analyse/commands_analyse.md`, `src/ma_analyse/analysis_ui.py` |
| `ma_analyse` | `heating` | ja | ja, Analyse-Wizard | ja | nutzbar | `docs/ma_analyse/commands_analyse.md`, `src/ma_analyse/analysis/` |
| `ma_analyse` | `cooling` | ja | ja, Analyse-Wizard | ja | nutzbar | `docs/ma_analyse/commands_analyse.md`, `src/ma_analyse/analysis/` |
| `ma_analyse` | `plot-template` / Streamlit `plot-template-analyse` | ja | ja, Analyse-Wizard | ja | nutzbar | `src/ma_analyse/analysis/templates.py`, `src/ma_ui/streamlit_app/module_views/analyse_view.py` |
| `ma_analyse` | `plot-template-examples` | ja | nein | nein | CLI/Referenz | `docs/ma_analyse/commands_analyse.md`, `docs/ma_analyse/plot_template_examples.md` |
| `ma_analyse` | `all` | ja | nein | teilweise ueber Tkinter | CLI/Legacy | `docs/ma_analyse/commands_analyse.md` |
| `ma_analyse.settings` | `python -m ma_analyse.settings.naming --dry-run` | ja | nein | nein | CLI/Pruefung | `docs/ma_analyse/commands_analyse.md` |
| `ma_variants` | `python -m streamlit run src/ma_variants/ui/app.py` | teilweise | teilweise, eigene alte UI | nein | uebergangsweise | `docs/ma_variants/commands_variants.md` |

## Ausgaben Nach Modul

| Modul | Ausgabe | Backend | Streamlit | Tkinter | Status | Nachweis |
|---|---|---:|---:|---:|---|---|
| `ma_core` | InputSource, IDs, Sitzungslogs | ja | indirekt | nein | nutzbar fuer Wetterpilot | `src/ma_core/`, `src/ma_weather/run_weather_analysis.py` |
| `ma_validation` | Diagnosen, Freigabestatus, Entscheidungen | ja | ja, Wetterdaten-Seite | nein | nutzbar fuer Wetterpilot | `src/ma_validation/`, `src/ma_ui/streamlit_app/pages/weather.py` |
| `ma_weather` | aufbereitete CSV | ja | als Ergebnisdatei sichtbar | nein | nutzbar | `data/ma_weather/output/<weather_key>/<run_id>/data/`, `src/ma_weather/run_weather_analysis.py` |
| `ma_weather` | PNG-Wetterdiagramme | ja | ja, Vorschau | nein | nutzbar | `data/ma_weather/output/<weather_key>/<run_id>/plots/`, `src/ma_weather/weather_plots.py` |
| `ma_weather` | Markdown-Wetterbericht | ja | als Ausgabedatei sichtbar | nein | nutzbar | `data/ma_weather/output/<weather_key>/<run_id>/reports/`, `src/ma_weather/weather_report.py` |
| `ma_weather` | Wetter-Run-Manifest | ja | als Ergebnisdatei sichtbar | nein | nutzbar | `data/ma_weather/output/<weather_key>/<run_id>/weather_run_manifest.json`, `src/ma_weather/weather_outputs.py` |
| `ma_weather` | kritische Wetterereignisse | ja | ja | nein | nutzbar | `src/ma_weather/weather_events.py` |
| `ma_analyse.data_preparation` | Raumtabellen, Basisbericht, Excel-Datenuebersicht | ja | ja, Wizard | ja | nutzbar | `src/ma_analyse/`, `docs/ma_analyse/commands_analyse.md` |
| `ma_analyse.stage_2_optimization` | Variantenvergleiche, Diagramme, Tabellen | ja | ja, Wizard | ja | nutzbar | `src/ma_analyse/analysis/`, `src/ma_ui/streamlit_app/module_views/analyse_view.py` |
| `ma_analyse.stage_3_standards_compliance` | ComplianceReport, Pass/Fail/Warnung | nein | nur Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_analyse.stage_4_sensitivity` | Sensitivitaetsvergleiche, kritische Zeitraeume | nein | nur Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_variants` | Varianten, Variantenwerte, Metadaten | teilweise | teilweise | nein | geplant/Bestandskern | `src/ma_workflow/catalog.py`, `docs/ma_variants/commands_variants.md` |
| `ma_project` | Projektkonfiguration, Benennungsprofil | nein | Modulinfo/P028-Ansicht | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_building` | validierte Gebaeudedaten | nein | Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_zones` | validierte Zonendaten | nein | Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_technical` | validierte Technikdaten | nein | Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_parameters` | zentrale Parameterliste, Optionsgruppen | nein | P028-Ansicht/Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_simulation_setup` | Run- und Simulationskonfiguration | nein | Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_export_simulation` | Exportpaket, Run-Manifest | nein | Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ida_ice` | Simulationsergebnisse, Meldungen | extern | Modulinfo | nein | manuell | `src/ma_workflow/catalog.py` |
| `ma_import_simulation` | standardisierte Simulationsergebnisse | nein | Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_economy` | wirtschaftliche Vergleichsergebnisse | nein | Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_sustainability` | CO2-, GWP- und Nachhaltigkeitsergebnisse | nein | Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_assessment` | Scores, Rankings, Entscheidungsvorlagen | teilweise | teilweise | nein | geplant/Grundansicht | `src/ma_workflow/catalog.py`, `src/ma_ui/streamlit_app/module_views/assessment_view.py` |
| `ma_reporting` | Berichte, Factsheets, Abbildungen | nein | Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `ma_data_export` | CSV-, JSON-, Excel- und Archivpakete | nein | Modulinfo | nein | geplant | `src/ma_workflow/catalog.py` |
| `project_documentation` | Plaene, Entscheidungen, Leitfaden, Changelog | ja, Dokuprozess | ja, Modulinfo | nein | nutzbar | `docs/project/`, `docs/common/commands_common.md` |

## Statuslogik

- `ja`: funktionsfaehiger Pfad ist im Code vorhanden.
- `teilweise`: Grundlogik oder Bestandskern ist vorhanden, aber nicht als
  geschlossener aktueller Workflow fertig.
- `nein`: noch kein belastbarer Backend- oder Frontendpfad vorhanden.
- `Modulinfo`: Streamlit zeigt den Bereich ueber den zentralen Katalog, aber
  noch keine eigene Fachbedienung.
