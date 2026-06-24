# ma_analyse Service-Schnittstelle

Stand: 2026-06-10

Aktueller Nachtrag 2026-06-24: Die Service-Schnittstelle bleibt fachlich
gueltig. Die Tkinter-Analyse liegt inzwischen unter
`ma_ui.tkinter_app.module_views.analyse`; `ma_analyse.gui` ist nur noch
Kompatibilitaet.

## Zweck

Dieses Dokument ist Phase 2 von P005. Es definiert den Zielvertrag fuer eine
UI-neutrale Service-Schicht in `ma_analyse`.

Status: Der erste Code-Slice ist umgesetzt. `src/ma_analyse/models.py` enthaelt
`AnalysisConfig` und `AnalysisResult`. `src/ma_analyse/services.py` enthaelt
`run_analysis(config)` als Fassade ueber bestehender Logik.

## Ziel

Die zentrale Oberflaeche `ma_ui` soll `ma_analyse` ohne Tkinter,
Streamlit-Importe im Fachmodul oder CLI-Argumentobjekte nutzen koennen.

Ziel-Schnittstelle:

```python
from ma_analyse.models import AnalysisConfig, AnalysisResult

def run_analysis(config: AnalysisConfig) -> AnalysisResult:
    ...
```

## Modelle

### AnalysisConfig

`AnalysisConfig` beschreibt einen fachlichen Analyseauftrag.

| Feld | Typ | Bedeutung |
|---|---|---|
| `steps` | `tuple[str, ...]` | Pipeline-Schritte, z. B. `prepare`, `plots`, `overview`, `analysis`, `analyze`, `heating`, `cooling`, `plot_template`, `all` |
| `input_dir` | `Path` | IDA-Importordner, Standard spaeter `data/ma_analyse/ida_imports` |
| `database_dir` | `Path` | aufbereitete Nutzdaten, Standard spaeter `data/ma_analyse/database` |
| `output_root` | `Path` | Ausgabewurzel, Standard spaeter `data/ma_analyse/output` |
| `run_id` | `str | None` | optionale Laufkennung |
| `variants` | `list[str] | None` | Varianten ohne `_rohdaten` oder `_nutzdaten` |
| `rooms` | `list[str]` | Raeume fuer Analyse und Plots |
| `debug` | `bool` | Debug-/Protokollausgabe aktivieren |
| `export_format` | `str` | Prepare-Export: `csv`, `excel` oder `both` |
| `comfort_output_type` | `str | None` | Comfort-Profil wie `plot`, `plot_overview`, `plot_analysis`, `plot_analysis_overview` |
| `load_kind` | `str | None` | `heating` oder `cooling` fuer Lastvergleiche |
| `view` | `str | None` | `bar`, `year`, `month`, `week` oder `day` |
| `month` | `str | None` | Monatsfilter |
| `week` | `int | None` | Kalenderwoche |
| `day` | `int | None` | Tag im Monat |
| `variant_mode` | `str | None` | `single` oder `compare` |
| `series_layout` | `str | None` | `separate` oder `combined` |
| `plot_template` | `str | None` | Plot-Template-Name |
| `plot_template_options` | `dict[str, object]` | Template-spezifische Optionen, Overlays und Achsen |

Defaults sollen aus `ma_analyse.core.config` und den bestehenden Settings-Modulen
kommen. Die UI soll keine Pfad- oder Plot-Defaults duplizieren.

### AnalysisResult

`AnalysisResult` beschreibt das Ergebnis eines Service-Aufrufs.

| Feld | Typ | Bedeutung |
|---|---|---|
| `success` | `bool` | Gesamtergebnis des Laufs |
| `steps` | `tuple[str, ...]` | tatsaechlich ausgefuehrte Schritte |
| `run_id` | `str | None` | verwendete Laufkennung |
| `created_files` | `list[Path]` | bekannte erzeugte Dateien, soweit ermittelbar |
| `summary_table` | `pd.DataFrame | None` | zentrale Ergebnistabelle, z. B. Comfort-Analyse |
| `detail_tables` | `dict[str, pd.DataFrame]` | optionale Detailtabellen |
| `warnings` | `list[str]` | fachliche Warnungen ohne Abbruch |
| `errors` | `list[str]` | Fehlertexte bei fehlgeschlagenem Lauf |
| `log_text` | `str` | gesammelte stdout-/stderr-Ausgabe aus bestehender Logik |

## Verhalten von run_analysis

Die erste Code-Umsetzung startet als Fassade ueber bestehender Logik, nicht als
Neuschreibung.

- `run_analysis(config)` validiert die Konfiguration.
- Die Funktion erzeugt intern das bisherige Runtime-Argumentobjekt, solange die
  bestehenden Funktionen dieses noch benoetigen.
- stdout/stderr werden gesammelt und in `AnalysisResult.log_text` abgelegt.
- Neue Dateien unter `database_dir` und `output_root` werden nach dem Lauf in
  `AnalysisResult.created_files` gelistet.
- `SystemExit` aus bestehender CLI-naher Logik wird abgefangen und in
  `AnalysisResult(success=False, errors=[...])` uebersetzt.
- Tkinter und Streamlit werden in dieser Schicht nicht importiert.
- Die Funktion zeigt keine Messageboxen an und ruft keine UI-Funktionen auf.
- Bestehende Funktionen werden nicht in diesem Schritt verschoben.

## Einbindung in ma_ui

`ma_ui/pages/analyse.py` soll nur:

- Nutzereingaben erfassen.
- `AnalysisConfig` bauen.
- `run_analysis(config)` aufrufen.
- `AnalysisResult` anzeigen.

Die UI soll keine PRN-Dateien lesen, keine Plotdaten berechnen und keine
Excel-Reports direkt erzeugen.

Ziel nach der P005-Verschaerfung: Die bestehende `pages/`-Analyse-Seite ist ein
Zwischenstand. Spaeter wird die Analysebedienung nach
`ma_ui/module_views/analyse_view.py` ueberfuehrt. Der Aufruf laeuft dann ueber
eine Workflow-Aktion, zum Beispiel:

```python
result = run_analysis(config)
```

oder auf Workflow-Ebene:

```python
result = run_analysis_action(config)
```

`ma_ui` baut nur die Konfiguration und zeigt `AnalysisResult` an.
`ma_workflow` koordiniert den Aufruf. `ma_analyse` fuehrt die fachliche Arbeit
aus.

## Nicht-Ziele des ersten Code-Slices

- Keine Aufteilung von `src/ma_analyse/gui/app.py`.
- Keine Verschiebung nach `ma_ui_legacy`.
- Keine fachlich vollstaendige Streamlit-Analyseoberflaeche.
- Keine Neuschreibung von Heating, Cooling oder Comfort.
- Keine Aenderung der bestehenden CLI.
- Keine Umbenennung der bestehenden `ma_ui/pages/`-Shell ohne eigenen
  Migrationsslice.
- Keine direkte Uebernahme von Tkinter-Widgets oder Tkinter-Dialogen in
  Streamlit.

## Akzeptanzkriterien fuer den ersten Code-Slice

- `ma_analyse.services.run_analysis(config)` ist importierbar.
- `AnalysisConfig` und `AnalysisResult` sind UI-neutral.
- `run_analysis(config)` funktioniert ohne Tkinter und ohne Streamlit.
- Bestehende CLI-Tests bleiben gruen.
- Ein einfacher Service-Test kann mindestens einen bestehenden Schritt ueber die
  Fassade ausfuehren und ein `AnalysisResult` zurueckgeben.
