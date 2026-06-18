# UI-Migrationsplan

Stand: 2026-06-10

## Zweck

Dieser Plan beschreibt die Trennung von Fachlogik und Oberflaeche. Die ersten
kleinen Code-Slices fuer `ma_analyse.services`, `ma_workflow` und `ma_ui` sind
umgesetzt. Bestehende Tkinter-Dateien wurden nicht verschoben.

## Grundsatzentscheidung

- Streamlit ist die Zieltechnik fuer die neue zentrale Oberflaeche `ma_ui`.
- Tkinter und Streamlit werden nicht direkt miteinander kombiniert.
- Die bestehende Tkinter-Oberflaeche aus `ma_analyse` bleibt zunaechst an Ort
  und Stelle und wird als Legacy-Bestand behandelt.
- Eine spaetere Auslagerung nach `ma_ui_legacy` braucht einen eigenen
  Refactoring-Slice.
- Fachmodule duerfen keine direkte Abhaengigkeit zu Streamlit oder Tkinter
  erhalten.

## Zielbild

```text
ma_ui
  Streamlit-Oberflaeche, Dashboard, Workflow-Ansichten, geteilte UI-Bausteine,
  modulbezogene Views und Projektzustand

ma_workflow
  UI-Aktionen, Pre-Process-Runner, Post-Process-Runner und Feedback-Routing

ma_ui_legacy
  optionale Uebergangsablage fuer bestehende Tkinter-Oberflaeche

ma_analyse
  fachlicher Kern der Simulationsergebnisanalyse
```

Die UI ruft Services auf. Die Fachmodule liefern neutrale Ergebnisobjekte
zurueck.

Aktueller Zwischenstand: `ma_ui` nutzt weiterhin `pages/` als
Kompatibilitaetsschicht. Zusaetzlich sind `module_views/` und `shared/` als
Zielstruktur vorbereitet. `ma_workflow` nutzt weiterhin `actions.py` und
`analysis.py`, besitzt aber zusaetzlich die geplanten Dateien fuer
Dashboard-Aktionen, Pre-/Post-Process und Feedback. Die verschaerfte
Zielstruktur ist:

```text
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

ma_workflow/
  workflow_manager.py
  dashboard_actions.py
  pre_process_runner.py
  post_process_runner.py
  feedback_router.py
```

Die bestehende `pages/`-Shell wird nicht geloescht, weil sie als stabiler
Zwischenstand und Kompatibilitaetsschicht dient.

Die Analyse-View nutzt inzwischen eine sichtbare Schrittstruktur nach der
fachlichen Tkinter-Zustandslogik. Die aktiven Bereiche lauten `Befehl`,
`Unterbefehl`, `Export / Ausgabe`, `Template / Diagramm`, `Varianten`,
`Raeume` und ein fester Aktionsbereich. Einen allgemeinen Bereich `Optionen`
gibt es nicht mehr. `plot-template-analyse` ist der UI-Befehl fuer
Analyse-Templates und wird intern auf den bestehenden Backend-Befehl
`plot-template` abgebildet. Nach Auswahl von Diagrammgruppe, Ausgabemodus und
Zeitansicht leitet die Streamlit-Bedienung Einzelraum-/Mehrraumlogik,
Template-Defaults und Overlay-Optionen aus den bestehenden
`ma_analyse`-Template-Spezifikationen ab.

## Schnittstelle fuer ma_analyse

```python
from ma_analyse.models import AnalysisConfig, AnalysisResult

def run_analysis(config: AnalysisConfig) -> AnalysisResult:
    ...
```

Umgesetzte Modelle:

- `AnalysisConfig`: Eingabeordner, Ausgabeordner, Varianten, Raeume,
  Report-Optionen.
- `AnalysisResult`: Zusammenfassungstabellen, Detailtabellen, Diagramme,
  Reportpfade und Warnungen.

## Phase 1 Bestandsanalyse

Ziel: Bestehenden Code analysieren, ohne ihn direkt umzubauen.

Status: Dokumentiert in `MA_ANALYSE_INVENTORY.md`.

Aufgaben:

- Dateien unter `src/ma_analyse/` pruefen.
- Tkinter-Abhaengigkeiten identifizieren.
- fachliche Analysefunktionen identifizieren.
- Plotfunktionen identifizieren.
- Excel-Report-Funktionen identifizieren.
- Datei-Importfunktionen identifizieren.
- direkte UI-Ausgaben, Statusmeldungen und Fehlerdialoge erfassen.
- Risiken dokumentieren.

Ergebnis: Eine klare Liste, welche Bestandteile in `ma_analyse` bleiben und
welche spaeter in einen UI- oder Legacy-Bereich gehoeren.

