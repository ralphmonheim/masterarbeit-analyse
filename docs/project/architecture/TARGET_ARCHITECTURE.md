# Zielarchitektur

Stand: 2026-06-08

## Zweck

Dieses Dokument ordnet den geplanten Gesamtworkflow und die Zielmodule ein. Es
setzt keine Fachlogik um und ersetzt keine bestehenden Module.

## Aktueller Bestand

| Bereich | Stand | Bewertung |
|---|---|---|
| `ma_analyse` | vorhanden | Bestehende Analysepipeline fuer IDA-ICE-Simulationsergebnisse mit CLI, Tkinter-GUI, Preprocessing, Analyse und Plot-Templates. |
| `ma_variants` | vorhanden | Variantenkern mit Parametern, Optionen, Varianten, IDA-Uebergabestruktur, Simulationsergebnisadapter, Wirtschaftlichkeit, Produkt-/Materialkatalogen und Streamlit-UI. |
| `ma_weather` | teilweise vorhanden | Struktur-Slice mit Wetterkatalog, Beispielkonfiguration und Tests; TRY-Importlogik folgt spaeter. |
| `ma_ui` | nicht vorhanden | Zielmodul fuer die spaetere gemeinsame Streamlit-Oberflaeche. |
| `ma_ui_legacy` | nicht vorhanden | Zielbereich fuer die bestehende Tkinter-Arbeit, falls sie spaeter aus `ma_analyse` ausgelagert wird. |
| `ma_workflow` | nicht vorhanden | Zielmodul fuer spaetere Prozesssteuerung zwischen UI und Fachmodulen. |
| `ma_shared` | nicht vorhanden | Zielbereich fuer wirklich gemeinsame Pfade, Konstanten, Exceptions und Ergebnisobjekte. |

## Zielmodule

| Modul | Zweck | Bestand | Empfohlene Aktion | Risiko |
|---|---|---|---|---|
| `ma_ui` | Gemeinsame lokale Streamlit-Oberflaeche mit Workflow-Dashboard | nein | Erst dokumentieren, spaeter minimalen App-Shell-Slice planen | mittel |
| `ma_ui_legacy` | Uebergangsbereich fuer bestehende Tkinter-Oberflaechen | nein | Erst nach Bestandsanalyse und Freigabe auslagern | hoch |
| `ma_workflow` | Orchestrierung zwischen Oberflaeche und Fachmodulen | nein | Erst Prozessaktionen definieren, dann schlanke Services anlegen | mittel |
| `ma_parameters` | Parameter- und Optionskatalog als eigenes Zielmodul | nein, Logik liegt in `ma_variants` | Vorerst nicht verschieben; spaeter Extraktion planen | hoch |
| `ma_weather` | Wetterdaten, TRY-Import, Wetterkennwerte, Wetteranalyse | teilweise | P002 weiter in Import, Validierung, Kennwerte, Diagramme gliedern | mittel |
| `ma_building` | Gebaeude- und Zonendaten fuer Varianten und Simulation | nein | Nur fachlich abgrenzen, spaeter minimal vorbereiten | mittel |
| `ma_variants` | Variantenbildung, Auswahl, Naming, Variantenuebersichten | ja | Stabil halten; Parameter-Extraktion spaeter pruefen | mittel |
| `ma_simulation_setup` | Simulationsrandbedingungen und Run-Metadaten | nein | Als separaten Slice zwischen Varianten und IDA-Export planen | gering bis mittel |
| `ma_export_ida` | Exportprozess vor der IDA-ICE-Simulation | teilweise in `ma_variants.ida_export` | Vorerst bestehende Logik nicht verschieben; spaeter Zielmodul pruefen | mittel |
| `ma_import_ida` | Import und Standardisierung nach der IDA-ICE-Simulation | teilweise ueber `ma_variants.simulation_results` und `ma_analyse` | Schnittstelle erst dokumentieren, dann Importadapter planen | hoch |
| `ma_analyse` | Analyse der IDA-ICE-Simulationsergebnisse | ja | Fachlogik dort belassen; GUI-Auslagerung separat pruefen | hoch |
| `ma_assessment` | Wirtschaftlichkeit und Nachhaltigkeit | teilweise in `ma_variants.economic_analysis` | Economics/Sustainability als spaetere Oberstruktur planen | mittel |
| `ma_feedback` | Problembehandlung und Rueckfuehrung in den Pre-Process | nein | Zunaechst nur dokumentieren; Implementierung erst nach stabilen Ergebnissen | mittel |
| `ma_shared` | Gemeinsame technische Grundlagen | nein | Nur anlegen, wenn echte Wiederverwendung entsteht | mittel |

## Architekturregeln fuer UI und Fachlogik

