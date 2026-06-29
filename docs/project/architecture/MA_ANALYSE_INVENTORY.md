# ma_analyse Bestandsanalyse

Stand: 2026-06-10

Aktueller Nachtrag 2026-06-28: Die Tkinter-Analyse wurde hart aus
`ma_analyse` herausgeloest. Der aktive Zielort ist
`ma_ui.tkinter_app.module_views.analyse`; `ma_analyse.gui` und der CLI-Befehl
`python -m ma_analyse gui` existieren nicht mehr. Aeltere Hinweise auf
`ma_ui_legacy` sind historisch. Der Tkinter-Runner baut seinen Analyseauftrag
inzwischen ueber `pipeline_config.py` als `AnalysisConfig` und startet ueber
`ma_workflow.run_analysis_action`; die eigentliche Config-Erzeugung wird an
`ma_analyse.analysis_ui.build_analysis_config` delegiert.

## Zweck

Dieses Dokument ist Phase 1 von P005. Es beschreibt den aktuellen Bestand von
`ma_analyse`, ohne Code zu verschieben oder Fachlogik zu aendern.

## Kurzbefund

- `ma_analyse` enthaelt keine Streamlit-Abhaengigkeit.
- `ma_analyse` enthaelt keine Tkinter-Abhaengigkeit mehr.
- Die Tkinter-Analyse liegt unter `src/ma_ui/tkinter_app/module_views/analyse/`
  und ist dort intern in Fassade, Mixins, Parser, Restart-, Auswahl- und
  Runner-Helfer zerlegt.
- Die fachliche Analyse liegt bereits ueberwiegend unter `src/ma_analyse/analysis/`
  und `src/ma_analyse/preprocessing/`.
- `src/ma_analyse/app/commands.py` ist der aktuelle zentrale Orchestrator, ist
  aber noch CLI-nah: `argparse.Namespace`, `print()` und `SystemExit` sind fuer
  eine UI-neutrale Service-Schicht nicht ideal.

## Bestand nach Bereichen

| Bereich | Rolle | Bewertung |
|---|---|---|
| `app/cli.py` | CLI-Parser, Defaults, Argumentnormalisierung | bleibt CLI-Schicht, nicht UI-neutral |
| `app/commands.py` | zentrale Befehlsausfuehrung fuer prepare, comfort, analyze, heating, cooling, plot-template, all | gute Extraktionsquelle fuer Services, aber noch stark CLI-/Print-orientiert |
| `preprocessing/prepare.py` | PRN-Rohdaten nach Raum-CSV/XLSX aufbereiten | fachlicher Kern, bleibt in `ma_analyse` |
| `analysis/comfort/` | Comfort-Plots, PDFs, Zonenanalyse, Tabellen | fachlicher Kern, bleibt in `ma_analyse` |
| `analysis/heating.py` | Heizleistungsplots und Vergleiche | fachlicher Kern, spaeter weiter modularisieren |
| `analysis/cooling.py` | Kuehlleistungsplots und Vergleiche | fachlicher Kern, spaeter mit Heating-Runnern angleichen |
| `analysis/templates/` | Plot-Template-Katalog und Template-Renderer | fachlicher Kern, bleibt in `ma_analyse` |
| `analysis/tables/` und `analysis/excel.py` | Excel-Reports und Tabellen | fachlicher Exportkern, bleibt in `ma_analyse` |
| `analysis/components/` | gemeinsame Helper fuer Zeitfenster, Varianten, Raeume, Runtime und Layout | fachliche Shared-Komponenten innerhalb von `ma_analyse` |
| `core/` und `settings/` | Pfade, Logging, Formate, Naming, Plot-Template-Defaults | technische Basis von `ma_analyse` |

## Tkinter-Bestandteile

- Ort: `src/ma_ui/tkinter_app/module_views/analyse/`.
- Kanonischer Start: `python -m ma_ui.tkinter_app.module_views.analyse`.
- Fensterstart und Hauptloop: `run_gui()`, `run_gui_refresh()`, `run_gui_menu()`.
- Hauptklasse: `PipelineGUI`.
- `app.py` ist nur noch Fassade; Layout, Schrittfluss, Auswahl-State,
  Plot-Template-State und Pipeline-Runner liegen in internen Mixins.
