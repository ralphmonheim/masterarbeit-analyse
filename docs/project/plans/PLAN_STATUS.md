# Plan Status

Stand: 2026-06-12

Diese Datei ist die aktive Planungsuebersicht. Sie wird nach Modulen gefuehrt und nach jeder Planumsetzung aktualisiert. Vollstaendige alte Planstaende liegen unter `docs/project/plans/archived/`.

## Projektorganisation

### Abgeschlossen

- P003 Projektstruktur, Planungsbereich und Nutzerentscheidungen: modulare Dokumentationsstruktur, Planindex, Strukturreview, Cleanup-Plan, Implementierungshinweise und getrennter Bereich fuer Nutzerentscheidungen wurden vorbereitet. Betroffen: `docs/project/`, `docs/ma_analyse/`, `docs/ma_variants/`, `docs/ma_weather/`, `docs/common/`.
- `docs/project/plans/archived/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md` ist nach Umsetzung archiviert.
- `docs/project/plans/archived/250603_Plan_Variantenmodul_GUI_Logikpruefung.md` ist nach Abschluss von P001 archiviert.
- `docs/project/plans/archived/PLAN_Projektplan_Version_1_0_0.md` ist ein abgelegter Plan und nicht mehr die aktive Steuerdatei.
- `data/test_output/` bleibt ein lokaler, semi-wichtiger Arbeits- und Smoke-Test-Ordner. Der Nutzer leert ihn regelmaessig manuell.
- `docs/examples/plot_templates/` bleibt die belastbare Referenzgalerie fuer aktuelle `ma_analyse`-Plot-Template-Beispiele.
- Der leere, nicht versionierte Ordner `scripts/` wurde entfernt.
- `docs/project/UPDATE_ROUTINES.md` dokumentiert die festen Codex-Routinen `update repo`, `direkt update repo` und `update planung`.
- `docs/project/UPDATE_ROUTINES.md` dokumentiert zusaetzlich `tagesstart`, `tagesende`, `tagesende direkt`, `wochenabschluss`, `projektlage`, `plan aufnehmen`, `entscheidung festhalten` und `release check`.
- `docs/project/weekly_reviews/` ist als Ablage fuer Wochenzusammenfassungen vorbereitet.
- Der alte leere Root-Dokumentenordner wurde entfernt; Produkt- und Materialdatenblaetter liegen aktiv unter `data/catalogs/documents/`.
- Nutzerentscheidung dokumentiert: Website- und Portfolio-Chats werden von der Masterarbeits-Entscheidungsanalyse ausgeschlossen.
- Nutzerentscheidung dokumentiert: Echte Produkt-, Material- und Datenbankinhalte werden nicht ins Git-Repo uebernommen; versioniert werden Struktur und klar gekennzeichnete Beispieldaten.
- Nutzerentscheidung dokumentiert: Relative/absolute Cooling-Logik bleibt vorerst nur in Plot-Templates; Hauptportal und regulaerer `cooling`-Befehl werden erst nach Abschluss der Diagrammbearbeitung erneut geprueft.
- Nutzerentscheidungen aus P005 dokumentiert: `ma_parameters` ersetzt `ma_input`, `ma_ui` und `ma_workflow` werden getrennte Zielmodule, `ma_analyse`-Fachlogik bleibt in `ma_analyse`, IDA-Export/-Import, Simulation-Setup, Assessment und Feedback werden getrennt geplant.
- Nutzerentscheidungen aus P005 ergaenzt: Streamlit ist Zieltechnik fuer `ma_ui`; Tkinter bleibt Legacy-Bestand und wird nicht mit Streamlit vermischt; `ma_analyse` soll langfristig eine UI-neutrale Service-Schnittstelle erhalten.
- Nutzerentscheidungen aus P005 verschaerft: `ma_simulation_setup` liegt zwischen Varianten und IDA-Export; die Tkinter-GUI dient als fachliche Ablaufvorlage, nicht als technische Streamlit-Vorlage; `ma_ui` zielt auf Dashboard, Workflow-Views, Shared-Komponenten und Module-Views; `ma_assessment` buendelt Economics und Sustainability.
- P005 Phase 1/2 dokumentiert: `ma_analyse`-Bestandsanalyse und Service-Schnittstellenentwurf liegen unter `docs/project/architecture/`.

