# UI-Migrationsplan

Stand: 2026-06-08

## Zweck

Dieser Plan beschreibt die spaetere Trennung von Fachlogik und Oberflaeche.
In diesem Dokumentationsschritt wird keine Fachlogik umgesetzt, kein Paket
angelegt und keine bestehende Tkinter-Datei verschoben.

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
  Streamlit-Oberflaeche, Navigation, Seiten, Komponenten, Projektzustand

ma_ui_legacy
  optionale Uebergangsablage fuer bestehende Tkinter-Oberflaeche

ma_analyse
  fachlicher Kern der Simulationsergebnisanalyse
```

Die UI ruft Services auf. Die Fachmodule liefern neutrale Ergebnisobjekte
zurueck.

## Geplante Schnittstelle fuer ma_analyse

Noch nicht implementieren:

```python
from ma_analyse.models import AnalysisConfig, AnalysisResult

def run_analysis(config: AnalysisConfig) -> AnalysisResult:
    ...
```

Geplante Modelle:

- `AnalysisConfig`: Eingabeordner, Ausgabeordner, Varianten, Raeume,
  Report-Optionen.
- `AnalysisResult`: Zusammenfassungstabellen, Detailtabellen, Diagramme,
  Reportpfade und Warnungen.

## Phase 1 Bestandsanalyse

Ziel: Bestehenden Code analysieren, ohne ihn direkt umzubauen.

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

## Phase 2 Schnittstellenentwurf

Ziel: Eine stabile Schnittstelle zwischen UI und Analysemodul planen.

Aufgaben:

- `AnalysisConfig` entwerfen.
- `AnalysisResult` entwerfen.
- zentrale Funktion `run_analysis(config)` definieren.
- benoetigte Eingaben dokumentieren.
- erwartete Rueckgaben dokumentieren.
- offene Fragen zur bestehenden Analyse erfassen.

Ergebnis: Ein freigegebener Vorschlag fuer die Service-Struktur von
`ma_analyse`.

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

## Phase 5 Aufbau der Streamlit-Grundstruktur

Ziel: Neue zentrale UI-Struktur anlegen.

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

Ergebnis: Die Streamlit-App kann lokal gestartet werden.

## Phase 6 Anbindung von ma_analyse an Streamlit

Ziel: Simulationsergebnisanalyse ueber Streamlit bedienbar machen.

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

## Phase 7 Einbindung weiterer Module

Ziel: Streamlit als zentrale Oberflaeche fuer den Gesamtworkflow erweitern.

Aufgaben:

- `ma_weather` anbinden.
- `ma_variants` anbinden.
- `ma_parameters` anbinden.
- `ma_simulation_setup` anbinden.
- spaeter `ma_import_ida`, `ma_export_ida` und `ma_assessment` anbinden.

Ergebnis: Die UI bildet den Workflow der Masterarbeit ab.

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