Zusatz aus der P005-Verschaerfung:

- Die bestehende Tkinter-GUI wird als fachliche Ablaufvorlage analysiert.
- Sie wird nicht direkt in Streamlit uebersetzt.
- Der reale Ablauf wird aus dem Code abgeleitet, nicht aus Vermutungen.
- Unklare Punkte werden als offene Fragen dokumentiert.

## Phase 2 Schnittstellenentwurf

Ziel: Eine stabile Schnittstelle zwischen UI und Analysemodul planen.

Status: Dokumentiert in `MA_ANALYSE_SERVICE_INTERFACE.md`.

Aufgaben:

- `AnalysisConfig` entwerfen.
- `AnalysisResult` entwerfen.
- zentrale Funktion `run_analysis(config)` definieren.
- benoetigte Eingaben dokumentieren.
- erwartete Rueckgaben dokumentieren.
- offene Fragen zur bestehenden Analyse erfassen.

Ergebnis: Ein freigegebener Vorschlag fuer die Service-Struktur von
`ma_analyse`.

## Phase 2a Erster Service-Code-Slice

Ziel: Die geplante Schnittstelle minimal als Fassade verfuegbar machen.

Status: Umgesetzt mit `ma_analyse.models.AnalysisConfig`,
`ma_analyse.models.AnalysisResult` und `ma_analyse.services.run_analysis`.

Ergebnis: Die Fassade ist importierbar, faengt CLI-nahe Fehler ab und gibt ein
UI-neutrales Ergebnisobjekt zurueck. Bestehende Tkinter-Dateien bleiben
unveraendert.

## Phase 3 Bereinigung von ma_analyse

Ziel: Fachlogik und UI-Code trennen.

Aufgaben:

- Tkinter-Code aus fachlichen Funktionen entfernen.
- Analysefunktionen ohne GUI ausfuehrbar machen.
- Plot-Erstellung in fachlichen Plotmodulen buendeln.
- Excel-Erstellung in fachlichen Exportmodulen buendeln.
- neutrale Datenmodelle anlegen.
- zentrale Service-Funktion erstellen.

Ergebnis: `ma_analyse` kann ohne Tkinter und ohne Streamlit genutzt werden.

## Phase 4 Auslagerung der Tkinter-Oberflaeche

Ziel: Bestehende Tkinter-Arbeit sichern.

Aufgaben:

- Tkinter-Bestandteile nach Freigabe nach `ma_ui_legacy` verschieben.
- Importpfade gezielt anpassen.
- Tkinter-Oberflaeche an die neue Service-Funktion anbinden.
- Startfaehigkeit der alten Oberflaeche pruefen.
- `ma_ui_legacy` klar als Uebergangsloesung dokumentieren.

Ergebnis: Die alte Oberflaeche bleibt optional nutzbar, ist aber nicht mehr
Teil des fachlichen Analysekerns.

Nicht in dieser Phase erlaubt ohne Freigabe:

- `src/ma_analyse/gui/app.py` umbenennen.
- Tkinter-Code direkt in `ma_ui` kopieren.
- Streamlit-Widgets in `ma_analyse` einbauen.
- Fachliche Analysefunktionen im selben Schritt verschieben.

## Phase 5 Aufbau der Streamlit-Grundstruktur

Ziel: Neue zentrale UI-Struktur anlegen.

Status: Minimal umgesetzt mit `src/ma_ui/app.py`, Navigation, Projektzustand,
Startseite, Analyse-Seite, Zielordnern `module_views/` und `shared/` sowie
Platzhalter-Views fuer geplante Module.

Aufgaben:

- `ma_ui` anlegen.
- `app.py` und Navigation vorbereiten.
- Startseite und Platzhalterseiten anlegen.
- Projektzustand vorbereiten.
- Streamlit-Importe auf `ma_ui` begrenzen.

Startbefehl:

```powershell
streamlit run src/ma_ui/app.py
```

Ergebnis: Die Streamlit-App kann lokal gestartet werden. Weitere Seiten sind
als Platzhalter erreichbar, aber noch nicht fachlich angebunden.

Verschaerfter Zielzuschnitt:

- `main_dashboard.py` zeigt den aktuellen Projekt- und Modulstatus.
- `workflow_view.py` bildet den Gesamtworkflow ab.
- `pre_process_view.py` sammelt Parameter, Wetter, Gebaeude, Varianten,
  Simulation-Setup und IDA-Export.
- `post_process_view.py` sammelt IDA-Import, Analyse, Assessment und Feedback.
- `shared/` enthaelt nur allgemeine UI-Bausteine.
- `module_views/` enthaelt modulbezogene Bedienseiten.