### Teilweise umgesetzt

- P005 Architektur-Slice umgesetzt: Zielarchitektur und UI-Auslagerungsreview liegen unter `docs/project/architecture/`.
- P005 ordnet den Workflow als Pre-Process, Simulation, Post-Process und Feedback ein.
- P005 bewertet bestehende Oberflaechen: `src/ma_analyse/gui/app.py` bleibt vorerst unveraendert; `src/ma_variants/ui/services.py` dient als positives Muster fuer Trennung von UI und Fachlogik.
- P005 Streamlit-/Tkinter-Anpassung dokumentiert: `docs/project/architecture/UI_MIGRATION_PLAN.md` beschreibt Bestandsanalyse, Schnittstellenentwurf, Bereinigung, Legacy-Auslagerung, Streamlit-Aufbau und spaetere Modulanbindung.
- P005 Bestandsanalyse dokumentiert: Tkinter sitzt nur in `src/ma_analyse/gui/app.py` und `dialogs.py`; `ma_analyse` hat keine Streamlit-Abhaengigkeit.
- P005 Schnittstellenentwurf dokumentiert: `AnalysisConfig`, `AnalysisResult` und `run_analysis(config)` bilden die UI-neutrale Service-Fassade.
- P005 erster Service-Code-Slice umgesetzt: `src/ma_analyse/models.py` und `src/ma_analyse/services.py` stellen `AnalysisConfig`, `AnalysisResult` und `run_analysis(config)` als UI-neutrale Fassade bereit.
- P005 Workflow-/UI-Shell umgesetzt: `src/ma_workflow/` enthaelt Workflow-Katalog und Analyse-Adapter; `src/ma_ui/` enthaelt eine Streamlit-Shell mit Startseite, Analyse-Seite, Navigation und Projektzustand.
- P005 Startseite erweitert: `ma_ui` zeigt Workflow-Statuskennzahlen,
  Phasenuebersicht, Workflow-Schritte und Dashboard-Aktionen aus
  `ma_workflow`.
- P005 Analyse-Seite erweitert: `ma_analyse` sammelt erzeugte Dateien in `AnalysisResult.created_files`; `ma_ui` zeigt Status, Fehler, Hinweise, erzeugte Dateien und Log strukturiert an.
- P005 Varianten-Uebersicht in `ma_ui` ergaenzt: Parameter, Optionen, Variantenraum, Auswahlmethoden und Exportdateien werden ueber bestehende `ma_variants`-Services angezeigt.
- P005 Wetter-Uebersicht in `ma_ui` ergaenzt: lokale TRY-Datensaetze werden aus dem `ma_weather`-Katalog angezeigt, ohne TRY-Dateien zu importieren.
- P005 Bewertungs-Uebersicht in `ma_ui` ergaenzt: generische Systemkosten, Energiepreise und Szenarien werden aus bestehenden Wirtschaftlichkeitsannahmen angezeigt, ohne Variantenkosten zu berechnen.
- P005 Planoptimierung nach verschaerfter Nutzer-Ausarbeitung umgesetzt: Zielstruktur fuer `ma_ui`, `ma_workflow`, `ma_assessment`, `ma_simulation_setup` und Tkinter-Legacy ist dokumentiert, ohne bestehende Dateien zu verschieben.
- P005 kompatibler Struktur-Slice umgesetzt: `ma_ui/shared/`, `ma_ui/module_views/`,
  `ma_ui/main_dashboard.py`, `ma_ui/workflow_view.py`, `ma_ui/pre_process_view.py`,
  `ma_ui/post_process_view.py` sowie die geplanten `ma_workflow`-Dateien fuer
  Dashboard-Aktionen, Pre-/Post-Process und Feedback sind vorbereitet.
