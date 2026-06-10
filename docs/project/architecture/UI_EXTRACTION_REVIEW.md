# UI-Auslagerungsreview

Stand: 2026-06-10

## Ziel

Dieses Dokument bewertet die bestehenden Oberflaechen und bereitet eine spaetere
Auslagerung in eine gemeinsame `ma_ui`-Struktur vor. Es werden keine Dateien
verschoben und keine Imports geaendert.

Streamlit ist die Zieltechnik fuer die neue zentrale Oberflaeche. Die bestehende
Tkinter-Oberflaeche aus `ma_analyse` wird als Legacy-Bestand bewertet und darf
nicht direkt mit Streamlit vermischt werden.

## Bestand

| Datei | Rolle | Allgemein nutzbar | Empfohlener Zielort | Risiko | Kommentar |
|---|---|---|---|---|---|
| `src/ma_analyse/gui/app.py` | Tkinter-Hauptoberflaeche, Fenster, Ablaufsteuerung, Auswahl, Loganzeige und Analysebefehle | teilweise | spaeter optional nach `ma_ui_legacy/tkinter_analyse_app.py`; neue Analyseansicht separat unter `ma_ui/pages/analyse.py` | hoch | Datei ist sehr gross und mischt UI, Prozesssteuerung und Analyseoptionen. Nicht direkt verschieben. |
| `src/ma_analyse/gui/dialogs.py` | Tkinter-Dialoge fuer Ausgabeformate und Namensmapping | teilweise | spaeter `ma_ui_legacy` oder fachnahe Settings bei `ma_analyse` | mittel | Enthaltene Logik ist an Analyse-Settings und Tkinter-Dialoge gekoppelt. |
| `src/ma_analyse/gui/selection.py` | Auswahlhelfer fuer Varianten und Raeume | teilweise | fachliche Auswahl fuer Analyse bleibt in `ma_analyse`; reine UI-State-Helfer koennen spaeter extrahiert werden | mittel | Enthaltene Variantenlogik nutzt Analysepfade und Suffixe. |
| `src/ma_analyse/gui/singleton.py` | Steuerung fuer nur eine laufende Tkinter-Instanz | teilweise | spaeter `ma_ui_legacy` | mittel | Technisch Tkinter-/Socket-nah und fuer Streamlit nicht relevant. |
| `src/ma_analyse/gui/worker.py` | Queue-Writer fuer Worker-Logs | ja, klein | spaeter `ma_ui_legacy` oder neutraler Logging-Helfer | gering | Einfacher Helfer; Zielort haengt von der spaeteren Service-Struktur ab. |
| `src/ma_variants/ui/app.py` | Streamlit-Oberflaeche fuer Variantenkontrolle | teilweise | spaeter als Modulseite in `ma_ui/pages/variants.py` denkbar | mittel | Besser getrennt als `ma_analyse/gui/app.py`, aber Streamlit-spezifisch. |
| `src/ma_variants/ui/services.py` | UI-nahe Services ohne Streamlit-Abhaengigkeit | ja | Muster fuer weitere UI-Services | gering | Gute Trennung zwischen Oberflaeche und Fachlogik. |

## Konkrete Tkinter-Inventur

Der aktuelle Tkinter-Bestand liegt fachlich vor allem in
`src/ma_analyse/gui/app.py`.

Gefundene Einstiegspunkte:

- `run_gui()`
- `run_gui_refresh()`
- `run_gui_menu()`
- Klasse `PipelineGUI`

Gefundene UI-Bereiche:

- Analyseumfang: einzelne Variante, mehrere Varianten, alle Varianten.
- Befehlswahl: Prepare, Comfort, Analyse, Heating, Cooling, Plot-Template und
  Gesamtlauf.
- befehlsspezifische Optionen: Prepare-Exportformat, Comfort-Typ,
  Heating-/Cooling-Ansicht, Plot-Template, Overlays, Monats-/Wochen-/Tageswahl.
- Variantenlisten und Raumlisten.
- Statusbereich, Fortschritt, Logausgabe und Fehlerdialoge.
- Start-, Reset-, Settings- und Log-Bedienung.

Gefundene technische Kopplungen:

- Tkinter-State wird direkt in Analyseoptionen uebersetzt.
- Messageboxen werden fuer Validierung und Fehler genutzt.
- Worker-Thread und Queue sind Teil der Tkinter-Laufsteuerung.
- Die GUI ruft bestehende Pipeline-Einstiegspunkte aus der Analyse auf.

Bewertung: Diese Struktur ist fachlich wertvoll, aber technisch nicht geeignet
fuer eine direkte Uebernahme in Streamlit.

## Fachlicher Ablauf als Vorlage

Aus der bestehenden Tkinter-GUI laesst sich folgender fachlicher Ablauf fuer die
spaetere Streamlit-Ansicht ableiten:

1. Projekt- und Datenpfade erkennen.
2. Analyseumfang festlegen.
3. Analysebefehl waehlen.
4. befehlsspezifische Optionen festlegen.
5. Varianten auswaehlen.
6. Raeume auswaehlen.
7. Eingaben pruefen.
8. Analyseauftrag starten.
9. Status, Warnungen, Fehler und Logs anzeigen.
10. erzeugte Dateien und Ergebnisse anzeigen.

Dieser Ablauf soll in `ma_ui/module_views/analyse_view.py` nachgebaut werden,
aber ueber `ma_workflow` und `ma_analyse.services`, nicht ueber Tkinter-Code.

## Ziel-Mapping fuer spaetere Auslagerung

| Aktueller Bereich | Spaeterer Zielbereich | Regel |
|---|---|---|
| allgemeine Layout-Helfer | `ma_ui/shared/layout.py` oder `widgets.py` | nur neu schreiben oder gezielt extrahieren, kein Copy-Paste von Tkinter |
| Datei- und Ordnerauswahl | `ma_ui/shared/file_selectors.py` | Streamlit-spezifisch in UI, Pfadlogik in Fachservices |
| Status- und Loganzeige | `ma_ui/shared/status_panel.py`, `log_panel.py` | Anzeige in UI, Logdaten kommen aus Ergebnissen |
| Tabellenanzeige | `ma_ui/shared/tables.py` | Anzeige in UI, Datenberechnung im Fachmodul |
| Diagrammanzeige | `ma_ui/shared/plot_viewer.py` | Anzeige in UI, Plot-Erzeugung im Fachmodul |
| Analysebedienung | `ma_ui/module_views/analyse_view.py` | baut `AnalysisConfig` und ruft Workflow-Aktion |
| Tkinter-Hauptfenster | `ma_ui_legacy/tkinter_analyse_app.py` | nur nach separater Freigabe |
| Analysefunktionen | `ma_analyse` | bleiben fachlicher Kern |

## Bewertung

`ma_analyse` enthaelt aktuell die kritischste UI-Struktur. `app.py` ist gross
und sollte nicht direkt in `ma_ui` verschoben werden. Der sichere Weg ist:

1. Fachliche Analysebefehle in `ma_analyse` belassen.
2. Tkinter-Bestandteile als Legacy-Bestand dokumentieren.
3. Wiederverwendbare UI-Helfer in kleinen Schritten identifizieren.
4. Die minimale Streamlit-`ma_ui`-Shell nur als Adapter auf Fachservices ausbauen.
5. Analyseansicht schrittweise ueber die UI-neutrale `ma_analyse`-Service-Schnittstelle erweitern.

`ma_variants` zeigt bereits die bessere Richtung: Die Streamlit-Datei ist
vergleichsweise klein, und die fachnahen Operationen liegen in `ui/services.py`.

## Zielregeln

- `ma_ui` nutzt Streamlit.
- `ma_ui_legacy` kann spaeter die bestehende Tkinter-Oberflaeche aufnehmen.
- `ma_analyse` soll langfristig keine verpflichtende Tkinter-Abhaengigkeit haben.
- Streamlit- und Tkinter-Code werden nicht in derselben Oberflaeche kombiniert.
- Berechnungslogik, Plotlogik und Excel-Reportlogik bleiben in Fachmodulen.
- UI-Seiten bauen Konfigurationen, rufen Services auf und zeigen Ergebnisse an.

## Analyse-Schnittstelle

```python
from ma_analyse.models import AnalysisConfig, AnalysisResult

def run_analysis(config: AnalysisConfig) -> AnalysisResult:
    ...
```

`AnalysisConfig` und `AnalysisResult` sind als erste UI-neutrale Modelle
umgesetzt. `run_analysis(config)` liegt in `ma_analyse.services` und kapselt
die bestehende Pipeline kontrolliert fuer spaetere UI- und Workflow-Aufrufe.

Wichtig: Bestehende CLI-nahe Runner in `ma_analyse` werden dadurch nicht
automatisch ersetzt. Die Service-Fassade ist ein erster Adapter; eine feinere
Rueckgabe von Tabellen, Diagrammen und Reportpfaden bleibt ein spaeterer
Ausbauschritt.

## Nicht jetzt umsetzen

- `src/ma_analyse/gui/app.py` nicht verschieben.
- Bestehende Tkinter-GUI nicht auf Streamlit umbauen.
- Keine Tkinter-Bestandteile direkt in Streamlit-Seiten einbauen.
- Keine Importpfade in `ma_analyse` aendern.
- Keine Fachlogik in `ma_ui` duplizieren.
- Keine neuen Zielmodule ohne separaten Implementierungsplan anlegen.
- Bestehende `src/ma_ui/pages/`-Struktur nicht ungeprueft nach
  `module_views/` umbenennen.
- Bestehende `src/ma_workflow/actions.py` nicht ungeprueft in mehrere Runner
  aufteilen.