Dieser Zielzuschnitt wird erst umgesetzt, wenn der vorhandene Zwischenstand
bewusst migriert wird.

## Phase 6 Anbindung von ma_analyse an Streamlit

Ziel: Simulationsergebnisanalyse ueber Streamlit bedienbar machen.

Status: Teilweise umgesetzt. Die Analyse-Seite erzeugt eine `AnalysisConfig`
und ruft `ma_workflow.run_analysis_action(config)` auf. Sie bildet erste
befehlsspezifische Optionen ab, ohne Fachlogik in die UI zu verschieben.

Aufgaben:

- `ma_ui/pages/analyse.py` aufbauen.
- Eingaben fuer Ergebnisordner, Varianten und Raeume ergaenzen.
- `AnalysisConfig` aus UI-Eingaben erzeugen.
- `ma_analyse.services.run_analysis(config)` aufrufen.
- Tabellen anzeigen.
- Diagramme anzeigen.
- Warnungen anzeigen.
- Reportpfad anzeigen oder Download vorbereiten.

Ergebnis: Die Analyse wird ueber Streamlit bedient, bleibt aber fachlich in
`ma_analyse`.

Aktueller Umsetzungsstand:

- Prepare-Exportformat wird abgefragt.
- Comfort nutzt `t_op / rel_hum` als Unterbefehl; das konkrete
  Comfort-Ausgabeprofil wird unter `Template / Diagramm` abgefragt.
- `analyze-data`/Excel-Auswertung mit `separate` oder `combined` wird
  abgefragt.
- Der Variantenumfang liegt im Bereich `Varianten`. Bei `Alle Varianten` wird
  `variants=None` an die Service-Fassade uebergeben.
- Der Raumumfang liegt im Bereich `Raeume` mit `Ein Raum`, `Mehrere Raeume`
  und `Alle Raeume`.
- Varianten und Raeume werden ueber `ma_analyse.services` fuer die UI
  bereitgestellt. Manuelle Texteingabe bleibt als Fallback erhalten.
- Heating-/Cooling-Unterbefehle `bar`/`timeline` werden abgefragt.
  `single`/`compare` und bei Bedarf `separate`/`combined` liegen unter
  `Export / Ausgabe`; Zeitansicht, Overlay und Diagrammanpassung liegen unter
  `Template / Diagramm`.
- Plot-Template, Zeitfilter, Sollwertband und Temperaturachsen werden
  abgefragt.
- Comfort hat keine separate Analyseebene mehr. Die vier bisherigen
  Comfort-Ausgaben bleiben als Diagrammauswahl unter `Template / Diagramm`
  erhalten; Varianten- und Raumumfang steuern die Auswahl.
- Der Aktionsbereich mit `Vorschau aktualisieren` und `Analyse starten` ist in
  Streamlit nicht einklappbar.
- Plot-Template-Overlays werden erst nach Varianten- und Raumauswahl
  angeboten, damit der Overlay-Katalog gezielt aus lokalen Daten gelesen wird.
- Freie Overlay-Linien koennen als einfache Textzeilen im Format
  `source,column,label,axis` uebergeben werden.
- Eine einfache Overlay-Katalogauswahl liest CSV-/AUX-Spalten ueber
  `ma_analyse.services.list_plot_overlay_sources` aus der ersten gewaehlten
  Variante und dem ersten Raum.
- Die alte `pages/analyse.py` bleibt Wrapper; die Ziel-View liegt unter
  `module_views/analyse_view.py`.
- UI-neutrale Auswahl-, Zeit-, Overlay- und Config-Helfer liegen in
  `ma_analyse.analysis_ui`; die Streamlit-View rendert diese Regeln nur noch.
- Die UI-neutrale Wizardlogik liegt in `ma_analyse.analysis_wizard` und wird
  von Tests gegen die neue Schrittstruktur geprueft.

Noch offen aus dem Tkinter-Abgleich:

- laufende Streamlit-App mit realen `ida_imports`-/Datenbankordnern manuell
  gegen den bisherigen Tkinter-Ablauf pruefen.
- Overlay-Bedienung fachlich testen: feste Overlays, freie Overlay-Linien,
  Entfernen und Experten-Textarea.
- Overlay-Strategie umsetzen: freie Datenreihen sollen aus lokalen Analyse-/
  Datenbankdaten in Diagramme geladen werden koennen; feste Additionen wie
  Temperaturband und Achsenbereiche bleiben kontrollierte Diagrammoptionen.
- Tkinter-Oberflaeche weiter reduzieren: Overlay und Diagrammbearbeitung
  langfristig in echte einklappbare Bereiche innerhalb `Template / Diagramm`
  ueberfuehren.