- P005 Analyse-View fachlich erweitert: `ma_ui/module_views/analyse_view.py`
  bildet Prepare-, Comfort-, Heating-/Cooling- und Plot-Template-Optionen auf
  `AnalysisConfig` ab; `pages/analyse.py` bleibt Kompatibilitaetswrapper.
- P005 Analyse-View gegen Tkinter-Ablauf weiter abgeglichen: `analyze-data`
  ist als eigener Excel-Auswertungsschritt mit `separate`/`combined`
  abgebildet.
- P005 Analyseumfang in Streamlit ergaenzt: `Eine Variante`, `Mehrere Varianten`
  und `Alle Varianten` werden erfasst; `Alle Varianten` wird als automatische
  Variantenauswahl an die Service-Fassade uebergeben.
- P005 automatische Analyseauswahl ergaenzt: Variantenlisten fuer Prepare- und
  Datenbankaufrufe sowie Raumlisten werden ueber `ma_analyse.services`
  bereitgestellt; manuelle Texteingabe bleibt als Fallback.
- P005 freie Overlay-Linien in der Analyse-View ergaenzt: einfache Texteingabe
  im Format `source,column,label,axis` wird in Plot-Template-Optionen
  uebersetzt.
- P005 einfache Overlay-Katalogauswahl ergaenzt: `ma_analyse.services`
  stellt CSV-/AUX-Spalten fuer Plot-Template-Overlays bereit; die Analyse-View
  kann daraus eine Overlay-Zeile uebernehmen.
- P005 Streamlit-Importrobustheit ergaenzt: optionale Overlay-Katalogfunktion
  wird in der Analyse-View defensiv zur Laufzeit geladen; Startdokumentation
  empfiehlt den venv-basierten Modulaufruf.
- P005 Plot-Template-Auswahl in Streamlit an Tkinter-Logik angenaehert:
  Nach Auswahl des Befehls `plot-template` werden Zeitfelder aus dem Template
  abgeleitet, Einzelraum-/Mehrraumlogik wird beachtet, Template-Defaults werden
  geladen, feste/freie Overlays sind bedienbar und erzeugte Bilddateien werden
  direkt als Vorschau angezeigt.
- P005 Analyse-Wizard umgesetzt: Die Streamlit-Analyse-Seite startet mit der
  Befehlsauswahl, blendet Folgeschritte nach der vorhandenen Tkinter-
  Zustandslogik ein, fasst vorherige Schritte zusammen und fuehrt technische
  Pfade unter `Erweiterte Pfade`.
- P005 Hybrid-Bedienung vorbereitet: Die Streamlit-Analyse-Seite kann die
  bestehende Tkinter-Analyse als separates Legacy-Fenster starten, ohne Tkinter
  in Streamlit einzubetten.
- P005 grafisches Workflow-Dashboard umgesetzt: Die `ma_ui`-Startseite zeigt
  Phasen, Workflow-Karten, Statusfarben, Iterationspfade und Buttons zu
  vorhandenen Modulansichten; Detailtabellen bleiben im Expander erreichbar.
- P005 Platzhalter-Views erweitert: Parameter, Gebaeude, Simulation-Setup,
  IDA-Export, IDA-Import und Feedback zeigen ihren Workflow-Kontext aus
  `ma_workflow`, ohne eigene Fachlogik zu implementieren.
- P005 Platzhalter-Views weiter konkretisiert: Parameter, Gebaeude,
  Simulation-Setup, IDA-Export, IDA-Import und Feedback zeigen vorhandene
  Projektressourcen, relevante Pfade und Dateizaehlungen ueber eine
  UI-neutrale `ma_ui.resource_status`-Schicht.

### Offen

- P002 liegt mit vollstaendigem Planinhalt als Markdown-Datei in `docs/project/plans/inbox/`.
- P005 naechster Schritt: Analyse-View in laufender Streamlit-App manuell gegen
  reale `ida_imports`-/Datenbankordner pruefen.
