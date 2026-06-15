# Zielarchitektur

Stand: 2026-06-10

## Zweck

Dieses Dokument ordnet den geplanten Gesamtworkflow und die Zielmodule ein. Es
setzt keine Fachlogik um und ersetzt keine bestehenden Module.

## Praezisierung P005

Die P005-Zielarchitektur wurde am 2026-06-10 verschaerft. Die bestehende
Tkinter-Oberflaeche aus `ma_analyse` wird nicht technisch nach Streamlit
uebersetzt. Sie dient nur als fachliche Ablaufvorlage fuer die spaetere
Streamlit-Oberflaeche.

Wichtig:

- Keine bestehende GUI-Datei wird ohne eigenen Refactoring-Slice verschoben.
- Keine bestehenden Analysefunktionen werden im Architektur-Slice umgebaut.
- `ma_ui` ist die zentrale Zieloberflaeche.
- `ma_workflow` ist die Vermittlung zwischen UI-Aktionen und Fachmodulen.
- Fachmodule bleiben UI-neutral.
- IDA ICE bleibt der externe Simulationsschritt zwischen Export und Import.

## Aktueller Bestand

| Bereich | Stand | Bewertung |
|---|---|---|
| `ma_analyse` | vorhanden | Bestehende Analysepipeline fuer IDA-ICE-Simulationsergebnisse mit CLI, Tkinter-GUI, Preprocessing, Analyse und Plot-Templates. |
| `ma_variants` | vorhanden | Variantenkern mit Parametern, Optionen, Varianten, IDA-Uebergabestruktur, Simulationsergebnisadapter, Wirtschaftlichkeit, Produkt-/Materialkatalogen und Streamlit-UI. |
| `ma_weather` | teilweise vorhanden | Wetterkatalog, TRY-Importer, Validierung, Kennwerte, Diagramme, Markdown-Bericht und Runner sind als lokale Pipeline vorhanden. |
| `ma_ui` | teilweise vorhanden | Minimale Streamlit-Shell mit Startseite, Analyse-Seite, Varianten-Uebersicht, Wetter-Uebersicht, Bewertungs-Uebersicht, Navigation und Projektzustand. |
| `ma_ui_legacy` | nicht vorhanden | Zielbereich fuer die bestehende Tkinter-Arbeit, falls sie spaeter aus `ma_analyse` ausgelagert wird. |
| `ma_workflow` | teilweise vorhanden | Neutraler Workflow-Katalog und Analyse-Adapter zwischen UI und Fachmodulen. |
| `ma_shared` | nicht vorhanden | Zielbereich fuer wirklich gemeinsame Pfade, Konstanten, Exceptions und Ergebnisobjekte. |

## Zielmodule

| Modul | Zweck | Bestand | Empfohlene Aktion | Risiko |
|---|---|---|---|---|
| `ma_ui` | Gemeinsame lokale Streamlit-Oberflaeche mit Workflow-Dashboard | teilweise | Shell schrittweise ausbauen, keine Fachlogik in UI verschieben | mittel |
| `ma_ui_legacy` | Uebergangsbereich fuer bestehende Tkinter-Oberflaechen | nein | Erst nach Bestandsanalyse und Freigabe auslagern | hoch |
| `ma_workflow` | Orchestrierung zwischen Oberflaeche und Fachmodulen | teilweise | Prozessaktionen schrittweise mit Fachservices verbinden | mittel |
| `ma_parameters` | Parameter- und Optionskatalog als eigenes Zielmodul | nein, Logik liegt in `ma_variants` | Vorerst nicht verschieben; spaeter Extraktion planen | hoch |
| `ma_weather` | Wetterdaten, TRY-Import, Wetterkennwerte, Wetteranalyse | teilweise | Reale TRY-Datei lokal pruefen und Diagrammgestaltung fachlich abstimmen | mittel |
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

## Rollen im Pre- und Post-Process

### Pre-Process

| Reihenfolge | Zielmodul | Aufgabe |
|---|---|---|
| 1 | `ma_parameters` | Technische Parameter, Optionsgruppen und spaetere Eingabekataloge verwalten. |
| 2 | `ma_weather` | Wetterdaten und TRY-Randbedingungen vorbereiten. |
| 3 | `ma_building` | Gebaeude-, Zonen- und Modellrandbedingungen vorbereiten. |
| 4 | `ma_variants` | Variantenentscheidungen, Auswahl und Benennung erzeugen. |
| 5 | `ma_simulation_setup` | Festlegen, wie Varianten simuliert werden: Zeitraum, Zeitschritt, Szenario, Run-Metadaten. |
| 6 | `ma_export_ida` | Uebergabestruktur fuer IDA ICE vorbereiten. |

`ma_simulation_setup` liegt bewusst zwischen `ma_variants` und `ma_export_ida`.
Die Varianten definieren, was simuliert wird. Das Simulation-Setup definiert,
wie simuliert wird. Erst danach wird die IDA-Uebergabe vorbereitet.

### Simulation

IDA ICE bleibt ausserhalb der Python-Fachmodule. Python bereitet Export und
Import vor, startet aber in diesem Architekturplan keine vollautomatische
Simulation.

### Post-Process