- Tkinter-Oberflaeche weiter an die neue Struktur angleichen: `single`/`compare`
  nach `Export / Ausgabe`, Comfort-Unterbefehl `t_op / rel_hum`, Comfort-
  Diagramme nach `Template / Diagramm` und Vorschau-Button zwischen
  `Zuruecksetzen` und `Start`.
- Tkinter-Vorschau so umsetzen, dass Vorschaubilder in einem temporaeren
  Vorschau-/Cachebereich entstehen und den regulaeren Output-Ordner nicht
  mit Testdiagrammen fuellen.

## Phase 7 Einbindung weiterer Module

Ziel: Streamlit als zentrale Oberflaeche fuer den Gesamtworkflow erweitern.

Aufgaben:

- `ma_weather` anbinden.
- Wetterdiagramme bleiben zunaechst im Modulbereich `ma_weather`; ein eigener
  UI-Befehl `plot-template-weather` bleibt ein offener spaeterer Strukturpunkt.
- `ma_variants` anbinden.
- `ma_parameters` anbinden.
- `ma_simulation_setup` anbinden.
- spaeter `ma_import_ida`, `ma_export_ida`, `ma_economy`,
  `ma_sustainability` und `ma_assessment` anbinden.

Ergebnis: Die UI bildet den Workflow der Masterarbeit ab.

Workflow-Aktionen als Zielvertrag:

| UI-Befehl | Workflow-Aktion | Ziel |
|---|---|---|
| Parameter oeffnen | `open_parameters` | Parameter- und Optionskatalog |
| Wetterdaten oeffnen | `open_weather` | Wetterdaten und TRY |
| Gebaeude oeffnen | `open_building` | Gebaeude-/Zonenbasis |
| Varianten oeffnen | `open_variants` | Variantenkatalog |
| Simulation konfigurieren | `open_simulation_setup` | Zeitraum, Zeitschritt, Szenario |
| IDA-Export starten | `run_ida_export` | Uebergabestruktur |
| IDA-Import starten | `run_ida_import` | Ergebnisordner standardisieren |
| Analyse starten | `run_analysis` | Simulationsergebnisanalyse |
| Bewertung starten | `run_assessment` | Gesamtbewertung, Scoring, Factsheets und Berichte |
| Feedback oeffnen | `open_feedback` | Rueckfuehrung und Problembehandlung |

## Phase 8 Dokumentation und Planstatus

Ziel: Aenderungen nachvollziehbar halten.

Aufgaben:

- Architekturplan aktualisieren.
- Planstatus aktualisieren.
- Changelog aktualisieren.
- technische Entscheidungen dokumentieren.
- Nutzerentscheidungen dokumentieren.
- offene Fragen dokumentieren.

Ergebnis: Die Struktur bleibt nachvollziehbar und kontrollierbar.

## Akzeptanzkriterien fuer die spaetere Umsetzung

- `ma_analyse` hat keine verpflichtende Tkinter-Abhaengigkeit mehr.
- `ma_analyse` hat keine Streamlit-Abhaengigkeit.
- Fachliche Analyse ist ohne GUI ausfuehrbar.
- Es gibt eine zentrale Service-Funktion fuer die Analyse.
- Es gibt neutrale Konfigurations- und Ergebnisobjekte.
- Bestehender Tkinter-Code wurde geprueft.
- Tkinter-Code wurde entweder ausgelagert oder als Altbestand dokumentiert.
- `ma_ui` existiert als eigenes Modul.
- Streamlit wird nur in `ma_ui` verwendet.
- Tabellen und Diagramme werden ueber die UI angezeigt, aber nicht dort berechnet.
- Fachlogik und UI sind klar getrennt.

## Risiken

- Bestehende Tkinter-Funktionen sind mit Analysefunktionen vermischt.
- Umzug des Codes kann bestehende Funktionalitaet beschaedigen.
- Streamlit wird zu frueh mit Fachlogik vermischt.
- `st.session_state` wird unuebersichtlich.
- Analysefunktionen haben zu viele Einzelparameter.
- Rueckgabeformate sind nicht klar definiert.
- Diagramme oder Excel-Reports werden direkt in der UI erzeugt.
- Mehrere Umbauschritte werden gleichzeitig durchgefuehrt.

## Gegenmassnahmen

- zuerst nur analysieren.
- fuer jede groessere Aenderung vorher einen Plan erstellen.
- bestehende Funktionen vor dem Verschieben dokumentieren.
- kleine Umbauschritte durchfuehren.
- nach jedem Schritt Startfaehigkeit pruefen.
- Fachlogik ueber Services kapseln.
- Datenmodelle fuer Eingaben und Ergebnisse verwenden.
- Streamlit-Importe auf `ma_ui` beschraenken.
- Tkinter-Code als Legacy sichern.