- Analyseauftrag: `pipeline_config.py` normalisiert Tkinter-Zustand und
  delegiert die `AnalysisConfig`-Erzeugung an
  `ma_analyse.analysis_ui.build_analysis_config`; `pipeline_runner.py` startet
  ueber `ma_workflow.run_analysis_action`.
- Status und Fehler: `messagebox.showinfo`, `showwarning`, `showerror`.
- Laufsteuerung: Hintergrundthread, Queue, Logfenster und Statusanzeige.
- Neustart/Refresh: `subprocess.Popen`, Singleton-Controller und Refresh-Port.

Bewertung: Dieser Bereich ist funktionsfaehiger Altbestand und bleibt vorerst
unter `ma_ui`. Die technische Zerlegung und der Service-Adapter fuer den
Pipeline-Start sind umgesetzt; offen bleiben Vorschau-Cache, feinere
Ergebnisanzeige und weitere Reduktion von UI-Mapping-Dopplung.

## Bedienlogik aus der bestehenden GUI

Die Tkinter-GUI enthaelt die aktuell beste Beschreibung des realen
Analyse-Workflows. Fuer P005 wird diese Logik fachlich ausgewertet, aber nicht
technisch uebernommen.

Erkannte Bedienentscheidungen:

| Bereich | Aktueller Ort | Fachliche Bedeutung |
|---|---|---|
| Analyseumfang | `PipelineGUI` | bestimmt, ob eine, mehrere oder alle Varianten verarbeitet werden |
| Befehl | `PipelineGUI` | waehlt Prepare, Comfort, Analyse, Heating, Cooling, Plot-Template oder All |
| Prepare-Format | `layout_steps.py`, `selection_state.py` | bestimmt CSV, Excel oder beide Exportformate |
| Comfort-Typ | `selection_state.py` | bestimmt Plot, Uebersicht, Analyse oder kombinierte Comfort-Auswertung |
| Lasttyp | `selection_state.py` | Heating oder Cooling |
| Zeitansicht | `selection_state.py` | Bar, Year, Month, Week oder Day |
| Template-Auswahl | `plot_template_state.py` | waehlt vorbereitete Plot-Templates und deren Optionen |
| Varianten | `selection.py`, `selection_state.py` | bestimmt die zu verarbeitenden Varianten |
| Raeume | `selection.py`, `selection_state.py` | bestimmt die zu verarbeitenden Raeume |
| Start/Validierung | `pipeline_runner.py`, `pipeline_config.py` | prueft Pflichtauswahlen, baut `AnalysisConfig` und startet ueber `ma_workflow` |
| Status/Log | `worker.py`, `pipeline_runner.py` | zeigt laufende Verarbeitung und Protokollausgaben |

Ableitung fuer Streamlit:

- Die spaetere Analyseansicht muss denselben fachlichen Ablauf abdecken.
- Die technische Umsetzung erfolgt ueber `ma_ui.streamlit_app.module_views.analyse_view`,
  `ma_workflow` und `ma_analyse.services`.
- Messageboxen werden durch Status-, Warn- und Fehlerbereiche ersetzt.
- Tkinter-Threads und Queues werden nicht direkt uebernommen.
- Fachliche Defaults kommen weiterhin aus `ma_analyse.core.config` und
  `ma_analyse.settings`.

## Fachliche Analysebestandteile

Diese Bestandteile sollen in `ma_analyse` bleiben:

- PRN-Import und Datenaufbereitung.
- Comfort-, Heating-, Cooling-, Energy- und Template-Auswertungen.
- Plot-Erzeugung.
- Excel- und Tabellenexporte.
- Raum-, Varianten-, Zeitfenster- und Runtime-Helfer.
- Pfad- und Formatkonfiguration.

