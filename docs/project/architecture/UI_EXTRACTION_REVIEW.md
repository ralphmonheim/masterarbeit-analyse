# UI-Auslagerungsreview

Stand: 2026-06-08

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

## Bewertung

`ma_analyse` enthaelt aktuell die kritischste UI-Struktur. `app.py` ist gross
und sollte nicht direkt in `ma_ui` verschoben werden. Der sichere Weg ist:

1. Fachliche Analysebefehle in `ma_analyse` belassen.
2. Tkinter-Bestandteile als Legacy-Bestand dokumentieren.
3. Wiederverwendbare UI-Helfer in kleinen Schritten identifizieren.
4. Zuerst eine Streamlit-`ma_ui`-Shell planen, die Modulansichten nur aufruft.
5. Analyseansicht erst spaeter als Adapter auf eine UI-neutrale `ma_analyse`-Service-Schnittstelle anbinden.

`ma_variants` zeigt bereits die bessere Richtung: Die Streamlit-Datei ist
vergleichsweise klein, und die fachnahen Operationen liegen in `ui/services.py`.

## Zielregeln

- `ma_ui` nutzt Streamlit.
- `ma_ui_legacy` kann spaeter die bestehende Tkinter-Oberflaeche aufnehmen.
- `ma_analyse` soll langfristig keine verpflichtende Tkinter-Abhaengigkeit haben.
- Streamlit- und Tkinter-Code werden nicht in derselben Oberflaeche kombiniert.
- Berechnungslogik, Plotlogik und Excel-Reportlogik bleiben in Fachmodulen.
- UI-Seiten bauen Konfigurationen, rufen Services auf und zeigen Ergebnisse an.

## Geplante Analyse-Schnittstelle

Die folgende Schnittstelle ist Zielbild und wird in diesem Review nicht
implementiert.

```python
from ma_analyse.models import AnalysisConfig, AnalysisResult

def run_analysis(config: AnalysisConfig) -> AnalysisResult:
    ...
```

`AnalysisConfig` soll Eingabeordner, Ausgabeordner, Varianten, Raeume und
Report-Optionen enthalten. `AnalysisResult` soll Tabellen, Diagramme,
Reportpfade und Warnungen zurueckgeben.

Wichtig: Bestehende CLI-nahe Runner in `ma_analyse` werden dadurch nicht
automatisch ersetzt. Die Service-Fassade wird erst nach separater Analyse
geplant und implementiert.

## Nicht jetzt umsetzen

- `src/ma_analyse/gui/app.py` nicht verschieben.
- Bestehende Tkinter-GUI nicht auf Streamlit umbauen.
- Keine Tkinter-Bestandteile direkt in Streamlit-Seiten einbauen.
- Keine Importpfade in `ma_analyse` aendern.
- Keine Fachlogik in `ma_ui` duplizieren.
- Keine neuen Zielmodule ohne separaten Implementierungsplan anlegen.