- P005 offener Analyse-View-Punkt: Schrittweisen Analyse-Wizard in der laufenden
  Streamlit-App fachlich gegen den bisherigen Tkinter-Ablauf pruefen.
- P005 spaeterer Schritt: Tkinter-GUI erst nach separater Freigabe nach `ma_ui_legacy` auslagern.
- P005 spaeterer Schritt: `ma_workflow`-Aktionsdateien mit echten Fachservice-Aufrufen erweitern.
- P005 spaeterer Schritt: `ma_assessment` als separates Bewertungsmodul planen, bevor Wirtschaftlichkeitslogik aus `ma_variants` verschoben wird.
- Neue externe Plaene nach manueller Ablage in `docs/project/plans/inbox/` pruefen und in `PLAN_INDEX.md` sowie in diese Statusdatei uebernehmen.
- Nach groesseren Aenderungen pruefen, ob alte Planstaende nach `docs/project/plans/archived/` ausgelagert werden sollen.

## Modul ma_analyse

### Abgeschlossen

- Plot-Template-Katalog aktualisiert: `heating-year` ist overlayfrei, `heating-overlay` fuehrt die festen Heating-Overlays separat.
- Cooling-Plot-Templates getrennt: `cooling-year`, `cooling-month`, `cooling-week` und `cooling-day` verwenden Rohwerte aus `zone_energy_q_cool`; `cooling-absolute-year`, `cooling-absolute-month`, `cooling-absolute-week` und `cooling-absolute-day` zeigen Betraege positiv nach oben.
- Plot-Template-Referenzgalerie unter `docs/examples/plot_templates/` wurde mit 33 aktuellen Beispielen neu erzeugt.
- GUI-Mousewheel-Handler faengt nicht aufloesbare Tkinter-Combobox-Popups robust ab und verhindert `KeyError: 'popdown'`.
- IDA-Importordner umbenannt: `ma_analyse` nutzt fuer Rohdatenvarianten `data/ma_analyse/ida_imports`; der bisherige Eingangsordner wurde entfernt.

### Teilweise umgesetzt

- Plot-Template-Katalog: Referenzbilder liegen unter `docs/examples/plot_templates/`; die Dokumentation liegt unter `docs/ma_analyse/plot_template_examples.md`.
- Heating-Jahresplot nutzt eine gemeinsame Layoutbasis. Absolute Cooling-Jahresplots koennen diese Layoutbasis ebenfalls nutzen; relative Cooling-Templates bleiben als eigene signierte Darstellung erhalten.
- Interne Lasten und Energiebilanz sind als Plot-Template-Experimente vorhanden.

### Offen

- Overlay-Uebernahme in Hauptfunktionen klaeren. Betroffen: `src/ma_analyse/analysis/heating.py`, `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/gui/app.py`, `src/ma_analyse/app/cli.py`.
- Nach Abschluss der Diagrammbearbeitung pruefen, ob der normale `cooling`-Befehl und die GUI relative Rohwerte und absolute Betraege als eigene Modi erhalten sollen.
- GUI in kleinere Komponenten fuer Layout, Dialoge, Auswahl und Laufsteuerung aufteilen. Betroffen: `src/ma_analyse/gui/app.py`.
- Heating und Cooling weiter in Datenladen, Runner und Plotmodule zerlegen. Betroffen: `src/ma_analyse/analysis/heating.py`, `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/analysis/energy/`.

### Unklar

- Welche Overlays sollen in Hauptfunktionen sichtbar werden: feste Standard-Overlays, freie Nutzer-Overlays oder nur CLI/Config?
- Soll die relative/absolute Cooling-Logik nach Abschluss der Diagrammbearbeitung auch in den regulaeren `cooling`-Befehl und die GUI uebernommen werden?
- Soll aus den Internal-Loads-Templates ein eigener Befehl entstehen oder eine Integration in bestehende Auswertungen?
- Soll die Energiebilanz absolute Leistung `[W]` behalten oder spaeter auf `[W/m2]` umgerechnet werden?