Diese Bestandteile sollen langfristig aus dem fachlichen Kern heraus:

- Tkinter-Fenster und Widgets.
- Tkinter-Dialoge und Messageboxen.
- direkte GUI-Statusmeldungen.
- Threading- und Queue-Mechanik der Tkinter-Oberflaeche.
- Restart-/Singleton-Logik der Tkinter-GUI.

## Aktuelle Kopplungsrisiken

- Die GUI baut aus Widget-State einen schmalen `AnalysisConfig`-Adapter. Das
  reduziert die Kopplung an `app.commands`; verbleibende Dopplung liegt vor
  allem noch in Options- und Preview-State.
- Die zentrale Befehlsausfuehrung nutzt `argparse.Namespace`, `print()` und
  teilweise `SystemExit`.
- Rueckgaben sind uneinheitlich: einige Funktionen geben Tabellen zurueck,
  andere schreiben nur Dateien und protokollieren ueber stdout.
- Fehler werden je nach Schicht als `None`, `SystemExit`, Exception, `print()`
  oder Messagebox behandelt.
- Heating und Cooling haben aehnliche Strukturen, sind aber noch nicht voll
  ueber gemeinsame Runner vereinheitlicht.

## Konsequenz fuer P005

Der sichere Weg bleibt: Die Tkinter-Datei wurde nach der harten Migration
zunaechst technisch zerlegt und startet Analyseauftraege jetzt ueber die
UI-neutrale Service-Fassade. Der naechste Schritt ist die weitere fachliche
Erweiterung dieser Fassade, der Vorschau-Logik und der Analyse-Seite. Die
minimale `ma_ui`-/`ma_workflow`-Shell ist bereits umgesetzt.

## Abdeckung in der Streamlit-Analyse-View

Bereits abgebildet:

- Befehlsauswahl fuer `prepare`, `comfort`, `analyze_data`,
  `heating`, `cooling`, `plot-template` und `all`.
- Analyseumfang mit `Eine Variante`, `Mehrere Varianten` und `Alle Varianten`.
- Prepare-Exportformat.
- Comfort-Ausgabeprofil.
- `analyze-data`-Excel-Ausgabe `separate` oder `combined`.
- Heating-/Cooling-Zeitansicht, Variantenmodus und Reihenlayout.
- Plot-Template-Auswahl, Zeitfilter, Sollwertband, Temperaturachsen und
  Aussenluft-Spalte.
- Pfade, Varianten, Raeume, Run-ID und Debug-Flag; technische Pfade werden in
  Streamlit unter `Erweiterte Pfade` gebuendelt.
- automatische Variantenlisten fuer Prepare- und Datenbankaufrufe ueber
  `ma_analyse.services`.
- automatische Raumliste aus der `ma_analyse`-Konfiguration.
- freie Overlay-Linien als einfache Texteingabe `source,column,label,axis`.
- einfache Overlay-Katalogauswahl fuer CSV-/AUX-Spalten der ersten gewaehlten
  Variante und des ersten Raums.

Noch nicht abgebildet:

- vollstaendige Overlay-Verwaltung wie in der Tkinter-GUI mit mehreren
  Katalogzeilen, Bearbeiten und Entfernen.
- Tkinter-spezifische Logfenster-, Threading- und Refresh-Funktionen. Diese
  sollen nicht in Streamlit kopiert werden.

## Offene Inventarfragen

- Welche Tkinter-Optionen brauchen noch eine bessere gemeinsame Mapping-Schicht
  mit der Streamlit-Analyse?
- Welche bestehenden Analysefunktionen liefern bereits verwertbare
  Ergebnisobjekte statt nur Dateien und stdout?
- Welche GUI-Validierungen gehoeren fachlich in `ma_analyse.services` und
  welche bleiben reine UI-Hinweise?
- Welche Auswahlhelfer aus `ma_ui.tkinter_app.module_views.analyse.selection`
  sollen spaeter fachlich nach `ma_analyse` oder technisch innerhalb von
  `ma_ui` weiter aufgeteilt werden?