- Streamlit ist die Zieltechnik fuer die neue zentrale Oberflaeche `ma_ui`.
- Tkinter und Streamlit werden nicht direkt miteinander kombiniert.
- `streamlit` darf spaeter nur in `ma_ui` importiert werden.
- `tkinter` darf spaeter nur in `ma_ui_legacy` oder voruebergehend in `ma_analyse/gui` vorkommen.
- Fachmodule wie `ma_analyse`, `ma_variants` und `ma_weather` duerfen keine direkte Abhaengigkeit zu einer konkreten UI-Technik haben.
- Berechnungslogik, Plot-Erzeugung, Excel-Report-Erzeugung und Variantenlogik gehoeren nicht direkt in `ma_ui`.
- Die UI nimmt Eingaben entgegen, ruft Service-Funktionen auf und zeigt neutrale Ergebnisse an.

## Geplante Zielstruktur

Diese Struktur ist Zielbild und wird nicht in diesem Dokumentationsschritt angelegt.

```text
src/
  ma_ui/
    app.py
    navigation.py
    pages/
      home.py
      parameters.py
      variants.py
      simulation_setup.py
      export_ida.py
      import_ida.py
      analyse.py
      weather.py
      assessment.py
    state/
      project_state.py
    components/
      file_selector.py
      status_box.py
      plot_container.py
      table_view.py
      workflow_stepper.py
    adapters/
      streamlit_adapter.py

  ma_ui_legacy/
    tkinter_analyse_app.py

  ma_analyse/
    services.py
    models.py
    io.py
    calculations.py
    plots.py
    export.py

  ma_weather/
    services.py
    models.py
    plots.py

  ma_parameters/
    services.py
    models.py

  ma_variants/
    services.py
    models.py

  ma_simulation_setup/
    services.py
    models.py

  ma_export_ida/
    services.py
    models.py

  ma_import_ida/
    services.py
    models.py

  ma_assessment/
    services.py
    models.py

  ma_shared/
    paths.py
    constants.py
    exceptions.py
    result_types.py
```

## Geplante Service-Schnittstelle fuer ma_analyse

Die Schnittstelle ist Zielbild und wird in diesem Schritt nicht implementiert.

```python
from ma_analyse.models import AnalysisConfig, AnalysisResult

def run_analysis(config: AnalysisConfig) -> AnalysisResult:
    ...
```

Geplante neutrale Modelle:

- `AnalysisConfig`: Eingabeordner, Ausgabeordner, Varianten, Raeume und Report-Optionen.
- `AnalysisResult`: Tabellen, Diagramme, Reportpfade und Warnungen.

Wichtig: Im bestehenden Code existieren bereits Analyse-Runner und CLI-nahe
Funktionen. Die geplante `ma_analyse.services.run_analysis(config)`-Schnittstelle
ist eine spaetere, UI-neutrale Service-Fassade und ersetzt diese nicht in diesem
Dokumentationsschritt.

## Oberster Workflow

```text
Pre-Process
  ma_parameters
  ma_weather
  ma_building
  ma_variants
  ma_simulation_setup
  ma_export_ida

Simulation
  IDA ICE

Post-Process
  ma_import_ida
  ma_analyse
  ma_assessment

Problembehandlung und Rueckfuehrung
  ma_feedback
  Ruecksprung in ma_parameters, ma_weather, ma_building,
  ma_variants oder ma_simulation_setup
```

## Dashboard-Zuordnung

| Dashboard-Aktion | Workflow-Aktion | Zielmodul |
|---|---|---|
| Parameter oeffnen | `open_parameters` | `ma_parameters` |
| Wetterdaten oeffnen | `open_weather` | `ma_weather` |
| Gebaeudedaten oeffnen | `open_building` | `ma_building` |
| Varianten oeffnen | `open_variants` | `ma_variants` |
| Simulation konfigurieren | `open_simulation_setup` | `ma_simulation_setup` |
| IDA-Export starten | `run_ida_export` | `ma_export_ida` |
| IDA-Import starten | `run_ida_import` | `ma_import_ida` |
| Analyse starten | `run_analysis` | `ma_analyse` |
| Bewertung starten | `run_assessment` | `ma_assessment` |
| Problembehandlung oeffnen | `open_feedback` | `ma_feedback` |

## Umsetzungshinweise

- Die Zielmodule werden nicht automatisch als Python-Pakete angelegt.
- Bestehende Logik wird erst nach separater Freigabe verschoben.
- Der naechste P005-Schritt ist die `ma_analyse`-Bestandsanalyse und der Schnittstellenentwurf fuer `AnalysisConfig`, `AnalysisResult` und `run_analysis(config)`.
- Eine spaetere `ma_ui`-/`ma_workflow`-Shell wird erst nach separater Freigabe vorbereitet und darf keine Fachlogik duplizieren.
- Bestehende `ma_analyse`-Fachfunktionen bleiben in `ma_analyse`.