## Modul ma_variants

### Abgeschlossen

- `ma_variants` ist als eigenes Paket unter `src/ma_variants/` vorhanden.
- Variantenbezogene Konfigurationen liegen unter `config/ma_variants/`.
- Variantenbezogene Import-, Export- und IDA-Uebergabeordner liegen unter `data/ma_variants/`.
- Produkt- und Materialdokumente liegen als eigener Katalogbereich unter `data/catalogs/documents/`.
- P001 Bestandspruefung: Import, Optionsimport, Variantenzahlung, Variantenerzeugung, Auswahl, Namensgebung und Export sind bereits als testbare Module vorhanden.
- P001 Variantenoberflaeche: `src/ma_variants/ui/app.py` bildet Parameter/Optionen, Variantenraum, Auswahl, Namensgebung, Export, Ergebnisse und Status getrennt ab.
- P001 UI-Services: `src/ma_variants/ui/services.py` kapselt manuelle Auswahl, reproduzierbare Zufallsauswahl, Filterauswahl und Namensgenerierung ausserhalb der Streamlit-Datei.
- P001 Variantenmodul GUI und Logikpruefung ist abgeschlossen: `tests -k ma_variants` wurde erfolgreich ausgefuehrt und die Streamlit-App wurde headless gestartet.
- P001 wurde nach `docs/project/plans/archived/250603_Plan_Variantenmodul_GUI_Logikpruefung.md` verschoben.

### Offen

- Falls weitere Modulordner unter `data/ma_variants/` gebraucht werden, zuerst im Planstatus dokumentieren.

## Modul ma_weather

### Teilweise umgesetzt

- P002 Struktur-Slice umgesetzt: `src/ma_weather/` ist als importierbares Paket vorbereitet.
- Wetterkatalog mit `WeatherDataset` und YAML-Import liegt unter `src/ma_weather/weather_catalog.py`.
- Beispielkatalog liegt unter `config/ma_weather/datasets/example_weather_datasets.yaml`.
- Reale TRY-Dateien werden lokal unter `data/ma_weather/input/` bereitgestellt und nicht versioniert.
- `data/ma_weather/database/` ist fuer spaeter aufbereitete Wetterdaten vorbereitet.
- `data/ma_weather/output/` ist fuer spaeter erzeugte Wetterdiagramme vorbereitet.
- Dokumentation liegt unter `docs/ma_weather/README.md`, `docs/ma_weather/workflow.md`, `docs/ma_weather/data_model.md` und `docs/ma_weather/commands_weather.md`.
- P002 Analyse-Slice umgesetzt: TRY-Importer, Wettervalidierung, Kennwerte,
  Diagramme, Markdown-Bericht und Runner sind als erste lokale Pipeline
  vorhanden.

### Offen

- Echte lokale TRY-Datei am Katalogpfad pruefen und 8760-Stunden-Integrationstest ausfuehren.
- Diagrammgestaltung fachlich pruefen und bei Bedarf an Masterarbeitslayout anpassen.
- P002 erst archivieren, wenn die reale TRY-Datei lokal erfolgreich verarbeitet wurde.

## Offene Nutzerentscheidungen

- Nach Abschluss der Diagrammbearbeitung klaeren, ob relative/absolute Cooling-Logik in den regulaeren `cooling`-Befehl und in die GUI uebernommen wird.

## Archiv

- `docs/project/plans/archived/2026-05-26.md`: alter Planstatus vor der modularen Struktur.
- `docs/project/plans/archived/250603_Plan_Variantenmodul_GUI_Logikpruefung.md`: abgeschlossener P001-Plan.
- `docs/project/plans/archived/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md`: umgesetzter Strukturplan P003.
- `docs/project/plans/archived/PLAN_Projektplan_Version_1_0_0.md`: abgelegter Projektplan Version 1.0.0.