| Reihenfolge | Zielmodul | Aufgabe |
|---|---|---|
| 1 | `ma_import_ida` | IDA-ICE-Ergebnisordner erkennen, pruefen und standardisieren. |
| 2 | `ma_analyse` | Simulationsergebnisse auswerten, Kennwerte, Diagramme und Reports erzeugen. |
| 3 | `ma_assessment` | Bewertung ueber Wirtschaftlichkeit und spaeter Nachhaltigkeit. |
| 4 | `ma_feedback` | Auffaelligkeiten und Rueckspruenge in Pre-Process-Module dokumentieren. |

## ma_assessment Zielzuschnitt

`ma_assessment` wird nicht als reine Wirtschaftlichkeitsdatei verstanden,
sondern als Bewertungsoberstruktur.

```text
ma_assessment/
  common/
  economics/
  sustainability/
  adapters/
```

Geplante Ausbaustufen:

1. Generische Wirtschaftlichkeitsbewertung.
2. Betriebsbezogene Nachhaltigkeit auf Basis von Simulationsergebnissen.
3. Detailbewertung mit Produktdaten.
4. Material- und Bauteilbezug, falls fachlich noetig.

## Geplante Zielstruktur

Diese Struktur ist das vollstaendige Zielbild. Ein minimaler erster Slice von
`ma_ui` und `ma_workflow` ist umgesetzt; die restliche Struktur wird nur nach
separater Freigabe ausgebaut.

```text
src/
  ma_ui/
    app.py
    main_dashboard.py
    workflow_view.py
    pre_process_view.py
    post_process_view.py
    shared/
      layout.py
      widgets.py
      status_panel.py
      log_panel.py
      file_selectors.py
      tables.py
      plot_viewer.py
    module_views/
      parameters_view.py
      weather_view.py
      building_view.py
      variants_view.py
      simulation_setup_view.py
      export_ida_view.py
      import_ida_view.py
      analyse_view.py
      assessment_view.py
      feedback_view.py
    state/
      project_state.py

  ma_workflow/
    workflow_manager.py
    dashboard_actions.py
    pre_process_runner.py
    post_process_runner.py
    feedback_router.py

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
    common/
    economics/
    sustainability/
    adapters/

  ma_shared/
    paths.py
    constants.py
    exceptions.py
    result_types.py
```

Aktueller Zwischenstand: `src/ma_ui/module_views/`, `src/ma_ui/shared/`,
`src/ma_workflow/dashboard_actions.py`, `src/ma_workflow/pre_process_runner.py`,
`src/ma_workflow/post_process_runner.py` und `src/ma_workflow/feedback_router.py`
sind als kompatibler Struktur-Slice vorbereitet. Die bestehenden `pages/` und
`actions.py` bleiben als Kompatibilitaets- und Zwischenstand erhalten.

## Service-Schnittstelle fuer ma_analyse

Der erste Code-Slice ist umgesetzt: `ma_analyse.models` enthaelt
`AnalysisConfig` und `AnalysisResult`, `ma_analyse.services` enthaelt
`run_analysis(config)` als UI-neutrale Fassade ueber bestehender Logik.

```python
from ma_analyse.models import AnalysisConfig, AnalysisResult

def run_analysis(config: AnalysisConfig) -> AnalysisResult:
    ...
```

Neutrale Modelle:

- `AnalysisConfig`: Eingabeordner, Ausgabeordner, Varianten, Raeume und Report-Optionen.
- `AnalysisResult`: Tabellen, Diagramme, Reportpfade und Warnungen.

Wichtig: Im bestehenden Code existieren weiterhin Analyse-Runner und CLI-nahe
Funktionen. Die neue Fassade ersetzt diese nicht, sondern ruft sie kontrolliert
auf. Eine feinere fachliche Rueckgabe mit Tabellen, Diagrammen und Reportpfaden
bleibt ein spaeterer Ausbauschritt.

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

Diese Tabelle ist der verbindliche Zielvertrag zwischen `ma_ui` und
`ma_workflow`. UI-Buttons duerfen spaeter keine Fachmodule direkt verdrahten,
sondern rufen Workflow-Aktionen auf. `ma_workflow` entscheidet dann, welcher
Fachservice angesprochen wird.

## Umsetzungshinweise

- Die Zielmodule werden nicht automatisch als Python-Pakete angelegt.
- Bestehende Logik wird erst nach separater Freigabe verschoben.
- Die `ma_analyse`-Bestandsanalyse und der Schnittstellenentwurf liegen in `MA_ANALYSE_INVENTORY.md` und `MA_ANALYSE_SERVICE_INTERFACE.md`.
- Der erste Code-Slice fuer `ma_analyse.models` und `ma_analyse.services` ist als Fassade ueber bestehender Logik umgesetzt.
- Der erste Code-Slice fuer `ma_workflow` und `ma_ui` ist als minimale Shell umgesetzt.
- Der zweite P005-Struktur-Slice bereitet `ma_ui/shared`, `ma_ui/module_views`
  und die geplanten `ma_workflow`-Aktions-/Runner-Dateien kompatibel vor.
- Die Varianten-Uebersicht nutzt bestehende `ma_variants`-Services und dupliziert keine Variantenlogik.
- Die Wetter-Uebersicht nutzt den bestehenden `ma_weather`-Katalog und importiert keine TRY-Dateien.
- Die Bewertungs-Uebersicht nutzt bestehende Wirtschaftlichkeitsannahmen und berechnet keine Variantenkosten in der UI.
- Der naechste P005-Schritt ist die fachliche Erweiterung der Analyse-Seite oder
  die schrittweise Befuellung der vorbereiteten Platzhalter-Views.
- Bestehende `ma_analyse`-Fachfunktionen bleiben in `ma_analyse`.
